======
Sofart
======

Quick and dirty python embedded and non-relationnal database.

| For production and test, heavly inspired by `Mongodb <http://www.mongodb.org/>`_.
| Use Pickle for storage.


| Can be use in ``single`` (default) and ``multi`` user.
| It means real-time sync or "database connection" sync.

Installation
------------

Install with pip: ::

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
	{'track': 'I love my jambon', '_id': 'b2d6bf60-6c11-4e26-9357-efb28056e60d', 'artist': 'Jambon'}$
	>>> c.remove('b2d6bf60-6c11-4e26-9357-efb28056e60d')
	>>> c.find_one()
	>>>

Some filter: ::

	>>> c.find_one({"artist": "Jambon"})
	{'track': 'I love my jambon', '_id': 'b2d6bf60-6c11-4e26-9357-efb28056e60d', 'artist': 'Jambon'}
	>>> c.find_one({"artist":"Bieber"})
	>>>

Tests
-----

You can run test under ``tests/test_test_sofart.py``.  
And there is a populate script into ``tests/populate.py``.  

Performances
------------

| Performances are certainly ridiculous, see `BENCH <https://raw.github.com/Socketubs/Sofart/master/BENCH>`_.	
| Single is higlhy faster than ``multi`` cause it's mainly work in RAM and just down data when database is closed.  
| In otherwise ``multi`` down data at each request.

Todo
----

- Add close database and collection method
- Add save database and collection method

Docs
----

class Database
==============

*constructor* ::

    Database(str(path), str(mode)) : Path is database file path
                                   : Mode is single or multi

*attributs* ::

    path        : Return database path
    collections : Return database collections list

*methods* ::

    new_collection(str(name))  : Create new collection
    drop_collection(str(name)) : Drop collection
    get_collections() : Return database collections list (same as `collections` attribut)
    get(str(name))    : Return `Collection` object
    total_entries()   : Return total database entries

class Collection
================

*attributs* ::

    name : Return collection name

*methods* ::

    total_entries()   : Return total collection entries
    save(dict(enreg)) : Save entrie into collection
    remove(str(_id))  : Remove entrie from collection
    find_one(dict(query), bool(case_sensitive))      : Return first founded result
    find(dict(query), bool(case_sensitive), int(nb)) : Return `nb` result founded

See `LICENSE <https://raw.github.com/Socketubs/Sofart/master/LICENSE>`_.