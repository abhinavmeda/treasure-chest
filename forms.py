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
                                                         Length(min=3, max=20)])
    email = StringField(label='email', validators=[DataRequired(), Email()])

    password = PasswordField(label='password', validators=[DataRequired(),
                                                           Length(min=6, max=12)])

    confirm_password = PasswordField(label='confirm password', validators=[DataRequired(),
                                                                           Length(min=6, max=12),
                                                                           EqualTo('password')])
    submit = SubmitField(label='register')


class LoginForm(FlaskForm):
    """Form that logs users into the application.

    """
    username = StringField(label='username', validators=[DataRequired(),
                                                         Length(min=3, max=20)])
    password = PasswordField(label='password', validators=[DataRequired(),
                                                           Length(min=6, max=12)])
    remember = BooleanField(label='remember me')

    submit = SubmitField(label='login')
