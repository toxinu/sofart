======
Sofart
======

.. image:: https://secure.travis-ci.org/socketubs/sofart.png?branch=master
        :target: https://travis-ci.org/socketubs/sofart

Python in-memory embedded and non-relational database.

For development and test, heavily inspired by `Mongodb <http://www.mongodb.org/>`_.

There are three serializers at this time, ``msgpack``, ``Pickle`` and ``Json`` for storage.

Sofart can be use in-memory synced with ``multi`` mode..

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
	>>> db.create_collection('test_collection')
	>>> db.collection_names()
	['test_collection']

Play with collection: ::

	>>> c = db.test_collection
	>>> post = {"artist": "Jambon",
	...         "track": "I love my jambon"}
	>>> c.save(post)
	>>> for i in c.find_one():
	...     print(i)
	...
	{'track': 'I love my jambon', '_id': 'b2d6bf60-6c11-4e26-9357-efb28056e60d', 'artist': 'Jambon'}
	>>> c.remove('b2d6bf60-6c11-4e26-9357-efb28056e60d')
	>>> c.find_one()

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

	Single(in-memory) is highly faster than ``multi`` cause it's mainly work in RAM and just down data when sync method is called.
	In otherwise ``multi`` down data at each request.

But you can have a pretty data control with ``sync`` method which down data in file when you call it.

Serializers
-----------

========== === === ====
Serializer Py2 Py3 Pypy
========== === === ====
Json        1   1   1
MsgPack     1   1   X
Pickle      1   1   1
========== === === ====

Pypy and ``msgpack-pure`` are not supported.

Misc.
-----

You can easily write your own serializer, have a look at ``serializers/_msgpack.py`` or ``_json.py`` file.

Remember that if someone write Ruby or other language driver for sofart, maybe using ``json`` or ``msgpack`` could be a good idea.

Docs
----

class Database
==============

*constructor* ::

    Database(str(path), str(mode), str(serializer)) : Path is database file path
                                                    : Mode is single or multi (Default: `single`)
                                                    : Serializer like msgpack, json or pickle (Default: `json`)

*attributs* ::

    path: Return database path

*methods* ::

    create_collection(str(name))    : Create new collection
    drop_collection(str(name))      : Drop collection
    rename(str(name), str(new_name)): Rename collection `name` to `new_name`
    collection_names(): Return database collections list (same as `collections` attribut)
    count()           : Return total database entries
    sync()            : Save every changes in database file

Retrieve collection with the followings methods:

::

    c = db.my_collection
    c = db['my_collection']

class Collection
================

*attributs* ::

    name: Return collection name

*methods* ::

    drop()           : Drop collection
    count()          : Return total collection entries
    save(dict(enreg)): Save entry into collection
    remove(str(_id)) : Remove entry from collection
    sync()           : Save every changes in database file
    rename(str(name)): Rename collection to `name`
    find_one(spec_or_id)              : Return first founded result
    find(dict(spec_or_id), int(limit)): Iterator which return `limit` result founded (limit=0 return all)

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

See `LICENSE <https://git.socketubs.org/?p=sofart.git;a=blob_plain;f=LICENSE;hb=HEAD>`_.
