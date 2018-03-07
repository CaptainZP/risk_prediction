import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from collections import Counter


# read data
data_all = pd.read_csv("..\\data\\alltable_12_5_2.csv")
# data_all = data_all.drop(['TARGET', 'ENDDATE'], axis=1)
data_all = data_all.fillna(0)  # 缺失值填充0

#
# data_all = data_all.drop(['3now_firststart'], axis=1)
# data_all = data_all.drop(['3now_firstend'], axis=1)
# data_all = data_all.drop(['3laststart_firstend'], axis=1)
# data_all = data_all.drop(['3lastend_firstend'], axis=1)
# data_all = data_all.drop(['3lastend_laststart'], axis=1)
# data_all = data_all.drop(['3lastend_firststart'], axis=1)

# data_all = data_all.drop(['4max_bt_interval'], axis=1)
# data_all = data_all.drop(['4min_bt_interval'], axis=1)
# data_all = data_all.drop(['4mean_bt_interval'], axis=1)
# data_all = data_all.drop(['4max_bt_startnum'], axis=1)
# data_all = data_all.drop(['4min_bt_startnum'], axis=1)
# data_all = data_all.drop(['4max_bt_endnum'], axis=1)
# data_all = data_all.drop(['4min_bt_endnum'], axis=1)

# 获取特征和标签
train_target = pd.read_csv("..\\data\\train.csv")
test_target = pd.read_csv("..\\data\\evaluation_public.csv")
train_feature = pd.merge(train_target, data_all, how='left', on='EID')
test_feature = pd.merge(test_target, data_all, how='left', on='EID')
# 删除EID
train_feature = train_feature.drop('EID', axis=1)
test_feature = test_feature.drop('EID', axis=1)
# 获取
train = train_feature.drop(['TARGET', 'ENDDATE'], axis=1)  # 训练集特征
label = train_target['TARGET']  # 训练集标签
test = test_feature  # 测试集特征


# 前2特征,后2标签
x_train, y_train, x_validation, y_validation = train_test_split(train, label, test_size=0.3, random_state=10000)

params = {
    'task': 'train',
    'boosting': 'gbdt',
    'objective': 'binary',
    'metric': {'auc', },
    'num_threads': 4,
    'learning_rate': 0.01,
    'num_leaves': 65,
    'max_depth': 15,
    'min_data_in_leaf': 60,
    'feature_fraction': 0.8,
    'bagging_fraction': 0.8,
    'bagging_freq': 5,
    'lambda_l1': 3,
    'lambda_l2': 2,
    'verbose': 0,
}
# params = {
#     'task': 'train',
#     'boosting': 'gbdt',
#     'objective': 'binary',
#     'metric': {'auc', },
#     'num_threads': 4,
#     'learning_rate': 0.01,
#     'num_leaves': 64,
#     'max_depth': 14,
#     'min_data_in_leaf': 60,
#     'feature_fraction': 0.8,
#     'bagging_fraction': 0.8,
#     'bagging_freq': 5,
#     'lambda_l1': 4,
#     'lambda_l2': 2,
#     'verbose': 0,
# }
# params = {
#     'task': 'train',
#     'boosting': 'gbdt',
#     'objective': 'binary',
#     'metric': {'auc', },
#     'num_threads': 4,
#     'learning_rate': 0.01,
#     'num_leaves': 64,
#     # 'max_depth': 14,
#     'min_data_in_leaf': 60,
#     'feature_fraction': 0.8,
#     'bagging_fraction': 0.8,
#     'bagging_freq': 5,
#     'lambda_l1': 2.9,
#     'lambda_l2': 1,
#     'verbose': 0,
# }
print('Start training...')
lgb_train = lgb.Dataset(x_train, x_validation)
lgb_eval = lgb.Dataset(y_train, y_validation)
gbm = lgb.train(params, lgb_train, num_boost_round=1500, valid_sets=lgb_eval, early_stopping_rounds=30)


# --------------------------预测----------------------------
y_pred = gbm.predict(test, num_iteration=gbm.best_iteration)
test_target['FORTARGET'] = y_pred
# auc根据预测的概率算的，调划分阈值只会影响f1，对结果前三位没影响
test_target['FORTARGET'] = test_target['FORTARGET'].apply(lambda x: 1 if x > 0.22 else 0)
test_target['PROB'] = y_pred
test_target.to_csv("..\\result\\result_lgm_12_8_1.csv", index=False)
print('train label number:{}'.format(Counter(label)[0]*1.0/Counter(label)[1]))
print('test label number:{}'.format(Counter(test_target['FORTARGET'])[0]*1.0/Counter(test_target['FORTARGET'])[1]))

importance = pd.DataFrame({'feature': gbm.feature_name(), 'importance': list(gbm.feature_importance())})
importance = importance.sort_values(['importance'], ascending=False)
importance.to_csv('..\\result\\result_lgm_12_8_importance.csv', index=False)

