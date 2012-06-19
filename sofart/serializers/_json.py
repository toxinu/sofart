import json

class Serializer(object):
	def __init__(self, path):
		self.path = path

	def init(self, schema):
		self.dump(schema)

	def dump(self, dump):
		json.dump(dump, open(self.path, 'w'))

	def load(self):
		return json.load(open(self.path, 'r'))
