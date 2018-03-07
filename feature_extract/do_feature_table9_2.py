import pandas as pd
import numpy as np
import re


datafile9 = '..\\data\\9recruit.csv'
data_9 = pd.read_csv(datafile9, low_memory=False)
data_9['count'] = 1  # 招聘次数
data_9['PNUM']= data_9['PNUM'].apply(lambda x: int(x) if str(x).isdigit() else np.nan)   # 招聘ren数
# 用所有的mean填充
data_9 = data_9.fillna({'PNUM': data_9['PNUM'].mean()})
data_9['IS_WZ1'] = data_9['WZCODE'].apply(lambda x: 1 if x=='zp01' else 0)   # 网站1招聘次数
data_9['IS_WZ2'] = data_9['WZCODE'].apply(lambda x: 1 if x=='zp02' else 0)
data_9['IS_WZ3'] = data_9['WZCODE'].apply(lambda x: 1 if x=='zp03' else 0)
data_9['WZ1_RECRNUM'] = data_9['IS_WZ1'] * data_9['PNUM']    # 网站1招聘人数
data_9['WZ2_RECRNUM'] = data_9['IS_WZ2'] * data_9['PNUM']
data_9['WZ3_RECRNUM'] = data_9['IS_WZ3'] * data_9['PNUM']

data_9['RECREDATE'] = pd.to_datetime(data_9['RECDATE'], format='%Y/%m/%d')
data_9['RETIME'] = data_9['RECREDATE'].apply(lambda x: x.year + (x.month - 1)/12)
data_9['REYEAR'] = data_9['RECREDATE'].apply(lambda x: x.year)
df_2 = data_9
data_9 = pd.concat([data_9, pd.get_dummies(data_9['REYEAR'], prefix='REYEAR')], axis=1)

data_9['92008num'] = data_9['REYEAR_2008'] * data_9['PNUM']
data_9['92012num'] = data_9['REYEAR_2012'] * data_9['PNUM']
data_9['92013num'] = data_9['REYEAR_2013'] * data_9['PNUM']
data_9['92014num'] = data_9['REYEAR_2014'] * data_9['PNUM']
data_9['92015num'] = data_9['REYEAR_2015'] * data_9['PNUM']
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
data_9_new['9year_count'] = data_9_new['REYEAR_2008'].apply(lambda x: 1 if  x>0 else 0) + \
                            data_9_new['REYEAR_2012'].apply(lambda x: 1 if  x>0 else 0) + \
                            data_9_new['REYEAR_2013'].apply(lambda x: 1 if  x>0 else 0) + \
                            data_9_new['REYEAR_2014'].apply(lambda x: 1 if  x>0 else 0) + \
                            data_9_new['REYEAR_2015'].apply(lambda x: 1 if  x>0 else 0)
data_9_new = data_9_new.drop(['RETIME', 'REYEAR'], axis=1)

# df_new = data_9_new[['REYEAR_2008', 'REYEAR_2012', 'REYEAR_2013', 'REYEAR_2014', 'REYEAR_2015']]
# df_new_max_year = df_new.max(axis=1)
# df_new_min_year = df_new.min(axis=1)
# # print(type(df_new_max_year))
# df_new_max_year = pd.DataFrame({'EID':data_9_new['EID'].values, 'df_new_max_year': df_new_max_year.values})
# df_new_min_year = pd.DataFrame({'EID':data_9_new['EID'].values, 'df_new_min_year': df_new_min_year.values})
#
# data_9_new = pd.merge(data_9_new, df_new_max_year, how='left', on='EID')
# data_9_new = pd.merge(data_9_new, df_new_min_year, how='left', on='EID')
# print(data_9_new.head())

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
df_alter_interval = df_1['RETIME'].groupby(df_1['EID'], sort=False)
df_max_alter_interval = df_alter_interval.agg(cal_max_interval)
print('df_max_alter_interval:\n', df_max_alter_interval)
df_min_alter_interval = df_alter_interval.agg(cal_min_interval)
print('df_min_alter_interval:\n', df_min_alter_interval)
df_mean_alter_interval = df_alter_interval.agg(cal_mean_interval)
print('df_mean_alter_interval:\n', df_mean_alter_interval)

