import pickle
import uuid

from .exceptions import CollectionError

class Collection(object):
	def __init__(self, name, path, db):
		self.name = name
		self.path = path
		self.entries = db.db[self.name]
		self.db = db
		self.total_entries = len(db.db[self.name])

	def update(self, new_collection):
		if not isinstance(new_collection, list):
			raise CollectionError('Collection update can\'t be empty')
		try:
			if self.db.mode == "multi":
				tmp = self.db.db
				tmp[self.name] = new_collection
				pickle.dump(tmp, open(self.path, 'w'))
				del tmp
			elif self.db.mode == "single":
				self.db.db[self.name] == new_collection
		except:
			raise CollectionError('Seems to be invalid')
			
	def save(self, enreg):
		if not isinstance(enreg, dict):
			raise CollectionError('Save is not valid')

		enreg['_id'] = str(uuid.uuid4())
		if self.db.mode == "single":
			self.entries.append(enreg)
			self.db.add_id(enreg['_id'])
		elif self.db.mode == "multi":
			tmp = self.entries
			tmp.append(enreg)
			self.update(tmp)
			self.db.add_id(enreg['_id'])
			del tmp

	def remove(self, enreg_id):
		if self.db.mode == "multi":
			tmp = self.entries
			tmp[:] = [d for d in tmp if d.get('_id') != str(enreg_id)]
			self.update(tmp)
			self.db.del_id(str(enreg_id))
		elif self.db.mode == "single":
			self.entries[:] = [d for d in self.entries if d.get('_id') != str(enreg_id)]
			self.db.del_id(str(enreg_id))

	def find_one(self, query={}, case_sensitive=False):
		if query:
			for enreg in self.entries:
				counter = True
				for key,value in query.items():
					if enreg.get(key, False):
						if isinstance(enreg[key], str):
							if not case_sensitive:
								if not enreg[key].lower() == value.lower():
									counter = False
									break
							else:
								if not enreg[key] == value:
									counter = False
									break
						else:
							if not enreg[key] == value:
								counter = False
								break
					else:
						counter = False
				if counter:
					return enreg
		else:
			return self.entries[0]

	def find(self, query={}, nb=50, case_sensitive=False):
		current_item = 0
		result = []
		for enreg in self.entries:
			if current_item >= nb:
				break
			counter = True
			for key,value in query.items():
				if enreg.get(key, False):
					if isinstance(enreg[key], str):
						if not case_sensitive:
							if not enreg[key].lower() == value.lower():
								counter = False
								break
						else:
							if not enreg[key] == value:
								counter = False
								break
					else:
						if not enreg[key] == value:
							counter = False
							break
				else:
					counter = False
			if counter:
				current_item += 1
				result.append(enreg)
		return result