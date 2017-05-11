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
consumer_key = 'VIzYfBOGxiJH9iQ6rBuyV8wFs'
consumer_secret = 'ttluNgk8ULjLxYEaopgM5hanUyeUhZgQOn1ybBZREFxK2jw8zj'
access_token = '856740454066290688-ejOKwpEhlMVkuolwgoYmXP6URHHQXV5'
access_token_secret = '1JGVhOZgRFYkGosYv5pDmqJnjvRWK8e6GGCox5iKZQkjK'
'''
# 2 used in clusters
consumer_key = 'X2NWWf04gfUjdtbfTH3Cid15U'
consumer_secret = '6yPaf6UwInpeDRLAJo4rPxVMDWxGBCCIwKOcdOnHWNnhvjkRdY'
access_token = '859727563022770176-FmoK9SZzWE3poR2heK9OoHZNbtJYqdo'
access_token_secret = 'Edfpr85YJZD4Dl3zB6WWDvJH4Py9KzQjW59oZnMFZGPH7'

# 2 used in small vms chaoyang
consumer_key = "DcAivbR4BuM3MLSQtKh3GGtF9"
consumer_secret = "brSIPnoY0YtqblmMqDr4dt6FHiCRIDwrL1XzCkGceNlyj5BaXT"
access_token = "4778110405-749P4Wz7rDwChVdQ4SL7f9bnY1jrtrINsxj5aZF"
access_token_secret = "dA39ttpbCkqyxfWjO140g37RQruBQMn4SQzInBm1b9o1S"
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