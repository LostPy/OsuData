"""
Project: OsuData

Author: LostPy
"""

import os

if not __name__ == "__main__":
	from .utility import Logs


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

	mode = input("What do you want to do ?"\
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
		if not path.endswith('.osu'):
			Logs.error(f"The file path isn't a beatmap ({path})!")
			return 6, path
	elif mode == '5':
		path = input("Path of folder: ")
		if not os.path.isdir(path):
			Logs.error(f"The path given isn't a folder or it wasn't found ({path})")
			return 6, path

	else:
		return 6, None

	return int(mode), path

if __name__ == "__main__":
	from express import osu_to_csv, osu_to_excel, from_beatmap, from_folder, play_music
	from utility import Logs

	mode, path = menu_mode()
	if mode == 1:
		number = input("Number of beatmap set to export (a integer), if you want export all beatmap set, pass this question: ")
		if number != "":
			try:
				number = int(number)
				number_isValid = True
			except ValueError:
				Logs.error(f"The value is not valid, please, the number must be a integer.")
				number_isValid = False
		else:
			number = None
		if number is None or number_isValid:
			csv_path = osu_to_csv(path, n=number)
			Logs.info(f"csv file save in {os.path.abspath(csv_path)}")

	elif mode == 2:
		number = input("Number of beatmap set to export (a integer), if you want export all beatmap set, pass this question: ")
		if number != "":
			try:
				number = int(number)
				number_isValid = True
			except ValueError:
				Logs.error(f"The value is not valid, please, the number must be a integer.")
				number_isValid = False
		else:
			number = None
		if number is None or number_isValid:
			excel_path = osu_to_excel(path, n=number)
			Logs.info(f"Excel file save in {os.path.abspath(excel_path)}")

	elif mode == 3:
		metadata, hitobjects, errors = from_folder(path)
		print("metadata:\n", metadata, end='\n\n')
		print("hitobjects:\n", hitobjects, end='\n\n')
		print("errors:\n", errors)

	elif mode == 4:
		valid, data = from_beatmap(path)
		if not valid:
			Logs.error("There is a error in this beatmap")
		else:
			print(data)

	elif mode == 5:
		play_music(path)
