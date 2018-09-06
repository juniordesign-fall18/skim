from app import app

from firebase import firebase
firebase = firebase.FirebaseApplication('https://skim-7d0f7.firebaseio.com/', None)
result = firebase.get('/test', None)
print result

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"