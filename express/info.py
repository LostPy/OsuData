"""
Project: OsuData

Author: LostPy
"""

import pandas as pd
from plotly.offline import plot
import plotly.express as px
import plotly.graph_objects as go
#from plotly.subplots import make_subplots

try:
	from ..osuDataClass import MusicOsu, Beatmap
except ValueError:  # When script.py is the __main__
	from osuDataClass import MusicOsu, Beatmap

def global_info(dataframe: pd.DataFrame):
	pass


def difficulties(dataframe: pd.DataFrame):
	pass


def time(dataframe: pd.DataFrame):
	pass


def version_fmt(dataframe: pd.DataFrame):
	df_version = dataframe.groupby('version_fmt').count()
	df_version.sort_index(inplace=True)
	fig = go.Figure(go.Pie(labels=df_version.index, values=df_version['title']))
	fig.update_traces(hoverinfo='label+percent+value', textinfo='percent+value')
	plot(fig)



def date_add(dataframe: pd.DataFrame):
	fig = px.histogram(dataframe, x=dataframe.index, color="mode", hover_data=dataframe.columns)
	plot(fig)


def beatmap_error(dataframe: pd.DataFrame):
	pass


def play_music(folder_path: str = None, musicosu: MusicOsu = None):
	if musicosu is not None:
		if isinstance(musicosu, MusicOsu):
			musicosu.play_music()
		else:
			raise TypeError("'musicosu' must be an instance of 'MusicOsu'")
	elif folder_path is not None:
		if isinstance(folder_path, str):
			MusicOsu.from_folder(folder_path).play_music()
		else:
			raise TypeError("folder_path must be a str")
	else:
		raise TypeError("Missing one argument: 'folder_path' or 'MusicOsu'.")


def beatmap_data(beatmap: Beatmap):
	pass


def folder_data(folerpath: str):
	pass


def osu_data(folder):
	pass

