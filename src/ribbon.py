
import pyglet
from pyglet.gl import *
from drawable import Drawable
from renderable import Renderable
from renderer import Pass

from resources import Resources
from entity import World
from graphics import Graphics

from random import random
from euclid import Vector3

from node import BillboardNode
from sprite import Sprite

class Particle(Structure):
	pass
Particle._fields_ = [
	('x', c_float),
	('y', c_float),
	('z', c_float),
	
	('nx', c_float),
	('ny', c_float),
	('nz', c_float),
	
	('s', c_float),
	('life', c_float)
]

class Dummy:
	def __init__(self, pos, norm):
		self.pos = pos
		self.norm = norm
		self.life = 1.0

class Ribbon(Drawable):
	def __init__(self, capacity, decay, cycles):
		self.capacity = capacity
		
		self.decay = decay
		self.cycles = cycles
		self.cycle = 0
		
		self.dummy = []
		self.data = (Particle * (capacity*2))()
		
		self.vbo = GLuint()
		glGenBuffers(1, byref(self.vbo))
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
		glBufferData(GL_ARRAY_BUFFER, sizeof(self.data), self.data, GL_STREAM_DRAW)
		glBindBuffer(GL_ARRAY_BUFFER, 0)
	
	def draw(self):
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		glDepthMask(GL_FALSE)
		
		glEnableClientState(GL_VERTEX_ARRAY);
		glEnableClientState(GL_NORMAL_ARRAY);
		glEnableClientState(GL_TEXTURE_COORD_ARRAY);
		
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
		
		glVertexPointer(3, GL_FLOAT, sizeof(Particle), 0);
		glNormalPointer(GL_FLOAT, sizeof(Particle), sizeof(GLfloat)*3);
		glTexCoordPointer(2, GL_FLOAT, sizeof(Particle), sizeof(GLfloat)*6);
		
		glDrawArrays(GL_TRIANGLE_STRIP, 0, len(self.dummy)*2);
		
		glBindBuffer(GL_ARRAY_BUFFER, 0)	
		
		glDisableClientState(GL_TEXTURE_COORD_ARRAY);
		glDisableClientState(GL_NORMAL_ARRAY);
		glDisableClientState(GL_VERTEX_ARRAY);
		
		glDepthMask(GL_TRUE)
		glDisable(GL_BLEND)
	
	def update_ribbon(self, dt, position, rotation):
		if len(self.dummy) == 0:
			d = Dummy(position, rotation*Vector3(0,0,-1))
		else:
			d = Dummy(position, self.dummy[-1].pos - position)
		
		if self.cycle <= 0:
			self.cycle = self.cycles
			
			self.dummy.append( d )
			
			if len(self.dummy) >= self.capacity:
				self.dummy.pop(0)
		else:
			self.cycle -= 1
			
			self.dummy[-1] = d
		
		for i, p in zip(range(len(self.dummy)), self.dummy):
			d = self.data[i*2]
			d.x, d.y, d.z = p.pos
			d.nx, d.ny, d.nz = p.norm
			d.s = 0.0
			d.life =  p.life
			
			d = self.data[i*2 + 1]
			d.x, d.y, d.z = p.pos
			d.nx, d.ny, d.nz = -p.norm
			d.s = 1.0
			d.life = p.life
			
			p.life -= dt*self.decay
		
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
		glBufferSubData(GL_ARRAY_BUFFER, 0, sizeof(self.data), self.data)
		glBindBuffer(GL_ARRAY_BUFFER, 0)

class RibbonTrail:	
	def __init__(self, ship, offset, texture):
		self.ship = ship
		self.offset = offset
				
		self.count = 50
				
		self.ribbon = Ribbon(self.count, 0.5, 2)
		self.r = Renderable(self.ribbon, Resources.load_shader('data/shaders/ribbon.shader'), [texture], Pass.trails)
		
		Graphics.root.renderables.append( self.r )
				
		self.ship.add_handlers(self.on_remove)
		World.add_handlers(self.on_update)
	
	def on_remove(self, ship):
			Graphics.root.renderables.remove(self.r)
			World.remove_handlers(self.on_update)
	
	def on_update(self, dt):
		pos = self.ship.position + self.ship.rotation*self.offset
		rot = self.ship.rotation
		
		self.ribbon.update_ribbon(dt, pos, rot)

class EngineFlare:
	def __init__(self, ship, offset, size, texture):
		
		self.sprite = BillboardNode(ship.node)
		self.sprite.model.translate(*offset)
		self.sprite.renderables.append( Renderable( Sprite(size, size), Resources.load_shader('data/shaders/unlit.shader'), [texture], Pass.flares) )
		
		ship.add_handlers(self.on_remove)
	
	def on_remove(self, ship):
			self.sprite.parent = None
