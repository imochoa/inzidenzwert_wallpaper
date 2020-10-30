#!/usr/bin/env python3

from covinfo import (DEFAULT_CONFIG_INI,
                     DEFAULT_BG_COLOR,
                     DEFAULT_FG_COLOR,
                     DEFAULT_TTF_FONT,
                     DEFAULT_LOCATION,
                     REPO_DIR,
                     )
from covinfo.img_utils import Desktop, DEFAULT_WALLPAPER_PATH
from covinfo.covid_api import LANDKREISE

INI_KEYS = {'location',
            'resolution',
            'bg_color',
            'font_color',
            'font_ttf',
            'src_img',
            'output_png',
            'desktop',
            'refresh_rate',
            }

if __name__ == '__main__':
    bullet_sep = '\n - '
    ini_report = f"""
# INI FILE CONFIG:
You can specify a configuration file by using the '--config' argument.
By default, it will take the file at `{DEFAULT_CONFIG_INI.relative_to((REPO_DIR/'..').resolve())}`

{bullet_sep.join([f"There are {len(INI_KEYS)} possible keys:"] + sorted(INI_KEYS))}

## desktop
This defines the tool that will be called to set the wallpaper.
{bullet_sep.join(["Possible desktop values:"] + sorted([f"`{e.value}`" for e in Desktop]))}

## src_img & bg_color
What image to use as the background. If not supplied, a plain *bg_color* background will be generated for you, where
*bg_color* is an RGB value 
(by default: {DEFAULT_BG_COLOR})

## font_color
RGB value to use on the font
(by default: {DEFAULT_FG_COLOR})

## font_ttf
What  *.ttf font to use for the text
(by default: `{DEFAULT_TTF_FONT.relative_to((REPO_DIR/'..').resolve())}`)

## location
What location to get the data from. The possible values are listed at the end.
(by default: {DEFAULT_LOCATION})

## output_png
Where to place the wallpaper PNG. 
{bullet_sep.join(["There are some defaults for each *desktop*:"]
                 + sorted([f"`{k.value}` -> `{p}`" for k, p in DEFAULT_WALLPAPER_PATH.items()]))}


## refresh_rate
How often to check for new data. Some possible values would be '1h', '2h', '30m', '100s' ...

## resolution
What (width, height) should the wallpaper image be? 
By default, the script will try to auto-detect the correct values for your script


### Known locations
{bullet_sep.join(["Possible location values:"] + sorted(LANDKREISE))}

    """

    print(ini_report)
