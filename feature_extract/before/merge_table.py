import pandas as pd


df1 = pd.read_csv("..\\data\\all_table.csv")
df2 = pd.read_csv("..\\data\\2alter_add7cols.csv")
merge_df = pd.merge(df1, df2, how='left', on='EID')
merge_df = merge_df.drop('change_number', axis=1)

print(merge_df.head(10))
merge_df.to_csv('..\\data\\all_table2.csv', index=False)

# left = pd.DataFrame({'key1': ['K0', 'K1', 'K2', 'K3'],
#                      'A': ['A0', 'A1', 'A2', 'A3'],
#                      'B': ['B0', 'B1', 'B2', 'B3']})
# right = pd.DataFrame({'key1': ['K0', 'K1', 'K1', 'K3'],
#                       'C': ['C0', 'C1', 'C2', 'C3'],
#                       'D': ['D0', 'D1', 'D2', 'D3']})
# result = pd.merge(left, right, how='left', on=['key1'])
# print(result)


