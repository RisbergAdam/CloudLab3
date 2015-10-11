# -*- coding: utf-8 -*-

import json
import os
import swiftclient.client
from celery import Celery

app = Celery("TwitterCounter", backend="amqp://", broker="amqp://")

@app.task
def countPronounsSwift(containerName, objectName, swiftConn):
    print "donwloading..."
    responce, obj = swiftConn.get_object(containerName, objectName)
    print "downloaded!"
    return "["+str(countPronouns(obj.split("\n")))+"]"
    
def countPronouns(obj):
    obj = filter(lambda x: not x == "" and not x == "\n", obj)

    pronouns = {"han": 0 , "hon": 0, "den": 0, "det": 0, "denna": 0, "denne": 0, "hen": 0}

    for tweet in obj:
        tweetText = json.loads(tweet)["text"]
        for pronoun, c in pronouns.items():
            pCount = count(tweetText, pronoun)
            pronouns[pronoun] = c + pCount

    return pronouns
    
def count(text, word):
    smallText = text.lower().split(" ")

    c = 0

    for w in smallText:
        if word in w: c += 1

    return c

#import os
#import swiftclient.client

#config = {'user':os.environ['OS_USERNAME'], 
#          'key':os.environ['OS_PASSWORD'],
#          'tenant_name':os.environ['OS_TENANT_NAME'],
#          'authurl':os.environ['OS_AUTH_URL']}

#conn = swiftclient.client.Connection(auth_version=2, **config)
#print countPronounsSwift("tweets", "tweets_19.txt", conn)

#f = open("twitterFile3", "r")
#print countPronouns(f.readlines())
            
