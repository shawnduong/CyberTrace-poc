import subprocess

def traceroute(dest: str) -> dict:
	"""
	Trace the route to some destination IP and return a dict of intermediates.
	In order to prevent the daemon itself from needing to run with elevated
	privileges, this is primarily handled by the system's traceroute utility.
	"""

	# Sanitize input.
	for char in dest:
		if char not in "ABCDEFabcdef12345567890.:":
			return -1

	# Run system traceroute.
	p = subprocess.Popen(["traceroute", "-q 1", dest], stdout=subprocess.PIPE)
	d = p.stdout.read().decode("utf-8")

	hops = {}

	# Parse the output.
	for line in d.split("\n"):

		try:
			tokens = line.split()
			n = int(tokens[0])

			if tokens[1] == "*":
				ip = "?"
			else:
				ip = tokens[2].strip("(").strip(")")

			hops[n] = ip
		except:
			pass

	return hops

