import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_scatter(df, xvar, yvar):
    '''
    画连续变量与因变量的散点图
    :param df: 数据的dataframe，dataframe
    :param xvar: 自变量，str
    :param yvar: 因变量，str
    :return:
    '''
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.subplots(1, 1, figsize=(15, 6))
    plt.scatter(df[xvar], df[yvar])
    plt.xlabel(xvar)
    plt.ylabel(yvar)
    plt.show()


def plot_box(df, xvar, yvar):
    '''
    画离散变量与因变量的箱型图
    :param df: 数据的datafrmae， dataframe
    :param xvar: 自变量，str
    :param yvar: 因变量，str
    :return:
    '''
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.subplots(1, 1, figsize=(15, 6))
    sns.boxplot(x=xvar, y=yvar, data=df)
    plt.show()

if __name__ == '__main__':
    file = "..\\data\\all_7.csv"
    df = pd.read_csv(file)
    plot_scatter(df, 'EID', 'TZINUM')
