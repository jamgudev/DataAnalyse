import os

import matplotlib.pyplot as plt
import numpy as np

from analyse.graph.GrapgNameSapce import GRAPH_all_interactions_cdf
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE
from util import ExcelUtil

# 读取 Excel 表格数据
dirName = TEST_OUTPUT_FILE + "/" + GRAPH_all_interactions_cdf
df = ExcelUtil.read_excel(dirName)

# 取第一列数据
data = df[0].values / (60 * 1000)

# 计算数据占比和对应的概率
data_sorted = np.sort(data)
cdf = np.arange(1, len(data_sorted) + 1) / len(data_sorted)
threshold = np.percentile(data_sorted, 80)  # 计算超过80%的阈值
plt.axvline(x=threshold, color='red', linestyle='--', label='Threshold')
# 在图中标出超过80%的x坐标点，并显示x值
plt.text(threshold, -0.075, f'{threshold:.2f}', color='red', ha='left', va='top')

# 绘制 CDF 图
plt.plot(data_sorted, cdf)
plt.xlabel('Interaction Length (mins)')
plt.ylabel('Rate')
plt.title('CDF Of Interactions Length')
plt.xlim(-3, 100)
plt.grid(True)
# 保存图像
current_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(current_dir, 'GRAPH_all_interactions_cdf.png')
plt.savefig(save_path)
plt.show()
