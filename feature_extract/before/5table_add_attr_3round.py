import pandas as pd


df = pd.read_csv("..\\data\\5right.csv")

df['ALTTIME1'] = pd.to_datetime(df['ASKDATE'], format='%Y/%m/%d')
df['ALTTIME11'] = df['ALTTIME1'].apply(lambda x: x.year + (x.month - 1)/12)

df['ALTTIME2'] = pd.to_datetime(df['FBDATE'], format='%Y/%m/%d')
df['ALTTIME22'] = df['ALTTIME2'].apply(lambda x: x.year + (x.month - 1)/12)

df_first_set_time = df.groupby('EID', sort=False)['ALTTIME11'].min()
df_last_set_time = df.groupby('EID', sort=False)['ALTTIME11'].max()

df_first_end_time = df.groupby('EID', sort=False)['ALTTIME22'].min()
df_last_end_time = df.groupby('EID', sort=False)['ALTTIME22'].max()

# 增加第一次、最后一次成立申请权利年份
df = df.drop_duplicates('EID')
first_set_time = pd.DataFrame({'EID': df['EID'].values, '5first_set_time': df_first_set_time.values})  # EID顺序要一致
last_set_time = pd.DataFrame({'EID': df['EID'].values, '5last_set_time': df_last_set_time.values})

# 增加第一次、最后一次关闭申请年份
first_end_time = pd.DataFrame({'EID': df['EID'].values, '5first_end_time': df_first_end_time.values})  # EID顺序要一致
last_end_time = pd.DataFrame({'EID': df['EID'].values, '5last_end_time': df_last_end_time.values})

# merge
df2 = pd.read_csv("..\\data\\5right_add_new.csv")
df2 = pd.merge(df2, first_set_time, how='left', on='EID')
df2 = pd.merge(df2, last_set_time, how='left', on='EID')
df2 = pd.merge(df2, first_end_time, how='left', on='EID')
df2 = pd.merge(df2, last_end_time, how='left', on='EID')

# 增加最后一次投资时间 - 第一次投资
df2['5set_time_diff'] = df2['5last_set_time'] - df2['5first_set_time']

# 增加统计年份 - 最后一次投资时间
df2['5set_stat_diff'] = 2015 + 7/12
df2['5set_stat_diff'] = df2['5set_stat_diff'] - df2['5last_set_time']

#  增加第一次关停年份 - 第一次投资年份
df2['5set_1stend_diff'] = df2['5first_end_time'] - df2['5first_set_time']

#  增加最后一次关停年份 - 第一次投资年份
df2['5set_lastend_diff'] = df2['5last_end_time'] - df2['5first_set_time']

# 增加统计年份 - 最后一次关闭时间
df2['5end_stat_diff'] = 2015 + 7/12
df2['5end_stat_diff'] = df2['5end_stat_diff'] - df2['5last_end_time']

# 增加最后一次关闭时间 - 第一次关闭成立
df2['5end_time_diff'] = df2['5last_end_time'] - df2['5first_end_time']

# 增加平均每年申请次数、平均每年赋予次数
df2['ave_RIGHT_COUNT'] = df2['RIGHT_COUNT']/(df2['5set_time_diff'] + 1)
df2['ave_FUYU_RIGHT'] = df2['FUYU_RIGHT']/(df2['5set_time_diff'] + 1)

print(df2)
df2.to_csv('..\\data\\5right_add_new3.csv', index=False)

