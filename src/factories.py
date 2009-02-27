
from entity import *

from resources import Resources
from node import Node, BillboardNode
from model import Model
from camera import CameraNode
from tether import Tether

from physics import FixedJoint, BallJoint, UniversalJoint, Hinge2Joint, CollisionMask

from sprite import Sprite

from ribbon import RibbonTrail, EngineFlare

from weapon import *

import math
import new

from euclid import Vector3

def create_camera(camera):
	e = Entity()
	
	e.graphics = True
	e.physics = True
	
	n = CameraNode(camera)
	e.node = n
	
	e.mass = 5.0
	
	return e

def cross_hairs(ship):
	r = Renderable(Sprite(10, 10), Resources.load_shader('data/shaders/unlit.shader'), [Resources.load_texture('data/images/aim.png')], Pass.overlay)
	
	n = BillboardNode(ship.node)
	n.renderables.append(r)
	n.model.translate(0, 0, 50)
	
	return n

def aim_assist(camera):
	r = Renderable(Sprite(0.25, 0.25), Resources.load_shader('data/shaders/unlit.shader'), [Resources.load_texture('data/images/lock.png')], Pass.overlay)
	
	n = BillboardNode(camera.node)
	n.renderables.append(r)
	n.model.translate(0, 0, -10)
	
	return n

def engine(entity, offset, size, trail=True):
	if trail:
		RibbonTrail(entity, offset, Resources.load_texture('data/images/trail_ship.png'))
	EngineFlare(entity, offset, size, Resources.load_texture('data/images/flare.png'))

def create_anaconda(position, team, ai=True):
	e = Entity('anaconda')
	
	e.graphics = True
	e.physics = True
	e.team = team
	
	if ai:
		e.ai = 'fighter'
	
	e.health = True
	
	e.max_life = 100
	e.life = 100
	e.damage = 1
	e.recharge_rate = 2
	
	e.position = position
	
	e.model = Resources.load_model('data/models/anaconda.model')
	
	n = Node()
	n.renderables.append( e.model )
	e.node = n
		
	e.throttle = 0.5
	
	e.min_acceleration = 450.0 #4000.0
	e.max_acceleration = 3800.0 #8000.0
	e.max_velocity = 4.0
	
	e.turn_rate = 150.0
	
	e.mass = 5.0
	e.extents = Vector3(8, 3, 10)
	
	e.engines = [engine(e, Vector3(0, 0.85, -5), 1.0)]

	e.primary_weapon = Weapon(e, bullet_factory, 0.25)
	e.secondary_weapon = Weapon(e, missile_factory, 1.0)
		
	e.fire_primary = new.instancemethod(lambda s: s.primary_weapon.fire(Vector3(0, 0, 20)), e, Entity)
	e.fire_secondary = new.instancemethod(lambda s: s.secondary_weapon.fire(Vector3(0, 0, 20)), e, Entity)

	e.category_mask = (CollisionMask.team & (team == 'blue')) | CollisionMask.fighter
	e.collide_mask = CollisionMask.all
		
	@e.event
	def on_death(self):
		e = create_explosion(self.position, Vector3(), 1000, 10.0, 0.0, 2.0)
		World.add(e)
		self.remove_from_world = True
		print 'anaconda killed'
	
	return e

