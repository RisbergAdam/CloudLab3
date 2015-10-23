import os
from novaclient.client import Client

config = {'username':os.environ['OS_USERNAME'], 
          'api_key':os.environ['OS_PASSWORD'],
          'project_id':os.environ['OS_TENANT_NAME'],
          'auth_url':os.environ['OS_AUTH_URL']}

workers = []
server_ip = "192.168.0.161"
nc = Client('2', **config)

def createWorker():
    image = nc.images.find(name="NopeWorkerSnapshot")
    flavor = nc.flavors.find(name="m1.medium")
    cloud_init = "#!/bin/bash \n" + \
                 " cd /home/ubuntu/CloudLab3 \n" + \
                 "git reset --hard && git pull \n" + \
                 " su -c 'celery -A CeleryWorker worker -b amqp://cloudworker:worker@" + \
                 server_ip + "//' ubuntu"
    server = nc.servers.create("NopeWorker" + str(len(workers)), image, flavor, userdata=cloud_init)
    print server
    workers.append(server)


while 1:
    action = raw_input("[c]reate/[d]elete/[q]uit: ")
    if action == "c":
        createWorker()
    elif action == "d" and len(workers) > 0:
        server = workers.pop()
        print server
        server.delete()
    elif action == "q":
        while len(workers) > 0:
            workers.pop().delete()
        break
