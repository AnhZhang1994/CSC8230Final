import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import logging

# 配置日志记录
logging.basicConfig(
    filename='data_processing.log',  # 日志文件名
    level=logging.INFO,              # 日志级别
    format='%(asctime)s - %(levelname)s - %(message)s'  # 日志格式
)

# 定义 CSV 文件路径
file_path = 'Y:\\reddit-data\\other\\时间序列分析用post数据\\anti-china.csv'

# 尝试读取 CSV 文件内容到 DataFrame
try:
    data = pd.read_csv(file_path)
    logging.info(f"Successfully read file: {file_path}")
except Exception as e:
    logging.error(f"Error reading file {file_path}: {e}")
    raise

# 确保时间戳列是 datetime 格式
try:
    data['created_time'] = pd.to_datetime(data['created_time'])
    logging.info("Converted 'created_time' to datetime format.")
except Exception as e:
    logging.error(f"Error converting 'created_time': {e}")
    raise

# 限制数据范围在 2021-01-01 至 2023-12-31 之间
start_date = pd.Timestamp('2021-01-01')
end_date = pd.Timestamp('2023-12-31')

# 筛选出符合时间范围的数据
data = data[(data['created_time'] >= start_date) & (data['created_time'] <= end_date)]

# 设置时间戳为索引
data.set_index('created_time', inplace=True)

# 按天统计帖子数量
daily_counts = data.resample('D').size()

# 将 Series 转换为 DataFrame 以便绘图
daily_counts = daily_counts.reset_index(name='Post Count')

# 找出前7个峰值
top_7_peaks = daily_counts.nlargest(7, 'Post Count').sort_values(by='created_time')
logging.info(f"Top 7 peak days: {top_7_peaks}")

# 打印前7峰值日期
print("Top 7 peak days:")
print(top_7_peaks)

# 绘制时间序列图
plt.figure(figsize=(18, 8))
sns.lineplot(x='created_time', y='Post Count', data=daily_counts)

# 设置 x 轴显示每年，并将标签旋转 45 度
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # 显示年份-月份
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))  # 设置每3个月显示一次
plt.xticks(rotation=45)  # 旋转标签

# 限制x轴的显示范围
plt.xlim(pd.Timestamp('2021-01-01'), pd.Timestamp('2023-12-31'))

# 添加垂直线标记前7个峰值，并在图表外标号
for i, row in enumerate(top_7_peaks.itertuples(), 1):
    peak_date = row.created_time
    plt.axvline(x=peak_date, color='red', linestyle='--', linewidth=0.8)
    
    # 根据标号调整垂直位置，7和8号的高度不同，避免重叠
    if i == 4:
        y_offset = 26  # 7号标号稍微高一些
    elif i == 5:
        y_offset = 18  # 8号标号稍微低一些
    else:
        y_offset = 18  # 其他标号默认
    
    # 在垂直线的上方，图表外部标号
    plt.text(peak_date, max(daily_counts['Post Count']) + y_offset, str(i), 
             horizontalalignment='center', color='black')

# 调整图表上边距，给标号留出空间
plt.subplots_adjust(top=0.85)

# 添加标题和标签
# plt.title('Number of Anti-China Posts Over Time (2021-2023)', pad=40)  # 标题向下移动，避免与标号重叠
plt.xlabel('Time')
plt.ylabel('Number of Posts')

# 保存图像到指定路径
plt.savefig('anti-china.png', dpi=300, bbox_inches='tight')
logging.info("Saved the plot as 'anti-china.png'.")

# 显示图像
plt.show()
