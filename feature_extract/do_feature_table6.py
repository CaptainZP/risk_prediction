import pandas as pd


datafile6 = '..\\data\\6project.csv'
data_6 = pd.read_csv(datafile6)

data_6['PROCOUNT'] = 1
data_6['BS_PROCOUNT'] = data_6['IFHOME']
data_6['WS_PROCOUNT'] = data_6['IFHOME'].apply(lambda x: 1 if x==0 else 0)
data_6['DJDATE'] = pd.to_datetime(data_6['DJDATE'], format='%Y/%m/%d')
data_6['DJYEAR_Y'] = data_6['DJDATE'].apply(lambda x: x.year)
data_6['DJTIME'] = data_6['DJDATE'].apply(lambda x: x.year + (x.month - 1) / 12)
data_6_1 = data_6

data_6 = pd.concat([data_6, pd.get_dummies(data_6['DJYEAR_Y'], prefix='DJYEAYR')], axis=1)
# print(data_6)
data_6_new = data_6.groupby('EID', sort=False).sum()
data_6_new = data_6_new.reset_index()
print(data_6_new)
data_6_new['BS_RATE'] = data_6_new['BS_PROCOUNT']/data_6_new['PROCOUNT']
data_6_new['WS_RATE'] = data_6_new['WS_PROCOUNT']/data_6_new['PROCOUNT']
data_6_new = data_6_new.drop(['TYPECODE','IFHOME', 'DJTIME', 'DJYEAR_Y'], axis=1)

data_6 = data_6_1
first_pro_year = data_6.groupby('EID', sort=False)['DJYEAR_Y'].min()
last_pro_year = data_6.groupby('EID', sort=False)['DJYEAR_Y'].max()
first_pro_time = data_6.groupby('EID', sort=False)['DJTIME'].min()
last_pro_time = data_6.groupby('EID', sort=False)['DJTIME'].max()
data_6 = data_6.drop_duplicates('EID')
first_pro_year = pd.DataFrame({'EID': data_6['EID'].values, '6first_pro_year': first_pro_year.values})
last_pro_year = pd.DataFrame({'EID': data_6['EID'].values, '6last_pro_year': last_pro_year.values})
first_pro_time = pd.DataFrame({'EID': data_6['EID'].values, '6first_pro_time': first_pro_time.values})
last_pro_time = pd.DataFrame({'EID': data_6['EID'].values, '6last_pro_time': last_pro_time.values})

data_6_new = pd.merge(data_6_new, first_pro_year, on='EID', how='left')
data_6_new = pd.merge(data_6_new, last_pro_year, on='EID', how='left')
data_6_new = pd.merge(data_6_new, first_pro_time, on='EID', how='left')
data_6_new = pd.merge(data_6_new, last_pro_time, on='EID', how='left')

data_6_new['6last_minus_first'] = data_6_new['6last_pro_time'] - data_6_new['6first_pro_time']
# data_6_new['6now_minus_first'] = 2015+(7/12) - data_6_new['6first_pro_time']
data_6_new['6now_minus_last'] = 2015+(7/12) - data_6_new['6last_pro_time']
data_6_new['pro_year_avg'] = data_6_new['PROCOUNT'] / (data_6_new['6last_pro_year'] - data_6_new['6first_pro_year'] + 1)
# print(data_6_new)

data_6_new.to_csv('..\\data\\6project_add.csv', index=False)
