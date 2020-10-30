#!/usr/bin/env python3

import os
import sys
import pathlib
import argparse
import re
import numbers
import collections
import typing as T
import configparser
import time

from covinfo import DEFAULT_CONFIG_INI, DEFAULT_BG_COLOR, DEFAULT_FG_COLOR, DEFAULT_TTF_FONT
from covinfo.covid_api import extract_muenchen_stadt_data, get_covid_df
from covinfo.wallpaper import make_wallpaper_with_text
from covinfo import img_utils


def parse_str_of_ints(str_of_ints: str) -> T.List[int]:
    try:
        return list(map(int, str_of_ints.split(',')))
    except Exception as e:
        sys.stderr.write(f"Was not a list of ints: {str_of_ints}\n")
    return []


def rgb_checker(rgb: T.Sequence[int], default: int = 0) -> T.Tuple[int]:
    rgb_len = len(rgb)
    if rgb_len < 3:
        rgb_len += tuple(default for _ in range(rgb_len))
    return tuple(map(lambda x: max(0, min(255, int(x))), rgb))[:3]


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Make a screensaver with the latest covid numbers')

    parser.add_argument("--config",
                        type=pathlib.Path,
                        default=DEFAULT_CONFIG_INI,
                        help=f"Where to find the 'config.ini' file (default {DEFAULT_CONFIG_INI})",
                        )

    parser.add_argument("--verbose",
                        help="increase output verbosity",
                        action="store_true",
                        )

    parser.add_argument("--debug",
                        help="Testing!",
                        action="store_true",
                        )
    args = parser.parse_args()

    if args.verbose:
        print("verbosity turned on")

    if not args.config.is_file():
        raise OSError(f"The config.ini file did not exist!\n{args.config}")

    # Read the config values
    config = configparser.ConfigParser()
    config.read(args.config)
    section_name = config.sections()[0]
    desktop = img_utils.Desktop(config.get(section_name, 'desktop', fallback='ubuntu').lower())

    resolution = config.get(section_name, 'resolution', fallback='auto')
    bg_color = config.get(section_name, 'bg_color', fallback=DEFAULT_BG_COLOR)
    font_color = config.get(section_name, 'font_color', fallback=DEFAULT_FG_COLOR)
    font_ttf = config.get(section_name, 'font_ttf', fallback=DEFAULT_TTF_FONT)
    src_img = config.get(section_name, 'src_img', fallback=None)
    output_png = config.get(section_name, 'output_png', fallback=img_utils.DEFAULT_WALLPAPER_PATH[desktop])
    refresh_rate = config.get(section_name, 'refresh_rate', fallback='1h')

    # Check them
    resolution = parse_str_of_ints(resolution) if resolution and 'auto' not in resolution.lower() else None
    bg_color = rgb_checker(parse_str_of_ints(str(bg_color)))
    font_color = rgb_checker(parse_str_of_ints(str(font_color)))
    src_img = pathlib.Path(src_img) if src_img and os.path.isfile(str(src_img)) else None
    font_ttf = pathlib.Path(font_ttf) if font_ttf.strip() else DEFAULT_TTF_FONT
    font_ttf = pathlib.Path(font_ttf)

    # Output png
    # TODO permission error when using '/usr/share/backgrounds/covid_wallpaper.png'!
    output_png_str = os.path.expanduser(str(output_png))
    if (os.path.isfile(output_png_str)
            or os.path.isdir(os.path.split(output_png_str)[0])):
        output_png = pathlib.Path(output_png_str)
    else:
        raise OSError(f"Invalid *output_png*: {output_png}")

    desktop = desktop if desktop else 'ubuntu'

    # Set image parameters
    if resolution is None:
        width, height = img_utils.get_screen_width_and_height()
    else:
        width, height = resolution[:2]


    def update():

        if not args.debug:
            timestamp, df = get_covid_df()
            # TODO more location options!
            inzidenzwert, munich_series = extract_muenchen_stadt_data(df)

            # Types
            # TODO More visual options!
            text = f"{inzidenzwert}\n{timestamp.strftime('%d/%b')}"
            # str(timestamp.date()) -> 2020-10-19
            # timestamp.strftime('%d/%b')  -> 19/Oct
            # timestamp.strftime('%d/%-m') -> 19/10
        else:
            text = "testing!"
        # img = make_wallpaper_with_text(text=text)
        img = img_utils.make_background_img(width=width,
                                            height=height,
                                            bg_color=bg_color,
                                            src_img=src_img,
                                            )
        img = img_utils.write_centered_text(img=img,
                                            text=text,
                                            ttf_path=font_ttf,
                                            fg_color=font_color,
                                            )
        try:
            img.save(str(output_png))
        except PermissionError as e:
            # TODO solve this?
            raise NotImplementedError(f"Ask the user to change the permissions?\n{e}")
        img_utils.set_wallpaper(img_path=output_png, desktop=desktop)
        sys.stdout.write(f"Updated the wallpaper to:\n{text}\n")


    # Run once!
    # ---------------------------------------------------------------------------------------------------------------- #
    update()

    # Keep updating?
    # ---------------------------------------------------------------------------------------------------------------- #
    num_re = r'(\d*\s*[.,]\s*)?\d+\s*'
    pattern = r'(?:(?P<hours>' + num_re + r')h)|(?:(?P<minutes>' + num_re + r')m)|(?:(?P<seconds>' + num_re + r')s)'
    match_iter = re.finditer(pattern=pattern,
                             string=refresh_rate,
                             flags=re.IGNORECASE | re.MULTILINE,
                             )

    time_d = dict()
    for m in match_iter:
        for key in ('hours', 'minutes', 'seconds'):
            val = m.groupdict().get(key)
            if not val:
                continue
            try:
                val = float(val.replace(',', '.').replace(' ', ''))
                time_d[key] = val
            except Exception as e:
                print(f"Failed to parse: {val}")

    period = (time_d.get('hours', 0.0) * 60.0 ** 2
              + time_d.get('minutes', 0.0) * 60.0
              + time_d.get('seconds', 0.0))  # [s]

    if isinstance(period, numbers.Number) and period > 0.0:
        next_refresh = time.time() + period
        while True:
            current_time = time.time()
            if current_time <= next_refresh:
                time.sleep(max(0.9 * (next_refresh - current_time), 5.0))
            else:
                update()
                next_refresh = current_time + period
