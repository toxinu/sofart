db_path = '/tmp/so.fart'
mode = 'single'

from sofart import Database
import pickle

d = Database(db_path, mode=mode)
d.drop_collection('test')
d.drop_collection('test2')
d.close
del d
_db = pickle.load(open(db_path))
if 'test' in _db['index']['collections']:
	raise Exception('Database not empty (drop failure)')
if 'test2' in _db['index']['collections']:
	raise Exception('Database not empty (drop failure)')
if len(_db['index']['ids']) > 0:
	raise Exception('Ids index is not empty')
