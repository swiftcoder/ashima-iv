
import pyglet
from pyglet.gl import *
from pyglet.window import key

from app import AppState

from window import Window

from resources import Resources

class OutcomeState(AppState):
	def __init__(self, victory):
		self.victory = victory
	
	def start(self):
		music = pyglet.resource.media('data/music/nightmare.mp3')
		
		self.batch = pyglet.graphics.Batch()
				
		background = pyglet.graphics.OrderedGroup(0)
		foreground = pyglet.graphics.OrderedGroup(1)
		
		image = Resources.load_texture('data/images/nasa/splash.jpg')
		self.sprite = pyglet.sprite.Sprite(image, batch=self.batch, group=background)
		
		w, h = image.width, image.height
		
		if self.victory:
			outcome = Resources.load_texture('data/images/victory.png')
		else:	
			outcome = Resources.load_texture('data/images/defeat.png')
		
		self.outcome = pyglet.sprite.Sprite(outcome, x=w/2 - outcome.width/2, y=h/2 - outcome.height/2, batch=self.batch, group=foreground)
		
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(0, w, 0, h, -1, 1)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		
		Window.push_handlers(self.on_key_press)
		
		self.player = music.play()
		self.elapsed = 0.0
	
	def stop(self):
		self.player.stop()
		Window.pop_handlers()
	
	def update(self, dt):
		self.elapsed += dt
		
	def on_key_press(self, k, mods):
		if self.elapsed > 4.0:
			pyglet.app.exit()
	
	def draw(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		
		glColor4f(1, 1, 1, 1)
		
		self.batch.draw()
