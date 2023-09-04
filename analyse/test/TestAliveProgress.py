import matplotlib.pyplot as plt
import numpy as np

success_data = [50, 30, 20]  # 成功的部分数据
total_data = [100, 150, 100]  # 所有的数据
categories = ['Category 1', 'Category 2', 'Category 3']  # 数据类别

# 计算失败的部分数据
failure_data = [total - success for total, success in zip(total_data, success_data)]

# 设置颜色和边界颜色
colors = ['lightblue', 'lightgreen', 'lightyellow']
edgecolors = ['black'] * len(categories)

# 绘制带有黑色边界的堆叠条形图
plt.bar(categories, failure_data, color=colors, edgecolor=edgecolors, label='Failures Data')
plt.bar(categories, success_data, bottom=failure_data, color=colors, edgecolor=edgecolors, label='Success Data')

plt.xlabel('Categories')
plt.ylabel('Data')
plt.title('Success Data vs. Total Data')
plt.legend()

plt.show()