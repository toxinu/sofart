======
Sofart
======

Python in-memory embedded and non-relationnal database.

For production and test, heavly inspired by `Mongodb <http://www.mongodb.org/>`_.

There are three serializers at this time, ``msgpack``, ``Pickle`` and ``Json`` for storage.

Sofart can be use out-of-memory with ``multi`` mode but it's very not encourage. Perfomances are so bad.

	Sofart is Python 3 ready.

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
	>>> db.get_collections()
	['test_collection']

Play with collection: ::

	>>> c = db.get('test_collection')
	>>> post = {    "artist": "Jambon",
	...             "track": "I love my jambon"}
	>>> c.save(post)
	>>> for i in c.find_one():
	...     print(i)
	...
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

You can run test under ``tests/test_sofart.py``.  
And there is a populate script into ``tests/populate.py``.  

Performances
------------

Performances are certainly ridiculous for ``multi``, see `BENCH <https://raw.github.com/Socketubs/Sofart/master/BENCH>`_.	

	Single(in-memory) is higlhy faster than ``multi`` cause it's mainly work in RAM and just down data when sync method is called.  
	In otherwise ``multi`` down data at each request.

But you can have a pretty data control with ``sync`` method which down data in file when you call it.

Misc.
-----

You can easily write your own serializer, have a look at ``serializers/_msgpack.py`` or ``_json.py`` file.

Remember that if someone write Ruby or other language driver for sofart, maybe using ``msgpack`` could be a good idea.

Docs
----

class Database
==============

*constructor* ::

    Database(str(path), str(mode), str(serializer)) : Path is database file path
                                                    : Mode is single or multi (Default: `single`)
                                                    : Serializer like msgpack, json or pickle (Default: `msgpack`)

*attributs* ::

    path        : Return database path

*methods* ::

    new_collection(str(name))        : Create new collection
    drop_collection(str(name))       : Drop collection
    rename(str(name), str(new_name)) : Rename collection `name` to `new_name`
    get_collections() : Return database collections list (same as `collections` attribut)
    get(str(name))    : Return `Collection` object
    count()           : Return total database entries
    sync()            : Save every changes in database file

class Collection
================

*attributs* ::

    name : Return collection name

*methods* ::

    drop()            : Drop collection
    count()           : Return total collection entries
    save(dict(enreg)) : Save entrie into collection
    remove(str(_id))  : Remove entrie from collection
    sync()            : Save every changes in database file
    rename(str(name)) : Rename collection to `name`
    find_one(dict(query), bool(case_sensitive))      : Return first founded result
    find(dict(query), bool(case_sensitive), int(nb)) : Iterator which return `nb` result founded

Query
-----

At this moment just following operands are available:

- ``<``
- ``<=``
- ``>``
- ``>=``
- ``all``
- ``exists``
- ``mod``
- ``ne``
- ``in``
- ``nin``

This is an example: ::

	>>> c.save({"value": 2})
	>>> c.find({"value": {"$exists": True}})
	[{'_id': '47e53aea-85b4-434b-8961-40e89c877b41', 'value': 2}]
	>>> c.find({"value": {"$in": [2, 3, 67]}})
	[{'_id': '47e53aea-85b4-434b-8961-40e89c877b41', 'value': 2}]
	>>> c.find({"value" : { "$gt": 1 }})
	[{'_id': '42567296-7d78-43b7-a4e0-50447b80eca8', 'value': 2}]

And another: ::

	>>> c.find({"value" : { "$gte": 2 }})
	[{'_id': '42567296-7d78-43b7-a4e0-50447b80eca8', 'value': 2}]
	>>> c.find({"value" : { "$gte": 2, "$lt" : 1 }})
	[]
	>>> c.find({"value": {"$mod": [2, 0]}})
	[{'_id': '47e53aea-85b4-434b-8961-40e89c877b41', 'value': 2}]

More informations `here <http://www.mongodb.org/display/DOCS/Advanced+Queries#AdvancedQueries>`_.

See `LICENSE <https://raw.github.com/Socketubs/Sofart/master/LICENSE>`_.
