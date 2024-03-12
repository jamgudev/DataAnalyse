import matplotlib.pyplot as plt
from scipy import stats

from analyse.graph.GrapgNameSapce import GRAPH_app_category_consumption
from analyse.graph.application.draw import AppColor
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE
from util import ExcelUtil

# 设置全局字体样式和大小
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 26

# 读取Excel数据
dirName = TEST_OUTPUT_FILE + "/" + GRAPH_app_category_consumption
data = ExcelUtil.read_excel(dirName)[1:]

# 列索引
user_col_index = 0      # 用户列索引
phone_brand_col_index = 1     # 用户手机品牌
app_category_col_index = 2     # app分类列索引
category_consumption_col_index = 4   # app功耗占比列索引
data.iloc[:, category_consumption_col_index] = data.iloc[:, category_consumption_col_index] * 100.0

result = data.groupby([data.iloc[:, app_category_col_index]])[category_consumption_col_index]\
    .agg(['mean', 'std']).reset_index()

result['mean'] = result['mean'].astype(float)
result['std'] = result['std'].astype(float)

# 计算均值的95%置信区间
result['lower_bound'], result['upper_bound'] = stats.t.interval(0.95, len(data)-1, loc=result['mean'], scale=result['std']/len(data)**0.5)

result = result.sort_values('mean', ascending=True)

# 绘制散点图
plt.figure(figsize=(16, 6))
ax = plt.axes()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_linewidth(0.5)
ax.spines['left'].set_linewidth(0.5)

# plt.scatter(result.iloc[:, 0], result.iloc[:, 1], label='Mean')
# plt.plot(result.iloc[:, 0], result.iloc[:, 1], linestyle='-', color='blue')
# plt.errorbar(result.iloc[:, 0], result.iloc[:, 1], yerr=(result['upper_bound'] - result['lower_bound'])/2,
#              linestyle='', color='black', capsize=3, label='95% Confidence Interval')

x_pos = result.iloc[:, 0].values
means = result.iloc[:, 1].values
ci_upper = result['upper_bound'].values
ci_lower = result['lower_bound'].values
plt.plot(x_pos, ci_upper, '_', label='Upper CI')
plt.plot(x_pos, means, 'o-', label='Mean', color=AppColor.keli_colors[0])
plt.plot(x_pos, ci_lower, '_', label='Lower CI')
# 绘制虚线段连接Upper_limit和lower_limit
for i in range(len(x_pos)):
    plt.plot([x_pos[i], x_pos[i]], [ci_upper[i], ci_lower[i]], 'k--')

# 在每个数据点上标明纵坐标值
for i, j in result.iterrows():
    if j[result.columns[1]] > 1:
        plt.text(j[result.columns[0]], j[result.columns[1]] + 1.5, f'{j[result.columns[1]]:.2f}', ha='center', va='bottom')

plt.xticks(rotation=25, ha='right')
plt.yticks(range(0, 61, 20))
plt.subplots_adjust(bottom=0.2)

plt.xlabel('App Categories')
plt.ylabel('Consumption Percentage (%)')
# plt.title('Average Hot Pages Count and 95% Confidence Interval by App Category')

plt.legend()

# 调整图形排版，使底部的图例完整显示
plt.tight_layout()

# 显示图形
plt.show()