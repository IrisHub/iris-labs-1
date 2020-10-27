from util import *
import random

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
		return {}

	return None
