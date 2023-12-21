import matplotlib.pyplot as plt
from scipy import stats

from analyse.graph.GrapgNameSapce import GRAPH_user_nis_consumption
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE
from util import ExcelUtil

# 读取Excel数据
dirName = TEST_OUTPUT_FILE + "/" + GRAPH_user_nis_consumption
data = ExcelUtil.read_excel(dirName)[1:]

# 列索引
user_col_index = 0      # 用户列索引
user_phone_col_index = 1     # 用户手机
phone_brand_col_index = 2     # 用户手机品牌
nis_consumption_ratio = 5     # NIS功耗占比
data.iloc[:, nis_consumption_ratio] = data.iloc[:, nis_consumption_ratio] * 100.0

# 获取用户ID和功耗占比数据
user_ids = data.iloc[:, user_col_index]
consumptions_ratios = data.iloc[:, nis_consumption_ratio]

# 绘制散点图和连接线条
plt.scatter(user_ids, consumptions_ratios, label='User')
plt.plot(user_ids, consumptions_ratios, linestyle='-', color='#00D26E')

# 计算功耗占比的平均值
mean_consumption = consumptions_ratios.mean()

# 在图表右上角标注功耗均值
plt.text(user_ids.max(), consumptions_ratios.max() + 1.15, f'Mean: {mean_consumption:.2f}%', ha='right', va='top')

# 在每个散点上方标注具体数值
for i, j in zip(user_ids, consumptions_ratios):
    plt.text(i, j + 0.3, f'{j:.2f}', ha='center', va='bottom')

plt.xlabel('Users')
plt.ylabel('Consumption Ratio(%)')
plt.ylim(1, 9)

plt.legend()

# 显示图形
plt.show()