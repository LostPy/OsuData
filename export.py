"""
Project: OsuDatas

Author: LostPy
"""

import os
import time

import pandas as pd
import pydub

from logs import Logs
from osuProgressBar import progress_bar
import musicOsu
from beatmapError import BeatmapError


def to_csv(folderpath: str, csv_path: str = ''):
	musicosu = musicOsu.MusicOsu.from_folder(folderpath)
	if musicosu.ratio_error < 1.:
		csv_path = f'./{musicosu.title}.csv' if csv_path == '' else csv_path
		musicosu.to_csv(csv_path)
		return csv_path
	else:
		raise BeatmapError(f"There isn't beatmap in the folder: '{folderpath}', or one error was found in all beatmaps")


def to_excel(folderpath: str, excel_path: str = '', *args, **kwargs):
	musicosu = musicOsu.MusicOsu.from_folder(folderpath)
	if musicosu.ratio_error < 1.:
		metadatas = musicosu.to_dataframe()
		music_data = musicosu.music_to_dataframe()
		hitobjects = musicosu.dataframe_hitobjects()
		excel_path = f'./{musicosu.title}.xlsx' if excel_path == '' else excel_path
		with pd.ExcelWriter(excel_path, 'a') as writer:
			for df, name in zip([metadatas, music_data, hitobjects], ['metadatas', 'music data', 'hitobjects']):
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
	This function extract osu! beatmaps data and return the list of MusicOsu object
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
			musicosu = musicOsu.from_folder(os.path.join(songspath, name))
			musicosu_objects.append(musicosu)
			errors += musicosu.errors
			end = time.time()
			speed = round(1 / (end - start), ndigits=3) if end - start != 0. else speed
	return musicosu_objects, errors


def osu_to_dataframe(osu_path: str, display_progress: bool = True):
	"""A function to extract beatmaps data from osu folder and return a dataframe."""
	musicosu_objects, errors = musicOsu_objects(osu_path, display_progress=display_progress)
	metadata = pd.concat([musicosu.to_dataframe() for musicosu in musicosu_objects], axis=1)
	hitobjects_data = pd.concat([musicosu.dataframe_hitobjects() for musicosu in musicosu_objects], axis=1)
	if display_progress and len(errors) > 0:
		Logs.warning(f'A error was found in these files: {errors}')
	return metadata, hitobjects_data


def osu_to_csv(osu_path: str, csv_path:str = '', data_type: str = 'metadata', display_progress=True):
	"""Export metadata or hitobjects in a csv file."""
	metadata, hitobjects = osu_to_dataframe(osu_path, display_progress)
	csv_path = f'./osu_{data_type}.csv' if csv_path == '' else csv_path
	if data_type == 'metadata':
		metadata.to_csv(csv_path, sep='$')
	elif data_type == 'hitobjects':
		hitobjects.to_csv(csv_path, sep='$')
	else:
		raise AttributeError("'data_type' must be a str and can take the values: 'metadata' or 'hitobjects'")
	return csv_path


def osu_to_excel(osu_path: str, excel_path: str = '', display_progress=True, **kwargs):
	"""Export metadata and hitobjects in a xlsx file."""
	metadata, hitobjects = osu_to_dataframe(osu_path, display_progress)
	excel_path = './osu_data.xlsx' if excel_path == '' else excel_path
	with pd.ExcelWriter(excel_path, 'a') as writer:
		metadata.to_excel(writer, sheet_name='metadata', **kwargs)
		hitobjects.to_excel(writer, sheet_name='hitobjects', **kwargs)
	return excel_path

