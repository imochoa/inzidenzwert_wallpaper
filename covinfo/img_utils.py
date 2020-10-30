#!/usr/bin/env python3

import enum
import typing as T
import pathlib
import os
import screeninfo
from PIL import Image, ImageDraw, ImageFont
from logzero import logger

from covinfo import DEFAULT_TTF_FONT


def get_screen_width_and_height() -> T.Tuple[int, int]:
    screen_resolutions = {(m.width, m.height) for m in screeninfo.get_monitors()}

    if len(screen_resolutions) != 1:
        raise OSError("Could not determine the screen resolution!")

    [(width, height)] = screen_resolutions

    return width, height


def make_background_img(width: int,
                        height: int,
                        bg_color: T.Tuple[int, int, int] = (0, 0, 0),
                        src_img: T.Optional[pathlib.Path] = None
                        ):
    if src_img and src_img.is_file():
        img = Image.open(src_img)
        # TODO
        logger.info("Correct the resolution?")
    else:
        img = Image.new('RGB',
                        size=(width, height),
                        color=bg_color,
                        )
    return img


def write_centered_text(img: Image,
                        text: str,
                        ttf_path: T.Union[pathlib.Path, str] = DEFAULT_TTF_FONT,
                        fg_color: T.Tuple[int, int, int] = (255, 255, 255),
                        ) -> Image:
    # Find the fontsize
    draw = ImageDraw.Draw(img)

    # portion of image width you want text width to be
    text_portion = 0.5
    # text_portion = 0.8

    # starting font size
    fontsize = 10
    load_font = lambda fontsize: ImageFont.truetype(str(ttf_path.absolute()), fontsize)
    get_size = lambda font, text: font.getsize_multiline(text)

    # Start looping (TODO make faster!)
    font = load_font(fontsize)
    font.getsize_multiline(text)
    # iterate until the text size is just larger than the criteria
    while get_size(font, text)[0] < text_portion * img.width:
        fontsize += 1
        font = load_font(fontsize)

    fontsize -= 1  # optionally de-increment to be sure it is less than criteria
    font = load_font(fontsize)

    text_w, text_h = get_size(font, text)
    draw.text(xy=((img.width - text_w) / 2,
                  (img.height - text_h) / 2),
              text=text,
              fill=fg_color,
              font=font,
              )
    return img


def _set_feh_wallpaper(img_path: pathlib.Path) -> None:
    os.system(" ".join(["feh",
                        "--bg-fill",
                        str(img_path)])
              )


def _set_gnome_wallpaper(img_path: pathlib.Path) -> None:
    os.system(" ".join(['gsettings',
                        'set',
                        'org.gnome.desktop.background',
                        'picture-uri',
                        f'file:///{img_path.absolute()}'])
              )


class Desktop(enum.Enum):
    i3 = 'i3'
    feh = 'feh'
    gnome = 'gnome'
    ubuntu = 'ubuntu'
    unity = 'unity'
    windows = 'unity'  # TODO?


GNOME_WALLPAPER_PATH = pathlib.Path('/usr/share/backgrounds/covid_wallpaper.png')

DEFAULT_WALLPAPER_PATH = {
    Desktop.i3:      GNOME_WALLPAPER_PATH,
    Desktop.feh:     GNOME_WALLPAPER_PATH,
    Desktop.gnome:   GNOME_WALLPAPER_PATH,
    Desktop.ubuntu:  GNOME_WALLPAPER_PATH,
    Desktop.unity:   GNOME_WALLPAPER_PATH,
    Desktop.windows: GNOME_WALLPAPER_PATH,
}


def set_wallpaper(img_path: pathlib.Path, desktop: T.Union[Desktop, str]) -> None:
    wallpaper_fcn = {
        Desktop.i3:      _set_feh_wallpaper,
        Desktop.feh:     _set_feh_wallpaper,
        Desktop.gnome:   _set_gnome_wallpaper,
        Desktop.ubuntu:  _set_gnome_wallpaper,
        Desktop.windows: _set_gnome_wallpaper,  # TODO?
    }[Desktop(desktop)]

    wallpaper_fcn(img_path)
