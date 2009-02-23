
import pyglet
from pyglet.gl import *
from ctypes import *
from euclid import Vector3, Matrix4

from node import Node

from utility import model_to_view_ortho_matrix

class Camera:
	def __init__(self, fovy, aspect, near, far):
		self.proj = Matrix4.new_perspective(fovy, aspect, near, far)
		self.view = Matrix4()

class CameraNode(Node):
	def __init__(self, camera):
		Node.__init__(self)
		self.camera = camera
	
	def update(self, camera):
		self._update_matrices()
		self.camera.view = model_to_view_ortho_matrix(self.transform)
		self._update_children(camera)
