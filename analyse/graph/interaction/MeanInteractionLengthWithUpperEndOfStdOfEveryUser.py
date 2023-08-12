from alive_progress import alive_bar

from analyse.graph.GrapgNameSapce import GRAPH_mean_interaction_length_with_upper_end_of_std_of_every_user
from analyse.graph.interaction.EveryDayAnalyseFromOutput import iter_idx_data_from_file_in_every_day
from analyse.util.AnalyseUtils import get_all_user_name_from_dir, get_mean_of_list, \
    get_upper_end_of_std
from analyse.util.FilePathDefinition import EXCEL_SUFFIX, EXPORT_SESSION_SUMMARY, TEST_OUTPUT_FILE
from util import ExcelUtil


def mean_interaction_length_with_upper_end_of_std_of_every_user():
    dirName = TEST_OUTPUT_FILE
    allUserName = get_all_user_name_from_dir(dirName)
    if allUserName:
        allUserData = []
        with alive_bar(len(allUserName), ctrl_c=True, force_tty=True, title=f'分析进度') as bar:
            for userName in allUserName:
                dataOfEveryDay = iter_idx_data_from_file_in_every_day(dirName, userName,
                                                                      EXPORT_SESSION_SUMMARY + EXCEL_SUFFIX, [3])
                # 该用户每天的数据的均值和标准差
                if isinstance(dataOfEveryDay, dict):
                    # 所有天数里，[3, 2]索引的数据，是一个dict
                    allDayData = []
                    # 将不同天里的所有数据整合在一起
                    for idx, data in enumerate(dataOfEveryDay.values()):
                        if len(allDayData) == 0:
                            allDayData = data[0]
                        else:
                            allDayData.extend(data[0])
                    # 取平均
                    result = []
                    # [...]
                    upperEndOfStd = get_upper_end_of_std(allDayData)
                    mean = get_mean_of_list(allDayData)
                    result.append(mean)
                    result.append(upperEndOfStd)
                    allUserData.append(result)
                bar()
            ExcelUtil.write_to_excel(allUserData, TEST_OUTPUT_FILE,
                                     GRAPH_mean_interaction_length_with_upper_end_of_std_of_every_user)


mean_interaction_length_with_upper_end_of_std_of_every_user()
