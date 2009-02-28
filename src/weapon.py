
from entity import Entity, World
from resources import Resources

from lifetime import Lifetime

from node import Node, BillboardNode, ZAxisBillboardNode
from sprite import Sprite
from ribbon import RibbonTrail

from renderable import Renderable
from renderer import Pass

from particles import create_explosion

from euclid import Vector3, Quaternion

from copy import copy
import math

from random import random

from physics import CollisionMask

def bullet_factory(position, rotation, velocity, team):
	e = Entity('bullet')
	
	e.graphics = True
	e.physics = True
	
	e.health = True
	
	e.max_life = 1
	e.life = 1
	e.damage = 10
	
	n = ZAxisBillboardNode()
	
	n2 = Node(n)
	n2.renderables.append( Renderable( Sprite(2.0, 4.0), Resources.load_shader('data/shaders/unlit.shader'), [Resources.load_texture('data/images/laser.png')], Pass.flares) )
	n2.model.rotate_axis(-math.pi/2, Vector3(1, 0, 0))
	
	e.node = n
	
	rot = Quaternion.new_rotate_axis(random()*math.pi/256.0, Vector3(random(), random(), random()))
	
	e.position = copy(position)
	e.rotation = copy(rotation) * rot
	
	e.linear_velocity = copy(velocity)
	
	e.throttle = 1.0
	
	e.max_acceleration = 10.0
	
	e.mass = 0.001 # 1 kg
	
	e.lifetime = 0.75
	
	e.remove_on_collide = True
	
	e.category_mask = (CollisionMask.team & (team == 'blue')) | CollisionMask.weapon
	e.collide_mask = (CollisionMask.team & (team != 'blue'))
		
	@e.event
	def on_death(entity):
		e = create_explosion(entity.position, Vector3(), 40, 2.0, 0.0, 1.0)
		World.add(e)
		entity.remove_from_world = True
	
	return e

def missile_factory(position, rotation, velocity, team):
	e = Entity('missile')
	
	e.graphics = True
	e.physics = True
	e.ai = 'missile'
	
	e.health = True
	
	e.max_life = 1
	e.life = 1
	e.damage = 60
	
	n = BillboardNode()
	n.renderables.append( Renderable(Sprite(1, 1), Resources.load_shader('data/shaders/unlit.shader'), [Resources.load_texture('data/images/burst.png')]) )
	e.node = n
		
	e.position = copy(position)
	e.rotation = copy(rotation)
	
	e.linear_velocity = copy(velocity)
	
	e.throttle = 1.0
	
	e.max_acceleration = 80.0
	
	e.turn_rate = 2.5
	
	e.mass = 0.05 # 50 kg
	e.extents = Vector3(5.0, 5.0, 5.0)
	
	e.lifetime = 10.0
	
	e.remove_on_collide = True
	
	e.category_mask = (CollisionMask.team & (team == 'blue')) | CollisionMask.weapon
	e.collide_mask = (CollisionMask.team & (team != 'blue'))
	
	e.team = team
	e.team_no_reticule = True
	
	e.engines = [RibbonTrail(e, Vector3(0, 0, -1), Resources.load_texture('data/images/trail_missile.png'))]
	
	@e.event
	def on_death(entity):
		e = create_explosion(entity.position, Vector3(), 400, 5.0, 0.0, 1.0)
		World.add(e)
		entity.remove_from_world = True
	
	return e

class Weapon:
	def __init__(self, entity, factory=bullet_factory, reload_delay=0.25):
		self.entity = entity
		self.factory = factory
		self.reload_delay = reload_delay
		self.last_fire = 0.0
		
		World.add_handlers(self.on_update)
	
	def on_update(self, dt):
		self.last_fire -= dt
		
	def fire(self, offset=Vector3()):
		if self.last_fire <= 0.0:
			rot = self.entity.rotation
			pos = self.entity.position + rot*offset
			
			b = self.factory(pos, rot, self.entity.linear_velocity, self.entity.team)
			World.add(b)
			
			self.last_fire = self.reload_delay
