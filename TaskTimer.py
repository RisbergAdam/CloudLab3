import time
import pycurl
import json
import cStringIO

start = time.time()

buf = cStringIO.StringIO()
c = pycurl.Curl()
c.setopt(c.URL, "127.0.0.1:5000/countInObject/tweets/tweets_19.txt")
c.setopt(c.WRITEFUNCTION, buf.write)
c.perform()
jResponse = json.loads(buf.getvalue())
taskId = jResponse["id"]

while 1:
    buf = cStringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, "127.0.0.1:5000/task/" + str(taskId))
    c.setopt(c.WRITEFUNCTION, buf.write)
    c.perform()


    jResponse = json.loads(buf.getvalue())
    if jResponse["done"]: break
    buf.close()
    time.sleep(1)
    print str(time.time() - start)

end = time.time()

print "total time taken: " + str(end - start)
