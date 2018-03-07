import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from collections import Counter
from sklearn import preprocessing
from imblearn.under_sampling import RandomUnderSampler, NearMiss
from imblearn.over_sampling import SMOTE

# 所需文件
input_path = "..\\data\\"
output_path = "..\\result\\"
data_all_file = "1entbase_add"
train_target_file = "train"
test_target_file = "evaluation_public"
result_file = "result_lgm_11_23_1"

# read data
data_all = pd.read_csv("..\\data\\1entbase_add.csv")
# data_all = data_all.drop('TARGET', axis=1)

# 做一些特征处理
data_all = data_all.fillna(0)  # 缺失值填充0
# data_all['ZCZB'] = preprocessing.scale(data_all['ZCZB'])  # 标准化
# data_all['ZCZB'] = np.log1p(data_all['ZCZB'])  # 做log处理
# data_all = data_all.drop(['HY_10', 'HY_11'], axis=1)  # 删除一些特征

# # 获取特征和标签
train_target = pd.read_csv("..\\data\\train.csv")
test_target = pd.read_csv("..\\data\\evaluation_public.csv")
train_feature = pd.merge(train_target, data_all, how='left', on='EID').drop('TARGET', axis=1)
test_feature = pd.merge(test_target, data_all, how='left', on='EID')
# 删除EID
train_feature = train_feature.drop('EID', axis=1)
test_feature = test_feature.drop('EID', axis=1)

# 特征再做一些处理
index = train_feature[train_feature['ZCZB'].isnull() == True].index  # 删除无ZCZB的样本，会删除预测EID
train_feature = train_feature.drop(index)
# 增加再做一些特征处理
# train_feature['ZCZB'] = train_feature['ZCZB'] + (train_feature['RGYEAR'].max() - train_feature['RGYEAR'])
# test_feature['ZCZB'] = test_feature['ZCZB'] + (test_feature['RGYEAR'].max() - test_feature['RGYEAR'])
# train_feature['zczb&finzb'] = train_feature['ZCZB'] - train_feature['FINZB']/10000
# test_feature['zczb&finzb'] = test_feature['ZCZB'] - test_feature['FINZB']/10000
# train_feature['to_now'] = 2015 - train_feature['RGYEAR']
# test_feature['to_now'] = 2017 - test_feature['RGYEAR']

# 获取
train = train_feature  # 训练集特征
label = train_target['TARGET']  # 训练集标签
test = test_feature  # 测试集特征

# # 升降采样
# rus = SMOTE(kind='borderline1')   # nearmiss降采样version = 1,2,3
# train, label = rus.fit_sample(train, label)

# 划分测试集和训练集,前2特征,后2标签
x_train, y_train, x_validation, y_validation = train_test_split(train, label, test_size=0.3, random_state=10000)

params = {
    'task': 'train',
    'boosting': 'gbdt',
    'objective': 'binary',
    'metric': {'auc'},
    'num_leaves': 64,
    'learning_rate': 0.01,
    'verbose': 0,
    'subsample': 0.8,
    'min_data_in_leaf': 60,
    'feature_fraction': 0.8,  # 原0.9
    'lambda_l1': 2.9,  # 原2
    'lambda_l2': 1,
    'bagging_fraction': 0.8,
    'bagging_freq': 5,
    'num_threads': 4,
}
# params = {
#     'task': 'train',
#     'boosting': 'gbdt',
#     'objective': 'binary',
#     'metric': {'auc', },
#     'num_leaves': 64,
#     'learning_rate': 0.01,
#     'min_data_in_leaf': 60,
#     'min_sum_hessian_in_leaf': 10,
#     'lambda_l1': 2.9,
#     'lambda_l2': 1,
#     'bagging_fraction': 0.8,
#     'bagging_freq': 5,
#     'feature_fraction': 0.8,
#     'verbose': 0,
#     'subsample': 0.8,
#     'num_threads': 4,
#     # 'is_unbalance': True,
# }
print('Start training...')
# lgb_train = lgb.Dataset(x_train, x_validation, categorical_feature=['HY', 'ETYPE'])
# lgb_eval = lgb.Dataset(y_train, y_validation, categorical_feature=['HY', 'ETYPE'])
lgb_train = lgb.Dataset(x_train, x_validation)
lgb_eval = lgb.Dataset(y_train, y_validation)
gbm = lgb.train(params, lgb_train, num_boost_round=1500, valid_sets=lgb_eval, early_stopping_rounds=30)


# 使用cv要注释掉上面的lgb.train
# print('Start cv...')
# # data for validation :not split any more
# X_train_1 = pd.concat([X_train, y_train])
# y_label = pd.concat([X_validation, y_validation])
# lgb_train = lgb.Dataset(X_train_1, label=y_label)
# bst = lgb.cv(params, lgb_train, num_boost_round=1500, nfold=5, stratified=True, early_stopping_rounds=30)
# print(len(bst['auc-mean']))
# print(bst['auc-mean'])
# gbm = lgb.train(params, lgb_train, num_boost_round=len(bst['auc-mean']))

# --------------------------预测----------------------------
# y_pred = gbm.predict(test, num_iteration=gbm.best_iteration)
# test_target['FORTARGET'] = y_pred
# # auc根据预测的概率算的，调划分阈值只会影响f1，对结果前三位没影响
# test_target['FORTARGET'] = test_target['FORTARGET'].apply(lambda x: 1 if x > 0.22 else 0)
# test_target['PROB'] = y_pred
# test_target.to_csv(output_path + result_file + '.csv', index=False)
# print('train label number:{}'.format(Counter(label)[0]*1.0/Counter(label)[1]))
# print('test label number:{}'.format(Counter(test_target['FORTARGET'])[0]*1.0/Counter(test_target['FORTARGET'])[1]))
#
# print('Calculate feature importance...')
# print('num of feature:', len(gbm.feature_name()))
# print('Feature name:', gbm.feature_name())
# print('Feature importance:', list(gbm.feature_importance()))

