
from entity import World

class _Teams:
	def __init__(self):
		self.teams = {}
		
		World.add_handlers(self.on_add, self.on_remove)
	
	def on_add(self, entity):
		if entity.has('team'):		
			if not entity.team in self.teams:
				self.teams[entity.team] = [entity]
			else:
				self.teams[entity.team].append(entity)
			entity.add_handlers(self.on_remove)
	
	def on_remove(self, entity):
		for v in self.teams.itervalues():
			if entity in v:
				v.remove(entity)
	
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
