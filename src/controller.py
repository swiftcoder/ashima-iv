
from window import Window
from entity import *

from entity import World

import pyglet
from pyglet.window import key

from copy import copy

import factories

class Controller:
	def __init__(self, e):
		self.e = e
				
		self.keymap = key.KeyStateHandler()

		Window.push_handlers(self.keymap)
		Window.push_handlers(self.on_key_press, self.on_key_release)
		World.add_handlers(self.on_update)
	
	def on_update(self, dt):
		if self.keymap[key.W]:
			self.e.throttle = 1.0
		elif self.keymap[key.S]:
			self.e.throttle = 0.0
		else:
			self.e.throttle = 0.5
		
		if self.keymap[key.LEFT]:
			self.e.yaw_left()
		elif self.keymap[key.RIGHT]:
			self.e.yaw_right()
		
		if self.keymap[key.UP]:
			self.e.pitch_up()
		elif self.keymap[key.DOWN]:
			self.e.pitch_down()
		
		if self.keymap[key.A]:
			self.e.roll_left()
		elif self.keymap[key.D]:
			self.e.roll_right()
		
		if self.keymap[key.SPACE]:
			self.e.fire_primary()
		if self.keymap[key.LSHIFT]:
			self.e.fire_secondary()
		
		if self.keymap[key.P]:
			print 'pos: ', self.e.position
	
	def on_key_press(self, k, mods):
		pass
	
	def on_key_release(self, k, mods):
		pass
