import os
import sqlalchemy as db

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

class ModuleDB:
	"""
	A database for all modules, including a table for modules as well as a
	table attacks/alerts.
	"""

	# Path to the DB.
	path = None

	# DB engine.
	engine = None

	# DB session.
	session = None

	# DB declarative base.
	base = declarative_base()

	class Module(base):
		"""
		A definition for a module, relating a module ID to a name, version, and
		description.
		"""

		__tablename__ = 'module'

		id           = db.Column(db.Integer, primary_key=True)
		name         = db.Column(db.String(256), nullable=False)
		version      = db.Column(db.String(256), nullable=False)
		description  = db.Column(db.String(256), nullable=False)

		def __init__(self, moduleID, name, version, description):

			self.id           = moduleID
			self.name         = name
			self.version      = version
			self.description  = description

	class Attack(base):
		"""
		A definition for an attack/alert, relating module IDs to attack IDs and
		descriptions.
		"""

		__tablename__ = 'attack'

		id           = db.Column(db.Integer, primary_key=True)
		moduleID     = db.Column(db.Integer, db.ForeignKey("module.id"), nullable=False)
		attackID     = db.Column(db.Integer, nullable=False)
		description  = db.Column(db.String(256), nullable=False)

		def __init__(self, moduleID, attackID, description):

			self.moduleID     = moduleID
			self.attackID     = attackID
			self.description  = description

	def __init__(self, path: str, refresh: bool=True):

		if refresh and os.access(path, os.F_OK):
			os.remove(path)

		self.path     = path
		self.engine   = db.create_engine(f"sqlite:///{path}")
		self.session  = Session(self.engine)

		self.base.metadata.create_all(self.engine)

