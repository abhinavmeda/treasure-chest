from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RedirectToLoginOrRegister(FlaskForm):
    # variable name will show up as the key and label will become value
    # when form data gets returned
    login = SubmitField(label='login')
    register = SubmitField(label='register')


class RegistrationForm(FlaskForm):
    """Form that registers users into the application

    """
    username = StringField(label='username', validators=[DataRequired(),
                                                         Length(min=3, max=20)], render_kw={'placeholder': 'username'})
    email = StringField(label='email', validators=[DataRequired(), Email()], render_kw={'placeholder': 'email'})

    password = PasswordField(label='password', validators=[DataRequired(),
                                                           Length(min=6, max=12)],
                             render_kw={'placeholder': 'password'})

    confirm_password = PasswordField(label='confirm password', validators=[DataRequired(),
                                                                           Length(min=6, max=12),
                                                                           EqualTo('password')],
                                     render_kw={'placeholder': 'confirm password'})
    submit = SubmitField(label='register')


def validate_email_or_username(form, field):
    # TODO Check if passed in field is a username or email in the database
    return True


class LoginForm(FlaskForm):
    """Form that logs users into the application.

    """
    email_or_username = StringField(label='email_or_username', validators=[DataRequired(),
                                                                           Length(min=3, max=20),
                                                                           validate_email_or_username],
                                    render_kw={'placeholder': 'Email address or username'})

    password = PasswordField(label='password', validators=[DataRequired(),
                                                           Length(min=6, max=12)],
                             render_kw={'placeholder': 'password'})
    remember = BooleanField(label='remember me')

    submit = SubmitField(label='login')


