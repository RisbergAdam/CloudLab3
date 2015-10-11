from flask import Flask, request
from CeleryWorker import countPronounsSwift
import os
import swiftclient.client
import json

config = {'user':os.environ['OS_USERNAME'], 
          'key':os.environ['OS_PASSWORD'],
          'tenant_name':os.environ['OS_TENANT_NAME'],
          'authurl':os.environ['OS_AUTH_URL']}

app = Flask(__name__)


@app.route("/countPronouns/<container>/<objectName>")
def countPronounsInObject(container, objectName):
#    container = request.form["container"]
#    objectName = request.form["object"]

    connection = swiftclient.client.Connection(auth_version=2, **config)

    return countPronounsSwift.delay(container, objectName, connection).get() + "\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
