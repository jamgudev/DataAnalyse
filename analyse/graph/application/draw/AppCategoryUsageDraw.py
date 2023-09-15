import os

import plotly.graph_objects as go

from analyse.graph.GrapgNameSapce import GRAPH_app_usage_in_all_users
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE
from util import ExcelUtil

# 读取Excel数据
dirName = TEST_OUTPUT_FILE + "/" + GRAPH_app_usage_in_all_users
df = ExcelUtil.read_excel(dirName)[1:]

# 使用列索引定位列
user_col_index = 0  # 用户列索引
app_col_index = 1   # 应用程序包名列索引
time_col_index = 2  # 使用时间列索引
app_category = 3    # app类别

# 计算每个类别的总使用时长
category_times = df.groupby(df.iloc[:, app_category])[time_col_index].sum()

# 计算总使用时长
total_time = category_times.sum()

# 计算每个类别的比率
category_ratios = category_times / total_time

# 将比率小于1%的类别归为"minority"类别
minority_threshold = 0.01
category_ratios_minority = category_ratios[category_ratios < minority_threshold]
category_ratios_majority = category_ratios[category_ratios >= minority_threshold]

# 将"minority"类别的总使用时长合并为一项
minority_time = category_times[category_ratios_minority.index].sum()
category_ratios_majority['minority'] = minority_time / total_time

# 创建饼图数据和标签
labels = category_ratios_majority.index.tolist() + ['minority']
sizes = category_ratios_majority.tolist() + [category_ratios_majority['minority']]

# 按照特定顺序重新排列标签和数值
# new_labels = labels[5:] + [labels[:5]]  # 将第一个标签放到最后
# new_sizes = sizes[5:] + [sizes[:5]]  # 对应的数值也要调整顺序

# 绘制饼图
fig = go.Figure(data=[go.Pie(labels=labels, values=sizes)])

# 设置标签的位置和方向
fig.update_traces(textinfo='percent+label', hole=0.55, textfont_size=16, insidetextorientation='horizontal',
                  rotation=110, textfont_color='black',
                  marker=dict(line=dict(color='#000000', width=1.5)))

# 修改图例字体大小
fig.update_layout(
    legend=dict(font=dict(size=16)))

# 保存图像
current_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(current_dir, 'GRAPH_app_usage_in_all_users_3.png')
fig.write_image(save_path, format="png", width=1000, height=800)

# 显示饼图
fig.show()
