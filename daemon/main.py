#!/usr/bin/env python3

import importlib
import inspect
import signal
import sys
import traceback
import os

from lib.Module import Module
from lib.auxiliary import *
from termcolor import colored
from threading import Thread

# Positional arguments.
P_ARGUMENTS = {
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

	print(f"Usage: {path} [ARGUMENTS]")
	print("Start the CyberTrace daemon.")
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

	log(NORMAL, "Initializing CyberTrace daemon...")

	# Parse CLI arguments.
	path = args[0]
	args = args[1::]

	settings = {
		"verbose": False,
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

	log(NORMAL, "Options:")
	log(NORMAL, f"| Verbose: {colored(settings['verbose'], 'yellow')}")

	# Appending the path declares effective root for imports.
	sys.path.append(os.path.dirname(os.path.abspath(__file__)))

	# Detection modules of type Module to be threaded by the daemon.
	buffer   = []
	modules  = []

	# Recursively import all modules files.
	for rt, dr, fn in os.walk(os.path.dirname(os.path.abspath(__file__))+"/modules"):
		for path in filter(lambda f: f.endswith(".py"), fn):
			spec = importlib.util.spec_from_file_location(
				path[:-3], os.path.join(rt, path))
			buffer.append(importlib.util.module_from_spec(spec))
			spec.loader.exec_module(buffer[-1])

	# Import individual modules.
	for module in buffer:
		for name, obj in inspect.getmembers(module):
			if inspect.isclass(obj) and obj != Module and issubclass(obj, Module):
				modules.append(obj)

	log(NORMAL, f"Loaded {len(modules)} module{'s' if len(modules) != 1 else ''}:")

	for module in modules:
		log(NORMAL, f"| {colored(module.name, 'green')} {module.version}")
		log(NORMAL, f"| -> {module.description}")

	log(NORMAL, "Initialization complete.")

	# Initialize all threads.
	threads = [Thread(target=module.irun, args=(module,)) for module in modules]

	# Run threads concurrently until a keyboard interrupt is detected.
	try:
		log(NORMAL, "Starting all threads.")
		for thread in threads: thread.start()
		for thread in threads: thread.join()

	# Upon keyboard interrupt, send kill signals to all threads and join.
	except KeyboardInterrupt:
		log(WARNING, "Sending kill signals to all threads.", start="\r")
		for module in modules: module.kill(module)
		for thread in threads: thread.join()

	# Output but otherwise ignore other exception cases.
	except:
		log(EMERGENCY, "Other exception occurred:")
		traceback.print_exc()

if __name__ == "__main__":
	main(sys.argv[0::])
