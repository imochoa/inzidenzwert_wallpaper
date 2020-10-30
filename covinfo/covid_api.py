#!/usr/bin/env python3

from typing import Tuple, Union
import pathlib
import subprocess
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import tempfile
import urllib.parse
from bs4 import BeautifulSoup

from covinfo import CHROMEDRIVER_PATH

COVID_URL = r'https://www.lgl.bayern.de/gesundheit/infektionsschutz/infektionskrankheiten_a_z/coronavirus/karte_coronavirus/'

LANDKREISE = {
    'Aichach-Friedberg',
    'Altötting',
    'Amberg Stadt',
    'Amberg-Sulzbach',
    'Ansbach',
    'Ansbach Stadt',
    'Aschaffenburg',
    'Aschaffenburg Stadt',
    'Augsburg',
    'Augsburg Stadt',
    'Bad Kissingen',
    'Bad Tölz',
    'Bamberg',
    'Bamberg Stadt',
    'Bayreuth',
    'Bayreuth Stadt',
    'Berchtesgadener Land',
    'Cham',
    'Coburg',
    'Coburg Stadt',
    'Dachau',
    'Deggendorf',
    'Dillingen a.d. Donau',
    'Dingolfing-Landau',
    'Donau-Ries',
    'Ebersberg',
    'Eichstätt',
    'Erding',
    'Erlangen Stadt',
    'Erlangen-Höchstadt',
    'Forchheim',
    'Freising',
    'Freyung-Grafenau',
    'Fürstenfeldbruck',
    'Fürth',
    'Fürth Stadt',
    'Garmisch-Partenkirchen',
    'Günzburg',
    'Haßberge',
    'Hof',
    'Hof Stadt',
    'Ingolstadt Stadt',
    'Kaufbeuren Stadt',
    'Kelheim',
    'Kempten Stadt',
    'Kitzingen',
    'Kronach',
    'Kulmbach',
    'Landsberg am Lech',
    'Landshut',
    'Landshut Stadt',
    'Lichtenfels',
    'Lindau (Bodensee)',
    'Main-Spessart',
    'Memmingen Stadt',
    'Miesbach',
    'Miltenberg',
    'Mühldorf a.Inn',
    'München',
    'München Stadt',
    'Neu-Ulm',
    'Neuburg-Schrobenhausen',
    'Neumarkt i.d.Opf.',
    'Neustadt a.d. Aisch-Bad Windsheim',
    'Neustadt a.d. Waldnaab',
    'Nürnberg Stadt',
    'Nürnberger Land',
    'Oberallgäu',
    'Ostallgäu',
    'Passau',
    'Passau Stadt',
    'Pfaffenhofen a.d.Ilm',
    'Regen',
    'Regensburg',
    'Regensburg Stadt',
    'Rhön-Grabfeld',
    'Rosenheim',
    'Rosenheim Stadt',
    'Roth',
    'Rottal-Inn',
    'Schwabach Stadt',
    'Schwandorf',
    'Schweinfurt',
    'Schweinfurt Stadt',
    'Starnberg',
    'Straubing Stadt',
    'Straubing-Bogen',
    'Tirschenreuth',
    'Traunstein',
    'Unterallgäu',
    'Weiden Stadt',
    'Weilheim-Schongau',
    'Weißenburg-Gunzenhausen',
    'Wunsiedel i.Fichtelgebirge',
    'Würzburg',
    'Würzburg Stadt',
    'Gesamtergebnis',
}


def get_html_docker(url: str) -> str:
    """Returns the rendered HTML at *url* as a string"""
    cmd = ['docker',
           'container',
           'run',
           '--rm',
           'zenika/alpine-chrome',
           '--no-sandbox',
           '--dump-dom',
           str(url)
           ]
    with tempfile.NamedTemporaryFile(suffix='.html') as fp:
        p = subprocess.run(cmd,
                           stdout=fp,
                           stderr=subprocess.STDOUT,
                           )
        if p.returncode != 0:
            raise OSError(f"Command failed [{p.returncode}]:\n{' '.join(cmd)}")

        with open(fp.name, 'rb') as fout:
            html_doc = fout.read().decode('utf8')

        # Clean up the cmd's previous print statements
        # html_doc = html_doc[html_doc.find('<html>'):].strip()

        if not html_doc:
            raise OSError(f"No HTML could be obtained for {url}")

        return html_doc


def get_html_selenium(url: str, chromedriver_path: pathlib.Path = CHROMEDRIVER_PATH) -> str:
    """Returns the rendered HTML at *url* as a string"""
    options = Options()
    options.headless = True
    with webdriver.Chrome(str(chromedriver_path.absolute()), options=options) as driver:
        driver.get(url)
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        # driver.save_screenshot('wtf.png')
        return driver.execute_script("return document.documentElement.outerHTML;")


def get_covid_df() -> Tuple[pd._libs.tslibs.timestamps.Timestamp, pd.DataFrame]:
    html_doc = get_html_docker(COVID_URL)
    # html = get_html_selenium(COVID_URL)

    soup = BeautifulSoup(html_doc, 'html.parser')

    html_table = soup.find('table', id='tableLandkreise')
    [df] = pd.read_html(str(html_table), thousands='.', decimal=',')

    # TIMESTAMP
    caption_str = html_table.find('caption').text.strip()
    re_iter = re.finditer(r'stand:([^,]+)', string=caption_str, flags=re.IGNORECASE)
    m = next(re_iter, None)
    if not m:
        raise ValueError("timestamp missing!")
    timestamp_str = m.group(1).strip()
    timestamp = pd.to_datetime(timestamp_str)

    return timestamp, df

    # options = Options()
    # options.headless = True
    # with webdriver.Chrome(str(CHROMEDRIVER_PATH.absolute()),
    #                       options=options) as driver:
    #     # driver = webdriver.Chrome('chromedriver')
    #     driver.get(url)
    #     time.sleep(1)
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #     time.sleep(4)
    #     # driver.save_screenshot('wtf.png')
    #     # DATAFRAME
    #     tables = driver.find_elements_by_id('tableLandkreise')
    #     if not tables:
    #         raise OSError("No tables?")
    #     elif len(tables) > 1:
    #         raise ValueError("too many tables!?")
    #     [html_table] = tables
    #     [df] = pd.read_html(html_table.get_attribute('outerHTML'), thousands='.', decimal=',')
    #
    #     # TIMESTAMP
    #     re_iter = re.finditer(r'stand:([^,]+)', string=html_table.text, flags=re.IGNORECASE)
    #     m = next(re_iter, None)
    #     if not m:
    #         raise ValueError("timestamp missing!")
    #     timestamp_str = m.group(1).strip()
    #     timestamp = pd.to_datetime(timestamp_str)
    #
    #     return timestamp, df


def extract_landkreis_data(df: pd.DataFrame, landkreis: str) -> Tuple[float, pd.Series]:
    landkreis_mask = (df.iloc[:, 0].apply(str.lower) == landkreis.lower())
    landkreis_series = df[landkreis_mask].squeeze()
    inzidenzwert = landkreis_series[5]
    return inzidenzwert, landkreis_series


def extract_muenchen_stadt_data(df: pd.DataFrame) -> Tuple[float, pd.Series]:
    return extract_landkreis_data(df=df, landkreis='München Stadt')


if __name__ == '__main__':
    timestamp, df = get_covid_df()
    inzidenzwert, munich_series = extract_muenchen_stadt_data(df)
    print(f"\n\nData from {timestamp}\nINZIDENZWERT {inzidenzwert}\n\n{munich_series.to_markdown()}")
