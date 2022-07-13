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

    def validate_username(self, field):
        # TODO Check database if username already exists and raise error if it does
        # if field.data in DB:
        # RAISE VALIDATION_ERROR
        pass

    def validate_email(self, field):
        # TODO Check database if email already exists and raise error if it does
        # if field.data in DB:
        # RAISE VALIDATION_ERROR
        pass


class LoginForm(FlaskForm):
    """Form that logs users into the application.

    """
    email_or_username = StringField(label='email_or_username', validators=[DataRequired(),
                                                                           Length(min=3, max=20)],
                                    render_kw={'placeholder': 'Email or username'})

    password = PasswordField(label='password', validators=[DataRequired(),
                                                           Length(min=6, max=12)],
                             render_kw={'placeholder': 'password'})
    remember = BooleanField(label='remember me')

    submit = SubmitField(label='login')

    def validate_email_or_username(self, field):
        # TODO Check if field.data is email by using regex
        # TODO Check if field.data is email
        # if field.data in DB:
        # RAISE VALIDATION_ERROR
        pass


