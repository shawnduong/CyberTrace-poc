from lib.Module import Module
from lib.auxiliary import *

class DirbusterNginx(Module):

	name = "dirbuster (nginx)"
	version = "(stub)"
	description = "Detect dirbuster attacks on an nginx server."

	mid = 0x10000001

	interval = 5

	atypes = {
		0x10000001: "Attack detected.",
	}

	rres = [
		"/var/log/nginx.log",
	]

	def run(self):

		self.alert(self, 1, "(stub)")

