
import pyglet
from pyglet.gl import *
from renderable import Renderable
from renderer import Pass

class Sprite(Renderable):
	def __init__(self, sx, sy, shader, texture):
		Renderable.__init__(self, shader, [texture])
		
		self.render_pass = Pass.overlay
		
		verts = [-sx,-sy, sx,-sy, sx,sy, -sx,sy]
		texcoords0 = [0,0, 1,0, 1,1, 0,1]
		
		indices = [0,1,2, 0,2,3]
		self.vlist = pyglet.graphics.vertex_list_indexed( len(verts)/2, indices, ('v2f', verts), ('0t2f', texcoords0) )
		
	def draw(self):		
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		
		self.vlist.draw(pyglet.gl.GL_TRIANGLES)
		
		glDisable(GL_BLEND)
