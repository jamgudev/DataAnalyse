import os
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import font_manager
from scipy import stats
from analyse.graph.GrapgNameSapce import GRAPH_app_page_usage_in_all
from analyse.graph.application.draw import AppColor
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE
from util import ExcelUtil

# 设置全局字体样式和大小
font_manager.fontManager.addfont('/Users/JAMGU_1/PycharmProjects/pythonProject/venv/lib/'
                                 'python3.9/site-packages/matplotlib/mpl-data/fonts/ttf/SimSun.ttf')
plt.rcParams['font.family'] = 'Times New Roman, SimSun'
plt.rcParams['font.size'] = 30

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

x = result.iloc[:, 0].values
mean = result.iloc[:, 1]
upper_ci = result['upper_bound']
lower_ci = result['lower_bound']
# 绘制散点图
plt.figure(figsize=(16, 6))
# plt.scatter(x, result.iloc[:, 1], label='Mean')
# plt.plot(x, result.iloc[:, 1], linestyle='-', color='blue')
# plt.errorbar(x, mean, yerr=(result['upper_bound'] - result['lower_bound'])/2, fmt='o-', color='black', capsize=3, label='95% Confidence Interval')

ax = plt.axes()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_linewidth(0.5)
ax.spines['left'].set_linewidth(0.5)

plt.plot(x, upper_ci, '_', label='CI上限')
plt.plot(x, mean, 'o-', label='均值', color=AppColor.keli_colors[0])
plt.plot(x, lower_ci, '_', label='CI上限')
# # 绘制虚线段连接Upper_limit和lower_limit
for i in range(len(x)):
    plt.plot([x[i], x[i]], [upper_ci.values[i], lower_ci.values[i]], 'k--')

# 在每个散点上方标出具体数值
for i in range(len(x)):
    if i % 2 == 0:
        plt.text(x[i], mean.values[i], f'{mean.values[i]:.1f}', ha='center', va='bottom')

plt.xticks(rotation=25, ha='right')
plt.subplots_adjust(bottom=0.2)

plt.xlabel('APP类别')
plt.ylabel('热门页面数量')
# plt.title('Average Hot Pages Count and 95% Confidence Interval by App Category')

plt.yticks(range(1, 6, 1))
plt.legend()
plt.tight_layout()

# 保存图像
current_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(current_dir, '../GRAPH_app_page_usage_in_all.png')
plt.savefig(save_path)

# 显示图形
plt.show()