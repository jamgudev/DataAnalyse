import os
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
from analyse.graph.GrapgNameSapce import GRAPH_app_page_usage_in_all
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE
from util import ExcelUtil

# 读取Excel数据
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
df['TimeRatio'] = df.groupby([df.columns[app_category_idx], df.columns[app_name_idx]])[df.columns[app_page_duration_idx]].transform(lambda x: x / x.sum()).fillna(0)

# 过滤时间占比超过0.5%的数据
df = df[df['TimeRatio'] > 0.05]

hot_pages_count = df.groupby([df.iloc[:, app_category_idx], df.iloc[:, app_name_idx]]).size().reset_index(name='Hot Pages Count')

result = hot_pages_count.groupby(hot_pages_count.iloc[:, app_category_idx])['Hot Pages Count'].agg(['mean', 'std']).reset_index()

# 计算均值的95%置信区间
result['lower_bound'], result['upper_bound'] = stats.t.interval(0.95, len(hot_pages_count)-1, loc=result['mean'], scale=result['std']/len(hot_pages_count)**0.5)

result = result.sort_values('mean', ascending=True)

# 绘制散点图
plt.figure(figsize=(10, 6))
plt.scatter(result.iloc[:, 0], result.iloc[:, 1], label='Mean')
plt.plot(result.iloc[:, 0], result.iloc[:, 1], linestyle='-', color='blue')
plt.errorbar(result.iloc[:, 0], result.iloc[:, 1], yerr=(result['upper_bound'] - result['lower_bound'])/2, linestyle='', color='black', capsize=3, label='95% Confidence Interval')

plt.xticks(rotation=35, ha='right')
plt.subplots_adjust(bottom=0.2)

plt.xlabel('App Category')
plt.ylabel('Hot Pages Count')
plt.title('Average Hot Pages Count and 95% Confidence Interval by App Category')

plt.legend()

# 保存图像
current_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(current_dir, 'GRAPH_app_page_usage_in_all.png')
plt.savefig(save_path)

# 显示图形
plt.show()