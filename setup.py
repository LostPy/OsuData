# Project: OsuData
# Author: LostPy

from setuptools import setup, find_packages

import OsuData

__doc__ = """A small framework to work or vizualise osu! beatmaps data.
This framework use object-oriented programming (OOP) to easily manage beatmap data.
You can use `export` and `info` modules to work without object-oriented programming.
For more informations, read the README.md file."""


setup(
	name='OsuData',
	version='1.0',
	author='LostPy',
	description="A small framework to work with osu! data",
	long_description=__doc__,
	include_package_data=True,
	url='https://github.com/LostPy/OsuData',
	classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - In progress",
        "License :: MIT",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5+",
        "Topic :: osu!",
    ],
    license='MIT'
    )
