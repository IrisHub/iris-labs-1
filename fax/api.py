import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime
import pytz
from datetime import timedelta
# from ip2geotools.databases.noncommercial import DbIpCity
from util import *
import json
import random

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

	# if 'ip' in event:
	# 	city = DbIpCity.get(event['ip'], api_key='free').city
	# 	t.update_item(
	# 		Key = {
	# 			"id":"main",
	# 		},
	# 		UpdateExpression = "SET fax_city = :i, timestamp = :t",
	# 		ExpressionAttributeValues = {
	# 			":i":city,
	# 			":t":int(time.time())
	# 		}
	# 	)

	# 	return {
	# 		"count":get_count(None, None),
	# 		"last_updated": f"LATEST FAX: {pprint_time(int(time.time()))} AGO IN {city}"
	# 	}
	return {
		"count": get_count(None, None),
		"people": get_count(None, None)//13,
		"date": datetime.strftime(datetime.now(pytz.timezone('US/Pacific')), '%B %d, %Y').upper(),
		"time":datetime.strftime(datetime.now(pytz.timezone('US/Pacific')), '%I:%M %p')
	}

def get_count(event, context):
	t = table_init("fax")
	item = t.get_item(
		Key={
			"id":"main"
		}
	)['Item']
	count = int(item['fax_count'])
	# last_time = int(item['timestamp'])
	# fax_city = item['fax_city']
	# diff = int(time.time()) - last_time
	# if diff > 1500: diff = random.randint(50, 1500)
	# return {
	# 		"count":count,
	# 		"last_updated": f"LATEST FAX: {pprint_time()} AGO IN {city}"
	# 	}
	return count * 13
