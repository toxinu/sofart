======
Sofart
======

Quick and dirty python embedded and non-relationnal database.  
For production and test, heavly inspired by `Mongodb <http://www.mongodb.org/>`_.  
Use Pickle for storage.

Installation
------------

Not yet available on pypi. So do it with source.::

	pip install sofart

Example
-------

Easy use: ::

	>>> from sofart import Database

Create Database and a collection: ::

	>>> db = Database('/tmp/so.fart')
	>>> db.new_collection('test_collection')
	>>> db.collections
	['test_collection']

Play with collection: ::

	>>> c = db.get('test_collection')
	>>> post = {
	...             "artist": "Jambon",
	...             "track": "I love my jambon"}
	>>> c.save(post)
	>>> c.find_one()
	{'track': 'I love my jambon', '_id': 'b2d6bf60-6c11-4e26-9357-efb28056e60d', 'artist': 'Jambon'}
	
Some filter: ::

	>>> c.find_one({"artist": "Jambon"})
	{'track': 'I love my jambon', '_id': 'b2d6bf60-6c11-4e26-9357-efb28056e60d', 'artist': 'Jambon'}
	>>> c.find_one({"artist":"Bieber"})
	>>>

Docs
----

class Database
==============

attributs ::

	path        				: Return database path
	collections 				: Return database collections list

methods ::

	new_collection(str(name))  	: Create new collection
	drop_collection(str(name))	: Drop collection
	get_collections()          	: Return database collections list (same as `collections` attribut)
	get(str(name))             	: Return `Collection` object

class Collection
================

attributs ::

	name : return collection name

methods ::

	save(dict(enreg))   		: Save entrie into collection
	remove(str(_id))      		: Remove entrie from collection
	find_one(dict(query), bool(case_sensitive))      : Return first founded result
	find(dict(query), bool(case_sensitive), int(nb)) : Return `nb` result founded
