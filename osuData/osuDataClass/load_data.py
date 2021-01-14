"""
Project: OsuData

Author: LostPy
"""

import pickle
import requests as req
from pandas import read_json

try:
	from sklearn import svm
	sklearn_imported = True
except ImportError:
	sklearn_imported = False
try:
	from ..bin import (
		path_diffAim_modelA, path_diffAim_modelB,
		path_diffSpeed_modelA, path_diffSpeed_modelB,
		path_stars_modelA, path_stars_modelB)
except ValueError:  # when the __main__ is script.py
	from bin import (
		path_diffAim_modelA, path_diffAim_modelB,
		path_diffSpeed_modelA, path_diffSpeed_modelB,
		path_stars_modelA, path_stars_modelB)


def predict_diff(hp: float, cs: float, od: float, ar: float, modelsA: list = None, modelsB: list = None):
	if sklearn_imported:
		if ar != '':
			if modelsA is None:
				with open(path_diffSpeed_modelA, 'rb') as save:
					model_speed = pickle.load(save)
				with open(path_diffAim_modelA, 'rb') as save:
					model_aim = pickle.load(save)
				with open(path_stars_modelA, 'rb') as save:
					model_stars = pickle.load(save)
			else:
				model_speed = modelsA[0]
				model_aim = modelsA[1]
				model_stars = modelsA[2]
			diff_speed = round(model_speed.predict([[od, ar]])[0], ndigits=3)
			diff_aim = round(model_aim.predict([[od, ar]])[0], ndigits=3)
			stars = round(model_stars.predict([[hp, cs, od, ar, diff_speed, diff_aim]])[0], ndigits=3)
		else:
			if modelsB is None:
				with open(path_diffSpeed_modelB, 'rb') as save:
					model_speed = pickle.load(save)
				with open(path_diffAim_modelB, 'rb') as save:
					model_aim = pickle.load(save)
				with open(path_stars_modelB, 'rb') as save:
					model_stars = pickle.load(save)
			else:
				model_speed = modelsB[0]
				model_aim = modelsB[1]
				model_stars = modelsB[2]
			diff_speed = round(model_speed.predict([[od]])[0], ndigits=3)
			diff_aim = round(model_aim.predict([[od]])[0], ndigits=3)
			stars = round(model_stars.predict([[od, diff_speed, diff_aim]])[0], ndigits=3)
	else:
		diff_speed = 0.
		diff_aim = 0.
		stars = 0.

	return stars, diff_speed, diff_aim


def load_beatmap(filepath: str, lines: list = None, modelsA: list = None, modelsB: list = None) -> dict:
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

		if version_fmt >= 5:
			countdown = int(general[3][-1])
		else:
			countdown = None

		data = {
		'version_fmt': version_fmt,
		'countdown': countdown,
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
		'time': int(time)}
		data['stars'], data['diff_speed'], data['diff_aim'] = predict_diff(data['hp'], data['cs'], data['od'], data['ar'], modelsA, modelsB)

		return True, data
	except IndexError:
		return False, [filepath]


def beatmaps_from_http(key: str, beatmapset_id: int = None, beatmap_id: int = None, mode: int = None):
	url = 'https://osu.ppy.sh/api/get_beatmaps?'
	r = req.get(url, params={'k': key, 's': beatmapset_id, 'b': beatmap_id, 'm': mode})
	return read_json(r.text)
