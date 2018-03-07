import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


'''研究各变量之间、各变量与标签的相关性
'''

def allvars_correlation(df):
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    corr_matrix = df.corr(method='pearson')   # 计算dataframe列的两两pearson/spearman相关关系，不包括空值
    fig, ax = plt.subplots(figsize=(12, 9))
    sns.heatmap(corr_matrix, ax=ax, linewidths=0.05, annot=True)
    ax.set_title('所有变量的相关矩阵')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
    plt.show()


def continuous_dependent_correlation(df, continuous_vars, dependent_var):
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    numerical_columns = df[continuous_vars].columns[df[continuous_vars].dtypes != object]
    labels = list()
    values = list()
    for col in numerical_columns:
        labels.append(col)
        values.append(np.corrcoef(df[col].values, df[dependent_var].values)[0, 1])   # 连续变量返回皮尔逊相关系数
    labels = np.array(labels)
    values = np.array(values)
    index = np.argsort(values)[::-1]
    values = values[index]
    labels = labels[index]
    ind = np.linspace(0, len(labels), len(labels))
    fig, ax = plt.subplots(figsize=(15, 6))  # 创建一个图和一组子图,返回图的对象、轴对象的数组
    bars = ax.bar(ind, np.array(values), color='red', edgecolor='black')  # 给定xy坐标，做一个条形图, 返回柱状图容器
    for bar in bars:   # 显示柱子的值
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height + 0.01, round(height, 3), ha='center', va='bottom')
    ax.set_xticks(ind)
    ax.set_xticklabels(labels, rotation=0)  # 设置x轴标签
    ax.set_title("与{}的pearson相关系数".format(dependent_var))
    plt.show()


def separated_dependent_correlation(df, separated_vars, dependent_var):
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    numerical_columns = df[separated_vars].columns[df[separated_vars].dtypes != object]
    print(numerical_columns)
    labels = list()
    values = list()
    for col in numerical_columns:
        labels.append(col)
        correlation, pvalue = stats.spearmanr(df[col].values, df[dependent_var].values)
        values.append(correlation)   # 离散变量返回spearman相关系数
    labels = np.array(labels)
    values = np.array(values)
    index = np.argsort(values)[::-1]
    values = values[index]
    labels = labels[index]
    ind = np.linspace(0, len(labels), len(labels))
    fig, ax = plt.subplots(figsize=(15, 6))  # 创建一个图和一组子图,返回图的对象、轴对象的数组
    bars = ax.bar(ind, np.array(values), color='red', edgecolor='black')  # 给定xy坐标，做一个条形图, 返回柱状图容器
    for bar in bars:  # 显示柱子的值
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height + 0.01, round(height, 3), ha='center', va='bottom')
    ax.set_xticks(ind)
    ax.set_xticklabels(labels, rotation=0)  # 设置x轴标签
    ax.set_title("与{}的spearman相关系数".format(dependent_var))
    plt.show()


if __name__ == '__main__':
    file = "..\\data\\6project_add_new.csv"
    feature_columns = ['销售价格', '销售日期', '卧室数', '浴室数', '房屋面积', '停车面积', '楼层数',
                       '房屋评分', '建筑面积', '地下室面积', '建筑年份', '修复年份', '纬度', '经度']
    continuous_columns = ['销售日期', '房屋面积', '停车面积', '建筑面积', '地下室面积', '建筑年份', '纬度', '经度']
    separated_columns = ['卧室数', '浴室数', '楼层数', '房屋评分', '修复年份']
    target_column = '销售价格'
    df = pd.read_csv(file)
    # 分析所有变量
    allvars_correlation(df)
    # # 连续型变量
    # continuous_dependent_correlation(df, continuous_columns, target_column)
    # # 离散型变量
    # separated_dependent_correlation(df, separated_columns, target_column)
