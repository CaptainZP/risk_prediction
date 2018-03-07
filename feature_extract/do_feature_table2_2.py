import pandas as pd
import numpy as np

df1 = pd.read_csv("..\\data\\2alter_add.csv")
df = pd.read_csv("..\\data\\2alter.csv")

# 增加最大最小资金差、资金差方差(存在争议，只有资金变更2次以上才有)
df['found_diff'] = df['ALTAF'] - df['ALTBE']
df_max_found_diff = df['found_diff'].groupby(df['EID'], sort=False).max()
df_min_found_diff = df['found_diff'].groupby(df['EID'], sort=False).min()
df_found_variance = df['found_diff'].groupby(df['EID'], sort=False).var()

# 增加年最大最小变更次数
df['ALTDATE'] = pd.to_datetime(df['ALTDATE'], format='%Y/%m/%d')
df['ALTYEAR'] = df['ALTDATE'].apply(lambda x: x.year)
df['alter_time'] = 1
df_year_alter_time = df.groupby(['EID', 'ALTYEAR'], sort=False)['alter_time'].sum()
df_max_year_altertime = df_year_alter_time.groupby(level=0).max()
df_min_year_altertime = df_year_alter_time.groupby(level=0).min()

# 增加年最大最小资金变更次数
df['found_change_number'] = df['ALTERNO'].apply(lambda x: 1 if x == 5 or x == 27 else 0)
df_year_found_change_number = df.groupby(['EID', 'ALTYEAR'], sort=False)['found_change_number'].sum()
df_max_year_found_change_number = df_year_found_change_number.groupby(level=0).max()
df_min_year_found_change_number = df_year_found_change_number.groupby(level=0).min()

# 增加非资金变更次数
df['not_found_change_number'] = df['ALTERNO'].apply(lambda x: 0 if x == 5 or x == 27 else 1)
df_not_found_change_number = df.groupby('EID', sort=False)['not_found_change_number'].sum()

# 增加年最大最小非资金变更次数
df_year_not_found_change_number = df.groupby(['EID', 'ALTYEAR'], sort=False)['not_found_change_number'].sum()
df_max_year_not_found_change_number = df_year_not_found_change_number.groupby(level=0).max()
df_min_year_not_found_change_number = df_year_found_change_number.groupby(level=0).min()

# 增加最大最小平均资金变更间隔
def cal_max_interval(arr):
    arr = arr.sort_values().values
    max_interval = 0
    for i in range(0, len(arr)):
        if 0 < i < len(arr):
            temp_interval = round(abs(int(arr[i] - arr[i-1]))/(10**9*60*60*24*30), 2)
            # print(temp_interval)
            if temp_interval > max_interval:
                max_interval = temp_interval
    return max_interval
def cal_min_interval(arr):
    arr = arr.sort_values().values
    min_interval = 999
    if len(arr) == 1:
        min_interval = 0
    else:
        for i in range(0, len(arr)):
            if 0 < i < len(arr):
                temp_interval = round(abs(int(arr[i] - arr[i-1]))/(10**9*60*60*24*30), 2)
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
                temp_interval = round(abs(int(arr[i] - arr[i-1]))/(10**9*60*60*24*30), 2)
                mean_interval = mean_interval + temp_interval
        mean_interval = round(mean_interval/(len(arr)-1), 2)
        return mean_interval
df['ALTTIME'] = pd.to_datetime(df['ALTDATE'], format='%Y/%m/%d')
df_alter_interval = df['ALTTIME'].groupby(df['EID'], sort=False)
df_max_alter_interval = df_alter_interval.agg(cal_max_interval)
df_min_alter_interval = df_alter_interval.agg(cal_min_interval)
df_mean_alter_interval = df_alter_interval.agg(cal_mean_interval)

# 有几类变更
df_alterno_typenum = df[['EID', 'ALTERNO']]
df_alterno_typenum = df_alterno_typenum.drop_duplicates(subset=['EID', 'ALTERNO'])
df_alterno_typenum['ALTERNO'] = 1
df_num_of_alter = df_alterno_typenum.groupby('EID', sort=False).sum()
df_num_of_alter = df_num_of_alter.reset_index()  # dataframe

# 合并,变化的是df1
max_found_diff = pd.DataFrame({'EID': df1['EID'].values, '2max_found_diff': df_max_found_diff.values})
min_found_diff = pd.DataFrame({'EID': df1['EID'].values, '2min_found_diff': df_min_found_diff.values})
found_variance = pd.DataFrame({'EID': df1['EID'].values, '2found_variance': df_found_variance})
df1 = pd.merge(df1, max_found_diff, how='left', on='EID')
df1 = pd.merge(df1, min_found_diff, how='left', on='EID')
df1 = pd.merge(df1, found_variance, how='left', on='EID')

