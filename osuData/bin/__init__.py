"""
Project: OsuData

Author: LostPy
"""

from os import path
from inspect import getfile
import osuData

path_diffAim_modelA = path.join(path.dirname(getfile(osuData)), 'bin/model_DiffAim_A.bin')
path_diffAim_modelB = path.join(path.dirname(getfile(osuData)), 'bin/model_DiffAim_B.bin')
path_diffSpeed_modelA = path.join(path.dirname(getfile(osuData)), 'bin/model_DiffSpeed_A.bin')
path_diffSpeed_modelB = path.join(path.dirname(getfile(osuData)), 'bin/model_DiffSpeed_B.bin')
path_stars_modelA = path.join(path.dirname(getfile(osuData)), 'bin/model_Stars_A.bin')
path_stars_modelB = path.join(path.dirname(getfile(osuData)), 'bin/model_Stars_B.bin')
