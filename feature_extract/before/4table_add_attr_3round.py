import pandas as pd


df = pd.read_csv("..\\data\\4invest.csv")

df_first_set_time = df.groupby('EID', sort=False)['BTYEAR'].min()
df_last_set_time = df.groupby('EID', sort=False)['BTYEAR'].max()

df_first_end_time = df.groupby('EID', sort=False)['BTENDYEAR'].min()
df_last_end_time = df.groupby('EID', sort=False)['BTENDYEAR'].max()

# 增加第一次、最后一次成立投资年份
df = df.drop_duplicates('EID')
first_set_time = pd.DataFrame({'EID': df['EID'].values, '4first_set_time': df_first_set_time.values})  # EID顺序要一致
last_set_time = pd.DataFrame({'EID': df['EID'].values, '4last_set_time': df_last_set_time.values})

# 增加第一次、最后一次关闭投资年份
first_end_time = pd.DataFrame({'EID': df['EID'].values, '4first_end_time': df_first_end_time.values})  # EID顺序要一致
last_end_time = pd.DataFrame({'EID': df['EID'].values, '4last_end_time': df_last_end_time.values})

# merge
df2 = pd.read_csv("..\\data\\4invest_add_new.csv")
df2 = pd.merge(df2, first_set_time, how='left', on='EID')
df2 = pd.merge(df2, last_set_time, how='left', on='EID')
df2 = pd.merge(df2, first_end_time, how='left', on='EID')
df2 = pd.merge(df2, last_end_time, how='left', on='EID')

# 增加最后一次投资时间 - 第一次投资
df2['4set_time_diff'] = df2['4last_set_time'] - df2['4first_set_time']

# 增加统计年份 - 最后一次投资时间
df2['4set_stat_diff'] = 2015
df2['4set_stat_diff'] = df2['4set_stat_diff'] - df2['4last_set_time']

#  增加第一次关停年份 - 第一次投资年份
df2['4set_1stend_diff'] = df2['4first_end_time'] - df2['4first_set_time']

#  增加最后一次关停年份 - 第一次投资年份
df2['4set_lastend_diff'] = df2['4last_end_time'] - df2['4first_set_time']

# 增加统计年份 - 最后一次关闭时间
df2['4end_stat_diff'] = 2015
df2['4end_stat_diff'] = df2['4end_stat_diff'] - df2['4last_end_time']

# 增加最后一次关闭时间 - 第一次关闭成立
df2['4end_time_diff'] = df2['4last_end_time'] - df2['4first_end_time']

# 增加平均每年成立次数、平均每年倒闭次数
df2['ave_BTCOUNT'] = df2['BTCOUNT']/(df2['4set_time_diff'] + 1)
df2['ave_BT_END_COUNT'] = df2['BT_END_COUNT']/(df2['4set_time_diff'] + 1)

print(df2)
df2.to_csv('..\\data\\4invest_add_new3.csv', index=False)

