import os

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.font_manager import FontProperties

from util import ExcelUtil

# 设置全局字体样式和大小
font_manager.fontManager.addfont('/Users/JAMGU_1/PycharmProjects/pythonProject/venv/lib/'
                                 'python3.9/site-packages/matplotlib/mpl-data/fonts/ttf/SimSun.ttf')
plt.rcParams['font.family'] = 'Times New Roman, SimSun'
plt.rcParams['font.size'] = 26
ax = plt.axes()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_linewidth(0.5)
ax.spines['left'].set_linewidth(0.5)

# 从Excel中读取数据
current_dir = os.path.dirname(os.path.abspath(__file__))
df = ExcelUtil.read_excel(current_dir + "/single_error_cdf.xlsx")
data = df[0].values

# 计算数据占比和对应的概率
data_sorted = np.sort(data)
cdf = np.arange(1, len(data_sorted) + 1) / len(data_sorted)
threshold_09 = np.percentile(data_sorted, 90)  # 计算超过80%的阈值
plt.axvline(x=threshold_09, color='red', linestyle='--', label='Threshold')
plt.axhline(y=0.9, color='red', linestyle='--', label='Threshold')
# 在图中标出超过80%的x坐标点，并显示x值
# plt.text(threshold_09, -0.03, f'{threshold_09:.2f}', color='red', ha='left', va='top')
# plt.text(-0.02, 0.9, '0.9', color='red', ha='right', va='center')
plt.text(threshold_09, -0.04, f'{threshold_09:.2f}', color='red', ha='left', va='top')
plt.text(-0.02, 0.85, '0.9', color='red', ha='right', va='center')

# 绘制 CDF 图
plt.plot(data_sorted, cdf)
# plt.xlabel('Error Ratio (a)', fontdict={'size': 20})
# plt.ylabel('Sample Percentage (%)', fontdict={'size': 20})
plt.xlabel('错误率')
plt.ylabel('样本占比 (%)')
plt.xlim(0, 1)
plt.ylim(0, 1)
# plt.title('CDF Of Error')
plt.grid(True)
plt.tight_layout()

# 保存图像
current_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(current_dir, '../../../test/GRAPH_all_interactions_cdf.png')
plt.savefig(save_path)
plt.show()
