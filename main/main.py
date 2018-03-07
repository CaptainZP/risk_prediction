import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import ExtraTreesClassifier
from feature_extract.before.missing_data_address import missing_data_statistics, missing_data_complement, delete_nacol
from collections import Counter
from sklearn import preprocessing
from imblearn.under_sampling import RandomUnderSampler, NearMiss


# 所需文件
input_path = "..\\data\\"
output_path = "..\\result\\"
data_all_file = "alltable_1_add"
train_target_file = "train"
predict_target_file = "evaluation_public"
result_file = "result_main_11_23_1"

# 读文件
data_all = pd.read_csv(input_path + data_all_file + '.csv')
data_all = data_all.drop('TARGET', axis=1)
print('特征行列大小：', data_all.shape)
# # 缺失值情况
# nan_info = missing_data_statistics(data_all)
# print('缺失值信息:\n', nan_info)
# # 删除高缺失率特征
# data_all = delete_nacol(data_all)
# print('删除后特征行列大小：', data_all.shape)

# 一些特征处理
data_all = data_all.fillna(0)  # 缺失值填充0
# data_all['ZCZB'] = preprocessing.scale(data_all['ZCZB'])  # 标准化
# data_all['ZCZB'] = np.log1p(data_all['ZCZB'])  # 做log处理
# data_all = data_all.drop(['HY_10', 'HY_11'], axis=1)  # 删除一些特征

# 获取特征和标签
train_target = pd.read_csv(input_path + train_target_file + '.csv')
predict_target = pd.read_csv(input_path + predict_target_file + '.csv')  # predict EID
train_feature = pd.merge(train_target, data_all, how='left', on='EID').drop('TARGET', axis=1)
test_feature = pd.merge(predict_target, data_all, how='left', on='EID')
# 再做一些特征处理
index = train_feature[train_feature['ZCZB'].isnull() == True].index  # 有这个操作会报错, 会删除预测的EID
train_feature = train_feature.drop(index)  # 删除无ZCZB的样本
# 获取
train = train_feature  # 训练集特征
label = train_target['TARGET']  # 训练集标签
test = test_feature  # 测试集特征

# 划分测试集和训练集,前2特征,后2标签
x_train, y_train, x_validation, y_validation = train_test_split(train, label, test_size=0.3, random_state=10000)

# 开始训练
# clf = SVC(probability=True)
# clf = SGDClassifier(loss='log')
# clf = XGBClassifier()
# clf = ExtraTreesClassifier()
clf = DecisionTreeClassifier()
clf.fit(x_train, x_validation)
y_train_pred = clf.predict(y_train)   # 测试集预测正数组
y_train_scores = clf.predict_proba(y_train)  # 估计为正例的概率
auc = roc_auc_score(y_validation, y_train_scores[:, 1])
print('auc=', auc)

# 开始预测
y_pred = clf.predict(test)   # 测试集预测正数组
y_scores = clf.predict_proba(test)  # 估计为正例的概率
predict_target['FORTARGET'] = y_pred  # 预测的标签
predict_target['PROB'] = y_scores  # 预测为正概率
predict_target.to_csv(output_path + result_file + '.csv', index=False)
print('train label number:{}'.format(Counter(label)[0]*1.0/Counter(label)[1]))
print('test label number:{}'.format(Counter(predict_target['FORTARGET'])[0] * 1.0 / Counter(predict_target['FORTARGET'])[1]))

