import os

import matplotlib.pyplot as plt

from analyse.graph.GrapgNameSapce import GRAPH_mean_active_time_per_day_with_std_of_every_user, GRAPH_as_mean_session_length_in_week_day
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE
from util import ExcelUtil

# 数据预处理:
# 1. 去掉title

# 读取Excel文件
dirName = TEST_OUTPUT_FILE + "/" + GRAPH_as_mean_session_length_in_week_day
data = ExcelUtil.read_excel(dirName)

# 获取用户ID、上限、平均时间和下限列的数据
weekDayMean = data.iloc[:, 0].apply(lambda x: x / (1000 * 60))
weekendMean = data.iloc[:, 1].apply(lambda x: x / (1000 * 60))
result = [a / b for a, b in zip(weekendMean, weekDayMean)]
# 升序排序
result = sorted(result, reverse=False)
user_id = [i for i in range(1, len(result) + 1)]

plt.plot(user_id, result, 'o', label='Upper Limit')

plt.xlabel('Users')
plt.ylabel('Mean AS Length in weekend/ Mean AS Length in weekday(mins)')
plt.title('All User')
# 设置y轴为对数刻度
# plt.yscale('log')
# 设置y轴刻度范围为10到1000
# plt.ylim(1, 1000)
# plt.legend()
# 保存图像
current_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(current_dir, 'GRAPH_as_mean_session_length_in_week_day.png')
# plt.savefig(save_path)

plt.show()