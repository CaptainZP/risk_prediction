import pandas as pd

df = pd.read_csv("..\\data\\all_7.csv")
print(df.columns)

df['all_ZB'] = df['MPNUM'] + df['INUM'] + df['FINZB'] + df['FSTINUM'] + df['TZINUM']
df['avg_ZB'] = df['all_ZB']/5

df.to_csv('..\\data\\all_7_new.csv', index=False)

