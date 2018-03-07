import pandas as pd


#  最先申请的年份、最后申请权利年份
df_old = pd.read_csv("..\\data\\5right.csv")
df_old['ASKDATE'] = pd.to_datetime(df_old['ASKDATE'], format='%Y/%m/%d')
df_old['ASKYEAR'] = df_old['ASKDATE'].apply(lambda x: x.year)
df_first_ask_year = df_old.groupby('EID', sort=True)['ASKYEAR'].min()
df_last_ask_year = df_old.groupby('EID', sort=True)['ASKYEAR'].max()

# 已赋予所占比例、未赋予所占比例
df = pd.read_csv("..\\data\\5right_add.csv")
df['fuyu_ratio'] = df['FUYU_RIGHT']/df['RIGHT_COUNT']
df['wfuyu_ratio'] = df['WFUYU_RIGHT']/df['RIGHT_COUNT']

# merge
first_ask_year = pd.DataFrame({'EID': df['EID'].values, '5first_ask_year': df_first_ask_year.values})
df = pd.merge(df, first_ask_year, how='left', on='EID')
last_ask_year = pd.DataFrame({'EID': df['EID'].values, '5last_ask_year': df_last_ask_year.values})
df = pd.merge(df, last_ask_year, how='left', on='EID')
df.to_csv('..\\data\\5right_add_new.csv', index=False)

