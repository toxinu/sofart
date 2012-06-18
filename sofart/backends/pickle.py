import cPickle as pickle

class Backend(object):
	def __init__(self, path):
		self.path = path

	def dump(self, dump):
			pickle.dump(dump, open(self.path, 'w'))

	def load(self):
		return pickle.load(open(self.path, 'r'))
