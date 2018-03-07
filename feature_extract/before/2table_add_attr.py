import pandas as pd


df = pd.read_csv("..\\data\\2alter.csv")

df_ALTERNO = pd.get_dummies(df['ALTERNO'], prefix='ALTERNO')
df_EID_ALTERNO = pd.concat([df['EID'], df_ALTERNO], axis=1)
df_EID_ALTERNO_sum = df_EID_ALTERNO.groupby('EID', sort=False).sum()
df_EID_ALTERNO_sum['EID'] = df_EID_ALTERNO_sum.index

df['ALTDATE'] = pd.to_datetime(df['ALTDATE'], format='%Y/%m/%d')

# d = (df['ALTDATE'][0] - df['ALTDATE'][1])
# print(d.days)

df['ALTYEAR'] = df['ALTDATE'].apply(lambda x: x.year)
df_first_alter_year = df.groupby('EID', sort=False)['ALTYEAR'].min()
df_last_alter_year = df.groupby('EID', sort=False)['ALTYEAR'].max()

# 增加变更次数
df['change_number'] = 1

# 增加资金变更次数
df['found_change_number'] = df['ALTERNO'].apply(lambda x: 1 if x == 5 or x == 27 else 0)

# 合并
df = df.groupby('EID', sort=False).sum()

# 增加是否变更
df['if_change'] = 1

# 增加资金是否变更
df['if_found_change'] = df['found_change_number'].apply(lambda x: 1 if x > 0 else 0)

# 增加资金差
df['found_diff'] = df['ALTAF'] - df['ALTBE']

# 增加是否资金增加
df['if_found_up'] = df['found_diff'].apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))

# 索引变列
df['EID'] = df.index

# 将EID变为第一列
cols = list(df)
cols.insert(0, cols.pop(cols.index('EID')))
df = df.ix[:, cols]

# 增加第一年和最后一年变更
first_alter_year = pd.DataFrame({'EID': df['EID'].values, 'first_alter_year': df_first_alter_year.values})
last_alter_year = pd.DataFrame({'EID': df['EID'].values, 'last_alter_year': df_last_alter_year.values})

df = pd.merge(df, df_EID_ALTERNO_sum, how='left', on='EID')
df = pd.merge(df, first_alter_year, how='left', on='EID')
df = pd.merge(df, last_alter_year, how='left', on='EID')

# 删除merge后没有用的列
df = df.drop(['ALTERNO', 'ALTYEAR'], axis=1)
df.to_csv('..\\data\\2alter_add_new.csv', index=False)

print(df)
