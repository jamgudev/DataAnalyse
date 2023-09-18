import os

import matplotlib.pyplot as plt

from analyse.graph.GrapgNameSapce import GRAPH_app_open_num_per_session
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE
from util import ExcelUtil

# 读取Excel数据
dirName = TEST_OUTPUT_FILE + "/" + GRAPH_app_open_num_per_session
df = ExcelUtil.read_excel(dirName)[1:]

# 计算session数量的总数
total_sessions = df.iloc[:, 1].sum()

# 计算不同app打开数量的session次数分别占session总数的比率
df['session_ratio'] = df.iloc[:, 1] / total_sessions

# 绘制条形图
plt.bar(df.iloc[:, 0], df['session_ratio'])
plt.xlabel("App Open Count")
plt.ylabel("Session Ratio")
plt.title("Session Ratio by App Open Count")
plt.xlim(0, 15)

# 保存图像
current_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(current_dir, 'GRAPH_app_open_num_per_session.png')
plt.savefig(save_path)

plt.show()

