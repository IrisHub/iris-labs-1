import requests
a = requests.post("https://l2wmf923e0.execute-api.us-west-1.amazonaws.com/fns/fax")
# a = requests.post("https://l2wmf923e0.execute-api.us-west-1.amazonaws.com/fns/count")
print(a.text)