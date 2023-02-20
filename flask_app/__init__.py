from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.secret_key = "password"

DATABASE = "recipes_schema"

BCRYPT = Bcrypt(app)