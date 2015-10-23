import json
import cPickle

class CeleryTask:

    def __init__(self, taskId, workerTasks):
        self.taskId = taskId
        self.workerTasks = map(lambda x: (x, True), workerTasks)
        self.taskCount = len(workerTasks)
        self.pronouns = {"han": 0 , "hon": 0, "den": 0, "det": 0, "denna": 0, "denne": 0, "hen": 0}
        print self.taskCount

    def status(self):
        for i, (task, state) in enumerate(self.workerTasks):
            if task.ready():
                self.workerTasks[i] = (task, False)
                p = cPickle.loads(task.get())
                self.combinePronouns(p)
        self.workerTasks = filter(lambda (k, v): v, self.workerTasks)
        return json.dumps({"id":self.taskId, "done":len(self.workerTasks) == 0, "pronouns":self.pronouns})

    def combinePronouns(self, p):
        for k, v in p.items():
            self.pronouns[k] += v
