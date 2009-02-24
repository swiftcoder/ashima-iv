
from entity import *
from euclid import Vector3, Quaternion, Matrix4
from node import Node

from teams import *

class _AI:	
	def __init__(self):		
		self.Nodes = {}
		self.factories = {}
				
		World.add_handlers(self.on_update, self.on_add, self.on_remove)
		
	def on_add(self, entity):
		if entity.has('ai'):
			self.Nodes[entity] = self.factories[entity.ai](entity)

	def on_remove(self, entity):
		if entity in self.Nodes:
			entity.node.parent = None
			del self.Nodes[entity]
	
	def on_update(self, dt):
		for k, v in self.Nodes.iteritems():
			v.update(dt)

class AINode:
	def __init__(self, entity):
		if not entity.has('position'):
			entity.position = Vector3(0, 0, 0)
		if not entity.has('rotation'):
			entity.rotation = Quaternion()
		
		if not entity.has('extents'):
			entity.extents = Vector3()
		
		self.entity = entity
	
	def find_targets(self):
		pos = self.entity.position
		
		targets = []
		for p in Teams.not_in_team(self.entity.team):
			dist = abs(pos - p.position)
			targets.append( (dist, p) )
		
		targets.sort()
		return targets
	
	def update(self, dt):
		pass

AI = _AI()
del _AI
