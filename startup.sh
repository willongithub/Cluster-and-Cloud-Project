#! /bin/sh

# start up script for harvester and server

# Group 30
# Surnames Names Student IDs
# Wu Siqi 750892
# Wu Chongchong 720722
# Zhao Danni 756200
# Yang Chao 795047
# Li Hanchen 807363

nohup python myserver.py > log.out 2>&1 &
nohup python tweetcollector.py > log.out 2>&1 &
