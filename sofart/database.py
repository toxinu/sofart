import pickle
import os

from .exceptions import DatabaseError
from .collection import Collection

class Database(object):
	def __init__(self, path=None, mode="single"):
		if not path:
			raise DatabaseError('Need path')
	
		self.init_schema = {"index": {"collections": [], "ids": []}}

		self.mode = mode
		self.path = path

		if self.mode == "single":
			self.initialize()
		elif self.mode == "mutli":
			self.db = self.initialize()

		self.collections = self.get_collections()

	def initialize(self):
		if not os.path.exists(self.path):
			pickle.dump(self.init_schema, open(self.path, 'w'))
		try:
			db = pickle.load(open(self.path, 'r')) 
			if not isinstance(db , dict):
				raise DatabaseError('Seems to be corrupt')
			if self.mode == "multi":
				return db
			elif self.mode == "single":
				self.db = db
		except EOFError:
			raise DatabaseError('Seems to be corrupt')

	def update(self, new_db):
		if not isinstance(new_db, dict):
			raise DatabaseError('Database update can\'t be empty')
		try:
			if self.mode == "multi":
				pickle.dump(new_db, open(self.path, 'w'))
			elif self.mode == "single":
				self.db = new_db
		except:
			raise DatabaseError('Update problem')

	def add_id(self, new_id):
		if self.mode == "multi":
			tmp = self.db
			tmp['index']['ids'].append(new_id)
			self.update(tmp)
		elif self.mode == "single":
			self.db['index']['ids'].append(new_id)

	def del_id(self, old_id):
		try:
			if self.mode == "multi":
				tmp = self.db
				tmp['index']['ids'].remove(old_id)
				self.update(tmp)
			elif self.mode == "single":
				self.db['index']['ids'].remove(old_id)
		except:
			raise DatabaseError('Id is not in database')

	def new_collection(self, collection_name):
		if not collection_name in self.get_collections():
			if self.mode == "multi":
				tmp = self.db
				tmp[collection_name] = []
				tmp['index']['collections'].append(collection_name)
				self.update(tmp)
				del tmp
			elif self.mode == "single":
				self.db[collection_name] = []
				self.db['index']['collections'].append(collection_name)

	def drop_collection(self, collection_name):
		try:
			if self.mode == "multi":
				tmp = self.db
				del tmp[collection_name]
				tmp['index']['collections'].remove(str(collection_name))
				self.update(tmp)
				del tmp
			elif self.mode == "single":
				del self.db[collection_name]
				self.db['index']['collections'].remove(str(collection_name))
		except:
			pass

	def get_collections(self):
		return self.db['index']['collections']	

	def get(self, collection_name):
		if not collection_name in self.get_collections():
			raise DatabaseError('Collection not exist')
		return Collection(collection_name, self.path, self)

	def __del__(self):
		if self.mode == "single":
			pickle.dump(self.db, open(self.path, 'w'))