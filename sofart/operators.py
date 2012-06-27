# -*- coding: utf-8 -*-

from .exceptions import QueryError

_01 = ['gt','lt','gte','lte']
_02 = []

_ops = _01 + _02

def isadvancedquery(value, query):
	if isinstance(query, dict):
		for key in query.keys():
			if isinstance(key, str) or isinstance(key, unicode):
				if key[0] == "$":
					if key[1:] in _ops:
						return True
	return False

def computequery(value, query):
	for key in query.keys():
		_key = key[1:]
		if _key == "gt":
			if not (value > query[key]):
				return False
		if _key == "lt":
			if not (value < query[key]):
				return False
		if _key == "gte":
			if not (value >= query[key]):
				return False
		if _key == "lte":
			if not (value <= query[key]):
				return False
	return True
