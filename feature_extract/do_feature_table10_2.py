import pandas as pd
import re
import numpy as np

datafile10 = '..\\10qualification.csv'
df = pd.read_csv(datafile10)

df['ADDCOUNT'] = 1
df['BEGINDATE'] = df['BEGINDATE'].apply(lambda x: re.findall(r"\d+\d*", str(x)))
df['EXPIRYDATE'] = df['EXPIRYDATE'].apply(lambda x: np.nan if x is np.nan else re.findall(r"\d+\d*", str(x)))
df['BEGINYEAR'] = df['BEGINDATE'].apply(lambda x: int(x[0]))
df['BEGINTIME'] = df['BEGINDATE'].apply(lambda x: int(x[0]) + (int(x[1]) - 1) / 12)
print(df.head())
df['EXPIRYYEAR'] = df['EXPIRYDATE'].apply(lambda x: int(x[0]) if x is not np.nan else np.nan)
df['EXPIRYTIME'] = df['EXPIRYDATE'].apply(lambda x: int(x[0]) + (int(x[1]) - 1) / 12 if x is not np.nan else np.nan)
df['HOLD_TIME'] = df['EXPIRYTIME'] - df['BEGINTIME']
df['EXPEND'] = df['EXPIRYTIME'].apply(lambda x: 1 if x<=(2015+7/12) else 0)
df['EXPIN'] = df['EXPIRYTIME'].apply(lambda x: 1 if x>=(2015+7/12) else 0)
df_2 = df
df = pd.concat([df, pd.get_dummies(df['ADDTYPE'], prefix='TYPE')], axis=1)
df = pd.concat([df, pd.get_dummies(df['BEGINYEAR'], prefix='BEGINYEAR')], axis=1)
df_1 = df

df = df.groupby('EID', sort=False).sum()
df = df.reset_index()
df = df.drop(['ADDTYPE', 'BEGINTIME', 'EXPIRYTIME', 'BEGINYEAR', 'EXPIRYYEAR'], axis=1)

max_hold_time = df_1.groupby('EID', sort=False)['HOLD_TIME'].max()
min_hold_time = df_1.groupby('EID', sort=False)['HOLD_TIME'].min()
mean_hold_time = df_1.groupby('EID', sort=False)['HOLD_TIME'].mean()

first_law_year = df_1.groupby('EID', sort=False)['BEGINYEAR'].min()
last_law_year = df_1.groupby('EID', sort=False)['BEGINYEAR'].max()
first_law_time = df_1.groupby('EID', sort=False)['BEGINTIME'].min()
last_law_time = df_1.groupby('EID', sort=False)['BEGINTIME'].max()
first_end_year = df_1.groupby('EID', sort=False)['EXPIRYYEAR'].min()
last_end_year = df_1.groupby('EID', sort=False)['EXPIRYYEAR'].max()
first_end_time = df_1.groupby('EID', sort=False)['EXPIRYTIME'].min()
last_end_time = df_1.groupby('EID', sort=False)['EXPIRYTIME'].max()

df_1 = df_1.drop_duplicates('EID')
first_law_year = pd.DataFrame({'EID': df_1['EID'].values, '10first_be_year': first_law_year.values})
last_law_year = pd.DataFrame({'EID': df_1['EID'].values, '10last_be_year': last_law_year.values})
first_law_time = pd.DataFrame({'EID': df_1['EID'].values, '10first_be_time': first_law_time.values})
last_law_time = pd.DataFrame({'EID': df_1['EID'].values, '10last_be_time': last_law_time.values})
first_end_year = pd.DataFrame({'EID': df_1['EID'].values, '10first_end_year': first_end_year.values})
last_end_year = pd.DataFrame({'EID': df_1['EID'].values, '10last_end_year': last_end_year.values})
first_end_time = pd.DataFrame({'EID': df_1['EID'].values, '10first_end_time': first_end_time.values})
last_end_time = pd.DataFrame({'EID': df_1['EID'].values, '10last_end_time': last_end_time.values})

