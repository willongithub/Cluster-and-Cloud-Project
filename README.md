# Cluster-and-Cloud-Project
It is repository for a project regarding cluster database system with its front end web page.

[Demo video](https://youtu.be/ebaxhc8ocqI)


## Cloud Preparation

Here we've build a CouchDB database cluster on NeCTAR cloud.

First, launch instance using NeCTAR dashboard.

Virtual machines on the cloud are based on image ***NeCTAR Ubuntu 16.04 LTS (Xenial) amd64***.


**Instance setting**

Availability Zone: ***melbourne-np*** (for extended volume).

KeyPair: Upload your own private key or generate a new oneasdasdasqwd

Security Group: Allow group ***default***, ***SSH*** and ***HTTP***. In ***HTTP*** group, need to add ingress rules for port ***5984 and 8848*** for CouchDB and myserver.

After couple of minutes, you will have your unpolished VMs.

Note the ***IP Addresses*** of your VMs, it will be used to setup CouchDB.


## CouchDB Setup

This part we use ***Ansible***. Details at [Link](https://github.com/willongithub/Cluster-and-Cloud-Project/blob/master/myansible).

When done, run on VMs:
'''sh startup.sh'''

it will start myserver.py and tweetcollector.py as background process on the machine.

myserver.py is our backend server.

tweetcolloctor.py is our harvester for Twitters from all over Aus.


## Data process server and Web client

myserver.py is a backend process used to handle request from web page. Now we've put it on one of the VMs on NeCTAR(115.146.93.176).

When request come, it will query CouchDB targeting certain database, CouchDB will do MapReduce then return desired data sets to myserver.py. Using those data, it can do sentiment analysis and get the results prepared for front end visualazation.

The Web client is a page based on Google Map with some charts.

## Upload data from AURIN using datainputer.py

You should put the json downloaded from AURIN in current folder.

suppose your file is: victoria_sport_and_recreation_facility_locations_2015-2016.json

then
'''python datainputer.py -i '115.146.93.174' -d 'victoria_sport_and_recreation_facility_locations_2015-2016' '''
will upload the data in it to couchDB on 115.146.93.174.
