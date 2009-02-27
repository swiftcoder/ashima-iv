
from euclid import Vector3, Quaternion

from ai import AI, AINode

from teams import Teams
import utility

import math

class FighterAI(AINode):
	def __init__(self, entity):
		AINode.__init__(self, entity)
		
		self.target = None
		self.last_acquire = 0.0
	
	def acquire_target(self):
		potential = self.find_targets()
		
		if len(potential):
			self.target = potential[-1][2]
			self.last_acquire = 0.0
	
	def get_force(self, target, repulse=True):
		diff = target.position - self.entity.position
		l = abs(diff)
		dir = diff/l
				
		if repulse:
			e = utility.vector_abs(dir).dot(target.extents)
			d = (l - e) / 10
			return -diff/math.pow(d, 3)
		return 10*diff/l
	
	def update(self, dt):
		force = Vector3()
				
		if not self.target or self.last_acquire > 2.0:
			self.acquire_target()
		else:
			force += self.get_force(self.target, False)
		
		avoid = Teams.all()
		for a in avoid:
			if not a is self.entity:
				force += self.get_force(a)
		
		dir = self.entity.rotation*Vector3(0, 0, 1)
		
		dot = dir.dot( (self.target.position - self.entity.position).normalized() )
		if abs(force) < 250 and dot > 0.75:
			self.entity.fire_primary()
		
		diff = utility.rotation_to(dir, force.normalized())
		angle, axis = diff.get_angle_axis()
		
		self.entity.turn_towards( axis )
		
		self.last_acquire += dt

def fighter_ai_factory(entity):
	return FighterAI(entity)

AI.factories['fighter'] = fighter_ai_factory
