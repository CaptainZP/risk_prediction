import pandas as pd


df = pd.read_csv("..\\data\\2alter.csv")
df['ALTBE'] = df['ALTBE'].astype(float)
df['ALTAF'] = df['ALTAF'].astype(float)

# 将ALTERNO进行get_dummies
df_ALTERNO = pd.get_dummies(df['ALTERNO'], prefix='ALTERNO')
df_EID_ALTERNO = pd.concat([df['EID'], df_ALTERNO], axis=1)
df_EID_ALTERNO_sum = df_EID_ALTERNO.groupby('EID', sort=False).sum()
df_EID_ALTERNO_sum['EID'] = df_EID_ALTERNO_sum.index


# 计算第一年和最后一年变更
df['ALTDATE'] = pd.to_datetime(df['ALTDATE'], format='%Y/%m/%d')
df['ALTYEAR'] = df['ALTDATE'].apply(lambda x: x.year)  # 删
df['ALTTIME'] = pd.to_datetime(df['ALTDATE'], format='%Y/%m/%d')
df['ALTTIME2'] = df['ALTTIME'].apply(lambda x: x.year + (x.month - 1)/12)  # 删
df_first_alter_year = df.groupby('EID', sort=False)['ALTYEAR'].min()
df_last_alter_year = df.groupby('EID', sort=False)['ALTYEAR'].max()
df_first_alter_time = df.groupby('EID', sort=False)['ALTTIME2'].min()
df_last_alter_time = df.groupby('EID', sort=False)['ALTTIME2'].max()

# 增加变更次数
df['change_number'] = 1

# 增加资金变更次数
df['found_change_number'] = df['ALTERNO'].apply(lambda x: 1 if x == 5 or x == 27 else 0)

# 合并
df = df.groupby('EID', sort=False).sum()
df = df.reset_index()
print(df)

# 增加是否变更
df['if_change'] = 1

# 增加资金是否变更
df['if_found_change'] = df['found_change_number'].apply(lambda x: 1 if x > 0 else 0)

# 增加资金差
df['found_diff'] = df['ALTAF'] - df['ALTBE']

# 增加是否资金增加
df['if_found_up'] = df['found_diff'].apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))

df = pd.merge(df, df_EID_ALTERNO_sum, how='left', on='EID')
# 增加第一年和最后一年变更
first_alter_year = pd.DataFrame({'EID': df['EID'].values, 'first_alter_year': df_first_alter_year.values})
last_alter_year = pd.DataFrame({'EID': df['EID'].values, 'last_alter_year': df_last_alter_year.values})
first_alter_time = pd.DataFrame({'EID': df['EID'].values, 'first_alter_time': df_first_alter_time.values})
last_alter_time = pd.DataFrame({'EID': df['EID'].values, 'last_alter_time': df_last_alter_time.values})
df = pd.merge(df, first_alter_year, how='left', on='EID')
df = pd.merge(df, last_alter_year, how='left', on='EID')
df = pd.merge(df, first_alter_time, how='left', on='EID')
df = pd.merge(df, last_alter_time, how='left', on='EID')

# 增加最后一次变更时间 - 第一次变更（待议）
df['alter_time_diff'] = df['last_alter_time'] - df['first_alter_time']

# 增加统计年月 - 最后一次变更时间（待议）
df['alter_stat_diff'] = 2015 + 7/12
df['alter_stat_diff'] = df['alter_stat_diff'] - df['last_alter_time']

# 增加平均每年变更次数、平均每年资金变更次数、平均资金差（待议）
df['ave_change_number'] = df['change_number']/(df['alter_time_diff'] + 1)
df['ave_found_change_number'] = df['found_change_number']/(df['alter_time_diff'] + 1)
df['ave_found_diff'] = df['found_diff']/df['found_change_number']


# 写文件
df = df.drop(['ALTERNO', 'ALTTIME2', 'ALTYEAR'], axis=1)  # 删除没用的列
df.to_csv('..\\data\\2alter_add.csv', index=False)
print(df)
