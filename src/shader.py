
from pyglet.gl import *
import pyglet

import euclid

class Shader:
	def __init__(self, vert = [], frag = []):
		self.Handle = glCreateProgram()
	#	print 'program: ', self.Handle
		self.Linked = False
		
		self.createShader(vert, GL_VERTEX_SHADER)
		self.createShader(frag, GL_FRAGMENT_SHADER)
		
		self.link()
	
	def createShader(self, strings, type):
		count = len(strings)
		if count < 1:
			return
		
		shader = glCreateShader(type)
	#	print 'shader: ', shader
				
		src = (c_char_p * count)(*strings)
		glShaderSource(shader, count, cast(pointer(src), POINTER(POINTER(c_char))), None)
		
		glCompileShader(shader)
		
		temp = c_int(0)
		glGetShaderiv(shader, GL_COMPILE_STATUS, byref(temp))
		if not temp:
			glGetShaderiv(shader, GL_INFO_LOG_LENGTH, byref(temp))
			buffer = create_string_buffer(temp.value)
			glGetShaderInfoLog(shader, temp, None, buffer)
			
			print buffer.value
		
		glAttachShader(self.Handle, shader);
	
	def link(self):
		glLinkProgram(self.Handle)
		
		temp = c_int(0)
		glGetProgramiv(self.Handle, GL_LINK_STATUS, byref(temp))
		if not temp:
			glGetProgramiv(self.Handle, GL_INFO_LOG_LENGTH, byref(temp))
			buffer = create_string_buffer(temp.value)
			glGetProgramInfoLog(self.Handle, temp, None, buffer)
			
			print buffer.value
		else:
			self.Linked = True
		
	def bind(self):
		if self.Linked:
			glUseProgram(self.Handle)
	
	def unbind(self):
		if self.Linked:
			glUseProgram(0)
	
	def uniform(self, name, vals):
		if self.Linked:
			if len(vals) in range(1, 5):
				{ 1 : glUniform1f,
					2 : glUniform2f,
					3 : glUniform3f,
					4 : glUniform4f
				}[len(vals)](glGetUniformLocation(self.Handle, name), *vals)
	
	def uniform_matrix(self, name, mat):
		if isinstance(mat, euclid.Matrix3):
			l = 9
		elif isinstance(mat, euclid.Matrix4):
			l = 16
		else:
			l = len(mat)
		
		if self.Linked:
			if l in [4, 9, 16]:
				{
					4: glUniformMatrix2fv,
					9: glUniformMatrix3fv,
					16: glUniformMatrix4fv,
				}[l](glGetUniformLocation(self.Handle, name), 1, False, (c_float * l)(*mat))
	
	def texture(self, unit):
		if self.Linked:
			glUniform1i(glGetUniformLocation(self.Handle, 'tex' + str(unit)), unit)

	
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
