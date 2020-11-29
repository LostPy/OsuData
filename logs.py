"""
Project: discord Bot "Stats Bot"
Version: 1.0
Author: LostPy | Discord : Lost Music 🎶:notes:#8691
"""

from datetime import datetime
from colorama import Fore, init


def datetime_log() -> str:
	current_datetime = datetime.now()
	return current_datetime.strftime("%Y-%m-%d to %H:%M:%S")


class Logs:
	init()  # init colorama for Window
	color_debug = Fore.CYAN
	color_info = Fore.WHITE
	color_warning = Fore.YELLOW
	color_error = Fore.RED
	color_success = Fore.GREEN

	@staticmethod
	def info(msg: str):
		msg_log = f"[{datetime_log()}][INFO] {msg}"
		print(Logs.color_info + msg_log + Fore.RESET)

	@staticmethod
	def debug(msg: str):
		msg_log = f"[{datetime_log()}][DEBUG] {msg}"
		print(Logs.color_debug + msg_log + Fore.RESET)

	@staticmethod
	def error(msg: str):
		msg_log = f"[{datetime_log()}][ERROR] {msg}"
		print(Logs.color_error + msg_log + Fore.RESET)

	@staticmethod
	def warning(msg: str):
		msg_log = f"[{datetime_log()}][WARNING] {msg}"
		print(Logs.color_warning + msg_log + Fore.RESET) 

	@staticmethod
	def success(msg: str):
		msg_log = f"[{datetime_log()}][SUCCESS] {msg}"		
		print(Logs.color_success + msg_log + Fore.RESET) 

