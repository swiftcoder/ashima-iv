
from entity import Entity, World
from resources import Resources

from lifetime import Lifetime

from node import BillboardNode
from sprite import Sprite
from ribbon import Engine

from particles import create_explosion

from euclid import Vector3

from copy import copy
import math

def bullet_factory(position, rotation, velocity, team):
	e = Entity()
	
	e.graphics = True
	e.physics = True
	
	n = BillboardNode()
	n.renderables.append( Sprite(0.5, 0.5, Resources.load_shader('data/shaders/unlit.shader'), Resources.load_texture('data/images/particle.png')) )
	e.node = n
		
	e.position = position
		
	e.position = copy(position)
	e.rotation = copy(rotation)
	
	e.linear_velocity = copy(velocity)
	
	e.throttle = 1.0
	
	e.max_acceleration = 20.0
	
	e.mass = 0.001 # 1 kg
	e.damping = 0.995
	
	e.lifetime = 0.75
	e.remove_on_collide = True
	
	e.team = team
	
	return e

def missile_factory(position, rotation, velocity, team):
	e = Entity()
	
	e.graphics = True
	e.physics = True
	e.ai = 'missile'
	
	n = BillboardNode()
	n.renderables.append( Sprite(1, 1, Resources.load_shader('data/shaders/unlit.shader'), Resources.load_texture('data/images/burst.png')) )
	e.node = n
		
	e.position = copy(position)
	e.rotation = copy(rotation)
	
	e.linear_velocity = copy(velocity)
	
	e.throttle = 1.0
	
	e.min_acceleration = 20.0
	e.max_acceleration = 80.0
	
	e.turn_rate = 0.125
	
	e.mass = 0.05 # 50 kg
	e.damping = 0.995
	
	e.lifetime = 10.0
	e.remove_on_collide = True
	
	e.engines = [Engine(e, Vector3(0, 0, -1))]
	
	e.team = team
	
	def on_remove(entity):
		e = create_explosion(entity.position, Vector3(), 400, 5.0, 0.0, 1.0)
		World.add(e)
	
	e.add_handlers(on_remove)
	
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
