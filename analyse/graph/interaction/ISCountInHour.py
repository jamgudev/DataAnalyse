from alive_progress import alive_bar

from analyse.graph.GrapgNameSapce import SS_APP_OPEN_NUM_IDX, SS_SESSION_LENGTH_IDX, SS_SESSION_START_TIME_IDX, \
    GRAPH_mean_IS_count_in_hour_per_day_for_all_users
from analyse.graph.base.__EveryDayAnalyseFromOutput import iter_idx_data_from_file_in_every_day
from analyse.util.AnalyseUtils import get_all_user_name_from_dir, get_mean_of_list
from analyse.util.FilePathDefinition import EXPORT_SESSION_SUMMARY, EXCEL_SUFFIX, TEST_OUTPUT_FILE
from util import JLog, ExcelUtil, TimeUtils


# Fig 7a，一天中各个小时段，所有用户触发的session持续时长(interactive time，有app交互的才算)
def mean_IS_count_in_hour_per_day_for_all_users():
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
                    interactMeanSessionCountInHour = []
                    ISCountInHourPerDay = {}
                    # 遍历每天数据
                    for idx, data in enumerate(dataOfEveryDay.values()):
                        try:
                            ISCountInHourInSingleDay = {}
                            # 某天数据
                            for session_idx, session_app_num in enumerate(data[0]):
                                has_launch = int(data[1][session_idx])
                                # 过滤无app的情况
                                if float(session_app_num) != 0:
                                    # 过滤只有launch页记录的情况
                                    if float(session_app_num) == 1 and has_launch == 1:
                                        continue
                                    # 根据时间段分组
                                    startTime = TimeUtils.get_hour_from_date_str_with_mills(data[2][session_idx])
                                    if startTime != -1:
                                        if startTime in ISCountInHourInSingleDay.keys():
                                            ISCountInHourInSingleDay[startTime].append(float(data[1][session_idx]))
                                        else:
                                            ISCountInHourInSingleDay[startTime] = [float(data[1][session_idx])]
                            # 计算该用户某天的在特定时间段内产生的session次数
                            for hour in range(24):
                                if hour in ISCountInHourInSingleDay:
                                    countInHourInSomeDay = len(ISCountInHourInSingleDay[hour])
                                else:
                                    countInHourInSomeDay = 0
                                if hour in ISCountInHourPerDay:
                                    ISCountInHourPerDay[hour].append(countInHourInSomeDay)
                                else:
                                    ISCountInHourPerDay[hour] = [countInHourInSomeDay]
                        except Exception as e:
                            JLog.e("mean_interactive_time_in_hour_for_all_users",
                                   f"error: userName:{userName}, idx[{idx}], data:{data}, e:{e}")
                    # 遍历完用户所有天数的数据后，ISCountInHourPerDay 每个小时间段，就有对应天数大小的list
                    for hour in range(24):
                        if hour in ISCountInHourPerDay:
                            meanSessionCount = get_mean_of_list(ISCountInHourPerDay[hour])
                            interactMeanSessionCountInHour.append(meanSessionCount)
                        else:
                            # 没有记录，说明在这个小时区间没有session，补0
                            interactMeanSessionCountInHour.append(0)
                    allUserData.append(interactMeanSessionCountInHour)
                bar()
            allUserData.insert(0, list(range(24)))
            ExcelUtil.write_to_excel(allUserData, dirName,
                                     GRAPH_mean_IS_count_in_hour_per_day_for_all_users)


mean_IS_count_in_hour_per_day_for_all_users()
