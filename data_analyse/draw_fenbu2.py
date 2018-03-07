import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import pandas as pd


plt.rcParams['font.sans-serif'] = ['SimHei']   # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号
file = "..\\data\\all_7.csv"

df = pd.read_csv(file)
df = df.fillna(0)
target = pd.read_csv(file, usecols=["TARGET"])


df['BF_COUNT'] = np.log1p(df['BF_COUNT'])
# df['BF_COUNT'] = np.log1p(df['BF_COUNT'])
# df['FSTINUM'] = np.log1p(df['FSTINUM'])
# df['FINZB'] = np.log1p(df['FINZB'])
# df['FINZB'] = np.log1p(df['FINZB'])
# df['INUM'] = np.log1p(df['INUM'])
# df['MPNUM'] = np.log1p(df['MPNUM'])
# df['ZCZB'] = np.log1p(df['ZCZB'])



# res = stats.probplot(df['TZINUM'], plot=plt)

sns.distplot(df['BF_COUNT'], fit=stats.norm)   # 价格直方图,房价并不服从正态分布

# target['TARGET'] = np.log1p(target['TARGET'])   # 对数据取对数取消正偏性log/ log1p
# res = stats.probplot(target['TARGET'], plot=plt)   # 概率图可以发现，数据具有明显的正偏性，因此可采用对数来缓解这种趋势
# sns.distplot(target['TARGET'], fit=stats.norm)
# # res = stats.probplot(bb['地下室面积'], plot=plt)]
plt.show()

# 查看其斜度skewness和峭度kurtosis，这是很重要的两个统计量
# print('skewness: {0}, kurtosis: {1}'.format(target['销售价格'].skew(), target['销售价格'].kurt()))


plt.show()
