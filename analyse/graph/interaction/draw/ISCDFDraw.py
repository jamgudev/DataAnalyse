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
data = df[0].values / 1000

# 计算数据占比和对应的概率
data_sorted = np.sort(data)
cdf = np.arange(1, len(data_sorted) + 1) / len(data_sorted)
threshold_02 = np.percentile(data_sorted, 20)  # 计算超过80%的阈值
threshold_08 = np.percentile(data_sorted, 80)  # 计算超过80%的阈值
plt.axvline(x=threshold_02, color='red', linestyle='--', label='Threshold')
plt.axvline(x=threshold_08, color='red', linestyle='--', label='Threshold')
# 在图中标出超过80%的x坐标点，并显示x值
plt.text(threshold_02, -0.075, f'{threshold_02:.2f}', color='red', ha='left', va='top')
plt.text(threshold_08, -0.075, f'{threshold_08:.2f}', color='red', ha='left', va='top')

# 绘制 CDF 图
plt.plot(data_sorted, cdf)
plt.xlabel('Interaction Length (s)')
plt.ylabel('Rate')
plt.title('CDF Of Interactions Length')
plt.xlim(-1 * 60, 10 * 60)
plt.grid(True)
# 保存图像
current_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(current_dir, 'GRAPH_all_interactions_cdf.png')
plt.savefig(save_path)
plt.show()
