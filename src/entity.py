
import events

class Entity(events.EventDispatcher):
	def __init__(self, name=''):
		self.name = name

	def has(self, attr):
		return hasattr(self, attr)

	def get(self, attr):
		return getattr(self, attr)

	def set(self, attr, val):
		setattr(self, attr, val)
	
	def default(self, attr, val):
		if not self.has(attr):
			self.set(attr, val)
	
	def perform_remove(self):
		self.dispatch_event('on_remove', self)
	
	def perform_death(self):
		self.dispatch_event('on_death', self)

	def perform_damage(self, damage):
		self.dispatch_event('on_damage', self, damage)

Entity.register_event_type('on_remove')
Entity.register_event_type('on_death')
Entity.register_event_type('on_damage')


class _World(events.EventDispatcher):	
	def __init__(self):
		self.Entities = []
		self.Player = None
	
	def perform_frame(self):
		self.dispatch_event('on_frame')
	
	def perform_update(self, dt):
		self.dispatch_event('on_update', dt)
		
		remove = [e for e in self.Entities if e.has('remove_from_world') and e.remove_from_world == True]
		for e in remove:
			self.remove(e)
	
	def add(self, entity):
		self.Entities.append(entity)
		self.dispatch_event('on_add', entity)
	
	def remove(self, entity):
		entity.perform_remove()
		self.dispatch_event('on_remove', entity)
		self.Entities.remove(entity)
	
	def get_player(self):
		return self.Player
	def set_player(self, p):
		self.dispatch_event('on_set_player', p, self.Player)
		self.Player = p
	player = property(get_player, set_player)

_World.register_event_type('on_frame')
_World.register_event_type('on_update')
_World.register_event_type('on_add')
_World.register_event_type('on_remove')
_World.register_event_type('on_set_player')

World = _World()
del _World
