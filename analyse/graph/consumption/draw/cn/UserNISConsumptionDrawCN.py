import matplotlib.pyplot as plt
from matplotlib import font_manager
from scipy import stats

from analyse.graph.GrapgNameSapce import GRAPH_user_nis_consumption
from analyse.graph.application.draw import AppColor
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE
from util import ExcelUtil

# 设置全局字体样式和大小
font_manager.fontManager.addfont('/Users/JAMGU_1/PycharmProjects/pythonProject/venv/lib/'
                                 'python3.9/site-packages/matplotlib/mpl-data/fonts/ttf/SimSun.ttf')
plt.rcParams['font.family'] = 'Times New Roman, SimSun'
plt.rcParams['font.size'] = 30
plt.figure(figsize=(16, 6))
ax = plt.axes()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_linewidth(0.5)
ax.spines['left'].set_linewidth(0.5)

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
plt.scatter(user_ids, consumptions_ratios, label='User', color=AppColor.keli_colors[0])
plt.plot(user_ids, consumptions_ratios, linestyle='-', color=AppColor.keli_colors[0])

# 计算功耗占比的平均值
mean_consumption = consumptions_ratios.mean()

# 在图表右上角标注功耗均值
plt.text(len(user_ids.values) - 0.2, consumptions_ratios.max() - 0.2, f'均值: {mean_consumption:.2f}%', ha='right', va='top')

# 在每个散点上方标注具体数值
for i, j in zip(user_ids, consumptions_ratios):
    plt.text(i, j + 0.3, f'{j:.2f}', ha='center', va='bottom')

plt.xlabel('用户')
plt.ylabel('能耗占比 (%)')
plt.ylim(1, 9)
plt.yticks(range(2, 9, 2))
plt.xticks(range(1, 14, 2))

# plt.legend()
plt.tight_layout()

# 显示图形
plt.show()