max_hold_time = pd.DataFrame({'EID': df_1['EID'].values, '10max_hold_time': max_hold_time})
min_hold_time = pd.DataFrame({'EID': df_1['EID'].values, '10min_hold_time': min_hold_time})
mean_hold_time = pd.DataFrame({'EID': df_1['EID'].values, '10mean_hold_time': mean_hold_time})

df_new = pd.merge(df, first_law_year, on='EID', how='left')
df_new = pd.merge(df_new, last_law_year, on='EID', how='left')
df_new = pd.merge(df_new, first_law_time, on='EID', how='left')
df_new = pd.merge(df_new, last_law_time, on='EID', how='left')
df_new = pd.merge(df_new, first_end_year, on='EID', how='left')
df_new = pd.merge(df_new, last_end_year, on='EID', how='left')
df_new = pd.merge(df_new, first_end_time, on='EID', how='left')
df_new = pd.merge(df_new, last_end_time, on='EID', how='left')

df_new = pd.merge(df_new, max_hold_time, on='EID', how='left')
df_new = pd.merge(df_new, min_hold_time, on='EID', how='left')
df_new = pd.merge(df_new, mean_hold_time, on='EID', how='left')

df_new['IS_EXIST_END'] = df_new['EXPEND'].apply(lambda x: 1 if x>0 else 0)
df_new['IS_EXIST_IN'] = df_new['EXPIN'].apply(lambda x: 1 if x>0 else 0)

df_new['10last_minus_firstbe'] = df_new['10last_be_time'] - df_new['10first_be_time']
df_new['10first_minus_first'] = df_new['10first_end_time'] - df_new['10first_be_time']
df_new['10now_minus_lastbe'] = 2015+(7/12) - df_new['10last_be_time']
df_new['10now_minus_lastend'] = 2015+(7/12) - df_new['10last_end_time']

df_new['10lastend_minus_firstin'] = df_new['10last_end_time'] - df_new['10first_be_time']
df_new['10now_minus_firstend'] = 2015+(7/12) - df_new['10first_end_time']
df_new['10now_minus_firstin'] = 2015+(7/12) - df_new['10first_be_time']
df_new['10lastend_minus_lastin'] = df_new['10last_end_time'] - df_new['10last_be_time']
df_new['10lastin_minus_firstend'] = df_new['10last_be_time'] - df_new['10first_end_time']
df_new['10lastend_minus_firstend'] = df_new['10last_end_time'] - df_new['10first_end_time']

df_new['10add_count_avg'] = df_new['ADDCOUNT'] / (df_new['10last_be_year'] - df_new['10first_be_year'] + 1)
df_new['10add_count_avg_in'] = df_new['EXPIN'] / (df_new['10last_be_year'] - df_new['10first_be_year'] + 1)
df_new['10add_count_avg_end'] = df_new['EXPEND'] / (df_new['10last_end_year'] - df_new['10first_end_year'] + 1)

# df_new_1 = df_new[['BEGINYEAR_2007','BEGINYEAR_2008', 'BEGINYEAR_2009', 'BEGINYEAR_2010', 'BEGINYEAR_2011', 'BEGINYEAR_2012', 'BEGINYEAR_2013', 'BEGINYEAR_2014', 'BEGINYEAR_2015']]
# df_new_max_year = df_new_1.max(axis=1)
# df_new_min_year = df_new_1.min(axis=1)
# # print(type(df_new_max_year))
# df_new_max_year = pd.DataFrame({'EID':df_new['EID'].values, '10df_new_max_year': df_new_max_year.values})
# df_new_min_year = pd.DataFrame({'EID':df_new['EID'].values, '10df_new_min_year': df_new_min_year.values})
# df_new = pd.merge(df_new, df_new_max_year, how='left', on='EID')
# df_new = pd.merge(df_new, df_new_min_year, how='left', on='EID')
# print(df_new.head())

df_max_year_alter_time = df_2.groupby(['EID', 'BEGINYEAR'], sort=False)['ADDCOUNT'].sum()
df_max_year_alter_time = df_max_year_alter_time.groupby(level=0).max()
df_min_year_alter_time = df_2.groupby(['EID', 'BEGINYEAR'], sort=False)['ADDCOUNT'].sum()
df_min_year_alter_time = df_min_year_alter_time.groupby(level=0).min()
df_max_year_alter_time = pd.DataFrame({'EID':df_new['EID'].values, '10df_new_max_year': df_max_year_alter_time.values})
df_min_year_alter_time = pd.DataFrame({'EID':df_new['EID'].values, '10df_new_min_year': df_min_year_alter_time.values})
df_new = pd.merge(df_new, df_max_year_alter_time, how='left', on='EID')
df_new = pd.merge(df_new, df_min_year_alter_time, how='left', on='EID')

