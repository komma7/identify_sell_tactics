import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
data = pd.read_csv('/Users/yinmengzi/Desktop/datasets/data/history_loan_data.csv')
member_tag = data.groupby('用户ID')['日期'].max().to_frame()
member_tag.columns = ['最近一次借款的日期']

member_tag['最近两年借款次数'] = data.groupby('用户ID')['日期'].count()
member_tag['最近两年贷款金额总额'] = data.groupby('用户ID')['贷款金额'].sum()
member_tag[['最近两年正常还款次数', '最近两年逾期率']] = data.groupby('用户ID')['还款标签'].agg([np.sum, np.mean])

member_tag['最近一次借款的日期'] = pd.to_datetime(member_tag['最近一次借款的日期'])
time_diff_max = member_tag['最近一次借款的日期'].max()
member_tag['上次贷款迄今时长'] = member_tag['最近一次借款的日期'].map(lambda x: (time_diff_max - x).days)

def plot_corr(df):
    f, ax = plt.subplots(figsize=[2.5 * df.shape[1], 2 * df.shape[1]])
    corr = df.corr()
    sns.heatmap(corr,
                mask=np.zeros_like(corr, dtype=np.bool),
                square=True,
                ax=ax)
plot_corr(member_tag[['上次贷款迄今时长', '最近两年借款次数', '最近两年贷款金额总额', '最近两年正常还款次数']])

member_tag['上次贷款迄今时长'].hist()
member_tag['最近两年借款次数'].hist()
member_tag['最近两年贷款金额总额'].hist()
member_tag['最近两年正常还款次数'].hist()

member_tag['上次贷款迄今时长_评分'] = pd.qcut(member_tag['上次贷款迄今时长'], q=5, duplicates='drop')
member_tag['最近两年借款次数_评分'] = pd.qcut(member_tag['最近两年借款次数'], q=5, duplicates='drop')
member_tag['最近两年贷款金额总额_评分'] = pd.qcut(member_tag['最近两年贷款金额总额'], q=5, duplicates='drop')
member_tag['最近两年正常还款次数_评分'] = pd.qcut(member_tag['最近两年正常还款次数'], q=5, duplicates='drop')

print('对“上次贷款迄今时长”进行等频分箱能分出%d箱' % member_tag['上次贷款迄今时长_评分'].nunique())
print('\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n查看“上次贷款迄今时长”分箱结果和最近两年逾期率的关系')
member_tag.groupby(['上次贷款迄今时长_评分'])['最近两年逾期率'].mean().sort_index()

print('对“最近两年借款次数”进行等频分箱能分出%d箱' % member_tag['最近两年借款次数_评分'].nunique())
print('\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n查看“最近两年借款次数”分箱结果和最近两年逾期率的关系')
member_tag.groupby(['最近两年借款次数_评分'])['最近两年逾期率'].mean().sort_index()

print('对“最近两年贷款金额总额”进行等频分箱能分出%d箱' % member_tag['最近两年贷款金额总额_评分'].nunique())
print('\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n查看“最近两年贷款金额总额”分箱结果和最近两年逾期率的关系')
member_tag.groupby(['最近两年贷款金额总额_评分'])['最近两年逾期率'].mean().sort_index()

print('对“最近两年正常还款次数”进行等频分箱能分出%d箱' % member_tag['最近两年正常还款次数_评分'].nunique())
print('\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n查看“最近两年正常还款次数”分箱结果和最近两年逾期率的关系')
member_tag.groupby(['最近两年正常还款次数_评分'])['最近两年逾期率'].mean().sort_index()
