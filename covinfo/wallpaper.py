#!/usr/bin/env python3

from typing import Tuple, Optional, Union
import pathlib
import os
import screeninfo
from PIL import Image, ImageDraw, ImageFont

from covinfo import RESOURCES_DIR, DEFAULT_TTF_FONT


def get_screen_width_and_height() -> Tuple[int, int]:
    screen_resolutions = {(m.width, m.height) for m in screeninfo.get_monitors()}

    if len(screen_resolutions) != 1:
        raise OSError("Could not determine the screen resolution!")

    [(img_width, img_height)] = screen_resolutions

    return img_width, img_height


def make_background_img(img_width: int,
                        img_height: int,
                        bg_color: Tuple[int, int, int] = (0, 0, 0),
                        ):
    # Create image
    if None in {img_width, img_height}:
        img_width, img_height = get_screen_width_and_height()

    img = Image.new('RGB',
                    size=(img_width, img_height),
                    color=bg_color)


def make_wallpaper_with_text(text: str,
                             ttf_path: Union[pathlib.Path, str] = DEFAULT_TTF_FONT,
                             img_width: Optional[int] = None,
                             img_height: Optional[int] = None,
                             bg_color: Tuple[int, int, int] = (0, 0, 0),
                             fg_color: Tuple[int, int, int] = (255, 255, 255),
                             background_img: Union[None, pathlib.Path, str] = None,
                             ) -> Image:
    # Load the font
    if not os.path.isfile(str(ttf_path)):
        raise OSError(f"MISSING FONT FILE: {ttf_path}")
    ttf_path = pathlib.Path(ttf_path)

    # Create the base image
    if background_img and os.path.isfile(background_img):
        # Load image from path
        background_img = pathlib.Path(background_img)
        img = Image.open(str(background_img.absolute()))
        img_width, img_height = img.height, img.width
    else:
        # Create image
        if None in {img_width, img_height}:
            img_width, img_height = get_screen_width_and_height()

        img = Image.new('RGB',
                        size=(img_width, img_height),
                        color=bg_color)

    # Find the fontsize
    draw = ImageDraw.Draw(img)

    # portion of image width you want text width to be
    text_portion = 0.5
    # text_portion = 0.8

    # starting font size
    fontsize = 10
    load_font = lambda fontsize: ImageFont.truetype(str(ttf_path.absolute()), fontsize)
    font = load_font(fontsize)

    font.getsize_multiline(text)

    # get_size = lambda font, text: font.getsize(text)
    get_size = lambda font, text: font.getsize_multiline(text)

    # TODO FASTER LOOPING
    # iterate until the text size is just larger than the criteria
    while get_size(font, text)[0] < text_portion * img_width:
        fontsize += 1
        font = load_font(fontsize)

    fontsize -= 1  # optionally de-increment to be sure it is less than criteria
    font = load_font(fontsize)

    text_w, text_h = get_size(font, text)

    draw.text(xy=((img_width - text_w) / 2,
                  (img_height - text_h) / 2),
              text=text,
              fill=fg_color,
              font=font,
              )

    # img.save("wallpaper.png", "PNG")
    return img
