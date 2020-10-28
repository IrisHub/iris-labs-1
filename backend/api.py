from util import *
import random
import time
from datetime import datetime
from datetime import timedelta
import humanize
import json
from boto3.dynamodb.conditions import Key

def courses_list(event, context):
	return sorted([{'course_id':k, 'course_name':v} for k,v in course_lookup.items()], key = lambda x: x['course_name'])

def auth(event, context):
	assert 'user_id' in event
	assert 'courses' in event
	assert 'phone' in event
	user_id = event['user_id']
	courses = event['courses']
	phone = event['phone']
	courses = [course_ids[e] for e in courses]
	utable = table_init('iris-labs-1-users')
	user_item = {
		"user_id":user_id,
		"nickname":get_nickname(),
		"courses":courses,
		"posts":[],
		"phone":phone,
	}
	user_init(utable, user_id, user_item = user_item)


def get_nickname():
	names = ['Strada', 'Campanile', 'Haas', 'Soda', 'Glade', 'Moffitt', 'Doe', 'Croads', 'Le Conte', 'VLSB', 'Cory', 'North Gate', 'Mezzo', 'Milano', 'Victory Point', 'Brewed Awakening', 'Trock', '51B', 'Big C', 'Unit 3', 'Blackwell', 'Foothill', 'CREAM', 'Imm Thai', 'Chipotle', 'Evans']
	return "Anonymous " + random.choice(names)

#TODO add post to list of posts in user table for deletion purposes
def make_post(event, context):
	assert 'user_id' in event
	user_id = event['user_id']
	needs = event['needs']
	offer = event['offer']
	course_ = event['course']

	post_id = idgen()

	utable = table_init('iris-labs-1-users')
	ptable = table_init('iris-labs-1-posts')

	user_info = utable.get_item(Key = {'user_id':user_id})['Item']
	utable.update_item(
		Key = {
			'user_id':user_id,
		},
		UpdateExpression = "SET posts = list_append(posts, :s)",
		ExpressionAttributeValues = {
			":s": [course_ids[course_] + ":" + post_id]
		}
	)
	nickname = user_info['nickname']
	phone = user_info['phone']

	ptable.put_item(
		Item = {
			'course_id':course_ids[course_],
			'post_id':post_id,
			'poster_nickname':nickname,
			'poster_id':user_id,
			'poster_phone':phone,
			'poster_needs':needs,
			'poster_offer':offer,
			'post_time': str(int(time.time())),
			'expiration_time':str(int(time.time())+604800),
			'solved':False,
		}
	)

def toggle_solved(event, context):
	assert 'course_id' in event
	assert 'post_id' in event
	course_id = event['course_id']
	post_id = event['post_id']

	ptable = table_init('iris-labs-1-posts')
	state = ptable.get_item(Key = {'course_id':course_id,'post_id':post_id})["Item"]['solved']
	ptable.update_item(
		Key = {
			'course_id':course_id,
			'post_id':post_id
		},
		UpdateExpression = "SET solved = :s",
		ExpressionAttributeValues = {
			":s":not state,
		}
	)

def get_user_courses(event, context):
	assert 'user_id' in event
	user_id = event['user_id']

	utable = table_init('iris-labs-1-users')
	user_courses = utable.get_item(Key={'user_id':user_id})["Item"]['courses']
	return sorted([{'course_id':c, 'course_name':course_lookup[c]} for c in user_courses], key=lambda x: x['course_name'])

def populate_feed(event, context):
	assert 'user_id' in event
	user_id = event['user_id']
	utable = table_init('iris-labs-1-users')
	user_courses = utable.get_item(Key={'user_id':user_id})["Item"]['courses']
	# user_courses = [course_lookup[e] for e in user_courses]

	ptable = table_init('iris-labs-1-posts')
	all_posts = []
	for c in user_courses:
		course_posts = ptable.query(
			KeyConditionExpression=Key('course_id').eq(c)
		)
		if "Items" in course_posts:
			all_posts.extend(course_posts['Items'])
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
		post['course_name'] = course_lookup[post['course_id']]

	return all_posts

def delete_user(event, context):
	assert 'user_id' in event
	user_id = event['user_id']

	utable = table_init('iris-labs-1-users')
	user_info = utable.get_item(Key={'user_id':user_id})['Item']
	for post in user_info['posts']:
		course_id, post_id = post.split(':')
		payload = {
			'course_id':course_id,
			'post_id':post_id
		}
		delete_post(payload, None)

	utable.delete_item(
		Key = {
			'user_id':user_id,
		}
	)

def delete_post(event, context):
	assert 'course_id' in event
	course_id = event['course_id']
	assert 'post_id' in event
	post_id = event['post_id']

	ptable = table_init('iris-labs-1-posts')

	ptable.delete_item(
		Key = {
			'course_id':course_id,
			'post_id':post_id,
		}
	)


# def __main__():
# 	print(courses_list(None, None))

# 	courses = ['CHEM 1A', 'CHEM 3A', 'ECON 1', 'ECON 2']
# 	user_id1 = 'sldkjfalksdjf;aj'
# 	payload = {'user_id':user_id1, 'courses':courses, 'phone':'1234567889'}
# 	auth(payload, None)

# 	courses = ['EECS 16A', 'CHEM 3A', 'ECON 1', 'ECON 2']
# 	user_id = 'sdfsdfaj'
# 	payload = {'user_id':user_id, 'courses':courses, 'phone':'1234567889'}
# 	auth(payload, None)

# 	post = {
# 		'user_id':user_id1,
# 		'needs':'check 2B',
# 		'offer':'can help w/ 3',
# 		'course':'CHEM 1A'
# 	}
# 	make_post(post, None)

# 	post = {
# 		'user_id':user_id,
# 		'needs':'wanna check 2b integral',
# 		'offer':'can help w/ 3',
# 		'course':'EECS 16A'
# 	}
# 	make_post(post, None)
	
# 	print(get_user_courses(payload, None))

# 	payload = {
# 		'course_id':'ecf8dc1335d8',
# 		'post_id':'02c6a46de612'
# 	}
# 	toggle_solved(payload, None)

# 	payload = {'user_id':user_id1}
# 	print(json.dumps(populate_feed(payload, None), indent=4))

# 	delete_user(payload, None)


# __main__()
