
from pyglet.gl import *
from euclid import Matrix4
from renderer import Pass

class Renderable:
	def __init__(self, drawable, shader, textures, render_pass=Pass.solid):
		self.drawable = drawable
		self.shader = shader
		self.textures = list(textures)
		self.render_pass = render_pass
	
	def update(self, camera, transform):
		pass
	
	def draw(self):
		self.drawable.draw()
