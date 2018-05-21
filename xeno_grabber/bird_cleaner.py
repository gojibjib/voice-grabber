#!/usr/bin/env python3
# bird_cleaner.py - Removes existing folders with species not part of xeno_birds.txt

import os, sys
import pandas as pd
from shutil import rmtree

# Compare xeno_birds.txt with birds_german_wiki_raw_desc.csv
xeno_birds_path = os.path.abspath("../xeno_birds.txt")
birds_csv_path = os.path.abspath("../birds_german_wiki_raw_desc.csv")

# Get all birds of xeno_birds.txt into list
with open(xeno_birds_path, "r") as rf:
    xeno_bird_list = rf.read().splitlines()

# Load csv into DataFrame
df = pd.read_csv(birds_csv_path, index_col=0, sep='|')
bird_csv_names = df['name'].values.tolist()

# Normalize names
bird_csv_names = [x.replace(" ", "_") for x in bird_csv_names[:]]

# Get intersection between two lists
btxt, bcsv = set(xeno_bird_list), set(bird_csv_names)
final_classes = btxt.intersection(bcsv)

# Remove birds from DataFrame which are not part of final_classes
kick_from_df = bcsv.difference(final_classes)
for bird in kick_from_df:
    df = df[df.name != bird.replace("_", " ")]
df.reset_index(inplace=True)
df.drop('id', 1, inplace=True)
df.index.name = 'id'

# Save to CSV
out_path = os.path.abspath("../birds_final.csv")
df.to_csv(out_path, sep='|')

# Delete other folders
files_path = os.path.abspath("../files")
for root, dirs, files in os.walk(files_path):
    bird_fs = root.split('/')[-1]
    if bird_fs not in final_classes:
        if bird_fs != "files":
            rmtree(root)    