"""
Project: OsuData

Author: LostPy
"""

from requests import ConnectionError
import pandas as pd

from .load_data import load_beatmap, beatmaps_from_http

# Class:
class Beatmap:

	"""Class to represent a beatmap with this data."""

	def __init__(self, path: str, **kwargs):
		"""Use static method `from_beatmap` to create a Beatmap objects with a .osu file."""
		self.path = path
		self.valid = False  # False if the beatmap is not initialize or if a error was found in file during the load.
		self.name = None if 'name' not in kwargs else kwargs['name']
		self.version_fmt = None if 'version_fmt' not in kwargs else kwargs['version_fmt']
		self.countdown = None if 'countdown' not in kwargs else kwargs['countdown']  # -1 when the beatmap is not load
		self.mode = 0 if 'mode' not in kwargs else kwargs['mode']
		self.creator = None if 'creator' not in kwargs else kwargs['creator']
		self.time = 0
		self.diffname = None if 'diffname' not in kwargs else kwargs['diffname']
		self.stars = 0
		self.difficulties = {'HP': None, 'CS': None, 'OD': None, 'AR': None, 'SliderMultiplier': None, 'SliderTickRate': None}
		self.count_normal = 0
		self.count_slider = 0
		self.count_spinner = 0
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

		raise TypeError("You can't compare an instance of Beatmap with another object")

	def __ne__(self, obj):
		"""Compare the difficulty."""
		if isinstance(obj, Beatmap):
			return self.stars != obj.stars

		raise TypeError("You can't compare an instance of Beatmap with another object")

	def __gt__(self, obj):
		"""Compare the difficulty."""
		if isinstance(obj, Beatmap):
			return self.stars > obj.stars

		raise TypeError("You can't compare an instance of Beatmap with another object")

	def __ge__(self, obj):
		"""Compare the difficulty."""
		if isinstance(obj, Beatmap):
			return self.stars >= obj.stars

		raise TypeError("You can't compare an instance of Beatmap with another object")

	def __lt__(self, obj):
		"""Compare the difficulty."""
		if isinstance(obj, Beatmap):
			return self.stars < obj.stars

		raise TypeError("You can't compare an instance of Beatmap with another object")

	def __le__(self, obj):
		"""Compare the difficulty."""
		if isinstance(obj, Beatmap):
			return self.stars <= obj.stars

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

	def load(self, lines: list = None, hitobjects=True, modelA=None, modelB=None):
		"""Load all data of beatmap and initialize the object."""

		with open(self.path, 'r', encoding='utf8') as beatmap:
			lines = [l for l in beatmap.read().split('\n') if l != '']
		valid, data = load_beatmap(self.path, lines=lines, modelA=modelA, modelB=modelB)

		if valid:
			self.name = data['title']
			self.version_fmt = data['version_fmt']
			self.countdown = data['countdown']
			self.mode = data['mode']
			self.creator = data['creator']
			self.difficulties['HP'] = data['hp']
			self.difficulties['CS'] = data['cs']
			self.difficulties['OD'] = data['od']
			self.difficulties['AR'] = data['ar']
			self.difficulties['SliderMultiplier'] = data['slider_multiplier']
			self.difficulties['SliderTickRate'] = data['slider_tick_rate']
			self.stars = data['stars']
			self.time = data['time']
			self.diffname = data['difficulty_name']

			if hitobjects:
				self.load_hitobjects(lines)
		self.valid = valid

	def load_hitobjects(self, lines: list = None):
		"""Load hitobjects data and set hitobects_data attribute."""
		if lines is None:
			with open(self.path, 'r', encoding='utf8') as f:
				lines = [l for l in f.read().split('\n') if l != '']
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
		'Version_fmt': self.version_fmt,
		'Countdown': self.countdown,
		'Mode': self.mode,
		'Title': self.name,
		'Creator': self.creator,
		'DifficultyName': self.diffname,
		'Stars': self.stars if self.stars > 0 else '',
		'HP': self.difficulties['HP'],
		'CS': self.difficulties['CS'],
		'OD': self.difficulties['OD'],
		'AR': self.difficulties['AR'],
		'SliderMultiplier': self.difficulties['SliderMultiplier'],
		'SliderTickRate': self.difficulties['SliderTickRate'],
		'CountNormal': self.count_normal,
		'CountSlider': self.count_slider,
		'CountSpinner': self.count_spinner,
		'Time': self.time}
		return pd.DataFrame(data=data, index=range(1), columns=data.keys())

	@staticmethod
	def from_file(filepath: str, hitobjects: bool = True, modelA=None, modelB=None):
		"""Return a Beatmap instance with all data find in filepath."""
		beatmap = Beatmap(filepath)
		beatmap.load(hitobjects=hitobjects, modelA=modelA, modelB=modelB)
		return beatmap
