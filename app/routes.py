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
    s = ""
    for section in class_data:
        s += '<br>'.join(section)
        s += '<br><br>'
    return s