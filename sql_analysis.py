import pandas as pd
import sqlite3

# 1. 读取清洗好的数据
df = pd.read_csv('cleaned_user_behavior.csv')
print("原始数据行数：", len(df))

# 2. 连接 SQLite 数据库（自动创建 ecommerce.db 文件）
conn = sqlite3.connect('ecommerce.db')

# 3. 把数据存入 SQLite 表
df.to_sql('behavior', conn, if_exists='replace', index=False)
print("数据已存入 SQLite 数据库")

# 4. SQL 查询1：每天 PV 和 UV
query_daily = """
SELECT date,
       COUNT(CASE WHEN behavior_type='pv' THEN 1 END) AS pv,
       COUNT(DISTINCT CASE WHEN behavior_type='pv' THEN user_id END) AS uv
FROM behavior
GROUP BY date
ORDER BY date
LIMIT 10;
"""
daily = pd.read_sql(query_daily, conn)
print("\n每日PV和UV（前10天）：")
print(daily)

# 5. SQL 查询2：每小时 PV 分布
query_hourly = """
SELECT hour,
       COUNT(*) AS pv_count
FROM behavior
WHERE behavior_type='pv'
GROUP BY hour
ORDER BY hour;
"""
hourly = pd.read_sql(query_hourly, conn)
print("\n每小时PV分布：")
print(hourly)

# 6. SQL 查询3：转化率（浏览→购买）
query_conversion = """
WITH user_flag AS (
    SELECT user_id,
           MAX(CASE WHEN behavior_type='pv' THEN 1 ELSE 0 END) AS has_pv,
           MAX(CASE WHEN behavior_type='buy' THEN 1 ELSE 0 END) AS has_buy
    FROM behavior
    GROUP BY user_id
)
SELECT 
    SUM(has_pv) AS total_pv_users,
    SUM(has_buy) AS total_buy_users,
    ROUND(SUM(has_buy)*1.0 / SUM(has_pv), 4) AS conversion_rate
FROM user_flag;
"""
conversion = pd.read_sql(query_conversion, conn)
print("\n转化率：")
print(conversion)

# 7. 关闭连接
conn.close()

# 8. 把结果保存为 CSV
daily.to_csv('daily_pv_uv.csv', index=False)
hourly.to_csv('hourly_pv.csv', index=False)
conversion.to_csv('conversion_rate.csv', index=False)
print("\n三个结果文件已保存：daily_pv_uv.csv, hourly_pv.csv, conversion_rate.csv")