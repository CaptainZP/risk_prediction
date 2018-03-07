import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from lightgbm import LGBMClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier


# 特征总文件
all_features = pd.read_csv("..\\data\\alltable_12_5_3.csv")
# all_features = all_features.drop(['TARGET', 'ENDDATE'], axis=1)
all_features = all_features.fillna(0)

# 特征与标签
train_file = pd.read_csv("..\\data\\train.csv")
evaluation_file = pd.read_csv("..\\data\\evaluation_public.csv")
train_feature = pd.merge(train_file, all_features, how='left', on='EID')  # 训练文件特征
test_feature = pd.merge(evaluation_file, all_features, how='left', on='EID')  # 测试文件特征
train_feature = train_feature.drop('EID', axis=1)  # 删除EID
test_feature = test_feature.drop('EID', axis=1)
train = train_feature.drop(['TARGET', 'ENDDATE'], axis=1)
label = train_file['TARGET']

# 划分测试集训练集
train_X, test_X, train_y, test_y = train_test_split(train.values, label.values, test_size=0.3, random_state=10000)

# stacking配置
train_size = train_X.shape[0]
test_size = test_X.shape[0]
seed = 0
nfold = 4
kf = KFold(n_splits=nfold, random_state=seed, shuffle=False)


def get_level1_predict(clf, train_X, train_y, test_X):
    oof_train = np.zeros((train_size,))  # 放level 1所有的预测值
    oof_test = np.zeros((test_size,))  # 放平均的测试集结果
    oof_test_skf = np.empty((nfold, test_size))

    for i, (train_index, test_index) in enumerate(kf.split(train_X)):  # 对训练集的每一份进行操作
        train_X_fold = train_X[train_index]  # part1特征
        test_X_fold = train_X[test_index]  # part2特征
        train_y_fold = train_y[train_index]  # part1标签

        clf.fit(train_X_fold, train_y_fold)
        oof_train[test_index] = clf.predict(test_X_fold)  # 训练集预测一折
        oof_test_skf[i, :] = clf.predict(test_X)  # 预测所有测试集

    oof_test[:] = oof_test_skf.mean(axis=0)  # 预测所有测试集取平均，一行
    return oof_train.reshape(-1, 1), oof_test.reshape(-1, 1)  # 变一列


# gbm1 = LGBMClassifier(boosting_type='gbdt', num_leaves=64, min_child_samples=40, max_depth=14, learning_rate=0.01, n_estimators=1000,
#                      objective='binary', subsample=0.8, subsample_freq=5, colsample_bytree=0.8, reg_alpha=3,
#                      reg_lambda=1, random_state=0, n_jobs=4, silent=False)
# gbm2 = LGBMClassifier(boosting_type='gbdt', num_leaves=64, min_child_samples=50, max_depth=9, learning_rate=0.01, n_estimators=1000,
#                      objective='binary', subsample=0.8, subsample_freq=5, colsample_bytree=0.8, reg_alpha=3,
#                      reg_lambda=1, random_state=10, n_jobs=4, silent=False)
# gbm3 = LGBMClassifier(boosting_type='gbdt', num_leaves=64, min_child_samples=40, max_depth=14, learning_rate=0.01, n_estimators=1000,
#                      objective='binary', subsample=0.8, subsample_freq=5, colsample_bytree=0.8, reg_alpha=3,
#                      reg_lambda=1, random_state=100, n_jobs=4, silent=False)
# gbm4 = LGBMClassifier(boosting_type='gbdt', num_leaves=64, min_child_samples=50, max_depth=9, learning_rate=0.01, n_estimators=1000,
#                      objective='binary', subsample=0.8, subsample_freq=5, colsample_bytree=0.8, reg_alpha=3,
#                      reg_lambda=1, random_state=1000, n_jobs=4, silent=False)
gbm1 = RandomForestClassifier(n_estimators=500, warm_start=True, max_features='sqrt', max_depth=6, min_samples_split=3, min_samples_leaf=2, n_jobs=-1, verbose=0)
gbm2 = GradientBoostingClassifier(n_estimators=500, learning_rate=0.008, min_samples_split=3, min_samples_leaf=2, max_depth=5, verbose=0)
gbm3 = DecisionTreeClassifier(max_depth=8)
gbm4 = ExtraTreesClassifier()
oof_train1, oof_test1 = get_level1_predict(gbm1, train_X, train_y, test_X)
oof_train2, oof_test2 = get_level1_predict(gbm2, train_X, train_y, test_X)
oof_train3, oof_test3 = get_level1_predict(gbm3, train_X, train_y, test_X)
oof_train4, oof_test4 = get_level1_predict(gbm4, train_X, train_y, test_X)
train_X = np.concatenate((oof_train1, oof_train2, oof_train3, oof_train4), axis=1)
test_X = np.concatenate((oof_test1, oof_test2, oof_test3, oof_test4), axis=1)

# 测试
xgb_train = xgb.DMatrix(train_X, label=train_y)
xgb_eval = xgb.DMatrix(test_X, label=test_y)
eval_list = [(xgb_eval, 'val')]
params = {
    # 通用参数
    'booster': 'gbtree',              # 每次迭代的模型
    'silent': 1,                      # 输出信息
    # booster参数
    'eta': 0.01,                      # 默认0.3,与learning rate类似，减少每一步的权重，可以提高模型的鲁棒性，典型值为0.01-0.2
    'max_depth': 9,                   # 默认6,树的最大深度，用来避免过拟合的。max_depth越大，模型会学到更具体更局部的样本。需要使用CV函数来进行调优。典型值：3-10
    'min_child_weight': 4,            # 默认1，最小叶子节点样本权重和，用于避免过拟合。当它的值较大时，可以避免模型学习到局部的特殊样本，值过高，会导致欠拟合。
    'gamma': 0,                       # 默认0,分裂后损失函数的值下降了才会分裂这个节点,指定了节点分裂所需的最小损失函数下降值。值越大，算法越保守,和损失函数息息相关，所以是需要调整的。
    'subsample': 0.8,                 # 默认1,控制对于每棵树随机采样的比例。减小这个参数的值，算法会更加保守，避免过拟合。但是如果这个值设置得过小，它可能会导致欠拟合。典型值：0.5-1
    'colsample_bytree': 0.8,          # 默认1,用来控制每棵随机采样的列数的占比(每一列是一个特征)。典型值：0.5-1
    'lambda': 1.5,                      # 默认1,权重的L2正则化项。(和Ridge regression类似)。这个参数是用来控制XGBoost的正则化部分的
    'alpha': 1,                       # 默认1,权重的L1正则化项。(和Lasso regression类似)。可以应用在很高维度的情况下，使得算法的速度更快
    # 学习目标参数
    'objective': 'binary:logistic',   # 这个参数定义需要被最小化的损失函数
    'eval_metric': 'auc',             # 度量方法
    'seed': 0                         # 默认0
}
gbm = xgb.train(params, xgb_train, num_boost_round=1000, evals=eval_list, early_stopping_rounds=30)
print("best best_score", gbm.best_score)


