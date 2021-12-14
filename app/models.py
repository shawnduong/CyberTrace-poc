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

	__tablename__ = "user"

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

class Host(db.Model):
	"""
	A definition for a single host IP and its associated host key.
	"""

	__tablename__ = "host"

	id  = db.Column(db.Integer, primary_key=True)
	ip  = db.Column(db.String(64), unique=True, nullable=False)
	key = db.Column(db.String(64), unique=True, nullable=False)

	def __init__(self, ip, key):
		"""
		Constructor method for Host type objects.
		"""

		self.ip  = ip
		self.key = key

class Association(db.Model):
	"""
	A definition for a single user-host mapping, denoting that said user is
	authorized to view data from such host.
	"""

	__tablename__ = "association"

	id    = db.Column(db.Integer, primary_key=True)
	user  = db.Column(db.Integer, db.ForeignKey(User.id), unique=False, nullable=False)
	host  = db.Column(db.Integer, db.ForeignKey(Host.id), unique=False, nullable=False)

	def __init__(self, user, host):
		"""
		Constructor method for Association type objects.
		"""

		self.user = user
		self.host = host

class Event(db.Model):
	"""
	A definition for a single event consisting of various types of information
	sent by the daemon via the middleware.
	"""

	__tablename__ = "event"

	id                   = db.Column(db.Integer, primary_key=True)
	epoch_timestamp      = db.Column(db.Integer)
	module_id            = db.Column(db.Integer)
	module_name          = db.Column(db.String(256))
	module_description   = db.Column(db.String(256))
	attack_type          = db.Column(db.Integer)
	attack_description   = db.Column(db.String(256))
	victim_ip_version    = db.Column(db.Integer)
	victim_ip_address    = db.Column(db.String(64))
	victim_lat           = db.Column(db.Float)
	victim_lon           = db.Column(db.Float)
	attacker_ip_version  = db.Column(db.Integer)
	attacker_ip_address  = db.Column(db.String(64))
	attacker_lat         = db.Column(db.Float)
	attacker_lon         = db.Column(db.Float)
	traceroute           = db.Column(db.JSON)

	def __init__(self, epoch_timestamp=-1, module_id=-1, module_name="",
		module_description="", attack_type=-1, attack_description="",
		victim_ip_version=-1, victim_ip_address="", victim_lat=-999.0,
		victim_lon=-999.0, attacker_ip_version=-1, attacker_ip_address="",
		attacker_lat=-999.0, attacker_lon=-999.0, traceroute={}
	):

		self.epoch_timestamp      = epoch_timestamp
		self.module_id            = module_id
		self.module_name          = module_name
		self.module_description   = module_description
		self.attack_type          = attack_type
		self.attack_description   = attack_description
		self.victim_ip_version    = victim_ip_version
		self.victim_ip_address    = victim_ip_address
		self.victim_lat           = victim_lat
		self.victim_lon           = victim_lon
		self.attacker_ip_version  = attacker_ip_version
		self.attacker_ip_address  = attacker_ip_address
		self.attacker_lat         = attacker_lat
		self.attacker_lon         = attacker_lon
		self.traceroute           = traceroute

