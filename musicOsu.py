"""
Project: OsuDatas

Author: LostPy
"""

import os
import pandas as pd
from scipy.io import wavfile

import pydub
from pydub.playback import play

from beatmap import Beatmap, load_beatmap


class MusicOsu:
	def __init__(self, folderpath: str, **kwargs):
		self.folderpath = folderpath
		self.music_path = None
		self.title = None
		self.artist = None
		self.time = 0
		self.beatmaps = []
		self.errors = []  # list of .osu file where a error was found.
		self.ratio_error = 0.
		self.date_add = None

	def __repr__(self):
		return self.to_dataframe().__repr__()

	def __str__(self):
		return self.__repr__()

	def __len__(self):
		return len(self.time)

	def __eq__(self, obj):
		if isinstance(obj, MusicOsu):
			return self.time == obj.time
		else:
			raise TypeError("You can't compare an instance of MusicOsu with another object")

	def __ne__(self, obj):
		if isinstance(obj, MusicOsu):
			return self.time != obj.time
		else:
			raise TypeError("You can't compare an instance of MusicOsu with another object")

	def __gt__(self, obj):
		if isinstance(obj, MusicOsu):
			return self.time > obj.time
		else:
			raise TypeError("You can't compare an instance of MusicOsu with another object")

	def __ge__(self, obj):
		if isinstance(obj, MusicOsu):
			return self.time >= obj.time
		else:
			raise TypeError("You can't compare an instance of MusicOsu with another object")

	def __lt__(self, obj):
		if isinstance(obj, MusicOsu):
			return self.time < obj.time
		else:
			raise TypeError("You can't compare an instance of MusicOsu with another object")

	def __le__(self, obj):
		if isinstance(obj, MusicOsu):
			return self.time <= obj.time
		else:
			raise TypeError("You can't compare an instance of MusicOsu with another object")

	def __getitem__(self, index):
		return self.beatmaps[index]

	def __setitem__(self, index, beatmap):
		if isinstance(beatmap, Beatmap):
			self.beatmaps.insert(index, beatmap)
		else:
			raise TypeError("The value must be an instance of Beatmap")

	def __delitem__(self, index):
		del(self.beatmaps[index])

	def __contains__(self, obj):
		return obj in self.beatmaps

	def append(self, beatmap):
		if isinstance(beatmap, Beatmap):
			self.beatmaps.append(beatmap)
		else:
			raise TypeError("The value must be an instance of Beatmap")

	def pop(self, index=-1):
		return self.beatmaps.pop(index=index)

	def metadata(self):
		return {k: v for k, v in self.__dict__().items()}

	def keys(self):
		return self.__dict__.keys()

	def values(self):
		return self.__dict__.values()

	def load(self):
		first = True
		print("avant for")
		for name in os.listdir(self.folderpath):
			path = os.path.isfile(os.path.join(self.folderpath, name))
			if path and name.endswith((".osu", )):
				if first:
					print('first beatmap found')
					with open(path, 'r') as f:
						print('yes')
						lines = f.read().split('\n')
						print(lines[:10])
						while '\n' in lines:
							print('ah')
							lines.remove('\n')
					valid, data = load_beatmap(path, lines)
					if valid:
						print('beatmap is valid')
						self.music_path = lines[...]
						self.title = data['title']
						self.artist = data['Artist']
						first = False
				beatmap = Beatmap.from_file(path)
				self.beatmaps.append(beatmap) if beatmap.valid else self.errors.append(path)

		rate, audData = self.data_music()
		self.time = audData.shape[0] / rate
		if len(self.errors) + len(self.beatmaps) > 0.:
			self.ratio_error = len(self.errors) / (len(self.errors) + len(self.beatmaps))
		else:
			self.ratio_error = 1.  # 100% error because there isn't beatmaps
		print('sortie de la fonction')

	def to_dataframe(self):
		df = pd.concat(self.beatmaps, axis=1)
		df['Artist'] = self.artist
		return df

	def dataframe_hitobjects(self):
		return pd.concat([beatmap.dataframe_hitobjects for beatmap in self.beatmaps], axis=1)
	
	def to_csv(self, path: str = None):
		return self.to_dataframe().to_csv(path, sep='$')

	def to_excel(self, path: str = None, sheet_name=''):
		sheet_name = self.title if sheet_name == '' else sheet_name
		return self.to_dataframe().to_excel(path, sheet_name=sheet_name)

	def mp3_object(self):
		return pydub.AudioSegment.from_mp3(self.music_path)

	def to_wav(self, folderpath: str):
		path = os.path.join(folderpath, self.title+'.wav')
		self.mp3_object().export(path, format="wav")
		return path

	def data_music(self):
		rate, audData = wavfile.read(self.to_wav())
		return rate, audData

	def music_to_dataframe(self):
		rate, audData = self.data_music()
		return pd.DataFrame(data=audData, columns=['L', 'R'])

	def play_music(self):
		play(self.mp3_object())

	@staticmethod
	def from_folder(folderpath):
		music_osu = MusicOsu(folderpath)
		music_osu.load()
		return music_osu

