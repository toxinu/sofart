#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import sys
import os


try:
	from sofart.backends import _json
except:
	print('You need to install sofart before')
	sys.exit(1)

from sofart import Database

db_path = './so.fart.db'
mode = 'single'
serializer = 'pickle'

_backend = __import__("sofart.backends.%s" % serializer)
_backend = sys.modules["sofart.backends.%s" % serializer]
backend = _backend.Backend(db_path)

class TestSetup(object):
	def setUp(self):
		pass

class EmbTestSuite(TestSetup, unittest.TestCase):
	def test_01_newdb(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		d.drop_collection('test')
		d.drop_collection('test2')
		if 'test' in d.collections:
			raise Exception('Database not empty (drop failure)')
		if 'test2' in d.collections:
			raise Exception('Database not empty (drop failure)')
		d.close()

		_db = backend.load()
		if 'test' in _db['index']['collections']:
			raise Exception('Database not empty (drop failure)')
		if 'test2' in _db['index']['collections']:
			raise Exception('Database not empty (drop failure)')
		if len(_db['index']['ids']) > 0:
			raise Exception('Ids index is not empty')

	def test_02_new_collection(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		d.new_collection('test')
		if not 'test' in d.collections:
			raise Exception('Collection not created')
		d.close()
		_db = backend.load()
		if len(_db['index']['ids']) > 0:
			raise Exception('Ids index is not empty')

	def test_03_getcollection(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		c = d.get('test')

	def test_04_addenreg(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		c = d.get('test')
		post = { 
			"artist": "Jambon",
			"music": "I love jambon"}	
		c.save(post)

	def test_05_listenreg(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		c = d.get('test')
		r = c.find_one()
		if not r:
			raise Exception('Enreg not found')
	
	def test_06_listnoenreg(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		c = d.get('test')
		r = c.find_one({"artist": "Jambon22"})
		if r:
			raise Exception('Enreg found')

	def test_07_nosensitive(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		c = d.get('test')
		r = c.find_one({"artist": "JambON"}, case_sensitive=False)
		if not r:
			raise Exception('Non-sensitive failed')

	def test_08_sensitive(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		c = d.get('test')
		r = c.find_one({"artist": "JamBOn"}, case_sensitive=True)
		if r:
			raise Exception('Sensitive failed')

	def test_09_removeenreg(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		c = d.get('test')
		r = c.find_one({"artist": "Jambon"})['_id']
		c.remove(r)
		if c.find_one({"artist": "Jambon"}):
			raise Exception('Enreg not removed')
		d.close()
		_db = backend.load()
		if r in _db['index']['ids']:
			raise Exception('Ids not removed in index')

	def test_10_countcollectionenreg(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		c = d.get('test')
		post = { 
			"artist": "Jambon",
			"music": "I love jambon"}	
		c.save(post)
		c.save(post)
		if c.total_entries() != 2:
			raise Exception('Data lose (%s)' % c.total_entries())

	def test_11_countdbenreg(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		d.new_collection('test2')
		c = d.get('test2')
		post = { 
			"artist": "Jambon",
			"music": "I love jambon"}	
		post2 = { 
			"artist": "Jambon",
			"music": "I love jambon"}	
		c.save(post)
		c.save(post2)
		if d.total_entries() != 4:
			raise Exception('Data lose (%s)' % d.total_entries())

if __name__ == '__main__':
    unittest.main()
