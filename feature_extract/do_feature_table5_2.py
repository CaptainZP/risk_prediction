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
df_2 = data_5
data_5 = pd.concat([data_5, pd.get_dummies(data_5['RIGHTTYPE'], prefix='RIGHT')], axis=1)
# data_5 = pd.concat([data_5, pd.get_dummies(data_5['5ASKYEAR'], prefix='askyear')], axis=1)

print(data_5.head(10))
df_1 = data_5

data_5_new = data_5.groupby('EID', sort=False).sum()
data_5_new = data_5_new.reset_index()
data_5_new['5IS_EXIST_WFU'] = data_5_new['5WFUYU_RIGHT'].apply(lambda x: 1 if x>0 else 0)
data_5_new['5IS_EXIST_FU'] = data_5_new['5FUYU_RIGHT'].apply(lambda x: 1 if x>0 else 0)
data_5_new = data_5_new.drop(['RIGHTTYPE', '5ASKYEAR', '5FBYEAR', '5ASKTIME', '5FBTIME'], axis=1)
data_5_new['5fu_ratio'] = data_5_new['5FUYU_RIGHT'] / data_5_new['5RIGHT_COUNT']
data_5_new['5wfu_ratio'] = data_5_new['5WFUYU_RIGHT'] / data_5_new['5RIGHT_COUNT']
data_5_new['5fu_wfu_ratio'] = data_5_new['5FUYU_RIGHT'] / data_5_new['5WFUYU_RIGHT']
data_5_new['5fu_wfu_ratio'] = data_5_new['5fu_wfu_ratio'].apply(lambda x: x if x != np.inf else np.nan)
print(data_5_new)

df2 = df_2[['EID', 'RIGHTTYPE']]
df2 = df2.drop_duplicates(subset=['EID', 'RIGHTTYPE'])
df2['RIGHTTYPE'] = 1
df_num_of_alter = df2.groupby('EID', sort=False).sum()
df_num_of_alter = df_num_of_alter.reset_index()  # dataframe
data_5_new = pd.merge(data_5_new, df_num_of_alter, how='left', on='EID')

# # 增加是否每种类型变更都存在（存在争议）
# data_5_new['2if_right11_exist'] = data_5_new['RIGHT_11'].apply(lambda x: 1 if x > 0 else 0)
# data_5_new['2if_right12_exist'] = data_5_new['RIGHT_12'].apply(lambda x: 1 if x > 0 else 0)
# data_5_new['2if_right20_exist'] = data_5_new['RIGHT_20'].apply(lambda x: 1 if x > 0 else 0)
# data_5_new['2if_right30_exist'] = data_5_new['RIGHT_30'].apply(lambda x: 1 if x > 0 else 0)
# data_5_new['2if_right40_exist'] = data_5_new['RIGHT_40'].apply(lambda x: 1 if x > 0 else 0)
# data_5_new['2if_right50_exist'] = data_5_new['RIGHT_50'].apply(lambda x: 1 if x > 0 else 0)
# data_5_new['2if_right60_exist'] = data_5_new['RIGHT_60'].apply(lambda x: 1 if x > 0 else 0)

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
mean_hold_time = df_1.groupby('EID', sort=False)['5hold_time'].mean()

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
mean_hold_time = pd.DataFrame({'EID': df_1['EID'].values, '5mean_hold_time': mean_hold_time})

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
df_new = pd.merge(df_new, mean_hold_time, on='EID', how='left')

df_new['5first_minus_last'] = df_new['5last_bg_time'] - df_new['5first_bg_time']
df_new['5first_minus_first'] = df_new['5first_end_time'] - df_new['5first_bg_time']
df_new['5now_minus_lastbe'] = 2015+(7/12) - df_new['5last_bg_time']
df_new['5now_minus_firstbe'] = 2015+(7/12) - df_new['5first_bg_time']
df_new['5now_minus_firstend'] = 2015+(7/12) - df_new['5first_end_time']
df_new['5now_minus_lastend'] = 2015+(7/12) - df_new['5last_end_time']
df_new['5firstend_lastask'] = df_new['5first_end_time'] - df_new['5last_bg_time']
df_new['5lastask_firstend'] = df_new['5last_bg_time'] - df_new['5first_end_time']
df_new['5lastend_firstend'] = df_new['5last_end_time'] - df_new['5first_end_time']
df_new['5lastend_lastask'] = df_new['5last_end_time'] - df_new['5last_bg_time']

