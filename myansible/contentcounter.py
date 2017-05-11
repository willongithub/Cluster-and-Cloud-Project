# count tweets with certain content
# Modified by Liam

import json
import requests
import re

#view = "http://localhost:5984/test2/_design/filter/_view/valid"
#server = "http://localhost:5984/"

# get count of certain content in tweets as per city
def search(city, content):
    #content = ''
    #city = 'syd'
    server = "http://localhost:5984/"
    view = "http://localhost:5984/aus/_design/tweetfilter/_view/" + city
    counter = 0
    compiled_pattern = re.compile(content, re.M|re.I)
    r = requests.get(view)
    data = r.json()['rows']
    for item in data:
        line = item['value'][1]
        if compiled_pattern.search(line):
            counter += 1
    print counter
    requests.get(server, headers={'Connection':'close'})
    return counter


# get tweets count as per city
def countbyhour(city):
    #city = 'per'
    server = "http://localhost:5984/"
    view = "http://localhost:5984/aus/_design/tweetfilter/_view/" + city
    #timeslots = {'0': 0, '2': 0, '4': 0, '6': 0, '8': 0, '10': 0, '12': 0, '14': 0, '16': 0, '18': 0, '20': 0, '22': 0}
    timeslots = {}
    for i in range(12):
        r = i*2
        #print r
        #content = '([0[0-9]|1[0-9]|2[0-4]):(\d\d):(\d\d)'
        #content = '(1[0-9]):(\d\d):(\d\d)'
        
        if r - 10 >= 0 and r - 10 < 10:
            content = '(1[' + str(r - 10) + '-' + str(r - 9) + ']):(\d\d):(\d\d)'
        elif r - 20 >= 0:
            content = '(2[' + str(r - 20) + '-' + str(r - 19) + ']):(\d\d):(\d\d)'
        else:
            content = '(0[' + str(r) + '-' + str(r + 1) + ']):(\d\d):(\d\d)'
        
        #content = '(10):(\d\d):(\d\d)'
        counter = 0
        #print content
        compiled_pattern = re.compile(content, re.M|re.I)
        d = requests.get(view)
        data = d.json()['rows']
        #print data
        for item in data:
            line = item['value'][0]
            if compiled_pattern.search(line):
                counter += 1
        #print counter
        #print str(r)
        timeslots[str(r)] = counter
    
    #print json.dumps(timeslots)
    requests.get(server, headers={'Connection':'close'})
    return json.dumps(timeslots)


# get avg hapiness score as per city
def avgscore(city, mood):
    #city = 'mel'
    mood = int(mood)
    server = "http://localhost:8848/"
    payload = {'city': city, 'limit': 100}
    r = requests.get(server, params=payload)
    data = r.json()
    if mood < 0:
        avg = [item['score'] for item in data if item['score'] < 0]
    elif mood == 0:
        avg = [item['score'] for item in data if item['score'] != 0]
    else:
        avg = [item['score'] for item in data if item['score'] > 0]
    avg = sum(avg)/len(avg)
    print avg
    requests.get(server, headers={'Connection':'close'})
    return avg
