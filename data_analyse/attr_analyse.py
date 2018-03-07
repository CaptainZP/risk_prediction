import pandas as pd
import matplotlib.pyplot as plt


df1 = pd.read_csv("..\\data\\alltable_12_5_4.csv")
df = pd.read_csv("..\\data\\train.csv")
df = pd.merge(df, df1, how='left', on='EID')
df = df.fillna(0)

part1 = df['RGYEAR'][df.TARGET == 1].value_counts()  # 1是停业
print('停业的：\n', part1)
part0 = df['RGYEAR'][df.TARGET == 0].value_counts()
print('正常的：\n', part0)
print('停业的占比：\n', part1 / (part0 + part1))
# part_all = pd.DataFrame({'1': part1, '0': part0})
part_all = pd.DataFrame({'end ratio': part1 / (part0 + part1)})
print((part1 / (part0 + part1)).mean())
print((part1 / (part0 + part1)).var())
print((part1 / (part0 + part1)).std())
part_all.plot(kind='bar', stacked=True)
plt.xlabel("value")
plt.ylabel('ratio')
plt.show()

# part1 = df.TARGET[df.ZCZB > df.ZCZB.mean()].value_counts()
# part2 = df.TARGET[df.ZCZB <= df.ZCZB.mean()].value_counts()
# print(part1)
# print(part2)
# print(part1[0]/(part1[1] + part1[0]))
# print(part2[0]/(part2[1] + part2[0]))
# part_all = pd.DataFrame({'part1': part1, 'part2': part2})
# part_all.plot(kind='bar', stacked=True)
# plt.xlabel("ZCZB")
# plt.ylabel('number')
# plt.show()
