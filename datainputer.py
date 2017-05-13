# upload json to couchDB 2.0

# Group 30
# Surnames Names Student IDs
# Wu Siqi 750892
# Wu Chongchong 720722
# Zhao Danni 756200
# Yang Chao 795047
# Li Hanchen 807363

import json
import requests
import argparse

# -i 'couchdb ip address' -d 'name of json file as well as database(newly created) name it will be in'
# only support json file from AURIN

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--ip-address", type=str, default='127.0.0.1',
	help="ip address of server")
ap.add_argument("-d", "--db-name", type=str, default='new-test',
	help="target database name")
args = vars(ap.parse_args())

dbname = args['db_name']
ip = args['ip_address']
filename = args['db_name'] + '.json'

server = "http://" + ip + ":5984/" + dbname + "?n=3&q=4"
headers = {'content-type': 'application/json'}
upload = "http://" + ip + ":5984/" + dbname

# create new database for importing data

a = requests.put(server)
print a
if a.json()['ok']:
    with open(filename, 'r') as f:
        content = json.load(f)

        print 'upload start!'

        for item in content['features']:
            payload = json.dumps(item)
            print payload
            r = requests.post(upload, data=payload, headers=headers)
            print r.text
        print 'upload done!'
else:
    print 'database already exist!'

