# OsuData

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/f48258e18c3c4a93a7f65b51206e0b88)](https://app.codacy.com/gh/LostPy/OsuData?utm_source=github.com&utm_medium=referral&utm_content=LostPy/OsuData&utm_campaign=Badge_Grade) [![CodeFactor](https://www.codefactor.io/repository/github/lostpy/osudata/badge)](https://www.codefactor.io/repository/github/lostpy/osudata)

A small framework to work or vizualise osu! beatmaps data.
This framework use object-oriented programming (OOP) to easily manage beatmap data.
You can use `export` and `info` modules to work without object-oriented programming.

## Index <a id="index"></a>
 1. [Global informations](#globalInfos)
 2. [Requirements](#requirements)
 3. [Installation](#installation)

## Global informations <a id="globalInfos"></a>
 * Author: [LostPy][me]

 * Version: 3.0
 
 * License: [MIT License][license]

 * Supported osu! file  
 This package can read the `.osu` file (beatmap) with a version format of 5 or higher.
 To check the osu file version, you can read the first line of a `.osu` file.

   **Note:** If you do not specify a [api][api] [key][api-key], the stars number of a beatmap is estimate with [sklearn][sklearn] if [sklearn][sklearn] is installed and if the beatmap file give the 'AR' stats (version of beatmap format > 7)

 * Utility link:
   * [osu! .osu file format][osu_format]
   * [osu! .db file format][osu_db_format]

 * [**Documentation**](https://github.com/LostPy/osuData/wiki)

## Requirements: <a id="requirements"></a>
### Mandatory
* [Python 3.x][py]
* [requests][req] (To execute https requests)
* [pydub][pydub] (To manipulate mp3 file and play music)
* [numpy][np] (Basis for data manipulation)
* [scipy][scipy] (To extract music data)
* [pandas][pd] (Basis for data manipulation)

### Optionnal
* [colorama][color] (For coulour logs)
* [plotly][plotly] or [seaborn][seaborn] (To visualize data)
* [scikit-learn][sklearn] (To initialize `stars` number without http requests)

## Installation <a id="installation"></a>
To install this package, you can use the following command:

`pip install git+https://github.com/LostPy/OsuData.git@main`

**Don't forget to install [dependencies](#requirements).**

**To update** the package, you can use:  
`pip install git+https://github.com/LostPy/OsuData.git@main --upgrade`

OR

`pip install git+https://github.com/LostPy/OsuData.git@main -U`


[py]: https://www.python.org/
[req]: https://requests.readthedocs.io/en/master/
[color]: https://pypi.org/project/colorama/
[pydub]: https://github.com/jiaaro/pydub
[np]: https://numpy.org/
[scipy]: https://www.scipy.org/docs.html
[pd]: https://pandas.pydata.org/
[pdDf]: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html
[pdToExcel]: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_excel.html
[plotly]: https://plotly.com/
[seaborn]: https://seaborn.pydata.org/
[sklearn]: https://sklearn.org/
[osu_format]: https://osu.ppy.sh/wiki/en/osu%21_File_Formats/Osu_%28file_format%29
[structure]: https://osu.ppy.sh/wiki/en/osu%21_File_Formats/Osu_%28file_format%29#structure
[general]: https://osu.ppy.sh/wiki/en/osu%21_File_Formats/Osu_%28file_format%29#general
[metadata]: https://osu.ppy.sh/wiki/en/osu%21_File_Formats/Osu_%28file_format%29#metadata
[difficulty]: https://osu.ppy.sh/wiki/en/osu%21_File_Formats/Osu_%28file_format%29#difficulty
[hit-objects]: https://osu.ppy.sh/wiki/en/osu%21_File_Formats/Osu_%28file_format%29#hit-objects
[osu_db_format]: https://osu.ppy.sh/wiki/en/osu%21_File_Formats/Db_%28file_format%29
[api]: https://github.com/ppy/osu-api/wiki
[api-key]: https://osu.ppy.sh/p/api/
[license]: https://github.com/LostPy/osuData/blob/main/LICENSE
[me]: https://osu.ppy.sh/users/11187592
