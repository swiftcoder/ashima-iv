
import pyglet

from window import Window

class AppState:
	def start(self):
		pass
	
	def stop(self):
		pass
	
	def resume(self):
		pass
	
	def pause(self):
		pass
	
	def update(self, dt):
		pass
	
	def draw(self):
		pass

states = []

def enter_state(state):
	if len(states):
		states[-1].pause()
	
	state.start()
	states.append(state)

def exit_state():	
	states[-1].stop()
	states.pop()
	
	if len(states):
		states[-1].resume()

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
	
	enter_state(GameState())
	enter_state(SplashState())
	
	pyglet.clock.schedule_interval(update, 1/60.0)	
	pyglet.app.run()
