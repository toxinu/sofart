#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sofart import Database
import uuid
import time
import os
import threading

worker_nb = 5
mode = "single"
serializer = "msgpack"
db_path = './sofart-test.db'
nb_collection = 2
nb_entrie_per_collection = 1000
entrie = {	"Jambon": "Godness", 
			"Haricot": "I saw for the first time the earth's shape. I could easily see the shores of continents, islands, great rivers, folds of the terrain, large bodies of water. The horizon is dark blue, smoothly turning to black. . . the feelings which filled me I can express with one word—joy.",
			"It's just mind-blowingly awesome. I apologize, and I wish I was more articulate, but it's hard to be articulate when your mind's blown—but in a very good way.": "123123_Dzajkdjazjdazhdhjazjkdhajzk"}

def connection(db_path, mode):
	return Database(db_path, mode=mode)

def new_collection(db):
	db.new_collection(str(uuid.uuid4()))

def populate_collection(db, collection, entrie):
	c = db.get(collection)
	for i in range(nb_entrie_per_collection):
		c.save(entrie)

def worker(mode, db_path, serializer):
	db = Database(path=db_path, mode=mode, serializer=serializer)
	for i in range(nb_collection):
		new_collection(db)

	for i in db.collections:
		populate_collection(db, i, entrie)

	db.sync()

if __name__=="__main__":
	if os.path.exists(db_path):
		os.remove(db_path)
	print(' :: Collections            : %s' % nb_collection)
	print(' :: Entrie per collection  : %s' % nb_entrie_per_collection)
	#print(' :: Entrie style         :\n %s' % entrie)
	start_time = time.time()
	print(' :: Start %s worker(s)' % worker_nb) 
	for i in range(worker_nb):
		t = threading.Thread(target=worker, args=(mode, db_path, serializer))
		t.start()

	total_time = time.time() - start_time
	db = Database(path=db_path, mode=mode, serializer=serializer)
	print(' :: Total in second        : %s' % total_time)
	print(' :: Second per entrie      : %s' % (total_time/(nb_collection*nb_entrie_per_collection)))
	#print(' :: Total entries per collection : %s' % c.total_entries())
	print(' :: Total database entries : %s' % db.total_entries())
