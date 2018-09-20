from app import app
# from firebase import firebase
import pyrebase
import datetime
import json
import urllib.request

from flask import render_template, request

index_URL = 'https://www.uah.edu/cgi-bin/schedule.pl?file=sprg2018.html'

config = {
  "apiKey": "AIzaSyB5bnl9QMIeQRFHg5Io5CfKEFLCTyMGIYU",
  "authDomain": "skim-7d0f7.firebaseapp.com",
  "databaseURL": "https://skim-7d0f7.firebaseio.com/",
  "storageBucket": "skim-7d0f7.appspot.com",
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

@app.route('/')

@app.route('/datastore')
def data_store(segment):
    fetched_data = getDecodedRequestSegment(segment)
    class_data = stripClassData(fetched_data)

    for x in range(len(class_data)):
        courses = class_data[x]

        for s in range(len(courses)):
            newline = courses[s].split("  ")

            if newline[0].isalpha():
                newline.remove(newline[0])

            while '' in newline:
                newline.remove('')
            
            course_number, section = newline[1].split(" ")[0], newline[1].split(" ")[1]
            title = newline[2]
            waitlist = newline[7].split(" ")[0]
            
            classEntry = {"name": title, "section": section, "currentEnrollment": newline[5], "maxEnrollment": newline[4], "waitlist": waitlist, "semester": "spring", "year": "2018"}

            result = db.child(segment).child(course_number).set(classEntry)

    return "Data stored"

@app.route('/segments')
def seg_fetch():
    fetched_data = getDecodedRequest()
    dep_names = stripClassNames(fetched_data)
    for dep in dep_names:
        data_store(dep)
    return str(dep_names)

@app.route('/search')
def data_fetch():
    fetched_data = getDecodedRequestSegment('ACC')
    class_data = stripClassData(fetched_data)
    # class_data is of the form [[line, line, ...], [line, line, ....], ...]
    result = {}
    all_classes = db.child("ACC").get()
    for c in all_classes.each():
        result[c.key()] = c.val()
    result = json.dumps(result)
    return render_template('index.html', data=result)

@app.route('/search',methods=['POST'])
def on_post():
    user_query = request.form['search']
    query = []
    for l in user_query:
        if l.isdigit():
            query.append(user_query[:user_query.index(l)])
            query.append(user_query[user_query.index(l):])
            break
    all_classes = db.child(query[0]).child(query[1]).get()
    result = {}
    for c in all_classes.each():
        result[c.key()] = c.val()
    return json.dumps(result)

def getSegmentURL(class_code):
    return index_URL + '&segment=' + class_code

def getDecodedRequestSegment(segment):
    return urllib.request.urlopen(getSegmentURL(segment)).read().decode('utf-8')

def getDecodedRequest():
    return urllib.request.urlopen(index_URL).read().decode('utf-8')

def stripClassData(data):
    split_data = [x.strip() for x in data.split('\n')]
    results = []
    pre_tag = '<pre>'
    hr_tag = '<HR>'
    while (pre_tag in split_data):
        pre_index = split_data.index(pre_tag)
        split_data = split_data[pre_index:]
        hr_index = split_data.index(hr_tag)
        results.append(split_data[4:hr_index])
        split_data = split_data[hr_index:]
    return results

def stripClassNames(data):
    split_data = [x.strip() for x in data.split('\n')]
    pre_tag = '<pre>'
    end_tag = '</pre>'
    pre_index = split_data.index(pre_tag)
    end_index = split_data.index(end_tag)
    split_data = split_data[pre_index+1:end_index]
    results = [line[line.index('>')+1:line.index('</')] for line in split_data]
    return results