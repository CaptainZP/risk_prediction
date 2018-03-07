import pandas as pd


# 最先失信的年份、最后失信年份
df_old = pd.read_csv("..\\data\\8breakfaith.csv")
df_old['FBDATE'] = pd.to_datetime(df_old['FBDATE'], format='%Y/%m/%d')
df_old['FBYEAR'] = df_old['FBDATE'].apply(lambda x: x.year)
df_first_bf_year = df_old.groupby('EID', sort=True)['FBYEAR'].min()
df_last_bf_year = df_old.groupby('EID', sort=True)['FBYEAR'].max()

# 每年失信个数
df_YEAR = pd.get_dummies(df_old['FBYEAR'], prefix='FBYEAR')
df_EID_YEAR = pd.concat([df_old['EID'], df_YEAR], axis=1)
df_EID_YEAR_sum = df_EID_YEAR.groupby('EID', sort=True).sum()
df_EID_YEAR_sum['EID'] = df_EID_YEAR_sum.index

# merge
df = pd.read_csv("..\\data\\8breakfaith_add.csv")
df = pd.merge(df, df_EID_YEAR_sum, how='left', on='EID')
first_bf_year = pd.DataFrame({'EID': df['EID'].values, '8first_bf_year': df_first_bf_year.values})
df = pd.merge(df, first_bf_year, how='left', on='EID')
last_bf_year = pd.DataFrame({'EID': df['EID'].values, '8last_bf_year': df_last_bf_year.values})
df = pd.merge(df, last_bf_year, how='left', on='EID')

# 平均每年失信个数
df['bf_even_year'] = df['BF_COUNT']/(df['8last_bf_year'] + 1 - df['8first_bf_year'])

df.to_csv('..\\data\\8breakfaith_add_new.csv', index=False)
