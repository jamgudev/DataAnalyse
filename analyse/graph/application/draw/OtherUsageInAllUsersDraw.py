import os

import pandas as pd
import matplotlib.pyplot as plt

from analyse.graph.GrapgNameSapce import GRAPH_app_usage_in_all_users
from analyse.util.FilePathDefinition import OUTPUT_FILE, TEST_OUTPUT_FILE
from util import ExcelUtil
# 读取Excel文件
dirName = TEST_OUTPUT_FILE + "/" + GRAPH_app_usage_in_all_users
df = ExcelUtil.read_excel(dirName)[1:]

# 使用列索引定位列
user_col_index = 0  # 用户列索引
app_col_index = 1   # 应用程序包名列索引
time_col_index = 2  # 使用时间列索引

# 将应用程序包名列中第一个.之前的的字符去掉
df.iloc[:, app_col_index] = df.iloc[:, app_col_index].str.replace(r'^[^.]*\.', '', regex=True)
# 将时间值转换为分钟
df.iloc[:, time_col_index] = df.iloc[:, time_col_index] / (60 * 1000)

# 计算每个用户每个app的使用时长占该用户总使用时长的比例
df['TimeRatio'] = df.groupby(df.iloc[:, user_col_index])[time_col_index].transform(lambda x: x / x.sum()).fillna(0)

# 计算每个app的总使用时长占总使用时长的比例
app_total_time = df.groupby(df.iloc[:, app_col_index])[time_col_index].sum()
app_total_ratio = app_total_time / app_total_time.sum()

# 将小于0.01的比例归类为"Other"
df.loc[df['TimeRatio'] > 0.05, df.columns[app_col_index]] = "Other"

# 绘制条形累计占比图
fig, ax = plt.subplots(figsize=(32, 20))

users = df.iloc[:, user_col_index].unique()
bottom = [0] * len(users)

# 创建一个包含所有用户的DataFrame，用于重新索引app_ratios
all_users_df = pd.DataFrame(index=users)
# 获取所有应用程序列表（除了"Other"）
apps = df[df.iloc[:, app_col_index] != "Other"].iloc[:, app_col_index].unique()

# 将"Other"应用程序放到最后
apps = list(apps) + ["Other"]
# for app in df.iloc[:, app_col_index].unique():
for app in apps:
    app_ratios = df[df.iloc[:, app_col_index] == app].groupby(df.iloc[:, user_col_index])['TimeRatio'].sum()
    app_ratios = app_ratios.reindex(all_users_df.index, fill_value=0)  # 重新索引并用0填充缺失值
    if app == "Other":
        # ax.bar(range(1, len(users) + 1), app_ratios.values, bottom=bottom, label=app, color="black")
        var = 11
    else:
        ax.bar(range(1, len(users) + 1), app_ratios.values, bottom=bottom, label=app)
    bottom += app_ratios

fontSize = 28
ax.set_xlabel('User', fontsize=fontSize)
ax.set_ylabel('App Usage Time Ratio', fontsize=fontSize)
ax.tick_params(axis='x', labelsize=fontSize)
ax.tick_params(axis='y', labelsize=fontSize)
ax.set_title('App Usage Time Ratio by User', fontsize=fontSize)
ax.set_xlim(0, 46)
# 调整图表和标签的位置
plt.subplots_adjust(top=0.96, left=0.05, right=0.95, bottom=0.45)

# 显示标签在图表的下方
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.06), ncol=6, fontsize=22)
# 保存图像
current_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(current_dir, 'GRAPH_other_app_usage_in_all_users.png')
plt.savefig(save_path)

plt.show()
