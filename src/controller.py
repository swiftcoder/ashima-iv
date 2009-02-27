
from window import Window
from entity import *

from entity import World

import pyglet
from pyglet.window import key, mouse

from copy import copy

import math

from euclid import Vector2

class Controller:
	def __init__(self, e):
		self.e = e
		
		self.left_mouse = False
		self.right_mouse = False
		
		self.m = Vector2()
		
		self.keymap = key.KeyStateHandler()
		Window.push_handlers(self.keymap)
		
		Window.push_handlers(self.on_key_press, self.on_key_release, self.on_mouse_press, self.on_mouse_release, self.on_mouse_motion, self.on_mouse_drag)
		
		World.add_handlers(self.on_update)
	
	def on_update(self, dt):
		if self.keymap[key.W]:
			self.e.throttle = 1.0
		elif self.keymap[key.S]:
			self.e.throttle = 0.0
		else:
			self.e.throttle = 0.5
		
		#============================
		
		l = abs(self.m)
		
		if l > 0.0:
			d = 0.1*self.m/math.sqrt(l)
			self.e._yaw = -d.x
			self.e._pitch = -d.y
		
		#if l < 300.0:
		self.m -= self.m*5.0*dt
		
		#============================
		
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
		
		if self.keymap[key.SPACE] or self.left_mouse:
			self.e.fire_primary()
		
		if self.keymap[key.LSHIFT] or self.right_mouse:
			self.e.fire_secondary()
		
		if self.keymap[key.P]:
			print 'pos: ', self.e.position
		
	def on_mouse_motion(self, x, y, dx, dy):
		self.m += Vector2(dx, dy)
	
	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		self.m += Vector2(dx, dy)
	
	def on_mouse_press(self, x, y, button, modifiers): 
		if button == mouse.LEFT:
			self.left_mouse = True
		elif button == mouse.RIGHT:
			self.right_mouse = True
	
	def on_mouse_release(self, x, y, button, modifiers): 
		if button == mouse.LEFT:
			self.left_mouse = False
		elif button == mouse.RIGHT:
			self.right_mouse = False
	
	def on_key_press(self, k, mods):
		pass
	
	def on_key_release(self, k, mods):
		pass
