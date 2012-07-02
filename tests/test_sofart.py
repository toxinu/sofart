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
		d.sync()

		_db = _serializer.load()
		self.assertNotIn('test', _db)
		self.assertNotIn('test2', _db)
		self.assertFalse(_db['_infos']['total_entries'] > 0, msg='Ids index is not empty')

	def test002_new_collection(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		d.new_collection('test')
		self.assertIn('test', d.get_collections(), msg='Collection not created')
		d.sync()
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
		d.sync()
		_db = _serializer.load()

	def test010_countcollectionenreg(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		c = d.get('test')
		post = { 
			"artist": "Jambon",
			"music": "I love jambon"}	
		c.save(post)
		c.save(post)
		self.assertEqual(c.count(), 2, msg='Data lose (%s)' % c.count())

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
		self.assertEqual(d.count(), 4, msg='Data lose (%s)' % d.count())

	def test012_basicoperand(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		c = d.get('test')
		c.save({'value': 2, 'value2': 150})
		r = c.find_one({'value': {'$gt': 1, '$lte': 2 }})
		self.assertTrue(r, msg='BasicOperand failed')
		r = c.find_one({'value': {'$gt': 1, '$lte': 2 },
						'value2':{'$gte': 150, '$lt': 2000 }})
		self.assertTrue(r, msg='BasicOperand failed')
		r = c.find_one({'value': {'$gt': 3, '$lte': 2 },
						'value2':{'$gte': 150, '$lt': 2000 }})
		self.assertFalse(r, msg='BasicOperand failed')

	def test013_alloperand(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		c = d.get('test')
		c.save({'test013': [1,2,3]})
		r = c.find_one({'test013': { "$all": [2,3,4] }})
		self.assertFalse(r, msg='AllOperand failed')
		r = c.find_one({'test013': { "$all": [2,3] }})
		self.assertTrue(r, msg='AllOperand failed')

	def test014_existsoperand(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		c = d.get('test')
		r = [i for i in c.find({'test013': {"$exists": True }})]
		self.assertTrue(r, msg='ExistsOperand failed')
		r = [i for i in c.find({'test013': {"$exists": False }})]
		self.assertTrue(r, msg='ExistsOperand failed')
		r = [i for i in c.find({'test080123': {"$exists": True }})]
		self.assertFalse(r, msg='ExistsOperand failed')
		r = [i for i in c.find({'test080123': {"$exists": False }})]
		self.assertTrue(r, msg='ExistsOperand failed')
		r = c.find_one({'test013': { "$all": [2,3,4], "$exists": False }})
		self.assertFalse(r, msg='ExistsOperand failed')

	def test015_modulooperand(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		c = d.get('test')
		r = [i for i in c.find({'value': {"$mod": [2, 0]}})]
		self.assertTrue(r, msg='Modulo operand failed')
		r = [i for i in c.find({'value2': {"$mod": [60, 30]}})]
		self.assertTrue(r, msg='Modulo operand failed')
		r = [i for i in c.find({'value2': {"$mod": [60, 25]}})]
		self.assertFalse(r, msg='Modulo operand failed')
		
	def test016_neoperand(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		c = d.get('test')
		r = [i for i in c.find({'value': {"$ne": 2}})]
		self.assertFalse(r, msg='Modulo operand failed')
		r = [i for i in c.find({'value': {"$ne": 3}})]
		self.assertTrue(r, msg='Modulo operand failed')

	def test017_inoperand(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		c = d.get('test')
		c.save({"test017": [1,2,5]})
		r = [i for i in c.find({'test017': {'$in': [1,6,9]}})]
		self.assertTrue(r, msg='In operand failed')
		r = [i for i in c.find({'test017': {'$in': [1,2,9]}})]
		self.assertTrue(r, msg='in operand failed')
		r = [i for i in c.find({'test017': {'$in': [6,120,9]}})]
		self.assertFalse(r, msg='In operand failed')
		c.save({"test017": 1})
		r = [i for i in c.find({'test017': {'$in': [1,6,9]}})]
		self.assertTrue(r, msg='In operand failed')

	def test018_ninoperand(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		c = d.get('test')
		c.save({"test017": [1,2,5]})
		r = [i for i in c.find({'test017': {'$nin': [1,6,9]}})]
		self.assertFalse(r, msg='Nin operand failed')
		r = [i for i in c.find({'test017': {'$nin': [1,2,9]}})]
		self.assertFalse(r, msg='Nin operand failed')
		r = [i for i in c.find({'test017': {'$nin': [6,120,9]}})]
		self.assertTrue(r, msg='Nin operand failed')
		c.save({"test017": 1})
		r = [i for i in c.find({'test017': {'$nin': [1,6,9]}})]
		self.assertFalse(r, msg='Nin operand failed')

	def test019_renameviacollection(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		d.new_collection('test19')
		c = d.get('test19')
		c.save({'test123': 123})
		c.rename('test19_')
		r = c.find_one({'test123': 123})
		self.assertTrue(r, msg='Save lost after rename')
		self.assertEqual(c.name, 'test19_', msg='Name not valid')

	def test020_renameviadatabase(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		d.rename('test19_', 'test19')
		c = d.get('test19')
		r = c.find_one({'test123': 123})
		self.assertTrue(r, msg='Save lost after rename')
		self.assertEqual(c.name, 'test19', msg='Name not valid')

	def test021_drop(self):
		d = Database(db_path, mode=mode, serializer=serializer)
		d.new_collection('test021')
		c = d.get('test021')
		c.drop()
		self.assertFalse('test021' in d.get_collections(), msg='Nin operand failed')
		d.new_collection('test021')
		d.drop_collection('test021')
		self.assertFalse('test021' in d.get_collections(), msg='Nin operand failed')

	def test099_clean(self):
		if clean:
			os.remove(db_path)

if __name__ == '__main__':
    unittest.main()
