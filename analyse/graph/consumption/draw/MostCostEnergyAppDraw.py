import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

from analyse.graph.GrapgNameSapce import GRAPH_most_cost_energy_app
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE
from util import ExcelUtil

# 设置全局字体样式和大小
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 26

# 绘制散点图
plt.figure(figsize=(20, 10))
ax = plt.axes()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_linewidth(0.5)
ax.spines['left'].set_linewidth(0.5)


# 读取Excel数据
dirName = TEST_OUTPUT_FILE + "/" + GRAPH_most_cost_energy_app
data = ExcelUtil.read_excel(dirName)[1:]

print(data)

user_idx_col = 0
user_name_col = 1
phone_brand_col = 2
app_category_col = 3
app_name_col = 4
stay_duration_col = 5
stay_duration_rate_col = 6
app_energy_cost_rate_col = 7
app_energy_cost_per_min_col = 8

# 过滤出常用app
filtered_df = data[data.iloc[:, stay_duration_rate_col] >= 0.05]
users = sorted(filtered_df.iloc[:, user_idx_col].unique())
appnames = filtered_df.iloc[:, app_name_col].unique()

# init dataset
dataset = {}
for app_name in appnames:
    dataset[app_name] = {}

for row_idx, row_data in data.iterrows():
    user_idx = row_data[user_idx_col]
    app_name = row_data[app_name_col]
    app_energy_cost = row_data[app_energy_cost_per_min_col]

    # 需要是常用的app才行
    if app_name not in appnames:
        continue

    # get app_line_data
    if app_name in dataset.keys():
        app_line_data = dataset[app_name]
    else:
        app_line_data = {}

    if user_idx in app_line_data.keys():
        raise ValueError(f"user_idx[${user_idx}] already in app_line_data[${app_line_data}].")

    app_line_data[user_idx] = app_energy_cost
    dataset[app_name] = app_line_data

# 遍历 dataset，查缺补漏，输出热力图的二维数组
hot_data = []
for app_name in appnames:
    if app_name in dataset.keys():
        app_line_data = dataset[app_name]
        app_energy_data = []
        for user_idx in users:
            if user_idx in app_line_data:
                app_energy_data.append(app_line_data[user_idx] * (10 ** 8))
            else:
                app_energy_data.append(0.0)
        hot_data.append(app_energy_data)
    else:
        hot_data.append(np.zeros(len(users)))

# 画图

# 自定义x坐标和y坐标的标签
x_labels = users
y_labels = appnames

# 使用seaborn库绘制热力图，并设置自定义的坐标标签
sns.heatmap(hot_data, annot=True, cmap="YlGnBu", xticklabels=x_labels, yticklabels=y_labels,
            linecolor='black', linewidths=1)

# 设置图表的标题和标签
plt.xlabel("Users")
plt.ylabel("APPs")

plt.tight_layout()

# 显示图表
plt.show()
