import pandas as pd
csv_file = 'birds.csv'
df = pd.read_csv(csv_file, index_col=0, sep=',')
df['title_de'] = 'None'
df['title_en'] = 'None'
df['desc_de'] = 'None'
df['desc_en'] = 'None'
df['country_of_origin'] = 'None'
df.to_csv(csv_file)
df.to_csv(csv_file, sep='|')