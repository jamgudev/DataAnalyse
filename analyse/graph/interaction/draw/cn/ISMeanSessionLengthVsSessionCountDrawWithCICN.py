import os

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt, font_manager
from scipy import stats

from analyse.graph.GrapgNameSapce import GRAPH_mean_session_length_vs_session_count_per_day_of_every_user
from analyse.graph.application.draw import AppColor
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE
from util import ExcelUtil

# 读取Excel文件数据
dirName = TEST_OUTPUT_FILE + "/" + GRAPH_mean_session_length_vs_session_count_per_day_of_every_user
data = ExcelUtil.read_excel(dirName)[1:]

# 设置全局字体样式和大小
font_manager.fontManager.addfont('/Users/JAMGU_1/PycharmProjects/pythonProject/venv/lib/'
                                 'python3.9/site-packages/matplotlib/mpl-data/fonts/ttf/SimSun.ttf')
plt.rcParams['font.family'] = 'Times New Roman, SimSun'
plt.rcParams['font.size'] = 30
plt.figure(figsize=(16, 6))
ax = plt.axes()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_linewidth(0.5)
ax.spines['left'].set_linewidth(0.5)

# 将每天使用次数分为5组
data['group'] = pd.qcut(data.iloc[:, 0].apply(lambda x: x / (1000 * 60)), q=5)

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

# plt.errorbar(x_pos, means, yerr=[(ci[1]-ci[0])/2 for ci in confidence_intervals], fmt='o-', capsize=2,
#              elinewidth=0.8, color=AppColor.keli_colors[0], ecolor='black')

plt.plot(x_pos, ci_upper, '_', label='CI上限')
plt.plot(x_pos, means, 'o-', label='均值', color=AppColor.keli_colors[0])
plt.plot(x_pos, ci_lower, '_', label='CI下限')
# 绘制虚线段连接Upper_limit和lower_limit
for i in range(len(x_pos)):
    plt.plot([x_pos[i], x_pos[i]], [ci_upper[i], ci_lower[i]], 'k--')

x_labels = ['({:.2f}, {:.2f}]'.format(interval.left, interval.right) for interval in groups]
plt.xticks(x_pos, x_labels)
plt.xlabel('平均Session长度 (min)')
plt.ylabel('每天平均Session次数')
# 设置y轴刻度的显示范围和间隔
plt.yticks(range(40, 200, 50))
plt.legend()
plt.tight_layout()
# plt.title('Mean Session Length with 95% Confidence Interval')
# 保存图像
current_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(current_dir, '../GRAPH_mean_session_length_vs_session_count_per_day_of_every_user_with_ci.png')
plt.savefig(save_path)

plt.show()