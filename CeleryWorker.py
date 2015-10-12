# -*- coding: utf-8 -*-

import json
import os
import swiftclient.client
from celery import Celery
import cPickle

app = Celery("TwitterCounter", backend="amqp://", broker="amqp://")

@app.task
def countPronounsSwift(containerName, objectName, swiftConn):
    print "donwloading " + objectName + "..."
    responce, obj = swiftConn.get_object(containerName, objectName)
    print "downloaded!"
    obj = filter(lambda x: not x == "" and not x == "\n", obj.split("\n"))
    retStr = str(cPickle.dumps(countPronouns(obj)))
    print "counted!"
    return retStr

def countPronounsSingle(tweetText):
    return str(cPickle.dumps(countPronouns(tweetText)))

def countPronouns(obj):
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
