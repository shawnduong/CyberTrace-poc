import os
import shlex

from lib.Module import Module
from lib.auxiliary import *

class DirbusterNginx(Module):

	name = "dirbuster (nginx)"
	version = "v0.1a"
	description = "Detect dirbuster attacks on an nginx server."

	mid = 0x10000001

	interval = 15

	atypes = {
		0x10000001: "Attack detected.",
	}

	root = os.path.dirname(os.path.abspath(__file__))

	rres = [
		f"{root}/links/access.log",
	]

	threshold = 8
	stamp = None

	def mod_init(self) -> int:
		"""
		Initialize the module by making sure that the symbolic link to the nginx
		access.log file is created. Also, add all wordlists to rres.
		"""

		conf = "/etc/nginx/nginx.conf"

		if not os.access(conf, os.F_OK):
			return FAILURE

		if not os.access(conf, os.R_OK):
			return FAILURE

		with open(conf, "r") as f:
			data = f.readlines()

		# Read the access_log setting from /etc/nginx/nginx.conf.
		for c in data:
			if "access_log" in c and ("#" not in c or c.index("access_log") < c.index("#")):
				logPath = c.split()[1][:-1]

		# Create links/ if nonexistent.
		if not os.path.exists(f"{self.root}/links/"):
			os.makedirs(f"{self.root}/links/")

		# Create wordlists/ if nonexistent.
		if not os.path.exists(f"{self.root}/wordlists/"):
			os.makedirs(f"{self.root}/wordlists/")

		# Remove pre-existing symlink if existent.
		if os.access(self.rres[0], os.F_OK):
			os.remove(self.rres[0])

		# Create symlink links/access.log -> logPath.
		os.symlink(logPath, self.rres[0])

		# Add all wordlists in wordlists/ to rres.
		for wordlist in os.listdir(f"{self.root}/wordlists/"):
			self.rres.append(f"{self.root}/wordlists/{wordlist}")

		return SUCCESS

	def tokenize(line: str) -> dict:
		"""
		Tokenize a single nginx log line and return a dictionary of the data.
		"""

		data = {
			"remote_addr"      : None,
			"remote_user"      : None,
			"time_local"       : None,
			"request"          : None,
			"status"           : None,
			"bytes_sent"       : None,
			"http_referer"     : None,
			"http_user_agent"  : None,
		}

		tokens = shlex.split(line)
		tokens[3] = " ".join([tokens[3], tokens[4]])
		tokens.pop(4)

		data["remote_addr"]      = tokens[0]
		data["remote_user"]      = tokens[2]
		data["time_local"]       = tokens[3]
		data["request"]          = tokens[4]
		data["status"]           = tokens[5]
		data["bytes_sent"]       = tokens[6]
		data["http_referer"]     = tokens[7]
		data["http_user_agent"]  = tokens[8]

		return data

	def run(self):

		# Read all available lines from the log file.
		lines = open(self.rres[0], "r").readlines()

		# Resolve the delta since the last interval.
		delta = []

		# Detected attackers.
		detected = []

		while len(lines) > 0:

			line = lines.pop()

			if line.split()[3] == self.stamp:
				break

			delta.append(line)

		# Delta length 0 implies no activity since last interval.
		if len(delta) == 0:
			return

		# Reverse delta such that index 0 is the oldest and -1 is the latest.
		delta = delta[::-1]

		# Keep track of the new stamp.
		self.stamp = delta[-1].split()[3]

		# Scan the delta for dirbuster attacks.
		for line in delta:

			data = self.tokenize(line)

			# Dirbuster advertises itself in the user agent.
			if "dirbuster" in data["http_user_agent"].lower() and data["remote_addr"] not in detected:
				self.alert(self, data["remote_addr"], 0x10000001, self.atypes[0x10000001])
				detected.append(data["remote_addr"])

