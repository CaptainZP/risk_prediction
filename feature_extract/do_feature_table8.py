import pandas as pd
import numpy as np
import re

# add feature for table 8
datafile8 = '..\\data\\8breakfaith.csv'
df = pd.read_csv(datafile8)

# do with no time
df['BF_COUNT'] = 1
df['BF_END'] = df['SXENDDATE'].apply(lambda x: 1 if x is not np.nan else 0)
df['BF_IN'] = df['SXENDDATE'].apply(lambda x: 1 if x is np.nan else 0)
# change to time type
df['SXENDDATE'] = pd.to_datetime(df['SXENDDATE'], format='%Y/%m/%d')
df['FBDATE'] = df['FBDATE'].apply(lambda x: (re.findall(r'\d+\d*', x)))
df['FBYEAR'] = df['FBDATE'].apply(lambda x: int(x[0]))
df['FBTIME'] = df['FBDATE'].apply(lambda x: int(x[0]) + (int(x[1]) - 1) / 12)
df['ENDYEAR'] = df['SXENDDATE'].apply(lambda x: x.year)
df['SXENDTIME'] = df['SXENDDATE'].apply(lambda x: x.year + (x.month - 1)/ 12)
df['FB_HOLD_TIME'] = df['SXENDTIME'] - df['FBTIME']
df = pd.concat([df, pd.get_dummies(df['FBYEAR'], prefix='FBYEAR')], axis=1)
df_1 = df

df = df.groupby('EID', sort=False).sum()
df = df.reset_index()
df['IS_EXIST_INBF'] = df['BF_IN'].apply(lambda x: 1 if x>0 else 0)
df['IS_INDYEND'] = df['BF_IN'] - df['BF_END']
df['IS_INDYEND'] = df['IS_INDYEND'].apply(lambda x: 1 if x>0 else 0)
df['BF_END_RATE'] = df['BF_END']/df['BF_COUNT']
df['BF_IN_RATE'] = df['BF_IN']/df['BF_COUNT']
df = df.drop(['TYPECODE', 'FBYEAR', 'FBTIME', 'SXENDTIME', 'ENDYEAR'], axis=1)

first_bg_year = df_1.groupby('EID', sort=False)['FBYEAR'].min()
last_bg_year = df_1.groupby('EID', sort=False)['FBYEAR'].max()
first_bg_time = df_1.groupby('EID', sort=False)['FBTIME'].min()
last_bg_time = df_1.groupby('EID', sort=False)['FBTIME'].max()
first_end_year = df_1.groupby('EID', sort=False)['ENDYEAR'].min()
last_end_year = df_1.groupby('EID', sort=False)['ENDYEAR'].max()
first_end_time = df_1.groupby('EID', sort=False)['SXENDTIME'].min()
last_end_time = df_1.groupby('EID', sort=False)['SXENDTIME'].max()
max_hold_time = df_1.groupby('EID', sort=False)['FB_HOLD_TIME'].max()
min_hold_time = df_1.groupby('EID', sort=False)['FB_HOLD_TIME'].min()
df_1 = df_1.drop_duplicates('EID')
first_bg_year = pd.DataFrame({'EID': df_1['EID'].values, '8first_fb_year': first_bg_year.values})
last_bg_year = pd.DataFrame({'EID': df_1['EID'].values, '8last_fb_year': last_bg_year.values})
first_bg_time = pd.DataFrame({'EID': df_1['EID'].values, '8first_fb_time': first_bg_time.values})
last_bg_time = pd.DataFrame({'EID': df_1['EID'].values, '8last_fb_time': last_bg_time.values})
first_end_year = pd.DataFrame({'EID': df_1['EID'].values, '8first_end_year': first_end_year.values})
last_end_year = pd.DataFrame({'EID': df_1['EID'].values, '8last_end_year': last_end_year.values})
first_end_time = pd.DataFrame({'EID': df_1['EID'].values, '8first_end_time': first_end_time.values})
last_end_time = pd.DataFrame({'EID': df_1['EID'].values, '8last_end_time': last_end_time.values})
max_hold_time = pd.DataFrame({'EID': df_1['EID'].values, '8max_hold_time': max_hold_time})
min_hold_time = pd.DataFrame({'EID': df_1['EID'].values, '8min_hold_time': min_hold_time})
df_new = pd.merge(df, first_bg_year, on='EID', how='left')
df_new = pd.merge(df_new, last_bg_year, on='EID', how='left')
df_new = pd.merge(df_new, first_bg_time, on='EID', how='left')
df_new = pd.merge(df_new, last_bg_time, on='EID', how='left')
df_new = pd.merge(df_new, first_end_year, on='EID', how='left')
df_new = pd.merge(df_new, last_end_year, on='EID', how='left')
df_new = pd.merge(df_new, first_end_time, on='EID', how='left')
df_new = pd.merge(df_new, last_end_time, on='EID', how='left')
df_new = pd.merge(df_new, max_hold_time, on='EID', how='left')
df_new = pd.merge(df_new, min_hold_time, on='EID', how='left')

df_new['8last_minus_firstbe'] = df_new['8last_fb_time'] - df_new['8first_fb_time']
df_new['8first_minus_first'] = df_new['8first_end_time'] - df_new['8first_fb_time']
df_new['8now_minus_lastbe'] = 2015+(7/12) - df_new['8first_end_time']
df_new['8now_minus_lastend'] = 2015+(7/12) - df_new['8last_end_time']
df_new['8bf_count_avg'] = df_new['BF_COUNT'] / (df_new['8last_fb_year'] - df_new['8first_fb_year'] + 1)
df_new['8endbf_count_avg'] = df_new['BF_END'] / (df_new['8last_fb_year'] - df_new['8first_fb_year'] + 1)
df_new['8inbf_count_avg'] = df_new['BF_IN'] / (df_new['8last_fb_year'] - df_new['8first_fb_year'] + 1)

df_new.to_csv('..\\data\\8breakfaith_add.csv', index=False)
#