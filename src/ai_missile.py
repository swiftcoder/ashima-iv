
from euclid import Vector3, Quaternion

from ai import AI, AINode

from teams import *
import utility

import math

class MissileAI(AINode):
	def __init__(self, entity):
		AINode.__init__(self, entity)
		
		self.target = None
	
	def acquire_target(self):
		potential = self.find_targets()
		
		if len(potential):
			self.target = potential[0][1]
	
	def get_force(self, target, repulse=True):
		diff = target.position - self.entity.position
		l = abs(diff)
		dir = diff/l
		
		e = utility.vector_abs(dir).dot(target.extents)
		d = (l - e) / 10
		
		if repulse:
			return -diff/math.pow(d, 3)
		return diff/d
	
	def update(self, dt):
		force = Vector3()
				
		if not self.target:
			self.acquire_target()
		else:
			force += self.get_force(self.target, False)
		
		avoid = Teams.all()
		for a in avoid:
			if not a in [self.entity, self.target]:
				force += self.get_force(a)
		
		dir = self.entity.rotation*Vector3(0, 0, 1)
		
		diff = utility.rotation_to(dir, force.normalized())
		angle, axis = diff.get_angle_axis()
		
		self.entity.turn_towards( axis )

def missile_ai_factory(entity):
	return MissileAI(entity)

AI.factories['missile'] = missile_ai_factory
