#!/usr/bin/env python3

import sys

from lib.auxiliary import *

# Positional arguments.
P_ARGUMENTS = {
	("<IP>",)      : "IP address the API resides on (default=\"127.0.0.1\")",
	("<PORT>",)    : "Port on the <IP> the API resides on (default=8080)",
	("<API>",)     : "API endpoint to POST to (default=\"/api/report\")",
	("<SOCKET>",)  : "IPC socket path (default=\"/tmp/ctrace.sock\")",
}

# Optional help arguments.
H_ARGUMENTS = {
	("-h", "--help"): "Display the help menu and exit.",
}

# Optional arguments.
O_ARGUMENTS = {
	("-v", "--verbose"): "Enable verbose output.",
}

def print_help(path: str="main.py", alignmentWidth: int=16) -> None:
	"""
	Output help menu to stdout upon request. LHS args are aligned to a fixed
	width of alignmentWidth columns.
	"""

	# Shorthand alignment function for aligning to the ALIGNMENT_WIDTH.
	align = lambda s: s + ' '*(alignmentWidth-len(s))

	print(f"Usage: {path} [ARGUMENTS] <IP> <PORT> <API> <SOCKET>")
	print("Start the CyberTrace middleware that connects the daemon to the API.")
	print()

	print("Help:")
	for key in H_ARGUMENTS:
		print(align(", ".join([*key])) + H_ARGUMENTS[key])

	print("Positional arguments:")
	for key in P_ARGUMENTS:
		print(align(", ".join([*key])) + P_ARGUMENTS[key])

	print("Optional arguments:")
	for key in O_ARGUMENTS:
		print(align(", ".join([*key])) + O_ARGUMENTS[key])

def main(args: list=["./main.py"]):

	# Parse CLI arguments.
	path = args[0]
	args = args[1::]

	settings = {
		"verbose"   : False,
		"ip"        : "127.0.0.1",
		"port"      : 8080,
		"api"       : "/api/report",
		"socket"    : "/tmp/ctrace.sock",
	}

	# Parsing help arguments.
	if any([arg in list(*H_ARGUMENTS.keys()) for arg in args]):
		print_help(path)
		return 0

	# Parsing verbose arguments.
	if any([arg in ("-v", "--verbose") for arg in args]):
		try:
			settings["verbose"] = True
			args.remove("-v")
			args.remove("--verbose")
		except:
			pass

	# Parsing positional arguments.
	try:
		settings["ip"]      = args.pop(0)
		settings["port"]    = args.pop(0)
		settings["api"]     = args.pop(0)
		settings["socket"]  = args.pop(0)
	except:
		pass

	log(NORMAL, "Initializing CyberTrace middleware...")
	log(NORMAL, "Options:")
	log(NORMAL, "| Verbose  : %s" % colored(settings["verbose"], "yellow"))
	log(NORMAL, "| Endpoint : %s" % colored(
		f"{settings['ip']}:{settings['port']}{settings['api']}", "yellow"))
	log(NORMAL, "| Socket   : %s" % colored(settings["socket"], "yellow"))

if __name__ == "__main__":
	main(sys.argv[0::])
