#!/usr/bin/env python3

import pathlib

PYPKG_DIR = pathlib.Path(__file__).parent
REPO_DIR = PYPKG_DIR / '..'
BIN_DIR = REPO_DIR / 'bin'
RESOURCES_DIR = REPO_DIR / 'resources'
FONT_DIR = RESOURCES_DIR / 'fonts'
ROBOTO_TTF = FONT_DIR / 'Roboto-Black.ttf'
CHROMEDRIVER_PATH = RESOURCES_DIR / 'chromedriver'
