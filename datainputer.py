# upload json to couchDB

# Group 30
# Surnames Names Student IDs
# Wu Siqi 750892
# Wu Chongchong 720722
# Zhao Danni 756200
# Yang Chao 795047
# Li Hanchen 807363

import json
import requests
#import uuid

filename = 'xxx.json'
server = "http://admin:password@localhost:5984/_membership"
headers = {'content-type': 'application/json'}
upload = "http://127.0.0.1:5984/aurin"
#upload = "http://127.0.0.1:5984/test/" + str(uuid.uuid4())

with open(filename, 'r') as f:
    while True:
        line = f.readline()
        if line.startswith('{'):
            line = line.rstrip('\n').rstrip(',')
            #content = json.loads(line)
            payload = line
            r = requests.post(upload, data=payload, headers=headers)
            print r.text
        if line.startswith(']'):
            q = requests.get(server)
            print q.text
            break

