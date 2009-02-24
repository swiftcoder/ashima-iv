
from euclid import Vector3, Quaternion

from ai import AI, AINode

from teams import *
import utility

class MissileAI(AINode):
	def __init__(self, entity):
		AINode.__init__(self, entity)
		
		self.target = None
	
	def acquire_target(self):
		potential = self.find_targets()
		
		if len(potential):
			self.target = potential[0][1]
	
	def update(self, dt):
		if not self.target:
			self.acquire_target()
		else:
			dir = self.entity.rotation*Vector3(0, 0, -1)
						
			t = self.target.position
			m = self.entity.position
			desired = t - m
			
			diff = desired.normalized() - dir
			
			self.entity.turn_towards(diff)

def missile_ai_factory(entity):
	return MissileAI(entity)

AI.factories['missile'] = missile_ai_factory
