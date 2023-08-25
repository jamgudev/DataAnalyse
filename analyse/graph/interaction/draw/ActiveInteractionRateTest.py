import os

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec

from analyse.graph.GrapgNameSapce import GRAPH_user_mean_active_time_per_day_vs_total_mean_active_time_per_day
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE
from util import ExcelUtil

# 数据预处理
# 去掉title
# 按User Active Times（D1），从小到大排序

# 读取Excel文件
dirName = TEST_OUTPUT_FILE + "/" + GRAPH_user_mean_active_time_per_day_vs_total_mean_active_time_per_day
data = ExcelUtil.read_excel(dirName, header=0)

# 创建网格布局
fig = plt.figure(figsize=(10, 10))  # 调整整个图形的大小
gs = GridSpec(1, 2, width_ratios=[2, 2])  # 指定两个子图的宽度比例

totalActiveTimePerDay = data.iloc[:, 0].apply(lambda x: x / (1000 * 60))
userActiveTimePerDay = data.iloc[:, 1].apply(lambda x: x / (1000 * 60))
ratios = [a / b for a, b in zip(userActiveTimePerDay, totalActiveTimePerDay)]
user_id = [i for i in range(1, len(totalActiveTimePerDay) + 1)]

ax1 = fig.add_subplot(gs[0])
ax1.bar(user_id, ratios)

ax1.set_xlabel('User ID')
ax1.set_ylabel('User Active Time / Total Active Time')
ax1.set_title('All User')
# plt.yscale('log')
ax1.set_ylim(0.8, 1)

totalActiveTimes = data.iloc[:, 2]
userActiveTimes = data.iloc[:, 3]

ax2 = fig.add_subplot(gs[1])
ax2.plot(user_id, totalActiveTimes, 'v', label='Upper Limit')
ax2.plot(user_id, userActiveTimes, 'o-', label='Average Time')
# 绘制虚线段连接Upper_limit和lower_limit
for i in range(len(user_id)):
    ax2.plot([user_id[i], user_id[i]], [totalActiveTimes[i], userActiveTimes[i]], 'k--')
ax2.set_xlabel('User ID')
ax2.set_ylabel('User Active Times / Total Active Times')
ax2.set_title('All User')

# 调整子图之间的间距
plt.subplots_adjust(wspace=0.4)  # 调整水平间距

# 保存图像
current_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(current_dir, 'GRAPH_user_mean_active_time_per_day_vs_total_mean_active_time_per_day.png')
plt.savefig(save_path)

plt.show()
