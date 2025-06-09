import json

f = open('saved_json/test.json')
d = eval(json.load(f).strip())
print(d['name'])