#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import sys
import os


try:
	from sofart import Database
except:
	print('You need to install sofart before')
	sys.exit(1)

from sofart import Database

#####################################################################################
# Configuration
#####################################################################################

#serializer = 'pickle'
#serializer = 'json'
serializer = 'msgpack'

db_path = './so.fart.%s.db' % serializer
mode = 'single'

clean = True

#####################################################################################
#####################################################################################

_serializer = __import__("sofart.serializers._%s" % serializer)
_serializer = sys.modules["sofart.serializers._%s" % serializer]
_serializer = _serializer.Serializer(db_path)

class TestSetup(object):
	def setUp(self):
		pass

class EmbTestSuite(TestSetup, unittest.TestCase):
	def test_01_newdb(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		d.drop_collection('test')
		d.drop_collection('test2')
		self.assertNotIn('test', d.collections, msg='Database not empty (drop failure)')
		self.assertNotIn('test2', d.collections, msg='Database not empty (drop failure)')
		d.close()

		_db = _serializer.load()
		self.assertNotIn('test', _db['index']['collections'])
		self.assertNotIn('test2', _db['index']['collections'])
		self.assertFalse(len(_db['index']['ids']) > 0, msg='Ids index is not empty')

	def test_02_new_collection(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		d.new_collection('test')
		self.assertIn('test', d.collections, msg='Collection not created')
		d.close()
		_db = _serializer.load()
		self.assertFalse(len(_db['index']['ids']) > 0, msg='Ids index is not empty')

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
		self.assertTrue(r, msg='Enreg not found')
	
	def test_06_listnoenreg(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		c = d.get('test')
		r = c.find_one({"artist": "Jambon22"})
		self.assertFalse(r, msg='Enreg found')

	def test_07_nosensitive(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		c = d.get('test')
		r = c.find_one({"artist": "JambON"}, case_sensitive=False)
		self.assertTrue(r, msg='Non-sensitive failed')

	def test_08_sensitive(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		c = d.get('test')
		r = c.find_one({"artist": "JamBOn"}, case_sensitive=True)
		self.assertFalse(r, msg='Sensitive failed')

	def test_09_removeenreg(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		c = d.get('test')
		r = c.find_one({"artist": "Jambon"})['_id']
		c.remove(r)
		r = c.find_one({"artist": "Jambon"})
		self.assertFalse(r, msg='Enreg not removed')
		d.close()
		_db = _serializer.load()
		self.assertNotIn(r, _db['index']['ids'], msg='Ids not removed in index')

	def test_10_countcollectionenreg(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		c = d.get('test')
		post = { 
			"artist": "Jambon",
			"music": "I love jambon"}	
		c.save(post)
		c.save(post)
		self.assertEqual(c.total_entries(), 2, msg='Data lose (%s)' % c.total_entries())

	def test_11_countdbenreg(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		d.new_collection('test2')
		c = d.get('test2')
		post = { 
			"artist": "Jambon",
			"music": "I love jambon"}	
		post2 = { 
			"artist": "Jambon",
			"music": "I love jambon2"}	
		c.save(post)
		c.save(post2)
		self.assertEqual(d.total_entries(), 4, msg='Data lose (%s)' % d.total_entries())

	def test_99_clean(self):
		if clean:
			os.remove(db_path)

if __name__ == '__main__':
    unittest.main()
