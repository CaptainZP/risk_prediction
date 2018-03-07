import pandas as pd


#  最先项目的年份、最后项目年份
df_old = pd.read_csv("..\\data\\7lawsuit.csv")
# df_old['DJDATE'] = pd.to_datetime(df_old['DJDATE'], format='%Y/%m/%d')
print(df_old)
df_old['LAWDATE'] = pd.to_datetime(df_old['LAWDATE'], format='%Y/%m/%d')
df_old['YEAR'] = df_old['LAWDATE'].apply(lambda x: x.year)
# 最后被执行的年份
df_first_lawsuit_year = df_old.groupby('EID', sort=True)['YEAR'].min()
df_last_lawsuit_year = df_old.groupby('EID', sort=True)['YEAR'].max()

# 每年的被执行个数
df_YEAR = pd.get_dummies(df_old['YEAR'], prefix='YEAR')
df_EID_YEAR = pd.concat([df_old['EID'], df_YEAR], axis=1)
df_EID_YEAR_sum = df_EID_YEAR.groupby('EID', sort=True).sum()
df_EID_YEAR_sum['EID'] = df_EID_YEAR_sum.index

df = pd.read_csv('..\\data\\7lawsuit_add.csv')
df = pd.merge(df, df_EID_YEAR_sum, on='EID', how='left')
first_lawsuit_year = pd.DataFrame({'EID': df['EID'].values, '7first_lawsuit_year': df_first_lawsuit_year.values})
df = pd.merge(df, first_lawsuit_year, how='left', on='EID')
last_lawsuit_year = pd.DataFrame({'EID': df['EID'].values, '7last_lawsuit_year': df_last_lawsuit_year.values})
df = pd.merge(df, last_lawsuit_year, how='left', on='EID')
print(df.head())
df.to_csv('..\\data\\7lawsuit_add_new.csv', index=False)

