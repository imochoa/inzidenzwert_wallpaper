#!/usr/bin/env python3

import os

from covinfo.covid_api import extract_muenchen_stadt_data, get_covid_df
from covinfo.wallpaper import make_wallpaper_with_text

timestamp, df = get_covid_df()
inzidenzwert, munich_series = extract_muenchen_stadt_data(df)

# Types
# str(timestamp.date()) -> 2020-10-19
# timestamp.strftime('%d/%b')  -> 19/Oct
# timestamp.strftime('%d/%-m') -> 19/10

img = make_wallpaper_with_text(text=f"{inzidenzwert}\n{timestamp.strftime('%d/%b')}")

# Set wallpaper:

# exec_always feh --bg-fill /usr/share/backgrounds/wallpaper.png

# img.save(f"wallpaper.png")
img.save("/usr/share/backgrounds/wallpaper.png")
os.system(" ".join(["feh", "--bg-fill", "/usr/share/backgrounds/wallpaper.png"]))
