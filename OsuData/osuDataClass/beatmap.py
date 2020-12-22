"""
Project: OsuData

Author: LostPy
"""

import pandas as pd


def load_beatmap(filepath: str, lines: list = None) -> dict:
	"""
	A function to extract beatmap datas.
	return a list with the datas of the beatmap : [version_fmt, Title, Artist, Creator, DifficultyName, HP, CS, OD, HR, time]
	"""
	try:
		if lines is None:
			with open(filepath, 'r', encoding='utf-8') as beatmap:
				lines = beatmap.read().split('\n')
				while '' in lines:
					lines.remove('')
		if '[Editor]' in lines:
			general = lines[lines.index('[General]')+1:lines.index('[Editor]')]
		else:
			general = lines[lines.index('[General]')+1:lines.index('[Metadata]')]
		metadatas = lines[lines.index('[Metadata]')+1:lines.index('[Difficulty]')]
		difficulties = lines[lines.index('[Difficulty]')+1:lines.index('[Events]')]
		time = lines[-1].split(',')[2]
		version_fmt = int(lines[0][lines[0].find("v")+1:])
		if version_fmt <= 5 and len(general) < 7:
			mode = 0
		elif version_fmt <= 5:
			mode = int(general[6][-1]) if general[6][:4].lower() == 'mode' else 0
		else:
			mode = int(general[6][-1])

		data = {
		'version_fmt': version_fmt,
		'countdown': int(general[3][-1]),
		'mode': mode,
		'title': metadatas[0][6:],
		'Artist': metadatas[1][7:] if version_fmt < 10 else metadatas[2][7:],
		'Creator': metadatas[2][8:] if version_fmt < 10 else metadatas[4][8:],
		'DifficultyName': metadatas[3][8:] if version_fmt < 10 else metadatas[5][8:],
		'HP': difficulties[0][12:],
		'CS': difficulties[1][11:],
		'OD': difficulties[2][18:],
		'AR': difficulties[3][13:] if version_fmt > 7 else '',
		'SliderMultiplier': difficulties[3][17:] if version_fmt <= 7 else difficulties[4][17:],
		'SliderTickRate': difficulties[4][15:] if version_fmt <= 7 else difficulties[5][15:],
		'time': int(time)}

		return True, data
	except IndexError:
		return False, [filepath]


# Class:
class Beatmap:

	"""Class to represent a beatmap with this data."""

	def __init__(self, path: str, **kwargs):
		"""Use static method `from_beatmap` to create a Beatmap objects with a .osu file."""
		self.path = path
		self.valid = False  # False if the beatmap is not initialize or if a error was found in file during the load.
		self.name = None if 'name' not in kwargs else kwargs['name']
		self.version_fmt = None if 'version_fmt' not in kwargs else kwargs['version_fmt']
		self.countdown = 1 if 'countdown' not in kwargs else kwargs['countdown']
		self.mode = 0 if 'mode' not in kwargs else kwargs['mode']
		self.creator = None if 'creator' not in kwargs else kwargs['creator']
		self.time = 0
		self.diffname = None if 'diffname' not in kwargs else kwargs['diffname']
		self.stars = 0
		self.difficulties = {'HP': None, 'CS': None, 'OD': None, 'AR': None, 'SliderMultiplier': None, 'SliderTickRate': None}
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

	def items(self):
		"""Return a list of tuple (name_attribute, value_attribute) of Beatmap object."""
		return self.__dict__.items()

	def load(self, lines: list = None, hitobjects=True):
		"""Load all data of beatmap and initialize the object."""
		if lines is None:
			with open(self.path, 'r', encoding='utf8') as beatmap:
				lines = beatmap.read().split('\n')
				while '' in lines:
					lines.remove('')

		valid, data = load_beatmap(self.path, lines=lines)
		if valid:
			self.name = data['title']
			self.version_fmt = data['version_fmt']
			self.countdown = data['countdown']
			self.mode = data['mode']
			self.creator = data['Creator']
			self.difficulties['HP'] = data['HP']
			self.difficulties['CS'] = data['CS']
			self.difficulties['OD'] = data['OD']
			self.difficulties['AR'] = data['AR']
			self.difficulties['SliderMultiplier'] = data['SliderMultiplier']
			self.difficulties['SliderTickRate'] = data['SliderTickRate']
			self.time = data['time']
			self.diffname = data['DifficultyName']
			if hitobjects:
				self.load_hitobjects(lines)
		self.valid = valid

	def load_hitobjects(self, lines: list = None):
		"""Load hitobjects data and set hitobects_data attribute."""
		if lines is None:
			with open(self.path, 'r', encoding='utf8') as f:
				lines = f.read().split('\n')
		version_fmt = int(lines[0][lines[0].find('v')+1:])
		lines = lines[lines.index('[HitObjects]')+1:]
		data = {'X': [],
				'Y': [],
				'time': [],
				'type': [],
				'objectParams': []}

		for l in lines:
			data_objects = l.split(',')
			data['X'].append(int(data_objects[0]))
			data['Y'].append(int(data_objects[1]))
			data['time'].append(int(data_objects[2]))
			data['type'].append(int(data_objects[3]))
			params = ''
			if version_fmt < 10 and len(data_objects) > 5:
				for param in data_objects[5:]:
					params += param + ','
			elif len(data_objects) > 5:
				for param in data_objects[5:-1]:
					params += param + ','
			params = params[:-1] if len(params) > 0 else params
			data['objectParams'].append(params)
		self.hitobjects_data = pd.DataFrame(data=data, index=range(len(lines)), columns=data.keys())

	def to_dataframe(self):
		"""Return a DataFrame with metadatas of a beatmap."""
		data = {
		'version_fmt': self.version_fmt,
		'countdown': self.countdown,
		'mode': self.mode,
		'title': self.name,
		'Creator': self.creator,
		'DifficultyName': self.diffname,
		'HP': self.difficulties['HP'],
		'CS': self.difficulties['CS'],
		'OD': self.difficulties['OD'],
		'AR': self.difficulties['AR'],
		'SliderMultiplier': self.difficulties['SliderMultiplier'],
		'SliderTickRate': self.difficulties['SliderTickRate'],
		'time': self.time}
		return pd.DataFrame(data=data, index=range(1), columns=data.keys())

	@staticmethod
	def from_file(filepath: str):
		"""Return a Beatmap instance with all data find in filepath."""
		beatmap = Beatmap(filepath)
		beatmap.load()
		return beatmap

