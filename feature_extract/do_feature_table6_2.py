import pandas as pd


datafile6 = '..\\data\\6project.csv'
data_6 = pd.read_csv(datafile6)

data_6['PROCOUNT'] = 1
data_6['BS_PROCOUNT'] = data_6['IFHOME']
data_6['WS_PROCOUNT'] = data_6['IFHOME'].apply(lambda x: 1 if x==0 else 0)
data_6['DJDATE'] = pd.to_datetime(data_6['DJDATE'], format='%Y/%m/%d')
data_6['DJYEAR_Y'] = data_6['DJDATE'].apply(lambda x: x.year)
data_6['DJTIME'] = data_6['DJDATE'].apply(lambda x: x.year + (x.month - 1) / 12)
data_6_1 = data_6

data_6 = pd.concat([data_6, pd.get_dummies(data_6['DJYEAR_Y'], prefix='DJYEAR')], axis=1)
# print(data_6)
data_6_new = data_6.groupby('EID', sort=False).sum()
data_6_new = data_6_new.reset_index()
print(data_6_new)
data_6_new['BS_RATE'] = data_6_new['BS_PROCOUNT']/data_6_new['PROCOUNT']
data_6_new['WS_RATE'] = data_6_new['WS_PROCOUNT']/data_6_new['PROCOUNT']
data_6_new = data_6_new.drop(['TYPECODE','IFHOME', 'DJTIME', 'DJYEAR_Y'], axis=1)

data_6 = data_6_1
first_pro_year = data_6.groupby('EID', sort=False)['DJYEAR_Y'].min()
last_pro_year = data_6.groupby('EID', sort=False)['DJYEAR_Y'].max()
first_pro_time = data_6.groupby('EID', sort=False)['DJTIME'].min()
last_pro_time = data_6.groupby('EID', sort=False)['DJTIME'].max()
data_6 = data_6.drop_duplicates('EID')
first_pro_year = pd.DataFrame({'EID': data_6['EID'].values, '6first_pro_year': first_pro_year.values})
last_pro_year = pd.DataFrame({'EID': data_6['EID'].values, '6last_pro_year': last_pro_year.values})
first_pro_time = pd.DataFrame({'EID': data_6['EID'].values, '6first_pro_time': first_pro_time.values})
last_pro_time = pd.DataFrame({'EID': data_6['EID'].values, '6last_pro_time': last_pro_time.values})

data_6_new = pd.merge(data_6_new, first_pro_year, on='EID', how='left')
data_6_new = pd.merge(data_6_new, last_pro_year, on='EID', how='left')
data_6_new = pd.merge(data_6_new, first_pro_time, on='EID', how='left')
data_6_new = pd.merge(data_6_new, last_pro_time, on='EID', how='left')

data_6_new['6year_count'] = data_6_new['DJYEAR_2013'].apply(lambda x: 1 if x>0 else 0) + \
                            data_6_new['DJYEAR_2014'].apply(lambda x: 1 if x>0 else 0) + \
                            data_6_new['DJYEAR_2015'].apply(lambda x: 1 if x>0 else 0)

data_6_new['6last_minus_first'] = data_6_new['6last_pro_time'] - data_6_new['6first_pro_time']
data_6_new['6now_minus_first'] = 2015+(7/12) - data_6_new['6first_pro_time']
data_6_new['6now_minus_last'] = 2015+(7/12) - data_6_new['6last_pro_time']

data_6_new['pro_year_avg'] = data_6_new['PROCOUNT'] / (data_6_new['6last_pro_year'] - data_6_new['6first_pro_year'] + 1)
max_pro_year = data_6_1.groupby(['EID', 'DJYEAR_Y'], sort=False)['PROCOUNT'].sum()
max_pro_year = max_pro_year.groupby(level=0).max()
min_pro_year = data_6_1.groupby(['EID', 'DJYEAR_Y'], sort=False)['PROCOUNT'].sum()
min_pro_year = min_pro_year.groupby(level=0).min()
max_pro_year = pd.DataFrame({'EID': data_6_new['EID'].values, '6max_pro_year': max_pro_year.values})
min_pro_year = pd.DataFrame({'EID': data_6_new['EID'].values, '6min_pro_year': min_pro_year.values})
data_6_new = pd.merge(data_6_new, max_pro_year, on="EID", how='left')
data_6_new = pd.merge(data_6_new, min_pro_year, on="EID", how='left')

def cal_max_interval(arr):
    arr = arr.values
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
    arr = arr.values
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
    arr = arr.values
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
df_alter_interval = data_6_1['DJTIME'].groupby(data_6_1['EID'], sort=False)
df_max_alter_interval = df_alter_interval.agg(cal_max_interval)
print('df_max_alter_interval:\n', df_max_alter_interval)
df_min_alter_interval = df_alter_interval.agg(cal_min_interval)
print('df_min_alter_interval:\n', df_min_alter_interval)
df_mean_alter_interval = df_alter_interval.agg(cal_mean_interval)
print('df_mean_alter_interval:\n', df_mean_alter_interval)

df_mean_alter_interval = pd.DataFrame({'EID': data_6_new['EID'].values, '6df_mean_alter_interval': df_mean_alter_interval.values})
df_max_alter_interval = pd.DataFrame({'EID': data_6_new['EID'].values, '6df_max_alter_interval': df_max_alter_interval.values})
df_min_alter_interval = pd.DataFrame({'EID': data_6_new['EID'].values, '6df_min_alter_interval': df_min_alter_interval.values})

data_6_new = pd.merge(data_6_new, df_mean_alter_interval, on='EID', how='left')
data_6_new = pd.merge(data_6_new, df_max_alter_interval, on='EID', how='left')
data_6_new = pd.merge(data_6_new, df_min_alter_interval, on='EID', how='left')

data_6_new.to_csv('..\\data\\6project_add_new.csv', index=False)
