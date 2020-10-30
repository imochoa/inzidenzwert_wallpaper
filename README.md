# inzidenzwert_wallpaper
See the latest COVID numbers on your wallpaper!

# Requirements
I might eventually put everything in a dockerfile, but for now...

- docker
- python >=3.6 virtual environment at `venv/`
- apt-get install -y python3-bs4

# TODO
ubuntu 
https://linuxconfig.org/set-wallpaper-on-ubuntu-20-04-using-command-line
https://askubuntu.com/questions/66914/how-to-change-desktop-background-from-command-line-in-unity

Background image instead of blank

The fonts are from google:
https://fonts.google.com/specimen/Roboto


# INI FILE CONFIG:
You can specify a configuration file by using the '--config' argument.
By default, it will take the file at `inzidenzwert_wallpaper/config.ini`

There are 9 possible keys:
 - bg_color
 - desktop
 - font_color
 - font_ttf
 - location
 - output_png
 - refresh_rate
 - resolution
 - src_img

## desktop
This defines the tool that will be called to set the wallpaper.
Possible desktop values:
 - `feh`
 - `gnome`
 - `i3`
 - `ubuntu`
 - `unity`

## src_img & bg_color
What image to use as the background. If not supplied, a plain *bg_color* background will be generated for you, where
*bg_color* is an RGB value 
(by default: (0, 0, 0))

## font_color
RGB value to use on the font
(by default: (255, 255, 255))

## font_ttf
What  *.ttf font to use for the text
(by default: `inzidenzwert_wallpaper/resources/fonts/Roboto-Black.ttf`)

## location
What location to get the data from. The possible values are listed at the end.
(by default: München Stadt)

## output_png
Where to place the wallpaper PNG. 
There are some defaults for each *desktop*:
 - `feh` -> `/usr/share/backgrounds/covid_wallpaper.png`
 - `gnome` -> `/usr/share/backgrounds/covid_wallpaper.png`
 - `i3` -> `/usr/share/backgrounds/covid_wallpaper.png`
 - `ubuntu` -> `/usr/share/backgrounds/covid_wallpaper.png`
 - `unity` -> `/usr/share/backgrounds/covid_wallpaper.png`


## refresh_rate
How often to check for new data. Some possible values would be '1h', '2h', '30m', '100s' ...

## resolution
What (width, height) should the wallpaper image be? 
By default, the script will try to auto-detect the correct values for your script


### Known locations
Possible location values:
 - Aichach-Friedberg
 - Altötting
 - Amberg Stadt
 - Amberg-Sulzbach
 - Ansbach
 - Ansbach Stadt
 - Aschaffenburg
 - Aschaffenburg Stadt
 - Augsburg
 - Augsburg Stadt
 - Bad Kissingen
 - Bad Tölz
 - Bamberg
 - Bamberg Stadt
 - Bayreuth
 - Bayreuth Stadt
 - Berchtesgadener Land
 - Cham
 - Coburg
 - Coburg Stadt
 - Dachau
 - Deggendorf
 - Dillingen a.d. Donau
 - Dingolfing-Landau
 - Donau-Ries
 - Ebersberg
 - Eichstätt
 - Erding
 - Erlangen Stadt
 - Erlangen-Höchstadt
 - Forchheim
 - Freising
 - Freyung-Grafenau
 - Fürstenfeldbruck
 - Fürth
 - Fürth Stadt
 - Garmisch-Partenkirchen
 - Gesamtergebnis
 - Günzburg
 - Haßberge
 - Hof
 - Hof Stadt
 - Ingolstadt Stadt
 - Kaufbeuren Stadt
 - Kelheim
 - Kempten Stadt
 - Kitzingen
 - Kronach
 - Kulmbach
 - Landsberg am Lech
 - Landshut
 - Landshut Stadt
 - Lichtenfels
 - Lindau (Bodensee)
 - Main-Spessart
 - Memmingen Stadt
 - Miesbach
 - Miltenberg
 - Mühldorf a.Inn
 - München
 - München Stadt
 - Neu-Ulm
 - Neuburg-Schrobenhausen
 - Neumarkt i.d.Opf.
 - Neustadt a.d. Aisch-Bad Windsheim
 - Neustadt a.d. Waldnaab
 - Nürnberg Stadt
 - Nürnberger Land
 - Oberallgäu
 - Ostallgäu
 - Passau
 - Passau Stadt
 - Pfaffenhofen a.d.Ilm
 - Regen
 - Regensburg
 - Regensburg Stadt
 - Rhön-Grabfeld
 - Rosenheim
 - Rosenheim Stadt
 - Roth
 - Rottal-Inn
 - Schwabach Stadt
 - Schwandorf
 - Schweinfurt
 - Schweinfurt Stadt
 - Starnberg
 - Straubing Stadt
 - Straubing-Bogen
 - Tirschenreuth
 - Traunstein
 - Unterallgäu
 - Weiden Stadt
 - Weilheim-Schongau
 - Weißenburg-Gunzenhausen
 - Wunsiedel i.Fichtelgebirge
 - Würzburg
 - Würzburg Stadt
