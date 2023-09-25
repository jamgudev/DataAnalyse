import os

import matplotlib.pyplot as plt
import pandas as pd

from analyse.graph.GrapgNameSapce import GRAPH_app_page_usage_in_all
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE
from util import ExcelUtil

# 读取Excel数据
# 读取Excel文件
dirName = TEST_OUTPUT_FILE + "/" + GRAPH_app_page_usage_in_all
df = ExcelUtil.read_excel(dirName)[1:]

# 各列索引
app_category_idx = 0
app_name_idx = 1
app_page_name_idx = 2
app_page_duration_idx = 3

# 把duration=0的过滤掉
df = df[df.iloc[:, app_page_duration_idx] != 0]

app_names = pd.DataFrame(index=df.iloc[:, app_name_idx].unique())

# 计算每个app的总停留时间
app_total_time = df.groupby(df.iloc[:, app_name_idx])[app_page_duration_idx].sum()

# 计算同类app里每个app内不同页面的停留时间在该app总停留时间的占比
df['TimeRatio'] = df.groupby([df.columns[app_category_idx],
                              df.columns[app_name_idx]])[df.columns[app_page_duration_idx]].transform(lambda x: x / x.sum()).fillna(0)

# 过滤时间占比超过0.5%的数据
df = df[df['TimeRatio'] > 0.05]

hot_pages_count = df.groupby([df.iloc[:, app_category_idx],
                                       df.iloc[:, app_name_idx]]).size().reset_index(name='Hot Pages Count')

result = hot_pages_count.groupby(hot_pages_count.iloc[:, app_category_idx])['Hot Pages Count'].agg(['mean', 'std',
                                                                         lambda x: x.mean() - 1 * x.std(),
                                                                         lambda x: x.mean() + 1 * x.std()])\
    .rename(columns={'<lambda_0>': 'Lower Limit', '<lambda_1>': 'Upper Limit'})

result = result.sort_values('mean', ascending=True)

# 绘制散点图
plt.figure(figsize=(10, 6))  # 设置图形的宽度为8，高度为6
plt.scatter(result.index, result['mean'], label='Mean')
plt.plot(result.index, result['mean'], linestyle='-', color='blue')
plt.errorbar(result.index, result['mean'], yerr=result['std'], linestyle='', color='black', capsize=3, label='Standard Deviation')
# plt.plot(result.index, result['Lower Limit'], linestyle='--', color='red', label='Lower Limit')
# plt.plot(result.index, result['Upper Limit'], linestyle='--', color='green', label='Upper Limit')

plt.xticks(rotation=45, ha='right')  # 设置刻度标签的旋转角度为0度，水平对齐方式为右对齐
plt.subplots_adjust(bottom=0.2)  # 调整图形底部的边距

# 添加标签和标题
plt.xlabel('App Category')
plt.ylabel('Hot Pages Count')
plt.title('Average Hot Pages Count and Standard Deviation by App Category')

# 添加图例
plt.legend()

# 保存图像
current_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(current_dir, 'GRAPH_app_page_usage_in_all.png')
plt.savefig(save_path)

# 显示图形
plt.show()