# df_max_year_alter_time = df_2.groupby(['EID', 'BEGINYEAR'], sort=False)['EXPIN'].sum()
# df_max_year_alter_time = df_max_year_alter_time.groupby(level=0).max()
# df_min_year_alter_time = df_2.groupby(['EID', 'BEGINYEAR'], sort=False)['EXPIN'].sum()
# df_min_year_alter_time = df_min_year_alter_time.groupby(level=0).min()
# df_max_year_alter_time = pd.DataFrame({'EID':df_new['EID'].values, '10df_new_max_in_year': df_max_year_alter_time.values})
# df_min_year_alter_time = pd.DataFrame({'EID':df_new['EID'].values, '10df_new_min_in_year': df_min_year_alter_time.values})
# df_new = pd.merge(df_new, df_max_year_alter_time, how='left', on='EID')
# df_new = pd.merge(df_new, df_min_year_alter_time, how='left', on='EID')

df_max_year_alter_time = df_2.groupby(['EID', 'EXPIRYYEAR'], sort=False)['EXPEND'].sum()
df_max_year_alter_time = df_max_year_alter_time.groupby(level=0).max()
df_max_year_alter_time = df_max_year_alter_time.reset_index()
df_min_year_alter_time = df_2.groupby(['EID', 'EXPIRYYEAR'], sort=False)['EXPEND'].sum()
df_min_year_alter_time = df_min_year_alter_time.groupby(level=0).min()
df_min_year_alter_time = df_min_year_alter_time.reset_index()
df_new = pd.merge(df_new, df_max_year_alter_time, how='left', on='EID')
df_new = pd.merge(df_new, df_min_year_alter_time, how='left', on='EID')

df_new['10_eixt_type1'] = df_new['TYPE_1'].apply(lambda x: 1 if x>0 else 0)
df_new['10_eixt_type2'] = df_new['TYPE_2'].apply(lambda x: 1 if x>0 else 0)
df_new['10_eixt_type3'] = df_new['TYPE_3'].apply(lambda x: 1 if x>0 else 0)
df_new['10type_count'] = df_new['10_eixt_type1'] + df_new['10_eixt_type2'] + df_new['10_eixt_type3']

def cal_max_interval(arr):
    arr = arr.sort_values().values
    max_interval = 0
    for i in range(0, len(arr)):
        if 0 < i < len(arr):
            temp_interval = abs(arr[i] - arr[i-1])
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
df_alter_interval = df_2['BEGINTIME'].groupby(df_2['EID'], sort=False)
df_max_alter_interval = df_alter_interval.agg(cal_max_interval)
print('df_max_alter_interval:\n', df_max_alter_interval)
df_min_alter_interval = df_alter_interval.agg(cal_min_interval)
print('df_min_alter_interval:\n', df_min_alter_interval)
df_mean_alter_interval = df_alter_interval.agg(cal_mean_interval)
print('df_mean_alter_interval:\n', df_mean_alter_interval)

df_mean_alter_interval = pd.DataFrame({'EID': df_1['EID'].values, '10df_mean_alter_interval': df_mean_alter_interval.values})
df_max_alter_interval = pd.DataFrame({'EID': df_1['EID'].values, '10df_max_alter_interval': df_max_alter_interval.values})
df_min_alter_interval = pd.DataFrame({'EID': df_1['EID'].values, '10df_min_alter_interval': df_min_alter_interval.values})

df_new = pd.merge(df_new, df_mean_alter_interval, on='EID', how='left')
df_new = pd.merge(df_new, df_max_alter_interval, on='EID', how='left')
df_new = pd.merge(df_new, df_min_alter_interval, on='EID', how='left')

print(df_new.head())
df_new.to_csv('..\\data\\10qualification_add_new.csv', index=False)