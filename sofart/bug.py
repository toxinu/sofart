import uuid

def test(record):
	record_list = []

	record_id = str(uuid.uuid4())
	record['_id'] = record_id
	record_list.append(record_id)
	return record_list, record

record_list, record = test({"jambon": "god"})

print(' :: record_list : %s' % record_list)
print(' :: record      : %s' % record)