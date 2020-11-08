import boto3
import uuid

def pprint_time(secs):
	if secs >= 86400:
		days = secs//86400
		return f"{days}D"
	if secs >= 3600:
		hours = secs // 3600
		return f"{hours}H"
	if secs >= 60:
		mins = secs // 60
		return f"{mins}M"
	if secs > 0:
		return f"{secs}S"
	else:
		return f"JUST NOW"


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
	"MATH 1A (CAL)": "d1bc38587429",
	"MATH 1B (CAL)": "836ad5f34cb3",
	"ECON 1 (CAL)": "e58efbabe08e",
	"ECON 2 (CAL)": "54bc2b4aead3", 
	"PHYS 7A (CAL)": "dacbf6e3fda4", 
	"PHYS 7B (CAL)": "b266c224509c", 
	"CHEM 1A (CAL)": "ecf8dc1335d8", 
	"CHEM 3A (CAL)": "6814359d12a8", 
	"STAT 20 (CAL)": "68c984605bbe", 
	"EECS 16A (CAL)": "386563c111a3",
	"MATH 16A (CAL)": "d4a2e318ee2a",
	"MATH 16B (CAL)": "39a106ece048",
	"EECS 16B (CAL)": "796f3d3569cc",
	"CS 61B (CAL)": "f61b0ab142f9",
	"CS 61C (CAL)": "79ec13ae222e",
	"MATH 53 (CAL)": "81b7816a45f4",
	"MATH 54 (CAL)": "fef831d1302d",
	"CS 70 (CAL)": "14028166ebef",
	"MATH 10A (CAL)": "a5d361401c18",
	"MATH 55 (CAL)": "0428ed904bca",
	"MATH 32 (CAL)": "6961c75e4aec",
	"CS 61A (CAL)": "6169b16978cd",
	"CS 10 (CAL)": "0e53fb50919c",
	"UGBA 10 (CAL)": "79c7447aff29",
	"DATA 8 (CAL)": "01d7c9aafc8a",
	"STAT 2 (CAL)": "e1b1619f695e",
	"STAT 88 (CAL)": "784f4a0bf63a",
	"PSYCH 1 (CAL)": "79210614ed27",
	"COGSCI 1 (CAL)": "6420ff189644",
	"CHEM 4A (CAL)": "8daf40505287",
	"PHYS 5A (CAL)": "e687ce7e5ba5",
	"BIO 1A (CAL)": "56dcd648c13f",
	"BIO 1B (CAL)": "dc04827ce29e",
	"PHYS 8A (CAL)": "8bfc3da38681",
	"POLISCI 1 (CAL)": "0e429d9f6510",
	"POLISCI 2 (CAL)": "3ff7c5cffa37",
	"HISTORY 7A (CAL)": "ee2ab10f971f",
	"ART 26 (CAL)": "769d93a53c31",
	"HIST 30 (CAL)": "fe7fc4d5021c",
	"AFRICAM 5A (CAL)": "aafedef2d6d8",
	"ESPM 50AC (CAL)": "6c0ca55fb4b9",
	"ASTRO 10 (CAL)": "5880b158abe6",
	"GEOG 10A (CAL)": "c32af3514702",
	"ENGIN 7 (CAL)": "063e72bd3fe1",
	"ENGIN 26 (CAL)": "b03c30f30588",
	"MATH 19 (STANFORD)": "3b8360ce49a4",
	"MATH 20 (STANFORD)": "a8d7785ede01",
	"MATH 21 (STANFORD)": "f4d8b22ef08a",
	"MATH 51 (STANFORD)": "041b5be65c2e",
	"MATH 53 (STANFORD)": "65b6dc2fd624",
	"CME 100 (STANFORD)": "bd378485d2fe",
	"STATS 60 (STANFORD)": "e7fa1dd4956a",
	"ENGR 62 (STANFORD)": "8e282602c0f3",
	"CS 109 (STANFORD)": "0d0ddc98b9c9",
	"STATS 110 (STANFORD)": "586f49cb8d3b",
	"CHEM 33 (STANFORD)": "5c41ce88f901",
	"PHYS 21 (STANFORD)": "37a0480677d0",
	"PHYS 23 (STANFORD)": "3779969c3070",
	"PHYS 41 (STANFORD)": "0b44858a5500",
	"PHYS 43 (STANFORD)": "6338edb80962",
	"PHYS 45 (STANFORD)": "63215e7f8f5d",
	"PHYS 61 (STANFORD)": "90b1c83a5fa5",
	"PHYS 63 (STANFORD)": "7e99e84c377f",
	"PHYS 65 (STANFORD)": "90afc597d69e",
	"CHEM 31A (STANFORD)": "d5b69ae70cd7",
	"CHEM 121 (STANFORD)": "c0d38f46b934",
	"BIO 60 (STANFORD)": "4470943cbd9d",
	"BIO 81 (STANFORD)": "cc01b3d51036",
	"BIO 83 (STANFORD)": "83583a179b3b",
	"BIO 45 (STANFORD)": "e278820a71ea",
	"CEE 63 (STANFORD)": "943cd5a8a869",
	"EARTHSYS 10 (STANFORD)": "8a4881c6d96c",
	"CHEM 31M (STANFORD)": "8a11364f0ead",
	"ENGR 14 (STANFORD)": "ab8dc088889f",
	"ENGR 15 (STANFORD)": "c728187ba961",
	"ENGR 40M (STANFORD)": "92fca1eb0bdb",
	"ENGR 60 (STANFORD)": "b89dedfce075",
	"ME 102 (STANFORD)": "0148fd51d00e",
	"CS 106A (STANFORD)": "fce7a49963d1",
	"CS 106B (STANFORD)": "2e4efe677a3c",
	"CS 107 (STANFORD)": "463c1a31647e",
	"CS 103 (STANFORD)": "f38ecdc0a7bf",
	"ECON 1 (STANFORD)": "401fcaa26348",
	"POLISCI 110 (STANFORD)": "bb3a7892b4e3",
	"POLISCI 103 (STANFORD)": "b9c0525967fa",
	"PSYCH 70 (STANFORD)": "c10e777cff8c",
	"PSYCH 1 (STANFORD)": "675cc0604577",
	"POLISCI 1 (STANFORD)": "ba2ee4c3615d",
	"COMM 1 (STANFORD)": "c745662a4bd6",
	"PHIL 1 (STANFORD)": "adad27ad1dc1"
}

course_lookup = {v:k for k,v in course_ids.items()}
course_lookup_short = {v:k.rsplit(" ", 1)[0] for k, v in course_ids.items()}
course_ids_short = {v:k for k, v in course_lookup_short.items()}