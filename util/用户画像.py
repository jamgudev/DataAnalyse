import pandas as pd
import plotly.graph_objects as go

from analyse.graph.application.draw import AppColor

# 读取Excel表格数据
data = pd.read_excel('用户年级分布.xlsx', header=None)

# 获取标签和数值数据
labels = data.iloc[:, 0]  # 第一列的索引号为0
values = data.iloc[:, 1]  # 第二列的索引号为1


# 绘制饼图
fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker=dict(colors=AppColor.C_11_3))])

fontsize = 30
# 设置标签的位置和方向
fig.update_traces(textinfo='label+value+percent', texttemplate='<b>%{label} (%{value}人): %{percent}</b>',
                  textfont=dict(size=fontsize, family='Times New Roman'),
                  hole=0.25, textfont_size=fontsize, insidetextorientation='horizontal',
                  textfont_family='Times New Roman',
                  rotation=45, textfont_color='black',
                  marker=dict(line=dict(color='#000000', width=1.5)))

# 修改图例字体大小
# fig.update_layout(
#     legend=dict(font=dict(size=fontsize, family='Times New Roman'),
#                 x=1.05,
#                 y=1.05,  # y轴上的位置，取值范围：0-1
#                 xanchor='center',  # x轴上的锚点位置，可选值：'auto', 'left', 'center', 'right'
#                 yanchor='top',  # y轴上的锚点位置，可选值：'auto', 'top', 'middle', 'bottom'
#                 ))
fig.update_layout(
    legend=dict(font=dict(size=24),
                x=0.15,  # 水平位置为居中（0为左对齐，1为右对齐）
                y=-0.05,  # 垂直位置为顶部（0为底部，1为顶部）
                orientation='h'))

# 显示饼图
fig.show()
