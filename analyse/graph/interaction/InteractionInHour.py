from alive_progress import alive_bar

from analyse.graph.GrapgNameSapce import SS_APP_OPEN_NUM_IDX, SS_SESSION_LENGTH_IDX, GRAPH_mean_active_time_per_day_with_std_of_every_user_pure, \
    GRAPH_mean_interactive_time_in_hour_for_all_users, SS_SESSION_START_TIME_IDX
from analyse.graph.interaction.__EveryDayAnalyseFromOutput import iter_idx_data_from_file_in_every_day
from analyse.util.AnalyseUtils import get_all_user_name_from_dir, get_upper_end_of_std, get_mean_of_list, get_lower_end_of_std
from analyse.util.FilePathDefinition import OUTPUT_FILE, EXPORT_SESSION_SUMMARY, EXCEL_SUFFIX, TEST_OUTPUT_FILE
from util import JLog, ExcelUtil, TimeUtils


# Fig 7a，一天中各个小时段，所有用户触发的session持续时长(interactive time，有app交互的才算)
def mean_interactive_time_in_hour_for_all_users():
    dirName = TEST_OUTPUT_FILE
    allUserName = get_all_user_name_from_dir(dirName)
    if allUserName:
        allUserData = []
        with alive_bar(len(allUserName), ctrl_c=True, force_tty=True, title=f'分析进度') as bar:
            for userName in allUserName:
                dataOfEveryDay = iter_idx_data_from_file_in_every_day(dirName, userName,
                                                                      EXPORT_SESSION_SUMMARY + EXCEL_SUFFIX,
                                                                      [SS_APP_OPEN_NUM_IDX, SS_SESSION_LENGTH_IDX, SS_SESSION_START_TIME_IDX])
                if isinstance(dataOfEveryDay, dict):
                    # 每个小时内，有app记录的mean session length
                    interactMeanSessionInHour = []
                    interactiveTimeInHour = {}
                    for idx, data in enumerate(dataOfEveryDay.values()):
                        try:
                            for session_idx, session_app_num in enumerate(data[0]):
                                # 过滤无app的情况
                                if float(session_app_num) != 0:
                                    # 根据时间段分组
                                    startTime = TimeUtils.get_hour_from_date_str_with_mills(data[2][session_idx])
                                    if startTime != -1:
                                        if startTime in interactiveTimeInHour.keys():
                                            interactiveTimeInHour[startTime].append(float(data[1][session_idx]))
                                        else:
                                            interactiveTimeInHour[startTime] = [float(data[1][session_idx])]
                        except Exception as e:
                            JLog.e("mean_active_time_per_day_with_std_of_every_user_pure",
                                   f"error: userName:{userName}, idx[{idx}], data:{data}, e:{e}")
                    for hour in range(24):
                        if hour in interactiveTimeInHour:
                            meanSessionLength = get_mean_of_list(interactiveTimeInHour[hour])
                            interactMeanSessionInHour.append(meanSessionLength)
                        else:
                            # 没有记录，说明在这个小时区间没有session，补0
                            interactMeanSessionInHour.append(0)
                    allUserData.append(interactMeanSessionInHour)
                bar()
            ExcelUtil.write_to_excel(allUserData, dirName,
                                     GRAPH_mean_interactive_time_in_hour_for_all_users)


mean_interactive_time_in_hour_for_all_users()
