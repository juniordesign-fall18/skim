from app import app

from firebase import firebase

@app.route('/')
@app.route('/index')
def index():
    dbapp = firebase.FirebaseApplication('https://skim-7d0f7.firebaseio.com/', None)
    result = dbapp.get('/test', None)
    return result