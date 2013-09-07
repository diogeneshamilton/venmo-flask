from flask import Flask, request, redirect, session
from constants import CONSUMER_KEY, CONSUMER_SECRET, APP_SECRET_KEY
import requests

app = Flask(__name__)
app.debug = True
app.secret_key = APP_SECRET_KEY

@app.route('/')
def index():
    if session.get('venmo_token'):
        return 'Your Venmo token is %s' % session.get('venmo_token')
    else:
        return redirect('https://api.venmo.com/oauth/authorize?client_id=%s&scope=make_payments,access_profile&response_type=code' % CONSUMER_KEY)

@app.route('/oauth-authorized')
def oauth_authorized():
    AUTHORIZATION_CODE = request.args.get('code')
    data = {
        "client_id":CONSUMER_KEY,
        "client_secret":CONSUMER_SECRET,
        "code":AUTHORIZATION_CODE
        }
    url = "https://api.venmo.com/oauth/access_token"
    response = requests.post(url, data)
    response_dict = response.json()
    app.logger.debug(response_dict)
    access_token = response_dict.get('access_token')
    user = response_dict.get('user')

    session['venmo_token'] = access_token
    session['venmo_username'] = user['username']

    return 'You were signed in as %s' % user['username']

if __name__ == '__main__':
    app.run()
