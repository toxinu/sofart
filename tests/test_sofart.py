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

serializer = 'msgpack'
#serializer = 'json'
#serializer = 'pickle'

db_path = './so.fart.%s.db' % serializer
mode = 'multi'

clean = True
#clean = False

#####################################################################################
#####################################################################################

_serializer = __import__("sofart.serializers._%s" % serializer)
_serializer = sys.modules["sofart.serializers._%s" % serializer]
_serializer = _serializer.Serializer(db_path)

class TestSetup(object):
	def setUp(self):
		pass

class EmbTestSuite(TestSetup, unittest.TestCase):
	def test001_newdb(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		d.drop_collection('test')
		d.drop_collection('test2')
		self.assertNotIn('test', d.get_collections(), msg='Database not empty (drop failure)')
		self.assertNotIn('test2', d.get_collections(), msg='Database not empty (drop failure)')
		d.close()

		_db = _serializer.load()
		self.assertNotIn('test', _db)
		self.assertNotIn('test2', _db)
		self.assertFalse(_db['_infos']['total_entries'] > 0, msg='Ids index is not empty')

	def test002_new_collection(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		d.new_collection('test')
		self.assertIn('test', d.get_collections(), msg='Collection not created')
		d.close()
		_db = _serializer.load()
		self.assertFalse(_db['_infos']['total_entries'] > 0, msg='Ids index is not empty')

	def test003_getcollection(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		c = d.get('test')

	def test004_addenreg(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		c = d.get('test')
		post = { 
			"artist": "Jambon",
			"music": "I love jambon"}	
		c.save(post)

	def test005_listenreg(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		c = d.get('test')
		r = c.find_one()
		self.assertTrue(r, msg='Enreg not found')
	
	def test006_listnoenreg(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		c = d.get('test')
		r = c.find_one({"artist": "Jambon22"})
		self.assertFalse(r, msg='Enreg found')

	def test007_nosensitive(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		c = d.get('test')
		r = c.find_one({"artist": "JambON"}, case_sensitive=False)
		a = c.find()
		self.assertTrue(r, msg='Non-sensitive failed (%s)' % r)

	def test008_sensitive(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		c = d.get('test')
		r = c.find_one({"artist": "JamBOn"}, case_sensitive=True)
		self.assertFalse(r, msg='Sensitive failed')

	def test009_removeenreg(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		c = d.get('test')
		r = c.find_one({"artist": "Jambon"})['_id']
		c.remove(r)
		r = c.find_one({"artist": "Jambon"})
		self.assertFalse(r, msg='Enreg not removed')
		d.close()
		_db = _serializer.load()

	def test010_countcollectionenreg(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		c = d.get('test')
		post = { 
			"artist": "Jambon",
			"music": "I love jambon"}	
		c.save(post)
		c.save(post)
		self.assertEqual(c.total_entries(), 2, msg='Data lose (%s)' % c.total_entries())

	def test011_countdbenreg(self):
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

	def test099_clean(self):
		if clean:
			os.remove(db_path)

if __name__ == '__main__':
    unittest.main()
