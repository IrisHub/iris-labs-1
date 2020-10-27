import boto3
import uuid

def pprint_time(secs):
	if secs >= 86400:
		days = secs//86400
		return f"{days}d"
	if secs >= 3600:
		hours = secs // 3600
		return f"{hours}h"
	if secs >= 60:
		mins = secs // 60
		return f"{mins}m"
	if secs > 0:
		return f"{secs}s"


def table_init(table_name):
	# Grab the DynamoDB table based on table_name
	dynamodb = boto3.resource('dynamodb')
	return dynamodb.Table(table_name)

def user_init(utable, user_id, user_item = {}):
	user = utable.get_item(Key={"user_id":user_id})
	if not "Item" in user:
		utable.put_item(
			Item = user_item
		)

def idgen():
	return str(uuid.uuid4()).split('-')[-1]

course_ids = {
    "MATH 1A": "d1bc38587429",
    "MATH 1B": "836ad5f34cb3",
    "ECON 1": "e58efbabe08e",
    "ECON 2": "54bc2b4aead3",
    "PHYSICS 7A": "dacbf6e3fda4",
    "PHYSICS 7B": "b266c224509c",
    "CHEM 1A": "ecf8dc1335d8",
    "CHEM 3A": "6814359d12a8",
    "STAT 20": "68c984605bbe",
    "EECS 16A": "386563c111a3"
}

course_lookup = {v:k for k,v in class_ids.items()}