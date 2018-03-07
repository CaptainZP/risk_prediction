import pandas as pd

table_list = ['1entbase', '2alter', '3branch', '4invest', '5right', '6project', '7lawsuit', '8breakfaith', '9recruit', 'train', 'evaluation_public']
for table in table_list:
    df = pd.read_csv('..\\data\\{}.csv'.format(table))
    print(table, ':\n', df.describe())  # 只能显示非object即非string类型变量信息
    print('------------------------------------------')
