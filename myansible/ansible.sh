#!/bin/bash
sudo cp hosts /etc/ansible
sudo cp mykey.pem /etc/ansible

ansible all -m ping

ansible all -m copy -a "src=./install-couchdb.sh dest=/home/ubuntu"
ansible all -m shell -a 'bash install-couchdb.sh'

ansible v1 -m copy -a "src=./vmv1.args dest=/home/couchdb/etc/vm.args" -u root --sudo
ansible v1 -m copy -a "src=./localv1.ini dest=/home/couchdb/etc/local.ini" -u root --sudo
ansible v2 -m copy -a "src=./vmv2.args dest=/home/couchdb/etc/vm.args" -u root --sudo
ansible v2 -m copy -a "src=./localv2.ini dest=/home/couchdb/etc/local.ini" -u root --sudo

ansible all -m shell -a 'sv restart couchdb' -u root --sudo

ansible all -m shell -a 'sudo apt install curl'

ansible all -m copy -a "src=./cluster.sh dest=/home/ubuntu"
ansible all -m shell -a 'bash cluster.sh'

ansible v1 -m copy -a "src=./connect.sh dest=/home/ubuntu"
ansible v1 -m shell -a 'bash connect.sh'

ansible v1 -m shell -a 'curl -X PUT "http://admin:password@localhost:5984/aus?n=3&q=8"'

ansible v1 -m copy -a 'src=./view.json dest=/home/ubuntu/'
ansible v1 -m shell -a 'curl -X PUT http://admin:password@localhost:5984/aus/_design/tweetfilter --data-binary @view.json'

ansible all -m shell -a 'sudo apt install python-pip -y'
ansible all -m shell -a 'sudo pip install --upgrade pip'
ansible all -m shell -a 'sudo pip install tweepy'
ansible all -m shell -a 'sudo pip install vaderSentiment'
ansible all -m shell -a 'sudo pip install --upgrade vaderSentiment'

ansible all -m copy -a 'src=./tweetcollector.py dest=/home/ubuntu'
ansible all -m copy -a 'src=./myserver.py dest=/home/ubuntu'
ansible all -m copy -a 'src=./contentcounter.py dest=/home/ubuntu'

ansible all -m shell -a 'nohup python tweetcollector.py > collector.txt 2>&1 &'
ansible all -m shell -a 'nohup python myserver.py > server.txt 2>&1 &'

