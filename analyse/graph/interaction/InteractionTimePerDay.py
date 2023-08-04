from alive_progress import alive_bar

from alive_progress import alive_bar

from analyse.graph.interaction.EveryDayAnalyseFromOutput import iter_idx_data_from_file_in_every_day
from analyse.util.AnalyseUtils import get_all_user_name_from_dir, get_standard_deviation_of_dict, get_mean_of_dict
from analyse.util.FilePathDefinition import INPUT_FILE, EXCEL_SUFFIX, EXPORT_SESSION_SUMMARY, OUTPUT_FILE
from util import ExcelUtil


def interaction_time_per_day():
    dirName = OUTPUT_FILE
    allUserName = get_all_user_name_from_dir(dirName)
    if allUserName:
        allUserStdData = []
        allUserMeanData = []
        with alive_bar(len(allUserName), ctrl_c=True, title=f'分析进度') as bar:
            for userName in allUserName:
                dataOfEveryDay = iter_idx_data_from_file_in_every_day(dirName, userName,
                                                                 EXPORT_SESSION_SUMMARY + EXCEL_SUFFIX, [3])
                # 该用户每天的数据的均值和标准差
                std = get_standard_deviation_of_dict(dataOfEveryDay)
                mean = get_mean_of_dict(dataOfEveryDay)
                allUserStdData.append(std)
                allUserMeanData.append(mean)
                bar()
            ExcelUtil.write_to_excel(allUserStdData, OUTPUT_FILE, "interaction_time_per_day_std.xlsx")
            ExcelUtil.write_to_excel(allUserMeanData, OUTPUT_FILE, "interaction_time_per_day_mean.xlsx")

interaction_time_per_day()