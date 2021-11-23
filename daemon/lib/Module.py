import ipaddress
import os
import socket
import time
import threading

from lib.auxiliary import *
from lib.ModuleDB import *
from sqlalchemy.orm import Session
from typing import Union

class Module:
	"""
	A template for module type classes, which all CyberTrace detection modules
	should inherit from.
	"""

	# Basic module information.
	name = None
	version = None
	description = None

	# Uniquely assigned module identification number.
	mid = None

	# Module verbosity setting.
	verbose = False

	# Thread event acts as a killswitch.
	tevent = threading.Event()

	# Database session.
	db = None

	# Socket for IPC.
	sock = None

	# Module settings.

	# Minimum polling interval in seconds.
	interval = 15

	# A dictionary of alert/attack types.
	atypes = {}

	# List of string paths to resources requiring read (4) access.
	rres = []

	# List of string paths to resources requiring write (2) access.
	wres = []

	# List of string paths to resources requiring executability (1).
	xres = []

	def log(self, msgType: int, msg: str) -> Union[None, tuple]:
		"""
		Wrap around the default logging function to include the module name in
		all logging messages.
		"""

		if msgType != VERBOSE or self.verbose:
			return log(msgType, f"[{self.name}] {msg}")

	def mod_init(self) -> int:
		"""
		Module-defined initialization method, usually used for prerequisite
		installation steps.
		"""

		return SUCCESS

	def init(self, db: Session, sock: socket.socket, verbosity: bool=False) -> int:
		"""
		Initialize variables; ensure that all resources have sufficient read,
		write, and/or executability permissions; and build the attack and alert
		type database.
		"""

		self.db       = db
		self.verbose  = verbosity
		self.sock     = sock

		self.log(self, VERBOSE, "Initializing module...")

		exitCode = SUCCESS

		if self.mod_init(self) == FAILURE:
			self.log(self, WARNING, f"Module-defined initialization sequence failed.")
			exitCode = FAILURE

		for res in set(self.rres + self.wres + self.xres):
			if not os.access(res, os.F_OK):
				self.log(self, WARNING, f"{res} could not be found.")
				exitCode = FAILURE

		for res in self.rres:
			if not os.access(res, os.R_OK):
				self.log(self, WARNING, f"{res} cannot be read from.")
				exitCode = FAILURE

		for res in self.wres:
			if not os.access(res, os.W_OK):
				self.log(self, WARNING, f"{res} cannot be written to.")
				exitCode = FAILURE

		for res in self.xres:
			if not os.access(res, os.X_OK):
				self.log(self, WARNING, f"{res} cannot be executed.")
				exitCode = FAILURE

		self.db.add(ModuleDB.Module(self.mid, self.name, self.version, self.description))
		self.db.commit()

		if len(self.atypes) > 0:
			for k in self.atypes.keys():
				self.db.add(ModuleDB.Attack(self.mid, k, self.atypes[k]))
				self.db.commit()

		self.log(self, VERBOSE, "Module and attack database built.")
		self.log(self, VERBOSE, "Module initialization complete.")

		return exitCode

	def run(self) -> None:
		"""
		Primary run method for the module, called on by the interval scheduler
		irun, which the daemon will search for and thread on.
		"""

		pass

	def irun(self, db: Session, sock: socket.socket, verbosity: bool=False) -> None:
		"""
		Interval scheduler for the run method, which the daemon will search for
		and thread on.
		"""

		if self.init(self, db, sock, verbosity) == FAILURE:
			self.log(self, EMERGENCY, "Module failed initialization.")
			return

		while not self.tevent.is_set():

			start = time.time()
			self.log(self, VERBOSE, "Starting interval...")
			self.run(self)
			self.log(self, VERBOSE, "Interval complete.")

			if ((e:=time.time()) - start) < self.interval:
				self.tevent.wait(self.interval - (e-start))

		self.log(self, VERBOSE, "Thread completed.")

	def kill(self) -> None:
		"""
		Kill a thread gracefully by setting the event killswitch.
		"""

		self.log(self, EMERGENCY, "Thread kill signal received.")
		self.tevent.set()

	def alert(self, ip: str, atype: int) -> None:
		"""
		Send an alert message amsg of type atype through a socket object sock.
		This will send a message of the following low-level byte format:
		[4 B mid][4 B atype][1 B ipversion][(4|16) B ipaddr]
		"""

		self.log(self, NORMAL, f"ALERT (type={hex(atype)}; ip={ip}): {self.atypes[atype]}")

		ipversion = 0
		ipaddr = 0

		if ip != None:
			if "." in ip:
				ipversion = 4
				ipaddr = int(ipaddress.IPv4Address(ip))
			elif ":" in ip:
				ipversion = 6
				ipaddr = int(ipaddress.IPv6Address(ip))

		msg  = b""
		msg += self.mid.to_bytes(4, "big")
		msg += atype.to_bytes(4, "big")
		msg += ipversion.to_bytes(1, "big")

		if ipversion == 4:
			msg += ipaddr.to_bytes(4, "big")
		elif ipversion == 6:
			msg += ipaddr.to_bytes(16, "big")
		else:
			msg += ipaddr.to_bytes(1, "big")

		self.sock.send(msg)

