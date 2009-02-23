
import pyglet
from renderable import Renderable

import ode

class Model(Renderable):
	def __init__(self, shader, textures, file, physics=True):
		Renderable.__init__(self, shader, textures)
		
		self.trimesh = None
		
		self._load(file, physics)
	
	def _load(self, fname, physics):		
		f = open(fname,'rt')
		lines = f.readlines()
		f.close()
		
		words = []
		
		faces = 0
		start = 0
				
		vertArray = []
		texArray = []
		normArray = []
		
		vertices = []
		texcoords = []
		normals = []
		
		if physics:
			pverts = []

		for line in lines:
			words = line.split()
			
			if len(words) < 1:
				continue
			
			if words[0] == 'v':
				x = float(words[1])
				y = float(words[2])
				z = float(words[3])
				vertArray += [x,y,z]
			
			if words[0] == 'vt':
				u = float(words[1])
				v = float(words[2])
				texArray += [u,v]
			
			if words[0] == 'vn':
				x = float(words[1])
				y = float(words[2])
				z = float(words[3])
				normArray += [x,y,z]
			
			if words[0] == 'f':
				for w in words[1:]:
					ind = w.split('/')
					for n in range(3):
						vertices.append(vertArray[(int(ind[0])-1)*3 + n])
					if physics:
						pverts.append([vertArray[(int(ind[0])-1)*3 + n] for n in range(3)])
					for n in range(2):
						texcoords.append(texArray[(int(ind[1])-1)*2 + n])
					for n in range(3):
						normals.append(normArray[(int(ind[2])-1)*3 + n])
				faces += 1
		
		self.vlist = pyglet.graphics.vertex_list( faces*3, ('v3f', vertices), ('n3f', normals), ('t2f', texcoords) )
		
		if physics:
			self.trimesh = ode.TriMeshData()
			self.trimesh.build(pverts, [(i+0, i+1, i+2) for i in range(0, faces*3, 3)])
	
	def draw(self):
		pyglet.gl.glColor4f(1, 1, 1, 1)
		
		self.vlist.draw(pyglet.gl.GL_TRIANGLES)
	
	@classmethod
	def load(Class, name):
		import demjson
		from resources import Resources
		
		f = pyglet.resource.file(name)		
		data = demjson.decode(f.read())
		f.close()
		
		if (data['version'] == 1):
			p = Class(Resources.load_shader(data['shader']), [Resources.load_texture(t) for t in data['textures']], data['model'])
			return p
		
		return None
