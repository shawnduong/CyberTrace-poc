import sys

from flask import *
from flask_sqlalchemy import *

# Instantiate the application and define settings.
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "YOUR_KEY_HERE"

# Load the database.
db = SQLAlchemy(app)
from models import *
db.create_all()

# Load the routes.
from routes import *

# Load the authentication functionality.
from authentication import *

if __name__ == "__main__":
	print("ERROR: This file should not be run directly. Did you mean to call"
		+ "the main entry point program instead?", file=sys.stderr)
	exit(-1)
