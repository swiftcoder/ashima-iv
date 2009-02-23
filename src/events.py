
import inspect

class EventDispatcher:
	
	@classmethod
	def register_event_type(cls, name):
		if not hasattr(cls, 'event_types'):
			cls.event_types = []
		cls.event_types.append(name)
	
	def add_handlers(self, *args, **kwargs):
		if not hasattr(self, 'event_handlers'):
			self.event_handlers = {}
		
		for obj in args:
			if inspect.isroutine(obj):
				name = obj.__name__
				if not name in self.event_types:
					raise Exception('unknown event type')
				self.add_handler(name, obj)
			else:
				for name in dir(obj):
					if name in self.event_types:
						self.add_handler(name, getattr(obj, name))
		
		for name, handler in kwargs.items():
			if not name in self.event_types:
				raise Exception('unknown event type')
			self.add_handler(name, handler)
	
	def remove_handlers(self, *args, **kwargs):
		if not hasattr(self, 'event_handlers'):
			return
		
		for obj in args:
			if inspect.isroutine(obj):
				name = obj.__name__
				if not name in self.event_types:
					raise Exception('unknown event type')
				self.remove_handler(name, obj)
			else:
				for name in dir(obj):
					if name in self.event_types:
						self.remove_handler(name, getattr(obj, name))
		
		for name, handler in kwargs.items():
			if not name in self.event_types:
				raise Exception('unknown event type')
			self.remove_handler(name, handler)
	
	def add_handler(self, name, handler):
		if not hasattr(self, 'handlers'):
			self.handlers = {}
		
		if not name in self.handlers:
			self.handlers[name] = []
		
		self.handlers[name].append(handler)
	
	def remove_handler(self, name, handler):
		if name in self.handlers:
			if handler in self.handlers[name]:
				self.handlers[name].remove(handler)
	
	def dispatch_event(self, type, *args):
		if not type in self.event_types:
			raise Exception('unknown event type')
		
		# print 'dispatching ' + type
		
		if hasattr(self, 'handlers'):
			if type in self.handlers:
				for handler in self.handlers[type]:
					handler(*args)
		
		if hasattr(self, type):
			getattr(self, type)(*args)
	
	def event(self, *args):
		'''Function decorator for an event handler.'''
		if len(args) == 0:                      # @window.event()
			def decorator(func):
				name = func.__name__
				self.add_handler(name, func)
				return func
			return decorator
		elif inspect.isroutine(args[0]):        # @window.event
			func = args[0]
			name = func.__name__
			self.add_handler(name, func)
			return args[0]
		elif type(args[0]) in (str, unicode):   # @window.event('on_resize')
			name = args[0]
			def decorator(func):
				self.add_handler(name, func)
				return func
			return decorator
