"""
Project: OsuDatas

Author: LostPy
"""

import os
import time

import numpy as np
import pandas as pd
import pydub

from logs import Logs
from osuProgressBar import progress_bar
from beatmap import Beatmap
from musicOsu import MusicOsu
from beatmapError import BeatmapError


def to_csv(folderpath: str, csv_path: str = ''):
	musicosu = MusicOsu.from_folder(folderpath)
	if musicosu.ratio_error < 1.:
		csv_path = f'./{musicosu.title}.csv' if csv_path == '' else csv_path
		musicosu.to_csv(csv_path)
		return csv_path
	else:
		raise BeatmapError(f"There isn't beatmap in the folder: '{folderpath}', or one error was found in all beatmaps")


def to_excel(folderpath: str, excel_path: str = '', *args, **kwargs):
	musicosu = MusicOsu.from_folder(folderpath)
	if musicosu.ratio_error < 1.:
		metadatas = musicosu.to_dataframe()
		hitobjects = musicosu.dataframe_hitobjects()
		print(metadatas)
		print(hitobjects)
		mode = 'w' if excel_path.strip() == '' else 'a'
		excel_path = f'./{musicosu.title}.xlsx' if excel_path == '' else excel_path
		print(mode)
		with pd.ExcelWriter(excel_path, mode=mode) as writer:
			for df, name in zip([metadatas, hitobjects], ['metadatas', 'hitobjects']):
				df.to_excel(writer, sheet_name=name, *args, **kwargs)  # à verifier
		return excel_path

	else:
		raise BeatmapError(f"There isn't beatmap in the folder: '{folderpath}', or one error was found in all beatmaps")


def mp3_to_wav(mp3_path: str, wav_path: str = ''):
	if wav_path == '':
		wav_path = './mp3_to_wav.wav'
	mp3 = pydub.AudioSegment.from_mp3(mp3_path)
	mp3.export(wav_path, format="wav")
	return wav_path


def musicOsu_objects(osu_path: str, display_progress: bool = True):
	"""
	A function to extract osu! beatmaps data and return the list of MusicOsu object
	and the list path of beatmaps where there is a error.
	"""
	musicosu_objects = []
	errors = []
	if display_progress:
		Logs.info(f"Playback of all .osu files in '{osu_path}' will start.")
		Logs.info("This action may take some time depending on the amount of files to be read..\n\n")
		time.sleep(5)
	songspath = os.path.join(osu_path, 'Songs/')
	list_dir = os.listdir(songspath)
	speed = 0.
	for i, name in enumerate(list_dir):
		if os.path.isdir(os.path.join(songspath, name)):
			start = time.time()
			if display_progress:
				progress_bar(i, len(list_dir), info=os.path.join(songspath, name), suffix=f'Directories - ({speed} dir/s)')
			musicosu = MusicOsu.from_folder(os.path.join(songspath, name))
			musicosu_objects.append(musicosu)
			errors += musicosu.errors
			end = time.time()
			if (end - start) != 0:
				speed = round((1 / (end - start)+speed*i) / (i+1), ndigits=3)
	return musicosu_objects, errors


def from_beatmap(filepath: str) -> pd.DataFrame:
	"""Function to extract metadatas of a beatmap."""
	beatmap = Beatmap.from_file(filepath)
	if valid:
		return True, beatmap.to_dataframe()
	else:
		return False, beatmap.path


def from_folder(folderpath: str):
	"""A function read and extract beatmaps datas of a folder."""
	musicosu_objects, errors = musicOsu_objects(osu_path, display_progress=display_progress)
	metadata = pd.concat([musicosu.to_dataframe() for musicosu in musicosu_objects], axis=0).reset_index(drop=True)
	hitobjects_data = pd.concat([musicosu.dataframe_hitobjects() for musicosu in musicosu_objects], axis=0).reset_index(drop=True)
	return metadata, hitobjects_data, errors


def from_osu(osu_path: str, display_progress: bool = True):
	"""A function to extract beatmaps data from osu folder and return two dataframe and a list of path where there is a error."""
	musicosu_objects, errors = musicOsu_objects(osu_path, display_progress=display_progress)
	metadata = pd.concat([musicosu.to_dataframe() for musicosu in musicosu_objects], axis=0).reset_index(drop=True)
	hitobjects_data = pd.concat([musicosu.dataframe_hitobjects() for musicosu in musicosu_objects], axis=0).reset_index(drop=True)
	if display_progress and len(errors) > 0:
		Logs.warning(f'A error was found in these files: {errors}')
	return metadata, hitobjects_data, errors


def osu_to_csv(osu_path: str, csv_path:str = '', data_type: str = 'metadata', display_progress=True):
	"""Export metadata or hitobjects in a csv file."""
	metadata, hitobjects, errors = from_osu(osu_path, display_progress)
	csv_path = f'./osu_{data_type}.csv' if csv_path == '' else csv_path
	Logs.info("the csv file is being created...")
	if data_type == 'metadata':
		metadata.to_csv(csv_path, sep='$')
	elif data_type == 'hitobjects':
		hitobjects.to_csv(csv_path, sep='$')
	else:
		raise AttributeError("'data_type' must be a str and can take the values: 'metadata' or 'hitobjects'")
	if len(errors) > 0:
		Logs.warning(f'There is a error or more was found in these files: {errors}')
	else:
		Logs.success('There is not error during the export data')
	return csv_path


def osu_to_excel(osu_path: str, excel_path: str = '', display_progress=True, **kwargs):
	"""Export metadata and hitobjects in a xlsx file."""
	metadata, hitobjects, errors = from_osu(osu_path, display_progress)
	mode = 'w' if excel_path.strip() == '' else 'a'
	excel_path = './osu_data.xlsx' if excel_path == '' else excel_path
	with pd.ExcelWriter(excel_path, mode=mode) as writer:
		Logs.info("the 'metadata' sheet is being created...")
		metadata[:1048576].to_excel(writer, sheet_name='metadata', **kwargs)
		Logs.info("the 'hitobjects' sheet is being created...")
		hitobjects[:1048576].to_excel(writer, sheet_name='hitobjects', **kwargs)

	if metadata.shape[0] > 1048576:
		Logs.warning(f'The sheet "metadata" is too large ({metadata.shape[0]} lines), the maximum size has been keeping (1048576)')
	if hitobjects.shape[0] > 1048576:
		Logs.warning(f'The sheet "hitobjects" is too large ({hitobjects.shape[0]} lines), the maximum size has been keeping (1048576)')
	if len(errors) > 0:
		Logs.warning(f'There is a error or more was found in these files: {errors}')
	else:
		Logs.success('There is not error during the export data')
	return excel_path

