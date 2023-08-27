import matplotlib.pyplot as plt
import numpy as np

from analyse.graph.GrapgNameSapce import GRAPH_all_interactions_cdf
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE
from util import ExcelUtil

# 读取 Excel 表格数据
dirName = TEST_OUTPUT_FILE + "/" + GRAPH_all_interactions_cdf
df = ExcelUtil.read_excel(dirName)

# 取第一列数据
data = df[1].values

# 计算数据占比和对应的概率
data_sorted = np.sort(data)
cdf = np.arange(1, len(data_sorted) + 1) / len(data_sorted)

# 绘制 CDF 图
plt.plot(data_sorted, cdf)
plt.xlabel('使用时间')
plt.ylabel('数据占比')
plt.title('使用时间数据的CDF图')
plt.grid(True)
plt.show()
