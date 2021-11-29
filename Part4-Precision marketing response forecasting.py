import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
#导入历史数据
data = pd.read_csv('/Users/yinmengzi/Desktop/datasets/data/history_loan_data.csv')
#导入RFM特征和标签
member_tag = pd.read_csv('/Users/yinmengzi/Desktop/datasets/data/member_tag.csv')
#导入响应数据
response_label = pd.read_csv('/Users/yinmengzi/Desktop/datasets/data/response_label.csv')
print('营销的平均响应率为%.4f'%response_label['response'].mean())#输出营销平均响应率
#合并数据
member_tag = pd.merge(member_tag, response_label, left_on='用户ID', right_on='member_id', how='left')
#绘图
fig = plt.figure()
#上次贷款迄今时长_评分和Response关系绘图
ax1 = fig.add_subplot(2, 2, 1)  # 画2行2列个图形的第1个
ax1.set_xlabel('上次贷款迄今时长_评分')
ax1.set_ylabel('Proportion of Responders')
member_tag.groupby('上次贷款迄今时长_评分')['response'].mean().plot(kind = 'bar',colormap = 'Blues_r')
#最近两年借款次数_评分和响应情况关系
ax2 = fig.add_subplot(2, 2, 2)  # 画2行2列个图形的第2个
ax2.set_xlabel('最近两年借款次数_评分')
ax2.set_ylabel('Proportion of Responders')
member_tag.groupby('最近两年借款次数_评分')['response'].mean().plot(kind = 'bar',colormap = 'Blues_r')
#最近两年贷款金额总额_评分和响应情况关系
ax3 = fig.add_subplot(2, 2, 3)  # 画2行2列个图形的第3个
ax3.set_xlabel('最近两年贷款金额总额_评分')
ax3.set_ylabel('Proportion of Responders')
member_tag.groupby('最近两年贷款金额总额_评分')['response'].mean().plot(kind = 'bar',colormap = 'Blues_r')
#最近两年正常还款次数_评分和响应情况关系
ax4 = fig.add_subplot(2, 2, 4)  # 画2行2列个图形的第3个
ax4.set_xlabel('最近两年正常还款次数_评分')
ax4.set_ylabel('Proportion of Responders')
member_tag.groupby('最近两年正常还款次数_评分')['response'].mean().plot(kind = 'bar',colormap = 'Blues_r')
plt.show()
#用户分类和响应情况关系
tmp = member_tag.groupby('用户分类')['response'].mean().reset_index()
x = tmp['用户分类']
y = tmp['response']
fig = plt.figure(figsize=(12,6))
sns.barplot(x, y, palette="Blues_d")
plt.show()
