
import pyglet
from pyglet.gl import *
from ctypes import *
from euclid import Vector3, Matrix4, Matrix3, Quaternion

import math

def pick(camera, viewport, x, y):
	z = GLfloat()
	glReadPixels(x, y, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT, byref(z))
	
	p = [GLdouble(), GLdouble(), GLdouble()]
	model = (GLdouble * 16)( *(camera.view) )
	proj = (GLdouble * 16)(*camera.proj)
	view = (GLint * 4)(*viewport)
	gluUnProject(x, y, z.value, model, proj, view, byref(p[0]), byref(p[1]), byref(p[2]))
	
	return Vector3(*[c.value for c in p])

def invert_ortho_matrix(m):
	n = Matrix4()
	
	n.a, n.b, n.c = m.a, m.e, m.i
	n.e, n.f, n.g = m.b, m.f, m.j
	n.i, n.j, n.k = m.c, m.g, m.k
	
	n.d, n.h, n.l = -m.d, -m.h, -m.l
	
	n.m, n.n, n.o, n.p = 0, 0, 0, 1
	
	return n

def model_to_view_ortho_matrix(m):
	n = Matrix4()
	
	n.a, n.b, n.c = m.a, m.e, m.i
	n.e, n.f, n.g = m.b, m.f, m.j
	n.i, n.j, n.k = m.c, m.g, m.k
	
	return n * Matrix4.new_translate(-m.d, -m.h, -m.l)

def look_at_quaternion(dir, up):
	q = Quaternion()
	
	z = dir.normalized() 
	x = up.cross(z).normalized()
	y = z.cross(x)
	tr = x.x + y.y + z.z
	
	q.x, q.y, q.z, q.w = y.z - z.y, z.x - x.z, x.y - y.x, tr + 1.0
	
	return q.normalized()

def inverse_quaternion(q):
	return q.normalized().conjugated()
	
def rotation_to(src, dst):
	c = src.cross(dst)
	
	q = Quaternion(
				math.sqrt(src.magnitude_squared() * dst.magnitude_squared()) + src.dot(dst),
				c.x, c.y, c.z
				)
	return q.normalized()
