
from pyglet.gl import *
from euclid import Matrix3, Matrix4

class Pass:
	sky = 0
	background = 1
	
	solid = 2
	
	flares = 3
	trails = 4
	
	overlay = 5

class _Renderer:
	def __init__(self):
		self.queues = {}
	
	def render(self, camera, transform, renderable, when=Pass.solid):
		q = self.queues.setdefault(when, [])
		q.append( (transform, camera.view, camera.proj, renderable) )
	
	def render_all(self):
		for p, q in self.queues.items():
			for i in q:
				self.render_item(*i)
			
			if p == Pass.sky or p == Pass.trails:
				glClear(GL_DEPTH_BUFFER_BIT)
		
		self.queues = {}
	
	def render_item(self, model, view, proj, renderable):
		model_view = view * model
		model_view_proj = proj * model_view
		
		s = renderable.shader
		
		s.bind()
		
		if 'model_matrix' in s.uniforms:
			s.uniform_matrix_4x4('model_matrix', model)
		if 'view_matrix' in s.uniforms:
			s.uniform_matrix_4x4('view_matrix', view)
		if 'proj_matrix' in s.uniforms:
			s.uniform_matrix_4x4('proj_matrix', proj)
		if 'model_view_matrix' in s.uniforms:
			s.uniform_matrix_4x4('model_view_matrix', model_view)
		if 'model_view_proj_matrix' in s.uniforms:
			s.uniform_matrix_4x4('model_view_proj_matrix', model_view_proj)
		
		if 'model_normal_matrix' in s.uniforms:
			m, v = Matrix3(), model
			m.a, m.b, m.c = v.a, v.b, v.c
			m.e, m.f, m.g = v.e, v.f, v.g
			m.i, m.j, m.k = v.i, v.j, v.k
			s.uniform_matrix_3x3('model_normal_matrix', m)
		
		if 'inv_model_normal_matrix' in s.uniforms:
			m, v = Matrix3(), model
			m.a, m.b, m.c = v.a, v.e, v.i
			m.e, m.f, m.g = v.b, v.f, v.j
			m.i, m.j, m.k = v.c, v.g, v.k
			s.uniform_matrix_3x3('inv_model_normal_matrix', m)
		
		if 'model_view_normal_matrix' in s.uniforms:
			m, v = Matrix3(), model_view
			m.a, m.b, m.c = v.a, v.b, v.c
			m.e, m.f, m.g = v.e, v.f, v.g
			m.i, m.j, m.k = v.i, v.j, v.k
			s.uniform_matrix_3x3('model_view_normal_matrix', m)
		
		textures = zip(range(len(renderable.textures)), renderable.textures)
		
		for i, t in textures:
			glActiveTexture(GL_TEXTURE0 + i)
			glBindTexture(t.target, t.id)
			s.texture(i)
		
		renderable.draw()
		
		textures.reverse()
		for i, t in textures:
			glActiveTexture(GL_TEXTURE0 + i)
			glBindTexture(t.target, 0)
		
		s.unbind()

Renderer = _Renderer()
del _Renderer
