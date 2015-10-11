#!/bin/bash
sudo apt-get install git emacs python-pip rabbitmq-server python-keystoneclient -y
sudo pip install celery python-swiftclient flask
git clone https://github.com/RisbergAdam/CloudLab3
