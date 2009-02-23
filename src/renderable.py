
from pyglet.gl import *
from euclid import Matrix4
from renderer import Pass

class Renderable:
	def __init__(self, shader, textures):
		self.shader = shader
		self.textures = list(textures)
		self.render_pass = Pass.solid
	
	def update(self, camera, transform):
		pass
	
	def draw(self):
		print 'draw unimplemented'
