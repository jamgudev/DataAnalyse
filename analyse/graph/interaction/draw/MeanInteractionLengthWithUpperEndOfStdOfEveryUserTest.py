import os

import matplotlib.pyplot as plt

from analyse.graph.GrapgNameSapce import GRAPH_mean_active_time_per_day_with_std_of_every_user
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE
from util import ExcelUtil

# 数据预处理:
# 1. 根据中位数降序排序
# 2. 排序后在在第一列加User_id

# 读取Excel文件
dirName = TEST_OUTPUT_FILE + "/" + GRAPH_mean_active_time_per_day_with_std_of_every_user
data = ExcelUtil.read_excel(dirName)

# 获取用户ID、上限、平均时间和下限列的数据
user_id = data.iloc[:, 0]
upper_limit = data.iloc[:, 1].apply(lambda x: x / (1000 * 60))
average_time = data.iloc[:, 2].apply(lambda x: x / (1000 * 60))
lower_limit = data.iloc[:, 3].apply(lambda x: x / (1000 * 60))
# 绘制虚线段连接Upper_limit和lower_limit
for i in range(len(user_id)):
    plt.plot([user_id[i], user_id[i]], [upper_limit[i], lower_limit[i]], 'k--')

plt.plot(user_id, upper_limit, 'v', label='Upper Limit')
plt.plot(user_id, average_time, 'o-', label='Average Time')
plt.plot(user_id, lower_limit, '^', label='Lower Limit')

plt.xlabel('User ID')
plt.ylabel('Phone Active Time(mins)')
plt.title('All User')
# 设置y轴为对数刻度
plt.yscale('log')
# 设置y轴刻度范围为10到1000
plt.ylim(1, 1000)
plt.legend()
# 保存图像
current_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(current_dir, 'GRAPH_mean_active_time_per_day_with_std_of_every_user.png')
plt.savefig(save_path)

plt.show()