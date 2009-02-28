
import pyglet

from window import Window

class AppState:
	def update(self, dt):
		pass
	
	def draw(self):
		pass

states = []

@Window.event
def on_draw():
	try:
		states[-1].draw()
	except IndexError:
		pyglet.app.exit()

def update(dt):
	try:
		states[-1].update(dt)
	except IndexError:
		pyglet.app.exit()

def run():	
	from game import GameState
	from splash import SplashState
	
	states.append(GameState())
	states.append(SplashState())
	
	pyglet.clock.schedule_interval(update, 1/60.0)	
	pyglet.app.run()
