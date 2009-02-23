
from entity import *

from resources import Resources
from node import Node, BillboardNode
from model import Model
from camera import CameraNode
from tether import Tether

from sprite import Sprite

from ribbon import Engine

from weapon import *

import math
import new

from euclid import Vector3

def create_camera(camera):
	e = Entity()
	
	e.graphics = True
	e.physics = True
	
	n = CameraNode(camera)
	e.node = n
	
	e.mass = 5.0
	
	return e

def create_anaconda():
	e = Entity()
	
	e.graphics = True
	e.physics = True
	
	e.model = Resources.load_model('data/models/anaconda.model')
	
	n = Node()
	n.renderables.append( e.model )
	e.node = n
		
	e.throttle = 0.5
	
	e.min_acceleration = 250.0 #4000.0
	e.max_acceleration = 2000.0 #8000.0
	e.max_velocity = 4.0
	
	e.max_yaw = 30.0 #math.pi/3
	e.max_pitch = 30.0 #math.pi/3
	e.max_roll = 30.0 #math.pi/3
	
	e.mass = 5.0
	e.extents = Vector3(8, 3, 10)
	
	e.engines = [Engine(e, Vector3(0, 0.125, 0))]

	e.primary_weapon = Weapon(e, bullet_factory, 0.25)
	e.secondary_weapon = Weapon(e, rocket_factory, 1.0)
		
	e.fire_primary = new.instancemethod(lambda s: s.primary_weapon.fire(Vector3(0, 0, 20)), e, Entity)
	e.fire_secondary = new.instancemethod(lambda s: s.secondary_weapon.fire(Vector3(0, 0, 20)), e, Entity)
	
	return e

def create_hammerfall():
	e = Entity()
	
	e.graphics = True
	e.physics = True
	
	e.model = Resources.load_model('data/models/hammerfall.model')
	
	n = Node()
	n.renderables.append( e.model )
	e.node = n
	
	e.throttle = 0.5
	
	e.min_acceleration = 4000.0 #4000.0
	e.max_acceleration = 8000.0 #8000.0
	e.max_velocity = 4.0
	
	e.max_yaw = math.pi/8
	e.max_pitch = math.pi/8
	e.max_roll = math.pi/8
	
	e.mass = 40.0
	e.extents = Vector3(80, 40, 200)
	
	e.engines = [Engine(e, Vector3(0, 0, -100))]
	
	return e
