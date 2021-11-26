from __future__ import annotations

import bcrypt

from app import db

from flask_login import UserMixin
from typing import Union

class User(UserMixin, db.Model):
	"""
	A definition for a single user, consisting of an ID, username, password, and
	account type (0=>admin; 1=>user; 2=>pending).
	"""

	id       = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(256), unique=True , nullable=False)
	password = db.Column(db.String(256), unique=False, nullable=False)
	acctType = db.Column(db.Integer    , unique=False, nullable=False)

	def __init__(self, username="", password="", acctType=""):
		"""
		Constructor method for User type objects.
		"""

		self.username = username
		self.password = password
		self.acctType = acctType

	def login(username: str, password: str) -> Union[User, bool]:
		"""
		Check if the username and password are valid, returning a User object
		if successful, or False if unsuccessful.
		"""

		if ((user:=User.query.filter_by(username=username).first()) != None
			and bcrypt.checkpw(password.encode(), user.password)
		):
			return user
		else:
			return False

	def register(username: str, password: str) -> bool:
		"""
		Attempt to register a user, returning True if successful or False if
		the registration failed.
		"""

		try:
			if User.query.filter_by(username=username).first() == None:
				user = User(username, bcrypt.hashpw(password.encode(), bcrypt.gensalt(4)), 2)
				db.session.add(user)
				db.session.commit()
				return True
		except:
			return False

		return False