wz1_time_mean = df_1.groupby('EID', sort=False)['IS_WZ1'].mean()
wz1_time_min = df_1.groupby('EID', sort=False)['IS_WZ1'].min()
wz1_time_max = df_1.groupby('EID', sort=False)['IS_WZ1'].max()
wz2_time_mean = df_1.groupby('EID', sort=False)['IS_WZ2'].mean()
wz2_time_min = df_1.groupby('EID', sort=False)['IS_WZ2'].min()
wz2_time_max = df_1.groupby('EID', sort=False)['IS_WZ2'].max()
wz3_time_mean = df_1.groupby('EID', sort=False)['IS_WZ3'].mean()
wz3_time_min = df_1.groupby('EID', sort=False)['IS_WZ3'].min()
wz3_time_max = df_1.groupby('EID', sort=False)['IS_WZ3'].max()
#
wz1_num_mean = df_1.groupby('EID', sort=False)['WZ1_RECRNUM'].mean()
wz1_num_min = df_1.groupby('EID', sort=False)['WZ1_RECRNUM'].min()
wz1_num_max = df_1.groupby('EID', sort=False)['WZ1_RECRNUM'].max()
wz2_num_mean = df_1.groupby('EID', sort=False)['WZ2_RECRNUM'].mean()
wz2_num_min = df_1.groupby('EID', sort=False)['WZ2_RECRNUM'].min()
wz2_num_max = df_1.groupby('EID', sort=False)['WZ2_RECRNUM'].max()
wz3_num_mean = df_1.groupby('EID', sort=False)['WZ3_RECRNUM'].mean()
wz3_num_min = df_1.groupby('EID', sort=False)['WZ3_RECRNUM'].min()
wz3_num_max = df_1.groupby('EID', sort=False)['WZ3_RECRNUM'].max()
#
# time_2008_mean = df_1.groupby('EID', sort=False)['REYEAR_2008'].mean()
# time_2008_max = df_1.groupby('EID', sort=False)['REYEAR_2008'].max()
# time_2008_min = df_1.groupby('EID', sort=False)['REYEAR_2008'].min()
# time_2012_mean = df_1.groupby('EID', sort=False)['REYEAR_2012'].mean()
# time_2012_max = df_1.groupby('EID', sort=False)['REYEAR_2012'].max()
# time_2012_min = df_1.groupby('EID', sort=False)['REYEAR_2012'].min()
# time_2013_mean = df_1.groupby('EID', sort=False)['REYEAR_2013'].mean()
# time_2013_max = df_1.groupby('EID', sort=False)['REYEAR_2013'].max()
# time_2013_min = df_1.groupby('EID', sort=False)['REYEAR_2013'].min()
# time_2014_mean = df_1.groupby('EID', sort=False)['REYEAR_2014'].mean()
# time_2014_max = df_1.groupby('EID', sort=False)['REYEAR_2014'].max()
# time_2014_min = df_1.groupby('EID', sort=False)['REYEAR_2014'].min()
# time_2015_mean = df_1.groupby('EID', sort=False)['REYEAR_2015'].mean()
# time_2015_max = df_1.groupby('EID', sort=False)['REYEAR_2015'].max()
# time_2015_min = df_1.groupby('EID', sort=False)['REYEAR_2015'].min()
#
# num_2008_mean = df_1.groupby('EID', sort=False)['92008num'].mean()
# num_2008_max = df_1.groupby('EID', sort=False)['92008num'].max()
# num_2008_min = df_1.groupby('EID', sort=False)['92008num'].min()
# num_2012_mean = df_1.groupby('EID', sort=False)['92012num'].mean()
# num_2012_max = df_1.groupby('EID', sort=False)['92012num'].max()
# num_2012_min = df_1.groupby('EID', sort=False)['92012num'].min()
# num_2013_mean = df_1.groupby('EID', sort=False)['92013num'].mean()
# num_2013_max = df_1.groupby('EID', sort=False)['92013num'].max()
# num_2013_min = df_1.groupby('EID', sort=False)['92013num'].min()
# num_2014_mean = df_1.groupby('EID', sort=False)['92014num'].mean()
# num_2014_max = df_1.groupby('EID', sort=False)['92014num'].max()
# num_2014_min = df_1.groupby('EID', sort=False)['92014num'].min()
# num_2015_mean = df_1.groupby('EID', sort=False)['92015num'].mean()
# num_2015_max = df_1.groupby('EID', sort=False)['92015num'].max()
# num_2015_min = df_1.groupby('EID', sort=False)['92015num'].min()


