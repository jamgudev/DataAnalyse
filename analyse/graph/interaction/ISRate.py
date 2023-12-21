from alive_progress import alive_bar

from analyse.graph.GrapgNameSapce import SS_SESSION_LENGTH_IDX, SS_APP_OPEN_NUM_IDX, \
    GRAPH_user_mean_active_time_per_day_vs_total_mean_active_time_per_day, SS_SESSION_NIS_LENGTH_IDX
from analyse.graph.base.__EveryDayAnalyseFromOutput import iter_idx_data_from_file_in_every_day
from analyse.init_analyse.power_params import PowerParamsUtil
from analyse.util.AnalyseUtils import get_all_user_name_from_dir, get_mean_of_list
from analyse.util.FilePathDefinition import EXPORT_SESSION_SUMMARY, EXCEL_SUFFIX, TEST_OUTPUT_FILE
from util import JLog, ExcelUtil


# 用户每天主动触发的session与用户每天的session占比图
def user_mean_active_time_per_day_vs_total_mean_active_time_per_day(path: str = None):
    if path is None:
        dirName = TEST_OUTPUT_FILE
    else:
        dirName = path
    allUserName = get_all_user_name_from_dir(dirName)
    if allUserName:
        allUserData = []
        with alive_bar(len(allUserName), ctrl_c=True, force_tty=True, title=f'分析进度') as bar:
            for userName in allUserName:
                dataOfEveryDay = iter_idx_data_from_file_in_every_day(dirName, userName,
                                                                      EXPORT_SESSION_SUMMARY + EXCEL_SUFFIX,
                                                                      [SS_APP_OPEN_NUM_IDX, SS_SESSION_LENGTH_IDX,
                                                                       SS_SESSION_NIS_LENGTH_IDX])
                if isinstance(dataOfEveryDay, dict):
                    # 每天的active_time：当天所以session length总和
                    TSLengthPerDay = []
                    ISLengthPerDay = []
                    # 下面是次数
                    TSTimesPerDay = []
                    ISTimesPerDay = []
                    for idx, data in enumerate(dataOfEveryDay.values()):
                        try:
                            tsDurations = []
                            # isDurations元素的个数代表了有app交互的session次数，因此不可以往这个list里添加0
                            isDurations = []
                            for session_idx, session_app_num in enumerate(data[0]):
                                if float(session_app_num) != 0:
                                    tsDuration = float(data[1][session_idx])
                                    nisDuration = float(data[2][session_idx])
                                    if tsDuration > nisDuration:
                                        isDurations.append(tsDuration - nisDuration)
                                    tsDurations.append(tsDuration)
                                # 无APP交互
                                else:
                                    tsDurations.append(float(data[1][session_idx]))
                            ISLengthPerDay.append(sum(isDurations))
                            TSLengthPerDay.append(sum(tsDurations))
                            ISTimesPerDay.append(len(isDurations))
                            TSTimesPerDay.append(len(data[1]))
                        except Exception as e:
                            JLog.e("mean_active_time_per_day_with_std_of_every_user_pure",
                                   f"error: userName:{userName}, idx[{idx}], data:{data}, e:{e}")
                    # 取平均
                    result = []
                    # [...]
                    totalActiveMean = get_mean_of_list(TSLengthPerDay)
                    userActiveMean = get_mean_of_list(ISLengthPerDay)
                    result.append(totalActiveMean)
                    result.append(userActiveMean)
                    result.append(get_mean_of_list(TSTimesPerDay))
                    result.append(get_mean_of_list(ISTimesPerDay))
                    result.append(userName)
                    brand = PowerParamsUtil.get_phone_brand_by_user_name(userName)
                    result.append(brand)
                    allUserData.append(result)
                bar()
            allUserData.insert(0, ["用户每天TS总平均时长", "用户IS平均时长",
                                   "用户每天手机TS总次数", "用户每天IS次数", "用户", "型号"])
            ExcelUtil.write_to_excel(allUserData, dirName,
                                     GRAPH_user_mean_active_time_per_day_vs_total_mean_active_time_per_day)


# user_mean_active_time_per_day_vs_total_mean_active_time_per_day()
