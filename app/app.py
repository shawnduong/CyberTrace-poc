import sys

from flask import *

# Instantiate the application and define settings.
app = Flask(__name__)

# Load the routes.
from routes import *

if __name__ == "__main__":
	print("ERROR: This file should not be run directly. Did you mean to call"
		+ "the main entry point program instead?", file=sys.stderr)
	exit(-1)
