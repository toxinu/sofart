======
Sofart
======

Quick and dirty python embedded and non-relationnal database.

Installation
------------

Not yet available on pypi. So do it with source.::

	git clone git://github.com/Socketubs/sofart.git
	cd sofart
	python setup.py install

Example
-------

Easy use: ::

	>>> from sofart import Database

Create Database and a collection: ::

	>>> db = Database('/tmp/my_sofart_database')
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
