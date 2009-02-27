
from entity import *
from euclid import Vector3, Quaternion
from math import sin, cos, atan2, fabs, degrees

import new

import ode

class CollisionMask:
	team = 0x1
	weapon = 0x2
	turret = 0x4
	fighter = 0x8
	ship = 0x16
	
	all = 0xffffffff

class _Physics:
	def __init__(self):		
		self.Nodes = {}
		
		self.world = ode.World()
		
		self.world.setERP(0.2)
		self.world.setCFM(0.0001)
		
		self.world.setLinearDamping(0.1)
		self.world.setAngularDamping(0.1)
		
		self.space = ode.Space(1)
		self.contactgroup = ode.JointGroup()
		
		self.last_step = 0.0
		
		World.add_handlers(self.on_update, self.on_add, self.on_remove)
	
	class PhysicsNode:
		def __init__(self, entity, world, space):
			if not entity.has('position'):
				entity.position = Vector3()
			if not entity.has('rotation'):
				entity.rotation = Quaternion()
						
			if not entity.has('linear_velocity'):
				entity.linear_velocity = Vector3()
			if not entity.has('angular_velocity'):
				entity.angular_velocity = Quaternion()
			
			if not entity.has('throttle'):
				entity.throttle = 0.0
			
			if not entity.has('_yaw'):
				entity._yaw = 0.0
			if not entity.has('_pitch'):
				entity._pitch = 0.0
			if not entity.has('_roll'):
				entity._roll = 0.0
			
			if not entity.has('max_velocity'):
				entity.max_velocity = 0.0
			if not entity.has('min_acceleration'):
				entity.min_acceleration = 0.0
			if not entity.has('max_acceleration'):
				entity.max_acceleration = 0.0
			if not entity.has('turn_rate'):
				entity.turn_rate = 0.0
			
			if not entity.has('mass'):
				entity.mass = 1.0
			if not entity.has('extents'):
				entity.extents = Vector3(1, 1, 1)

			if not entity.has('category_mask'):
				entity.category_mask = 0xffffffff
			if not entity.has('collide_mask'):
				entity.collide_mask = 0xffffffff
			
			if not entity.has('remove_on_collide'):
				entity.remove_on_collide = False
			
			def yaw(self, dir):
				self._yaw = dir
			entity.yaw_left = new.instancemethod(lambda s: yaw(s,1), entity, Entity)
			entity.yaw_right = new.instancemethod(lambda s: yaw(s, -1), entity, Entity)
			
			def pitch(self, dir):
				self._pitch = dir
			entity.pitch_up = new.instancemethod(lambda s: pitch(s,-1), entity, Entity)
			entity.pitch_down = new.instancemethod(lambda s: pitch(s, 1), entity, Entity)
			
			def roll(self, dir):
				self._roll = dir
			entity.roll_left = new.instancemethod(lambda s: roll(s,-1), entity, Entity)
			entity.roll_right = new.instancemethod(lambda s: roll(s, 1), entity, Entity)
			
			def turn_towards(self, dir):
				Physics.Nodes[self].body.addTorque(dir*entity.turn_rate)
			entity.turn_towards = new.instancemethod(turn_towards, entity, Entity)
				
			def set_pos(self, pos):
				self.position = pos			
			entity.warp = new.instancemethod(set_pos, entity, Entity)
			
			self.body = ode.Body(world)
			
			self.body.entity = entity
			
			M = ode.Mass()
			M.setBoxTotal(entity.mass, *entity.extents)
			self.body.setMass(M)
			
			if entity.has('model'):
				self.geom = ode.GeomTriMesh(entity.model.drawable.trimesh, space)
			else:
				self.geom = ode.GeomBox(space, entity.extents)
			self.geom.setBody(self.body)
			
			self.geom.setCategoryBits(entity.category_mask)
			self.geom.setCollideBits(entity.collide_mask)
			
			self.body.setPosition(entity.position)
			self.body.setLinearVel(entity.linear_velocity)
			
			angle, axis = entity.angular_velocity.get_angle_axis()
			self.body.setAngularVel(axis*angle)
			
			m = entity.rotation.get_matrix()
			self.body.setRotation([m.a, m.b, m.c, m.e, m.f, m.g, m.i, m.j, m.k])
		
		def update(self, entity):			
			entity.position = Vector3(*self.body.getPosition())
			entity.rotation = Quaternion(*self.body.getQuaternion())
			
			linear = self.body.getLinearVel()
			entity.linear_velocity = Vector3(*linear)
			
			angular = Vector3(*self.body.getLinearVel())
			entity.angular_velocity = Quaternion.new_rotate_axis(abs(angular), angular)
			
			thrust = entity.min_acceleration + entity.throttle*(entity.max_acceleration - entity.min_acceleration)
			self.body.addRelForce(Vector3(0, 0, 1)*thrust)
			
			self.body.addRelTorque(Vector3(entity._pitch, entity._yaw, entity._roll)*entity.turn_rate)
			
			entity._yaw, entity._pitch, entity._roll = 0, 0, 0
			entity._thrust = 0
		
	def on_add(self, entity):
		if entity.has('physics') and entity.physics == True:
			self.Nodes[entity] = self.PhysicsNode(entity, self.world, self.space)
	
	def on_remove(self, entity):
		if entity in self.Nodes:
			del self.Nodes[entity]
	
	def collision_callback(self, args, geom1, geom2):
		# Check if the objects do collide
		contacts = ode.collide(geom1, geom2)
		
		if len(contacts):
			b1, b2 = geom1.getBody(), geom2.getBody()
			
			#print 'collision between', b1.entity.name, 'and', b2.entity.name, len(contacts), 'contacts'
			
			# Create contact joints
			world, contactgroup = args
			for c in contacts:
				c.setMu(1000.0)
				#c.setBounce(0.9)
				#c.setMode(ode.ContactBounce)
				j = ode.ContactJoint(world, contactgroup, c)
				j.attach(b1, b2)
			
			if b1.entity.has('health') and b1.entity.health:
				b1.entity.deal_damage(b2.entity)
			if b2.entity.has('health') and b2.entity.health:
				b2.entity.deal_damage(b1.entity)
	
	def on_update(self, dt):		
		for k, v in self.Nodes.iteritems():
			v.update(k)
		
		step_size = 1.0/60.0
		dt += self.last_step
		
		while dt >= step_size:
			self.space.collide((self.world, self.contactgroup), self.collision_callback)
			
			self.world.step(step_size)
			
			self.contactgroup.empty()
			
			dt -= step_size
		
		self.last_step = dt

