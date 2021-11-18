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

	# Thread event acts as a killswitch.
	tevent = threading.Event()

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

		return log(msgType, f"[{self.name}] {msg}")

	def run(self) -> None:
		"""
		Primary run method for the module, called on by the interval scheduler
		irun, which the daemon will search for and thread on.
		"""

		pass

	def irun(self) -> None:
		"""
		Interval scheduler for the run method, which the daemon will search for
		and thread on.
		"""

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

