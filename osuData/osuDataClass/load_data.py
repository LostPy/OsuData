"""
Project: OsuData

Author: LostPy
"""

import pickle
import requests as req

try:
	from sklearn import svm
	sklearn_imported = True
except ImportError:
	sklearn_imported = False
try:
	from ..bin import save_model_path
except ValueError:  # when the __main__ is script.py
	from bin import save_model_path


def stars_diff(hp: float, cs: float, od: float, ar: float, slider_multiplier: float, model=None):
	if sklearn_imported and ar != '':
		if model is None:
			with open(save_model_path, 'rb') as save:
				model = pickle.load(save)
		stars = round(model.predict([[hp, cs, od, ar, slider_multiplier]])[0], ndigits=2)
	else:
		stars = 0.

	return stars


def load_beatmap(filepath: str, lines: list = None, count_hitobjects: bool = True, model=None) -> dict:
	"""
	A function to extract beatmap datas.
	return a list with the datas of the beatmap : [version_fmt, Title, Artist, Creator, DifficultyName, HP, CS, OD, HR, time]
	"""
	try:
		if lines is None:
			with open(filepath, 'r', encoding='utf-8') as beatmap:
				lines = [l for l in beatmap.read().split('\n') if l != '']

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

		count_normal = 0
		count_slider = 0
		count_spinner = 0
		if count_hitobjects:
			hitobjects = lines[line.index('[HitObjects]')+1:]
			for line in hitobjects:
				hit_data = line.split(',')[3]
				if hit_data[3] == 0:
					count_normal += 1
				elif hit_data[3] == 1:
					count_slider += 1
				elif hit_data[3] == 3:
					count_spinner += 1
		data = {
		'version_fmt': version_fmt,
		'countdown': int(general[3][-1]),
		'mode': mode,
		'title': metadatas[0][6:],
		'artist': metadatas[1][7:] if version_fmt < 10 else metadatas[2][7:],
		'creator': metadatas[2][8:] if version_fmt < 10 else metadatas[4][8:],
		'difficulty_name': metadatas[3][8:] if version_fmt < 10 else metadatas[5][8:],
		'hp': difficulties[0][12:],
		'cs': difficulties[1][11:],
		'od': difficulties[2][18:],
		'ar': difficulties[3][13:] if version_fmt > 7 else '',
		'slider_multiplier': difficulties[3][17:] if version_fmt <= 7 else difficulties[4][17:],
		'slider_tick_rate': difficulties[4][15:] if version_fmt <= 7 else difficulties[5][15:],
		'time': int(time),
		'count_normal': count_normal,
		'count_slider': count_slider,
		'count_spinner': count_spinner}
		data['stars'] = stars_diff(data['hp'], data['cs'], data['od'], data['ar'], data['slider_multiplier'], model)

		return True, data
	except IndexError:
		return False, [filepath]