first_law_year = df_1.groupby('EID', sort=False)['REYEAR'].min()
last_law_year = df_1.groupby('EID', sort=False)['REYEAR'].max()
first_law_time = df_1.groupby('EID', sort=False)['RETIME'].min()
last_law_time = df_1.groupby('EID', sort=False)['RETIME'].max()
#
df_1 = df_1.drop_duplicates('EID')
df_mean_alter_interval = pd.DataFrame({'EID': df_1['EID'].values, '9df_mean_alter_interval': df_mean_alter_interval.values})
df_max_alter_interval = pd.DataFrame({'EID': df_1['EID'].values, '9df_max_alter_interval': df_max_alter_interval.values})
df_min_alter_interval = pd.DataFrame({'EID': df_1['EID'].values, '9df_min_alter_interval': df_min_alter_interval.values})

wz1_time_mean = pd.DataFrame({'EID': df_1['EID'].values, '9wz1_time_mean': wz1_time_mean.values})
wz1_time_min = pd.DataFrame({'EID': df_1['EID'].values, 'wz1_time_min': wz1_time_min.values})
wz1_time_max = pd.DataFrame({'EID': df_1['EID'].values, 'wz1_time_max': wz1_time_max.values})
wz2_time_mean = pd.DataFrame({'EID': df_1['EID'].values, 'wz2_time_mean': wz2_time_mean.values})
wz2_time_min = pd.DataFrame({'EID': df_1['EID'].values, 'wz2_time_min': wz2_time_min.values})
wz2_time_max = pd.DataFrame({'EID': df_1['EID'].values, 'wz2_time_max': wz2_time_max.values})
wz3_time_mean = pd.DataFrame({'EID': df_1['EID'].values, 'wz3_time_mean': wz3_time_mean.values})
wz3_time_min = pd.DataFrame({'EID': df_1['EID'].values, 'wz3_time_min': wz3_time_min.values})
wz3_time_max = pd.DataFrame({'EID': df_1['EID'].values, 'wz3_time_max': wz3_time_max.values})
#
wz1_num_mean = pd.DataFrame({'EID': df_1['EID'].values, 'wz1_num_mean': wz1_num_mean.values})
wz1_num_min = pd.DataFrame({'EID': df_1['EID'].values, 'wz1_num_min': wz1_num_min.values})
wz1_num_max = pd.DataFrame({'EID': df_1['EID'].values, 'wz1_num_max': wz1_num_max.values})
wz2_num_mean = pd.DataFrame({'EID': df_1['EID'].values, 'wz2_num_mean': wz2_num_mean.values})
wz2_num_min = pd.DataFrame({'EID': df_1['EID'].values, 'wz2_num_min': wz2_num_min.values})
wz2_num_max = pd.DataFrame({'EID': df_1['EID'].values, 'wz2_num_max': wz2_num_max.values})
wz3_num_mean = pd.DataFrame({'EID': df_1['EID'].values, 'wz3_num_mean': wz3_num_mean.values})
wz3_num_min = pd.DataFrame({'EID': df_1['EID'].values, 'wz3_num_min': wz3_num_min.values})
print(wz3_num_max.values)
wz3_num_max = pd.DataFrame({'EID': df_1['EID'].values, 'wz3_num_max': wz3_num_max.values})

