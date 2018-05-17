#!/usr/bin/env python3
# wiki_grabber.py - Gets information from birds.csv and gets the description from Wikipedia

import json, sys, os
import pandas as pd

def get_info(url):
    import requests

    r = requests.get(url)

    if r.status_code != 200:
        print('Status for {} is {}'.format(url, url.status_code))
        r.close()
        return None

    j = r.json()

    # Unpacking dict into list literal to extract page id
    page_id = [*j['query']['pages'].keys()][0]
    if page_id == '-1':
        r.close()
        return None

    return (j['query']['pages'][page_id]['title'], repr(j['query']['pages'][page_id]['extract']).strip("'"))

def get_all_info():
    protocol = 'https://'
    url = {
        'en': 'en.wikipedia.org/w/api.php?action=query&prop=extracts&format=json&redirects&explaintext=&titles=',
        'de': 'de.wikipedia.org/w/api.php?action=query&prop=extracts&format=json&redirects&explaintext=&titles='
    }

    csv_file = os.path.abspath("../birds.csv")
    df = pd.read_csv(csv_file, index_col=0, sep='|')
    n = df.shape[0]

    # Iterate over every row in the DataFrame
    for ir in df.itertuples():
        index, name = ir[0], ir[1]
        print("{}/{} - {}".format(index + 1, n, name))

        # Getting German info
        url['current'] = protocol + url['de'] + name
        info = get_info(url['current'])
        if info != None:
            df.at[index, 'title_de'] = info[0]
            df.at[index, 'desc_de'] = info[1]
        else:
            print("No German data for {}".format(name))

        # Getting English info
        url['current'] = protocol + url['en'] + name
        info = get_info(url['current'])
        if info != None:
            df.at[index, 'title_en'] = info[0]
            df.at[index, 'desc_en'] = info[1]
        else:
            print("No English data for {}".format(name))

    df.to_csv(csv_file, sep='|')

def throw_out_non_german():
    csv_file = os.path.abspath("../birds.csv")
    df = pd.read_csv(csv_file, index_col=0, sep='|')

    df.query("title_de != 'None'", True)
    df.reset_index()

    out_file = "../birds_german_wiki.csv"
    df.to_csv(out_file, sep='|')

if __name__ == "__main__":
    # Step 1, get all info
    # get_all_info()

    # Step 2, throw out all columns without a German entry
    # throw_out_non_german()



