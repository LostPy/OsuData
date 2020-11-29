"""
Project: OsuDatas

Author: LostPy
"""

import os
import pandas as pd

from logs import Logs
from osuProgressBar import progress_bar


def load_beatmap(filepath: str, lines: list = None) -> dict:
	"""
	A function to extract beatmap datas.
	return a list with the datas of the beatmap : [version_fmt, Title, Artist, Creator, DifficultyName, HP, CS, OD, HR, time]
	"""
	try:
		if lines is None:
			with open(filepath, 'r', encoding='utf-8') as beatmap:
				lines = beatmap.read().split('\n')
				while '' in lines:
					lines.remove('')
		metadatas = lines[lines.index('[Metadata]')+1:lines.index('[Difficulty]')]
		difficulties = lines[lines.index('[Difficulty]')+1:lines.index('[Events]')]
		time = lines[-1].split(',')[2]
		version_fmt = int(lines[0][lines[0].find("v")+1:])
	except IndexError:
		return False, [filepath]

	datas = {
	'version_fmt': version_fmt,
	'title': metadatas[0][6:],
	'Artist': metadatas[1][7:] if version_fmt < 10 else metadatas[2][7:],
	'Creator': metadatas[2][8:] if version_fmt < 10 else metadatas[4][8:],
	'DifficultyName': metadatas[3][8:] if version_fmt < 10 else metadatas[5][8:],
	'HP': difficulties[0][12:],
	'CS': difficulties[1][11:],
	'OD': difficulties[2][18:],
	'AR': difficulties[3][13:] if version_fmt > 7 else '',
	'time': int(time)}

	return True, datas


def from_beatmap(filepath: str) -> pd.DataFrame:
	"""
	Function to extract metadatas of a beatmap
	"""
	valid, datas = load_beatmap(filepath)
	if valid:
		return True, pd.DataFrame(data=datas, columns=datas.keys(), index=range(1))
	else:
		return False, datas


def from_folder(folderpath: str):
	"""
	A function read and extract beatmaps datas of a folder
	"""
	beatmaps = []
	errors = []

	for name in os.listdir(folderpath):
		if os.path.isfile(os.path.join(folderpath, name)) and name.endswith((".osu", )):
			valid, df = from_beatmap(os.path.join(folderpath, name))
			if valid:
				beatmaps.append([df])
			else:
				errors += df
	df_beatmaps = pd.concat(beatmaps).reset_index(drop=True, inplace=True)
	return df_beatmaps, errors


def from_osu(folderpath: str):
	"""
	The main function: read the osu! folder and extract beatmaps datas.
	"""
	beatmaps = []
	errors = []

	Logs.info(f"La lecture de tout les fichiers .osu se trouvant dans '{folderpath}' va débuter.")
	Logs.info("Cette action peut prendre quelque temps selon la quantité de fichiers à lire.\n\n")
	time.sleep(5)
	songspath = os.path.join(folderpath, 'Songs/')

	list_dir = os.listdir(songspath)
	speed = 0.
	for i, name in enumerate(list_dir):
		if os.path.isdir(os.path.join(songspath, name)):
			start = time.time()
			progress_bar(i, len(list_dir), info=os.path.join(songspath, name), suffix=f'Directories - ({speed} dir/s)')
			beatmaps_folder, errors_folder = from_folder(os.path.join(songspath, name))
			beatmaps.append(beatmaps_folder)
			errors += errors_folder
			end = time.time()
			speed = round(1 / (end - start), ndigits=3) if end - start != 0. else speed
	
	df_beatmaps = pd.concat(beatmaps).reset_index(drop=True, inplace=True)
	return df_beatmaps, errors