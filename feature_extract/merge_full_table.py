import pandas as pd


datafile1 = '..\\data\\1entbase_add.csv'
datafile2 = '..\\data\\2alter_add_new.csv'
datafile3 = '..\\data\\3branch_add_new.csv'
datafile4 = '..\\data\\4invest_add_new.csv'
datafile5 = '..\\data\\5right_add_new.csv'
datafile6 = '..\\data\\6project_add_new.csv'
datafile7 = '..\\data\\7lawsuit_add_new.csv'
datafile8 = '..\\data\\8breakfaith_add_new.csv'
datafile9 = '..\\data\\9recruit_add_new.csv'
datafile10 = '..\\data\\10qualification_add_new.csv'
data_1 = pd.read_csv(datafile1)
data_2 = pd.read_csv(datafile2)
data_3 = pd.read_csv(datafile3)
data_4 = pd.read_csv(datafile4)
data_5 = pd.read_csv(datafile5)
data_6 = pd.read_csv(datafile6)
data_7 = pd.read_csv(datafile7)
data_8 = pd.read_csv(datafile8)
data_9 = pd.read_csv(datafile9)
data_10 = pd.read_csv(datafile10)
all = pd.merge(data_1, data_2, how='left', on='EID')
all = pd.merge(all, data_3,  how='left', on='EID')
all = pd.merge(all, data_4,  how='left', on='EID')
all = pd.merge(all, data_5,  how='left', on='EID')
all = pd.merge(all, data_6,  how='left', on='EID')
all = pd.merge(all, data_7,  how='left', on='EID')
all = pd.merge(all, data_8,  how='left', on='EID')
all = pd.merge(all, data_9,  how='left', on='EID')
all = pd.merge(all, data_10,  how='left', on='EID')
data_all = all
# data_all['2setup_first_alter'] = data_all['first_alter_time'] - data_all['RGYEAR']
# data_all['2setup_last_alter'] = data_all['last_alter_time'] - data_all['RGYEAR']
# data_all['3setup_first_set'] = data_all['3first_br_year'] - data_all['RGYEAR']
# data_all['3setup_last_set'] = data_all['3last_br_year'] - data_all['RGYEAR']
# data_all['3setup_first_end'] = data_all['3first_end_year'] - data_all['RGYEAR']
# data_all['3setup_last_end'] = data_all['3last_end_year'] - data_all['RGYEAR']
# data_all['4setup_first_set'] = data_all['4first_bt_year'] - data_all['RGYEAR']
# data_all['4setup_last_set'] = data_all['4last_bt_year'] - data_all['RGYEAR']
# data_all['4setup_first_end'] = data_all['4first_end_year'] - data_all['RGYEAR']
# data_all['4setup_last_end'] = data_all['4last_end_year'] - data_all['RGYEAR']
# data_all['5setup_first_set'] = data_all['5first_bg_year'] - data_all['RGYEAR']
# data_all['5setup_last_set'] = data_all['5last_bg_year'] - data_all['RGYEAR']
# data_all['5setup_first_end'] = data_all['5first_end_year'] - data_all['RGYEAR']
# data_all['5setup_last_end'] = data_all['5last_end_year'] - data_all['RGYEAR']
# data_all['6setup_first_pro'] = data_all['6first_pro_year'] - data_all['RGYEAR']
# data_all['6setup_last_pro'] = data_all['6last_pro_year'] - data_all['RGYEAR']
# data_all['7setup_first_law'] = data_all['7first_law_year'] - data_all['RGYEAR']
# data_all['7setup_last_law'] = data_all['7last_law_year'] - data_all['RGYEAR']
# data_all['8setup_first_bf'] = data_all['8first_fb_year'] - data_all['RGYEAR']
# data_all['8setup_last_bf'] = data_all['8last_fb_year'] - data_all['RGYEAR']
# data_all['8setup_first_end'] = data_all['8first_end_year'] - data_all['RGYEAR']
# data_all['8setup_last_end'] = data_all['8last_end_year'] - data_all['RGYEAR']
# data_all['9first'] = data_all['9first_year'] - data_all['RGYEAR']
# data_all['9last'] = data_all['9last_year'] - data_all['RGYEAR']
# data_all['10setup_first_bf'] = data_all['10first_be_year'] - data_all['RGYEAR']
# data_all['10setup_last_bf'] = data_all['10last_be_year'] - data_all['RGYEAR']
# data_all['10setup_first_end'] = data_all['10first_end_year'] - data_all['RGYEAR']
# data_all['10setup_last_end'] = data_all['10first_end_year'] - data_all['RGYEAR']

# print(all.head())
data_all.to_csv('..\\data\\alltable_12_6_3.csv', index=False)
