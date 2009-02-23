
from pyglet.gl import *
import pyglet

import euclid

class Shader:
	def __init__(self, vert = [], frag = []):
		self.Handle = glCreateProgramObjectARB()
	#	print 'program: ', self.Handle
		self.Linked = False
		
		self.createShader(vert, GL_VERTEX_SHADER_ARB)
		self.createShader(frag, GL_FRAGMENT_SHADER_ARB)
		
		self.link()
	
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
		
	def bind(self):
		if self.Linked:
			glUseProgramObjectARB(self.Handle)
	
	def unbind(self):
		if self.Linked:
			glUseProgramObjectARB(0)
	
	def uniform(self, name, vals):
		if self.Linked:
			if len(vals) in range(1, 5):
				{ 1 : glUniform1fARB,
					2 : glUniform2fARB,
					3 : glUniform3fARB,
					4 : glUniform4fARB
				}[len(vals)](glGetUniformLocationARB(self.Handle, name), *vals)
	
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
					4: glUniformMatrix2fvARB,
					9: glUniformMatrix3fvARB,
					16: glUniformMatrix4fvARB,
				}[l](glGetUniformLocationARB(self.Handle, name), 1, False, (c_float * l)(*mat))
	
	def texture(self, unit):
		if self.Linked:
			glUniform1iARB(glGetUniformLocationARB(self.Handle, 'tex' + str(unit)), unit)

	
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
