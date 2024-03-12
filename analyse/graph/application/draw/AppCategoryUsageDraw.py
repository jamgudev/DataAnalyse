import os

import plotly.graph_objects as go
from matplotlib import pyplot as plt, font_manager

from analyse.graph.GrapgNameSapce import GRAPH_app_usage_in_all_users
from analyse.graph.application.draw import AppColor
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE
from util import ExcelUtil

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

# 读取Excel数据
dirName = TEST_OUTPUT_FILE + "/" + GRAPH_app_usage_in_all_users
df = ExcelUtil.read_excel(dirName)[1:]

# 使用列索引定位列
user_col_index = 0  # 用户列索引
app_col_index = 1   # 应用程序包名列索引
time_col_index = 2  # 使用时间列索引
app_category = 3    # app类别

# 计算每个类别的总使用时长
category_times = df.groupby(df.iloc[:, app_category])[time_col_index].sum()

# 计算总使用时长
total_time = category_times.sum()

# 计算每个类别的比率
category_ratios = category_times / total_time

# 将比率小于0.5%的类别归为"minority"类别
minority_threshold = 0.005
category_ratios_minority = category_ratios[category_ratios < minority_threshold]
category_ratios_majority = category_ratios[category_ratios >= minority_threshold]

# 将"minority"类别的总使用时长合并为一项
minority_time = category_times[category_ratios_minority.index].sum()
category_ratios_majority['minority'] = minority_time / total_time

# 降序排序
category_ratios_majority = category_ratios_majority.sort_values(ascending=False)

# 创建饼图数据和标签
labels = category_ratios_majority.index.tolist()
sizes = category_ratios_majority.tolist()

# 按照特定顺序重新排列标签和数值
# new_labels = labels[5:] + [labels[:5]]  # 将第一个标签放到最后
# new_sizes = sizes[5:] + [sizes[:5]]  # 对应的数值也要调整顺序

# 绘制饼图
fig = go.Figure(data=[go.Pie(labels=labels, values=sizes, marker=dict(colors=AppColor.C_20_2),
                             insidetextorientation='horizontal')])

# 将time_col_index索引的值乘以100
sizes = [x * 100 for x in sizes]

# 绘制条形图
plt.bar(labels, sizes, color=AppColor.C_11_3)
plt.xlabel("应用类别")
plt.ylabel("停留时间占比(%)")

# 在每个条形图的顶部添加文本标签
for index, value in enumerate(sizes):
    if index >= 12:
        break
    plt.text(labels[index], value, str(round(value, 2)), ha='center', va='bottom')

plt.text(len(labels) - 1.1, max(sizes) - 0.04, "minority: 占比小于0.5%的应用类别总和", ha='right', va='bottom')

plt.xticks(rotation=25, ha='right')  # 设置刻度标签的旋转角度为0度，水平对齐方式为右对齐

plt.tight_layout()

# 保存图像
current_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(current_dir, 'GRAPH_app_category_usage_in_all.png')
plt.savefig(save_path)

# 显示饼图
plt.show()