df_new['5right_count_avg'] = df_new['5RIGHT_COUNT'] / (df_new['5last_bg_year'] - df_new['5first_bg_year'] + 1)
df_max_year_alter_time = df_2.groupby(['EID', '5ASKYEAR'], sort=False)['5RIGHT_COUNT'].sum()
df_max_year_alter_time = df_max_year_alter_time.groupby(level=0).max()
df_min_year_alter_time = df_2.groupby(['EID', '5ASKYEAR'], sort=False)['5RIGHT_COUNT'].sum()
df_min_year_alter_time = df_min_year_alter_time.groupby(level=0).min()
df_max_year_alter_time = pd.DataFrame({'EID':df_new['EID'].values, '5right_max_year': df_max_year_alter_time.values})
df_min_year_alter_time = pd.DataFrame({'EID':df_new['EID'].values, '5right_min_year': df_min_year_alter_time.values})
df_new = pd.merge(df_new, df_max_year_alter_time, how='left', on='EID')
df_new = pd.merge(df_new, df_min_year_alter_time, how='left', on='EID')

df_new['5right_fuyu_avg'] = df_new['5FUYU_RIGHT'] / (df_new['5last_bg_year'] - df_new['5first_bg_year'] + 1)
df_max_year_alter_time = df_2.groupby(['EID', '5FBYEAR'], sort=False)['5FUYU_RIGHT'].sum()
df_max_year_alter_time = df_max_year_alter_time.groupby(level=0).max()
df_min_year_alter_time = df_2.groupby(['EID', '5FBYEAR'], sort=False)['5FUYU_RIGHT'].sum()
df_min_year_alter_time = df_min_year_alter_time.groupby(level=0).min()
df_max_year_alter_time = pd.DataFrame({'EID':df_new['EID'].values, '5fuyuright_max_year': df_max_year_alter_time.values})
df_min_year_alter_time = pd.DataFrame({'EID':df_new['EID'].values, '5fuyuright_min_year': df_min_year_alter_time.values})
df_new = pd.merge(df_new, df_max_year_alter_time, how='left', on='EID')
df_new = pd.merge(df_new, df_min_year_alter_time, how='left', on='EID')

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
df_alter_interval = df_2['5ASKTIME'].groupby(df_2['EID'], sort=False)
df_max_alter_interval = df_alter_interval.agg(cal_max_interval)
print('df_max_alter_interval:\n', df_max_alter_interval)
df_min_alter_interval = df_alter_interval.agg(cal_min_interval)
print('df_min_alter_interval:\n', df_min_alter_interval)
df_mean_alter_interval = df_alter_interval.agg(cal_mean_interval)
print('df_mean_alter_interval:\n', df_mean_alter_interval)

df_mean_alter_interval = pd.DataFrame({'EID': df_1['EID'].values, '5df_mean_alter_interval': df_mean_alter_interval.values})
df_max_alter_interval = pd.DataFrame({'EID': df_1['EID'].values, '5df_max_alter_interval': df_max_alter_interval.values})
df_min_alter_interval = pd.DataFrame({'EID': df_1['EID'].values, '5df_min_alter_interval': df_min_alter_interval.values})

df_new = pd.merge(df_new, df_mean_alter_interval, on='EID', how='left')
df_new = pd.merge(df_new, df_max_alter_interval, on='EID', how='left')
df_new = pd.merge(df_new, df_min_alter_interval, on='EID', how='left')


df_new.to_csv('..\\data\\5right_add_new.csv', index=False)