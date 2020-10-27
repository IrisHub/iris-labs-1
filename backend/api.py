from util import *
import random
import time
from datetime import datetime
from datetime import timedelta
import humanize

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
	user_classes = [class_lookup[e] for e in user_classes]

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

	now = datetime.now()
	for post in all_posts:
		post_time = datetime.fromtimestamp(int(post['post_time']))
		diff = now - post_time
		all_posts['post_time'] = humanize.naturaldelta(diff)

	return all_posts


