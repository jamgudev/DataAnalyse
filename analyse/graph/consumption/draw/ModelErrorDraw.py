import os

import pandas as pd
import matplotlib.pyplot as plt

from analyse.graph.application.draw import AppColor

# 从Excel中读取数据
current_dir = os.path.dirname(os.path.abspath(__file__))
data = pd.read_excel(current_dir + "/scenario_error.xlsx")

# 设置全局字体样式和大小
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 22

# 绘制条形累计分布图
fig, ax = plt.subplots(figsize=(10, 4))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_linewidth(0.5)
ax.spines['left'].set_linewidth(0.5)

# 提取场景名称和错误率列
scene_names = data.iloc[:, 0]
error_rates = data.iloc[:, 1]

# 创建条形图
plt.bar(scene_names, error_rates, color=AppColor.C_9_1, edgecolor='black', linewidth=1)

# 设置x轴标签旋转角度，使其更易读
plt.xticks(rotation=15)

# 添加标题和坐标轴标签
plt.xlabel('Test Case')
plt.ylabel('Error Rate')

# 将错误率显示为小数点后两位
# plt.gca().yaxis.set_major_formatter('{:.2%}'.format)

# 在每个条形上标出具体数值
for i in range(len(scene_names)):
    plt.text(i, error_rates[i], str(round(error_rates[i], 2)), ha='center', va='bottom')


plt.tight_layout()

# 显示图形
plt.show()