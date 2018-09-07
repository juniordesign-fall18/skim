from app import app
from firebase import firebase
import datetime
import json
import urllib.request

URL = 'https://www.uah.edu/cgi-bin/schedule.pl?file=sprg2018.html&segment=ACC'

@app.route('/')

@app.route('/index')
def index():
    dbapp = firebase.FirebaseApplication('https://skim-7d0f7.firebaseio.com/', None)
    result = dbapp.get('/test', None)
    return result


@app.route('/datastore')
def data_store():
    dbapp = firebase.FirebaseApplication('https://skim-7d0f7.firebaseio.com/', None)

    fetched_data = urllib.request.urlopen(URL).read().decode('utf-8')
    class_data = stripHTML(fetched_data)

    for x in range(len(class_data)):
        courses = class_data[x]

        for s in range(len(courses)):
            newline = courses[s].split("  ")

            if newline[0].isalpha():
                newline.remove(newline[0])

            while '' in newline:
                newline.remove('')

            #fix waitlist issues
            
            classEntry = {"courseAndSection": newline[1], "name": newline[2], "maxEnrollment": newline[4], "currentEnrollment": newline[5], "waitlist": newline[7].split(" ")[:1], "semester": "spring", "year": "2018"}

            dbapp.post('https://skim-7d0f7.firebaseio.com/', classEntry)


    # courses = class_data[0]
    # newline = courses[0].split("  ")
    #
    # if newline[0].isalpha():
    #     newline.remove(newline[0])
    #
    # while '' in newline:
    #     newline.remove('')
    #
    # classEntry = {"courseAndSection": newline[0], "name": newline[1], "maxEnrollment": newline[3], "currentEnrollment": newline[4], "waitlist": newline[6], "semester": "spring", "year": "2018"}
    #
    # dbapp.post('https://skim-7d0f7.firebaseio.com/', classEntry)

    return "0"




def stripHTML(data):
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

@app.route('/data')
def data_fetch():
    fetched_data = urllib.request.urlopen(URL).read().decode('utf-8')
    class_data = stripHTML(fetched_data)
    # class_data is of the form [[line, line, ...], [line, line, ....], ...]
    s = ""
    for section in class_data:
        s += '<br>'.join(section)
        s += '<br><br>'
        print('\n'.join(section))
    return s


# def data_store():
#     AccountingForBusiness = {"courseNumber": "210", "sectionNumber": "01", "name": "Accounting For Business", "maxEnrollment": "53", "currentEnrollment": "49", "waitlist": "0"} db.child("skim-7d0f7").push(AccountingForBusiness, user['idToken'])

# dbapp = db.reference('https://skim-7d0f7.firebaseio.com/')
# classes_dbapp = dbapp.child('classes')
# classes_dbapp.set({
#     'alanisawesome': {
#         'date_of_birth': 'June 23, 1912',
#         'full_name': 'Alan Turing'
#     },
#     'gracehop': {
#         'date_of_birth': 'December 9, 1906',
#         'full_name': 'Grace Hopper'
#     }
# })
