import pandas as pd


data_all = pd.read_csv('..\\data\\alltable_1_1.csv')
data_all['2setup_first_alter'] = data_all['first_alter_time'] - data_all['RGYEAR']
data_all['2setup_last_alter'] = data_all['last_alter_time'] - data_all['RGYEAR']
data_all['3setup_first_set'] = data_all['3first_br_year'] - data_all['RGYEAR']
data_all['3setup_last_set'] = data_all['3last_br_year'] - data_all['RGYEAR']
data_all['3setup_first_end'] = data_all['3first_end_year'] - data_all['RGYEAR']
data_all['3setup_last_end'] = data_all['3last_end_year'] - data_all['RGYEAR']
data_all['4setup_first_set'] = data_all['4first_bt_year'] - data_all['RGYEAR']
data_all['4setup_last_set'] = data_all['4last_bt_year'] - data_all['RGYEAR']
data_all['4setup_first_end'] = data_all['4first_end_year'] - data_all['RGYEAR']
data_all['4setup_last_end'] = data_all['4last_end_year'] - data_all['RGYEAR']
data_all['5setup_first_set'] = data_all['5first_bg_year'] - data_all['RGYEAR']
data_all['5setup_last_set'] = data_all['5last_bg_year'] - data_all['RGYEAR']
data_all['5setup_first_end'] = data_all['5first_end_year'] - data_all['RGYEAR']
data_all['5setup_last_end'] = data_all['5last_end_year'] - data_all['RGYEAR']
data_all['6setup_first_pro'] = data_all['6first_pro_year'] - data_all['RGYEAR']
data_all['6setup_last_pro'] = data_all['6last_pro_year'] - data_all['RGYEAR']
data_all['7setup_first_law'] = data_all['7first_law_year'] - data_all['RGYEAR']
data_all['7setup_last_law'] = data_all['7last_law_year'] - data_all['RGYEAR']
data_all['8setup_first_bf'] = data_all['8first_fb_year'] - data_all['RGYEAR']
data_all['8setup_last_bf'] = data_all['8last_fb_year'] - data_all['RGYEAR']
data_all['8setup_first_end'] = data_all['8first_end_year'] - data_all['RGYEAR']
data_all['8setup_last_end'] = data_all['8last_end_year'] - data_all['RGYEAR']
data_all['9first'] = data_all['9first_year'] - data_all['RGYEAR']
data_all['9last'] = data_all['9last_year'] - data_all['RGYEAR']
data_all['10setup_first_bf'] = data_all['10first_be_year'] - data_all['RGYEAR']
data_all['10setup_last_bf'] = data_all['10last_be_year'] - data_all['RGYEAR']
data_all['10setup_first_end'] = data_all['10first_end_year'] - data_all['RGYEAR']
data_all['10setup_last_end'] = data_all['10first_end_year'] - data_all['RGYEAR']

data_all.to_csv('..\\data\\alltable_1_1_add.csv', index=False)
