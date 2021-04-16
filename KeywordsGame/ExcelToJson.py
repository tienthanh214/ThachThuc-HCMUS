import pandas
import json



excel_data_df = pandas.read_excel('E:\GoogleDrive\ThachThuc\Keywords-Contribute.xlsx', engine = 'openpyxl', usecols = ["Keyword"]).dropna()

json_str = excel_data_df.to_json(orient = 'records')


# print(json_str)
# print(len(excel_data_df))

data = json.loads(json_str)
link = 'C:/Users/ninhh/Downloads/auto-py-to-exe-master/auto-py-to-exe-master/output/keywords/keywords_.json'
file = open(link)
feeds = json.load(file)
feeds.extend(data)
print(len(feeds))

with open(link, 'w') as file:
    file.write(json.dumps(feeds, indent = 4))
    file.close()
