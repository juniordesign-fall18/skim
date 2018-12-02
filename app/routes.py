from app import app
import pyrebase
import datetime
import json
import urllib.request
# app._static_folder = app.path.abspath("static/style.css")
from flask import render_template, request


config = {
  "apiKey": "AIzaSyB5bnl9QMIeQRFHg5Io5CfKEFLCTyMGIYU",
  "authDomain": "skim-7d0f7.firebaseapp.com",
  "databaseURL": "https://skim-7d0f7.firebaseio.com/",
  "storageBucket": "skim-7d0f7.appspot.com",
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

index_URL = 'https://www.uah.edu/cgi-bin/schedule.pl?file='

current_year = 2018
current_semester = 0

@app.route('/')
def chart_fetch():
    subjects = db.get().val()
    class_dict = {}
    for subject, classes in subjects.items():
        class_dict[subject] = {}
        for class_no, years in classes.items():
            currentEnrollment_data = []
            maxEnrollment_data = []
            labels = []
            for year, semesters in sorted(years.items()):
                for semester, data in reversed(sorted(semesters.items())):
                    maxEnrollment_data.append(data["maxEnrollment"])
                    currentEnrollment_data.append(data["currentEnrollment"])
                    labels.append(semester + " " + year)
            class_dict[subject][class_no] = (labels, currentEnrollment_data, maxEnrollment_data)
    return render_template('chart.html', data=class_dict)

@app.route('/datastore')
def data_store(segment, year, semester):
    fetched_data = getDecodedRequestSegment(segment, year, semester)
    class_data = stripClassData(fetched_data)

    if semester == 0:
        sem = "Spring"
    else:
        sem = "Fall"

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
            classEntry = {"name": title, "section": section, "currentEnrollment": newline[5], "maxEnrollment": newline[4], "waitlist": waitlist}
            result = db.child(segment).child(course_number).child(year).child(sem).set(classEntry)
    return "Data stored"

@app.route('/segments')
def seg_fetch():
    for i in range(2017, 2018):
        for j in range(2):
            if j != 1:
                fetched_data = getDecodedRequest(i, j)
                dep_names = stripClassNames(fetched_data)
                for dep in dep_names:
                    data_store(dep, i, j)
    # return str(dep_names)
    return "Data successfully stored"

def getIndexURL(year, semester):
    season = 'sprg' if semester == 0 else 'fall'
    archived = '' if year == current_year else '&dir=archived'
    return index_URL + str(season) + str(year) + '.html' + archived

def getSegmentURL(segment, year, semester):
    return getIndexURL(year, semester) + '&segment=' + segment

def getDecodedRequestSegment(segment, year, semester):
    url = getSegmentURL(segment, year, semester)
    print(url)
    return urllib.request.urlopen(url).read().decode('utf-8')

def getDecodedRequest(year, semester):
    url = getIndexURL(year, semester)
    print(url)
    return urllib.request.urlopen(url).read().decode('utf-8')

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
