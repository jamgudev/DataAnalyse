import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

from analyse.graph.GrapgNameSapce import GRAPH_most_cost_energy_app_page
from analyse.graph.application.draw import AppColor
from analyse.graph.consumption.draw.OutputMostCostEnergyPage import output_most_cost_energy_app_page
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE
from util import ExcelUtil

output_most_cost_energy_app_page()

# 设置全局字体样式和大小
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 20

# 绘制散点图
plt.figure(figsize=(20, 10))
ax = plt.axes()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_linewidth(0.5)
ax.spines['left'].set_linewidth(0.5)


# 读取Excel数据
dirName = TEST_OUTPUT_FILE + "/" + GRAPH_most_cost_energy_app_page
data = ExcelUtil.read_excel(dirName)[1:]

print(data)

user_idx_col = 0
user_name_col = 1
phone_brand_col = 2
app_category_col = 3
app_name_col = 4
app_page_name_col = 5
stay_duration_col = 6
stay_duration_rate_col = 7
app_energy_cost_rate_col = 8
app_energy_cost_per_min_col = 9

# 获取所有的用户名
data["show_name"] = data.iloc[:, user_idx_col].astype(str) + "_" + data.iloc[:, phone_brand_col]
data["combined_page_name"] = data.iloc[:, app_name_col] + "/" + data.iloc[:, app_page_name_col]

data = data.sort_values(by=data.columns[user_idx_col], ascending=True)
# 过滤出常用app page
filtered_df = data[data.iloc[:, stay_duration_rate_col] >= 0.05]
users = sorted(filtered_df.iloc[:, user_idx_col].unique())
app_page_names = filtered_df["combined_page_name"].unique()

# init dataset
dataset = {}
for app_page_name in app_page_names:
    dataset[app_page_name] = {}

for row_idx, row_data in data.iterrows():
    user_idx = row_data[user_idx_col]
    app_page_name = row_data["combined_page_name"]
    app_energy_cost = row_data[app_energy_cost_per_min_col]

    # 需要是常用的app才行
    if app_page_name not in app_page_names:
        continue

    # get app_line_data
    if app_page_name in dataset.keys():
        app_line_data = dataset[app_page_name]
    else:
        app_line_data = {}

    if user_idx in app_line_data.keys():
        raise ValueError(f"user_idx[${user_idx}] already in app_line_data[${app_line_data}].")

    app_line_data[user_idx] = app_energy_cost
    dataset[app_page_name] = app_line_data

# 进一步过滤出大家都有的热门页面进行统计，需要人眼统计
filtered_app_page_names = []
for app_page_name in app_page_names:
    if app_page_name in dataset.keys():
        app_line_data = dataset[app_page_name]
        # 大部分都有，过滤出来
        hasNum = len(app_line_data.keys())
        if hasNum >= (len(users) - 10):
            filtered_app_page_names.append(app_page_name)


# 遍历 dataset，查缺补漏，输出热力图的二维数组
hot_data = []
for app_page_name in filtered_app_page_names:
    if app_page_name in dataset.keys():
        app_line_data = dataset[app_page_name]
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
x_labels = data["show_name"].unique()
y_labels = filtered_app_page_names

# 使用seaborn库绘制热力图，并设置自定义的坐标标签
sns.heatmap(hot_data, annot=True, cmap=AppColor.cmap, xticklabels=x_labels, yticklabels=y_labels,
            linecolor='black', linewidths=1, annot_kws={"fontsize": 36})

# 设置x轴标签倾斜角度
ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha='right')

# 设置图表的标题和标签
# plt.xlabel("Users")
# plt.ylabel("APPs")

plt.tight_layout()

# 显示图表
plt.show()
