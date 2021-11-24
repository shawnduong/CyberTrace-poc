import random
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, login_required
from flask_login import current_user, login_user, logout_user

# Instantiate the application and define settings.
app = Flask(__name__)
app.config["FLASK_ADMIN_SWATCH"] = "united"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = random.randbytes(256)

# Instantiate the database.
db = SQLAlchemy(app)

from models import Users
from routes import *
from admin import *

db.create_all()

def run(host="127.0.0.1", port=5000, debug=False):
    app.run(host=ip, port=port, debug=debug)


if __name__ == "__main__":
    print("ERROR: This file should not be run directly. Did you mean to call the main entry point program instead?", file=sys.stderr)
    exit(-1)
