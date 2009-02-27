
import pyglet

from pyglet.window import key
from pyglet.gl import *

import os

class _Window(pyglet.window.Window):
	
	def __init__(self):
		pyglet.window.Window.__init__(self, 1024, 640, 'Planets', vsync=True)
		
		self.set_mouse_visible(False)
		self.set_exclusive_mouse(True)
		
		self.inFullscreen = False
		self.startup = True
		self.shot = 0
		
		self.center()
		
		glClearColor(0, 0, 0, 0.0)
		self.clear()
		self.flip()
	
	def center(self):
		self.set_location(self.screen.width/2 - self.width/2, self.screen.height/2 - self.height/2)
	
	def on_resize(self, width, height):		
		if self.startup:
			self.startup = False
		else:
			self.center()
		glViewport(0, 0, width, height)
	
	def toggle_fullscreen(self):
		self.inFullscreen = not self.inFullscreen
		self.set_fullscreen(self.inFullscreen)
		if not self.inFullscreen:
			self.set_size(1024, 640)
	
	def on_key_press(self, symbol, modifiers):		
		if symbol == key.ESCAPE:
			pyglet.app.exit()
		elif symbol == key.F:
			self.toggle_fullscreen()
		elif symbol == key.F1:
			self.shot += 1
			name = 'screenshot%03d.png' % self.shot
			file = os.path.join(os.path.expanduser('~/Desktop'), name)
			pyglet.image.get_buffer_manager().get_color_buffer().save(file)			

Window = _Window()
del _Window
