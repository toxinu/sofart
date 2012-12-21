#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import sys
import os
import re
import isit

try:
    from sofart import Database
except:
    print('You need to install sofart before')
    sys.exit(1)

from sofart import Database

if isit.py25 or isit.py26:
    import unittest2 as unittest

#####################################################################################
# Configuration
#####################################################################################
serializers = ['msgpack','json','pickle']
modes = ['single','multi']
#####################################################################################

class TestSetup(object):
    def setUp(self):
        self.d = Database(db_path, mode=mode, serializer=serializer)

class SofartTest(TestSetup, unittest.TestCase):
    def test001_newdb(self):
        print('=> %s::%s' % (mode,serializer))
        d = Database(db_path, mode=mode, serializer=serializer)
        d.drop_collection('test')
        d.drop_collection('test2')
        self.assertNotIn('test', d.collection_names(), msg='Database not empty (drop failure)')
        self.assertNotIn('test2', d.collection_names(), msg='Database not empty (drop failure)')
        d.sync()

        _db = _serializer.load()
        self.assertNotIn('test', _db)
        self.assertNotIn('test2', _db)
        self.assertFalse(_db['_infos']['total_entries'] > 0, msg='Ids index is not empty')

    def test002_new_collection(self):
        d = Database(db_path, mode=mode, serializer=serializer)
        d.test.save({'key':'value'})
        self.assertIn('test', d.collection_names(), msg='Collection not created')
        d.sync()
        _db = _serializer.load()
        self.assertFalse(_db['_infos']['total_entries'] > 1, msg='Ids index is not empty')

    def test003_getcollection(self):
        d = Database(db_path, mode=mode, serializer=serializer)
        c = d.test

    def test004_addenreg(self):
        d = Database(db_path, mode=mode, serializer=serializer)
        c = d['test']
        post = {
            "artist": "Jambon",
            "music": "I love jambon"}
        c.save(post)
        if mode == "single":
            d.sync()

    def test005_listenreg(self):
        d = Database(db_path, mode=mode, serializer=serializer)
        c = d.test
        r = c.find_one()
        self.assertTrue(r, msg='Enreg not found')

    def test006_listnoenreg(self):
        d = Database(db_path, mode=mode, serializer=serializer)
        c = d['test']
        r = c.find_one({"artist": "Jambon22"})
        self.assertFalse(r, msg='Enreg found')

    def test007_nosensitive(self):
        d = Database(db_path, mode=mode, serializer=serializer)
        c = d['test']
        regexp = re.compile("^JambON",re.IGNORECASE)
        r = c.find_one({"artist": regexp})
        a = c.find()
        self.assertTrue(r, msg='Non-sensitive failed (%s)' % r)

    def test008_sensitive(self):
        d = Database(db_path, mode=mode, serializer=serializer)
        c = d.test
        r = c.find_one({"artist": "JamBOn"})
        self.assertFalse(r, msg='Sensitive failed')

    def test009_removeenreg(self):
        d = Database(db_path, mode=mode, serializer=serializer)
        c = d.test
        r = c.find_one({"artist": "Jambon"})['_id']
        c.remove(r)
        r = c.find_one({"artist": "Jambon"})
        self.assertFalse(r, msg='Enreg not removed')
        d.sync()
        _db = _serializer.load()

    def test010_countcollectionenreg(self):
        d = Database(db_path, mode=mode, serializer=serializer)
        c = d['test']
        post = {
            "artist": "Jambon",
            "music": "I love jambon"}
        c.save(post)
        c.save(post)
        self.assertEqual(len(c.entries), 3, msg='Data lose (%s)' % len(c.entries))

    def test011_countdbenreg(self):
        d = Database(db_path, mode=mode, serializer=serializer)
        c = d.test2
        post = {
            "artist": "Jambon",
            "music": "I love jambon"}
        post2 = {
            "artist": "Jambon",
            "music": "I love jambon2"}
        c.save(post)
        c.save(post2)
        self.assertEqual(len(c.entries), 2, msg='Data lose (%s)' % len(c.entries))

    def test012_basicoperand(self):
        d = Database(db_path, mode=mode, serializer=serializer)
        c = d.test
        c.save({'value': 2, 'value2': 150})
        r = c.find_one({'value': {'$gt': 1, '$lte': 2 }})
        self.assertTrue(r, msg='BasicOperand failed')
        r = c.find_one({'value': {'$gt': 1, '$lte': 2 },
                        'value2':{'$gte': 150, '$lt': 2000 }})
        self.assertTrue(r, msg='BasicOperand failed')
        r = c.find_one({'value': {'$gt': 3, '$lte': 2 },
                        'value2':{'$gte': 150, '$lt': 2000 }})
        self.assertFalse(r, msg='BasicOperand failed')
        if mode == "single":
            d.sync()

    def test013_alloperand(self):
        d = Database(db_path, mode=mode, serializer=serializer)
        c = d.test
        c.save({'test013': [1,2,3]})
        r = c.find_one({'test013': { "$all": [2,3,4] }})
        self.assertFalse(r, msg='AllOperand failed')
        r = c.find_one({'test013': { "$all": [2,3] }})
        self.assertTrue(r, msg='AllOperand failed')
        if mode == "single":
            d.sync()

    def test014_existsoperand(self):
        d = Database(db_path, mode=mode, serializer=serializer)
        c = d.test
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
        c = d['test']
        r = [i for i in c.find({'value': {"$mod": [2, 0]}})]
        self.assertTrue(r, msg='Modulo operand failed')
        r = [i for i in c.find({'value2': {"$mod": [60, 30]}})]
        self.assertTrue(r, msg='Modulo operand failed')
        r = [i for i in c.find({'value2': {"$mod": [60, 25]}})]
        self.assertFalse(r, msg='Modulo operand failed')

    def test016_neoperand(self):
        d = Database(db_path, mode=mode, serializer=serializer)
        c = d['test']
        r = [i for i in c.find({'value': {"$ne": 2}})]
        self.assertFalse(r, msg='Modulo operand failed')
        r = [i for i in c.find({'value': {"$ne": 3}})]
        self.assertTrue(r, msg='Modulo operand failed')

    def test017_inoperand(self):
        d = Database(db_path, mode=mode, serializer=serializer)
        c = d['test']
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
        c = d['test']
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
        c = d.test19
        c.save({'test123': 123})
        c.rename('test19_')
        r = c.find_one({'test123': 123})
        self.assertTrue(r, msg='Save lost after rename')
        self.assertEqual(c.name, 'test19_', msg='Name not valid')
        if mode == "single":
            d.sync()

    def test020_renameviadatabase(self):
        d = Database(db_path, mode=mode, serializer=serializer)
        d.rename('test19_', 'test19')
        c = d.test19
        r = c.find_one({'test123': 123})
        self.assertTrue(r, msg='Save lost after rename')
        self.assertEqual(c.name, 'test19', msg='Name not valid')

    def test021_drop(self):
        d = Database(db_path, mode=mode, serializer=serializer)
        c = d.test021
        c.drop()
        self.assertFalse('test021' in d.collection_names(), msg='Nin operand failed')
        d.create_collection('test021')
        d.drop_collection('test021')
        self.assertFalse('test021' in d.collection_names(), msg='Nin operand failed')

    def test22_boolean(self):
        # Boolean False
        _id = self.d.stuff.save({'read':False})
        self.assertIsNone(self.d.stuff.find_one({'read':True}))
        self.assertEqual(self.d.stuff.find_one({'read':False}), {'read':False,'_id':_id})

        r = 0
        for i in self.d.stuff.find({'read':True}):
            r += 1
        self.assertIs(r, 0)

        r = 0
        for i in self.d.stuff.find({'read':False}):
            r += 1
        self.assertIs(r, 1)
        self.d.stuff.remove(_id)

        # Boolean True
        _id = self.d.stuff.save({'read':True})
        self.assertIsNone(self.d.stuff.find_one({'read':False}))
        self.assertEqual(self.d.stuff.find_one({'read':True}), {'read':True,'_id':_id})

        r = 0
        for i in self.d.stuff.find({'read':False}):
            r += 1
        self.assertIs(r, 0)

        r = 0
        for i in self.d.stuff.find({'read':True}):
            r += 1
        self.assertIs(r, 1)

    def test23_boolean_and_other(self):
        # Boolean False with string
        _id = self.d.stuff.save({'read':False,'string':'Yeah'})
        _enreg = {'read':False,'string':'Yeah','_id':_id}
        self.assertIsNone(self.d.stuff.find_one({'read':True,'string':'Yeah'}))
        self.assertIsNone(self.d.stuff.find_one({'read':True,'string':'Yo'}))
        self.assertIsNone(self.d.stuff.find_one({'read':False,'string':'Yo'}))

        self.assertEqual(self.d.stuff.find_one({'read':False,'string':'Yeah'}), _enreg)
        self.assertEqual(self.d.stuff.find_one({'string':'Yeah'}), _enreg)
        self.assertEqual(self.d.stuff.find_one({'read':False}), _enreg)

    def test24_remove_during_find(self):
        self.d.stuff.save({'read':False, 'name':'socketubs'})
        self.d.stuff.save({'read':True, 'bike':'jambon'})

        c = 0
        for i in self.d.stuff.find():
            self.d.stuff.remove(i['_id'])
            c += 1
        if mode == "multi":
            self.assertEqual(c, 4)
        else:
            self.assertEqual(c, 2)

    def test25_find_with_id(self):
        _id = self.d.stuff.save({'key':'value'})
        self.assertIsNone(self.d.stuff.find_one('1233212-123123'))
        self.assertEqual(self.d.stuff.find_one(_id), {'key':'value','_id':_id})

        c = 0
        for i in self.d.stuff.find('123123543'):
            c += 1
        self.assertEqual(c, 0)

        c = 0
        for i in self.d.stuff.find(_id):
            c += 1
        self.assertEqual(c, 1)

if __name__ == '__main__':
    for mode in modes:
        for serializer in serializers:
            db_path = './so.fart.%s.db' % serializer
            if os.path.exists(db_path):
                os.remove(db_path)
            _serializer = __import__("sofart.serializers._%s" % serializer)
            _serializer = sys.modules["sofart.serializers._%s" % serializer]
            _serializer = _serializer.Serializer(db_path)
            unittest.main(exit=False)
    sys.exit(0)
