import pickle
import os

from .exceptions import DatabaseError
from .collection import Collection

class Database(object):
	def __init__(self, path=None):
		if not path:
			raise DatabaseError('Need path')
	
		self.init_schema = {"index": {"collections": [], "ids": []}}

		self.path = path
		self.db = self.initialize()
		self.collections = self.get_collections()

	def initialize(self):
		if not os.path.exists(self.path):
			pickle.dump(self.init_schema, open(self.path, 'w'))
		try:
			db = pickle.load(open(self.path, 'r')) 
			if not isinstance(db , dict):
				raise DatabaseError('Seems to be corrupt')
			return db
		except EOFError:
			raise DatabaseError('Seems to be corrupt')

	def update(self, new_db):
		if not isinstance(new_db, dict):
			raise DatabaseError('Database update can\'t be empty')
		try:
			pickle.dump(new_db, open(self.path, 'w'))
		except:
			raise DatabaseError('Update problem')

	def add_id(self, new_id):
		tmp = self.db
		tmp['index']['ids'].append(new_id)
		self.update(tmp)

	def del_id(self, old_id):
		tmp = self.db
		try:
			tmp['index']['ids'].remove(old_id)
		except:
			raise DatabaseError('Id is not in database')
		self.update(tmp)

	def new_collection(self, collection_name):
		if not collection_name in self.get_collections():
			tmp = self.db
			tmp[collection_name] = []
			tmp['index']['collections'].append(collection_name)
			#self.update(self.db.update(dict(collection_name=[])))
			#self.update(self.db['index']['collections'].append(collection_name))
			self.update(tmp)
			del tmp

	def drop_collection(self, collection_name):
		try:
			tmp = self.db
			del tmp[collection_name]
			tmp['index']['collections'].remove(str(collection_name))
			#self.update(self.db.pop(collection_name))
			#self.update(self.db['index']['collections'].remove(collection_name))
			self.update(tmp)
			del tmp
		except:
			pass
			#raise DatabaseError('Collection not exist')

	def get_collections(self):
		return self.db['index']['collections']	

	def get(self, collection_name):
		if not collection_name in self.get_collections():
			raise DatabaseError('Collection not exist')
		return Collection(collection_name, self.path, self)
