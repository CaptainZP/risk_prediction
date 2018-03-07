import pandas as pd


df1 = pd.read_csv("..\\data\\4invest_add.csv")
df = pd.read_csv("..\\data\\4invest.csv")

# 增加最大最小平均投资间隔
def cal_max_interval(arr):
    arr = arr.sort_values().values
    max_interval = 0
    for i in range(0, len(arr)):
        if 0 < i < len(arr):
            temp_interval = round(abs((arr[i] - arr[i-1])), 2)
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
                temp_interval = round(abs((arr[i] - arr[i-1])), 2)
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
                temp_interval = round(abs((arr[i] - arr[i-1])), 2)
                mean_interval = mean_interval + temp_interval
        mean_interval = round(mean_interval/(len(arr)-1), 2)
        return mean_interval
df_bt_interval = df['BTYEAR'].groupby(df['EID'], sort=False)
df_max_bt_interval = df_bt_interval.agg(cal_max_interval)
# print('df_max_bt_interval:\n', df_max_bt_interval)
df_min_bt_interval = df_bt_interval.agg(cal_min_interval)
# print('df_min_bt_interval:\n', df_min_bt_interval)
df_mean_bt_interval = df_bt_interval.agg(cal_mean_interval)
# print('df_mean_bt_interval:\n', df_mean_bt_interval)

# 增加最大最小年投资数（最小可能没有意义）
df['bt_start_time'] = 1
df_year_start_time = df.groupby(['EID', 'BTYEAR'], sort=False)['bt_start_time'].sum()
df_max_year_starttime = df_year_start_time.groupby(level=0).max()
df_min_year_starttime = df_year_start_time.groupby(level=0).min()

# 增加最大最小年投资关停次数（最小可能没有意义）
df['bt_end_time'] = df['BTENDYEAR'].apply(lambda x: 1 if x > 0 else 0)
df['BTENDYEAR'] = df['BTENDYEAR'].fillna(2015)
df_year_end_time = df.groupby(['EID', 'BTENDYEAR'], sort=False)['bt_end_time'].sum()
df_max_year_endtime = df_year_end_time.groupby(level=0).max()
df_min_year_endtime = df_year_end_time.groupby(level=0).min()
# print(df_min_year_endtime)

# 合并
df_max_bt_interval = pd.DataFrame({'EID': df1['EID'].values, '4max_bt_interval': df_max_bt_interval.values})
df1 = pd.merge(df1, df_max_bt_interval, how='left', on='EID')
df_min_bt_interval = pd.DataFrame({'EID': df1['EID'].values, '4min_bt_interval': df_min_bt_interval.values})
df1 = pd.merge(df1, df_min_bt_interval, how='left', on='EID')
df_mean_bt_interval = pd.DataFrame({'EID': df1['EID'].values, '4mean_bt_interval': df_mean_bt_interval.values})
df1 = pd.merge(df1, df_mean_bt_interval, how='left', on='EID')

df_max_bt_startnum = pd.DataFrame({'EID': df1['EID'].values, '4max_bt_startnum': df_max_year_starttime.values})
df1 = pd.merge(df1, df_max_bt_startnum, how='left', on='EID')
df_min_bt_startnum = pd.DataFrame({'EID': df1['EID'].values, '4min_bt_startnum': df_min_year_starttime.values})
df1 = pd.merge(df1, df_min_bt_startnum, how='left', on='EID')

df_max_bt_endnum = pd.DataFrame({'EID': df1['EID'].values, '4max_bt_endnum': df_max_year_endtime.values})  # 可能有EID没有end
df1 = pd.merge(df1, df_max_bt_endnum, how='left', on='EID')
df_min_bt_endnum = pd.DataFrame({'EID': df1['EID'].values, '4min_bt_endnum': df_min_year_endtime.values})
df1 = pd.merge(df1, df_min_bt_endnum, how='left', on='EID')


# 首次倒闭-首次投资
df1['4firstend_firststart'] = df1['4first_end_year'] - df1['4first_bt_year']
# 最后倒闭-首次投资
df1['4lastend_firststart'] = df1['4last_end_year'] - df1['4first_bt_year']
# 最后倒闭-最后投资
df1['4lastend_laststart'] = df1['4last_end_year'] - df1['4last_bt_year']
# 最后倒闭-首次倒闭
df1['4lastend_firstend'] = df1['4last_end_year'] - df1['4first_end_year']
# 最后投资-首次倒闭
df1['4laststart_firstend'] = df1['4last_bt_year'] - df1['4first_end_year']
# 统计-首次倒闭
df1['4now_firstend'] = 2015 + 7/12
df1['4now_firstend'] = df1['4now_firstend'] - df1['4first_end_year']
# 统计-首次投资
df1['4now_firststart'] = 2015 + 7/12
df1['4now_firststart'] = df1['4now_firststart'] - df1['4first_bt_year']

df1.to_csv('..\\data\\4invest_add_new.csv', index=False)
