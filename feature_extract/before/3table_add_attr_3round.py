import pandas as pd


df = pd.read_csv("..\\data\\3branch.csv")

df_first_set_time = df.groupby('EID', sort=False)['B_REYEAR'].min()
df_last_set_time = df.groupby('EID', sort=False)['B_REYEAR'].max()

df_first_end_time = df.groupby('EID', sort=False)['B_ENDYEAR'].min()
df_last_end_time = df.groupby('EID', sort=False)['B_ENDYEAR'].max()

# 增加第一次、最后一次成立分支年份
df = df.drop_duplicates('EID')
first_set_time = pd.DataFrame({'EID': df['EID'].values, '3first_set_time': df_first_set_time.values})  # EID顺序要一致
last_set_time = pd.DataFrame({'EID': df['EID'].values, '3last_set_time': df_last_set_time.values})

# 增加第一次、最后一次关闭分支年份
first_end_time = pd.DataFrame({'EID': df['EID'].values, '3first_end_time': df_first_end_time.values})  # EID顺序要一致
last_end_time = pd.DataFrame({'EID': df['EID'].values, '3last_end_time': df_last_end_time.values})

# merge
df2 = pd.read_csv("..\\data\\3branch_add_new.csv")
df2 = pd.merge(df2, first_set_time, how='left', on='EID')
df2 = pd.merge(df2, last_set_time, how='left', on='EID')
df2 = pd.merge(df2, first_end_time, how='left', on='EID')
df2 = pd.merge(df2, last_end_time, how='left', on='EID')

# 增加最后一次成立时间 - 第一次成立
df2['3set_time_diff'] = df2['3last_set_time'] - df2['3first_set_time']

# 增加统计年份 - 最后一次变更时间
df2['3set_stat_diff'] = 2015
df2['3set_stat_diff'] = df2['3set_stat_diff'] - df2['3last_set_time']

#  增加第一次关停年份 - 第一次成立年份
df2['3set_1stend_diff'] = df2['3first_end_time'] - df2['3first_set_time']

#  增加最后一次关停年份 - 第一次成立年份
df2['3set_lastend_diff'] = df2['3last_end_time'] - df2['3first_set_time']

# 增加统计年份 - 最后一次关闭时间
df2['3end_stat_diff'] = 2015
df2['3end_stat_diff'] = df2['3end_stat_diff'] - df2['3last_end_time']

# 增加最后一次关闭时间 - 第一次关闭成立
df2['3end_time_diff'] = df2['3last_end_time'] - df2['3first_end_time']

# 变更年数
df2['alter_year_len'] = df2['3set_time_diff'] + 1

# 增加平均每年成立次数、平均每年倒闭次数
df2['ave_BR_COUNT'] = df2['BR_COUNT']/(df2['3set_time_diff'] + 1)
df2['ave_END_BR'] = df2['END_BR']/(df2['3set_time_diff'] + 1)

print(df2)
df2.to_csv('..\\data\\3branch_add_new3.csv', index=False)

