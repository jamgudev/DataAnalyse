from alive_progress import alive_bar

from analyse.graph.GrapgNameSapce import GRAPH_mean_active_time_per_day_with_std_of_every_user, \
    GRAPH_mean_session_count_per_day_with_std_of_every_user, GRAPH_mean_session_length_with_std_of_every_user, SS_SESSION_LENGTH_IDX
from analyse.graph.interaction.__EveryDayAnalyseFromOutput import iter_idx_data_from_file_in_every_day
from analyse.util.AnalyseUtils import get_all_user_name_from_dir, get_mean_of_list, \
    get_upper_end_of_std, get_lower_end_of_std
from analyse.util.FilePathDefinition import EXCEL_SUFFIX, EXPORT_SESSION_SUMMARY, TEST_OUTPUT_FILE, OUTPUT_FILE
from util import ExcelUtil, JLog


# Fig 3(a)
def mean_active_time_per_day_with_std_of_every_user():
    dirName = TEST_OUTPUT_FILE
    allUserName = get_all_user_name_from_dir(dirName)
    if allUserName:
        allUserData = []
        with alive_bar(len(allUserName), ctrl_c=True, force_tty=True, title=f'分析进度') as bar:
            for userName in allUserName:
                dataOfEveryDay = iter_idx_data_from_file_in_every_day(dirName, userName,
                                                                      EXPORT_SESSION_SUMMARY + EXCEL_SUFFIX,
                                                                      [SS_SESSION_LENGTH_IDX])
                # 该用户每天的数据的均值和标准差
                if isinstance(dataOfEveryDay, dict):
                    # 每天的active_time：当天所以session length总和
                    activeTimePerDay = []
                    for idx, data in enumerate(dataOfEveryDay.values()):
                        try:
                            data_str = "+".join(data[0])
                            data_sum = eval(data_str)
                            activeTimePerDay.append(int(data_sum))
                        except Exception as e:
                            JLog.e("mean_active_time_per_day_with_std_of_every_user",
                                   f"error: userName:{userName}, idx[{idx}], data:{data}, e:{e}")
                    # 取平均
                    result = []
                    # [...]
                    upperEndOfStd = get_upper_end_of_std(activeTimePerDay)
                    mean = get_mean_of_list(activeTimePerDay)
                    lowerEnd0fStd = get_lower_end_of_std(activeTimePerDay)
                    result.append(upperEndOfStd)
                    result.append(mean)
                    result.append(lowerEnd0fStd)
                    allUserData.append(result)
                bar()
            ExcelUtil.write_to_excel(allUserData, dirName,
                                     GRAPH_mean_active_time_per_day_with_std_of_every_user)


# Fig 4(a)
def mean_session_count_per_day_with_std_of_every_user():
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
                    sessionCountPerDay = []
                    for idx, data in enumerate(dataOfEveryDay.values()):
                        sessionCountPerDay.append(len(data[0]))
                    # 取平均
                    result = []
                    # [...]
                    upperEndOfStd = get_upper_end_of_std(sessionCountPerDay)
                    mean = get_mean_of_list(sessionCountPerDay)
                    lowerEnd0fStd = get_lower_end_of_std(sessionCountPerDay)
                    result.append(upperEndOfStd)
                    result.append(mean)
                    result.append(lowerEnd0fStd)
                    allUserData.append(result)
                bar()
            ExcelUtil.write_to_excel(allUserData, dirName,
                                     GRAPH_mean_session_count_per_day_with_std_of_every_user)


# Fig 4(b)
def mean_session_length_with_std_of_every_user():
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
                    # 所有的sessions
                    allSessions = []
                    for idx, data in enumerate(dataOfEveryDay.values()):
                        if len(allSessions) == 0:
                            allSessions = data[0]
                        else:
                            allSessions.extend(data[0])
                    # 取平均
                    result = []
                    # [...]
                    upperEndOfStd = get_upper_end_of_std(allSessions)
                    mean = get_mean_of_list(allSessions)
                    lowerEnd0fStd = get_lower_end_of_std(allSessions)
                    result.append(upperEndOfStd)
                    result.append(mean)
                    result.append(lowerEnd0fStd)
                    allUserData.append(result)
                bar()
            ExcelUtil.write_to_excel(allUserData, dirName,
                                     GRAPH_mean_session_length_with_std_of_every_user)


mean_active_time_per_day_with_std_of_every_user()
# mean_session_count_per_day_with_std_of_every_user()
# mean_session_length_with_std_of_every_user()
