import os

import pandas as pd
import matplotlib.pyplot as plt

from analyse.graph.GrapgNameSapce import GRAPH_app_usage_in_all_users
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE
from util import ExcelUtil

# 读取Excel文件
dirName = TEST_OUTPUT_FILE + "/" + GRAPH_app_usage_in_all_users
df = ExcelUtil.read_excel(dirName)[1:]

# 使用列索引定位列
user_col_index = 0  # 用户列索引
app_col_index = 1   # 应用程序包名列索引
time_col_index = 2  # 使用时间列索引
app_category = 3    # app类别

# 计算每个用户的总使用时间
user_total_time = df.groupby(df.iloc[:, user_col_index])[time_col_index].sum()

# 计算每个用户在每个类别的app使用时间
user_category_time = df.groupby([df.iloc[:, user_col_index], df.iloc[:, app_category]])[time_col_index].sum().unstack(fill_value=0)

# 计算每个用户每个类别的app使用时间占比
user_category_percentage = user_category_time.div(user_total_time, axis=0)

custom_colors = [
    "#FF0000", "#B7FD01", "#FF69B4", "#D27B68", "#E2DA34", "#7FFF00", "#F0F0F0", "#F000F0", "#00F0F0", "#FFD6FE",
    "#CC0000", "#00CC00", "#0000CC", "#A39D24", "#00CCCC", "#E54444", "#C0C0C0", "#0177FF", "#FE8D00", "#D0D2FF",
    "#00688C", "#FB8282", "#FFFF11", "#111FFF", "#7E84FF", "#1FFF00", "#D2721C", "#FF001F", "#6FFF0F", "#F6F60F",
    "#880000", "#008800", "#000088", "#888000", "#008888", "#880080", "#808080", "#FF1493", "#008080", "#FF6347",
    "#7FFF00", "#0000FF", "#00C0C0", "#FFF000", "#8B008B", "#00EA6A", "#FF4500", "#48D1CC",
]

# 创建新的图形对象并设置宽高比例
fig = plt.figure(figsize=(32, 20))
ax = fig.add_subplot(111)

# 获取x轴刻度位置
x = range(len(user_category_percentage))

# 每个条形的宽度
bar_width = 0.8

# 绘制每个类别的条形
bottom = None
for i, col in enumerate(user_category_percentage.columns):
    values = user_category_percentage[col]
    if bottom is None:
        ax.bar(x, values, width=bar_width, color=custom_colors[i], label=col)
        bottom = values
    else:
        ax.bar(x, values, width=bar_width, bottom=bottom, color=custom_colors[i], label=col)
        bottom += values

# 设置图形的标题和标签
fontSize = 30
# ax.set_title('App Usage Time Percentage by Category', fontsize=fontSize)
ax.set_xlabel('User', fontsize=fontSize)
ax.set_ylabel('App Usage Time Ratio', fontsize=fontSize)
ax.tick_params(axis='x', labelsize=fontSize)
ax.tick_params(axis='y', labelsize=fontSize)
ax.set_xlim(-1, 45)
ax.set_ylim(0.0, 1.0)

# 设置x轴刻度和标签
x_labels = range(1, len(user_category_percentage.index) + 1)
x_ticks = list(x[::10])  # 每隔10个取一个刻度位置
ax.set_xticks(x_ticks)
ax.set_xticklabels(x_labels[::10])  # 每隔5个取一个标签

# 调整图表和标签的位置
plt.subplots_adjust(top=0.94, left=0.05, right=0.95, bottom=0.25)

# 显示标签在图表的下方
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.08), ncol=8, fontsize=fontSize)

# 保存图像
current_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(current_dir, 'GRAPH_app_usage_in_all_users_2.png')
plt.savefig(save_path)

# 显示图形
plt.show()