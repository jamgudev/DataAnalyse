import os

import matplotlib.pyplot as plt
import numpy as np

from analyse.graph.GrapgNameSapce import GRAPH_mean_session_length_vs_session_count_per_day_of_every_user
from analyse.graph.application.draw import AppColor
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE
from util import ExcelUtil

dirName = TEST_OUTPUT_FILE + "/" + GRAPH_mean_session_length_vs_session_count_per_day_of_every_user
data = ExcelUtil.read_excel(dirName)[1:]

# 设置全局字体样式和大小
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 30
plt.figure(figsize=(16, 6))
ax = plt.axes()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_linewidth(0.5)
ax.spines['left'].set_linewidth(0.5)


# 提取 x 和 y 轴数据
y = data.iloc[:, 1].values
x = data.iloc[:, 0].values / (60 * 1000)
colors = np.random.rand(len(x))

# 绘制散点图
plt.scatter(x, y, c=AppColor.custom_colors[0:46])
plt.xlabel('Mean Session Length (mins)')
plt.ylabel('Session Count Per Day')
plt.tight_layout()

# 保存图像
current_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(current_dir, 'GRAPH_mean_session_length_vs_session_count_per_day_of_every_user.png')
plt.savefig(save_path)

plt.show()
