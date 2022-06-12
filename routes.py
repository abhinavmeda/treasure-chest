from typing import List
import os
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

with open("sessions.txt") as f:
    first_line = f.readline()

session = {'user': first_line}
f.close()
saved_route = 'https://oauth.reddit.com/user/Equivalent_Turn/saved?limit=100'


@app.route("/", methods=["GET", "POST"])
def root():
    if request.method == 'POST' and session['user'] == '':
        if request.form['submit_button'] == 'login':
            return redirect("/login")
    elif request.method == 'GET' and session['user'] == '':
        return render_template("root.html")
    else:
        return redirect("/redditor")


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

    if session['user'] == '':
        return redirect(url_builder(authorization_endpoint, params))
    else:
        return redirect("/redditor")


@app.route("/redditor")
def get_the_access_token():
    if session['user'] == '':
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
        session["user"] = token_json["access_token"]
        file = open('sessions.txt', 'w')
        file.write(token_json["access_token"])
        file.close()

    headers = {"User-Agent": "treasure chest v1.0.0 by /u/Equivalent_Turn",
               'Authorization': "Bearer " + session["user"]}
    if os.stat('data.txt').st_size == 0:
        json_response = requests.get(saved_route, headers=headers).json()
        ls = parse_json_to_usable_dictionary(json_response)
        after_parameter = json_response['data']['after']
        while after_parameter is not None:
            after_route = saved_route + '&after={}'.format(after_parameter)
            new_response = requests.get(after_route, headers=headers).json()
            after_parameter = new_response['data']['after']
            ls += parse_json_to_usable_dictionary(new_response)
        with open("data.txt", "w") as file:
            for data in ls:
                file.write(str(data))
                file.write("\n")

    with open("data.txt", "r") as file:
        lines = file.readlines()
    return render_template("treasure.html", data=lines)


@app.route("/logout")
def logout():
    if session['user'] != '':
        session['user'] = ''
    file = open('sessions.txt', 'w')
    file.write('\n')
    file.close()
    return 'done!'


def state_generator(size=25, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def url_builder(endpoint, parameters):
    params = '&'.join(['%s=%s' % (k, v) for k, v in parameters.items()])
    url = '%s%s?%s' % (base_auth_url, endpoint, params)
    return url


def parse_json_to_usable_dictionary(json_response) -> List:
    ls = []
    for things in json_response['data']['children']:
        kind = things["kind"]
        if kind == "t1":
            data = things["data"]
            ls.append({"kind": things["kind"],
                       "subreddit": data["subreddit"],
                       "author": data["author"],
                       "body": data["body"],
                       "link": data["link_url"]})
        elif kind == "t3":
            data = things["data"]
            keys = data.keys()
            if 'url_overridden_by_dest' in keys:
                ls.append({"kind": things["kind"],
                           "subreddit": data["subreddit"],
                           "author": data["author"],
                           "picture": data["url_overridden_by_dest"],
                           "link": data["url"]})
            else:
                ls.append({"kind": things["kind"],
                           "subreddit": data["subreddit"],
                           "author": data["author"],
                           "body": data["selftext"],
                           "link": data["url"]})

    return ls


if __name__ == "__main__":
    app.run(debug=True)

# created: time that the post was made.
