from util import *
import random
import time
from datetime import datetime
from datetime import timedelta
import humanize
import json
from boto3.dynamodb.conditions import Key

def classes_list(event, context):
	return sorted(class_ids.keys())

def auth(event, context):
	assert 'user_id' in event
	assert 'classes' in event
	user_id = event['user_id']
	classes = event['classes']
	classes = [class_ids[e] for e in classes]
	utable = table_init('iris-labs-1-users')
	user_item = {
		"user_id":user_id,
		"nickname":get_nickname(),
		"classes":classes,
	}
	user_init(utable, user_id, user_item = user_item)


def get_nickname():
	names = ['Strada', 'Campanile', 'Haas', 'Soda', 'Glade', 'Moffitt', 'Doe', 'Croads', 'Le Conte', 'VLSB', 'Cory', 'North Gate', 'Mezzo', 'Milano', 'Victory Point', 'Brewed Awakening', 'Trock', '51B', 'Big C', 'Unit 3', 'Blackwell', 'Foothill', 'CREAM', 'Imm Thai', 'Chipotle', 'Evans']
	return "Anonymous " + random.choice(names)

def make_post(event, context):
	assert 'user_id' in event
	user_id = event['user_id']
	needs = event['needs']
	offer = event['offer']
	class_ = event['class']

	post_id = idgen()

	utable = table_init('iris-labs-1-users')
	ptable = table_init('iris-labs-1-posts')

	user_info = utable.get_item(Key = {'user_id':user_id})['Item']
	nickname = user_info['nickname']

	ptable.put_item(
		Item = {
			'course_id':class_ids[class_],
			'post_id':post_id,
			'poster_nickname':nickname,
			'poster_id':user_id,
			'poster_needs':needs,
			'poster_offer':offer,
			'post_time': str(int(time.time()))
		}
	)



def populate_feed(event, context):
	assert 'user_id' in event
	user_id = event['user_id']
	utable = table_init('iris-labs-1-users')
	user_classes = utable.get_item(Key={'user_id':user_id})["Item"]['classes']
	# user_classes = [class_lookup[e] for e in user_classes]

	ptable = table_init('iris-labs-1-posts')
	all_posts = []
	for c in user_classes:
		class_posts = ptable.query(
			KeyConditionExpression=Key('course_id').eq(c)
		)
		if "Items" in class_posts:
			all_posts.extend(class_posts['Items'])
		else:
			continue
	
	if not all_posts:
		return {
		}

	all_posts = sorted(all_posts, key=lambda x: int(x['post_time']))[::-1]

	now = int(time.time())
	for post in all_posts:
		post_time = int(post['post_time'])
		diff = now - post_time
		post['post_time'] = pprint_time(diff)
		del post['post_id']
		post['course'] = class_lookup[post['course_id']]
		del post['course_id']

	return all_posts

# def __main__():
# 	print(classes_list(None, None))

# 	classes = ['CHEM 1A', 'CHEM 3A', 'ECON 1', 'ECON 2']
# 	user_id = 'testtesttest'
# 	payload = {'user_id':user_id, 'classes':classes}
# 	# auth(payload, None)

# 	post = {
# 		'user_id':'testtesttest',
# 		'needs':'wanna check 2b integral',
# 		'offer':'can help w/ 3',
# 		'class':'CHEM 1A'
# 	}
# 	# make_post(post, None)

# 	payload = {'user_id':user_id}
# 	print(json.dumps(populate_feed(payload, None), indent=4))


# __main__()
