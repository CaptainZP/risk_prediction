import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.mlab as mlab

plt.rcParams['font.sans-serif'] = ['SimHei']   # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号
X = np.linspace(0, 600000, 10000, endpoint=True)
Y = pd.read_csv("..\\data\\1entbase.csv", usecols=["ZCZB"])
Y = Y.fillna(0).values

# figure
plt.figure(figsize=(10, 6))
# plt.scatter(X, C, c='r', label='cos')   # 散点图， x轴数组，y轴数组，颜色，标签
# plt.plot(X, S, 'b-', label='sin')   # 折线图， x轴数组，y轴数组，颜色线型，标签
# plt.bar(X, T, color='y', label='bar', width=0.1)
n, bins, patches = plt.hist(Y, 100, normed=1, facecolor='pink', edgecolor='black', label='hist')  # bins是分成几个柱子
y = mlab.normpdf(bins, Y.mean(), Y.std())
# y = mlab.normpdf(bins)
plt.plot(bins, y, '--')
# plt.plot(bins, '--')
plt.legend(loc='upper right')   # 标签的位 置
plt.xlabel('x轴', rotation='horizontal')
plt.ylabel('y轴', rotation='horizontal')

# plt.xlim(X.min()*1.1, X.max()*1.1)   # 调整轴的范围
# plt.ylim(C.min()*1.1, C.max()*1.1)
# plt.xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi])   # 调整轴的刻度
# plt.yticks([-1, 0, 1])

# plt.savefig('result.png')
plt.show()   # 显示图