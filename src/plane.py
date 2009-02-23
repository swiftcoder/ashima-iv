
import pyglet

class Plane:
	def __init__(self, size):
		
		verts = [-size,0,-size, size,0,-size, size,0,size, -size,0,size]
		normals = [0,1,0]*4
		tangents = [1,0,0]*4
		texcoords = [0,0, 1,0, 1,1, 0,1]
				
		indices = [0,2,1, 0,3,2]
		
		self.vlist = pyglet.graphics.vertex_list_indexed( 4, indices, ('v3f', verts), ('n3f', normals), ('t2f', texcoords), ('0g3f', tangents) )
	
	def draw(self):
		self.vlist.draw(pyglet.gl.GL_TRIANGLES)
