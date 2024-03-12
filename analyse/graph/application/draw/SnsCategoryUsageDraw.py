from matplotlib import font_manager, pyplot as plt

from analyse.graph.GrapgNameSapce import GRAPH_app_page_usage_in_sns
from analyse.graph.application import AppCategory
from analyse.graph.application.draw import AppColor
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE
from util import ExcelUtil


# 设置全局字体样式和大小
font_manager.fontManager.addfont('/Users/JAMGU_1/PycharmProjects/pythonProject/venv/lib/'
                                 'python3.9/site-packages/matplotlib/mpl-data/fonts/ttf/SimSun.ttf')
plt.rcParams['font.family'] = 'Times New Roman, SimSun'
plt.rcParams['font.size'] = 30
plt.figure(figsize=(16, 6))
ax = plt.axes()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_linewidth(0.5)
ax.spines['left'].set_linewidth(0.5)


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

# 将比率小于0.5%的类别归为"minority"类别
minority_threshold = 0.005
category_ratios_minority = percentages[percentages < minority_threshold]
category_ratios_majority = percentages[percentages >= minority_threshold]

# 将"minority"类别的总使用时长合并为一项
minority_time = percentages[category_ratios_minority.index].sum()
category_ratios_majority['minority'] = minority_time

# 降序排序
category_ratios_majority = category_ratios_majority.sort_values(ascending=False)

# 创建饼图数据和标签
labels = category_ratios_majority.index.tolist()
sizes = category_ratios_majority.tolist()

for idx, label in enumerate(labels):
    if label == "minority":
        labels[idx] = label
        continue
    # labels[idx] = label + "(" + AppCategory.get_app_name("", label) + ")"
    else:
        labels[idx] = AppCategory.get_app_name("", label)
        if labels[idx] == "虎扑体育":
            labels[idx] = "虎扑"


# 绘制条形图
plt.bar(labels, sizes, color=AppColor.C_11_3)
plt.xlabel("sns类应用")
plt.ylabel("停留时间占比")

# 在每个条形图的顶部添加文本标签
for index, value in enumerate(sizes):
    if index >= 12:
        break
    plt.text(labels[index], value, str(round(value, 2)), ha='center', va='bottom')

plt.text(len(labels) - 0.85, max(sizes) - 0.04, "minority: 占比小于0.5%的应用总和", ha='right', va='bottom')

# plt.xticks(rotation=35, ha='right')  # 设置刻度标签的旋转角度为0度，水平对齐方式为右对齐

plt.tight_layout()

plt.show()