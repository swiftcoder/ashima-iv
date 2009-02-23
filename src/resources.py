
import pyglet
from shader import Shader
from model import Model

class _Resources:
	_res = {}
	
	def load_texture(self, name):
		try:
			t = self._res[name]
		except KeyError:
			t = pyglet.resource.texture(name)
			self._res[name] = t
		return t
	
	def load_shader(self, name):
		try:
			s = self._res[name]
		except KeyError:
			s = Shader.load(name)
			self._res[name] = s
		return s
	
	def load_model(self, name):
		try:
			m = self._res[name]
		except KeyError:
			m = Model.load(name)
			self._res[name] = m
		return m

Resources = _Resources()
del _Resources
