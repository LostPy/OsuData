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
		"\n\t2- Read osu! folder and export datas in excel"\
		"\n\t3- Read beatmaps of a folder and display datas"\
		"\n\t4- Read a beatmap and display datas."\
		"\n\t5- Play the music of a osu folder"\
		"\n\t6- [Other answer] stop the program.\nAnswer: ")

	if mode == '1':
		path = input("Path folder of your 'osu!' application: ")
		type_ = input("Type data to export (metadata or hitobjects): ")
		if not os.path.isdir(path):
			Logs.error(f"The path given isn't a folder or it wasn't found ({path})")
			path = ""
			return 6, path, type_
		elif type_.lower() not in ("metadata", "hitobjects"):
			Logs.error(f"Option not valid: '{type_}'. Choose 'metadata' or 'hitobjects'")
			return 6, path, type_

	elif mode == '2':
		path = input("Path folder of your 'osu!' application: ")
		if not os.path.isdir(path):
			Logs.error(f"The path given isn't a folder or it wasn't found ({path})")
			path = ""
			return 6, path, type_

	elif mode == '3':
		path = input("Path of folder: ")
		if not os.path.isdir(path):
			Logs.error(f"The path given isn't a folder or it wasn't found ({path})")
			path = ""
			return 6, path, type_

	elif mode == '4':
		path = input("Path of file '.osu': ")
		if not path_beatmap.endswith('.osu'):
			Logs.error(f"The file path isn't a beatmap ({path})!")
			path == ""
			return 6, path, type_
	elif mode == '5':
		path = input("Path of folder: ")
		if not os.path.isdir(path):
			Logs.error(f"The path given isn't a folder or it wasn't found ({path})")
			path = ""
			return 6, path, type_

	else:
		return 6, None, type_

	return int(mode), path, type_

if __name__ == "__main__":
	mode, path, type_ = menu_mode()
	if mode == 1:
		export.osu_to_csv(path, data_type=type_)

	elif mode == 2:
		export.osu_to_excel(path)

	elif mode == 3:
		excel_path = export.to_excel(path)
		Logs.info(f"Excel file save in {excel_path}")

	elif mode == 4:
		pass

	elif mode == 5:
		info.play_music(path)

	Logs.info('END\n---------------')