Physics = _Physics()
del _Physics

class FixedJoint:
	def __init__(self, entity1, entity2):
		self.joint = ode.FixedJoint(Physics.world)
		self.joint.attach(Physics.Nodes[entity1].body, Physics.Nodes[entity2].body)
		self.joint.setFixed()

class BallJoint:
	def __init__(self, entity1, entity2, anchor):
		self.joint = ode.BallJoint(Physics.world)
		self.joint.attach(Physics.Nodes[entity1].body, Physics.Nodes[entity2].body)
		self.joint.setAnchor(anchor)

class UniversalJoint:
	def __init__(self, entity1, entity2, anchor, axis1, axis2):
		self.joint = ode.UniversalJoint(Physics.world)
		self.joint.attach(Physics.Nodes[entity1].body, Physics.Nodes[entity2].body)
		self.joint.setAnchor(anchor)
		self.joint.setAxis1(axis1)
		self.joint.setAxis2(axis2)

class Hinge2Joint:
	def __init__(self, entity1, entity2, anchor, axis1, axis2, limitLo, limitHi):
		self.joint = ode.Hinge2Joint(Physics.world)
		self.joint.attach(Physics.Nodes[entity1].body, Physics.Nodes[entity2].body)
		self.joint.setAnchor(anchor)
		self.joint.setAxis1(axis1)
		self.joint.setAxis2(axis2)
		self.joint.setParam(ode.ParamLoStop, limitLo)
		self.joint.setParam(ode.ParamHiStop, limitHi)
