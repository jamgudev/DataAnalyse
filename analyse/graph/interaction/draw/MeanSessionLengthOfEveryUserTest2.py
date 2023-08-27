import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy import stats

from analyse.graph.GrapgNameSapce import GRAPH_mean_session_length_vs_session_count_per_day_of_every_user
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE
from util import ExcelUtil

# 读取Excel文件数据
dirName = TEST_OUTPUT_FILE + "/" + GRAPH_mean_session_length_vs_session_count_per_day_of_every_user
data = ExcelUtil.read_excel(dirName)


# 将每天使用次数分为5组
data['group'] = pd.qcut(data.iloc[:, 0].apply(lambda x: x / (1000 * 60)), q=4)

# 计算每组平均使用时间的平均数
grouped_data = data.groupby('group')[1].mean()

# 计算每组平均使用时间的95%置信区间
confidence_intervals = data.groupby('group')[1].apply(lambda x: stats.t.interval(0.95, len(x)-1, loc=x.mean(), scale=stats.sem(x)))

# 打印结果
# for group, avg_time, interval in zip(grouped_data.index, grouped_data, confidence_intervals):
#     print(f"Group {group}:")
#     print(f"Average Usage Time: {avg_time}")
#     print(f"Confidence Interval (95%): {interval}")
#     print()

# 提取置信区间的上界和下界
ci_lower = [ci[0] for ci in confidence_intervals]
ci_upper = [ci[1] for ci in confidence_intervals]

# 绘制每组平均使用时间及置信区间的图形
groups = grouped_data.index
x_pos = np.arange(len(groups))
means = grouped_data.values

plt.errorbar(x_pos, means, yerr=[(ci[1]-ci[0])/2 for ci in confidence_intervals], fmt='o-', capsize=4)
plt.xticks(x_pos, groups)
plt.xlabel('Session Lengths')
plt.ylabel('Session Counts')
plt.title('Average Usage Time with 95% Confidence Interval')
plt.show()