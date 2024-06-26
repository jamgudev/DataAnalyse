import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

from analyse.graph.GrapgNameSapce import GRAPH_most_cost_energy_app_category
from analyse.graph.application.draw import AppColor
from analyse.graph.consumption.draw.OutputMostCostEnergyAppCategory import output_most_cost_energy_app_category
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE
from util import ExcelUtil

output_most_cost_energy_app_category()

# 设置全局字体样式和大小
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 48

# 绘制散点图
plt.figure(figsize=(26, 13))
ax = plt.axes()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_linewidth(0.5)
ax.spines['left'].set_linewidth(0.5)

# 读取Excel数据
dirName = TEST_OUTPUT_FILE + "/" + GRAPH_most_cost_energy_app_category
data = ExcelUtil.read_excel(dirName)[1:]

print(data)

user_idx_col = 0
user_name_col = 1
phone_brand_col = 2
app_category_col = 3
stay_duration_col = 4
stay_duration_rate_col = 5
app_energy_cost_rate_col = 6
app_energy_cost_per_min_col = 7

# 获取所有的用户名
data["show_name"] = data.iloc[:, user_idx_col].astype(str) + "_" + data.iloc[:, phone_brand_col]
data = data.sort_values(by=data.columns[user_idx_col], ascending=True)

# 过滤出常用app
filtered_df = data[data.iloc[:, stay_duration_rate_col] >= 0.05]
users = sorted(filtered_df.iloc[:, user_idx_col].unique())
categories = filtered_df.iloc[:, app_category_col].unique()

# init dataset
dataset = {}
for category_name in categories:
    dataset[category_name] = {}

for row_idx, row_data in data.iterrows():
    user_idx = row_data[user_idx_col]
    category_name = row_data[app_category_col]
    app_energy_cost = row_data[app_energy_cost_per_min_col]

    # 需要是常用的app才行
    if category_name not in categories:
        continue

    # get app_line_data
    if category_name in dataset.keys():
        app_line_data = dataset[category_name]
    else:
        app_line_data = {}

    if user_idx in app_line_data.keys():
        raise ValueError(f"user_idx[${user_idx}] already in app_line_data[${app_line_data}].")

    app_line_data[user_idx] = app_energy_cost
    dataset[category_name] = app_line_data

# 遍历 dataset，查缺补漏，输出热力图的二维数组
hot_data = []
for category_name in categories:
    if category_name in dataset.keys():
        app_line_data = dataset[category_name]
        app_energy_data = []
        for user_idx in users:
            if user_idx in app_line_data:
                ec = app_line_data[user_idx] * (10 ** 8)
                app_energy_data.append(ec)
            else:
                app_energy_data.append(0.0)
        hot_data.append(app_energy_data)
    else:
        hot_data.append(np.zeros(len(users)))

# 画图

# 自定义x坐标和y坐标的标签
# x_labels = np.concatenate([data["show_name"].unique(), ['mean']])
x_labels = data["show_name"].unique()
y_labels = categories

# 使用seaborn库绘制热力图，并设置自定义的坐标标签
sns.heatmap(hot_data, annot=True, cmap=AppColor.cmap, xticklabels=x_labels, yticklabels=y_labels,
            linecolor='black', linewidths=1, annot_kws={"fontsize": 48})

# 设置x轴标签倾斜角度
ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha='right')

# 设置图表的标题和标签
# plt.xlabel("Users")
# plt.ylabel("APP categories")

plt.tight_layout()

# 显示图表
plt.show()
