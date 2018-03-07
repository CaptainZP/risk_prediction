import pandas as pd


df1 = pd.read_csv("..\\data\\3branch_add.csv")
df = pd.read_csv("..\\data\\3branch.csv")

# 增加最大最小平均分支成立间隔
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
df_br_interval = df['B_REYEAR'].groupby(df['EID'], sort=False)
df_max_br_interval = df_br_interval.agg(cal_max_interval)
df_min_br_interval = df_br_interval.agg(cal_min_interval)
df_mean_br_interval = df_br_interval.agg(cal_mean_interval)

# 增加最大最小年分支成立数（最小可能没有意义）
df['br_start_time'] = 1
df_year_start_time = df.groupby(['EID', 'B_REYEAR'], sort=False)['br_start_time'].sum()
df_max_year_starttime = df_year_start_time.groupby(level=0).max()
df_min_year_starttime = df_year_start_time.groupby(level=0).min()

# 增加最大最小年分支关停次数（最小可能没有意义）
df['br_end_time'] = df['B_ENDYEAR'].apply(lambda x: 1 if x > 0 else 0)
df['B_ENDYEAR'] = df['B_ENDYEAR'].fillna(2015)
df_year_end_time = df.groupby(['EID', 'B_ENDYEAR'], sort=False)['br_end_time'].sum()
df_max_year_endtime = df_year_end_time.groupby(level=0).max()
df_min_year_endtime = df_year_end_time.groupby(level=0).min()

# 合并
df_max_br_interval = pd.DataFrame({'EID': df1['EID'].values, '3max_br_interval': df_max_br_interval.values})
df1 = pd.merge(df1, df_max_br_interval, how='left', on='EID')
df_min_br_interval = pd.DataFrame({'EID': df1['EID'].values, '3min_br_interval': df_min_br_interval.values})
df1 = pd.merge(df1, df_min_br_interval, how='left', on='EID')
df_mean_br_interval = pd.DataFrame({'EID': df1['EID'].values, '3mean_br_interval': df_mean_br_interval.values})
df1 = pd.merge(df1, df_mean_br_interval, how='left', on='EID')

df_max_br_startnum = pd.DataFrame({'EID': df1['EID'].values, '3max_br_startnum': df_max_year_starttime.values})
df1 = pd.merge(df1, df_max_br_startnum, how='left', on='EID')
df_min_br_startnum = pd.DataFrame({'EID': df1['EID'].values, '3min_br_startnum': df_min_year_starttime.values})
df1 = pd.merge(df1, df_min_br_startnum, how='left', on='EID')

df_max_br_endnum = pd.DataFrame({'EID': df1['EID'].values, '3max_br_endnum': df_max_year_endtime.values})  # 可能有EID没有end
df1 = pd.merge(df1, df_max_br_endnum, how='left', on='EID')
df_min_br_endnum = pd.DataFrame({'EID': df1['EID'].values, '3min_br_endnum': df_min_year_endtime.values})
df1 = pd.merge(df1, df_min_br_endnum, how='left', on='EID')

# 最后关停-首次开始
df1['3lastend_firststart'] = df1['3last_end_year'] - df1['3first_br_year']
# 最后关停-最后开始
df1['3lastend_laststart'] = df1['3last_end_year'] - df1['3last_br_year']
# 最后关停-首次关停
df1['3lastend_firstend'] = df1['3last_end_year'] - df1['3first_end_year']
# 最后开始-首次关停
df1['3laststart_firstend'] = df1['3last_br_year'] - df1['3first_end_year']

# 统计-首次关停
df1['3now_firstend'] = 2015 + 7/12
df1['3now_firstend'] = df1['3now_firstend'] - df1['3first_end_year']
# 统计-首次开始
df1['3now_firststart'] = 2015 + 7/12
df1['3now_firststart'] = df1['3now_firststart'] - df1['3first_br_year']

df1.to_csv('..\\data\\3branch_add_new.csv', index=False)
