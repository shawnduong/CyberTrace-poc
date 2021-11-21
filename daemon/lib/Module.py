import socket
import time
import threading

from lib.auxiliary import *
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

	# Socket for IPC.
	sock = None

	# Module settings.

	# Minimum polling interval in seconds.
	interval = 15

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

	def run(self) -> None:
		"""
		Primary run method for the module, called on by the interval scheduler
		irun, which the daemon will search for and thread on.
		"""

		pass

	def irun(self, sock: socket.socket, verbosity: bool=False) -> None:
		"""
		Interval scheduler for the run method, which the daemon will search for
		and thread on.
		"""

		self.verbose = verbosity
		self.sock    = sock

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

	def alert(self, atype: int, amsg: str) -> None:
		"""
		Send an alert message amsg of type atype through a socket object sock.
		This will send a message of the following low-level byte format:
		[4 B mid][4 B atype][4 B len][len B amsg]
		"""

		self.log(self, NORMAL, f"ALERT (type={atype}): {amsg}")

		msg  = b""
		msg += self.mid.to_bytes(4, "big")
		msg += atype.to_bytes(4, "big")
		msg += len(amsg).to_bytes(4, "big")
		msg += amsg.encode()

		self.sock.send(msg)

