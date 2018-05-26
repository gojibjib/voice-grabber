import pandas as pd 
import json

df = pd.read_csv("birds_final.csv", index_col=0, sep="|")

# Normalize strings
n = len(df)
for lang in ['desc_de', 'desc_en']:
    for i in range(n):
        if df[lang].iat[i].startswith('"') or df[lang].iat[i].startswith('"') or df[lang].iat[i].endswith('"') or df[lang].iat[i].endswith('"'):
            df[lang].iat[i] = df[lang].iat[i].strip('"')

        df[lang].iat[i] = df[lang].iat[i].replace('"', '\"')

        if " (Art)" in df['title_de'].iat[i]:
            df['title_de'].iat[i] = df['title_de'].iat[i].strip(" (Art)")

df.drop('country_of_origin', axis=1, inplace=True)
df.drop('voice_files', axis=1, inplace=True)

# Populate exportable dict
export = []
for i in range(n):
    tmp = {}
    tmp['id'] = i
    tmp['name'] = df['name'].iat[i]
    tmp['genus'] = df['genus'].iat[i]
    tmp['species'] = df['species'].iat[i]
    tmp['title_de'] = df['title_de'].iat[i]
    tmp['title_en'] = df['title_en'].iat[i]
    tmp['desc_de'] = df['desc_de'].iat[i]
    tmp['desc_en'] = df['desc_en'].iat[i]

    export.append(tmp)

# df.to_csv("birds_final2.csv", sep="|")
# df.to_json("birds_final.json")

with open("birds_final2.json", "w") as wf:
    json.dump(export, wf)