import pandas as pd
missing_data = pd.read_csv('/Users/yinmengzi/Desktop/datasets/data/former_data.csv', encoding='gbk')
missing_data.head()
print(missing_data.shape)
drop_missing_data = missing_data.dropna() # 直接丢失含有缺失值的行记录
print(drop_missing_data.shape)
print(missing_data.info)
print(drop_missing_data.info)