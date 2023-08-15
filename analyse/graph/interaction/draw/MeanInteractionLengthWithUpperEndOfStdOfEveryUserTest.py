import matplotlib.pyplot as plt
import numpy as np

from analyse.graph.GrapgNameSapce import GRAPH_mean_interaction_length_with_upper_end_of_std_of_every_user
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE
from util import ExcelUtil

dirName = TEST_OUTPUT_FILE + "/" + GRAPH_mean_interaction_length_with_upper_end_of_std_of_every_user
data = ExcelUtil.read_excel(dirName)
user_ids = data.iloc[:, 0].values  # 第一列为用户编号
usage_times = data.iloc[:, 1:].values  # 从第二列开始为手机使用时间

# IMPORTANT: 运行前需要往第一列里添加User_ID
for i in range(len(user_ids)):
    # 将ms转换成mins
    usage_times[i] = [val / (1000 * 60) for val in usage_times[i]]
    x = user_ids[i]
    y = usage_times[i]
    plt.plot([x, x], [min(y), max(y)], '--', color='red', linewidth=1)  # 绘制虚线段连接一条直线上的点
    plt.plot(x, min(y), '^', color='red', markersize=5)  # 绘制下顶点，使用向下的三角形
    plt.plot(x, max(y), 'v', color='red', markersize=5)  # 绘制上顶点，使用向上的三角形

plt.xlabel('User ID')
plt.ylabel('Mean Session Length(mins)')
plt.title('Phone Usage Time by User')
plt.yscale('log')  # 设置y轴为对数刻度
plt.ylim(1, 100)  # 设置y轴范围
plt.show()