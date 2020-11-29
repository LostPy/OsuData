"""
Project: OsuDatas

Author: LostPy
"""

import pandas as pd

from musicOsu import MusicOsu
from beatmap import Beatmap


def global_info(file_path: str = None, dataframe: pd.DataFrame = None):
	pass


def difficulties(file_path: str = None, dataframe: pd.DataFrame = None):
	pass


def time(file_path: str = None, dataframe: pd.DataFrame = None):
	pass


def version_fmt(file_path: str = None, dataframe: pd.DataFrame = None):
	pass


def date_add(file_path: str = None, dataframe: pd.DataFrame = None):
	pass


def beatmap_error(file_path: str = None, dataframe: pd.DataFrame = None):
	pass


def play_music(folder_path: str, musicosu: MusicOsu = None):
	if musicosu is not None:
		if isinstance(musicosu, MusicOsu):
			musicosu.play_music()
		else:
			raise TypeError("'musicosu' must be an instance of 'MusicOsu'")
	else:
		if type(folder_path) is str:
			MusicOsu.from_folder(folder_path).play_music()
		else:
			raise TypeError("folder_path must be a str")


def beatmap_data(beatmap: Beatmap):
	pass


def folder_data(folerpath: str):
	pass


def osu_data(folder):
	pass

