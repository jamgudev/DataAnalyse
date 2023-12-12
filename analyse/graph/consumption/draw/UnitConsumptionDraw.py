import matplotlib.pyplot as plt

from analyse.graph.GrapgNameSapce import GRAPH_units_consumption
from analyse.util.FilePathDefinition import OUTPUT_FILE, TEST_OUTPUT_FILE
from util import ExcelUtil

# 读取Excel数据
dirName = TEST_OUTPUT_FILE + "/" + GRAPH_units_consumption
df = ExcelUtil.read_excel(dirName)[1:]

# 获取部件名称和功耗占比数据列
part_names = df.iloc[:, 0].tolist()
power_consumption = df.iloc[:, 1].tolist()
power_consumption = [p * 100 for p in power_consumption]

# 创建条形图
plt.bar(part_names, power_consumption)

# 设置标题和轴标签
plt.title("Power Consumption of Phone Components")
plt.xlabel("Component")
plt.ylabel("Power Consumption (%)")

# 旋转x轴标签，以避免重叠
# plt.xticks(rotation=90)

# 在每个条形的上方标注具体数值（小数点后两位）
for i in range(len(part_names)):
    plt.text(i, power_consumption[i], "{:.2f}".format(power_consumption[i]), ha='center', va='bottom')

# 显示图形
plt.show()
