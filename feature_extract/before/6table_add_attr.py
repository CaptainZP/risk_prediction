import pandas as pd


#  最先项目的年份、最后项目年份
df_old = pd.read_csv("..\\data\\6project.csv")
df_old['DJDATE'] = pd.to_datetime(df_old['DJDATE'], format='%Y/%m/%d')
df_old['DJYEAR'] = df_old['DJDATE'].apply(lambda x: x.year)
df_first_project_year = df_old.groupby('EID', sort=True)['DJYEAR'].min()
df_last_project_year = df_old.groupby('EID', sort=True)['DJYEAR'].max()

# 每年的中标个数
df_DJYEAR = pd.get_dummies(df_old['DJYEAR'], prefix='DJYEAR')
df_EID_DJYEAR = pd.concat([df_old['EID'], df_DJYEAR], axis=1)
df_EID_DJYEAR_sum = df_EID_DJYEAR.groupby('EID', sort=True).sum()
df_EID_DJYEAR_sum['EID'] = df_EID_DJYEAR_sum.index

# 已赋予所占比例、未赋予所占比例
df = pd.read_csv("..\\data\\6project_add.csv")
df['6ws_ratio'] = df['WS_PROCOUNT']/df['PROCOUNT']

# merge
df = pd.merge(df, df_EID_DJYEAR_sum, how='left', on='EID')
first_project_year = pd.DataFrame({'EID': df['EID'].values, '6first_project_year': df_first_project_year.values})
df = pd.merge(df, first_project_year, how='left', on='EID')
last_project_year = pd.DataFrame({'EID': df['EID'].values, '6last_project_year': df_last_project_year.values})
df = pd.merge(df, last_project_year, how='left', on='EID')
df.to_csv('..\\data\\6project_add_new.csv', index=False)

