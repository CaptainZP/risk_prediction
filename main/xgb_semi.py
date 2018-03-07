import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split


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
train_X, test_X, train_y, test_y = train_test_split(train, label, test_size=0.3, random_state=10000)

# 测试与预测
xgb_train = xgb.DMatrix(train_X, label=train_y)
xgb_eval = xgb.DMatrix(test_X, label=test_y)
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
eval_list = [(xgb_eval, 'val')]
gbm = xgb.train(params, xgb_train, num_boost_round=1000, evals=eval_list, early_stopping_rounds=30)
print("best best_score", gbm.best_score)

test_feature = xgb.DMatrix(test_feature)
pred = gbm.predict(test_feature, ntree_limit=gbm.best_iteration)
evaluation_file['FORTARGET'] = pred
evaluation_file['FORTARGET'] = evaluation_file['FORTARGET'].apply(lambda x: 1 if x > 0.22 else 0)
evaluation_file['PROB'] = pred
evaluation_file.to_csv("..\\result\\result_xgb_12_8_1.csv", index=False)

