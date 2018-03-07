import pandas as pd


# 最先招聘的年份、最后招聘年份
df_old = pd.read_csv("..\\data\\9recruit.csv")
df_old['RECDATE'] = pd.to_datetime(df_old['RECDATE'], format='%Y/%m/%d')
df_old['RECDATE'] = df_old['RECDATE'].apply(lambda x: x.year)
df_first_recruit_year = df_old.groupby('EID', sort=True)['RECDATE'].min()
df_last_recruit_year = df_old.groupby('EID', sort=True)['RECDATE'].max()

# 每年招聘次数
df_YEAR = pd.get_dummies(df_old['RECDATE'], prefix='RECDATE')
df_EID_YEAR = pd.concat([df_old['EID'], df_YEAR], axis=1)
df_EID_YEAR_sum = df_EID_YEAR.groupby('EID', sort=True).sum()
df_EID_YEAR_sum['EID'] = df_EID_YEAR_sum.index

# 半年总职位数/半年总招聘次数
df_old['half_half_recruit'] = df_old['RECRNUM'].isnull().apply(lambda x: 1 if x != True else 0)
df_half_half_recruit = df_old.groupby('EID')['half_half_recruit'].sum()

# 半年总职位数/总招聘次数
df = pd.read_csv("..\\data\\9recruit_add.csv")
df['half_all_recruit'] = df['RECRNUM']/df['WZ_COUNT']

half_half_recruit = pd.DataFrame({'EID': df['EID'].values, 'half_half_recruit': df_half_half_recruit.values})

# merge
df = pd.merge(df, half_half_recruit, how='left', on='EID')
df['half_half_recruit'] = df['RECRNUM']/df['half_half_recruit']

df = pd.merge(df, df_EID_YEAR_sum, how='left', on='EID')
first_recruit_year = pd.DataFrame({'EID': df['EID'].values, '9first_recruit_year': df_first_recruit_year.values})
df = pd.merge(df, first_recruit_year, how='left', on='EID')
last_recruit_year = pd.DataFrame({'EID': df['EID'].values, '9last_bf_year': df_last_recruit_year.values})
df = pd.merge(df, last_recruit_year, how='left', on='EID')
df.to_csv('..\\data\\9recruit_add_new.csv', index=False)
