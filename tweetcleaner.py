# find and remove duplicated data from couchDB

# Group 30
# Surnames Names Student IDs
# Wu Siqi 750892
# Wu Chongchong 720722
# Zhao Danni 756200
# Yang Chao 795047
# Li Hanchen 807363

import json
import requests
import sys

#server = "http://115.146.93.175:5984/aus"
#view = "http://115.146.93.176:5984/aus/_design/tweetfilter/_view/validdata"
server = "http://localhost:5984/aus/"
view = "http://localhost:5984/aus/_design/tweetfilter/_view/all"

try:
    # get new id list
    l = requests.get(view)

    # initialise
    deleted = 0
    

    dataview = l.json()['rows']
    idlist = [item['key'] for item in dataview]
    idlist = [i for i in idlist if idlist.count(i) > 1]

    while idlist:
        deletelist = []
        duplist = []
        for i in idlist:
            if i not in duplist:
                duplist.append(i)
        for item in dataview:
            for i in duplist:
                if i == item['key']:
                    deletelist.append(item['id'])
                    duplist.remove(i)

        for item in deletelist:        
            # delete doc with id
            docrev = server + item
            r = requests.get(docrev)
            rev = r.json()['_rev']
            payload = {'rev': rev}
            r = requests.delete(docrev, params=payload)
            print r.text
            deleted += 1
        
        # get new id list
        l = requests.get(view)

        dataview = l.json()['rows']
        idlist = [item['key'] for item in dataview]
        idlist = [i for i in idlist if idlist.count(i) > 1]

    # close connection
    requests.get(server, headers={'Connection':'close'})
    print str(deleted) + ' duplicated data have been removed!'
    
except KeyboardInterrupt:
    print 'Cleaner offline!'
sys.exit(0)
