import pandas as pd
import json
import os
import pickle

csv_path = os.path.abspath("./meta/birds.csv")
df = pd.read_csv(csv_path, index_col=0, sep="|")

bird_id_map = {}
n = len(df)
for i in range(n):
    name = df['name'].iat[i].replace(" ", "_")
    bird_id_map[name] = i

pickle_path = os.path.abspath("./meta/bird_id_map.pickle")
with open(pickle_path, "wb") as wf:
    pickle.dump(bird_id_map, wf, protocol=2)