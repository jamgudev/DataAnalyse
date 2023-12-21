import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from analyse.graph.GrapgNameSapce import GRAPH_app_page_usage_in_sns, GRAPH_app_page_usage_in_streaming, GRAPH_app_page_usage_in_game
from analyse.graph.application.draw import AppColor
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE, OUTPUT_FILE
from util import ExcelUtil

# 读取Excel数据
# 读取Excel文件
dirName = TEST_OUTPUT_FILE + "/" + GRAPH_app_page_usage_in_sns
df = ExcelUtil.read_excel(dirName)[1:]

# 各列索引
app_name_idx = 1
app_page_name_idx = 2
app_page_duration_idx = 3

# 把duration=0的过滤掉
df = df[df.iloc[:, app_page_duration_idx] != 0]

app_names = pd.DataFrame(index=df.iloc[:, app_name_idx].unique())

# 计算每个app的总停留时间
app_total_time = df.groupby(df.iloc[:, app_name_idx])[app_page_duration_idx].sum()

# 计算每个app内不同页面的停留时间在该app总停留时间的占比
df['TimeRatio'] = df.groupby(df.iloc[:, app_name_idx])[app_page_duration_idx].transform(lambda x: x / x.sum()).fillna(0)
# 按分组排序并按占比升序排序
df = df.sort_values([df.columns[app_name_idx], 'TimeRatio'], ascending=False)

# 将小于0.05的比例归类为"Other"
df.loc[df['TimeRatio'] < 0.05, df.columns[app_page_name_idx]] = "minority"
usage_ratio_less_than_5_percent_name = "minority"

# 获取所有应用程序列表（除了"Other"）
appPages = df[df.iloc[:, app_page_name_idx] != usage_ratio_less_than_5_percent_name].iloc[:, app_page_name_idx].unique()

# 将"minority"应用程序放到最后
appPages = list(appPages) + [usage_ratio_less_than_5_percent_name]

# 绘制条形累计分布图
fig, ax = plt.subplots(figsize=(36, 10))

# 获取每个app的编号
app_ids = np.arange(len(app_total_time)) + 1

# 绘制每个页面的条形图
colors = AppColor.custom_colors
x = range(1, len(df.iloc[:, app_name_idx].unique()) + 1)
bottom = [0] * len(app_ids)
for i, appPageName in enumerate(appPages):
    app_page_ratios = df[df.iloc[:, app_page_name_idx] == appPageName].groupby(df.iloc[:, app_name_idx])['TimeRatio'].sum()
    app_page_ratios = app_page_ratios.reindex(app_names.index, fill_value=0)  # 重新索引并用0填充缺失值
    if appPageName == usage_ratio_less_than_5_percent_name:
        ax.bar(x, app_page_ratios.values, bottom=bottom, label=appPageName, color="black")
    else:
        ax.bar(x, app_page_ratios.values, bottom=bottom, label=appPageName, color=colors[i % len(colors)])
    bottom += app_page_ratios

# 设置x轴标签和刻度
fontSize = 28
x_ticks = list(app_ids[::10])  # 每隔10个取一个刻度位置
ax.set_xticks(x_ticks)
ax.set_xticklabels(x_ticks)
ax.set_xlim(0, len(x) + 1)

# 设置y轴标签和范围
ax.set_xlabel('App', fontsize=fontSize)
ax.tick_params(axis='x', labelsize=fontSize)
ax.tick_params(axis='y', labelsize=fontSize)
ax.set_ylabel('Page Usage Time Ratio', fontsize=fontSize)
ax.set_ylim(0, 1)

# 添加图例
# ax.legend()

# 展示图像
plt.show()
