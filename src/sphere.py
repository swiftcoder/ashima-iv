
import pyglet

from math import pi, sin, cos, sqrt
from euclid import Vector3

class Sphere:
	def __init__(self, radius, steps):
		hStep = 2.0*pi/steps
		vStep = 2.0*pi/steps
		
		verts = []
		normals = []
		tangents = []
		texcoords = []
		
		for j in range(steps+1):
			for i in range(steps+1):
				r = sin(j*vStep)
				v = Vector3(r*cos(i*hStep), cos(j*vStep), r*sin(i*hStep))
				
				v.normalize();
				normals += v[:]
				
				t = v.cross(Vector3(0.0,1.0,0.0))
				tangents += t[:]
				
				v *= radius;
				verts += v[:]
				
				texcoords += [i/float(steps), cos(j*vStep)*0.5 + 0.5]
		
		indices = []
		for j in range(steps):
			for i in range(steps+1):
				ip = (0 if i == steps else i+1)
				indices.append(j*steps + i)
				indices.append(j*steps + ip)
				indices.append((j+1)*steps + ip)
				
				indices.append(j*steps + i);
				indices.append((j+1)*steps + ip)
				indices.append((j+1)*steps + i)
		
		self.vlist = pyglet.graphics.vertex_list_indexed( len(verts)/3, indices, ('v3f', verts), ('n3f', normals), ('t2f', texcoords), ('0g3f', tangents) )
	
	def draw(self):
		self.vlist.draw(pyglet.gl.GL_TRIANGLES)
