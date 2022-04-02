import json

link = 'E:/HCMUS/CONTEST/THACH_THUC/KeywordsGame/keywords/keywords_.json' 
new_link = link

file = open(link)
feeds = json.load(file)
file.close()

values = set()
for item in feeds: 
    values.add(item['Keyword'])

values = [{'Keyword' : keyword} for keyword in values]

print(len(values))

with open(new_link, 'w') as file:
    file.write(json.dumps(values, indent = 4))
    file.close()