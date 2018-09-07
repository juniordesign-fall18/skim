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

@app.route('/data')
def data_fetch():
    url = urllib.request.urlopen(URL)
    output = url.read()
    return output