import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from analyse.graph.GrapgNameSapce import GRAPH_app_page_usage_in_sns
from analyse.graph.application import AppCategory
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE
from util import ExcelUtil

# 读取Excel文件
dirName = TEST_OUTPUT_FILE + "/" + GRAPH_app_page_usage_in_sns
df = ExcelUtil.read_excel(dirName)[1:]

# 使用列索引定位列
category_col_index = 0  # 分类列索引
package_col_index = 1   # 应用程序包名列索引
page_col_index = 2      # 页面索引
duration_col_index = 3  # 使用时间列索引

# 按包名分组并计算总时间
grouped = df.groupby(df.iloc[:, package_col_index])[df.columns[duration_col_index]].sum()
# df['TimeRatio'] = df.groupby(df.iloc[:, package_col_index])[duration_col_index].transform(lambda x: x / x.sum()).fillna(0)

# 计算总时间
total_time = grouped.sum()

# 计算每个包名的时间占比
percentages = grouped / total_time

# 将比率小于1%的类别归为"minority"类别
minority_threshold = 0.005
category_ratios_minority = percentages[percentages < minority_threshold]
category_ratios_majority = percentages[percentages >= minority_threshold]

# 将"minority"类别的总使用时长合并为一项
minority_time = percentages[category_ratios_minority.index].sum()
category_ratios_majority['minority'] = minority_time

# 创建饼图数据和标签
labels = category_ratios_majority.index.tolist()
sizes = category_ratios_majority.tolist()

for idx, label in enumerate(labels):
    if label == "minority":
        labels[idx] = label + "(占比小于0.5%的应用总和)"
        continue
    labels[idx] = label + "(" + AppCategory.get_app_name("", label) + ")"

# 绘制饼图
fig = go.Figure(data=[go.Pie(labels=labels, values=sizes)])

# 设置标签的位置和方向
fig.update_traces(textinfo='percent+label', hole=0.55, textfont_size=24, insidetextorientation='horizontal',
                  rotation=160, textfont_color='black',
                  marker=dict(line=dict(color='#000000', width=1.5)))

# 修改图例字体大小
fig.update_layout(
    legend=dict(font=dict(size=16),
                x=0.15,  # 水平位置为居中（0为左对齐，1为右对齐）
                y=-0.05,  # 垂直位置为顶部（0为底部，1为顶部）
                orientation='h'))

# 显示饼图
fig.show()