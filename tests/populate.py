#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid
import time
import os
import sys

from sofart import Database

if sys.version < '3':
  import codecs
  def u(x):
    return codecs.unicode_escape_decode(x)[0]
else:
  def u(x):
    return x

mode = "single"
serializer = "json"
db_path = './sofart-test.db'
nb_collection = 10
nb_entrie_per_collection = 5000
entrie = {"sada123123123": True, u("It's just mind-blowingly awesome. I apologize, and I wish I was more articulate, but it's hard to be articulate when your mind's blownéé 4but in a very good way."): '123123_Dzajkdjazjdazhdhjazjkdhajzk', 'Haricot': "I saw for the first time the earth's shape. I could easily see the shores of continents, islands, great rivers, folds of the terrain, large bodies of water. The horizon is dark blue, smoothly turning to black. . . the feelings which filled me I can express with one word\xe2\x80\x94joy.", 'Jambon': 'Godness'}

def populate_collection(db, collection, entrie):
    c = db[collection]
    for i in range(nb_entrie_per_collection):
        c.save(entrie)

def worker(db):
    for i in range(nb_collection):
        db.create_collection(str(uuid.uuid4()))

    for i in db.collection_names():
        populate_collection(db, i, entrie)

if __name__=="__main__":
    print(' :: Collections            : %s' % nb_collection)
    print(' :: Entrie per collection  : %s' % nb_entrie_per_collection)
    #print(' :: Entrie style         :\n %s' % entrie)
    db = Database(path=db_path, mode=mode, serializer=serializer)
    start_time = time.time()
    worker(db)

    total_time = time.time() - start_time
    print(' :: Total in second        : %s' % total_time)
    print(' :: Second per entrie      : %s' % (total_time/(nb_collection*nb_entrie_per_collection)))
    total_entries = 0
    for c in db.collection_names():
        total_entries += db[c].count()
    print(' :: Total database entries : %s' % total_entries)
 #   os.remove(db_path)
