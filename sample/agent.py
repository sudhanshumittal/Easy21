class agent(object):
	def get_action(self, state): raise NotImplementedError("implement me")
	def __init__(self):
		self.HIT = 0;
		self.STICK = 1;
		self.action_space = [self.HIT, self.STICK]
