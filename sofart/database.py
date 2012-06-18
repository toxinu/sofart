#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid
import os
import sys

from .exceptions import DatabaseError
from .collection import Collection

class Database(object):
	def __init__(self, path = None, mode = "single", serializer = "json"):
		if not path:
			raise DatabaseError('Need path')
	
		self.init_schema = {"index": {"collections": [], "ids": []}}

		self.mode = mode
		self.path = path

		self.serializer = serializer
		_backend = __import__("sofart.backends._%s" % self.serializer)
		_backend = sys.modules["sofart.backends._%s" % self.serializer]
		self.backend = _backend.Backend(self.path)

		if self.mode == "single":
			self.initialize()
		elif self.mode == "multi":
			self.db = self.initialize()

		self.collections = self.get_collections()

	def total_entries(self):
		return len(self.db['index']['ids'])

	def initialize(self):
		if not os.path.exists(self.path):
			try:
				self.backend.init(self.init_schema)
			except Exception as err:
				raise DatabaseError('Seems to be corrupt or not %s object (%s)' % (self.serializer, err))
		try:
			db = self.backend.load() 
			if not isinstance(db , dict):
				raise DatabaseError('Seems to be corrupt or not %s object' % self.serializer)
			if self.mode == "multi":
				return db
			elif self.mode == "single":
				self.db = db
		except:
			raise DatabaseError('Seems to be corrupt or not %s object' % self.serializer)

	def update(self, new_db):
		if not isinstance(new_db, dict):
			raise DatabaseError('Database update can\'t be empty')
		try:
			if self.mode == "multi":
				self.backend.dump(self.db)
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
				ids = [e['_id'] for e in tmp[collection_name]]
				del tmp[collection_name]
				tmp['index']['collections'].remove(str(collection_name))
				for i in ids:
					self.del_id(i)
				self.update(tmp)
				del tmp
			elif self.mode == "single":
				ids = [e['_id'] for e in self.db[collection_name]]
				for i in ids:
					self.del_id(i)
				del self.db[collection_name]
				self.db['index']['collections'].remove(collection_name)
		except KeyError as err:
			pass

	def get_collections(self):
		return self.db['index']['collections']	

	def get(self, collection_name):
		if not collection_name in self.get_collections():
			raise DatabaseError('Collection not exist')
		return Collection(collection_name, self.path, self)

	def sync(self):
		self.backend.dump(self.db)

	def close(self):
		self.sync()

	def __del__(self):
		self.sync()
