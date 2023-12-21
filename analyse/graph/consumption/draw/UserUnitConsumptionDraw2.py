import matplotlib.pyplot as plt
from scipy import stats

from analyse.graph.GrapgNameSapce import GRAPH_user_units_consumption
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE
from util import ExcelUtil

# 读取Excel数据
dirName = TEST_OUTPUT_FILE + "/" + GRAPH_user_units_consumption
data = ExcelUtil.read_excel(dirName)[1:]


# 列索引
user_col_index = 0      # 用户列索引
user_brand_index = 1    # 用户手机品牌索引
units_col_index = 2     # 部件列索引
units_consumption_col_index = 3   # 部件功耗占比列索引
data.iloc[:, units_consumption_col_index] = data.iloc[:, units_consumption_col_index] * 100

# 过滤功耗占比为0的bluetooth
data = data[data.iloc[:, units_consumption_col_index] != 0]

result = data.groupby([data.iloc[:, units_col_index]])[units_consumption_col_index] \
    .agg(['mean', 'std']).reset_index()

result['mean'] = result['mean'].astype(float)
result['std'] = result['std'].astype(float)

# 计算均值的95%置信区间
result['lower_bound'], result['upper_bound'] = stats.t.interval(0.95, len(data)-1, loc=result['mean'], scale=result['std']/len(data)**0.5)

result = result.sort_values('mean', ascending=True)

# 绘制散点图
plt.figure(figsize=(6, 6))
plt.scatter(result.iloc[:, 0], result.iloc[:, 1], label='Mean')
plt.plot(result.iloc[:, 0], result.iloc[:, 1], linestyle='-', color='blue')
plt.errorbar(result.iloc[:, 0], result.iloc[:, 1], yerr=(result['upper_bound'] - result['lower_bound'])/2,
             linestyle='', color='black', capsize=3, label='95% Confidence Interval')

# 在每个数据点上标明纵坐标值
for i, j in result.iterrows():
    plt.text(j[result.columns[0]], j[result.columns[1]] + 1.5, f'{j[result.columns[1]]:.2f}', ha='center', va='bottom')

# plt.xticks(rotation=35, ha='right')
plt.subplots_adjust(bottom=0.2)

plt.xlabel('App Category')
plt.ylabel('Consumption Ratios(%)')
# plt.title('Average Hot Pages Count and 95% Confidence Interval by App Category')

plt.legend()

# 显示图形
plt.show()