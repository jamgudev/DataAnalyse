import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager

from analyse.graph.GrapgNameSapce import GRAPH_app_category_consumption
from analyse.graph.application.draw import AppColor
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE
from util import ExcelUtil

# 设置全局字体样式和大小
font_manager.fontManager.addfont('/Users/JAMGU_1/PycharmProjects/pythonProject/venv/lib/'
                                 'python3.9/site-packages/matplotlib/mpl-data/fonts/ttf/SimSun.ttf')
plt.rcParams['font.family'] = 'Times New Roman, SimSun'
plt.rcParams['font.size'] = 30

# 读取Excel数据
dirName = TEST_OUTPUT_FILE + "/" + GRAPH_app_category_consumption
data = ExcelUtil.read_excel(dirName)[1:]

# 列索引
user_col_index = 0      # 用户列索引
phone_brand_col_index = 1     # 用户手机品牌
app_category_col_index = 2     # app分类列索引
category_consumption_col_index = 4   # app功耗占比列索引
data.iloc[:, category_consumption_col_index] = data.iloc[:, category_consumption_col_index] * 100

# 将小于0.005的比例归类为"Other"
# data.loc[data.columns[category_consumption_col_index] < 0.5, data.columns[app_category_col_index]] = "minority"

# 按用户名分组
grouped_data = data.groupby(data.columns[user_col_index])

# 获取所有的用户名
data["show_name"] = data.iloc[:, user_col_index] + "_" + data.iloc[:, phone_brand_col_index]
showNames = data["show_name"].unique()

# 获取应用分类
categories = data.iloc[:, app_category_col_index].unique()

# 绘制条形累计分布图
fig, ax = plt.subplots(figsize=(16, 6))
ax.spines['top'].set_linewidth(1)
ax.spines['right'].set_linewidth(1)
ax.spines['bottom'].set_linewidth(1)
ax.spines['left'].set_linewidth(1)

# 每个条形的宽度
bar_width = 0.6

bottom = [0] * len(showNames)
# 遍历每个部件
for i, part in enumerate(categories):
    # 获取该部件的功耗占比数据
    part_data = data[data.iloc[:, app_category_col_index] == part]
    power_consumption = part_data.iloc[:, category_consumption_col_index]

    # 将power_consumption转换为NumPy数组并替换NaN值为0
    power_consumption = np.nan_to_num(power_consumption)

    # 绘制条形图
    ax.bar(showNames, power_consumption, bottom=bottom, width=bar_width, color=AppColor.C_20_3[i], label=part)

    bottom += power_consumption

# 添加图例和标签
# ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=len(parts))
# ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.35), ncol=4, fontsize=30)  # 将图例显示在条形图的外部右侧
ax.set_xlabel('用户')
ax.set_ylabel('能耗占比 (%)')
# ax.set_ylim(0, 120)

# 设置x轴刻度标签为用户ID
ax.set_xticks(showNames)
plt.xticks(rotation=25, ha='right')  # 设置刻度标签的旋转角度为0度，水平对齐方式为右对齐
plt.yticks(range(0, 110, 50))

# 调整图形排版，使底部的图例完整显示
plt.tight_layout()

# 保存图像
current_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(current_dir, 'GRAPH_app_category_consumption.png')
plt.savefig(save_path)


# 显示图形
plt.show()