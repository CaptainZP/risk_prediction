import pandas as pd

# 与 numpy 的ndarray数据相比，DataFrame数据自带有行列信息
df = pd.DataFrame({'id': [1, 2, 3, 4], 'raw': ['a', 'b', 'a', 'd']})
print(df)
df['grade'] = df['raw'].astype('category')
print(df)
print(df.dtypes)
df['grade'].cat.categories = ['very good', 'good', 'bad']   # Categorical类型数据重命名为更有意义的名称
print(df)
df['grade'].cat.set_categories(['very good', 'good', 'medium', 'bad', 'very bad'])   # 增加类别和排序， 此顺序即顺序
print(df['grade'])
df2 = df.sort_values('grade')
print(df2)
# count = df.groupby('grade').sum()  # 数字列求和
count = df.groupby('grade').size()   # 此列计数
print(count)
# df2.to_csv('foo.csv')   # 存文件


df3 = pd.DataFrame({'id': [1, 2, 3, 4], 'raw': [10, 20, 30, 40], 'col': [100, 200, 300, 400]})
print(df3)
df3 = df3.cumsum()   # 上行往下行逐行加入
print(df3)
