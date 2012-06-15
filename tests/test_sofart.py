#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import sys
import os
sys.path.insert(0, os.path.abspath('..'))

from sofart import Database

db_path = '/tmp/test_sofart.db'

class TestSetup(object):
	def setUp(self):
		pass
#		d = Database(db_path)
#		d.drop_collection('test')

class EmbTestSuite(TestSetup, unittest.TestCase):
	def test_01_newdb(self):
		d = Database(db_path)	

	def test_02_new_collection(self):
		d = Database(db_path)
		d.new_collection('test')
		if not 'test' in d.collections:
			raise Exception('Collection not created')

	def test_03_getcollection(self):
		d = Database(db_path)
		c = d.get('test')

	def test_04_addenreg(self):
		d = Database(db_path)
		c = d.get('test')
		post = { 
			"artist": "Jambon",
			"music": "I love jambon"}	
		c.save(post)

	def test_05_listenreg(self):
		d = Database(db_path)
		c = d.get('test')
		r = c.find_one()
		if not r:
			raise Exception('Enreg not found')
	
	def test_06_listnoenreg(self):
		d = Database(db_path)
		c = d.get('test')
		r = c.find_one({"artist": "Jambon22"})
		if r:
			raise Exception('Enreg found')

	def test_07_nosensitive(self):
		d = Database(db_path)
		c = d.get('test')
		r = c.find_one({"artist": "JambON", case_sensitive=False})
		if not r:
			raise Exception('Non-sensitive failed')

	def test_08_sensitive(self):
		d = Database(db_path)
		c = d.get('test')
		r = c.find_one({"artist": "JamBOn", case_sensitive=True})
		if r:
			raise Exception('Sensitive failed')

	def test_09_removeenreg(self):
		d = Database(db_path)
		c = d.get('test')
		r = c.find_one({"artist": "Jambon"})['_id']
		c.remove(r)
		if not c.find_one({"artist": "Jambon"}):
			raise Exception('Enreg not removed')

if __name__ == '__main__':
    unittest.main()
