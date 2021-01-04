"""
Project: OsuData

Author: LostPy
"""

from os import path
from inspect import getfile
import osuData

save_model_path = path.join(path.dirname(getfile(osuData)), 'bin/save_model.bin')
print(path.dirname(getfile(osuData)))