# Auxiliary definitions.

import time

from termcolor import colored
from typing import Union

# Universal failure/success return codes.
FAILURE = -1
SUCCESS =  0

# Log message types.
NORMAL     = 0
VERBOSE    = 1
WARNING    = 2
EMERGENCY  = 3

def log(msgType: int, msg: str) -> Union[None, tuple]:
	"""
	Logging function that will automatically color and channelize log messages
	given a msgType (NORMAL, VERBOSE, WARNING, EMERGENCY) and message.
	"""

	msg = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] :: {msg}"

	if msgType in (0, 1):
		print(msg)
	elif msgType == 2:
		print(colored(msg, "yellow"))
	elif msgType == 3:
		print(colored(msg, "red"))
	else:
		return (FAILURE, f"Invalid msgType={msgType}")

