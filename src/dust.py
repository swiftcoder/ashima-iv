
import pyglet
from pyglet.gl import *
from renderable import Renderable

from renderer import Pass

from resources import Resources

from random import random
from euclid import Vector3

class Dust(Renderable):
	def __init__(self, blocks, size, density):
		Renderable.__init__(self, Resources.load_shader('data/shaders/dust.shader'), [])
		
		self.render_pass = Pass.sky
		
		block = []
		for d in range(density):
			v = Vector3(random(), random(), random())*size
			block.append(v)
		
		verts = []
		for i in range(-blocks/2, blocks/2):
			for j in range(-blocks/2, blocks/2):
				for k in range(-blocks/2, blocks/2):
					u = Vector3(i, j, k)*size
					for b in block:
						v = u + b
						verts += v.x, v.y, v.z
		
		self.vlist = pyglet.graphics.vertex_list( len(verts)/3, ('v3f', verts) )
	
	def draw(self):
		#glEnable(GL_FOG)
		#glFogfv(GL_FOG_COLOR, (GLfloat * 4)(0.0, 0.0, 0.0, 0.0))
		#glFogf(GL_FOG_START, 5.0)
		#glFogf(GL_FOG_END, 10.0)
		self.vlist.draw(pyglet.gl.GL_POINTS)
		#glDisable(GL_FOG)
