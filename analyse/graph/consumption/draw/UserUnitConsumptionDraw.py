import matplotlib.pyplot as plt
import numpy as np

from analyse.graph.GrapgNameSapce import GRAPH_user_units_consumption
from analyse.graph.application.draw import AppColor
from analyse.util.FilePathDefinition import OUTPUT_FILE
from util import ExcelUtil

# 读取Excel数据
dirName = OUTPUT_FILE + "/" + GRAPH_user_units_consumption
data = ExcelUtil.read_excel(dirName)[1:]


# 列索引
user_col_index = 0      # 用户列索引
user_brand_index = 1    # 用户手机品牌索引
units_col_index = 2     # 部件列索引
units_consumption_col_index = 3   # 部件功耗占比列索引
data.iloc[:, units_consumption_col_index] = data.iloc[:, units_consumption_col_index] * 100

# 根据某列数据排序
# data = data.sort_values(data.columns[user_brand_index], ascending=True)
data["show_name"] = data.iloc[:, user_col_index] + "_" + data.iloc[:, user_brand_index]

# 获取所有的用户名
showNames = data["show_name"].unique()

# 获取手机部件名
parts = data.iloc[:, units_col_index].unique()

# 绘制条形累计分布图
fig, ax = plt.subplots()

# 每个条形的宽度
bar_width = 0.6

bottom = [0] * len(showNames)
# 遍历每个部件
for i, part in enumerate(parts):
    # 获取该部件的功耗占比数据
    part_data = data[data.iloc[:, units_col_index] == part]
    power_consumption = part_data.iloc[:, units_consumption_col_index]

    # 将power_consumption转换为NumPy数组并替换NaN值为0
    power_consumption = np.nan_to_num(power_consumption)

    # 绘制条形图
    ax.bar(showNames, power_consumption, bottom=bottom, width=bar_width, color=AppColor.custom_colors[i + 15], label=part)

    bottom += power_consumption

# 在条形图上方标出部件功耗的总占比
for j, power in enumerate(bottom):
    ax.text(showNames[j], power, f'{power:.2f}', ha='center', va='bottom')

# 添加图例和标签
# ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=len(parts))
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))  # 将图例显示在条形图的外部右侧
ax.set_xlabel('Users')
ax.set_ylabel('Consumption Ratios(%)')
# ax.set_ylim(0, 120)

# 设置x轴刻度标签为用户ID
ax.set_xticks(showNames)

# 调整图形排版，使底部的图例完整显示
plt.tight_layout()

# 显示图形
plt.show()