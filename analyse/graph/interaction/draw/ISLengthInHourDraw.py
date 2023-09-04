import os

import numpy as np
from matplotlib import pyplot as plt
from scipy import stats

from analyse.graph.GrapgNameSapce import GRAPH_mean_interactive_length_in_hour_for_all_users
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE
from util import ExcelUtil

# 读取Excel文件数据
dirName = TEST_OUTPUT_FILE + "/" + GRAPH_mean_interactive_length_in_hour_for_all_users
df = ExcelUtil.read_excel(dirName)

# 存储每一列的数据的列表
data_lists = []

# 提取每一列的数据并存储到列表中
for column in df.columns:
    data = df[column].tolist()
    # 除以 （60 * 1000）
    data_lists.append([x / (60 * 1000) for x in data])

# 计算每个列表的平均值
averages = [np.mean(data) for data in data_lists]

# 计算每个列表的置信区间
confidence_intervals = [stats.t.interval(0.95, len(data)-1, loc=np.mean(data), scale=stats.sem(data)) for data in data_lists]

# 绘制图表
plt.figure(figsize=(10, 6))
x = np.arange(len(df.columns))
plt.errorbar(x, averages, yerr=[(ci[1]-ci[0])/2 for ci in confidence_intervals], fmt='o-', capsize=4)

plt.xticks(x)
plt.xlabel('Hour In Day')
plt.ylabel('Session Length (in mins)')
plt.title('Average with 95% Confidence Interval')
# 保存图像
current_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(current_dir, 'GRAPH_mean_interactive_time_in_hour_for_all_users.png')
plt.savefig(save_path)

plt.show()
