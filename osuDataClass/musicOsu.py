"""
Project: OsuData

Author: LostPy
"""

import os
from datetime import datetime
import pandas as pd
from scipy.io import wavfile

import pydub
from pydub.playback import play

from .beatmap import Beatmap, load_beatmap


class MusicOsu:
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
		if isinstance(obj, MusicOsu):
			return len(self.beatmaps) == len(obj.beatmaps)
		else:
			raise TypeError("You can't compare an instance of MusicOsu with another object")

	def __ne__(self, obj):
		"""Compare with the number of beatmaps."""
		if isinstance(obj, MusicOsu):
			return len(self.beatmaps) != len(obj.beatmaps)
		else:
			raise TypeError("You can't compare an instance of MusicOsu with another object")

	def __gt__(self, obj):
		"""Compare with the number of beatmaps."""
		if isinstance(obj, MusicOsu):
			return len(self.beatmaps) > len(obj.beatmaps)
		else:
			raise TypeError("You can't compare an instance of MusicOsu with another object")

	def __ge__(self, obj):
		"""Compare with the number of beatmaps."""
		if isinstance(obj, MusicOsu):
			return len(self.beatmaps) >= len(obj.beatmaps)
		else:
			raise TypeError("You can't compare an instance of MusicOsu with another object")

	def __lt__(self, obj):
		"""Compare with the number of beatmaps."""
		if isinstance(obj, MusicOsu):
			return len(self.beatmaps) < len(obj.beatmaps)
		else:
			raise TypeError("You can't compare an instance of MusicOsu with another object")

	def __le__(self, obj):
		"""Compare with the number of beatmaps."""
		if isinstance(obj, MusicOsu):
			return len(self.beatmaps) <= len(obj.beatmaps)
		else:
			raise TypeError("You can't compare an instance of MusicOsu with another object")

	def __getitem__(self, index):
		"""Get beatmap with a index."""
		return self.beatmaps[index]

	def __setitem__(self, index, beatmap):
		"""Insert a beatmap in the list of beatmaps."""
		if isinstance(beatmap, Beatmap):
			self.beatmaps.insert(index, beatmap)
		else:
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
		else:
			raise TypeError("The value must be an instance of Beatmap")

	def pop(self, index=-1):
		"""Use pop method on the list of beatmaps."""
		return self.beatmaps.pop(index=index)

	def metadata(self):
		"""Export MusicOsu object in a dictionary."""
		return self.__dict__

	def keys(self):
		"""Similar to the keys method of dict objects but with all attributes of MusicOsu."""
		return self.__dict__.keys()

	def values(self):
		"""Similar to the values method of dict objects but with all attributes of MusicOsu."""
		return self.__dict__.values()

	def items(self):
		"""Similar to the items method of dict objects but with all attributes of MusicOsu."""
		return [(key, value) for key, value in self.__dict__.items()]

	def load(self, modes=[0, 1, 2, 3]):
		"""
		Initialize MusicOsu object.
		Use `modes` argument if you want get specifics modes.
		"""
		self.date_add = datetime.fromtimestamp(os.path.getctime(self.folderpath)).strftime('%Y-%m-%d %H:%M:%S')

		first = True
		for name in os.listdir(self.folderpath):
			path = os.path.join(self.folderpath, name)
			if os.path.isfile(path) and name.endswith((".osu", )):
				if first:
					with open(path, mode='r', encoding='utf8') as f:
						lines = f.read().split('\n')
						while '' in lines:
							lines.remove('')
					valid, data = load_beatmap(path, lines)
					if valid:
						self.music_path = lines[2][lines[2].find(" ")+1:]
						self.title = data['title']
						self.artist = data['Artist']
						first = False
				beatmap = Beatmap.from_file(path)
				if beatmap.valid and beatmap.mode in modes:
					self.beatmaps.append(beatmap)
				elif not beatmap.valid:
					self.errors.append(path)
		if len(self.errors) + len(self.beatmaps) > 0.:
			self.ratio_error = len(self.errors) / (len(self.errors) + len(self.beatmaps))
		else:
			self.ratio_error = 1.  # 100% error because there isn't beatmaps

	def to_dataframe(self):
		"""Export MusicOsu object in a DataFrame."""
		if len(self.beatmaps) > 0:
			df = pd.concat([beatmap.to_dataframe() for beatmap in self.beatmaps], axis=0).reset_index(drop=True)
			df['Artist'] = self.artist
			df['date_add'] = self.date_add
		else:
			df = pd.DataFrame(columns=['version_fmt', 'countdown', 'mode', 'title', 'Creator', 'DifficultyName', 'HP', 'CS', 'OD', 'AR', 'SliderMultiplier', 'SliderTickRate', 'time', 'date_add'])
		return df

	def dataframe_hitobjects(self):
		"""Return a DataFrame with hitobjects of all beatmaps from MusicOsu object."""
		if len(self.beatmaps) > 0:
			return pd.concat([beatmap.hitobjects_data for beatmap in self.beatmaps], axis=0).reset_index(drop=True)
		else:
			return pd.DataFrame(columns=['X', 'Y', 'time', 'type', 'objectParams'])

	def to_csv(self, path: str = None):
		"""Export MusicOsu object in a csv file."""
		return self.to_dataframe().to_csv(path, sep='$', index=False)

	def to_excel(self, path: str = None, sheet_name='', **kwargs):
		"""Export MusicOsu object in a xlsx file."""
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
	def from_folder(folderpath: str, modes=[0, 1, 2, 3]):
		"""
		Return a MusicOsu instance with all data find in folderpath.
		Use `modes` argument if you want get specifics modes.
		"""
		music_osu = MusicOsu(folderpath)
		music_osu.load(modes)
		return music_osu

