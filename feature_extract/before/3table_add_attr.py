import pandas as pd

df = pd.read_csv("..\\data\\3branch_add.csv")
print(df.columns)

df['inhome_ratio'] = df['BS_BR']*1.0/df['BR_COUNT']

df['outhome_ratio'] = df['WS_BR']*1.0/df['BR_COUNT']

df['live_ratio'] = df['NORMAL_BR']*1.0/df['BR_COUNT']

df['end_ratio'] = df['END_BR']*1.0/df['BR_COUNT']

df.to_csv('..\\data\\3branch_add_new.csv', index=False)

