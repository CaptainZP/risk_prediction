import pandas as pd

df_old = pd.read_csv("..\\data\\4invest.csv")
df_last_alter_year = df_old.groupby('EID', sort=True)['BTYEAR'].max()

df = pd.read_csv("..\\data\\4invest_add.csv")

df['4live_ratio'] = df['BT_NORMAL_COUNT']*1.0/df['BTCOUNT']

df['4end_ratio'] = df['BT_END_COUNT']*1.0/df['BTCOUNT']

last_alter_year = pd.DataFrame({'EID': df['EID'].values, '4last_alter_year': df_last_alter_year.values})
df = pd.merge(df, last_alter_year, how='left', on='EID')

df.to_csv('..\\data\\4invest_add_new.csv', index=False)

