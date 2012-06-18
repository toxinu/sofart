#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
import uuid

from .exceptions import CollectionError

class Collection(object):
	def __init__(self, name, path, db):
		self.name = name
		self.path = path
		self.entries = db.db[self.name]
		self.db = db

	def total_entries(self):
		return len(self.entries)

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
			
	def save(self, record):
		if not isinstance(record, dict):
			raise CollectionError('Save is not valid')

		self.db.save(record, self.name)

		#record_id = str(uuid.uuid4())
		#record.update({'_id': record_id})
		#print(' :: record_id : %s' % record_id)
		#print(' :: record    : %s' % record)
		#if self.db.mode == "single":
		#	self.db.db[self.name] += [record]
		#	self.db.add_id(record_id)

		#elif self.db.mode == "multi":
		#	tmp = self.entries
		#	tmp.append(record)
		#	self.update(tmp)
		#	self.db.add_id(record_ir)
		#	del tmp
		#del record

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

	def sync(self):
		if self.db.mode == 'single':
			pickle.dump(self.db.db, open(self.path, 'w'))

	def close(self):
		self.sync()

	#def __del__(self):
	#	self.sync()