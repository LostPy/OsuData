"""
Project: OsuData

Author: LostPy
"""

import os
import time
import pickle

import pandas as pd
import pydub
try:
	from sklearn import svm
	sklearn_imported = True
except ImportError:
	sklearn_imported = False

try:
	from ..utility import Logs, progress_bar
	from ..osuDataClass import Beatmap, BeatmapSet
	from ..osuDataClass.beatmapError import BeatmapError
except ValueError:  # When script.py is the __main__
	from utility import Logs, progress_bar
	from osuDataClass import Beatmap, BeatmapSet
	from osuDataClass.beatmapError import BeatmapError


def to_csv(folderpath: str, api_key: str = None, csv_path: str = ''):
	beatmap_set = BeatmapSet.from_folder(folderpath, api_key=api_key, hitobjects=False)
	if beatmap_set.ratio_error < 1.:
		csv_path = f'./{beatmap_set.title}.csv' if csv_path == '' else csv_path
		beatmap_set.to_csv(csv_path)
		return csv_path

	raise BeatmapError(f"There isn't beatmap in the folder: '{folderpath}', or one error was found in all beatmaps")


def to_excel(folderpath: str, api_key: str = None, excel_path: str = '', **kwargs):
	beatmap_set = BeatmapSet.from_folder(folderpath, api_key=api_key)
	if beatmap_set.ratio_error < 1.:
		metadatas = beatmap_set.to_dataframe()
		hitobjects = beatmap_set.dataframe_hitobjects()
		excel_path = f'./{beatmap_set.title}.xlsx' if excel_path == '' else excel_path
		with pd.ExcelWriter(excel_path, mode='w') as writer:
			for df, name in zip([metadatas, hitobjects], ['metadatas', 'hitobjects']):
				df.to_excel(writer, sheet_name=name, **kwargs)
		return excel_path

	raise BeatmapError(f"There isn't beatmap in the folder: '{folderpath}', or one error was found in all beatmaps")


def mp3_to_wav(mp3_path: str, wav_path: str = ''):
	if wav_path == '':
		wav_path = './mp3_to_wav.wav'
	mp3 = pydub.AudioSegment.from_mp3(mp3_path)
	mp3.export(wav_path, format="wav")
	return wav_path


def beatmapSet_objects(osu_path: str, api_key: str = None, n: int = None, hitobjects=False, compact_log: bool = False, display_progress: bool = True):
	"""
	A function to extract osu! beatmaps data and return the list of BeatmapSet object
	and the list path of beatmaps where there is a error.
	"""
	beatmap_set_objects = []
	errors = []
	if display_progress:
		Logs.info(f"Playback of all .osu files in '{osu_path}' will start.")
		Logs.info("This action may take some time depending on the amount of files to be read...\n\n")
		if api_key is not None:
			Logs.warning("\rIn order not to exceed the limit imposed by the osu! reference API, the speed of folder reading can be reduced if necessary. https://osu.ppy.sh/docs/index.html#terms-of-use\n\n")
			time.sleep(2)
		time.sleep(5)
	songspath = os.path.join(osu_path, 'Songs/')
	list_dir = os.listdir(songspath)
	if n is None or n > len(list_dir):
		n = len(list_dir)
	n_init = n
	speed = 0.
	current_speed = 0.
	try:
		for i, name in enumerate(list_dir):
			if os.path.isdir(os.path.join(songspath, name)):
				start = time.time()
				if display_progress:  # update of the progress bar
					i_real = i-(n-n_init)
					progress_bar(i_real, n_init, start=0 if i == i_real else -1, info=os.path.join(songspath, name), length=60, suffix=f'Directories - ({current_speed} dir/s - mean: {speed} dir/s)', compact=compact_log)
				try:
					beatmap_set = BeatmapSet.from_folder(os.path.join(songspath, name), api_key=api_key, hitobjects=hitobjects)
					beatmap_set_objects.append(beatmap_set)
				except ValueError:  # BeatmapSet not published
					beatmap_set = BeatmapSet(os.path.join(songspath, name))
					beatmap_set.ratio_error = 1.
					errors.append(os.path.join(songspath, name))
				errors += beatmap_set.errors
				end = time.time()
				delay = end - start
				if delay != 0:
					if api_key is not None and (n > 1200 and len(list_dir) > 1200) and delay < (60/1000):  # To keep a number of request < 1200/min (https://osu.ppy.sh/docs/index.html#terms-of-use)
						time.sleep(6/100)
						delay += 6/100
					speed = round((1 / delay+speed*i) / (i+1), ndigits=3)
					current_speed = round(1 / delay, ndigits=3)
				if beatmap_set.ratio_error == 1.:
					n += 1
				if i == n_init:
					break
	except ConnectionError:
		Logs.errors("A error of connection was raised, check your connection and retry after several seconds.")
	return beatmap_set_objects, errors


