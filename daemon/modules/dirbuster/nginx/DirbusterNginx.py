from lib.Module import Module
from lib.auxiliary import *

class DirbusterNginx(Module):

	name = "dirbuster (nginx)"
	version = "(stub)"
	description = "Detect dirbuster attacks on an nginx server."

	interval = 5

	def run(self):

		self.log(self, VERBOSE, "(stub)")

