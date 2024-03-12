import os

import matplotlib.pyplot as plt

from analyse.graph.GrapgNameSapce import GRAPH_mean_active_time_per_day_with_std_of_every_user
from analyse.graph.application.draw import AppColor
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE
from util import ExcelUtil

# 读取Excel文件
dirName = TEST_OUTPUT_FILE + "/" + GRAPH_mean_active_time_per_day_with_std_of_every_user
data = ExcelUtil.read_excel(dirName)[1:]
data = data.sort_values([data.columns[1]], ascending=True)

# 创建一个图像对象并设置宽度和高度
fig = plt.figure(figsize=(16, 6))

# 设置全局字体样式和大小
# 设置全局字体样式和大小
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 30

ax = plt.axes()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_linewidth(0.5)
ax.spines['left'].set_linewidth(0.5)

# 获取用户ID、上限、平均时间和下限列的数据s
upper_limit = data.iloc[:, 0].apply(lambda x: x / (1000 * 60))
average_time = data.iloc[:, 1].apply(lambda x: x / (1000 * 60))
lower_limit = data.iloc[:, 2].apply(lambda x: x / (1000 * 60))
user_id = [i for i in range(1, len(average_time) + 1)]

plt.plot(user_id, upper_limit, '_', label='Upper End Of Std Deviation', linewidth=4)
plt.plot(user_id, average_time, 'o-', label='Mean', color=AppColor.keli_colors[0])
plt.plot(user_id, lower_limit, '_', label='Lower End Of Std Deviation')
# 绘制虚线段连接Upper_limit和lower_limit
for i in range(len(user_id)):
    plt.plot([user_id[i], user_id[i]], [upper_limit.values[i], lower_limit.values[i]], 'k--')

plt.xlabel('Users')
plt.ylabel('Mean TS Length (mins)')
# 设置y轴刻度的显示范围和间隔
plt.xticks(range(0, 50, 15))
plt.yticks(range(0, 1000, 300))

plt.tight_layout()

# ax.spines['bottom'].set_visible(False)
# ax.spines['left'].set_visible(False)

# 设置y轴为对数刻度
# plt.yscale('log')
# 设置y轴刻度范围为10到1000
# plt.ylim(1, 1000)
plt.legend(fontsize=26)
# 保存图像
current_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(current_dir, 'GRAPH_mean_active_time_per_day_with_std_of_every_user.png')
plt.savefig(save_path)

plt.show()