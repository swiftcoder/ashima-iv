
from entity import World, Entity

class _Lifetime:
	def __init__(self):		
		self.nodes = []
				
		World.add_handlers(self.on_add, self.on_remove, self.on_update)
	
	def on_add(self, entity):
		if entity.has('lifetime'):
			self.nodes.append(entity)
	
	def add(self, entity):
		if not entity.has('lifetime'):
			entity.lifetime = 1.0
		
		self.nodes.append(entity)
	
	def on_remove(self, entity):
		if entity in self.nodes:
			self.nodes.remove(entity)
		
	def on_update(self, dt):
		for e in self.nodes:
			e.lifetime -= dt
			if e.lifetime < 0.0 and (not e.has('remove_from_world') or not e.remove_from_world):
				e.remove_from_world = True

Lifetime = _Lifetime()
del _Lifetime
