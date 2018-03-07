from collections import Counter

import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split

from feature_extract.before.missing_data_address import missing_data_complement


print('\n文件缺失值信息与处理............')
all_features = pd.read_csv("..\\data\\alltable_1_add.csv")
all_features = all_features.drop(['TARGET', 'ENDDATE'], axis=1)
# na_info = missing_data_statistics(all_features)  # 打印缺失值信息
# print('缺失值信息:\n', na_info)
# all_features = delete_nacol(all_features)  # 删除高缺失值的列结果变低

all_features = missing_data_complement(all_features)  # 数值缺失填充0 = all_features.fillna(0)
# all_features = all_features[all_features.ZCZB != 0]  # 去除注册资本为0的样本
# all_features['ZCZB'] = all_features['ZCZB'].fillna(all_features['ZCZB'].mean())  # 注册资本用均值填充

print('\n求两文件特征与标签............')
train_target = pd.read_csv("..\\data\\train.csv")
test_target = pd.read_csv("..\\data\\evaluation_public.csv")
train_feature = pd.merge(train_target, all_features, how='left', on='EID')  # 获取训练集的特征
test_feature = pd.merge(test_target, all_features, how='left', on='EID')  # 获取测试集的特征
# 删除EID
train_feature = train_feature.drop('EID', axis=1)
test_feature = test_feature.drop('EID', axis=1)
# 获取
train = train_feature.drop(['TARGET', 'ENDDATE'], axis=1)  # 训练集特征
label = train_target['TARGET']  # 训练集标签
test = test_feature  # 测试集特征

# # temp增加处理
# index = train_feature[train_feature['ZCZB'].isnull() == True].index
# train_feature = train_feature.drop(index)
# train_target = train_target.drop(index)
# train_feature['ZCZB'] = train_feature['ZCZB'] + (train_feature['RGYEAR'].max() - train_feature['RGYEAR'])
# test_feature['ZCZB'] = test_feature['ZCZB'] + (test_feature['RGYEAR'].max() - test_feature['RGYEAR'])
# train_feature['zczb&finzb'] = train_feature['ZCZB'] - train_feature['FINZB']/10000
# test_feature['zczb&finzb'] = test_feature['ZCZB'] - test_feature['FINZB']/10000
# train_feature['to_now'] = 2015 - train_feature['RGYEAR']
# test_feature['to_now'] = 2017 - test_feature['RGYEAR']

print('\n划分测试集训练集............')
x_train, x_test, y_train, y_test = train_test_split(train, label, test_size=0.3, random_state=10000)

print('\n测试与预测............')
xgb_all = xgb.DMatrix(train, label=label)
xgb_train = xgb.DMatrix(x_train, label=y_train)
xgb_eval = xgb.DMatrix(x_test, label=y_test)
params = {
    # 通用参数
    'booster': 'gbtree',              # 每次迭代的模型
    'silent': 1,                      # 输出信息
    # booster参数
    'eta': 0.02,                      # 默认0.3,与learning rate类似，减少每一步的权重，可以提高模型的鲁棒性，典型值为0.01-0.2
    'max_depth': 9,                   # 默认6,树的最大深度，用来避免过拟合的。max_depth越大，模型会学到更具体更局部的样本。需要使用CV函数来进行调优。典型值：3-10
    'min_child_weight': 4,            # 默认1，最小叶子节点样本权重和，用于避免过拟合。当它的值较大时，可以避免模型学习到局部的特殊样本，值过高，会导致欠拟合。
    'gamma': 0,                       # 默认0,分裂后损失函数的值下降了才会分裂这个节点,指定了节点分裂所需的最小损失函数下降值。值越大，算法越保守,和损失函数息息相关，所以是需要调整的。
    'subsample': 0.8,                 # 默认1,控制对于每棵树随机采样的比例。减小这个参数的值，算法会更加保守，避免过拟合。但是如果这个值设置得过小，它可能会导致欠拟合。典型值：0.5-1
    'colsample_bytree': 0.8,          # 默认1,用来控制每棵随机采样的列数的占比(每一列是一个特征)。典型值：0.5-1
    'lambda': 2,                      # 默认1,权重的L2正则化项。(和Ridge regression类似)。这个参数是用来控制XGBoost的正则化部分的
    'alpha': 1,                       # 默认1,权重的L1正则化项。(和Lasso regression类似)。可以应用在很高维度的情况下，使得算法的速度更快
    # 学习目标参数
    'objective': 'binary:logistic',   # 这个参数定义需要被最小化的损失函数
    'eval_metric': 'auc',             # 度量方法
    'seed': 0                         # 默认0
}
print('Start training............')
eval_list = [(xgb_eval, 'val')]

# 使用cv
# bst = xgb.cv(params, xgb_all, num_boost_round=1000, nfold=5, stratified=True, metrics='auc', early_stopping_rounds=30)
# print(bst['test-auc-mean'])
# gbm = xgb.train(
#     params,
#     xgb_train,
#     num_boost_round=len(bst['test-auc-mean']),
#     evals=eval_list,
#     early_stopping_rounds=30
# )

# 不使用cv，直接使用调好的参数
gbm = xgb.train(params, xgb_train, num_boost_round=1000, evals=eval_list, early_stopping_rounds=30)

# 调参
# param_test = {
#     'learning_rate': [0.01, 0.05, 0.1, 0.3, 0.5],
#     'max_depth': [4, 6, 9, 11],
#     'min_child_weight': [2, 4, 6, 10],
#     'gamma': [0, 0.1, 0.3],
#     'subsample': [0.7, 0.8, 0.9, 1],
#     'colsample_bytree': [0.7, 0.8, 0.9, 1],
#     'reg_lambda': [0.1, 0.01, 1, 10, 100],
#     'reg_alpha': [0.1, 0.01, 1, 10, 100]
# }
# gsearch = GridSearchCV(
#     estimator=XGBClassifier(
#         learning_rate=0.05,
#         n_estimators=1000,
#         max_depth=9,
#         min_child_weight=4,
#         gamma=0,
#         subsample=0.8,
#         colsample_bytree=0.8,
#         reg_lambda=1,
#         objective='binary:logistic',
#         nthread=6),
#     param_grid=param_test,
#     scoring='roc_auc',
#     n_jobs=1,
#     cv=StratifiedKFold(n_splits=5,  shuffle=True)
# )
# gsearch.fit(x_test, y_test)
# print('cv result:\n', gsearch.grid_scores_, gsearch.best_params_, gsearch.best_score_)

print("best best_score", gbm.best_score)
print("best best_iteration", gbm.best_iteration)
print("best best_ntree_limit", gbm.best_ntree_limit)

print('Start predicting............')
test_feature = xgb.DMatrix(test_feature)
y_pred = gbm.predict(test_feature, ntree_limit=gbm.best_iteration)
test_target['FORTARGET'] = y_pred
test_target['FORTARGET'] = test_target['FORTARGET'].apply(lambda x: 1 if x > 0.22 else 0)  # test_target是DataFrame
test_target['PROB'] = y_pred
test_target.to_csv("..\\result\\result_xgb_11_23_1.csv", index=False)
print('train label number:{}'.format(Counter(label)[0]*1.0/Counter(label)[1]))
print('test label number:{}'.format(Counter(test_target['FORTARGET'])[0]*1.0/Counter(test_target['FORTARGET'])[1]))