# num_2008_mean = pd.DataFrame({'EID': df_1['EID'].values, 'num_2008_mean': num_2008_mean.values})
# num_2008_min = pd.DataFrame({'EID': df_1['EID'].values, 'num_2008_min': num_2008_min.values})
# num_2008_max = pd.DataFrame({'EID': df_1['EID'].values, 'num_2008_max': num_2008_max.values})
# num_2012_mean = pd.DataFrame({'EID': df_1['EID'].values, 'num_2012_mean': num_2012_mean.values})
# num_2012_min = pd.DataFrame({'EID': df_1['EID'].values, 'num_2012_min': num_2012_min.values})
# num_2012_max = pd.DataFrame({'EID': df_1['EID'].values, 'num_2012_max': num_2012_max.values})
# num_2013_mean = pd.DataFrame({'EID': df_1['EID'].values, 'num_2013_mean': num_2013_mean.values})
# num_2013_min = pd.DataFrame({'EID': df_1['EID'].values, 'num_2013_min': num_2013_min.values})
# num_2013_max = pd.DataFrame({'EID': df_1['EID'].values, 'num_2013_max': num_2013_max.values})
# num_2014_mean = pd.DataFrame({'EID': df_1['EID'].values, 'num_2014_mean': num_2014_mean.values})
# num_2014_min = pd.DataFrame({'EID': df_1['EID'].values, 'num_2014_min': num_2014_min.values})
# num_2014_max = pd.DataFrame({'EID': df_1['EID'].values, 'num_2014_max': num_2014_max.values})
# num_2015_mean = pd.DataFrame({'EID': df_1['EID'].values, 'num_2015_mean': num_2015_mean.values})
# num_2015_min = pd.DataFrame({'EID': df_1['EID'].values, 'num_2015_min': num_2015_min.values})
# num_2015_max = pd.DataFrame({'EID': df_1['EID'].values, 'num_2015_max': num_2015_max.values})
#
# time_2008_mean = pd.DataFrame({'EID': df_1['EID'].values, 'time_2008_mean': time_2008_mean.values})
# time_2008_min = pd.DataFrame({'EID': df_1['EID'].values, 'time_2008_min': time_2008_min.values})
# time_2008_max = pd.DataFrame({'EID': df_1['EID'].values, 'time_2008_max': time_2008_max.values})
# time_2012_mean = pd.DataFrame({'EID': df_1['EID'].values, 'time_2012_mean': time_2012_mean.values})
# time_2012_min = pd.DataFrame({'EID': df_1['EID'].values, 'time_2012_min': time_2012_min.values})
# time_2012_max = pd.DataFrame({'EID': df_1['EID'].values, 'time_2012_max': time_2012_max.values})
# time_2013_mean = pd.DataFrame({'EID': df_1['EID'].values, 'time_2013_mean': time_2013_mean.values})
# time_2013_min = pd.DataFrame({'EID': df_1['EID'].values, 'time_2013_min': time_2013_min.values})
# time_2013_max = pd.DataFrame({'EID': df_1['EID'].values, 'time_2013_max': time_2013_max.values})
# time_2014_mean = pd.DataFrame({'EID': df_1['EID'].values, 'time_2014_mean': time_2014_mean.values})
# time_2014_min = pd.DataFrame({'EID': df_1['EID'].values, 'time_2014_min': time_2014_min.values})
# time_2014_max = pd.DataFrame({'EID': df_1['EID'].values, 'time_2014_max': time_2014_max.values})
# time_2015_mean = pd.DataFrame({'EID': df_1['EID'].values, 'time_2015_mean': time_2015_mean.values})
# time_2015_min = pd.DataFrame({'EID': df_1['EID'].values, 'time_2015_min': time_2015_min.values})
# time_2015_max = pd.DataFrame({'EID': df_1['EID'].values, 'time_2015_max': time_2015_max.values})

