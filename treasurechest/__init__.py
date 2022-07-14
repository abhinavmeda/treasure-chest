from flask import Flask
from decouple import config

app = Flask(__name__)
app.config['SECRET_KEY'] = config('SECRET_KEY')

from treasurechest import routes
