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
df_2 = df
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
df_new['8lastend_minus_firstin'] = df_new['8last_end_time'] - df_new['8first_fb_time']
df_new['8now_minus_firstend'] = 2015+(7/12) - df_new['8first_end_time']
df_new['8now_minus_firstin'] = 2015+(7/12) - df_new['8first_fb_time']
df_new['8lastend_minus_lastin'] = df_new['8last_end_time'] - df_new['8last_fb_time']
df_new['8lastin_minus_firstend'] = df_new['8last_fb_time'] - df_new['8first_end_time']
df_new['8lastend_minus_firstend'] = df_new['8last_end_time'] - df_new['8first_end_time']

df_new['8bf_count_avg'] = df_new['BF_COUNT'] / (df_new['8last_fb_year'] - df_new['8first_fb_year'] + 1)
df_new['8endbf_count_avg'] = df_new['BF_END'] / (df_new['8last_end_year'] - df_new['8first_end_year'] + 1)
df_new['8inbf_count_avg'] = df_new['BF_IN'] / (df_new['8last_fb_year'] - df_new['8first_fb_year'] + 1)

df_new['8mean_hold_time'] = df_new['FB_HOLD_TIME'] / df_new['BF_COUNT']

df_new['8bf_year_count'] = df_new['FBYEAR_2013'].apply(lambda x: 1 if x>0 else 0) + \
                           df_new['FBYEAR_2014'].apply(lambda x: 1 if x>0 else 0) + \
                           df_new['FBYEAR_2015'].apply(lambda x: 1 if x>0 else 0)

df_max_year_alter_time = df_2.groupby(['EID', 'FBYEAR'], sort=False)['BF_COUNT'].sum()
df_max_year_alter_time = df_max_year_alter_time.groupby(level=0).max()
df_min_year_alter_time = df_2.groupby(['EID', 'FBYEAR'], sort=False)['BF_COUNT'].sum()
df_min_year_alter_time = df_min_year_alter_time.groupby(level=0).min()
df_max_year_alter_time = pd.DataFrame({'EID':df_new['EID'].values, '8df_new_max_year': df_max_year_alter_time.values})
df_min_year_alter_time = pd.DataFrame({'EID':df_new['EID'].values, '8df_new_min_year': df_min_year_alter_time.values})
df_new = pd.merge(df_new, df_max_year_alter_time, how='left', on='EID')
df_new = pd.merge(df_new, df_min_year_alter_time, how='left', on='EID')

# df_max_year_alter_time = df_2.groupby(['EID', 'FBYEAR'], sort=False)['BF_IN'].sum()
# df_max_year_alter_time = df_max_year_alter_time.groupby(level=0).max()
# df_min_year_alter_time = df_2.groupby(['EID', 'FBYEAR'], sort=False)['BF_IN'].sum()
# df_min_year_alter_time = df_min_year_alter_time.groupby(level=0).min()
# df_max_year_alter_time = pd.DataFrame({'EID':df_new['EID'].values, '8df_new_max_in_year': df_max_year_alter_time.values})
# df_min_year_alter_time = pd.DataFrame({'EID':df_new['EID'].values, '8df_new_min_in_year': df_min_year_alter_time.values})
# df_new = pd.merge(df_new, df_max_year_alter_time, how='left', on='EID')
# df_new = pd.merge(df_new, df_min_year_alter_time, how='left', on='EID')

# df_year_alter_time = df_2.groupby(['EID', 'ENDYEAR'], sort=False)['BF_END'].sum()  # 失信时间都是一样的，先不做年失信统计
# df_max_year_alter_time = df_year_alter_time.groupby(level=0).max()
# df_min_year_alter_time = df_year_alter_time.groupby(level=0).min()
# df_max_year_alter_time = df_max_year_alter_time.reset_index()
# df_min_year_alter_time = df_min_year_alter_time.reset_index()
# df_new = pd.merge(df_new, df_max_year_alter_time, how='left', on='EID')
# df_new = pd.merge(df_new, df_min_year_alter_time, how='left', on='EID')
#
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
df_alter_interval = df_2['FBTIME'].groupby(df_2['EID'], sort=False)
df_max_alter_interval = df_alter_interval.agg(cal_max_interval)
print('df_max_alter_interval:\n', df_max_alter_interval)
df_min_alter_interval = df_alter_interval.agg(cal_min_interval)
print('df_min_alter_interval:\n', df_min_alter_interval)
df_mean_alter_interval = df_alter_interval.agg(cal_mean_interval)
print('df_mean_alter_interval:\n', df_mean_alter_interval)

df_mean_alter_interval = pd.DataFrame({'EID': df_1['EID'].values, '8df_mean_alter_interval': df_mean_alter_interval.values})
df_max_alter_interval = pd.DataFrame({'EID': df_1['EID'].values, '8df_max_alter_interval': df_max_alter_interval.values})
df_min_alter_interval = pd.DataFrame({'EID': df_1['EID'].values, '8df_min_alter_interval': df_min_alter_interval.values})

df_new = pd.merge(df_new, df_mean_alter_interval, on='EID', how='left')
df_new = pd.merge(df_new, df_max_alter_interval, on='EID', how='left')
df_new = pd.merge(df_new, df_min_alter_interval, on='EID', how='left')

df_new.to_csv('..\\data\\8breakfaith_add_new.csv', index=False)
#