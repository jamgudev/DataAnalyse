from alive_progress import alive_bar

from analyse.graph.GrapgNameSapce import SS_SESSION_LENGTH_IDX, GRAPH_mean_active_time_per_day_with_std_of_every_user, SS_SESSION_START_TIME_IDX, \
    GRAPH_as_mean_session_length_in_week_day
from analyse.graph.interaction.__EveryDayAnalyseFromOutput import iter_idx_data_from_file_in_every_day
from analyse.util.AnalyseUtils import get_all_user_name_from_dir, get_upper_end_of_std, get_mean_of_list, get_lower_end_of_std
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE, EXPORT_SESSION_SUMMARY, EXCEL_SUFFIX
from util import JLog, ExcelUtil, TimeUtils


# Fig 3(a)
def as_mean_session_length_in_week_day():
    dirName = TEST_OUTPUT_FILE
    allUserName = get_all_user_name_from_dir(dirName)
    if allUserName:
        allUserData = []
        with alive_bar(len(allUserName), ctrl_c=True, force_tty=True, title=f'分析进度') as bar:
            for userName in allUserName:
                dataOfEveryDay = iter_idx_data_from_file_in_every_day(dirName, userName,
                                                                      EXPORT_SESSION_SUMMARY + EXCEL_SUFFIX,
                                                                      [SS_SESSION_LENGTH_IDX, SS_SESSION_START_TIME_IDX])
                # 该用户每天的数据的均值和标准差
                if isinstance(dataOfEveryDay, dict):
                    # 每天的active_time：当天所以session length总和
                    activeTimeInWeekDay = []
                    activeTimeInWeekend = []
                    for idx, data in enumerate(dataOfEveryDay.values()):
                        try:
                            data_str = "+".join(data[0])
                            data_sum = float(eval(data_str))
                            if TimeUtils.is_week_day(data[1][0]):
                                activeTimeInWeekDay.append(data_sum)
                            else:
                                activeTimeInWeekend.append(data_sum)
                        except Exception as e:
                            JLog.e("mean_active_time_per_day_with_std_of_every_user",
                                   f"error: userName:{userName}, idx[{idx}], data:{data}, e:{e}")
                    # 取平均
                    result = []
                    # [...]
                    weekDayMean = get_mean_of_list(activeTimeInWeekDay)
                    weekendMean = get_mean_of_list(activeTimeInWeekend)
                    result.append(weekDayMean)
                    result.append(weekendMean)
                    allUserData.append(result)
                bar()
            if allUserData:
                allUserData.insert(0, ["用户工作日的平均Active时长", "用户周末的平均Active时长"])
                ExcelUtil.write_to_excel(allUserData, dirName,
                                     GRAPH_as_mean_session_length_in_week_day)


as_mean_session_length_in_week_day()
