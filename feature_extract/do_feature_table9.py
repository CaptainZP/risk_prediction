import pandas as pd
import numpy as np
import re


datafile9 = '..\\data\\9recruit.csv'
data_9 = pd.read_csv(datafile9, low_memory=False)
data_9['count'] = 1
# data_9['PNUM'] = data_9['PNUM'].apply(lambda x: re.findall(r"\d*", str(x)))
data_9['PNUM']= data_9['PNUM'].apply(lambda x: int(x) if str(x).isdigit() else 0)
data_9['IS_WZ1'] = data_9['WZCODE'].apply(lambda x: 1 if x=='zp01' else 0)
data_9['IS_WZ2'] = data_9['WZCODE'].apply(lambda x: 1 if x=='zp02' else 0)
data_9['IS_WZ3'] = data_9['WZCODE'].apply(lambda x: 1 if x=='zp03' else 0)
data_9['WZ1_RECRNUM'] = data_9['IS_WZ1'] * data_9['PNUM']
data_9['WZ2_RECRNUM'] = data_9['IS_WZ2'] * data_9['PNUM']
data_9['WZ3_RECRNUM'] = data_9['IS_WZ3'] * data_9['PNUM']
data_9['RECREDATE'] = pd.to_datetime(data_9['RECDATE'], format='%Y/%m/%d')
data_9['RETIME'] = data_9['RECREDATE'].apply(lambda x: x.year + (x.month - 1)/12)
data_9['REYEAR'] = data_9['RECREDATE'].apply(lambda x: x.year)
data_9 = pd.concat([data_9, pd.get_dummies(data_9['REYEAR'], prefix='REYEAR')], axis=1)
print(data_9.head())
df_1 = data_9

data_9_new = data_9.groupby('EID', sort=False).sum()
data_9_new = data_9_new.reset_index()
print(data_9_new.head())
data_9_new['IS_WZ1_exist'] = data_9_new['IS_WZ1'].apply(lambda x: 1 if  x>0 else 0)
data_9_new['IS_WZ2_exist'] = data_9_new['IS_WZ2'].apply(lambda x: 1 if  x>0 else 0)
data_9_new['IS_WZ3_exist'] = data_9_new['IS_WZ3'].apply(lambda x: 1 if  x>0 else 0)
data_9_new['wz_lei_count'] = data_9_new['IS_WZ1_exist'] + data_9_new['IS_WZ2_exist'] + data_9_new['IS_WZ3_exist']
data_9_new['IS_RECR'] = data_9_new['PNUM'].apply(lambda x: 1 if x>0 else 0)
data_9_new = data_9_new.drop(['RETIME', 'REYEAR'], axis=1)

first_law_year = df_1.groupby('EID', sort=False)['REYEAR'].min()
last_law_year = df_1.groupby('EID', sort=False)['REYEAR'].max()
first_law_time = df_1.groupby('EID', sort=False)['RETIME'].min()
last_law_time = df_1.groupby('EID', sort=False)['RETIME'].max()
df_1 = df_1.drop_duplicates('EID')
first_law_year = pd.DataFrame({'EID': df_1['EID'].values, '9first_year': first_law_year.values})
last_law_year = pd.DataFrame({'EID': df_1['EID'].values, '9last_year': last_law_year.values})
first_law_time = pd.DataFrame({'EID': df_1['EID'].values, '9first_time': first_law_time.values})
last_law_time = pd.DataFrame({'EID': df_1['EID'].values, '9last_time': last_law_time.values})
df_new = pd.merge(data_9_new, first_law_year, on='EID', how='left')
df_new = pd.merge(df_new, last_law_year, on='EID', how='left')
df_new = pd.merge(df_new, first_law_time, on='EID', how='left')
df_new = pd.merge(df_new, last_law_time, on='EID', how='left')

df_new['9rec_avg_year'] = df_new['PNUM'] / np.floor(df_new['9last_year'] - df_new['9first_year'] + 1)
df_new['9last_minus_first'] = df_new['9last_time'] - df_new['9first_time']
df_new['9now_minus_last'] = 2015+(7/12) - df_new['9last_time']
df_new['9rec_avg_wz'] = df_new['PNUM'] / df_new['wz_lei_count']
df_new['half_half_rec'] = df_new['PNUM'] / df_new['count']
df_new['rec_dec'] = df_new['REYEAR_2014'] - df_new['REYEAR_2015']
df_new['rec_dec'] = df_new['rec_dec'].apply(lambda x: 1 if x>1 else 0)

print(df_new)
df_new.to_csv('..\\data\\9recruit_add.csv', index=False)
