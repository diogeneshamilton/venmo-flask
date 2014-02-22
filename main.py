from flask import Flask, request, redirect, session
from constants import CONSUMER_ID, CONSUMER_SECRET, APP_SECRET
import requests

app = Flask(__name__)
# comment out when you're done testing
app.debug = True
app.secret_key = APP_SECRET

@app.route('/')
def index():
    if session.get('venmo_token'):
        return 'Your Venmo token is %s' % session.get('venmo_token')
    else:
        return redirect('https://api.venmo.com/v1/oauth/authorize?client_id=%s&scope=make_payments,access_profile&response_type=code' % CONSUMER_ID)

@app.route('/oauth-authorized')
def oauth_authorized():
    AUTHORIZATION_CODE = request.args.get('code')
    data = {
        "client_id":CONSUMER_ID,
        "client_secret":CONSUMER_SECRET,
        "code":AUTHORIZATION_CODE
        }
    url = "https://api.venmo.com/v1/oauth/access_token"
    response = requests.post(url, data)
    response_dict = response.json()
    access_token = response_dict.get('access_token')
    user = response_dict.get('user')

    session['venmo_token'] = access_token
    session['venmo_username'] = user['username']

    return 'You were signed in as %s' % user['username']

if __name__ == '__main__':
    app.run()
