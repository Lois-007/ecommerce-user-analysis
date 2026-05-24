# 导入 pandas 库，并简写为 pd
import pandas as pd

# 1. 读取 CSV，返回一个 DataFrame（类似 Excel 表格），因为第一行是列名，用 header=0
df = pd.read_csv('UserBehavior.csv', header=0, nrows=500000,encoding='gb18030')  # 先取50万行测试，如果内存够可以去掉 nrows

# 2. 重命名列
# 原列名: user_id, goods_id, category_id, behavior, timestamp, sex, address, device, price, amount, comment
# 建议保留原名，但 behavior 原代码用的是 'behavior_type'，统一一下
df.rename(columns={'behavior': 'behavior_type'}, inplace=True)

# 检查缺失值
print("缺失值统计：")
print(df[['user_id', 'timestamp', 'behavior_type']].isnull().sum())

# 3. 转换时间戳（单位：秒）
# pd.to_datetime(..., unit='s')：把秒数转换成正常的日期时间格式（例如 2024-05-29 14:03:05）。结果存入新列 datetime。
# df['datetime'].dt.date：从日期时间中提取日期部分（例如 2024-05-29），存入新列 date。
# 提取小时（0~23），存入新列 hour。
df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
df['date'] = df['datetime'].dt.date
df['hour'] = df['datetime'].dt.hour

# 4. 筛选合理的行为类型（只保留浏览(pv)、加购(cart)、收藏(fav)、购买(buy)。)
valid_behaviors = ['pv', 'cart', 'fav', 'buy']
df = df[df['behavior_type'].isin(valid_behaviors)]


# 5. 保存清洗后的文件（CSV 格式）
# 将清洗后的 DataFrame 保存为新的 CSV 文件，文件名 cleaned_user_behavior.csv。
# index=False：不保存行索引（避免多出一列无用的序号）。
# .tolist() 转换成 Python 列表。打印出来，方便你检查有哪些列。
# df.to_csv('cleaned_user_behavior.csv', index=False)
print("清洗完成，剩余行数：", df.shape[0])
print("字段列表：", df.columns.tolist())


