# CHANGELOG

## V3.20210114
Optimisation of model ! with two news stats estimated (if you don't use http requests):
 * DiffSpeed
 * DiffAim

## V2.20200104
Updated with https requests!
 * The data of beatmaps can be loaded with http requests and the [osu!api][api]. To do this, use the `api_key` argument (In function and method of load data). For more information, look the [wiki][wiki].

**Next update:** an optimisation of the model for the calculation of the value without the api.

## V1.20201229
 * Several modules are now optional

 * `osuDataClass.beatmap.Beatmap`
   * `Beatmap.stars` attribute initialize with a estimated value for versions of .osu file > 5.

 * `express.export`
   * Logs can be compacted with the argument: `compact_log`

## V1.20201222
 * The package is functional and can be install with `pip install` command (see [README.md][readme])
 * The package supports .osu files of version 5 or higher
 * The info module is not finished

[readme]: https://github.com/LostPy/OsuData/blob/main/README.md
[api]: https://github.com/ppy/osu-api/wiki
[wiki]: https://github.com/LostPy/OsuData/wiki