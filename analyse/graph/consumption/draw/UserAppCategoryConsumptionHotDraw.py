import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from analyse.graph.GrapgNameSapce import GRAPH_app_category_consumption
from analyse.graph.application.draw import AppColor
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE
from util import ExcelUtil

# 设置全局字体样式和大小
plt.rcParams['font.family'] = 'Times New Roman'
fontsize = 40
plt.rcParams['font.size'] = fontsize

# 绘制条形累计分布图
fig, ax = plt.subplots(figsize=(20, 16))
ax.spines['top'].set_linewidth(1)
ax.spines['right'].set_linewidth(1)
ax.spines['bottom'].set_linewidth(1)
ax.spines['left'].set_linewidth(1)

# 读取Excel数据
dirName = TEST_OUTPUT_FILE + "/" + GRAPH_app_category_consumption
data = ExcelUtil.read_excel(dirName)[1:]


# 列索引
user_col_index = 0      # 用户列索引
user_name_index = 1     # 用户手机品牌
phone_brand_col_index = 2     # 用户手机品牌
app_category_col_index = 3     # app分类列索引
category_consumption_col_index = 5   # app功耗占比列索引
data.iloc[:, category_consumption_col_index] = data.iloc[:, category_consumption_col_index] * 100
# 获取所有的用户名
data["show_name"] = data.iloc[:, user_col_index].astype(str) + "_" + data.iloc[:, phone_brand_col_index]

# 将小于0.005的比例归类为"Other"
# data.loc[data.columns[category_consumption_col_index] < 0.5, data.columns[app_category_col_index]] = "minority"


# 获取所有用户
users = data.iloc[:, user_col_index].unique()
# 获取应用分类
categories = data.iloc[:, app_category_col_index].unique()

# init dataset
dataset = {}
for category in categories:
    dataset[category] = {}

for row_idx, row_data in data.iterrows():
    user_idx = row_data[user_col_index]
    category = row_data[app_category_col_index]
    energy_cost_rate = row_data[category_consumption_col_index]

    if category not in categories:
        continue

    # get app_line_data
    if category in dataset.keys():
        app_line_data = dataset[category]
    else:
        app_line_data = {}

    if user_idx in app_line_data.keys():
        raise ValueError(f"user_idx[${user_idx}] already in app_line_data[${app_line_data}].")

    app_line_data[user_idx] = energy_cost_rate
    dataset[category] = app_line_data

# 遍历 dataset，查缺补漏，输出热力图的二维数组
hot_data = []
for category in categories:
    if category in dataset.keys():
        app_line_data = dataset[category]
        app_energy_data = []
        for user_idx in users:
            if user_idx in app_line_data:
                app_energy_data.append(round(app_line_data[user_idx], 1))
            else:
                app_energy_data.append(0.0)
        hot_data.append(app_energy_data)
    else:
        hot_data.append(np.zeros(len(users)))


# 画图
# 自定义x坐标和y坐标的标签

x_labels = data["show_name"].unique()
y_labels = categories

# 使用seaborn库绘制热力图，并设置自定义的坐标标签
ax = sns.heatmap(hot_data, annot=True, cbar=False, cmap=AppColor.cmap, xticklabels=x_labels, yticklabels=y_labels,
                 linecolor='black', linewidths=1, annot_kws={"fontsize": fontsize},
                 cbar_kws={'label': '%'})


# 设置x轴标签倾斜角度
ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha='right')

# 添加颜色条
cbar = plt.colorbar(ax.collections[0], orientation='vertical')
# cbar.ax.set_ylabel('%', rotation=0, fontsize=fontsize)  # 设置颜色条的标签和字体大小
# cbar.ax.yaxis.set_ticks_position('right')  # 设置刻度的位置为左侧
# cbar.ax.yaxis.set_label_coords(5, 0)  # 设置标签的位置

# 设置颜色条刻度显示范围和间隔
# cbar.ax.yaxis.set_ticks([0, 20, 40, 60, 80])  # 设置刻度的显示范围

# 设置图表的标题和标签
# plt.xlabel("Users")
# plt.ylabel("Hardware Units")

plt.tight_layout()

# 显示图表
plt.show()