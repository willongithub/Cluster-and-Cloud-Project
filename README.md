# Cluster-and-Cloud-Project
It is repository for a project regarding cluster database system with its front end web page.

## Cloud Preparation

Here we've build a CouchDB database cluster on NeCTAR cloud.

Virtual machines on the cloud are based on image ***NeCTAR Ubuntu 16.04 LTS (Xenial) amd64***.

First, launch instance using NeCTAR dashboard. 

***Instance setting***

Availability Zone: melbourne-np (for extended volume).

KeyPair: Upload your own private key or generate a new one.

Security Group: Allow group ***default***, ***SSH*** and ***HTTP***. In ***HTTP*** group, need to add ingress rules for port 5984 and 8848 for CouchDB and myserver.

After couple of minutes, you will have your unpolished VMs.

Note the IP Addresses of your VMs, it will be used to setup CouchDB.

## CouchDB Setup
