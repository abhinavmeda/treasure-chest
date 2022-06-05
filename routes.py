import requests
import requests.auth
from flask import Flask, redirect, request, render_template
import string
import random
from decouple import config

app = Flask(__name__)

client_id = config("CLIENT_ID")
client_secret = config("CLIENT_SECRET")

base_auth_url = 'https://www.reddit.com/api/v1'
authorization_endpoint = '/authorize'
access_token_endpoint = '/access_token'

saved_route = 'https://oauth.reddit.com/user/Equivalent_Turn/saved?limit=100&after=t1_g3i8q9u'


@app.route("/", methods=["GET", "POST"])
def root():
    if request.method == 'POST':
        if request.form['submit_button'] == 'login':
            return redirect("/login")
    elif request.method == 'GET':
        return render_template("root.html")


@app.route("/login")
def first_redirect():
    state = state_generator()
    params = {
        'client_id': client_id,
        'response_type': 'code',
        'state': state,
        'redirect_uri': 'http://localhost:5000/redditor',
        'duration': 'temporary',
        'scope': 'identity, history',
        'user-agent': 'testing v0.1 by /u/Equivalent_Turn'
    }
    return redirect(url_builder(authorization_endpoint, params))


@app.route("/redditor")
def get_the_access_token():
    code = request.args.get('code')
    client_auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    post_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://localhost:5000/redditor',
    }
    post_headers = {
        'user-agent': 'testing v0.1 by /u/Equivalent_Turn'
    }
    response = requests.post(base_auth_url + access_token_endpoint, auth=client_auth, data=post_data,
                             headers=post_headers)
    token_json = response.json()
    headers = {"User-Agent": "treasure chest v1.0.0 by /u/Equivalent_Turn",
               'Authorization': "Bearer " + token_json["access_token"]}

    res = requests.get(saved_route, headers=headers).json()
    headers = {"User-Agent": "treasure chest v1.0.0 by /u/Equivalent_Turn",
               'Authorization': "Bearer " + token_json["access_token"]}
    # grab the last value at the name parameter in the json response to go through and retrieve the next 100 posts
    # from the API!

    # you're pretty much all set for the backend now.

    # just need to figure out sessions to store the username + access_token
    # work on the frontend UI
    res = requests.get(saved_route, headers=headers).json()
    return res


def state_generator(size=25, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def url_builder(endpoint, parameters):
    params = '&'.join(['%s=%s' % (k, v) for k, v in parameters.items()])
    url = '%s%s?%s' % (base_auth_url, endpoint, params)
    return url


if __name__ == "__main__":
    app.run(debug=True)

# created: time that the post was made.