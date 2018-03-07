import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

print('\n文件缺失值信息与处理............')
all_features = pd.read_csv("data\\all_11_1_add.csv").drop('TARGET', axis=1)

all_features = all_features.fillna(0)  # 数值缺失填充0 = all_features.fillna(0)


print('\n求两文件特征与标签............')
train_target = pd.read_csv('data\\train.csv')
test_target = pd.read_csv('data\\evaluation_public.csv')

train_feature = pd.merge(train_target, all_features, how='left', on='EID').drop(['TARGET'], axis=1)  # 获取训练集的特征
train_label = train_target['TARGET']  # 获取训练集的标签
test_feature = pd.merge(test_target, all_features, how='left', on='EID')  # 获取测试集的特征


print('\n划分测试集训练集............')
x_train, x_test, y_train, y_test = train_test_split(train_feature, train_label, test_size=0.3, random_state=10000)

gbm = GradientBoostingClassifier(n_estimators=10, learning_rate=0.01, max_depth=9, subsample=0.8, random_state=100)
gbm.fit(x_train, y_train)
y_pred = gbm.predict(x_test)   # 测试集预测正负结果数组
y_scores = gbm.predict_proba(x_test)  # 估计为正例的概率
auc = roc_auc_score(y_test, y_scores[:, 1])
print('auc = {}'.format(auc))