def from_beatmap(filepath: str):
	"""Function to extract metadatas of a beatmap."""
	beatmap = Beatmap.from_file(filepath)
	if beatmap.valid:
		return True, beatmap.to_dataframe()

	return False, beatmap.path  # return the path of beatmap if there is a error in import.


def from_folder(folderpath: str, api_key: str = None):
	"""A function read and extract beatmaps datas of a folder."""
	beatmap_set = BeatmapSet.from_folder(folderpath, api_key=api_key)
	metadata = beatmap_set.to_dataframe()
	hitobjects_data = beatmap_set.dataframe_hitobjects()
	return metadata, hitobjects_data, beatmap_set.errors


def from_osu(osu_path: str, api_key: str = None, n: int = None, compact_log: bool = False, display_progress: bool = True):
	"""A function to extract beatmaps data from osu folder and return two dataframe and a list of path where there is a error."""
	beatmap_set_objects, errors = beatmapSet_objects(osu_path, api_key=api_key, n=n, compact_log=compact_log, display_progress=display_progress)
	Logs.info("Merge all data...")
	metadata = pd.concat([beatmap_set.to_dataframe() for beatmap_set in beatmap_set_objects], axis=0).reset_index(drop=True)
	if display_progress and len(errors) > 0:
		Logs.warning(f'A error was found in these files: {errors}')
		Logs.warning('A error can be raise if the version of osu! file format is < 5. If you use the api key argument, the error is a connexion error')
	elif display_progress and len(errors) == 0:
		Logs.success('There is not error during the export data')
	Logs.success("Merge all data completed")
	return metadata, errors


def osu_to_csv(osu_path: str, api_key: str = None, csv_path:str = '', n: int = None, compact_log: bool = False, display_progress=True):
	"""Export metadata or hitobjects in a csv file."""
	metadata, errors = from_osu(osu_path, api_key=api_key, n=n, compact_log=compact_log, display_progress=display_progress)
	Logs.info("the csv file is being created...")
	csv_path = './osu_data.csv' if csv_path == '' else csv_path
	metadata.to_csv(csv_path, sep='$', index=False)
	return csv_path


def osu_to_excel(osu_path: str, api_key: str = None, excel_path: str = '', n: int = None, compact_log: bool = False, display_progress=True, **kwargs):
	"""Export metadata and hitobjects in a xlsx file."""
	metadata, errors = from_osu(osu_path, api_key=api_key, n=n, compact_log=compact_log, display_progress=display_progress)
	mode = 'w' if excel_path.strip() == '' else 'a'
	excel_path = './osu_data.xlsx' if excel_path == '' else excel_path
	with pd.ExcelWriter(excel_path, mode=mode) as writer:
		Logs.info("the 'metadata' sheet is being created...")
		metadata[:1048576].to_excel(writer, sheet_name='metadata', index=False, **kwargs)

	if metadata.shape[0] > 1048576:
		Logs.warning(f'The sheet "metadata" is too large ({metadata.shape[0]} lines), the maximum size has been keeping (1048576)')
	if len(errors) > 0:
		Logs.warning(f'There is a error or more was found in these files: {errors}')
		Logs.warning('A error can be raise if the version of osu! file format is < 5.')
	else:
		Logs.success('There is not error during the export data')
	return excel_path
