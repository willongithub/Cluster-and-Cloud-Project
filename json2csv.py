# json to csv convertor

# Group 30
# Surnames Names Student IDs
# Wu Siqi 750892
# Wu Chongchong 720722
# Zhao Danni 756200
# Yang Chao 795047
# Li Hanchen 807363

import csv
import json

filename = 'test.json'

csvfile = csv.writer(open("test.csv", "wb+"))
csvfile.writerow(["score", "x", "y", "time"])

with open(filename, 'r') as jsonfile:
    content = json.load(jsonfile)
    for item in content:
        csvfile.writerow([item["score"],item['coordinates'][1],item['coordinates'][0],item['time']])
