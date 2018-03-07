import pandas as pd
import numpy as np


# file = "C:\\Users\\captainzp\\Desktop\\houseprice_train.csv"
# feature_columns = ['卧室数', '浴室数', '房屋面积', '停车面积', '楼层数', '房屋评分', '建筑面积',
#                    '地下室面积', '建筑年份', '修复年份', '纬度', '经度', '总房间数', '总面积']
# target_column = ['销售价格']   # date_column = ['销售日期']
#
# # all_features = pd.read_csv("C:\\Users\\captainzp\\Desktop\\houseprice_train.csv", encoding='gbk')
# # print(all_features.columns)
# # an_feature = all_features.drop(['销售日期', '销售价格'], axis=1)   # 另一种比较简便的从多列中提取特征列的方法
# # print(an_feature.columns)
#
# features = get_features(file, cols=feature_columns, date_col=False)
# targets = get_target(file, target_column)
# print(features.columns)   # 显示包含的列名
# print(targets.columns)
#
# # nan = features.isnull()   # 返回每行每列的每个元素是否为nan
# nan = features.isnull().any()   # 返回每列是否有nan，更易查找
# print('------------------------------------')
# print(nan)

df = pd.DataFrame([[1, None, 10, 1], [4, 4, 4, 4], [3, 3, None, None], [4, 4, 4, 4]])
print(df)
print(df.isnull())
col = df.isnull().any()
print('col:', df.isnull().any())
nan = df[3].isnull().values == True   # 对特定的有缺失的列，找到缺失值得行号
print(nan)
print(df[3][nan])

# 删除缺失行
data = df.dropna()   # 删除有缺失值的行，参数how='all'删除全为nan的行，默认是any只要有就删
print(data)
data2 = df.dropna(axis=1)   # 删除有缺失值的列
print(data2)
data3 = df.dropna(thresh=3)   # 删除有效值少于3个的行
print(data3)
data4 = df.drop([2, 3], axis=0)   # 删除指定的行
print('-----------------------')
print(data4)
print('-----------------------')

# 填充
data5 = df.fillna(0)   # 用常数填充所有的nan, inplace=True修改原变量不产生副本
print(data5)
data6 = df.fillna({1: 1, 2: 2, 3: 3})   # 指定不同的行不同的填充数
print(data6)
data7 = df.fillna({1: df[1].mean()})    # 用所有非nan的平均值填充
print(data7)

# 删除冗余
duplicate = df.duplicated()   # 返回各行是否重复， 第一个为flase，其余重复为true
print(duplicate)
duplicate1 = df.duplicated(subset=[1, 2])   # 返回各行是否重复,只看特定的行
print(duplicate1)
data8 = df.drop_duplicates()   # 删除重复行
print(data8)


# 定位想要的点
index = df[(df[0] < 4) & (df[2] > 4)].index   # 两列分别满足条件
print('index:\n', index)
data9 = df.drop(index)
print('---\n', data9)
