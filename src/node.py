
import math
from copy import copy

from pyglet.gl import *
from euclid import Matrix4, Vector3, Point3
from renderer import Renderer

class Node(object):
	def __init__(self, parent=None):
		self.model = Matrix4()
		self.transform = Matrix4()
		
		self.renderables = []
		
		self.children = []
		self._parent = None
		
		self.parent = parent
	
	def _set_parent(self, parent):
		if self._parent:
			self._parent.children.remove(self)
		
		self._parent = parent
		
		if self._parent:
			self._parent.children.append(self)
	
	def _get_parent(self):
		return self._parent
	
	parent = property(_get_parent, _set_parent)
	
	def update(self, camera):
		self._update_matrices()
		self._update_children(camera)
		
	def _update_matrices(self):
		if self.parent:
			self.transform = self.parent.transform * self.model
		else:
			self.transform = copy(self.model)
	
	def _update_children(self, camera):
		for r in self.renderables:
			r.update(camera, self.transform)
		
		for c in self.children:
			c.update(camera)
	
	def render(self, camera):
		for r in self.renderables:
			Renderer.render(camera, self.transform, r, r.render_pass)
		
		for c in self.children:
			c.render(camera)

class BillboardNode(Node):
	def render(self, camera):
		m, v = self.transform, camera.view
		m.a, m.b, m.c = v.a, v.e, v.i
		m.e, m.f, m.g = v.b, v.f, v.j
		m.i, m.j, m.k = v.c, v.g, v.k
		
		Node.render(self, camera)

class ZAxisBillboardNode(Node):
	def render(self, camera):
		'''m, v = self.transform, camera.view
		m.a, m.b, m.c = v.a, v.e, 0
		m.e, m.f, m.g = v.b, v.f, 0
		m.i, m.j, m.k = 0,   0,   1'''
		
		cam = camera.view*Point3() - self.transform*Point3()
		z = self.transform*Vector3(0, 0, 1)
		y = cam.cross(z)
		self.transform = Matrix4.new_rotate_triple_axis(cam, y, z)
		
		Node.render(self, camera)

class SkyNode(Node):	
	def render(self, camera):
		m = self.transform
		
		m.a, m.b, m.c = 1, 0, 0
		m.e, m.f, m.g = 0, 1, 0
		m.i, m.j, m.k = 0, 0, 1
		
		Node.render(self, camera)

class IntervalNode(Node):
	def __init__(self, interval=10, parent=None):
		Node.__init__(self, parent)
		
		self.interval = interval
	
	def render(self, camera):
		m = self.transform
		
		m.a, m.b, m.c = 1, 0, 0
		m.e, m.f, m.g = 0, 1, 0
		m.i, m.j, m.k = 0, 0, 1
		
		m.d -= math.fmod(m.d, self.interval)
		m.h -= math.fmod(m.h, self.interval)
		m.l -= math.fmod(m.l, self.interval)
		
		Node.render(self, camera)
