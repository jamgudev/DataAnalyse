from analyse.graph.GrapgNameSapce import GRAPH_app_page_consumption, GRAPH_most_cost_energy_app_page
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE
from util import ExcelUtil


def output_most_cost_energy_app_page():
    # 读取Excel数据
    dirName = TEST_OUTPUT_FILE + "/" + GRAPH_app_page_consumption
    data = ExcelUtil.read_excel(dirName)[1:]

    user_idx_col = 0
    user_name_col = 1
    phone_brand_col = 2
    app_category_col = 3
    app_name_col = 4
    app_page_name_col = 5
    stay_duration_col = 6
    stay_duration_rate_col = 7
    app_energy_cost_rate_col = 8
    app_energy_cost_per_min_col = 9

    grouped_data = data.groupby([data.iloc[:, user_idx_col],
                                 data.iloc[:, user_name_col],
                                 data.iloc[:, phone_brand_col],
                                 data.iloc[:, app_category_col],
                                 data.iloc[:, app_name_col], data.iloc[:, app_page_name_col]])[[stay_duration_col,
                                                                                                stay_duration_rate_col,
                                                                                                app_energy_cost_rate_col]].sum()

    grouped_data['result'] = grouped_data.apply(lambda row: row[app_energy_cost_rate_col] / row[stay_duration_col], axis=1)

    # sorted_df = grouped_data.sort_values(by=grouped_data.columns[2], ascending=False)

    sorted_df = grouped_data.sort_values(by='result', ascending=False)
    filtered_df = sorted_df[sorted_df.iloc[:, 1] >= 0.05]
    output = filtered_df.head(200)
    print(output)

    # 重置索引并将索引列作为分组信息的列
    output.reset_index(inplace=True)
    output.to_excel(TEST_OUTPUT_FILE + "/" + GRAPH_most_cost_energy_app_page, index=False)

    # for index, group in enumerate(output.index):
    #     separator = " "  # 中间的分隔符
    #     print(group[0] + "_" + group[1] + "          " + separator.join(str(x) for x in output.values[index]))
