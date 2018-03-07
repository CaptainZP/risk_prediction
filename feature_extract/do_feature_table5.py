import pandas as pd
import numpy as np

datafile5 = '..\\data\\5right.csv'
data_5 = pd.read_csv(datafile5)

data_5['5RIGHT_COUNT'] = 1
data_5['5ASKDATE'] = pd.to_datetime(data_5['ASKDATE'], format='%Y/%m/%d')
data_5['5FBDATE'] = pd.to_datetime(data_5['FBDATE'], format='%Y/%m/%d')
data_5['5ASKYEAR'] = data_5['5ASKDATE'].apply(lambda x: x.year)
data_5['5FBYEAR'] = data_5['5FBDATE'].apply(lambda x: x.year)
data_5['5ASKTIME'] = data_5['5ASKDATE'].apply(lambda x: x.year + (x.month - 1)/12)
data_5['5FBTIME'] = data_5['5FBDATE'].apply(lambda x: x.year + (x.month - 1)/12)
data_5['5hold_time'] = data_5['5FBTIME'] - data_5['5ASKTIME']

data_5['5FUYU_RIGHT'] = data_5['5FBYEAR'].apply(lambda x: 1 if x>0 else 0)
data_5['5WFUYU_RIGHT'] = data_5['5FBYEAR'].apply(lambda x: 0 if x>0 else 1)
data_5 = pd.concat([data_5, pd.get_dummies(data_5['RIGHTTYPE'], prefix='RIGHT')], axis=1)
print(data_5.head(10))
df_1 = data_5

data_5_new = data_5.groupby('EID', sort=False).sum()
data_5_new = data_5_new.reset_index()
data_5_new['5IS_EXIST_WFU'] = data_5_new['5WFUYU_RIGHT'].apply(lambda x: 1 if x>0 else 0)
data_5_new = data_5_new.drop(['RIGHTTYPE', '5ASKYEAR', '5FBYEAR', '5ASKTIME', '5FBTIME'], axis=1)
data_5_new['5fu_ratio'] = data_5_new['5FUYU_RIGHT'] / data_5_new['5RIGHT_COUNT']
data_5_new['5wfu_ratio'] = data_5_new['5WFUYU_RIGHT'] / data_5_new['5RIGHT_COUNT']

first_bg_year = df_1.groupby('EID', sort=False)['5ASKYEAR'].min()
last_bg_year = df_1.groupby('EID', sort=False)['5ASKYEAR'].max()
first_bg_time = df_1.groupby('EID', sort=False)['5ASKTIME'].min()
last_bg_time = df_1.groupby('EID', sort=False)['5ASKTIME'].max()
first_end_year = df_1.groupby('EID', sort=False)['5FBYEAR'].min()
last_end_year = df_1.groupby('EID', sort=False)['5FBYEAR'].max()
first_end_time = df_1.groupby('EID', sort=False)['5FBTIME'].min()
last_end_time = df_1.groupby('EID', sort=False)['5FBTIME'].max()
max_hold_time = df_1.groupby('EID', sort=False)['5hold_time'].max()
min_hold_time = df_1.groupby('EID', sort=False)['5hold_time'].min()
df_1 = df_1.drop_duplicates('EID')
first_bg_year = pd.DataFrame({'EID': df_1['EID'].values, '5first_bg_year': first_bg_year.values})
last_bg_year = pd.DataFrame({'EID': df_1['EID'].values, '5last_bg_year': last_bg_year.values})
first_bg_time = pd.DataFrame({'EID': df_1['EID'].values, '5first_bg_time': first_bg_time.values})
last_bg_time = pd.DataFrame({'EID': df_1['EID'].values, '5last_bg_time': last_bg_time.values})
first_end_year = pd.DataFrame({'EID': df_1['EID'].values, '5first_end_year': first_end_year.values})
last_end_year = pd.DataFrame({'EID': df_1['EID'].values, '5last_end_year': last_end_year.values})
first_end_time = pd.DataFrame({'EID': df_1['EID'].values, '5first_end_time': first_end_time.values})
last_end_time = pd.DataFrame({'EID': df_1['EID'].values, '5last_end_time': last_end_time.values})
max_hold_time = pd.DataFrame({'EID': df_1['EID'].values, '5max_hold_time': max_hold_time})
min_hold_time = pd.DataFrame({'EID': df_1['EID'].values, '5min_hold_time': min_hold_time})
df_new = pd.merge(data_5_new, first_bg_year, on='EID', how='left')
df_new = pd.merge(df_new, last_bg_year, on='EID', how='left')
df_new = pd.merge(df_new, first_bg_time, on='EID', how='left')
df_new = pd.merge(df_new, last_bg_time, on='EID', how='left')
df_new = pd.merge(df_new, first_end_year, on='EID', how='left')
df_new = pd.merge(df_new, last_end_year, on='EID', how='left')
df_new = pd.merge(df_new, first_end_time, on='EID', how='left')
df_new = pd.merge(df_new, last_end_time, on='EID', how='left')
df_new = pd.merge(df_new, max_hold_time, on='EID', how='left')
df_new = pd.merge(df_new, min_hold_time, on='EID', how='left')

df_new['5first_minus_last'] = df_new['5last_bg_time'] - df_new['5first_bg_time']
df_new['5first_minus_first'] = df_new['5first_end_time'] - df_new['5first_bg_time']
df_new['5now_minus_lastbe'] = 2015+(7/12) - df_new['5last_bg_time']
df_new['5now_minus_lastend'] = 2015+(7/12) - df_new['5last_end_time']
df_new['5right_count_avg'] = df_new['5RIGHT_COUNT'] / (df_new['5last_bg_year'] - df_new['5first_bg_year'] + 1)
df_new['5right_fuyu_avg'] = df_new['5FUYU_RIGHT'] / (df_new['5last_bg_year'] - df_new['5first_bg_year'] + 1)
# print(data_5.head(200))
print(df_new.head())

df_new.to_csv('..\\data\\5right_add.csv', index=False)