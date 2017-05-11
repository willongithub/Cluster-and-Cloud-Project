# sentiment analysis server
# Modified by siqi on Sun May 7 2017

import time
import csv
import cgi
import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
# import helper data reading functions
#from tweetanalyser import *
import json
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
#from textblob import TextBlob
#from textblob.sentiments import NaiveBayesAnalyzer
from contentcounter import *

# Main parameters
#HOST = 'localhost'
HOST = '0.0.0.0'
PORT = 8848

class MyHandler(BaseHTTPRequestHandler):
    ''' HTTP request handler class extending BaseHTTPRequestHandler '''
     
    def myparse_getrequest(self):  
        ''' GET request: parse the path and extract query  '''
        parsed_path = urlparse.urlparse(self.path)
        pathlist = parsed_path.path.split('/')[1:]
        querylist = parsed_path.query.split('&')
        querydict = {}
        for item in querylist:
            keyvalpair = item.split('=')
            querydict[keyvalpair[0]] = keyvalpair[1]
            
        # return path components in a list (ordered)
        # and query variables&values in a dictionary (unordered)
        return pathlist, querydict

    # respond to a GET request
    def do_GET(self):
        ''' responds to a GET request '''   
        
        # send response
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        
        
        pathlist, querydict = self.myparse_getrequest()
        #print querydict
        #if querydict['request'] == 'true':
        #block = int(querydict['step'])
        #total = getrows(querydict)
        #rep = int(total/block)
        #print querydict
        if not querydict.has_key('html'):
            querydict['html'] = 'no'
        if not querydict.has_key('city'):
            querydict['city'] = 'all'
        if not querydict.has_key('step'):
            querydict['step'] = '10'
        if not querydict.has_key('time'):
            querydict['time'] = 'no'
        if not querydict.has_key('search'):
            querydict['search'] = 'no'
        if not querydict.has_key('ratio'):
            querydict['ratio'] = 'no'
        if not querydict.has_key('mood'):
            # mood can be 1, 0, -1
            querydict['mood'] = 'no'
        #querydict['content'] = ''

        if querydict['html'] == 'yes':
            f = open("index.html", "r")
            result = f.read()
            self.wfile.write(result)
        elif querydict['time'] == 'yes':
            result = countbyhour(querydict['city'])
            self.wfile.write(result)
        elif querydict['search'] != 'no':
            result = search(querydict['city'], querydict['search'])
            self.wfile.write(result)
        elif querydict['mood'] != 'no':
            #result = avgscore(querydict['city'], querydict['mood'])
            slot, result = analysis(querydict)
            self.wfile.write(result)
        elif querydict['ratio'] == 'yes':
            #result = avgscore(querydict['city'], querydict['mood'])
            slot, result = analysis(querydict)
            self.wfile.write(result)
        else:
            #index = 1
            result, slot = analysis(querydict)
            self.wfile.write(result)

        #else:
        #    result = 'No request'
        #    self.wfile.write(result)
        # send back parsed request content for debugging
        #self.wfile.write(pathlist)
        #self.wfile.write(querydict)
        ####------------------------------------------------------

        return

def analysis(par):
    #headers = {'content-type': 'application/json'}
    # server = "http://115.146.93.176:5984/aus/_design/tweetfilter/_view/validdata"
    bound = int(par['step'])
    #step = bound*inx
    #bound = 100
    step = 0
    totalpos = 0
    totalneu = 0
    totalneg = 0
    scorepos = 0
    scoreneg = 0

    payload = {'limit': bound, 'reduce': 'false', 'skip': step}
    #city = 'brisbane'
    #r = requests.get(server, key=city, params=payload)
    #print json.dumps(r.json())

    city = par['city']
    server = "http://localhost:5984/aus/_design/tweetfilter/_view/" + city

    # retrieve mapped tweets
    r = requests.get(server, params=payload)
    data = r.json()['rows']
    #print r.json()

    #close connection
    #requests.get(server, headers={'Connection':'close'})

    # do analysis
    analyzer = SentimentIntensityAnalyzer()
    resultset = []
    for item in data:
        item = item['value']
        sentence = item[1]
        temp = {}
        #blob = TextBlob(sentence, analyzer=NaiveBayesAnalyzer())
        #score = blob.sentiment
        vs = analyzer.polarity_scores(sentence)
        #time = json.dumps(item[0])
        #temp = '{\"' + content + '\",\"' + str(vs['compound']) + '\",\"' + item[2] '\"}'
        temp['time'] = item[0]
        temp['score'] = vs['compound']
        if vs['compound'] > 0:
            totalpos += 1
            scorepos += vs['compound']
        elif vs['compound'] < 0:
            totalneg += 1
            scoreneg += vs['compound']
        else:
            totalneu += 1
            #scoreneu += vs['compound']
	    #total += vs['compound']
        temp['coordinates'] = item[2]
        #d = json.dumps(temp)
        resultset.append(temp)
        d = json.dumps(resultset, indent=4, separators=(',', ': '))

    if par['mood'] != 'no':
        if int(par['mood']) > 0:
            d = scorepos/totalpos
        if int(par['mood']) < 0:
            d = scoreneg/totalneg
        if int(par['mood']) == 0:
            d = (scorepos + scoreneg)/(totalpos + totalneu + totalneg)
    if par['ratio'] == 'yes':
        d = float(totalpos)/(totalpos + totalneu + totalneg)
    return d
    

def getrows(par):
    payload = {'reduce': 'false'}
    city = par['city']
    server = "http://localhost:5984/aus/_design/tweetfilter/_view/" + city
    # retrieve number of tweets
    r = requests.get(server, params=payload)
    d = r.json()['total_rows']
    #close connection
    #requests.get(server, headers={'Connection':'close'})
    return int(d)

httpd = HTTPServer((HOST, PORT), MyHandler)
print time.asctime(), "Server Starts - %s:%s" % (HOST, PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print 'Server offline!'
httpd.server_close()
#close connection
server = "http://localhost:5984/"
requests.get(server, headers={'Connection':'close'})
print time.asctime(), "Server Stops - %s:%s" % (HOST, PORT)
