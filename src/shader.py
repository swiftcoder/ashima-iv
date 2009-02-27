
from pyglet.gl import *
import pyglet

import euclid

from collections import defaultdict

class Shader:
	def __init__(self, vert = [], frag = []):
		self.Handle = glCreateProgramObjectARB()
	#	print 'program: ', self.Handle
		self.Linked = False
		self.uniforms = {}
		
		self.createShader(vert, GL_VERTEX_SHADER_ARB)
		self.createShader(frag, GL_FRAGMENT_SHADER_ARB)
				
		self.link()
		self.query_uniforms()
			
	def createShader(self, strings, type):
		count = len(strings)
		if count < 1:
			return
		
		shader = glCreateShaderObjectARB(type)
	#	print 'shader: ', shader
				
		src = (c_char_p * count)(*strings)
		glShaderSourceARB(shader, count, cast(pointer(src), POINTER(POINTER(c_char))), None)
		
		glCompileShaderARB(shader)
		
		temp = c_int(0)
		glGetObjectParameterivARB(shader, GL_OBJECT_COMPILE_STATUS_ARB, byref(temp))
		if not temp:
			glGetObjectParameterivARB(shader, GL_OBJECT_INFO_LOG_LENGTH_ARB, byref(temp))
			buffer = create_string_buffer(temp.value)
			glGetInfoLogARB(shader, temp, None, buffer)
			
			print buffer.value
		
		glAttachObjectARB(self.Handle, shader);
	
	def link(self):
		glLinkProgramARB(self.Handle)
		
		temp = c_int(0)
		glGetObjectParameterivARB(self.Handle, GL_OBJECT_LINK_STATUS_ARB, byref(temp))
		if not temp:
			glGetObjectParameterivARB(self.Handle, GL_OBJECT_INFO_LOG_LENGTH_ARB, byref(temp))
			buffer = create_string_buffer(temp.value)
			glGetInfoLogARB(self.Handle, temp, None, buffer)
			
			print buffer.value
		else:
			self.Linked = True
	
	def query_uniforms(self):
		count = GLint()
		glGetObjectParameterivARB(self.Handle, GL_ACTIVE_UNIFORMS, byref(count))
		
		length = GLint()
		glGetObjectParameterivARB(self.Handle, GL_ACTIVE_UNIFORM_MAX_LENGTH, byref(length))
		
		size = GLint()
		_type = GLenum()
		buf = create_string_buffer(length.value)
		
		for i in range(count.value):
			glGetActiveUniformARB(self.Handle, i, length, None, byref(size), byref(_type), buf)
			self.uniforms[buf.value] = i
		
		del buf
		
		#print self.uniforms
	
	def bind(self):
		if self.Linked:
			glUseProgramObjectARB(self.Handle)
	
	def unbind(self):
		if self.Linked:
			glUseProgramObjectARB(0)
	
	def uniform(self, name, vals):
		loc = self.uniforms[name]
		
		if len(vals) in range(1, 5):
			{ 1 : glUniform1fARB,
				2 : glUniform2fARB,
				3 : glUniform3fARB,
				4 : glUniform4fARB
			}[len(vals)](loc, *vals)
	
	def uniform_matrix_3x3(self, name, mat):
		loc = self.uniforms[name]
		
		glUniformMatrix3fvARB(loc, 1, False, (c_float * 16)(*mat))
	
	def uniform_matrix_4x4(self, name, mat):
		loc = self.uniforms[name]
		
		glUniformMatrix4fvARB(loc, 1, False, (c_float * 16)(*mat))
	
	def texture(self, unit):
		loc = self.uniforms['tex' + str(unit)]
		
		glUniform1iARB(loc, unit)
	
	@classmethod
	def load(Class, name):
		import demjson
		
		f = pyglet.resource.file(name)		
		data = demjson.decode(f.read())
		f.close()
		
		if (data['version'] == 1):
			p = Class([data['vertex']['source']], [data['fragment']['source']])
			return p
		
		return None
