
from entity import World

from sprite import Sprite
from renderable import Renderable
from renderer import Pass
from node import BillboardNode
from resources import Resources

class _Teams:
	team_colours = {'red': [1, 0, 0, 1], 'blue': [0, 0, 1, 1]}

	def __init__(self):
		self.teams = {}
		self.player = None
		
		World.add_handlers(self.on_add, self.on_remove, self.on_set_player)
	
	def on_add(self, entity):
		if entity.has('team'):		
			if not entity.team in self.teams:
				self.teams[entity.team] = [entity]
			else:
				self.teams[entity.team].append(entity)
			entity.add_handlers(self.on_remove)
			
			if not entity.has('team_no_reticule') or not entity.team_no_reticule:
				size = max(entity.extents)
				r = Renderable(Sprite(size, size, self.team_colours[entity.team]), Resources.load_shader('data/shaders/unlit.shader'), [Resources.load_texture('data/images/target.png')], Pass.overlay)
				
				entity._reticule = BillboardNode(entity.node)
				entity._reticule.renderables.append(r)
	
	def on_remove(self, entity):
		for v in self.teams.itervalues():
			if entity in v:
				v.remove(entity)
	
	def on_set_player(self, player, old):
		self.player = player
		
		if self.player:
			self.player._reticule.parent = None
			del self.player._reticule
		
	def in_team(self, team):
		'''returns all the members of team, or [] if team does not exist'''
		if team in self.teams:
			return self.teams[team]
		return []
	
	def not_in_team(self, team):
		'''returns all entities not in team'''
		if not team in self.teams:
			return self.teams
		vals = [v for k, v in self.teams.iteritems() if k != team]
		res = []
		for a in vals:
			res.extend(a)
		return res
	
	def all(self):
		return reduce(lambda x, y: x + y, [v for k, v in self.teams.iteritems()])

Teams = _Teams()
del _Teams
