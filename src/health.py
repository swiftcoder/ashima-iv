
from entity import *

import new

class _Health:	
	def __init__(self):		
		self.Nodes = {}
		
		World.add_handlers(self.on_update, self.on_add)
	
	class HealthNode:
		def __init__(self, entity):
			if not entity.has('max_life'):
				entity.max_life = 100.0
			if not entity.has('recharge_rate'):
				entity.recharge_rate = 10.0
			if not entity.has('recharge_delay'):
				entity.recharge_delay = 3.0
			
			if not entity.has('damage'):
				entity.damage = 0.0
			
			if not entity.has('life'):
				entity.life = entity.max_life
			
			if not entity.has('_last_damaged'):
				entity._last_damaged = entity.recharge_delay + 1.0
			if not entity.has('_last_damaged_by'):
				entity._last_damage_by = None
			if not entity.has('_dead'):
				entity._dead = False
			
			def deal_damage(self, entity):
				if self._last_damage_by != entity:
					self.life -= entity.damage
					self._last_dammaged = 0.0
					self._last_damage_by = entity
					
					print self.name, '(', self.life, ') damages', entity.name, '(', entity.life, ')'
					
					if self.life <= 0.0 and not self._dead:
						self._dead = True
						self.perform_death()
			entity.deal_damage = new.instancemethod(deal_damage, entity, Entity)
		
		def update(self, entity, dt):
			if entity.life < entity.max_life and entity._last_damaged > entity.recharge_delay:
				entity.life = min(entity.max_life, entity.life + entity.recharge_rate*dt)
			else:
				entity._last_damaged += dt
	
	def on_add(self, entity):
		if entity.has('health') and entity.health == True:
			self.Nodes[entity] = self.HealthNode(entity)
			entity.add_handlers(self.on_remove)
	
	def on_remove(self, entity):
		del self.Nodes[entity]
	
	def on_update(self, dt):
		for k, v in self.Nodes.iteritems():
			v.update(k, dt)

Health = _Health()
del _Health
