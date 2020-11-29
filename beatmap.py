"""
Project: OsuDatas

Author: LostPy
"""

import pandas as pd

from loads import load_beatmap


class Beatmap:
	"""Class to represent a beatmap with this data."""

	def __init__(self, path: str, **kwargs):
		self.path = path
		self.valid = False  # False if the beatmap is not initialize or if a error was found in file during the load.
		self.name = None if 'name' not in kwargs else kwargs['name']
		self.version_fmt = None if 'version_fmt' not in kwargs else kwargs['version_fmt']
		self.creator = None if 'creator' not in kwargs else kwargs['creator']
		self.time = 0
		self.diffname = None if 'diffname' not in kwargs else kwargs['diffname']
		self.stars = 0
		self.difficulties = {'HP': None, 'CS': None, 'OD': None, 'AR': None}
		self.hitobjects_data = None

	def __repr__(self):
		"""Return the representation of the dataframe of metadata."""
		return self.to_dataframe().__repr__()

	def __str__(self):
		"""Return the str of the dataframe of metadata."""
		return self.__repr__()

	def __len__(self):
		"""Return the time of the beatmap."""
		return self.time

	def __eq__(self, obj):
		"""Compare the difficulty."""
		if isinstance(obj, Beatmap):
			return self.stars == obj.stars
		else:
			raise TypeError("You can't compare an instance of Beatmap with another object")

	def __ne__(self, obj):
		"""Compare the difficulty."""
		if isinstance(obj, Beatmap):
			return self.stars != obj.stars
		else:
			raise TypeError("You can't compare an instance of Beatmap with another object")

	def __gt__(self, obj):
		"""Compare the difficulty."""
		if isinstance(obj, Beatmap):
			return self.stars > obj.stars
		else:
			raise TypeError("You can't compare an instance of Beatmap with another object")

	def __ge__(self, obj):
		"""Compare the difficulty."""
		if isinstance(obj, Beatmap):
			return self.stars >= obj.stars
		else:
			raise TypeError("You can't compare an instance of Beatmap with another object")

	def __lt__(self, obj):
		"""Compare the difficulty."""
		if isinstance(obj, Beatmap):
			return self.stars < obj.stars
		else:
			raise TypeError("You can't compare an instance of Beatmap with another object")

	def __le__(self, obj):
		"""Compare the difficulty."""
		if isinstance(obj, Beatmap):
			return self.stars <= obj.stars
		else:
			raise TypeError("You can't compare an instance of Beatmap with another object")

	def metadata(self):
		"""Return a dict with metadata of beatmaps."""
		return {k: v for k, v in self.__dict__.items() if k != 'hitobjects_data'}

	def keys(self):
		"""Return the name of attributes."""
		return self.__dict__.keys()

	def values(self):
		"""Return the values of attributes."""
		return self.__dict__.values()

	def load(self, lines: list = None, hitobjects=True):
		"""Load all data of beatmap and initialize the object."""
		if lines is None:
			with open(self.path, 'r') as beatmap:
				lines = beatmap.read().split('\n')
				while '' in lines:
					lines.remove('')

		valid, datas = load_beatmap(self.path, lines=lines)
		if valid:
			self.name = datas['title']
			self.version_fmt = datas['version_fmt']
			self.creator = datas['Creator']
			self.difficulties['HP'] = datas['HP']
			self.difficulties['CS'] = datas['CS']
			self.difficulties['OD'] = datas['OD']
			self.difficulties['AR'] = datas['AR']
			self.time = datas['time']
			self.diffname = datas['DifficultyName']
			if hitobjects:
				self.load_hitobjects(lines)
		else:
			self.valid = False

	def load_hitobjects(self, lines: list = None):
		"""Load hitobjects data and set hitobects_data attribute."""
		if lines is None:
			with open(self.path, 'r') as f:
				lines = f.readlines()
				nb_columns_circle = 5 if int(lines[0][lines[0].find('v')+1:-1]) < 10 else 6
				lines = lines[lines.index('[HitObjects]\n')+1:]
		datas = {'X': [],
				'Y': [],
				'time': [],
				'type': []}

		for l in lines:
			datas_objects = l.split(',')
			datas['X'].append(int(datas_objects[0]))
			datas['Y'].append(int(datas_objects[1]))
			datas['time'].append(int(datas_objects[2]))
			if len(datas_objects) <= nb_columns_circle:
				datas['type'].append(0)
			elif '|' in datas_objects[5]:
				datas['type'].append(1)
			else:
				datas['type'].append(2)
		self.hitobjects_data = pd.DataFrame(data=datas, index=range(len(lines)), columns=datas.keys())

	def to_dataframe(self):
		"""Return a DataFrame with metadatas of a beatmap."""
		metadata = {
		'version_fmt': self.version_fmt,
		'title': self.name,
		'Creator': self.creator,
		'DifficultyName': self.diffname,
		'HP': self.difficulties['HP'],
		'CS': self.difficulties['CS'],
		'OD': self.difficulties['OD'],
		'AR': self.difficulties['AR'],
		'time': self.time}
		return pd.DataFrame(data=metadata, index=range(1), columns=metadata.keys())

	@staticmethod
	def from_file(filepath: str):
		"""Return a Beatmap instance with all data find in filepath."""
		beatmap = Beatmap(filepath)
		beatmap.load()
		return beatmap

