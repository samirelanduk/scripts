#! /usr/bin/env python3

import sys
import os
from collections import Counter
import requests
from bs4 import BeautifulSoup

if len(sys.argv) < 2:
    print("\nWhat is directory?\n")
    sys.exit()
directory = sys.argv[1]
if len(sys.argv) < 3:
    print("\nWhat is the IMDB ID?\n")
    sys.exit()
imdb_id = sys.argv[2]


# Get seasons
dirs = [d for d in os.listdir(directory) if "." not in d]
season_num = [int(d.split()[-1]) for d in dirs]
seasons = zip(dirs, season_num)
seasons = sorted(seasons, key=lambda k: k[1])

for d, num in seasons:
    files = os.listdir("{}/{}".format(directory, d))
    extensions = Counter([f.split(".")[-1] for f in files])
    extension = extensions.most_common()[0][0]
    files = [f for f in files if f.split(".")[-1] == extension]
    files = sorted(files)

    # Spoof browser
    print("https://www.imdb.com/title/{}/episodes?season={}".format(imdb_id, num))
    html = requests.get(
     "https://www.imdb.com/title/{}/episodes?season={}".format(imdb_id, num),
        headers={
            "Accept-Language": "en-US,en;q=0.5",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
        }
    ).text
    soup = BeautifulSoup(html, "html.parser")
    info = soup.find_all("div", {"class": "ipc-list-card"})
    info = [i for i in info if i.find("a") and i.find("a").text != "Sign In"]
    episode_titles = [[a for a in div.find_all("a") if a.text][0].text for div in info]
    episode_titles = [f.replace(":", "") for f in episode_titles]
    episode_titles = [e.split(" ∙ ")[1] if " ∙ " in e else e for e in episode_titles]

    for index, titles in enumerate(zip(files, episode_titles), start=1):
        os.rename(
         "{}/{}/{}".format(directory, d, titles[0]),
         "{}/{}/{} - {}.{}".format(directory, d, index, titles[1], extension)
        )
