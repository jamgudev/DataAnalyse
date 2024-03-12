import os

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt, font_manager
from scipy import stats

from analyse.graph.GrapgNameSapce import GRAPH_app_category_usage_in_diff_group_users
from analyse.graph.application.draw import AppColor
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE
from util import ExcelUtil

# 设置全局字体样式和大小
font_manager.fontManager.addfont('/Users/JAMGU_1/PycharmProjects/pythonProject/venv/lib/'
                                 'python3.9/site-packages/matplotlib/mpl-data/fonts/ttf/SimSun.ttf')
plt.rcParams['font.family'] = 'Times New Roman, SimSun'
plt.rcParams['font.size'] = 48

# 读取Excel数据
dirName = TEST_OUTPUT_FILE + "/" + GRAPH_app_category_usage_in_diff_group_users
df = ExcelUtil.read_excel(dirName)[1:]

# 使用列索引定位列
group_col_index = 0         # 用户类别
user_col_index = 1          # 用户
app_category_col_idx = 2    # app类别
time_col_index = 3          # 使用时间列索引

# 计算不同用户在各自不同类别app上的使用时间占比
df['TimeRatio'] = df.groupby(df.iloc[:, user_col_index])[time_col_index].transform(lambda x: x * 100 / x.sum()).fillna(0)

# 计算相同分组内，不同用户在同一 app 类别上的使用时间占比的均值和95%置信区间
grouped_values = df.groupby([df.iloc[:, group_col_index], df.iloc[:, app_category_col_idx]])['TimeRatio'].agg(['mean', lambda x: stats.t.interval(0.95, len(x)-1, loc=np.mean(x), scale=stats.sem(x))]).reset_index()
grouped_values[['lower_bound', 'upper_bound']] = pd.DataFrame(grouped_values['<lambda_0>'].tolist(), index=grouped_values.index)

# 根据'mean'列从大到小排序
grouped_values = grouped_values.sort_values(by='mean', ascending=False)

# 绘制条形图
fig, ax = plt.subplots(figsize=(26, 10))
categories = grouped_values[app_category_col_idx].unique()
x = np.arange(len(categories))
width = 0.4

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_linewidth(0.5)
ax.spines['left'].set_linewidth(0.5)


for i, (group, data) in enumerate(grouped_values.groupby(grouped_values.columns[group_col_index])):
    offset = (i - 1) * width
    ax.bar(x + offset, data['mean'], yerr=data['upper_bound'] - data['mean'],
           error_kw={'ecolor': AppColor.C_11_3[i], 'linewidth': 4, 'capsize': 10},
           width=width, linewidth=2, label=group, edgecolor='black', color=AppColor.C_11_3[i])

# 设置 x 轴的刻度和标签
ax.set_xticks(x)
ax.set_xticklabels(categories)
plt.xticks(rotation=25, ha='right')  # 设置刻度标签的旋转角度为0度，水平对齐方式为右对齐
plt.subplots_adjust(bottom=0.2)  # 调整图形底部的边距
plt.ylim(0, 61)
plt.yticks(range(0, 61, 20))
plt.ylabel("时长占比 (%)")
plt.xlabel("APP 类别")

plt.tight_layout()

# 添加图例
ax.legend()

# 保存图像
current_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(current_dir, '../GRAPH_app_category_usage_in_diff_group_users.png')
plt.savefig(save_path)

# 显示图形
plt.show()