first_law_year = pd.DataFrame({'EID': df_1['EID'].values, '9first_year': first_law_year.values})
last_law_year = pd.DataFrame({'EID': df_1['EID'].values, '9last_year': last_law_year.values})
first_law_time = pd.DataFrame({'EID': df_1['EID'].values, '9first_time': first_law_time.values})
last_law_time = pd.DataFrame({'EID': df_1['EID'].values, '9last_time': last_law_time.values})
#
df_new = pd.merge(data_9_new, first_law_year, on='EID', how='left')
df_new = pd.merge(df_new, last_law_year, on='EID', how='left')
df_new = pd.merge(df_new, first_law_time, on='EID', how='left')
df_new = pd.merge(df_new, last_law_time, on='EID', how='left')
#
df_new = pd.merge(df_new, df_mean_alter_interval, on='EID', how='left')
df_new = pd.merge(df_new, df_max_alter_interval, on='EID', how='left')
df_new = pd.merge(df_new, df_min_alter_interval, on='EID', how='left')

df_new = pd.merge(df_new, wz1_time_mean, on='EID', how='left')
df_new = pd.merge(df_new, wz1_time_min, on='EID', how='left')
df_new = pd.merge(df_new, wz1_time_max, on='EID', how='left')
df_new = pd.merge(df_new, wz2_time_mean, on='EID', how='left')
df_new = pd.merge(df_new, wz2_time_min, on='EID', how='left')
df_new = pd.merge(df_new, wz2_time_max, on='EID', how='left')
df_new = pd.merge(df_new, wz3_time_mean, on='EID', how='left')
df_new = pd.merge(df_new, wz3_time_min, on='EID', how='left')
df_new = pd.merge(df_new, wz3_time_max, on='EID', how='left')
#
df_new = pd.merge(df_new, wz1_num_mean, on='EID', how='left')
df_new = pd.merge(df_new, wz1_num_min, on='EID', how='left')
df_new = pd.merge(df_new, wz1_num_max, on='EID', how='left')
df_new = pd.merge(df_new, wz2_num_mean, on='EID', how='left')
df_new = pd.merge(df_new, wz2_num_min, on='EID', how='left')
df_new = pd.merge(df_new, wz2_num_max, on='EID', how='left')
df_new = pd.merge(df_new, wz3_num_mean, on='EID', how='left')
df_new = pd.merge(df_new, wz3_num_min, on='EID', how='left')
df_new = pd.merge(df_new, wz3_num_max, on='EID', how='left')

# df_new = pd.merge(df_new, num_2008_mean, on='EID', how='left')
# df_new = pd.merge(df_new, num_2008_min, on='EID', how='left')
# df_new = pd.merge(df_new, num_2008_max, on='EID', how='left')
# df_new = pd.merge(df_new, num_2012_mean, on='EID', how='left')
# df_new = pd.merge(df_new, num_2012_min, on='EID', how='left')
# df_new = pd.merge(df_new, num_2012_max, on='EID', how='left')
# df_new = pd.merge(df_new, num_2013_mean, on='EID', how='left')
# df_new = pd.merge(df_new, num_2013_min, on='EID', how='left')
# df_new = pd.merge(df_new, num_2013_max, on='EID', how='left')
# df_new = pd.merge(df_new, num_2014_mean, on='EID', how='left')
# df_new = pd.merge(df_new, num_2014_min, on='EID', how='left')
# df_new = pd.merge(df_new, num_2014_max, on='EID', how='left')
# df_new = pd.merge(df_new, num_2015_mean, on='EID', how='left')
# df_new = pd.merge(df_new, num_2015_min, on='EID', how='left')
# df_new = pd.merge(df_new, num_2015_max, on='EID', how='left')

