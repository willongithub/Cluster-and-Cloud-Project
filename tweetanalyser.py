#!/usr/bin/python

# Group 30
# Surnames Names Student IDs
# Wu Siqi 750892
# Wu Chongchong 720722
# Zhao Danni 756200
# Yang Chao 795047
# Li Hanchen 807363

# analyser 1
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    #note: depending on how you installed (e.g., using source code download versus pip install), you may need to import like this:
    #from vaderSentiment import SentimentIntensityAnalyzer
# analyser 2
#from textblob import TextBlob
#from textblob.sentiments import NaiveBayesAnalyzer
import json
import requests
#import sys

def analysis(par):
    #headers = {'content-type': 'application/json'}
    server = "http://115.146.93.176:5984/aus/_design/tweetfilter/_view/validdata"
    payload = {'limit': 1000, 'reduce': 'false'}
    #city = 'brisbane'
    #r = requests.get(server, key=city, params=payload)
    #print json.dumps(r.json())

    city = par['city']
    #print city

    # retrieve mapped tweets
    r = requests.get(server, params=payload)
    data = r.json()['rows']

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
        temp['coordinates'] = item[2]
        #d = json.dumps(temp)
        resultset.append(temp)
        d = json.dumps(resultset)
    
    requests.get(server, headers={'Connection':'close'})
    return d

par = {'limit':'100','city':'mel'}
result = analysis(par)
print result

