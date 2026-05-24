import pandas as pd

# 1. 读取 CSV（因为第一行是列名，用 header=0）
df = pd.read_csv('UserBehavior.csv', header=0, nrows=500000,encoding='gb18030')  # 先取50万行测试，如果内存够可以去掉 nrows

# 2. 重命名列（可选，为了后续代码更好写）
# 原列名: user_id, goods_id, category_id, behavior, timestamp, sex, address, device, price, amount, comment
# 建议保留原名，但 behavior 原代码用的是 'behavior_type'，统一一下
df.rename(columns={'behavior': 'behavior_type'}, inplace=True)

# 3. 转换时间戳（单位：秒）
df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
df['date'] = df['datetime'].dt.date
df['hour'] = df['datetime'].dt.hour

# 4. 筛选合理的行为类型（只保留 pv, cart, fav, buy）
valid_behaviors = ['pv', 'cart', 'fav', 'buy']
df = df[df['behavior_type'].isin(valid_behaviors)]

# 5. （可选）如果 price 或 amount 字段有缺失值，可以填充或删除，这里简单保留
# 如果后续分析不需要 sex, address, device, price, amount, comment，可以只保留核心列
# 但为了保留扩展性，先全部保留

# 6. 保存清洗后的文件（CSV 格式）
df.to_csv('cleaned_user_behavior.csv', index=False)
print("清洗完成，剩余行数：", df.shape[0])
print("字段列表：", df.columns.tolist())