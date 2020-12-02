"""
Project: OsuDatas

Author: LostPy
"""

import os

from logs import Logs
import export
import info


def menu_mode():
	"""
	A simple menu console to choose the action between:
		1- read osu! folder and export datas in csv
		2- read beatmaps of a folder and display datas
		3- read a beatmap and display datas
		4- stop the program
	"""

	type_ = None

	mode = input("What do you do ?"\
		"\n\t1- Read osu! folder and export datas in csv"\
		"\n\t2- Read beatmaps of a folder and display datas"\
		"\n\t3- Read a beatmap and display datas."\
		"\n\t4- [Other answer] stop the program.\nAnswer: ")

	if mode == '1':
		path = input("Path folder of your 'osu!' application: ")
		type_ = input("Type data to export (metadata or hitobjects): ")
		if not os.path.isdir(path):
			Logs.error(f"The path given isn't a folder or it wasn't found ({path})")
			path = ""
			return 4, path, type_
		elif type_.lower() not in ("metadata", "hitobjects"):
			Logs.error(f"Option not valid: '{type_}'. Choose 'metadata' or 'hitobjects'")
			return 4, path, type_

	elif mode == '2':
		path = input("Path of folder: ")
		if not os.path.isdir(path):
			Logs.error(f"The path given isn't a folder or it wasn't found ({path})")
			path = ""
			return 4, path, type_

	elif mode == '3':
		path = input("Path of file '.osu': ")
		if not path_beatmap.endswith('.osu'):
			Logs.error(f"The file path isn't a beatmap ({path})!")
			path == ""
			return 4, path, type_

	else:
		return 4, None, type_

	return int(mode), path, type_

if __name__ == "__main__":
	mode, path, type_ = menu_mode()
	if mode == 1:
		export.osu_to_csv(path, data_type=type_)

	elif mode == 2:
		pass

	elif mode == 3:
		pass

	Logs.info('END\n---------------')