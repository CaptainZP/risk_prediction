import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


'''查看数据的多重线性:即变量间的相关关系
共线性增加系数的标准差， 共线性使得一些变量在统计上应该有用时无用
完全删除这些变量，（1）通过相加或其他操作添加新特性（2）使用PCA，它将把特性集减少到少量的非共线特性
'''


def allvars_collinearity(df, threshold=0.5):
    corr_matrix = df.corr(method='pearson')
    # 找出相关性大于0.5且不为1的,unstack将矩阵分解为一行对应一组变量,dropna去掉Nan,to_dict()将结果变成字典
    important_corrs = (corr_matrix[abs(corr_matrix) > threshold][corr_matrix != 1.0]).unstack().dropna().to_dict()
    unique_important_corrs = pd.DataFrame(
        list(set([(tuple(sorted(key)), important_corrs[key]) for key in important_corrs]))
        , columns=['Attribute Pair', 'Correlation'])
    unique_important_corrs = unique_important_corrs.ix[abs(unique_important_corrs['Correlation']).argsort()[::-1]]
    print(unique_important_corrs)
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    fig, ax = plt.subplots(figsize=(15, 6))  # 创建一个图和一组子图,返回图的对象、轴对象的数组
    ind = np.linspace(0, len(unique_important_corrs), len(unique_important_corrs))
    bars = ax.bar(ind, np.array(unique_important_corrs['Correlation']), color='red', edgecolor='black')  # 给定xy坐标，做一个条形图, 返回柱状图容器
    for bar in bars:  # 显示柱子的值
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height + 0.01, round(height, 3), ha='center', va='bottom')
    ax.set_xticks(ind)
    ax.set_xticklabels(unique_important_corrs['Attribute Pair'], rotation=10)  # 设置x轴标签
    ax.set_title("所有变量间的共线性")
    plt.show()


def continuous_vars_collinearity(df, continuous_vars, threshold=0.5):
    df = df[continuous_vars]
    corr_matrix = df.corr(method='pearson')
    # 找出相关性大于0.5且不为1的,unstack将矩阵分解为一行对应一组变量,dropna去掉Nan,to_dict()将结果变成字典
    important_corrs = (corr_matrix[abs(corr_matrix) > threshold][corr_matrix != 1.0]).unstack().dropna().to_dict()
    unique_important_corrs = pd.DataFrame(
        list(set([(tuple(sorted(key)), important_corrs[key]) for key in important_corrs]))
        , columns=['Attribute Pair', 'Correlation'])
    unique_important_corrs = unique_important_corrs.ix[
        abs(unique_important_corrs['Correlation']).argsort()[::-1]]
    print(unique_important_corrs)
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    fig, ax = plt.subplots(figsize=(15, 6))  # 创建一个图和一组子图,返回图的对象、轴对象的数组
    ind = np.linspace(0, len(unique_important_corrs), len(unique_important_corrs))
    bars = ax.bar(ind, np.array(unique_important_corrs['Correlation']), color='red',
                  edgecolor='black')  # 给定xy坐标，做一个条形图, 返回柱状图容器
    for bar in bars:  # 显示柱子的值
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height + 0.01, round(height, 3), ha='center', va='bottom')
    ax.set_xticks(ind)
    ax.set_xticklabels(unique_important_corrs['Attribute Pair'], rotation=10)  # 设置x轴标签
    ax.set_title("所有变量间的共线性")
    plt.show()


def separated_vars_collinearity(df, separated_vars, threshold=0.5):
    df = df[separated_vars]
    corr_matrix = df.corr(method='spearman')
    important_corrs = (corr_matrix[abs(corr_matrix) > threshold][corr_matrix != 1.0]).unstack().dropna().to_dict()
    unique_important_corrs = pd.DataFrame(
        list(set([(tuple(sorted(key)), important_corrs[key]) for key in important_corrs]))
        , columns=['Attribute Pair', 'Correlation'])
    unique_important_corrs = unique_important_corrs.ix[
        abs(unique_important_corrs['Correlation']).argsort()[::-1]]
    print(unique_important_corrs)
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    fig, ax = plt.subplots(figsize=(15, 6))  # 创建一个图和一组子图,返回图的对象、轴对象的数组
    ind = np.linspace(0, len(unique_important_corrs), len(unique_important_corrs))
    bars = ax.bar(ind, np.array(unique_important_corrs['Correlation']), color='red',
                  edgecolor='black')  # 给定xy坐标，做一个条形图, 返回柱状图容器
    for bar in bars:  # 显示柱子的值
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height + 0.01, round(height, 3), ha='center', va='bottom')
    ax.set_xticks(ind)
    ax.set_xticklabels(unique_important_corrs['Attribute Pair'], rotation=10)  # 设置x轴标签
    ax.set_title("所有变量间的共线性")
    plt.show()


if __name__ == '__main__':
    file = "..\\data\\1entbase.csv"
    # all_columns = ['销售日期', '卧室数', '浴室数', '房屋面积', '停车面积', '楼层数', '房屋评分',
    #                '建筑面积', '地下室面积', '建筑年份', '修复年份', '纬度', '经度']
    # continuous_columns = ['销售日期', '房屋面积', '停车面积', '建筑面积', '地下室面积', '建筑年份', '纬度', '经度']
    # separated_columns = ['卧室数', '浴室数', '楼层数', '房屋评分', '修复年份']
    df = pd.read_csv(file)
    # df = pd.read_csv(file, usecols=all_columns)
    allvars_collinearity(df)
    # continuous_vars_collinearity(df, continuous_columns)
    # separated_vars_collinearity(df, separated_columns)