max_year_altertime = pd.DataFrame({'EID': df1['EID'].values, '2max_year_altertime': df_max_year_altertime.values})
min_year_altertime = pd.DataFrame({'EID': df1['EID'].values, '2min_year_altertime': df_min_year_altertime.values})
df1 = pd.merge(df1, max_year_altertime, how='left', on='EID')
df1 = pd.merge(df1, min_year_altertime, how='left', on='EID')

max_year_found_change_number = pd.DataFrame({'EID': df1['EID'].values, '2max_year_found_change_number': df_max_year_found_change_number.values})
min_year_found_change_number = pd.DataFrame({'EID': df1['EID'].values, '2min_year_found_change_number': df_min_year_found_change_number.values})
df1 = pd.merge(df1, max_year_found_change_number, how='left', on='EID')
df1 = pd.merge(df1, min_year_found_change_number, how='left', on='EID')

not_found_change_number = pd.DataFrame({'EID': df1['EID'].values, '2not_found_change_number': df_not_found_change_number.values})
df1 = pd.merge(df1, not_found_change_number, how='left', on='EID')

max_year_not_found_change_number = pd.DataFrame({'EID': df1['EID'].values, '2max_year_not_found_change_number': df_max_year_not_found_change_number.values})
min_year_not_found_change_number = pd.DataFrame({'EID': df1['EID'].values, '2min_year_not_found_change_number': df_min_year_not_found_change_number.values})
df1 = pd.merge(df1, max_year_not_found_change_number, how='left', on='EID')
df1 = pd.merge(df1, min_year_not_found_change_number, how='left', on='EID')

df_max_alter_interval = pd.DataFrame({'EID': df1['EID'].values, '2max_alter_interval': df_max_alter_interval.values})
df1 = pd.merge(df1, df_max_alter_interval, how='left', on='EID')
df_min_alter_interval = pd.DataFrame({'EID': df1['EID'].values, '2min_alter_interval': df_min_alter_interval.values})
df1 = pd.merge(df1, df_min_alter_interval, how='left', on='EID')
df_mean_alter_interval = pd.DataFrame({'EID': df1['EID'].values, '2mean_alter_interval': df_mean_alter_interval.values})
df1 = pd.merge(df1, df_mean_alter_interval, how='left', on='EID')

df1 = pd.merge(df1, df_num_of_alter, how='left', on='EID')

# 增加平均每年的非资金变更次数
df1['2ave_year_not_found_change_number'] = df1['2not_found_change_number']/(df1['last_alter_year']-df1['first_alter_year']+1)

# 增加平均资金变更前资本、平均资金变更后资本、资金差方差(前面)
df1['found_change_number'] = df1['found_change_number'].apply(lambda x: np.nan if x == 0 else x)
df1['2ave_ALTBE'] = df1['ALTBE']/df1['found_change_number']
df1['2ave_ALTAF'] = df1['ALTAF']/df1['found_change_number']

# 增加统计时间-第一次变更
df1['2statis_firstalter_diff'] = 2015 + 7/12
df1['2statis_firstalter_diff'] = df1['2statis_firstalter_diff'] - df1['first_alter_time']

# 增加是否每种类型变更都存在（存在争议）
df1['2if_ALTERNO1_exist'] = df1['ALTERNO_1'].apply(lambda x: 1 if x > 0 else 0)
df1['2if_ALTERNO2_exist'] = df1['ALTERNO_2'].apply(lambda x: 1 if x > 0 else 0)
df1['2if_ALTERNO3_exist'] = df1['ALTERNO_3'].apply(lambda x: 1 if x > 0 else 0)
df1['2if_ALTERNO4_exist'] = df1['ALTERNO_4'].apply(lambda x: 1 if x > 0 else 0)
df1['2if_ALTERNO5_exist'] = df1['ALTERNO_5'].apply(lambda x: 1 if x > 0 else 0)
df1['2if_ALTERNO10_exist'] = df1['ALTERNO_10'].apply(lambda x: 1 if x > 0 else 0)
df1['2if_ALTERNO12_exist'] = df1['ALTERNO_12'].apply(lambda x: 1 if x > 0 else 0)
df1['2if_ALTERNO13_exist'] = df1['ALTERNO_13'].apply(lambda x: 1 if x > 0 else 0)
df1['2if_ALTERNO14_exist'] = df1['ALTERNO_14'].apply(lambda x: 1 if x > 0 else 0)
df1['2if_ALTERNO15_exist'] = df1['ALTERNO_15'].apply(lambda x: 1 if x > 0 else 0)
df1['2if_ALTERNO27_exist'] = df1['ALTERNO_27'].apply(lambda x: 1 if x > 0 else 0)
df1['2if_ALTERNO99_exist'] = df1['ALTERNO_99'].apply(lambda x: 1 if x > 0 else 0)

df1.to_csv('..\\data\\2alter_add_new.csv', index=False)

