"""
Project: OsuDatas

Author: LostPy
"""

import pandas as pd


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

