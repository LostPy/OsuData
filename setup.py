# Project: OsuData
# Author: LostPy

from setuptools import setup, find_packages

import osuData

__doc__ = """A small framework to work or vizualise osu! beatmaps data.
This framework use object-oriented programming (OOP) to easily manage beatmap data.
You can use `export` and `info` modules to work without object-oriented programming.
For more informations, read the README.md file."""


setup(
	name='osuData',
	version='2.20200110',
	author='LostPy',
	description="A small framework to work with osu! data",
	long_description=__doc__,
    package_dir = {'osuData': './osuData'},
    package_data = {'': ['LICENSE.txt'], 'osuData': ['bin/*.bin']},
	include_package_data=True,
	url='https://github.com/LostPy/OsuData',
	classifiers=[
        "Programming Language :: Python",
        "Development Status :: Functionnal - improvement in progress",
        "License :: MIT",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5+",
        "Topic :: osu!",
    ],
    license='MIT',
    packages = find_packages()
    )
