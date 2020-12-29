"""
Project: OsuData

Author: LostPy
"""

import requests
import pickle

try:
	from sklearn import svm
	sklearn_imported = True
except ImportError:
	sklearn_imported = False


def stars_diff(hp: float, cs: float, od: float, ar: float, slider_multiplier: float, save=None):
	if sklearn_imported:
		save_isNone = save is None
		if save_isNone:
			save = open('../bin/save_model.bin', 'rb')
		model = pickle.load(save)

		if save_isNone:
			save.close()

		stars = model.predict([[hp, cs, od, ar, slider_multiplier]])[0]
	else:
		stars = 0.

	return stars


def load_beatmap(filepath: str, lines: list = None, file_model=None) -> dict:
	"""
	A function to extract beatmap datas.
	return a list with the datas of the beatmap : [version_fmt, Title, Artist, Creator, DifficultyName, HP, CS, OD, HR, time]
	"""
	try:
		if lines is None:
			with open(filepath, 'r', encoding='utf-8') as beatmap:
				lines = beatmap.read().split('\n')
				lines = [l for l in lines if l != '']
		if '[Editor]' in lines:
			general = lines[lines.index('[General]')+1:lines.index('[Editor]')]
		else:
			general = lines[lines.index('[General]')+1:lines.index('[Metadata]')]
		metadatas = lines[lines.index('[Metadata]')+1:lines.index('[Difficulty]')]
		difficulties = lines[lines.index('[Difficulty]')+1:lines.index('[Events]')]
		time = lines[-1].split(',')[2]
		version_fmt = int(lines[0][lines[0].find("v")+1:])
		if version_fmt <= 5 and len(general) < 7:
			mode = 0
		elif version_fmt <= 5:
			mode = int(general[6][-1]) if general[6][:4].lower() == 'mode' else 0
		else:
			mode = int(general[6][-1])

		data = {
		'version_fmt': version_fmt,
		'countdown': int(general[3][-1]),
		'mode': mode,
		'title': metadatas[0][6:],
		'Artist': metadatas[1][7:] if version_fmt < 10 else metadatas[2][7:],
		'Creator': metadatas[2][8:] if version_fmt < 10 else metadatas[4][8:],
		'DifficultyName': metadatas[3][8:] if version_fmt < 10 else metadatas[5][8:],
		'HP': difficulties[0][12:],
		'CS': difficulties[1][11:],
		'OD': difficulties[2][18:],
		'AR': difficulties[3][13:] if version_fmt > 7 else '',
		'SliderMultiplier': difficulties[3][17:] if version_fmt <= 7 else difficulties[4][17:],
		'SliderTickRate': difficulties[4][15:] if version_fmt <= 7 else difficulties[5][15:],
		'time': int(time)}
		data['Stars'] = stars_diff(data['HP'], data['CS'], data['OD'], data['AR'], data['SliderMultiplier'], file_model)

		return True, data
	except IndexError:
		return False, [filepath]


if __name__ == '__main__':
	print(load_beatmap('/media/lost/Data-Windows-Jeux/osu!/Songs/3631 Elfen Lied - Lilium/Elfen Lied - Lilium (Saturos-fangirl) [Easy].osu')[1])
