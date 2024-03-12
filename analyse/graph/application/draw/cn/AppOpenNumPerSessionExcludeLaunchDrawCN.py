import os

import matplotlib.pyplot as plt
from matplotlib import font_manager

from analyse.graph.GrapgNameSapce import GRAPH_app_open_num_per_session, GRAPH_app_open_num_exclude_launch_per_session
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
dirName = TEST_OUTPUT_FILE + "/" + GRAPH_app_open_num_exclude_launch_per_session
df = ExcelUtil.read_excel(dirName)[1:]

# 计算session数量的总数
total_sessions = df.iloc[:, 1].sum()

# 计算不同app打开数量的session次数分别占session总数的比率
df['session_ratio'] = df.iloc[:, 1] / total_sessions * 100

# 绘制条形图
plt.bar(df.iloc[:, 0], df.loc[:, 'session_ratio'], color=AppColor.C_11_3)
plt.xlabel("APP打开数量")
plt.ylabel("占比 (%)")
# plt.title("Session Ratio by App Open Count")
plt.xlim(0, 12)
plt.ylim(0, 40)
plt.xticks(range(1, 13, 2))
plt.yticks(range(0, 60, 20))

# 在每个条形图的顶部添加文本标签
for index, value in enumerate(df.loc[0:8, 'session_ratio']):
    if index >= 8:
        break
    plt.text(df.iloc[index, 0], value, str(round(value, 1)), ha='center', va='bottom', fontdict={'size':40})

plt.tight_layout()

# 保存图像
current_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(current_dir, '../GRAPH_app_open_num_per_session.png')
plt.savefig(save_path)

plt.show()

