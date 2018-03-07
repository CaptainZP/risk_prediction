import pandas as pd
import re


datafile7 = '..\\data\\7lawsuit.csv'
data_7 = pd.read_csv(datafile7)

# do with no time
data_7['LAW_COUNT'] = 1
# data_7['LAWDATE'] = data_7['LAWDATE'].apply(lambda x: x.encode('gbk'))
data_7['LAWDATE'] = data_7['LAWDATE'].apply(lambda x: (re.findall(r"\d+\.?\d*", x)))
print(data_7.head())
# data_7['LAWDATE'] = pd.to_datetime(data_7['LAWDATE'], format='%Y/%m/%d')
data_7['LAWYEAR'] = data_7['LAWDATE'].apply(lambda x: int(x[0]))
data_7['LAWTIME'] = data_7['LAWDATE'].apply(lambda x: int(x[0]) + (int(x[1]) - 1) / 12)
data_7 = pd.concat([data_7, pd.get_dummies(data_7['LAWYEAR'], prefix='LAWYEAR')], axis=1)

# no nomoney item
data_7['LAW_YMONEY_COUNT'] = data_7['LAWAMOUNT'].apply(lambda x: 1 if x!=0 else 0)
data_7['LAW_WMONEY_COUNT'] = data_7['LAWAMOUNT'].apply(lambda x: 1 if x==0 else 0)
data_7_1 = data_7

data_7 = data_7.groupby('EID', sort=False).sum()
data_7 = data_7.reset_index()
print(data_7.head())
data_7['LAW_AMOUNT_AVG'] = data_7['LAWAMOUNT']/data_7['LAW_COUNT']
data_7['LAW_AMOUNT_AVG_YB'] = data_7['LAWAMOUNT']/data_7['LAW_YMONEY_COUNT']
data_7['IS_YBDYWB'] = data_7['LAW_YMONEY_COUNT']-data_7['LAW_WMONEY_COUNT']
data_7['IS_YBDYWB'] = data_7['IS_YBDYWB'].apply(lambda x: 1 if x>0 else 0)
data_7['LAW_YB_RATE'] = data_7['LAW_YMONEY_COUNT'] / data_7['LAW_COUNT']
data_7['LAW_WB_RATE'] = data_7['LAW_WMONEY_COUNT'] / data_7['LAW_COUNT']
data_7['IS_EXIST_YB'] = data_7['LAW_YMONEY_COUNT'].apply(lambda x: 1 if x>0 else 0)
data_7['IS_EXIST_WB'] = data_7['LAW_WMONEY_COUNT'].apply(lambda x: 1 if x>0 else 0)
data_7 = data_7.drop(['TYPECODE', 'LAWYEAR', 'LAWTIME'], axis=1)

max_money = data_7_1.groupby('EID', sort=False)['LAWAMOUNT'].max()
first_law_year = data_7_1.groupby('EID', sort=False)['LAWYEAR'].min()
last_law_year = data_7_1.groupby('EID', sort=False)['LAWYEAR'].max()
first_law_time = data_7_1.groupby('EID', sort=False)['LAWTIME'].min()
last_law_time = data_7_1.groupby('EID', sort=False)['LAWTIME'].max()
data_7_1 = data_7_1.drop_duplicates('EID')
max_money = pd.DataFrame({'EID': data_7_1['EID'].values, '7max_money': max_money.values})
first_law_year = pd.DataFrame({'EID': data_7_1['EID'].values, '7first_law_year': first_law_year.values})
last_law_year = pd.DataFrame({'EID': data_7_1['EID'].values, '7last_law_year': last_law_year.values})
first_law_time = pd.DataFrame({'EID': data_7_1['EID'].values, '7first_law_time': first_law_time.values})
last_law_time = pd.DataFrame({'EID': data_7_1['EID'].values, '7last_law_time': last_law_time.values})
data_7_new = pd.merge(data_7, first_law_year, on='EID', how='left')
data_7_new = pd.merge(data_7_new, last_law_year, on='EID', how='left')
data_7_new = pd.merge(data_7_new, first_law_time, on='EID', how='left')
data_7_new = pd.merge(data_7_new, last_law_time, on='EID', how='left')
data_7_new = pd.merge(data_7_new, max_money, on='EID', how='left')

data_7_new['7last_minus_first'] = data_7_new['7last_law_time'] - data_7_new['7first_law_time']
data_7_new['7now_minus_last'] = 2015+(7/12) - data_7_new['7first_law_time']
data_7_new['7law_count_avg'] = data_7_new['LAW_COUNT'] / (data_7_new['7last_law_year'] - data_7_new['7first_law_year'] + 1)
data_7_new['7law_money_avg_year'] = data_7_new['LAWAMOUNT'] / (data_7_new['7last_law_year'] - data_7_new['7first_law_year'] + 1)

data_7_new.to_csv('..\\data\\7lawsuit_add.csv', index=False)

# deal with time