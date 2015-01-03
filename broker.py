from flask import Flask, json, request, jsonify
import re #Used to get data out of our commits
from pytrack import pytrack

class youtrackMessage:
    ''' This class will carry all data and the final message
    to send to youtrack '''
    def __init__(self, ticket, author, commitMessage, commit, commitURL, timeSpent, repo, repoOwner, branch, node=None):
        self.ticket = ticket
        self.author = author
        self.commitMessage = commitMessage
        self.commit = commit
        self.commitURL = commitURL
        self.timeSpent = timeSpent
        self.repo = repo
        self.repoOwner = repoOwner
        self.branch = branch
        self.node = node

    def get_message(self):
        # return the message in it's entirety to send it to youtrack
        message = "Repository: " + self.repo + "\n" +\
            "Repository Owner: " + self.repoOwner + "\n" +\
            "Branch: " + self.branch + "\n" +\
            "Author: " + self.author + "\n" +\
            "Commit: " + self.commit + "\n" +\
            "Commit_URL: " + self.commitURL + "\n" +\
            "Commit Message: " + self.commitMessage + "\n" +\
            "Ticket: " + self.ticket + "\n"
            # "Time Spent: " + self.timeSpent
        return message

def get_timeSpent(message):
    pass

def get_ticket(message):
    ticket = re.search('([A-z])+\-([0-9]+)', message)
    ticket = ticket.group(0)
    return ticket


app = Flask(__name__)
#app.config['DEBUG'] = True

@app.route('/', methods=['GET', 'POST'])
def getData():
    #Initialize the class
    #create a new message object
    hooks = []
    repo = ''
    repoOwner = ''
    branch = ''

    if request.headers['Content-Type'] == 'text/plain':
        return "Text Message: " + request.data

    elif request.headers['Content-Type'] == 'application/json':
        # return "JSON Message: " + json.dumps(request.json)
        print request.data
        return parseInput(request.data)

    elif request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        # Production data has a 'payload' value that needs to be processed out
        data = json.dumps(request.form, encoding="utf8")
        #Convert to useable json
        data = json.loads(data)
        #get out of the payload nest!
        data = json.loads(data['payload'])
        parseData = data
        print parseData
        for key in parseData:
            print "\t", key
            if key == "repository":
                print "REPOSITORY--------------------------------"
                tempData = json.dumps(parseData[key], encoding='utf8')
                tempData = json.loads(tempData)
                print "\t\t", tempData
                for i in tempData:
                    print "\t\t\t", i
                repo = tempData["name"].lower()
                repoOwner = tempData["owner"]
                branch = ""
            elif key == "commits":
                print "COMMITS--------------------------------------"
                tempCommits = json.dumps(parseData[key], encoding='utf8')
                tempCommits = json.loads(tempCommits)

                for i in tempCommits:
                    hook = youtrackMessage('', '', '', '', '', '', '', '', '')
                    newCommit = json.dumps(i)
                    #add commit elements to the hook info
                    hook.author = i["author"]
                    hook.commitURL = "https://bitbucket.org/" + hook.repoOwner + "/" + hook.repo + "/commits/" + i["raw_node"]
                    hook.commit = "<a href ='" + hook.commitURL + "'>" + i["node"] + "</a>"
                    hook.commitMessage = i["message"]
                    hook.ticket = get_ticket(hook.commitMessage)
                    hooks.append(hook)
                print len(tempCommits)
                print

            else:
                continue
            for msg in hooks:
                msg.repo = repo
                msg.repoOwner = repoOwner
                msg.branch = ''

        print "---Hook Details---"
        # print hook.get_message()
        for i in hooks:
            print i.get_message()
        try:
            # Push to youtrack!
            for msg in hooks:
                #Set up PyTrack
                p = pytrack(<YOUTRACK_URL>, <YOUTRACK_PORT>, <USERNAME>, <PASSWORD>)
                #Create/send the comment with PyTrack
                p.add_comment(msg.ticket, msg.author, msg.get_message())
        except:
            return "Failed to submit to youtrack!"
        return hooks[0].get_message()
    else:
        return "415 - Unsupported Media Type."

if __name__ == '__main__':
  app.run(host='0.0.0.0')