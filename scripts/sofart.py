#!/usr/bin/env python
import cmd
import readline
import sys
from sofart import Database

db = Database(sys.argv[1])

class SofartCli(cmd.Cmd):
	"""Sofart Client."""
	def __init__(self):
		cmd.Cmd.__init__(self)
		self.prompt = '%s >> ' % sys.argv[1]

	def do_collections(self, line):
		"""Show collections"""
		collections = db.get_collections()
		for collection in collections:
			print(collection)

	def do_current(self, line):
		"""Show current collection"""
		print(self.c.name)

	def do_use(self, name):
		"""Use collection"""
		try:
			self.c = db.get(name)
		except:
			print('Collection not exist')

	def do_find(self, query):
		"""Find in a collection
		find {'key': 'value'}
		"""
		if query:
			query = eval(query)
		else:
			query = {}
		if not isinstance(query, dict):
			print('Must be a python dict object')
			exit(1)
		for result in self.c.find(query):
			print(result)

	def do_EOF(self, line):
		return True

	def postloop(self):
		print()

if __name__ == '__main__':
	SofartCli().cmdloop()
