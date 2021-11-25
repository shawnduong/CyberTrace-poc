from __future__ import annotations

import bcrypt

from app import db
from flask_login import UserMixin
from typing import Union

class User(UserMixin, db.Model):
	"""
	A definition for a single user, consisting of an ID, username, password, and
	account type (0=>admin; 1=>user).
	"""

	id       = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(256), unique=True , nullable=False)
	password = db.Column(db.String(256), unique=False, nullable=False)
	acctType = db.Column(db.Integer    , unique=False, nullable=False)

	def login(username: str, password: str) -> Union[User, bool]:
		"""
		Check if the username and password are valid, returning a 
		"""

		# For debugging, passwords are currently stored in plaintext. Hashing
		# will be implemented later.
#		if ((user:=User.query.filter_by(username=username).first()) != None
#			and bcrypt.checkpw(password.encode(), user.password)
#			and password == user.password

		if ((user:=User.query.filter_by(username=username).first()) != None
			and password == user.password
		):
			return user
		else:
			return False

