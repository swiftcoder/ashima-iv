
import pyglet
from pyglet.window import key

from window import Window

from entity import World
from graphics import Graphics
from physics import Physics
from lifetime import Lifetime
from teams import Teams
from ai import AI

import ai_missile, ai_fighter

import factories

from camera import Camera
from node import Node, BillboardNode, SkyNode, IntervalNode
from model import Model

from controller import Controller
from tether import Tether

from renderer import Pass

from dust import Dust

import utility

from resources import Resources

from pyglet.gl import *

from euclid import Vector3, Matrix4, Quaternion
from math import sin, cos, pi

sunlight = Resources.load_shader('data/shaders/sunlight.shader')

ship = factories.create_hammerfall()
ship.position = Vector3(0, 0, 250)
ship.team = 'red'
World.add(ship)

for i in range(4, 0, -1):
	ship = factories.create_anaconda()
	ship.position = Vector3(i*5, i*10, i*10 + 250)
	ship.team = 'red'
	World.add(ship)

for i in range(2, 0, -1):
	ship = factories.create_viper(i != 1)
	ship.position = Vector3(i*10, i*-10, i*10 + 5)
	ship.team = 'blue'
	World.add(ship)

control = Controller(ship)

#select = BillboardNode(Graphics.root)
#select.renderables.append( Selection(0.125, 0.125, Resources.load_shader('data/shaders/unlit.shader'), Resources.load_texture('data/images/target.png')) )

fps_display = pyglet.clock.ClockDisplay()

def init():	
	glEnable(GL_CULL_FACE)
	glFrontFace(GL_CCW)
	
	glEnable(GL_DEPTH_TEST)
	glDepthFunc(GL_LEQUAL)
	glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
		
	aspect = float(Window.width)/float(Window.height)
	
	global camera
	camera = Camera(pi/4, aspect, 0.1, 100000.0)
	
	camera.view.rotatey(pi/3).translate(4, -0.5, -8)
	
	Graphics.camera = camera
	
	cam = factories.create_camera(camera)
	World.add(cam)
		
	tether = Tether(cam, ship, Vector3(0, 5, -16), Vector3(0, 0, 16))

	sky = SkyNode(cam.node)
	sphere = Resources.load_model('data/models/sky.model')
	sphere.render_pass = Pass.sky
	sky.renderables.append( sphere )
	
	#dust = IntervalNode(10, ship.node)
	#dust.renderables.append( Dust(4, 10, 100) )
	
	Window.set_mouse_visible(False)

elapsed_t = 0.0
delta_t = 0.0

mouse_x = 0
mouse_y = 0

'''keymap = key.KeyStateHandler()
Window.push_handlers(keymap)

@Window.event
def on_mouse_motion(x, y, dx, dy):
	global mouse_x, mouse_y
	mouse_x = x
	mouse_y = y

@Window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
	global mouse_x, mouse_y
	mouse_x = x
	mouse_y = y

@Window.event
def on_mouse_press(x, y, button, modifiers): 
	p = utility.pick(camera, [0, 0, Window.width, Window.height], mouse_x, mouse_y)
	print p, abs(p)'''
	
def update(dt):
	global elapsed_t, delta_t
	elapsed_t += dt
	delta_t = dt
	
	World.perform_update(dt)

@Window.event
def on_draw():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	
	global elapsed_t, delta_t
	
	glColor4f(1, 1, 1, 1)
	
	sunlight.bind()
	sunlight.uniform('sunDir', Vector3(-1, 1, 0).normalize())
	sunlight.unbind()
	
	#p = utility.pick(camera, [0, 0, Window.width, Window.height], mouse_x, mouse_y)
	#if abs(p) < 1000:
	#	print select.model
	#	print select.transform
	#	select.model = Matrix4.new_translate(*p)
	
	World.perform_frame()
	
	glMatrixMode(GL_PROJECTION) 
	glLoadIdentity()
	glOrtho(0, Window.width, 0, Window.height, -100, 100)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	
	fps_display.draw()
	
	glMatrixMode(GL_PROJECTION) 
	glMatrixMode(GL_MODELVIEW)

def run():
	init()
	
	pyglet.clock.schedule_interval(update, 1/60.0)	
	pyglet.app.run()
