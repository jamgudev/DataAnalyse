from alive_progress import alive_bar

from analyse.graph.GrapgNameSapce import SS_SESSION_LENGTH_IDX, SS_APP_OPEN_NUM_IDX, \
    GRAPH_user_mean_active_time_per_day_vs_total_mean_active_time_per_day
from analyse.graph.interaction.__EveryDayAnalyseFromOutput import iter_idx_data_from_file_in_every_day
from analyse.util.AnalyseUtils import get_all_user_name_from_dir, get_mean_of_list
from analyse.util.FilePathDefinition import EXPORT_SESSION_SUMMARY, EXCEL_SUFFIX, TEST_OUTPUT_FILE
from util import JLog, ExcelUtil


# 用户每天主动触发的session与用户每天的session占比图
def user_mean_active_time_per_day_vs_total_mean_active_time_per_day():
    dirName = TEST_OUTPUT_FILE
    allUserName = get_all_user_name_from_dir(dirName)
    if allUserName:
        allUserData = []
        with alive_bar(len(allUserName), ctrl_c=True, force_tty=True, title=f'分析进度') as bar:
            for userName in allUserName:
                dataOfEveryDay = iter_idx_data_from_file_in_every_day(dirName, userName,
                                                                      EXPORT_SESSION_SUMMARY + EXCEL_SUFFIX,
                                                                      [SS_APP_OPEN_NUM_IDX, SS_SESSION_LENGTH_IDX])
                # 该用户每天的数据的均值和标准差
                if isinstance(dataOfEveryDay, dict):
                    # 每天的active_time：当天所以session length总和
                    totalActiveTimePerDay = []
                    userActiveTimePerDay = []
                    # 下面是次数
                    totalActiveTimesPerDay = []
                    userActiveTimesPerDay = []
                    for idx, data in enumerate(dataOfEveryDay.values()):
                        try:
                            activeInteractions = []
                            for session_idx, session_app_num in enumerate(data[0]):
                                if float(session_app_num) != 0:
                                    activeInteractions.append(float(data[1][session_idx]))
                            userActiveTimePerDay.append(sum(activeInteractions))
                            data_str = "+".join(data[1])
                            data_sum = eval(data_str)
                            totalActiveTimePerDay.append(int(data_sum))
                            totalActiveTimesPerDay.append(len(data[1]))
                            userActiveTimesPerDay.append(len(activeInteractions))
                        except Exception as e:
                            JLog.e("mean_active_time_per_day_with_std_of_every_user_pure",
                                   f"error: userName:{userName}, idx[{idx}], data:{data}, e:{e}")
                    # 取平均
                    result = []
                    # [...]
                    totalActiveMean = get_mean_of_list(totalActiveTimePerDay)
                    userActiveMean = get_mean_of_list(userActiveTimePerDay)
                    result.append(totalActiveMean)
                    result.append(userActiveMean)
                    result.append(get_mean_of_list(totalActiveTimesPerDay))
                    result.append(get_mean_of_list(userActiveTimesPerDay))
                    allUserData.append(result)
                bar()
            allUserData.insert(0, ["用户每天Active总平均时长", "用户每天主动触发的Active平均时长",
                                   "用户每天手机总Active次数", "用户每天手机中用户触发的Active次数"])
            ExcelUtil.write_to_excel(allUserData, dirName,
                                     GRAPH_user_mean_active_time_per_day_vs_total_mean_active_time_per_day)


user_mean_active_time_per_day_vs_total_mean_active_time_per_day()
