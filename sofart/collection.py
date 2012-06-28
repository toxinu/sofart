#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid
import copy
import sys

from sofart.operators import isadvancedquery
from sofart.operators import computequery
from .exceptions import CollectionError

if sys.version < '3':
	import codecs
	def isstring(x):
		if isinstance(x, str) or isinstance(x, unicode):
			return True
		return False
else:
	def isstring(x):
		if isinstance(x, str):
			return True
		return False

class Collection(object):
	def __init__(self, name, path, db):
		self.name = name
		self.path = path
		self.entries = db.db[self.name]
		self.db = db

	def count(self):
		return len(self.entries)

	def update(self, new_collection):
		if not isinstance(new_collection, list):
			raise CollectionError('Collection update can\'t be empty')
		try:
			if self.db.mode == "multi":
				tmp = self.db.db
				tmp[self.name] = new_collection
				self.db._serializer.dump(tmp)
				del tmp
			elif self.db.mode == "single":
				self.db.db[self.name] == new_collection
		except:
			raise CollectionError('Seems to be invalid')
			
	def save(self, record):
		if not isinstance(record, dict):
			raise CollectionError('Save is not valid')

		record = copy.copy(record)
		record_id = str(uuid.uuid4())
		record['_id'] = record_id
		if self.db.mode == "single":
			self.entries.append(record)
			self.db.add_id(record_id)
		elif self.db.mode == "multi":
			tmp = self.entries
			tmp.append(record)
			self.update(tmp)
			self.db.add_id(record_id)
			del tmp
		del record

	def remove(self, enreg_id):
		if self.db.mode == "multi":
			tmp = self.entries
			tmp[:] = [d for d in tmp if d.get('_id') != enreg_id]
			self.update(tmp)
			self.db.del_id(enreg_id)
		elif self.db.mode == "single":
			self.entries[:] = [d for d in self.entries if d.get('_id') != enreg_id]
			self.db.del_id(enreg_id)

	def find_one(self, query={}, case_sensitive=False):
		for r in self.find(query=query, nb=1, case_sensitive=case_sensitive):
			if not r:
				return None
			else:
				return r

	def find(self, query={}, nb=50, case_sensitive=False):
		if not isinstance(query, dict):
			raise CollectionError('Query must be dict')
		current_item = 0
		for enreg in self.entries:
			if current_item >= nb:
				break
			counter = True
			for key, value in query.items():
				if isadvancedquery(enreg.get(key, None), value):
					if not computequery(enreg.get(key, None), value):
						counter = False
						break
				elif enreg.get(key, False):
					if isstring(enreg[key]):
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
				yield enreg

	def sync(self):
		self.db.sync()

	def close(self):
		self.sync()

	def __del__(self):
		self.sync()

	def __unicode__(self):
		return self.name

	def __str__(self):
		return self.name
