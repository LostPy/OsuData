"""
Project: OsuData

Author: LostPy
"""

import pandas as pd

try:
	from plotly.offline import plot
	import plotly.express as px
	import plotly.graph_objects as go
	#from plotly.subplots import make_subplots
	plotly_imported = True
except ImportError:
	try:
		from matplotlib import pyplot as plt
		import seaborn as sns
		plotly_imported = False
		sns.set_style(style='darkgrid')
	except ImportError:
		raise ImportError("plotly module and seaborn module not found. Please, install plotly or seaborn")

try:
	from ..osuDataClass import BeatmapSet, Beatmap
except ValueError:  # When script.py is the __main__
	from osuDataClass import BeatmapSet, Beatmap


def global_info(dataframe: pd.DataFrame):
	pass


def difficulties(dataframe: pd.DataFrame):
	pass


def time(dataframe: pd.DataFrame):
	pass


def version_fmt(dataframe: pd.DataFrame):
	df_version = dataframe.groupby('version_fmt').count()
	df_version.sort_index(inplace=True)
	if plotly_imported:
		fig = go.Figure(go.Pie(labels=df_version.index, values=df_version['title']))
		fig.update_traces(hoverinfo='label+percent+value', textinfo='percent+value')
		plot(fig)
	else:
		plt.pie(df_version['title'], labels=df_version.index)
		plt.legend()
		plt.show()


def date_add(dataframe: pd.DataFrame):
	if plotly_imported:
		fig = px.histogram(dataframe, x=dataframe.index, color="mode", hover_data=dataframe.columns)
		plot(fig)
	else:
		sns.histplot(data=dataframe, x=dataframe.index, hue="mode")
		plt.legend()
		plt.show()


def beatmap_error(dataframe: pd.DataFrame):
	pass


def play_music(folder_path: str = None, beatmap_set: BeatmapSet = None):
	if beatmap_set is not None:
		if isinstance(beatmap_set, BeatmapSet):
			beatmap_set.play_music()
		else:
			raise TypeError("'beatmap_set' must be an instance of 'BeatmapSet'")
	elif folder_path is not None:
		if isinstance(folder_path, str):
			BeatmapSet.from_folder(folder_path).play_music()
		else:
			raise TypeError("folder_path must be a str")
	else:
		raise TypeError("Missing one argument: 'folder_path' or 'BeatmapSet'.")


def beatmap_data(beatmap: Beatmap):
	pass


def folder_data(folerpath: str):
	pass


def osu_data(folder):
	pass

