import pandas
import json

data_link = '/Users/lap15158/Downloads/Keywords-Contribute.xlsx' 
link = './KeywordsGame/keywords/keywords_.json' 

excel_data_df = pandas.read_excel(data_link, engine = 'openpyxl').dropna(how = 'all')

idx = int(excel_data_df['UpdatedIndex'][0])
print("Old length: ", idx)

if (idx >= len(excel_data_df)):
    print("You're already newest data")
    exit()

json_str = excel_data_df[['Keyword']][idx:].to_json(orient = 'records')
print(json_str)
print(excel_data_df[idx:])

idx += len(excel_data_df['Keyword'][idx:])
print("New length: ", idx)

excel_data_df.update({'UpdatedIndex' : [idx]})

writer = pandas.ExcelWriter(data_link, engine = 'xlsxwriter')
excel_data_df.to_excel(writer, sheet_name = 'Sheet1', header = True, index = False)
writer.save()


# ------------- update new records to data_base ----------------

data = json.loads(json_str)
file = open(link)
feeds = json.load(file)
feeds.extend(data)
file.close()
print('Number of keywords: ', len(feeds))

with open(link, 'w') as file:
    file.write(json.dumps(feeds, indent = 4))
    file.close()
