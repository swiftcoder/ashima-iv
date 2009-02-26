
from entity import Entity, World
from resources import Resources

from lifetime import Lifetime

from node import Node, BillboardNode, ZAxisBillboardNode
from sprite import Sprite
from ribbon import Engine

from renderable import Renderable
from renderer import Pass

from particles import create_explosion

from euclid import Vector3, Quaternion

from copy import copy
import math

from random import random

def bullet_factory(position, rotation, velocity, team):
	e = Entity('bullet')
	
	e.graphics = True
	e.physics = True
	
	n = ZAxisBillboardNode()
	
	n2 = Node(n)
	n2.renderables.append( Renderable( Sprite(1.0, 2.0), Resources.load_shader('data/shaders/unlit.shader'), [Resources.load_texture('data/images/laser.png')], Pass.flares) )
	n2.model.rotate_axis(-math.pi/2, Vector3(1, 0, 0))
	
	e.node = n
	
	rot = Quaternion.new_rotate_axis(random()*math.pi/32.0, Vector3(random(), random(), random()))
	
	e.position = copy(position)
	e.rotation = copy(rotation) * rot
	
	e.linear_velocity = copy(velocity)
	
	e.throttle = 1.0
	
	e.max_acceleration = 2.5
	
	e.mass = 0.001 # 1 kg
	
	e.lifetime = 0.75
	
	e.remove_on_collide = True
	e.category_mask = 0x0
		
	return e

def missile_factory(position, rotation, velocity, team):
	e = Entity('missile')
	
	e.graphics = True
	e.physics = True
	e.ai = 'missile'
	
	n = Node()
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
	e.category_mask = 0x0
	
	e.engines = [Engine(e, Vector3(0, 0, -1), 1.0, [Resources.load_texture('data/images/trail_missile.png'), Resources.load_texture('data/images/burst.png')])]
	
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
