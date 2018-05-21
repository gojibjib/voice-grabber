fin#!/usr/bin/env python3
# xeno_crawler.py - Crawling xeno-canto.org to get German bird recordings

from bs4 import BeautifulSoup as bs
import requests, sys, time, os

proto = "https://"
url = "www.xeno-canto.org/explore?query=+cnt%3A%22Germany%22&view=1&pg="

# 474 search pages
i = 1
n = 474

page_birds = []
total_set = set()

# We're nice
header_dict = {
    'User-Agent': 'Mozilla/5.0 (Nice crawler for extracting German birds and sounds. See github.com/gojibjib - Thank you)'
}

while i != n + 1:
    print("Parsing page {} ...".format(i))
    # Getting HTML
    curr_url = proto + url + str(i)
    r = requests.get(curr_url, headers=header_dict)
    if r.status_code != 200:
        print("Got status code {} on {}".format(r.status_code, url + i))
        continue
        
    html = r.content

    # Parsing it
    soup = bs(html, "lxml")
    for tag in soup.find_all("span", class_="scientific-name"):
        page_birds.append(tag.string)

    total_set.update(page_birds)
    time.sleep(1)
    i += 1

# Saving output
out_path = os.path.abspath("../xeno_birds.txt")
with open(out_path, "w") as wf:
    for item in total_set:
        wf.write("{}\n".format(item.replace(' ', '_')))

