
import pyglet
from pyglet.gl import *
from renderable import Renderable
from renderer import Pass

from resources import Resources
from entity import Entity, World
from graphics import Graphics
from node import Node

from random import random
from euclid import Vector3

class Particle(Structure):
	pass
Particle._fields_ = [
	('x', c_float),
	('y', c_float),
	('z', c_float),
	
	('vx', c_float),
	('vy', c_float),
	('vz', c_float),
	
	('life', c_float)
]
	
class Particles(Renderable):
	def __init__(self, capacity):
		Renderable.__init__(self, Resources.load_shader('data/shaders/particles.shader'), [Resources.load_texture('data/images/burst2.png')])
		
		self.render_pass = Pass.transparent
		
		self.capacity = capacity
		self.count = 0
		
		self.data = (Particle * capacity)()
		
		self.vbo = GLuint()
		glGenBuffers(1, byref(self.vbo))
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
		glBufferData(GL_ARRAY_BUFFER, sizeof(self.data), self.data, GL_STREAM_DRAW)
		glBindBuffer(GL_ARRAY_BUFFER, 0)
	
	def draw(self):
		glEnable(GL_POINT_SPRITE)
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		glDepthMask(GL_FALSE)
		
		glTexEnvi(GL_POINT_SPRITE_ARB, GL_COORD_REPLACE_ARB, GL_FALSE)
		
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
		
		glEnableClientState(GL_VERTEX_ARRAY)
		glVertexPointer(3, GL_FLOAT, sizeof(Particle), 0)
		
		glClientActiveTexture(GL_TEXTURE1)
		glEnableClientState(GL_TEXTURE_COORD_ARRAY)
		glTexCoordPointer(1, GL_FLOAT, sizeof(Particle), sizeof(c_float)*6)
		
		glDrawArrays(GL_POINTS, 0, self.count)

		glDisableClientState(GL_TEXTURE_COORD_ARRAY)
		glClientActiveTexture(GL_TEXTURE0)
		
		glDisableClientState(GL_VERTEX_ARRAY)
		
		glBindBuffer(GL_ARRAY_BUFFER, 0)
				
		glDepthMask(GL_TRUE)
		glDisable(GL_BLEND)
		glDisable(GL_POINT_SPRITE)
	
	def update_particles(self, dt):
		i = 0		
		while i < self.count:
			p = self.data[i]
			p.life -= dt
			if p.life < 0:
				self.count -= 1
				self.data[i] = self.data[self.count]
				continue
			
			p.x += p.vx*dt
			p.y += p.vy*dt
			p.z += p.vz*dt
			
			i += 1
		
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
		glBufferSubData(GL_ARRAY_BUFFER, 0, sizeof(self.data), self.data)
		glBindBuffer(GL_ARRAY_BUFFER, 0)
		
	def emit(self, position, velocity, life):
		if self.count < self.capacity:
			p = self.data[self.count]
			
			p.x, p.y, p.z = position
			p.vx, p.vy, p.vz = velocity			
			p.life = life
			
			self.count += 1

class Explosion:	
	def __init__(self, entity, count, force, life):
		self.entity = entity
		self.force = force
		
		self.emission = count
		self.count = count
		self.life = life
		
		self.rate = 1.0/self.emission
		self.last = 0.0
		
		self.particles = Particles(self.count)
		self.entity.node.renderables.append(self.particles)
		
		for i in range(self.count/2):
			vel = Vector3(random()*2 - 1, random()*2 - 1, random()*2 - 1).normalized()*self.force*random()
			self.particles.emit(Vector3(), vel, self.life)
		
		self.entity.add_handlers(self.on_remove)
		World.add_handlers(self.on_update)
	
	def on_remove(self, entity):
		World.remove_handlers(self.on_update)
	
	def on_update(self, dt):
		self.particles.update_particles(dt)
		
		vel = Vector3(random()*2 - 1, random()*2 - 1, random()*2 - 1).normalized()*self.force*random()
				
		time = dt + self.last
		#print time/self.rate
		while time > self.rate:
			time -= self.rate
			self.particles.emit(Vector3(), vel, self.life)
		self.last = time

def create_explosion(position, velocity, count, force, duration, life):
	e = Entity()
	
	e.graphics = True
	e.lifetime = duration+life
	
	e.node = Node()
	
	e.explosion = Explosion(e, count, force, life)
	
	e.position = position
	
	return e
