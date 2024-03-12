import os

from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec

from analyse.graph.GrapgNameSapce import GRAPH_user_mean_active_time_per_day_vs_total_mean_active_time_per_day
from analyse.graph.application.draw import AppColor
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE
from util import ExcelUtil

# 读取Excel文件
dirName = TEST_OUTPUT_FILE + "/" + GRAPH_user_mean_active_time_per_day_vs_total_mean_active_time_per_day
data = ExcelUtil.read_excel(dirName, header=0)[1:]
# 按User Active Times（D1），从小到大排序
data = data.sort_values(data.columns[3], ascending=True)

# 创建网格布局
fig = plt.figure(figsize=(24, 8))  # 调整整个图形的大小
gs = GridSpec(1, 2, width_ratios=[1, 1])  # 指定两个子图的宽度比例

# 设置全局字体样式和大小
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 30

totalActiveTimePerDay = data.iloc[:, 0].apply(lambda x: x / (1000 * 60))
userActiveTimePerDay = data.iloc[:, 1].apply(lambda x: x / (1000 * 60))
activeSum = sum(userActiveTimePerDay)
totalSum = sum(totalActiveTimePerDay)
non_interactive_rate = "{:.2f}".format((totalSum - activeSum) / totalSum * 100)
ratios = [a / b for a, b in zip(userActiveTimePerDay, totalActiveTimePerDay)]
user_id = [i for i in range(1, len(totalActiveTimePerDay) + 1)]

ax1 = fig.add_subplot(gs[0])
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['bottom'].set_linewidth(0.5)
ax1.spines['left'].set_linewidth(0.5)
# ax1.bar(user_id, ratios)
# 柱子宽度
width = 1
# 柱间间隔
spacing = 0.3
# 计算每个柱子的位置
# x = np.arange(len(user_id))
# x = x * (width + spacing)
x = user_id
edgecolors = ['black'] * len(x)
# ax1.bar(np.arange(len(user_id)), totalActiveTimePerDay, width, label='Bar 1')
# ax1.bar(np.arange(len(user_id)) + width, userActiveTimePerDay, width, label='Bar 2')
# 绘制第一个条形图，颜色较深
ax1.bar(x, totalActiveTimePerDay, width, alpha=1, color='white', edgecolor=edgecolors, label='TS Length')

# 绘制第二个条形图，颜色较浅
ax1.bar(x, userActiveTimePerDay, width, color=AppColor.C_11_3[1], edgecolor=edgecolors, label='IS Length')
ax1.text(max(x), max(totalActiveTimePerDay) - 164, f"NILR: {non_interactive_rate}%", ha='right', va='top')
ax1.set_xlabel('Users')
ax1.set_ylabel('Average Session Length Per Day (mins)')
ax1.legend(fontsize=28)
# plt.yscale('log')

totalActiveTimes = data.iloc[:, 2]
userActiveTimes = data.iloc[:, 3]
activeSum = sum(userActiveTimes)
totalSum = sum(totalActiveTimes)
non_interactive_rate = "{:.2f}".format((totalSum - activeSum) / totalSum * 100)

ax2 = fig.add_subplot(gs[1])
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['bottom'].set_linewidth(0.5)
ax2.spines['left'].set_linewidth(0.5)

# ax2.plot(user_id, totalActiveTimes, 'v', label='Upper Limit')
# ax2.plot(user_id, userActiveTimes, 'o', label='Average Time')
# # 绘制虚线段连接Upper_limit和lower_limit
# for i in range(len(user_id)):
#     ax2.plot([user_id[i], user_id[i]], [totalActiveTimes[i], userActiveTimes[i]], 'k--')
# 绘制第一个条形图，颜色较深
ax2.bar(x, totalActiveTimes, width, alpha=1, color='white', edgecolor=edgecolors, label='TS Count')

# 绘制第二个条形图，颜色较浅
ax2.bar(x, userActiveTimes, width, color=AppColor.C_11_3[1], edgecolor=edgecolors, label='IS Count')
ax2.text(0, max(totalActiveTimes) - 82, f"NICR: {non_interactive_rate}%", ha='left', va='top')
ax2.set_xlabel('Users')
ax2.set_ylabel('Session Counts Per Day')
ax2.legend(fontsize=28)

# 调整子图之间的间距
plt.subplots_adjust(wspace=0.14)  # 调整水平间距

# 保存图像
current_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(current_dir, 'GRAPH_user_mean_active_time_per_day_vs_total_mean_active_time_per_day.png')
plt.savefig(save_path)

plt.show()
