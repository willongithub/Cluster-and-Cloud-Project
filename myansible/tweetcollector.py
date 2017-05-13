# tweetcollector 2.0 (duplicate free)
# use twitter stream api to collect random twitters
# modified by Liam at Mon 8 May

import tweepy
import json
import requests
#import time
import sys

headers = {'content-type': 'application/json'}
#server = "http://115.146.93.175:5984/aus"
server = "http://localhost:5984/aus"
#view = "http://115.146.93.176:5984/aus/_design/tweetfilter/_view/all"
view = "http://localhost:5984/aus/_design/tweetfilter/_view/all"

# Specify the account credentials in the following variables:
# two streams per credential limit

# 1 left
consumer_key = 
consumer_secret = 
access_token = 
access_token_secret = 
'''
# 2 used in clusters
consumer_key = 
consumer_secret = 
access_token = 
access_token_secret = 

# 2 used in small vms chaoyang
consumer_key = 
consumer_secret = 
access_token = 
access_token_secret = 
'''

# This listener will print out all Tweets it receives
class PrintListener(tweepy.StreamListener):
    def on_data(self, data):
        # Decode the JSON data
        tweet = json.loads(data)
        
        if tweet['id'] not in idlist:
            payload = data

            # Post tweets to database
            r = requests.post(server, data=payload, headers=headers)
            #close connection
            requests.get(server, headers={'Connection':'close'})
            print r
            print r.text
        
        else:
            print tweet['id'] + 'is already there'

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    # request existed id list
    #payload = {'limit': 10, 'reduce': 'false'}
    l = requests.get(view)
    #print l.json()
    idlist = []
    dataview = l.json()['rows']
    idlist = [item['key'] for item in dataview]

    # close connection
    requests.get(server, headers={'Connection':'close'})

    try:
        listener = PrintListener()

        # Authenticate
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        # Connect the stream to our listener
        stream = tweepy.Stream(auth, listener)
        # tweets with 'Python'
        #stream.filter(track=['Python'])
        # Twitter from Brisbane
        #stream.filter(locations = [152.87,-27.58,153.26,-27.29])
        # from all Aussie
        stream.filter(locations = [109.48,-43.41,153.14,-10.72])
    except KeyboardInterrupt:
        print 'Collector offline!'
    sys.exit(0)
