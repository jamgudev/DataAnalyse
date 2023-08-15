import matplotlib.pyplot as plt

from analyse.graph.GrapgNameSapce import GRAPH_mean_session_length_vs_session_count_per_day_of_every_user
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE
from util import ExcelUtil

dirName = TEST_OUTPUT_FILE + "/" + GRAPH_mean_session_length_vs_session_count_per_day_of_every_user
data = ExcelUtil.read_excel(dirName)

# 提取 x 和 y 轴数据
x = data.iloc[:, 0].values / (60 * 1000)
y = data.iloc[:, 1].values

# 绘制散点图
plt.scatter(x, y)
plt.xlabel('Mean Session Length (in minutes)')
plt.ylabel('Session Count')
plt.title('Scatter Plot')

plt.show()