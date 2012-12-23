#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid
import sys
import isit

from copy import copy

from sofart.operators import isadvancedquery
from sofart.operators import computequery
from sofart.exceptions import CollectionException

if isit.py2:
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

	def rename(self, name):
		if name in self.db.collection_names():
			raise CollectionException('Collection name already taken')
		if self.db.mode == "multi":
			tmp = self.db.db
			tmp[name] = tmp.pop(self.name)
			self.db._update(tmp)
			del tmp
		elif self.db.mode == "single":
			self.db.db[name] = self.db.db.pop(self.name)
		self.name = name

	def _update(self, new_collection):
		if not isinstance(new_collection, list):
			raise CollectionException("Collection update can't be empty")
		try:
			if self.db.mode == "multi":
				tmp = self.db.db
				tmp[self.name] = new_collection
				self.db.serializer.dump(tmp)
				del tmp
			elif self.db.mode == "single":
				self.db.db[self.name] == new_collection
		except Exception as err:
			raise CollectionException('Seems to be invalid (%s)' % err)

	def save(self, record):
		if not isinstance(record, dict):
			raise CollectionException('Save is not valid')

		record = copy(record)
		if not record.get('_id', False):
			record_id = str(uuid.uuid4())
			record['_id'] = record_id
		else:
			if [rec['_id'] for rec in self.entries if rec['_id'] == record['_id']]:
				raise CollectionException('Id already taken')
			else:
				record_id = record['_id']

		if self.db.mode == "single":
			self.entries.append(record)
			self.db._add_id(record_id)
		elif self.db.mode == "multi":
			tmp = self.entries
			tmp.append(record)
			self._update(tmp)
			self.db._add_id(record_id)
			del tmp
		del record
		return record_id

	def remove(self, enreg_id):
		if self.db.mode == "multi":
			tmp = self.entries
			tmp[:] = [d for d in tmp if d.get('_id') != enreg_id]
			self._update(tmp)
			self.db._del_id(enreg_id)
		elif self.db.mode == "single":
			self.entries[:] = [d for d in self.entries if d.get('_id') != enreg_id]
			self.db._del_id(enreg_id)

	def find_one(self, query={}, case_sensitive=False):
		for r in self.find(query=query, nb=1, case_sensitive=case_sensitive):
			if not r:
				return None
			else:
				return copy(r)

	def find(self, query={}, nb=50, case_sensitive=False):
		if not isinstance(query, dict):
			raise CollectionException('Query must be dict')
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
				yield copy(enreg)

	def drop(self):
		self.db.drop_collection(self.name)

	def sync(self):
		self.db.sync()
