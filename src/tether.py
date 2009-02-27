
from entity import World
from physics import Physics

import pyglet
import ode

from euclid import Vector3, Quaternion, Matrix4

class Tether:
	
	def __init__(self, entity, target, follow_offset, look_offset, stiffness = 250.0):
		self.e, self.t, self.fo, self.lo = entity, target, follow_offset, look_offset
		self.stiffness = stiffness
		
		World.add_handlers(self.on_update)
	
	def on_update(self, dt):
		desired = self.t.position + self.t.rotation*self.fo
		stretch = desired - self.e.position
		force = self.stiffness*stretch
		
		node = Physics.Nodes[self.e]
		node.body.addForce(force)
		
		at = self.t.position + self.t.rotation*self.lo
		up = self.t.rotation * Vector3(0, 1, 0)
		
		m = Matrix4.new_look_at(self.e.position, at, up)
		self.e.rotation = Quaternion.new_rotate_matrix(m)
