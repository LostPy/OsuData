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
		1- Read osu! folder and export datas in csv
		2- Read osu! folder and export datas in excel
		3- Read beatmaps of a folder and display datas
		4- Read a beatmap and display datas.
		5- Play the music of a osu folder
		6- [Other answer] stop the program.Answer: 
	"""

	mode = input("What do you do ?"\
		"\n\t1- Read osu! folder and export datas in csv"\
		"\n\t2- Read osu! folder and export datas in excel"\
		"\n\t3- Read beatmaps of a folder and display datas"\
		"\n\t4- Read a beatmap and display datas."\
		"\n\t5- Play the music of a osu folder"\
		"\n\t6- [Other answer] stop the program.\nAnswer: ")

	if mode == '1':
		path = input("Path folder of your 'osu!' application: ")
		if not os.path.isdir(path):
			Logs.error(f"The path given isn't a folder or it wasn't found ({path})")
			return 6, path

	elif mode == '2':
		path = input("Path folder of your 'osu!' application: ")
		if not os.path.isdir(path):
			Logs.error(f"The path given isn't a folder or it wasn't found ({path})")
			return 6, path

	elif mode == '3':
		path = input("Path of folder: ")
		if not os.path.isdir(path):
			Logs.error(f"The path given isn't a folder or it wasn't found ({path})")
			return 6, path

	elif mode == '4':
		path = input("Path of file '.osu': ")
		if not path_beatmap.endswith('.osu'):
			Logs.error(f"The file path isn't a beatmap ({path})!")
			return 6, path
	elif mode == '5':
		path = input("Path of folder: ")
		if not os.path.isdir(path):
			Logs.error(f"The path given isn't a folder or it wasn't found ({path})")
			return 6, path

	else:
		return int(mode), None

	return int(mode), path

if __name__ == "__main__":
	mode, path = menu_mode()
	if mode == 1:
		csv_path = export.osu_to_csv(path)
		Logs.info(f"csv file save in {os.path.abspath(csv_path)}")

	elif mode == 2:
		excel_path = export.osu_to_excel(path)
		Logs.info(f"Excel file save in {os.path.abspath(excel_path)}")

	elif mode == 3:
		metadata, hitobjects, errors = export.from_folder(path)
		print("metadata:\n", metadata, end='\n\n')
		print("hitobjects:\n", hitobjects, end='\n\n')
		print("errors:\n", errors)

	elif mode == 4:
		valid, data = export.from_beatmap(path)
		if not valid:
			Logs.error("There is a error in this beatmap")
		else:
			print(data)

	elif mode == 5:
		info.play_music(path)
