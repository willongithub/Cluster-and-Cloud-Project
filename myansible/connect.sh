#!/bin/bash
curl -X POST -H "Content-Type: application/json" http://admin:password@127.0.0.1:5984/_cluster_setup -d '{"action": "enable_cluster", "bind_address":"0.0.0.0", "username": "admin", "password":"password", "port": 5984, "remote_node": "115.146.93.174", "remote_current_user": "admin", "remote_current_password": "password" }'
curl -X POST -H "Content-Type: application/json" http://admin:password@127.0.0.1:5984/_cluster_setup -d '{"action": "add_node", "host":"115.146.93.174", "port": "5984", "username": "admin", "password":"password"}'

curl -X POST -H "Content-Type: application/json" http://admin:password@127.0.0.1:5984/_cluster_setup -d '{"action": "enable_cluster", "bind_address":"0.0.0.0", "username": "admin", "password":"password", "port": 5984, "remote_node": "115.146.93.175", "remote_current_user": "admin", "remote_current_password": "password" }'
curl -X POST -H "Content-Type: application/json" http://admin:password@127.0.0.1:5984/_cluster_setup -d '{"action": "add_node", "host":"115.146.93.175", "port": "5984", "username": "admin", "password":"password"}'

curl -X POST -H "Content-Type: application/json" http://admin:password@127.0.0.1:5984/_cluster_setup -d '{"action": "enable_cluster", "bind_address":"0.0.0.0", "username": "admin", "password":"password", "port": 5984, "remote_node": "130.56.250.233", "remote_current_user": "admin", "remote_current_password": "password" }'
curl -X POST -H "Content-Type: application/json" http://admin:password@127.0.0.1:5984/_cluster_setup -d '{"action": "add_node", "host":"130.56.250.233", "port": "5984", "username": "admin", "password":"password"}'

curl -X POST -H "Content-Type: application/json" http://admin:password@127.0.0.1:5984/_cluster_setup -d '{"action": "finish_cluster"}'