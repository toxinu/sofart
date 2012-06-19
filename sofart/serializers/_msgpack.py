import msgpack

class Serializer(object):
	def __init__(self, path):
		self.path = path
		self.packer = msgpack.Packer()
		self.unpacker = msgpack.Unpacker(use_list=True)

	def init(self, schema):
		self.dump(schema)

	def dump(self, dump):
		open(self.path, 'w').write(self.packer.pack(dump))

	def load(self):
		self.unpacker.feed(open(self.path, 'r').read())
		return self.unpacker.unpack()
