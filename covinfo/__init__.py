#!/usr/bin/env python3

import pathlib

# PATHS
PYPKG_DIR = pathlib.Path(__file__).parent
REPO_DIR = (PYPKG_DIR / '..').resolve()
DEFAULT_CONFIG_INI = REPO_DIR / 'config.ini'
BIN_DIR = REPO_DIR / 'bin'
RESOURCES_DIR = REPO_DIR / 'resources'
FONT_DIR = RESOURCES_DIR / 'fonts'
DEFAULT_TTF_FONT = FONT_DIR / 'Roboto-Black.ttf'
CHROMEDRIVER_PATH = RESOURCES_DIR / 'chromedriver'
DEFAULT_LOCATION = 'München Stadt'

# VISUAL DEFAULTS
DEFAULT_BG_COLOR = (0, 0, 0)
DEFAULT_FG_COLOR = (255, 255, 255)
