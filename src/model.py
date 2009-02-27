
import pyglet
from drawable import Drawable
from renderable import Renderable

import ode

class Model(Drawable):
	def __init__(self, file, physics):		
		self.trimesh = None
		
		self._load(file)
		self._load_physics(physics)
	
	def _load(self, fname):		
		f = open(fname,'rt')
		lines = f.readlines()
		f.close()
		
		words = []
		
		faces = 0
		
		vertArray = []
		texArray = []
		normArray = []
		
		vertices = []
		texcoords = []
		normals = []
		
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
					for n in range(2):
						texcoords.append(texArray[(int(ind[1])-1)*2 + n])
					for n in range(3):
						normals.append(normArray[(int(ind[2])-1)*3 + n])
				faces += 1
		
		self.vlist = pyglet.graphics.vertex_list( faces*3, ('v3f', vertices), ('n3f', normals), ('t2f', texcoords) )
		
	def _load_physics(self, fname):
		if not fname:
			return
		
		f = open(fname,'rt')
		lines = f.readlines()
		f.close()
		
		words = []
		
		faces = 0
		
		vertArray = []
		
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
						
			if words[0] == 'f':
				for w in words[1:]:
					ind = w.split('/')
					pverts.append([vertArray[(int(ind[0])-1)*3 + n] for n in range(3)])
				faces += 1
		
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
			physics = (data['collision hull'] if 'collision hull' in data else '')
			
			p = Renderable( Class(data['model'], physics), Resources.load_shader(data['shader']), [Resources.load_texture(t) for t in data['textures']])
			return p
		
		return None
