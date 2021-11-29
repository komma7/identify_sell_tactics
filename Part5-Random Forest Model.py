import joblib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from model_evaluation import plot_all_figures
from imblearn.over_sampling import SMOTE

'''读入相关数据（在8-10part中有）'''
#导入历史数据
data = pd.read_csv('/Users/yinmengzi/Desktop/datasets/data/history_loan_data.csv')
#导入RFM特征和标签
member_tag = pd.read_csv('/Users/yinmengzi/Desktop/datasets/data/member_tag.csv')
#导入响应数据
response_label = pd.read_csv('/Users/yinmengzi/Desktop/datasets/data/response_label.csv')
#合并数据
member_tag = pd.merge(member_tag, response_label, left_on='用户ID', right_on='member_id', how='left')

'''样本准备'''
#样本准备
X = member_tag[['用户ID', '上次贷款迄今时长', '最近两年借款次数', '最近两年贷款金额总额', '最近两年正常还款次数', 'RFM分数']]
y = member_tag['response']
X_train,X_test,y_train,y_test = train_test_split(X, y, test_size = 0.3)
print('黑白样本的分布为：')
print(y_train.value_counts(normalize=True))

# 此处对样本进行SMOTE上采样。SMOTE(Synthetic Minority Oversampling Technique)是合成少数类过采样技术
smo = SMOTE(random_state=42)
print('\n经过SMOTE上采样前样本大小为%d' % X_train.shape[0])
# 经过SMOTE上采样前样本大小为147805
oversample = SMOTE()
X_smo, y_smo = oversample.fit_resample(X_train, y_train)
print('\n经过SMOTE上采样后样本大小为%d' % X_smo.shape[0])
# 经过SMOTE上采样后样本大小为244344
y_smo.value_counts()

# 模型训练
rf = RandomForestClassifier(n_estimators=300, max_depth=4)
rf.fit(X_train.drop(['用户ID'], axis=1), y_train)

X_smo['rf_prob'] = rf.predict_proba(X_smo.drop(['用户ID'], axis=1))[:, 1]
X_train['rf_prob'] = rf.predict_proba(X_train.drop(['用户ID'], axis=1))[:, 1]
X_test['rf_prob'] = rf.predict_proba(X_test.drop(['用户ID'], axis=1))[:, 1]

# 模型评估
plot_all_figures(X_train['rf_prob'], y_train, X_test['rf_prob'], y_test,
                 pred_test_value=None, real_test_label=None, pos_label=1,
                 fig_list=['roc', 'sort'], model_name='randomforest')
plt.show()

tmp = pd.concat([X_train, X_test])[['用户ID', 'rf_prob']]
# pd.concat()可以将数据根据不同的轴作简单的融合
member_tag = pd.merge(member_tag, tmp, on='用户ID')
# pd.merge()只能用于两个表的拼接，左右拼接，不能用于表的上下拼接
member_tag.head()
# head( )函数只能读取前五行数据

member_tag = member_tag[['用户ID', '上次贷款迄今时长_评分', '最近两年借款次数_评分', '最近两年贷款金额总额_评分',
                         '最近两年正常还款次数_评分', '用户分类', 'RFM分数', 'response', 'rf_prob']]
member_tag.columns = ['用户ID', 'Recency_score', 'Frequency_score', 'Monetary_score',
                      'Repayment_score', '用户分类', 'RFM_score', 'response', 'response_prob']
member_tag.head()

member_tag.to_excel('/Users/yinmengzi/Desktop/output.xlsx', index=None)

# 保存模型
save_m_file = '/Users/yinmengzi/Desktop/response_model.m'
joblib.dump(rf, save_m_file)

