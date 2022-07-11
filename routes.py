from flask import Flask, redirect, request, render_template
from forms import RegistrationForm, LoginForm, RedirectToLoginOrRegister
import requests
import requests.auth
import string
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ab6f63cb8ebded43ea3cb70bcb9389fa'


@app.route("/", methods=["GET", "POST"])
def homepage():
    button = RedirectToLoginOrRegister()
    if request.method == 'GET':
        return render_template("homepage.html", form=button)
    if request.method == 'POST':
        if 'login' in request.form:
            return redirect("/login")
        elif 'register' in request.form:
            return redirect("/register")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)
    # if request.method == "GET":
    #     return render_template("login.html")
    # else:
    #     # TODO check if form fields for username and email exist in database.
    #     return "Account logged in as {}".format(request.form.get("value"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        form = RegistrationForm()
        return render_template('register.html', form=form)
    else:
        s = ""
        for k in request.form:
            s += "{} = {} ".format(k, request.form[k])
        return s
    # if request.method == "GET":
    #     return render_template("register.html")
    # else:
    #     # TODO check if form fields for username and email exist in database.
    #     return "Account Created {}, {}".format(request.form.get("username_field"), request.form.get("email_field"))


if __name__ == "__main__":
    app.run(debug=True)
