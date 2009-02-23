
from entity import *
from euclid import Vector3, Quaternion, Matrix4
from node import Node
from renderer import Renderer

import new

class _Graphics:	
	def __init__(self):		
		self.Nodes = {}
		
		self.root = Node()		
		self.camera = None
		
		World.add_handlers(self.on_frame, self.on_add, self.on_remove)
	
	class GraphicsNode:
		def __init__(self, entity):
			if not entity.has('position'):
				entity.position = Vector3(0, 0, 0)
			if not entity.has('rotation'):
				entity.rotation = Quaternion()
			
			if not entity.has('radius'):
				entity.radius = 1.0
			
			if not entity.has('node'):
				entity.node = Node()
			
			entity.node.parent = Graphics.root
		
		def update(self, entity):
			entity.node.model = Matrix4.new_translate(*entity.position) * entity.rotation.get_matrix()
	
	def on_add(self, entity):
		if entity.has('graphics') and entity.graphics == True:
			self.Nodes[entity] = self.GraphicsNode(entity)

	def on_remove(self, entity):
		if entity in self.Nodes:
			entity.node.parent = None
			del self.Nodes[entity]
	
	def on_frame(self):
		if self.camera:
			for k, v in self.Nodes.iteritems():
				v.update(k)
			
			self.root.update(self.camera)			
			self.root.render(self.camera)
		
		Renderer.render_all()

Graphics = _Graphics()
del _Graphics
