import pandas as pd
import matplotlib.pyplot as plt

# 设置中文字体，避免图表显示方块（Windows 用 SimHei，Mac 用 Arial Unicode MS）
plt.rcParams['font.sans-serif'] = ['SimHei']  # Windows
# plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 如果你用的是 Mac，取消这行注释，并注释掉上面那行
plt.rcParams['axes.unicode_minus'] = False   # 解决负号显示问题

# 读取之前保存的 CSV 结果文件
hourly = pd.read_csv('hourly_pv.csv')
daily = pd.read_csv('daily_pv_uv.csv')
conversion = pd.read_csv('conversion_rate.csv')

# 图1：每小时 PV 分布（柱状图）
plt.figure(figsize=(12, 6))
plt.bar(hourly['hour'], hourly['pv_count'], color='skyblue')
plt.title('各小时PV分布（访问高峰分析）', fontsize=14)
plt.xlabel('小时 (0-23)')
plt.ylabel('PV 数量')
plt.xticks(range(0, 24))  # 显示所有小时
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('hourly_pv_chart.png', dpi=150)
plt.show()

# 图2：每日 PV 和 UV 趋势（折线图，取前15天）
plt.figure(figsize=(12, 6))
plt.plot(daily['date'].head(15), daily['pv'].head(15), marker='o', label='PV', color='blue')
plt.plot(daily['date'].head(15), daily['uv'].head(15), marker='s', label='UV', color='orange')
plt.title('每日 PV 和 UV 趋势（前15天）', fontsize=14)
plt.xlabel('日期')
plt.ylabel('数量')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('daily_pv_uv_trend.png', dpi=150)
plt.show()

# 图3：转化率漏斗（简单饼图或条形图）
plt.figure(figsize=(6, 6))
labels = ['浏览用户 (有 PV)', '购买用户 (有 Buy)']
sizes = [conversion['total_pv_users'].iloc[0], conversion['total_buy_users'].iloc[0]]
colors = ['lightblue', 'lightcoral']
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
plt.title(f"转化率: {conversion['conversion_rate'].iloc[0]*100:.2f}%", fontsize=14)
plt.axis('equal')
plt.tight_layout()
plt.savefig('conversion_pie.png', dpi=150)
plt.show()

print("图表已保存：hourly_pv_chart.png, daily_pv_uv_trend.png, conversion_pie.png")