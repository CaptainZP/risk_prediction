import pandas as pd
import re
import numpy as np

datafile10 = '..\\10qualification.csv'
df = pd.read_csv(datafile10)

df['ADDCOUNT'] = 1
df['BEGINDATE'] = df['BEGINDATE'].apply(lambda x: re.findall(r"\d+\d*", str(x)))
df['EXPIRYDATE'] = df['EXPIRYDATE'].apply(lambda x: np.nan if x is np.nan else re.findall(r"\d+\d*", str(x)))
df['BEGINYEAR'] = df['BEGINDATE'].apply(lambda x: int(x[0]))
df['BEGINTIME'] = df['BEGINDATE'].apply(lambda x: int(x[0]) + (int(x[1]) - 1) / 12)
print(df.head())
df['EXPIRYYEAR'] = df['EXPIRYDATE'].apply(lambda x: int(x[0]) if x is not np.nan else np.nan)
df['EXPIRYTIME'] = df['EXPIRYDATE'].apply(lambda x: int(x[0]) + (int(x[1]) - 1) / 12 if x is not np.nan else np.nan)
df['HOLD_TIME'] = df['EXPIRYTIME'] - df['BEGINTIME']
df['EXPEND'] = df['EXPIRYTIME'].apply(lambda x: 1 if x<=(2015+7/12) else 0)
df['EXPIN'] = df['EXPIRYTIME'].apply(lambda x: 1 if x>=(2015+7/12) else 0)
df = pd.concat([df, pd.get_dummies(df['ADDTYPE'], prefix='TYPE')], axis=1)
df_1 = df
df = df.groupby('EID', sort=False).sum()
df = df.reset_index()
df = df.drop(['ADDTYPE', 'BEGINTIME', 'EXPIRYTIME', 'BEGINYEAR', 'EXPIRYYEAR'], axis=1)

max_hold_time = df_1.groupby('EID', sort=False)['HOLD_TIME'].max()
min_hold_time = df_1.groupby('EID', sort=False)['HOLD_TIME'].min()

first_law_year = df_1.groupby('EID', sort=False)['BEGINYEAR'].min()
last_law_year = df_1.groupby('EID', sort=False)['BEGINYEAR'].max()
first_law_time = df_1.groupby('EID', sort=False)['BEGINTIME'].min()
last_law_time = df_1.groupby('EID', sort=False)['BEGINTIME'].max()

first_end_year = df_1.groupby('EID', sort=False)['EXPIRYYEAR'].min()
last_end_year = df_1.groupby('EID', sort=False)['EXPIRYYEAR'].max()
first_end_time = df_1.groupby('EID', sort=False)['EXPIRYTIME'].min()
last_end_time = df_1.groupby('EID', sort=False)['EXPIRYTIME'].max()

df_1 = df_1.drop_duplicates('EID')
first_law_year = pd.DataFrame({'EID': df_1['EID'].values, '10first_be_year': first_law_year.values})
last_law_year = pd.DataFrame({'EID': df_1['EID'].values, '10last_be_year': last_law_year.values})
first_law_time = pd.DataFrame({'EID': df_1['EID'].values, '10first_be_time': first_law_time.values})
last_law_time = pd.DataFrame({'EID': df_1['EID'].values, '10last_be_time': last_law_time.values})
first_end_year = pd.DataFrame({'EID': df_1['EID'].values, '10first_end_year': first_end_year.values})
last_end_year = pd.DataFrame({'EID': df_1['EID'].values, '10last_end_year': last_end_year.values})
first_end_time = pd.DataFrame({'EID': df_1['EID'].values, '10first_end_time': first_end_time.values})
last_end_time = pd.DataFrame({'EID': df_1['EID'].values, '10last_end_time': last_end_time.values})

max_hold_time = pd.DataFrame({'EID': df_1['EID'].values, '10max_hold_time': max_hold_time})
min_hold_time = pd.DataFrame({'EID': df_1['EID'].values, '10min_hold_time': min_hold_time})
df_new = pd.merge(df, first_law_year, on='EID', how='left')
df_new = pd.merge(df_new, last_law_year, on='EID', how='left')
df_new = pd.merge(df_new, first_law_time, on='EID', how='left')
df_new = pd.merge(df_new, last_law_time, on='EID', how='left')
df_new = pd.merge(df_new, max_hold_time, on='EID', how='left')
df_new = pd.merge(df_new, min_hold_time, on='EID', how='left')
df_new = pd.merge(df_new, first_end_year, on='EID', how='left')
df_new = pd.merge(df_new, last_end_year, on='EID', how='left')
df_new = pd.merge(df_new, first_end_time, on='EID', how='left')
df_new = pd.merge(df_new, last_end_time, on='EID', how='left')
df_new['IS_EXIST_END'] = df_new['EXPEND'].apply(lambda x: 1 if x>0 else 0)
df_new['IS_EXIST_IN'] = df_new['EXPIN'].apply(lambda x: 1 if x>0 else 0)

df_new['10last_minus_firstbe'] = df_new['10last_be_time'] - df_new['10first_be_time']
df_new['10first_minus_first'] = df_new['10first_end_time'] - df_new['10first_be_time']
df_new['10now_minus_lastbe'] = 2015+(7/12) - df_new['10last_be_time']
df_new['10now_minus_lastend'] = 2015+(7/12) - df_new['10last_end_time']
df_new['10add_count_avg'] = df_new['ADDCOUNT'] / (df_new['10last_be_year'] - df_new['10first_be_year'] + 1)
df_new['10add_count_avg_in'] = df_new['EXPIN'] / (df_new['10last_be_year'] - df_new['10first_be_year'] + 1)
df_new['10add_count_avg_end'] = df_new['EXPEND'] / (df_new['10last_be_year'] - df_new['10first_be_year'] + 1)

print(df_new.head())
df_new.to_csv('..\\data\\10qualification_add.csv', index=False)