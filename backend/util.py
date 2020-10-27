import boto3

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

class_ids = {
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

class_lookup = {v:k for k:v in class_ids.items()}