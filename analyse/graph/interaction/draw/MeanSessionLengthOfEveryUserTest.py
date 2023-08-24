import os

import matplotlib.pyplot as plt
import numpy as np

from analyse.graph.GrapgNameSapce import GRAPH_mean_session_length_vs_session_count_per_day_of_every_user
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE
from util import ExcelUtil

dirName = TEST_OUTPUT_FILE + "/" + GRAPH_mean_session_length_vs_session_count_per_day_of_every_user
data = ExcelUtil.read_excel(dirName)

# 提取 x 和 y 轴数据
x = data.iloc[:, 1].values
y = data.iloc[:, 0].values / (60 * 1000)
colors = np.random.rand(len(x))

# 绘制散点图
plt.scatter(x, y, c=colors)
plt.xlabel('Session Count')
plt.ylabel('Mean Session Length (in minutes)')
plt.title('Scatter Plot')

# 保存图像
current_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(current_dir, 'GRAPH_mean_session_length_vs_session_count_per_day_of_every_user.png')
plt.savefig(save_path)

plt.show()
