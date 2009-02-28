
import pyglet
from pyglet.gl import *

import math

from app import AppState, enter_state
from outcome import OutcomeState

from window import Window
from entity import World
import factories
from euclid import Vector3

from resources import Resources
from camera import Camera
from controller import Controller
from tether import Tether

from graphics import Graphics
from teams import Teams

class GameState(AppState):
	def start(self):
		music = pyglet.resource.media('data/music/the_moonlight_strikers_act1.mp3')
		self.player = music.play()
		
		self.sunlight = Resources.load_shader('data/shaders/sunlight.shader')
		
		ship = factories.create_hammerfall(Vector3(0, -250, 2400), 'red')
		World.add(ship)
		
		for i in range(4, 0, -1):
			ship = factories.create_anaconda(Vector3(i*5, i*10, i*10 + 1000), 'red')
			World.add(ship)
		
		for i in range(2, 0, -1):
			ship = factories.create_viper(Vector3(i*40, i*-10, i*10 + 25), 'blue', i != 1)
			World.add(ship)
		
		self.ship = ship
		World.set_player(self.ship)
		
		@ship.event
		def on_remove(ship):
			print 'defeat'
			enter_state( OutcomeState(False) )

		self.fps_display = pyglet.clock.ClockDisplay()
		
		glEnable(GL_CULL_FACE)
		glFrontFace(GL_CCW)
		
		glEnable(GL_DEPTH_TEST)
		glDepthFunc(GL_LEQUAL)
		glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
			
		aspect = float(Window.width)/float(Window.height)
		
		camera = Camera(math.pi/4, aspect, 0.1, 100000.0)
		Graphics.camera = camera
		
		cam = factories.create_camera(camera)
		World.add(cam)
				
		tether = Tether(cam, ship, Vector3(-5, 8, -16), Vector3(0, 0, 65))
		
		aim = factories.aim_assist(cam)
		crosshairs = factories.cross_hairs(ship)
		
		factories.create_sky(cam)
		
	def resume(self):
		control = Controller(self.ship)
		self.player.play()
			
	def pause(self):
		if self.player:
			self.player.pause()
	
	def update(self, dt):
		World.perform_update(dt)
		
		if Teams.in_team('red') == []:
			print 'victory'
			enter_state( OutcomeState(True) )
			
	def draw(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		
		glColor4f(1, 1, 1, 1)
		
		self.sunlight.bind()
		self.sunlight.uniform('sunDir', Vector3(-1, 1, 0).normalize())
		self.sunlight.unbind()
			
		World.perform_frame()
		
		glMatrixMode(GL_PROJECTION) 
		glLoadIdentity()
		glOrtho(0, Window.width, 0, Window.height, -100, 100)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		
		self.fps_display.draw()
