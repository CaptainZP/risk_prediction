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
# no nomoney item
data_7['LAW_YMONEY_COUNT'] = data_7['LAWAMOUNT'].apply(lambda x: 1 if x!=0 else 0)
data_7['LAW_WMONEY_COUNT'] = data_7['LAWAMOUNT'].apply(lambda x: 1 if x==0 else 0)
df_1 = data_7
data_7 = pd.concat([data_7, pd.get_dummies(data_7['LAWYEAR'], prefix='LAWYEAR')], axis=1)
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
min_money = data_7_1.groupby('EID', sort=False)['LAWAMOUNT'].min()

first_law_year = data_7_1.groupby('EID', sort=False)['LAWYEAR'].min()
last_law_year = data_7_1.groupby('EID', sort=False)['LAWYEAR'].max()
first_law_time = data_7_1.groupby('EID', sort=False)['LAWTIME'].min()
last_law_time = data_7_1.groupby('EID', sort=False)['LAWTIME'].max()
data_7_1 = data_7_1.drop_duplicates('EID')
max_money = pd.DataFrame({'EID': data_7_1['EID'].values, '7max_money': max_money.values})
min_money = pd.DataFrame({'EID': data_7_1['EID'].values, '7min_money': min_money.values})
first_law_year = pd.DataFrame({'EID': data_7_1['EID'].values, '7first_law_year': first_law_year.values})
last_law_year = pd.DataFrame({'EID': data_7_1['EID'].values, '7last_law_year': last_law_year.values})
first_law_time = pd.DataFrame({'EID': data_7_1['EID'].values, '7first_law_time': first_law_time.values})
last_law_time = pd.DataFrame({'EID': data_7_1['EID'].values, '7last_law_time': last_law_time.values})
data_7_new = pd.merge(data_7, first_law_year, on='EID', how='left')
data_7_new = pd.merge(data_7_new, last_law_year, on='EID', how='left')
data_7_new = pd.merge(data_7_new, first_law_time, on='EID', how='left')
data_7_new = pd.merge(data_7_new, last_law_time, on='EID', how='left')
data_7_new = pd.merge(data_7_new, max_money, on='EID', how='left')
data_7_new = pd.merge(data_7_new, min_money, on='EID', how='left')

data_7_new['7last_minus_first'] = data_7_new['7last_law_time'] - data_7_new['7first_law_time']
data_7_new['7now_minus_last'] = 2015+(7/12) - data_7_new['7last_law_time']
data_7_new['7now_minus_first'] = 2015+(7/12) - data_7_new['7first_law_time']

data_7_new['7year_count'] = data_7_new['LAWYEAR_2013'].apply(lambda x: 1 if x>0 else 0) +\
                            data_7_new['LAWYEAR_2014'].apply(lambda x: 1 if x>0 else 0) +\
                            data_7_new['LAWYEAR_2015'].apply(lambda x: 1 if x>0 else 0)

data_7_new['7law_count_avg'] = data_7_new['LAW_COUNT'] / (data_7_new['7last_law_year'] - data_7_new['7first_law_year'] + 1)
df_max_year_alter_time = df_1.groupby(['EID', 'LAWYEAR'], sort=False)['LAW_COUNT'].sum()
df_max_year_alter_time = df_max_year_alter_time.groupby(level=0).max()
df_min_year_alter_time = df_1.groupby(['EID', 'LAWYEAR'], sort=False)['LAW_COUNT'].sum()
df_min_year_alter_time = df_min_year_alter_time.groupby(level=0).min()
df_max_year_alter_time = pd.DataFrame({'EID':data_7_new['EID'].values, '7lawcount_max_year': df_max_year_alter_time.values})
df_min_year_alter_time = pd.DataFrame({'EID':data_7_new['EID'].values, '7lawcount_min_year': df_min_year_alter_time.values})
data_7_new = pd.merge(data_7_new, df_max_year_alter_time, how='left', on='EID')
data_7_new = pd.merge(data_7_new, df_min_year_alter_time, how='left', on='EID')

