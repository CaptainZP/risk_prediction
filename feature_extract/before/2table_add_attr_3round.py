import pandas as pd


df = pd.read_csv("..\\data\\2alter.csv")
df['ALTTIME'] = pd.to_datetime(df['ALTDATE'], format='%Y/%m/%d')

df['ALTTIME2'] = df['ALTTIME'].apply(lambda x: x.year + (x.month - 1)/12)
print(df['ALTTIME2'])
df_first_alter_time = df.groupby('EID', sort=False)['ALTTIME2'].min()
print(df_first_alter_time)
df_last_alter_time = df.groupby('EID', sort=False)['ALTTIME2'].max()

# 增加第一次、最后一次变更年月
df = df.drop_duplicates('EID')
first_alter_time = pd.DataFrame({'EID': df['EID'].values, 'first_alter_time': df_first_alter_time.values})  # EID顺序要一致
last_alter_time = pd.DataFrame({'EID': df['EID'].values, 'last_alter_time': df_last_alter_time.values})

# merge
df2 = pd.read_csv("..\\data\\2alter_add_new.csv")
df2 = pd.merge(df2, first_alter_time, how='left', on='EID')
df2 = pd.merge(df2, last_alter_time, how='left', on='EID')

# 增加最后一次变更时间 - 第一次变更
df2['alter_time_diff'] = df2['last_alter_time'] - df2['first_alter_time']

# 增加统计年月 - 最后一次变更时间
df2['alter_stat_diff'] = 2015 + 7/12
df2['alter_stat_diff'] = df2['alter_stat_diff'] - df2['last_alter_time']

# 变更年数
df2['alter_year_len'] = df2['last_alter_year'] - df2['first_alter_year'] + 1

# 增加平均每年变更次数、平均每年资金变更次数、平均资金差
df2['ave_change_number'] = df2['change_number']/df2['alter_year_len']
df2['ave_found_change_number'] = df2['found_change_number']/df2['alter_year_len']
df2['ave_found_diff'] = df2['found_diff']/df2['found_change_number']

print(df2)
df2.to_csv('..\\data\\2alter_add_new3.csv', index=False)
