import matplotlib.pyplot as plt

from analyse.graph.GrapgNameSapce import GRAPH_mean_active_time_per_day_with_std_of_every_user
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE
from util import ExcelUtil

# 读取Excel文件
dirName = TEST_OUTPUT_FILE + "/" + GRAPH_mean_active_time_per_day_with_std_of_every_user
data = ExcelUtil.read_excel(dirName)

# 获取用户ID、上限、平均时间和下限列的数据
user_id = data.iloc[:, 0]
upper_limit = data.iloc[:, 1]
average_time = data.iloc[:, 2]
lower_limit = data.iloc[:, 3]
# 绘制虚线段连接Upper_limit和lower_limit
for i in range(len(user_id)):
    plt.plot([user_id[i], user_id[i]], [upper_limit[i], lower_limit[i]], 'k--')

plt.plot(user_id, upper_limit, 'v', label='Upper Limit')
plt.plot(user_id, average_time, 'o-', label='Average Time')
plt.plot(user_id, lower_limit, '^', label='Lower Limit')

plt.xlabel('User ID')
plt.ylabel('Phone Usage Time')
plt.title('User Phone Usage Data')
plt.legend()
plt.show()