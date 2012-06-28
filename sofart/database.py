#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid
import os
import sys
import datetime

from .exceptions import DatabaseError
from .collection import Collection

class Database(object):
	def __init__(self, path = None, mode = "single", serializer = "msgpack"):
		if not path:
			raise DatabaseError('Need path')
	
		self.init_schema = {"_infos": {	"creation_date": datetime.datetime.now().isoformat(), 
										"serializer": serializer,
										"total_entries": 0}}

		self.mode = mode
		self.path = path

		self.serializer = serializer
		_serializer = __import__("sofart.serializers._%s" % self.serializer)
		_serializer = sys.modules["sofart.serializers._%s" % self.serializer]
		self._serializer = _serializer.Serializer(self.path)

		if self.mode == "single":
			self.initialize()
		elif self.mode == "multi":
			self.db = self.initialize()

	def count(self):
		return self.db['_infos']['total_entries']

	def initialize(self):
		if not os.path.exists(self.path):
			self._serializer.init(self.init_schema)
		try:
			db = self._serializer.load() 
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
				self._serializer.dump(self.db)
			elif self.mode == "single":
				self.db = new_db
		except:
			raise DatabaseError('Update problem')

	def add_id(self, new_id):
		if self.mode == "multi":
			tmp = self.db
			tmp['_infos']['total_entries'] += 1
			self.update(tmp)
		elif self.mode == "single":
			self.db['_infos']['total_entries'] += 1

	def del_id(self, old_id):
		try:
			if self.mode == "multi":
				tmp = self.db
				tmp['_infos']['total_entries'] -= 1
				self.update(tmp)
			elif self.mode == "single":
				self.db['_infos']['total_entries'] -= 1
		except:
			raise DatabaseError('Id is not in database')

	def new_collection(self, name):
		if not name in self.get_collections():
			if self.mode == "multi":
				tmp = self.db
				tmp[name] = []
				self.update(tmp)
				del tmp
			elif self.mode == "single":
				self.db[name] = []

	def drop_collection(self, name):
		if name == "_infos":
			raise DatabaseError('Can\'t remove \"_infos\" database')
		try:
			if self.mode == "multi":
				tmp = self.db
				tmp['_infos']['total_entries'] -= len(tmp[name])
				del tmp[name]
				self.update(tmp)
				del tmp
			elif self.mode == "single":
				self.db['_infos']['total_entries'] -= len(self.db[name])
				del self.db[name]
		except KeyError as err:
			pass

	def get_collections(self):
		return [c for c in self.db.keys() if c != '_infos']

	def get(self, collection_name):
		if not collection_name in self.get_collections():
			raise DatabaseError('Collection not exist')
		return Collection(collection_name, self.path, self)

	def sync(self):
		self._serializer.dump(self.db)

	def close(self):
		self.sync()

	def __del__(self):
		self.sync()

	def __unicode__(self):
		return self.path

	def __str__(self):
		return self.path
