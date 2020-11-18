import boto3
from boto3.dynamodb.conditions import Key
from util import *

def fax(event, context):
	t = table_init("fax")
	t.update_item(
		Key = {
			"id":"main",
		},
		UpdateExpression = "ADD fax_count :v",
		ExpressionAttributeValues = {
			":v": 1,
		}
	)
	return get_count(None, None)

def get_count(event, context):
	t = table_init("fax")
	count = int(t.get_item(
		Key={
			"id":"main"
		}
	)['Item']['fax_count'])
	return count * 10
