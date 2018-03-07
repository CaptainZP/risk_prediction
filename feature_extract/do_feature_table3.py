import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time

datafile3 = '..\\data\\3branch.csv'
data_3 = pd.read_csv(datafile3)

t = time.time()
# add feature for table3
# data_3 = data_3.fillna(0)

data_3['BR_COUNT'] = 1
data_3['NORMAL_BR'] = data_3['B_ENDYEAR'].apply(lambda x: 0 if x>0 else 1)
data_3['END_BR'] = data_3['B_ENDYEAR'].apply(lambda x: 1 if x>0 else 0)
data_3['WS_BR'] = data_3['IFHOME'].apply(lambda x: 0 if x==1 else 1)
data_3['BS_BR'] = data_3['IFHOME'].apply(lambda x: 1 if x==1 else 0)
data_3['BS_NORMAL_BR'] = data_3['BS_BR']
data_3['BS_NORMAL_BR'] = data_3['NORMAL_BR'] & data_3['BS_NORMAL_BR']
# data_3['BS_NORMAL_BR'] = 0
# index = data_3[data_3['IFHOME']==1].index & data_3[data_3['B_ENDYEAR']==0].index
# data_3.iloc[index] = 1
data_3['BS_END_BR'] = data_3['BS_BR'] & data_3['END_BR']
data_3['WS_NORMAL_BR'] = data_3['WS_BR'] & data_3['NORMAL_BR']
data_3['WS_END_BR'] = data_3['WS_BR'] & data_3['END_BR']
brlive = data_3['B_ENDYEAR'] - data_3['B_REYEAR']
data_3['BRLIVE'] = brlive[brlive>=0]
data_3['BS_END_BR_LIVE'] = data_3['BRLIVE'] * data_3['BS_END_BR']
data_3['WS_END_BR_LIVE'] = data_3['BRLIVE'] * data_3['WS_END_BR']
df_1 = data_3

data_3 = data_3.groupby('EID', sort=False).sum()
data_3 = data_3.reset_index()
data_3['BRLIVE_AVG'] = data_3['BRLIVE'] / data_3['END_BR']
data_3['BS_END_BR_LIVE_AVG'] = data_3['BS_END_BR_LIVE'] / data_3['BS_END_BR']
data_3['WS_END_BR_LIVE_AVG'] = data_3['WS_END_BR_LIVE'] / data_3['WS_END_BR']
data_3['3live_ratio'] = data_3['NORMAL_BR'] / data_3['BR_COUNT']
data_3['3end_ratio'] = data_3['END_BR'] / data_3['BR_COUNT']
data_3['3bs_ratio'] = data_3['BS_BR'] / data_3['BR_COUNT']
data_3['3ws_ratio'] = data_3['WS_BR'] / data_3['BR_COUNT']

data_3 = data_3.drop(['IFHOME', 'B_REYEAR', 'B_ENDYEAR'], axis=1)
print(data_3)
#
# data_3['EID'] = data_3.index
# cols = list(data_3)
# cols.insert(0, cols.pop(cols.index('EID')))
# data_3 = data_3.ix[:, cols]
# print(data_3.head())

last_bt_year = df_1.groupby('EID', sort=False)['B_REYEAR'].max()
first_bt_year = df_1.groupby('EID', sort=False)['B_REYEAR'].min()
last_end_year = df_1.groupby('EID', sort=False)['B_ENDYEAR'].max()
first_end_year = df_1.groupby('EID', sort=False)['B_ENDYEAR'].min()
max_hold_time = df_1.groupby('EID', sort=False)['BRLIVE'].max()
min_hold_time = df_1.groupby('EID', sort=False)['BRLIVE'].min()
df_1 = df_1.drop_duplicates('EID')
last_bt_year = pd.DataFrame({"EID": df_1['EID'].values, '3last_br_year': last_bt_year.values})
first_bt_year = pd.DataFrame({"EID": df_1['EID'].values, '3first_br_year': first_bt_year.values})
last_end_year = pd.DataFrame({"EID": df_1['EID'].values, '3last_end_year': last_end_year.values})
first_end_year = pd.DataFrame({"EID": df_1['EID'].values, '3first_end_year': first_end_year.values})
max_hold_time = pd.DataFrame({'EID': df_1['EID'].values, '3max_hold_time': max_hold_time})
min_hold_time = pd.DataFrame({'EID': df_1['EID'].values, '3min_hold_time': min_hold_time})
df_new = pd.merge(data_3, last_bt_year, on='EID', how='left')
df_new = pd.merge(df_new, first_bt_year, on='EID', how='left')
df_new = pd.merge(df_new, last_end_year, on='EID', how='left')
df_new = pd.merge(df_new, first_end_year, on='EID', how='left')
df_new = pd.merge(df_new, max_hold_time, on='EID', how='left')
df_new = pd.merge(df_new, min_hold_time, on='EID', how='left')

df_new['3last_minus_first'] = df_new['3last_br_year'] - df_new['3first_br_year']
df_new['3first_minus_first'] = df_new['3first_end_year'] - df_new['3first_br_year']
df_new['3now_minus_lastbe'] = 2015+(7/12) - df_new['3last_br_year']
df_new['3now_minus_lastend'] = 2015+(7/12) - df_new['3last_end_year']
df_new['3br_avg'] = df_new['BR_COUNT'] / (df_new['3last_minus_first'] + 1)
df_new['3br_avg_end'] = df_new['END_BR'] / (df_new['3last_minus_first'] + 1)
df_new['3br_avg_in'] = df_new['NORMAL_BR'] / (df_new['3last_minus_first'] + 1)

df_new.to_csv('..\\data\\3branch_add.csv', index=False)

print('run time is :', time.time() - t)







