"""
Project: OsuDatas

Author: LostPy
"""


class BeatmapError(Exception):
	def __init__(self, message: str):
		self.message = message

	def __repr__(self):
		return self.message

	def __str__(self):
		return self.__repr__()

