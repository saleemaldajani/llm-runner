import json
with open('data.json', 'r') as file:
    data = [json.loads(line) for line in file if line.strip()]
for index, item in enumerate(data):
    print(item['cid'],index)
    print(item['author'],index)
    print(item['text'],index)
