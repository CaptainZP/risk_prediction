import pandas as pd


def missing_data_statistics(df):
    '''
    统计所有行的缺失值的情况，包括个数和所占比率
    :param df: 原始dataframe
    :return na_info: 缺失值统计情况的dataframe
    '''
    na_count = df.isnull().sum().sort_values(ascending=False)  # 按na个数降序返回每一列na个数
    na_rate = na_count / len(df)  # 返回每一列na所占的比率
    na_info = pd.concat([na_count, na_rate], axis=1, keys=['count', 'ratio'])  # 格式化打印
    return na_info


def delete_nacol(df, thresh=0.95):
    '''
    删除na较多的列，一般缺失值超过15%即认为缺失过多可删除，但非一定
    :param df: 原始dataframe
    :param na_info: missing_data_statistics返回的缺失值统计dataframe
    :param thresh: 1-缺失值所占比率的阈值
    :return: 删除后的dataframe
    '''
    na_info = missing_data_statistics(df)
    df = df.drop(na_info[na_info['ratio'] > thresh].index, axis=1)
    return df


def delete_nasample(df, col):
    '''
    删除含有较少na的列的na所在的行
    :param df: 原始dataframe
    :param col: 需要删除的列
    :return: df 删除后dataframe
    '''
    df = df.drop(df.loc[df[col].isnull()].index)  # 删除较少na的列的na所在的行
    return df


def missing_data_complement(df):
    '''
    分别对数值型和非数值型列进行缺失值补全
    :param df: 原始dataframe
    :return: 无
    '''
    numerical_cols = [col for col in df.columns if df.dtypes[col] != 'object']
    categorical_cols = [col for col in df.columns if df.dtypes[col] == 'object']
    df[numerical_cols] = df[numerical_cols].fillna(0)  # 目前数值型缺失值取0,后分析后再优化
    for col in categorical_cols:
        df[col] = df[col].astype('category')
        if df[col].isnull().any():  # 返回此列是否有na
            df[col] = df[col].cat.add_categories(['MISSING'])
            df[col] = df[col].fillna('MISSING')
    return df


if __name__ == '__main__':
    table = "..\\data\\1entbase.csv"
    df = pd.read_csv(table)
    na_info = missing_data_statistics(df)
    print('na_info:\n', na_info)
    print(df.shape)
    df = delete_nacol(df)
    new_na_info = missing_data_statistics(df)
    print('new_na_info:\n', new_na_info)
    print(df.shape)
    df = delete_nasample(df, 'ZCZB')
    print(df.head(5))
    print(df.shape)
    df = missing_data_complement(df)
    print(df.head(5))
