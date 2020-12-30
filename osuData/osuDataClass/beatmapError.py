"""
Project: OsuData

Author: LostPy
"""


class BeatmapError(Exception):
	def __init__(self, message: str):
		"""A Error type with a simple error message."""
		self.message = message

	def __repr__(self):
		"""Return the error message."""
		return self.message

	def __str__(self):
		"""Return the error message."""
		return self.__repr__()
