"""
Project: OsuData

Author: LostPy
"""

import os
from datetime import datetime
import pickle
import pandas as pd
from scipy.io import wavfile
try:
	from sklearn import svm
	sklearn_imported = True
except ImportError:
	sklearn_imported = False

import pydub
from pydub.playback import play

from .beatmap import Beatmap, load_beatmap
try:
	from ..bin import save_model_path
except ValueError:  # when the __main__ is script.py
	from bin import save_model_path


class BeatmapSet:
	def __init__(self, folderpath: str, **kwargs):
		self.folderpath = folderpath
		self.music_path = None
		self.title = None
		self.artist = None
		self.beatmaps = []
		self.errors = []  # list of .osu file where a error was found.
		self.ratio_error = 0.
		self.date_add = None

	def __repr__(self):
		"""Return the representation of the dataframe of metadata."""
		return self.to_dataframe().__repr__()

	def __str__(self):
		"""Return the str of the dataframe of metadata."""
		return self.__repr__()

	def __len__(self):
		"""Number of beatmaps."""
		return len(self.beatmaps)

	def __eq__(self, obj):
		"""Compare with the number of beatmaps."""
		if isinstance(obj, BeatmapSet):
			return len(self.beatmaps) == len(obj.beatmaps)

		raise TypeError("You can't compare an instance of BeatmapSet with another object")

	def __ne__(self, obj):
		"""Compare with the number of beatmaps."""
		if isinstance(obj, BeatmapSet):
			return len(self.beatmaps) != len(obj.beatmaps)

		raise TypeError("You can't compare an instance of BeatmapSet with another object")

	def __gt__(self, obj):
		"""Compare with the number of beatmaps."""
		if isinstance(obj, BeatmapSet):
			return len(self.beatmaps) > len(obj.beatmaps)

		raise TypeError("You can't compare an instance of BeatmapSet with another object")

	def __ge__(self, obj):
		"""Compare with the number of beatmaps."""
		if isinstance(obj, BeatmapSet):
			return len(self.beatmaps) >= len(obj.beatmaps)

		raise TypeError("You can't compare an instance of BeatmapSet with another object")

	def __lt__(self, obj):
		"""Compare with the number of beatmaps."""
		if isinstance(obj, BeatmapSet):
			return len(self.beatmaps) < len(obj.beatmaps)

		raise TypeError("You can't compare an instance of BeatmapSet with another object")

	def __le__(self, obj):
		"""Compare with the number of beatmaps."""
		if isinstance(obj, BeatmapSet):
			return len(self.beatmaps) <= len(obj.beatmaps)

		raise TypeError("You can't compare an instance of BeatmapSet with another object")

	def __getitem__(self, index):
		"""Get beatmap with a index."""
		return self.beatmaps[index]

	def __setitem__(self, index, beatmap):
		"""Insert a beatmap in the list of beatmaps."""
		if isinstance(beatmap, Beatmap):
			self.beatmaps.insert(index, beatmap)

		raise TypeError("The value must be an instance of Beatmap")

	def __delitem__(self, index):
		"""Delete the beatmap with the index."""
		del(self.beatmaps[index])

	def __contains__(self, obj):
		"""Return True if obj in the list of beatmaps."""
		return obj in self.beatmaps

	def append(self, beatmap):
		"""Append beatmap in the list of beatmaps."""
		if isinstance(beatmap, Beatmap):
			self.beatmaps.append(beatmap)

		raise TypeError("The value must be an instance of Beatmap")

	def pop(self, index=-1):
		"""Use pop method on the list of beatmaps."""
		return self.beatmaps.pop(index=index)

	def metadata(self):
		"""Export BeatmapSet object in a dictionary."""
		return self.__dict__

	def keys(self):
		"""Similar to the keys method of dict objects but with all attributes of BeatmapSet."""
		return self.__dict__.keys()

	def values(self):
		"""Similar to the values method of dict objects but with all attributes of BeatmapSet."""
		return self.__dict__.values()

	def items(self):
		"""Similar to the items method of dict objects but with all attributes of BeatmapSet."""
		return [(key, value) for key, value in self.__dict__.items()]

	def load(self, modes=[0, 1, 2, 3], count_hitobjects: bool = True, hitobjects=True, model=None):
		"""
		Initialize BeatmapSet object.
		Use `modes` argument if you want get specifics modes.
		"""
		self.date_add = datetime.fromtimestamp(os.path.getctime(self.folderpath)).strftime('%Y-%m-%d %H:%M:%S')
		
		if model is None and sklearn_imported:
			with open(save_model_path, 'rb') as save:
				model = pickle.load(save)
		elif model is not None and not sklearn_imported:
			model = None

		first = True
		for name in os.listdir(self.folderpath):
			path = os.path.join(self.folderpath, name)
			if os.path.isfile(path) and name.endswith((".osu", )):
				with open(path, mode='r', encoding='utf8') as f:
					lines = [l for l in f.read().split('\n') if l != '']

				if first:
					valid, data = load_beatmap(path, lines, count_hitobjects=False, model)
					if valid:
						self.music_path = lines[2][lines[2].find(" ")+1:]
						self.title = data['title']
						self.artist = data['artist']
						first = False

				beatmap = Beatmap(path)
				beatmap.load(lines=lines, count_hitobjects=count_hitobjects, hitobjects=hitobjects, model=model)
				if beatmap.valid and beatmap.mode in modes:
					self.beatmaps.append(beatmap)
				elif not beatmap.valid:
					self.errors.append(path)

		if len(self.errors) + len(self.beatmaps) > 0.:
			self.ratio_error = len(self.errors) / (len(self.errors) + len(self.beatmaps))
		else:
			self.ratio_error = 1.  # 100% error because there isn't beatmaps

	def to_dataframe(self):
		"""Export BeatmapSet object in a DataFrame."""
		if len(self.beatmaps) > 0:
			df = pd.concat([beatmap.to_dataframe() for beatmap in self.beatmaps], axis=0).reset_index(drop=True)
			df['Artist'] = self.artist
			df['date_add'] = self.date_add
		else:
			df = pd.DataFrame(columns=['version_fmt', 'countdown', 'mode', 'title', 'Creator', 'DifficultyName', 'Stars', 'HP', 'CS', 'OD', 'AR', 'SliderMultiplier', 'SliderTickRate', 'time', 'date_add'])
		return df

	def dataframe_hitobjects(self):
		"""Return a DataFrame with hitobjects of all beatmaps from BeatmapSet object."""
		if len(self.beatmaps) > 0:
			return pd.concat([beatmap.hitobjects_data for beatmap in self.beatmaps], axis=0).reset_index(drop=True)

		return pd.DataFrame(columns=['X', 'Y', 'time', 'type', 'objectParams'])

	def to_csv(self, path: str = None):
		"""Export BeatmapSet object in a csv file."""
		return self.to_dataframe().to_csv(path, sep='$', index=False)

	def to_excel(self, path: str = None, sheet_name='', **kwargs):
		"""Export BeatmapSet object in a xlsx file."""
		sheet_name = self.title if sheet_name == '' else sheet_name
		return self.to_dataframe().to_excel(path, sheet_name=sheet_name, index=False, **kwargs)

	def mp3_object(self):
		"""Return a mp3 object (module pydub)."""
		return pydub.AudioSegment.from_mp3(os.path.join(self.folderpath, self.music_path))

	def to_wav(self, name='audio_wav'):
		"""Export the mp3 file in a wav file."""
		path = os.path.join(self.folderpath, name+'.wav')
		self.mp3_object().export(path, format="wav")
		return path

	def data_music(self):
		"""Extract audio data of the mp3 file."""
		path = self.to_wav()
		rate, audData = wavfile.read(path)
		os.remove(path)
		return rate, audData

	def music_to_dataframe(self):
		"""Return a DataFrame with audio data of the music."""
		rate, audData = self.data_music()
		return pd.DataFrame(data=audData, columns=['L', 'R'])

	def play_music(self):
		"""Play the music. Note: This isn't a async method."""
		play(self.mp3_object())

	@staticmethod
	def from_folder(folderpath: str, modes=[0, 1, 2, 3], count_hitobjects: bool = True, hitobjects: bool = True, model=None):
		"""
		Return a BeatmapSet instance with all data find in folderpath.
		Use `modes` argument if you want get specifics modes.
		"""
		beatmap_set = BeatmapSet(folderpath)
		beatmap_set.load(modes, count_hitobjects=count_hitobjects, hitobjects=hitobjects, model=model)
		return beatmap_set
