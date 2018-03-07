import pandas as pd
from collections import Counter

df = pd.read_csv("..\\data\\2alter.csv")
obj_columns = ['ALTBE']
for col in obj_columns:
    df[col] = df[col].astype(float)
print(df.head(10))

# print(df.info())
index0 = (df.ALTERNO == '5')
# print(index0)
new_df0 = df['EID'][index0]
print(new_df0.head(10))


# index = (df.ALTERNO == '5') & (df.ALTBE > df.ALTAF)
index = (df.ALTERNO == '5') | (df.ALTERNO == '27')
# print(index)
new_df = df['EID'][index]
print('aa:\n', new_df.head(10))

df2 = pd.read_csv("..\\data\\train.csv")
label2 = df2[df2['EID'].isin(new_df)]
print(label2.head())
print('label number:{}'.format(Counter(label2['TARGET'])))
