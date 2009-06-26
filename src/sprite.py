
from drawable import Drawable

import pyglet
from pyglet.gl import *

class Sprite(Drawable):
	def __init__(self, sx, sy, tint=[1,1,1,1]):
		self.tint = tint
		
		verts = [-sx,-sy, sx,-sy, sx,sy, -sx,sy]
		texcoords0 = [0,0, 1,0, 1,1, 0,1]
		
		indices = [0,1,2, 0,2,3]
		self.vlist = pyglet.graphics.vertex_list_indexed( len(verts)/2, indices, ('v2f', verts), ('t2f', texcoords0) )
	
	def draw(self):		
		glDepthMask(GL_FALSE)
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		
		glColor4f(*self.tint)
		
		self.vlist.draw(pyglet.gl.GL_TRIANGLES)
		
		glDisable(GL_BLEND)
		glDepthMask(GL_TRUE)
