import os
import sqlalchemy as db

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

class CacheDB:
	"""
	A database for cached items, including IP address approximate coordinates.
	"""

	# Path to the DB.
	path = None

	# DB engine.
	engine = None

	# DB session.
	session = None

	# DB declarative base.
	base = declarative_base()

	class IP(base):
		"""
		A definition for an IP address, relating an IPv4 or IPv6 address to a
		set of latitude, longitude coordinates.
		"""

		__tablename__ = 'ip'

		ip         = db.Column(db.String, primary_key=True)
		latitude   = db.Column(db.Float, nullable=False)
		longitude  = db.Column(db.Float, nullable=False)

		def __init__(self, ip, latitude, longitude):

			self.ip         = ip
			self.latitude   = latitude
			self.longitude  = longitude

	def __init__(self, path: str):

		self.path     = path
		self.engine   = db.create_engine(f"sqlite:///{path}")
		self.session  = Session(self.engine)

		self.base.metadata.create_all(self.engine)

