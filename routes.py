from flask import Flask, redirect, request, render_template, flash, url_for
from forms import RegistrationForm, LoginForm, RedirectToLoginOrRegister
from decouple import config

app = Flask(__name__)
app.config['SECRET_KEY'] = config('SECRET_KEY')


@app.route("/", methods=["GET", "POST"])
def homepage():
    button = RedirectToLoginOrRegister()
    if button.is_submitted():
        if 'login' in request.form:
            return redirect("/login")
        elif 'register' in request.form:
            return redirect("/register")
    else:
        return render_template("homepage.html", form=button, visibility="hidden")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        s = ""
        for k in request.form:
            s += "{} = {} ".format(k, request.form[k])
        return s
    print(form.errors)
    return render_template('login.html', form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash("Account created for {}".format(form.username.data), 'success')
        return redirect(url_for('homepage'))
    else:
        pass
        # TODO flash("Account created for {}".format(form.username.data), 'danger')
    return render_template('register.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
