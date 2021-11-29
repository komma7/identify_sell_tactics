import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
member_tag = pd.read_csv("/Users/yinmengzi/Desktop/datasets/data/history_loan_data.csv")
# print(member_tag.head())
# print([i for i in member_tag])
# 除了上次贷款迄今时长是越短/少越好，其余的FM+R都是越多/高越好，因此按照下面给定标签
member_tag['上次贷款迄今时长_评分'] = pd.qcut(member_tag['上次贷款迄今时长'], q=5, duplicates='drop', labels=range(5, 0, -1)).astype(int)
member_tag['最近两年借款次数_评分'] = pd.qcut(member_tag['最近两年借款次数'], q=5, duplicates='drop', labels=range(2, 6)).astype(int)
member_tag['最近两年贷款金额总额_评分'] = pd.qcut(member_tag['最近两年贷款金额总额'], q=5, duplicates='drop', labels=range(1, 6)).astype(int)
member_tag['最近两年正常还款次数_评分'] = pd.qcut(member_tag['最近两年正常还款次数'], q=5, duplicates='drop', labels=[1, 5]).astype(int)
print(member_tag.head())
member_tag.loc[:, '用户分类'] = '其他'
member_tag.loc[(member_tag['上次贷款迄今时长_评分']==1) & (member_tag['最近两年借款次数_评分']==2) & \
     (member_tag['最近两年贷款金额总额_评分']==1) & (member_tag['最近两年正常还款次数_评分']==1), '用户分类'] = '一般挽留用户'
member_tag.loc[(member_tag['上次贷款迄今时长_评分']==2) & (member_tag['最近两年借款次数_评分']==2) & \
     (member_tag['最近两年贷款金额总额_评分']>=1) & (member_tag['最近两年正常还款次数_评分']==1), '用户分类'] = '一般发展用户'

member_tag.loc[(member_tag['上次贷款迄今时长_评分']==2) & (member_tag['最近两年借款次数_评分']>=3) & \
     (member_tag['最近两年贷款金额总额_评分']>=2) & (member_tag['最近两年正常还款次数_评分']==1), '用户分类'] = '一般保持用户'
member_tag.loc[(member_tag['上次贷款迄今时长_评分']>=2) & (member_tag['最近两年借款次数_评分']>=2) & \
     (member_tag['最近两年贷款金额总额_评分']>=2) & (member_tag['最近两年正常还款次数_评分']>=3), '用户分类'] = '一般价值用户'

member_tag.loc[(member_tag['上次贷款迄今时长_评分']==1) & (member_tag['最近两年借款次数_评分']>=3) & \
     (member_tag['最近两年贷款金额总额_评分']>=3) & (member_tag['最近两年正常还款次数_评分']>=3), '用户分类'] = '重要挽留用户'

member_tag.loc[(member_tag['上次贷款迄今时长_评分']>=3) & (member_tag['最近两年借款次数_评分']>=2) & \
     (member_tag['最近两年贷款金额总额_评分']>=3) & (member_tag['最近两年正常还款次数_评分']>=3), '用户分类'] = '重要发展用户'
member_tag.loc[(member_tag['上次贷款迄今时长_评分']>=2) & (member_tag['最近两年借款次数_评分']>=4) & \
     (member_tag['最近两年贷款金额总额_评分']>=3) & (member_tag['最近两年正常还款次数_评分']>=3), '用户分类'] = '重要保持用户'

member_tag.loc[(member_tag['上次贷款迄今时长_评分']>=3) & (member_tag['最近两年借款次数_评分']>=4) & \
     (member_tag['最近两年贷款金额总额_评分']>=3) & (member_tag['最近两年正常还款次数_评分']>=3), '用户分类'] = '重要价值用户'
print(member_tag['用户分类'].value_counts())
member_tag['用户分类'].value_counts()
# member_tag.reset_index().to_csv('./datasets/data/member_tag.csv', index=None)
member_tag.reset_index().to_csv("/Users/yinmengzi/Desktop/datasets/data/member_tag.csv", index=None)