def create_viper(position, team, ai=True):
	e = Entity('viper')
	
	e.graphics = True
	e.physics = True
	e.team = team
	
	if ai:
		e.ai = 'fighter'
	
	e.health = True
	
	e.max_life = 250
	e.life = 250
	e.damage = 1
	e.recharge_rate = 4
	
	e.position = position
	
	e.model = Resources.load_model('data/models/viper.model')
	
	n = Node()
	n.renderables.append( e.model )
	e.node = n
		
	e.throttle = 0.5
	
	e.min_acceleration = 750.0 #4000.0
	e.max_acceleration = 6500.0 #8000.0
	e.max_velocity = 4.0
	
	e.turn_rate = 800.0
	
	e.mass = 7.5
	e.extents = Vector3(8, 6, 10)
	
	e.engines = [engine(e, Vector3(-1.3, 1.0, -6), 1.5), engine(e, Vector3(1.3, 1.0, -6), 1.5)]

	e.primary_weapon = Weapon(e, bullet_factory, 0.25)
	e.secondary_weapon = Weapon(e, missile_factory, 1.0)
		
	e.fire_primary = new.instancemethod(lambda s: s.primary_weapon.fire(Vector3(0, 0, 15)), e, Entity)
	e.fire_secondary = new.instancemethod(lambda s: s.secondary_weapon.fire(Vector3(0, 0, 15)), e, Entity)
	
	e.category_mask = (CollisionMask.team & (team == 'blue')) | CollisionMask.fighter
	e.collide_mask = CollisionMask.all
	
	@e.event
	def on_death(self):
		e = create_explosion(self.position, Vector3(), 1500, 15.0, 0.0, 2.0)
		World.add(e)
		self.remove_from_world = True
		print 'viper killed'
	
	return e

def create_turret(parent, offset, team):
	e = Entity('turret')
	
	e.graphics = True
	e.physics = True
	e.ai = 'turret'
	e.team = team
	
	e.health = True
	
	e.max_life = 80
	e.life = 80
	e.damage = 1
	
	e.model = Resources.load_model('data/models/turret.model')
	
	n = Node()
	n.renderables.append( e.model )
	e.node = n
	
	e.position = parent.position + offset
	
	e.turn_rate = 4200.0
	e.mass = 10.0
	e.extents = Vector3(20, 20, 20)
	
	@e.event
	def on_add(entity):
		e.j = BallJoint(e, parent, parent.position+offset)
	
	e.primary_weapon = Weapon(e, bullet_factory, 0.25)
	e.fire_primary = new.instancemethod(lambda s: s.primary_weapon.fire(Vector3(0, 0, 15)), e, Entity)
	
	e.category_mask = CollisionMask.turret
	e.collide_mask = CollisionMask.all ^ CollisionMask.ship
	
	@e.event
	def on_death(self):
		e = create_explosion(self.position, Vector3(), 1000, 14.0, 0.0, 2.0)
		World.add(e)
		self.remove_from_world = True
		print 'turret killed'
	
	return e

def create_hammerfall(position, team):
	e = Entity('hammerfall')
	
	e.graphics = True
	e.physics = True
	e.team = team
	
	e.health = True
	
	e.max_life = 1500
	e.life = 1500
	e.damage = 1
	
	e.position = position
	
	e.model = Resources.load_model('data/models/hammerfall.model')
	
	n = Node()
	n.renderables.append( e.model )
	e.node = n
	
	e.throttle = 0.5
	
	e.min_acceleration = 4000000.0 #4000.0
	e.max_acceleration = 8000000.0 #8000.0
	
	e.turn_rate = 100.0
	
	e.mass = 40000.0
	e.extents = Vector3(800, 400, 2000)
	
	e.engines = [engine(e, Vector3(0, -20, -830), 70.0, False), engine(e, Vector3(190, -20, -830), 70.0, False), engine(e, Vector3(-190, -20, -830), 70.0, False)]
	
	e.turrets = [create_turret(e, Vector3(180, 70, -550), team), create_turret(e, Vector3(-180, 70, -550), team)]

	e.category_mask = (CollisionMask.team & (team == 'blue')) | CollisionMask.ship
	e.collide_mask = CollisionMask.all ^ CollisionMask.turret
	
	@e.event
	def on_add(self):
		for t in self.turrets:
			World.add(t)
	
	@e.event
	def on_death(self):
		e = create_explosion(self.position, Vector3(), 2000, 200.0, 0.0, 5.0)
		World.add(e)
		
		self.damage = 10000
		for t in self.turrets:
			t.deal_damage(self)
		self.damage = 1
		
		@e.event
		def on_remove(e):
			self.remove_from_world = True
			print 'hammerfall killed'
	
	return e
