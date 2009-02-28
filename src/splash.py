
import pyglet
from pyglet.gl import *
from pyglet.window import key

from app import AppState, states

from window import Window

from resources import Resources

class SplashState(AppState):
	def __init__(self):
		self.batch = pyglet.graphics.Batch()
				
		background = pyglet.graphics.OrderedGroup(0)
		foreground = pyglet.graphics.OrderedGroup(1)
		
		image = Resources.load_texture('data/images/splash.jpg')
		self.sprite = pyglet.sprite.Sprite(image, batch=self.batch, group=background)
		
		w, h = image.width, image.height
		
		play = Resources.load_texture('data/images/play.png')
		quit = Resources.load_texture('data/images/quit.png')
		
		self.buttons = [pyglet.sprite.Sprite(play, x=w-500, y=h-500, batch=self.batch, group=foreground), pyglet.sprite.Sprite(quit, x=w-500, y=h-650, batch=self.batch, group=foreground)]
		
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(0, w, 0, h, -1, 1)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		
		Window.push_handlers(self.on_key_press)
	
	def pop(self):
		Window.pop_handlers()
		states.pop()
	
	def update(self, dt):
		pass
		
	def on_key_press(self, k, mods):
		if k == key.P:
			self.pop()
		elif k == key.Q:
			pyglet.app.exit()
	
	def draw(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		
		glColor4f(1, 1, 1, 1)
		
		self.batch.draw()
