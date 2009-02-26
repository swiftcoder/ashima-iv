
from euclid import Vector3, Quaternion

from ai import AI, AINode

from teams import *
import utility

import math

def predicate(a, b):
	return cmp(a[1], b[1])

class MissileAI(AINode):
	def __init__(self, entity):
		AINode.__init__(self, entity)
		
		self.target = None
	
	def acquire_target(self):
		potential = self.find_targets()
		
		if len(potential):
			potential.sort(predicate)
			self.target = potential[0][2]
			#print 'target aquired: ', self.target.name
	
	def get_force(self, target, repulse=True):
		#v = abs(self.entity.linear_velocity + target.linear_velocity)
		#f = abs(self.entity.linear_velocity)/self.entity.max_acceleration*self.entity.mass
		f = 1.0
		
		t = target.position + target.linear_velocity*f
		e = self.entity.position + self.entity.linear_velocity*f
		
		diff = t - e
		l = abs(diff)
		dir = diff/l
				
		if repulse:
			extents = utility.vector_abs(dir).dot(target.extents)
			d = (l - 2*extents) / 10
			return -diff/math.pow(d, 5)
		return 10*diff/l
	
	def update(self, dt):
		force = Vector3()
				
		if not self.target:
			self.acquire_target()
		
		force += self.get_force(self.target, False)
		
		avoid = Teams.all()
		for a in avoid:
			if not a in [self.entity, self.target]:
				force += self.get_force(a)
		
		dir = self.entity.rotation*Vector3(0, 0, 1)
		
		diff = utility.rotation_to(dir, force)
		angle, axis = diff.get_angle_axis()
		
		self.entity.turn_towards( axis*angle )

def missile_ai_factory(entity):
	return MissileAI(entity)

AI.factories['missile'] = missile_ai_factory
