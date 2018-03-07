import pandas as pd
import numpy as np

datafile4 = '..\\data\\4invest.csv'
data_4 = pd.read_csv(datafile4)
# data_4 = data_4.fillna(0)

data_4['BTCOUNT'] = 1
data_4['BS_BTCOUNT'] = data_4['IFHOME'].apply(lambda x: 1 if x==1 else 0)
data_4['WS_BTCOUNT'] = data_4['IFHOME'].apply(lambda x: 1 if x!=1 else 0)
data_4['BT_END_COUNT'] = data_4['BTENDYEAR'].apply(lambda x: 1 if x>0 else 0)
data_4['BT_NORMAL_COUNT'] = data_4['BTENDYEAR'].apply(lambda x: 0 if x>0 else 1)
data_4['BS_BT_END'] = data_4['BS_BTCOUNT'] & data_4['BT_END_COUNT']
data_4['WS_BT_END'] = data_4['WS_BTCOUNT'] & data_4['BT_END_COUNT']
btlive = data_4['BTENDYEAR'] - data_4['BTYEAR']
data_4['BT_LIVE'] = btlive[btlive>=0]
data_4['BS_BT_LIVE'] = data_4['BS_BTCOUNT'] * data_4['BT_LIVE']
data_4['WS_BT_LIVE'] = data_4['WS_BTCOUNT'] * data_4['BT_LIVE']
data_4['BS_BT_BL'] = data_4['BS_BTCOUNT'] * data_4['BTBL']
data_4['WS_BT_BL'] = data_4['WS_BTCOUNT'] * data_4['BTBL']
print(data_4.tail(10))
df_1 =data_4

data_4_new = data_4.groupby('EID', sort=False).sum()
data_4_new = data_4_new.reset_index()
data_4_new['BS_BT_LIVE_AVG'] = data_4_new['BS_BT_LIVE']/data_4_new['BS_BTCOUNT']
data_4_new['WS_BT_LIVE_AVG'] = data_4_new['WS_BT_LIVE']/data_4_new['WS_BTCOUNT']
data_4_new['BT_LIVE_AVG'] = data_4_new['BT_LIVE']/data_4_new['BTCOUNT']
data_4_new['BT_BL_AVG'] = data_4_new['BTBL']/data_4_new['BTCOUNT']
data_4_new['BS_BT_BL_AVG'] = data_4_new['BS_BT_BL']/data_4_new['BS_BTCOUNT']
data_4_new['WS_BT_BL_AVG'] = data_4_new['WS_BT_BL']/data_4_new['WS_BTCOUNT']
data_4_new['IS_EXIST_BT'] = data_4_new['BTCOUNT'].apply(lambda x: 1 if x>0 else 0)
data_4_new['IS_EXIST_NORMAL_BT'] = data_4_new['BT_NORMAL_COUNT'].apply(lambda x: 1 if x>0 else 0)
data_4_new['4live_ratio'] = data_4_new['BT_NORMAL_COUNT'] / data_4_new['BTCOUNT']
data_4_new['4end_ratio'] = data_4_new['BT_END_COUNT'] / data_4_new['BTCOUNT']

data_4_new = data_4_new.drop(['IFHOME', 'BTYEAR', 'BTENDYEAR'], axis=1)
print(data_4_new.tail(10))

last_bt_year = df_1.groupby('EID', sort=False)['BTYEAR'].max()
first_bt_year = df_1.groupby('EID', sort=False)['BTYEAR'].min()
last_end_year = df_1.groupby('EID', sort=False)['BTENDYEAR'].max()
first_end_year = df_1.groupby('EID', sort=False)['BTENDYEAR'].min()
max_hold_time = df_1.groupby('EID', sort=False)['BT_LIVE'].max()
min_hold_time = df_1.groupby('EID', sort=False)['BT_LIVE'].min()
df_1 = df_1.drop_duplicates('EID')
last_bt_year = pd.DataFrame({"EID": df_1['EID'].values, '4last_bt_year': last_bt_year.values})
first_bt_year = pd.DataFrame({"EID": df_1['EID'].values, '4first_bt_year': first_bt_year.values})
last_end_year = pd.DataFrame({"EID": df_1['EID'].values, '4last_end_year': last_end_year.values})
first_end_year = pd.DataFrame({"EID": df_1['EID'].values, '4first_end_year': first_end_year.values})
max_hold_time = pd.DataFrame({'EID': df_1['EID'].values, '4max_hold_time': max_hold_time})
min_hold_time = pd.DataFrame({'EID': df_1['EID'].values, '4min_hold_time': min_hold_time})
df_new = pd.merge(data_4_new, last_bt_year, on='EID', how='left')
df_new = pd.merge(df_new, first_bt_year, on='EID', how='left')
df_new = pd.merge(df_new, last_end_year, on='EID', how='left')
df_new = pd.merge(df_new, first_end_year, on='EID', how='left')
df_new = pd.merge(df_new, max_hold_time, on='EID', how='left')
df_new = pd.merge(df_new, min_hold_time, on='EID', how='left')

df_new['4last_minus_first'] = df_new['4last_bt_year'] - df_new['4first_bt_year']
df_new['4first_minus_first'] = df_new['4first_end_year'] - df_new['4first_bt_year']
df_new['4now_minus_lastbe'] = 2015+(7/12) - df_new['4last_bt_year']
df_new['4now_minus_lastend'] = 2015+(7/12) - df_new['4last_end_year']
df_new['4bt_avg'] = df_new['BTCOUNT'] / (df_new['4last_minus_first'] + 1)
df_new['4bt_avg_end'] = df_new['BT_END_COUNT'] / (df_new['4last_minus_first'] + 1)
df_new['4bt_avg_in'] = df_new['BT_NORMAL_COUNT'] / (df_new['4last_minus_first'] + 1)

df_new.to_csv('..\\data\\4invest_add.csv', index=False)