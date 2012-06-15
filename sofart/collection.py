import pickle
import uuid

from .exceptions import CollectionError

class Collection(object):
	def __init__(self, name, path, db):
		self.name = name
		self.path = path
		self.entries = db.db[self.name]
		self.db = db

	def update(self, new_collection):
		if not isinstance(new_collection, list):
			raise CollectionError('Collection update can\'t be empty')
		try:
			tmp = self.db.db
			tmp[self.name] = new_collection
			pickle.dump(tmp, open(self.path, 'w'))
			del tmp
		except:
			raise CollectionError('Seems to be invalid')
			
	def save(self, enreg):
		if not isinstance(enreg, dict):
			raise CollectionError('Save is not valid')
		enreg['_id'] = str(uuid.uuid4())
		tmp = self.entries
		tmp.append(enreg)
		self.update(tmp)
		self.db.add_id(enreg['_id'])
		del tmp

	def remove(self, enreg_id):
		tmp = self.entries
		tmp[:] = [d for d in tmp if d.get('_id') != enreg_id]
		self.update(tmp)
		self.db.del_id(enreg_id)

	def find_one(self, filter=None):
		if filter:
			for enreg in self.entries:
				counter = True
				for key,value in filter.items():
					if not enreg.get(key, False) == value:
						counter = False
						break
				if counter:
					return enreg
		else:
			return self.entries[0]

	def find(self, filter=None):
		if filter:
			result = []
			for enreg in self.entries:
				counter = True
				for key,value in filter.items():
					if not enreg.get(key, False) == value:
						counter = False
						break
				if counter:
					result.append(enreg)
			return result
		else:
			self.find_one()
