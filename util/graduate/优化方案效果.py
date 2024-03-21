import pandas as pd
import matplotlib.pyplot as plt

# 读取Excel文件
df = pd.read_excel('优化方案效果.xlsx', header=None)
plt.rcParams['font.sans-serif'] = ['Heiti TC']

# 计算功耗差异
difference = df.columns[0] - df.columns[1]

# 创建面积图
plt.fill_between(df.index, df.columns[0], alpha=0.5, label='默认方案')
plt.fill_between(df.index, df.columns[1], alpha=0.5, label='优化方案')
plt.fill_between(df.index, difference, alpha=0.5, label='功耗差异')

# 添加图例、标题和坐标轴标签
plt.legend(loc='upper left')
plt.title('默认方案与优化方案功耗对比')
plt.xlabel('数据点')
plt.ylabel('功耗')

# 显示图表
plt.show()