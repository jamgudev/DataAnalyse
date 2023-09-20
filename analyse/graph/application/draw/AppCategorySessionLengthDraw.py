import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats

from analyse.graph.GrapgNameSapce import GRAPH_app_usage_in_all_users
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE
from util import ExcelUtil

# 读取Excel数据
dirName = TEST_OUTPUT_FILE + "/" + GRAPH_app_usage_in_all_users
df = ExcelUtil.read_excel(dirName)[1:]

# 列索引
user_col_index = 0  # 用户编号列索引
time_col_index = 2  # app使用时间列索引
app_category = 3    # app类别列索引

# 将第三列转换为数值类型
df.iloc[:, time_col_index] = pd.to_numeric(df.iloc[:, time_col_index], errors='coerce')
df.iloc[:, time_col_index] = df.iloc[:, time_col_index] / (60 * 1000)

# 按app类别计算总使用时间
category_total_usage_time = df.groupby(df.iloc[:, app_category])[df.columns[time_col_index]].mean()

# 计算每组的95%置信区间
confidence_intervals = []
for category, group in df.groupby(df.iloc[:, app_category]):
    usage_times = group.iloc[:, time_col_index]
    mean = usage_times.mean()
    std = usage_times.std()
    confidence_interval = stats.norm.interval(0.95, loc=mean, scale=std)
    confidence_intervals.append(confidence_interval)

# 绘制误差棒图
fig, ax = plt.subplots()
ax.errorbar(
    category_total_usage_time.index,
    category_total_usage_time.values,
    yerr=[(ci[1] - ci[0]) / 2 for ci in confidence_intervals],
    fmt="o",
    capsize=4,
    label="App使用时间",
)
ax.set_xlabel("App类别")
ax.set_ylabel("App使用时间")
ax.set_title("App使用时间按类别统计")
ax.set_xticklabels(category_total_usage_time.index, rotation=90)

# 在图中添加置信区间
# for i, ci in enumerate(confidence_intervals):
#     ax.plot([i, i], [ci[0], ci[1]], color='red', linewidth=2)

ax.legend()
plt.show()