data_7_new['7law_money_avg_year'] = data_7_new['LAWAMOUNT'] / (data_7_new['7last_law_year'] - data_7_new['7first_law_year'] + 1)
df_max_year_alter_time = df_1.groupby(['EID', 'LAWYEAR'], sort=False)['LAWAMOUNT'].sum()
df_max_year_alter_time = df_max_year_alter_time.groupby(level=0).max()
df_min_year_alter_time = df_1.groupby(['EID', 'LAWYEAR'], sort=False)['LAWAMOUNT'].sum()
df_min_year_alter_time = df_min_year_alter_time.groupby(level=0).min()
df_max_year_alter_time = pd.DataFrame({'EID':data_7_new['EID'].values, '7money_max_in_year': df_max_year_alter_time.values})
df_min_year_alter_time = pd.DataFrame({'EID':data_7_new['EID'].values, '7money_min_in_year': df_min_year_alter_time.values})
data_7_new = pd.merge(data_7_new, df_max_year_alter_time, how='left', on='EID')
data_7_new = pd.merge(data_7_new, df_min_year_alter_time, how='left', on='EID')

data_7_new['7law_ymoney_avg_year'] = data_7_new['LAW_YMONEY_COUNT'] / (data_7_new['7last_law_year'] - data_7_new['7first_law_year'] + 1)
df_max_year_alter_time = df_1.groupby(['EID', 'LAWYEAR'], sort=False)['LAW_YMONEY_COUNT'].sum()
df_max_year_alter_time = df_max_year_alter_time.groupby(level=0).max()
df_min_year_alter_time = df_1.groupby(['EID', 'LAWYEAR'], sort=False)['LAW_YMONEY_COUNT'].sum()
df_min_year_alter_time = df_min_year_alter_time.groupby(level=0).min()
df_max_year_alter_time = pd.DataFrame({'EID':data_7_new['EID'].values, '7ymoney_max_year': df_max_year_alter_time.values})
df_min_year_alter_time = pd.DataFrame({'EID':data_7_new['EID'].values, '7ymoney_min_year': df_min_year_alter_time.values})
data_7_new = pd.merge(data_7_new, df_max_year_alter_time, how='left', on='EID')
data_7_new = pd.merge(data_7_new, df_min_year_alter_time, how='left', on='EID')

def cal_max_interval(arr):
    arr = arr.sort_values().values
    max_interval = 0
    # print(arr[0].astype('datetime64[D]'))
    for i in range(0, len(arr)):
        if 0 < i < len(arr):
            temp_interval = abs(arr[i] - arr[i-1])
            # print(temp_interval)
            if temp_interval > max_interval:
                max_interval = temp_interval
    return max_interval
def cal_min_interval(arr):
    arr = arr.sort_values().values
    min_interval = 999
    # print(arr[0].astype('datetime64[D]'))
    if len(arr) == 1:
        min_interval = 0
    else:
        for i in range(0, len(arr)):
            if 0 < i < len(arr):
                temp_interval = abs(arr[i] - arr[i-1])
                # print(temp_interval)
                if temp_interval < min_interval:
                    min_interval = temp_interval
    return min_interval
def cal_mean_interval(arr):
    arr = arr.sort_values().values
    mean_interval = 0
    if len(arr) == 1:
        return mean_interval
    else:
        for i in range(0, len(arr)):
            if 0 < i < len(arr):
                temp_interval = abs(arr[i] - arr[i-1])
                mean_interval = mean_interval + temp_interval
        mean_interval = round(mean_interval/(len(arr)-1), 2)
        return mean_interval
df_alter_interval = df_1['LAWTIME'].groupby(df_1['EID'], sort=False)
df_max_alter_interval = df_alter_interval.agg(cal_max_interval)
print('df_max_alter_interval:\n', df_max_alter_interval)
df_min_alter_interval = df_alter_interval.agg(cal_min_interval)
print('df_min_alter_interval:\n', df_min_alter_interval)
df_mean_alter_interval = df_alter_interval.agg(cal_mean_interval)
print('df_mean_alter_interval:\n', df_mean_alter_interval)

df_mean_alter_interval = pd.DataFrame({'EID': data_7_new['EID'].values, '7df_mean_alter_interval': df_mean_alter_interval.values})
df_max_alter_interval = pd.DataFrame({'EID': data_7_new['EID'].values, '7df_max_alter_interval': df_max_alter_interval.values})
df_min_alter_interval = pd.DataFrame({'EID': data_7_new['EID'].values, '7df_min_alter_interval': df_min_alter_interval.values})

data_7_new = pd.merge(data_7_new, df_mean_alter_interval, on='EID', how='left')
data_7_new = pd.merge(data_7_new, df_max_alter_interval, on='EID', how='left')
data_7_new = pd.merge(data_7_new, df_min_alter_interval, on='EID', how='left')

data_7_new.to_csv('..\\data\\7lawsuit_add_new.csv', index=False)

# deal with time