# df_new = pd.merge(df_new, time_2008_mean, on='EID', how='left')
# df_new = pd.merge(df_new, time_2008_min, on='EID', how='left')
# df_new = pd.merge(df_new, time_2008_max, on='EID', how='left')
# df_new = pd.merge(df_new, time_2012_mean, on='EID', how='left')
# df_new = pd.merge(df_new, time_2012_min, on='EID', how='left')
# df_new = pd.merge(df_new, time_2012_max, on='EID', how='left')
# df_new = pd.merge(df_new, time_2013_mean, on='EID', how='left')
# df_new = pd.merge(df_new, time_2013_min, on='EID', how='left')
# df_new = pd.merge(df_new, time_2013_max, on='EID', how='left')
# df_new = pd.merge(df_new, time_2014_mean, on='EID', how='left')
# df_new = pd.merge(df_new, time_2014_min, on='EID', how='left')
# df_new = pd.merge(df_new, time_2014_max, on='EID', how='left')
# df_new = pd.merge(df_new, time_2015_mean, on='EID', how='left')
# df_new = pd.merge(df_new, time_2015_min, on='EID', how='left')
# df_new = pd.merge(df_new, time_2015_max, on='EID', how='left')
#
df_new['9rec_avg_year'] = df_new['PNUM'] / np.floor(df_new['9last_year'] - df_new['9first_year'] + 1)
df_new['9time_avg_year'] = df_new['count'] / np.floor(df_new['9last_year'] - df_new['9first_year'] + 1)

df_max_year_alter_time = df_2.groupby(['EID', 'REYEAR'], sort=False)['PNUM'].sum()
df_max_year_alter_time = df_max_year_alter_time.groupby(level=0).max()
df_min_year_alter_time = df_2.groupby(['EID', 'REYEAR'], sort=False)['PNUM'].sum()
df_min_year_alter_time = df_min_year_alter_time.groupby(level=0).min()
df_max_year_alter_time = pd.DataFrame({'EID':df_new['EID'].values, '9pnum_max_year': df_max_year_alter_time.values})
df_min_year_alter_time = pd.DataFrame({'EID':df_new['EID'].values, '9pnum_min_year': df_min_year_alter_time.values})
df_new = pd.merge(df_new, df_max_year_alter_time, how='left', on='EID')
df_new = pd.merge(df_new, df_min_year_alter_time, how='left', on='EID')

df_max_year_alter_time = df_2.groupby(['EID', 'REYEAR'], sort=False)['count'].sum()
df_max_year_alter_time = df_max_year_alter_time.groupby(level=0).max()
df_min_year_alter_time = df_2.groupby(['EID', 'REYEAR'], sort=False)['count'].sum()
df_min_year_alter_time = df_min_year_alter_time.groupby(level=0).min()
df_max_year_alter_time = pd.DataFrame({'EID':df_new['EID'].values, '9count_max_year': df_max_year_alter_time.values})
df_min_year_alter_time = pd.DataFrame({'EID':df_new['EID'].values, '9count_min_year': df_min_year_alter_time.values})
df_new = pd.merge(df_new, df_max_year_alter_time, how='left', on='EID')
df_new = pd.merge(df_new, df_min_year_alter_time, how='left', on='EID')

df_new['9last_minus_first'] = df_new['9last_time'] - df_new['9first_time']
df_new['9now_minus_last'] = 2015+(7/12) - df_new['9last_time']
df_new['9now_minus_first'] = 2015+(7/12) - df_new['9first_time']
df_new['9rec_avg_wz'] = df_new['PNUM'] / df_new['wz_lei_count']
df_new['9time_avg_wz'] = df_new['count'] / df_new['wz_lei_count']
df_new['9num_avg_time'] = df_new['PNUM'] / df_new['count']

# print(df_new)
df_new.to_csv('..\\data\\9recruit_add_new.csv', index=False)
