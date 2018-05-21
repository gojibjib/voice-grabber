#!/usr/bin/env python3
# xeno_downloader.py - Downloads 50 recordings of each bird from xeno-canto.org

import requests, os, time, pickle
import pandas as pd
from bs4 import BeautifulSoup as bs

# Get birds
birds_csv = os.path.abspath("../birds_final.csv")
df = pd.read_csv(birds_csv, index_col=0, sep='|')
birds = df['name'].values.tolist()
birds_folder = [x.replace(" ", "_") for x in birds]
birds_xeno = [x.replace(" ", "-") for x in birds]

# Initialize requests
proto = "https://"
search_url = "www.xeno-canto.org/species" # + /$SPECIES
download_url = "www.xeno-canto.org" # + /$ID/download 
header_dict = {
    'User-Agent': 'Mozilla/5.0 (Nice crawler for extracting German birds and sounds. See github.com/gojibjib - Thank you)'
}

dl_dict = {}
birds_total = len(birds_xeno)
curr_bird = 1
# For every bird ..
for species in birds_xeno:
    print("{}/{} - {}".format(curr_bird, birds_total, species))
    
    # ... grab the IDs of 50 voice files
    i = 1
    n = 2
    ids = []

    while i != n + 1:
        # Open results page
        curr_url = "{}{}/{}?&view=1&pg={}".format(proto, search_url, species, i)
        r = requests.get(curr_url, headers=header_dict)
        if r.status_code != 200:
            print("Got status code {} on {}".format(r.status_code, curr_url))
            continue

        # Get & parse HTML
        html = r.content
        soup = bs(html, "lxml")
        for x in soup.find("table", class_="results").find_all("td", attrs={"style": "white-space: nowrap;"}):
            ids.append(x.find("a")['href'])

        i += 1
        time.sleep(1)

    dl_dict[species] = ids
    curr_bird += 1

