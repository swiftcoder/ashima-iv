
from euclid import Vector3, Quaternion

from ai import AI, AINode

from teams import *
import utility

import math

class TurretAI(AINode):
	def __init__(self, entity):
		AINode.__init__(self, entity)
		
		self.target = None
		self.last_acquire = 0.0
	
	def acquire_target(self):
		potential = self.find_targets()
		
		if len(potential):
			self.target = potential[0][2]
	
	def get_force(self, target):
		f = 0.1
		
		t = target.position + target.linear_velocity*f
		e = self.entity.position + self.entity.linear_velocity*f
		
		diff = t - e
		
		return diff
	
	def update(self, dt):		
		self.last_acquire += dt
		
		if not self.target or self.last_acquire > 0.1:
			self.acquire_target()
			self.last_acquire = 0.0
		
		force = self.get_force(self.target)
		
		dir = self.entity.rotation*Vector3(0, 0, 1)
		dot =  dir.dot(force.normalized())
		
		if abs(force) < 2500 and dot > 0.75:
			self.entity.fire_primary()
		
		diff = utility.rotation_to(dir, force)
		angle, axis = diff.get_angle_axis()
		
		self.entity.turn_towards( axis*angle )

def turret_ai_factory(entity):
	return TurretAI(entity)

AI.factories['turret'] = turret_ai_factory
