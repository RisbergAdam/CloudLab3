from flask import Flask, request
from CeleryWorker import countPronounsSwift, countPronounsSingle
from CeleryTask import CeleryTask
import os
import swiftclient.client
import json
import cPickle
import time

config = {'user':os.environ['OS_USERNAME'], 
          'key':os.environ['OS_PASSWORD'],
          'tenant_name':os.environ['OS_TENANT_NAME'],
          'authurl':os.environ['OS_AUTH_URL']}

app = Flask(__name__)

celeryTasks = []

@app.route("/task/<taskId>")
def getTask(taskId):
    for task in celeryTasks:
        if task.taskId == int(taskId):
            return task.status() + "\n"
    return json.dumps(["No task found"])

@app.route("/countInObject/<container>/<objectName>")
def countPronounsInObject(container, objectName):
    connection = swiftclient.client.Connection(auth_version=2, **config)
    return startTask(container, [objectName], connection) + "\n"


@app.route("/countInObjects/<container>", methods=["POST"])
def countSpecific(container):
    objectList = request.form["objects"].split(",")
    connection = swiftclient.client.Connection(auth_version=2, **config)

    return startTask(container, objectList, connection) + "\n"


@app.route("/countAll/<container>")
def countPronouns(container):
    connection = swiftclient.client.Connection(auth_version=2, **config)

    resonse, objectList = connection.get_container(container)
    objectList = map(lambda x: x["name"], objectList)

    return startTask(container, objectList, connection) + "\n"


def startTask(container, objectList, connection):
    tasks = []

    for o in objectList:
        task = countPronounsSwift.delay(container, o, connection)
        tasks.append(task)

    celeryTask = CeleryTask(len(celeryTasks), tasks)
    celeryTasks.append(celeryTask)

    return celeryTask.status()


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
