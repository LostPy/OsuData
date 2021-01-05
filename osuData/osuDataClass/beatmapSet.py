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

from .beatmap import Beatmap
from .load_data import load_beatmap, beatmaps_from_http


class BeatmapSet:
	def __init__(self, folderpath: str, id_: int = None):
		self.folderpath = folderpath
		self.id = id_
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

	def load_from_files(self, mode: int = None, hitobjects=True, model=None):
		"""
		Initialize BeatmapSet object from files of beatmaps.
		Use `modes` argument if you want get specifics modes.
		"""
		self.date_add = datetime.fromtimestamp(os.path.getctime(self.folderpath)).strftime('%Y-%m-%d %H:%M:%S')
		try:
			self.id = int(os.path.basename(self.folderpath).split(' ')[0])
		except ValueError as e:
			pass

		first = True
		for name in os.listdir(self.folderpath):
			path = os.path.join(self.folderpath, name)
			if os.path.isfile(path) and name.endswith((".osu", )):
				with open(path, mode='r', encoding='utf8') as f:
					lines = [l for l in f.read().split('\n') if l != '']

				if first:
					valid, data = load_beatmap(path, lines)
					if valid:
						self.music_path = lines[2][lines[2].find(" ")+1:]
						self.title = data['title']
						self.artist = data['artist']
						first = False

				beatmap = Beatmap(path)
				beatmap.load(lines=lines, hitobjects=hitobjects)
				if beatmap.valid and (mode is None or beatmap.mode == mode):
					self.beatmaps.append(beatmap)
				elif not beatmap.valid:
					self.errors.append(path)

		if len(self.errors) + len(self.beatmaps) > 0.:
			self.ratio_error = len(self.errors) / (len(self.errors) + len(self.beatmaps))
		else:
			self.ratio_error = 1.  # 100% error because there isn't beatmaps

	def load_from_http(self, api_key: str, mode: int = None, hitobjects: bool = True):
		"""
		Initialize BeatmapSet object from https (with osu!api).
		Use `mode` argument if you want get a specifics mode.
		"""
		try:
			self.id = int(os.path.basename(self.folderpath).split(' ')[0])
		except ValueError as e:
			self.ratio_error = 1.
			raise ValueError("this beatmaps set is probably not published, impossible to find it by https queries.")
		
		self.date_add = datetime.fromtimestamp(os.path.getctime(self.folderpath)).strftime('%Y-%m-%d %H:%M:%S')
		beatmaps = beatmaps_from_http(api_key, beatmapset_id=self.id, mode=mode)
		try:
			self.title = beatmaps['title'][0]
			self.artist = beatmaps['artist'][0]
			for i in beatmaps.index:
				line = beatmaps.iloc[i]
				path = os.path.join(self.folderpath, f"{line['artist']} - {line['title']} ({line['creator']}) [{line['version']}].osu")
				beatmap = Beatmap(path)
				beatmap.valid = True
				beatmap.name = line['title']
				beatmap.mode = int(line['mode'])
				beatmap.creator = line['creator']
				beatmap.diffname = line['version']
				beatmap.time = int(line['hit_length']) * 1000
				beatmap.stars = float(line['difficultyrating'])
				beatmap.difficulties = {'HP': line['diff_drain'], 'CS': line['diff_size'],
				'OD': line['diff_overall'], 'AR': line['diff_approach'],
				'SliderMultiplier': line['diff_speed'], 'SliderTickRate': line['diff_aim']}
				beatmap.count_normal = line['count_normal']
				beatmap.count_slider = line['count_slider']
				beatmap.count_spinner = line['count_spinner']
				if hitobjects:
					beatmap.load_hitobjects()
				self.beatmaps.append(beatmap)
		except KeyError:
			self.ratio_error = 1.
			self.errors.append(self.folderpath)

	def load(self, api_key: str = None, **kwargs):
		"""
		Initialize BeatmapSet object from https (with osu!api) or files of beatmaps.
		Use keywords arguments of method `load_from_files` or `load_from_http`.

		If api_key is None, load BeatmapSet from files, else load BeatmapSet from http
		"""
		if api_key is None:
			self.load_from_files(**kwargs)
		else:
			if 'model' in kwargs:
				del(kwargs['model'])
			self.load_from_http(api_key=api_key, **kwargs)

	def to_dataframe(self):
		"""Export BeatmapSet object in a DataFrame."""
		if len(self.beatmaps) > 0:
			df = pd.concat([beatmap.to_dataframe() for beatmap in self.beatmaps], axis=0).reset_index(drop=True)
			df['Artist'] = self.artist
			df['Date_Add'] = self.date_add
			df[df['Countdown'] == -1]['Countdown'] = ''
		else:
			df = pd.DataFrame(columns=['Version_fmt', 'Countdown', 'Mode', 'Title',
				'Creator', 'DifficultyName', 'Stars', 'HP', 'CS', 'OD', 'AR', 'SliderMultiplier',
				'SliderTickRate', 'CountNormal', 'CountSlider', 'CountSpinner', 'Time', 'Date_Add'])
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
	def from_folder(folderpath: str, api_key: str = None, mode=None, hitobjects: bool = True, model=None):
		"""
		Return a BeatmapSet instance with all data find in folderpath.
		If `modes` contain several osu! modes (2 or more) and than `api_key` is not None, all beatmaps are export.
		"""
		beatmap_set = BeatmapSet(folderpath)
		beatmap_set.load(api_key=api_key, mode=mode, hitobjects=hitobjects, model=model)
		return beatmap_set
