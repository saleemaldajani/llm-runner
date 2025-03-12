# -------------------------------------------
# Verify that you can read the json file
# -------------------------------------------
import json
file = open('data.json')
data = json.load(file)
# print(data[0])
# print(data[0]['cid'])
# print(data[0]['text'])
for index, item in enumerate(data):
    print(item['cid'],index)
    print(item['text'],index)