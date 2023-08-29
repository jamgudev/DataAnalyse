from alive_progress import alive_bar

from analyse.graph.GrapgNameSapce import SS_SESSION_LENGTH_IDX, SS_SESSION_START_TIME_IDX, \
    GRAPH_mean_session_length_vs_session_count_per_day_of_every_user, SS_APP_OPEN_NUM_IDX
from analyse.graph.interaction.__EveryDayAnalyseFromOutput import iter_idx_data_from_file_in_every_day
from analyse.util.AnalyseUtils import get_all_user_name_from_dir, get_mean_of_dict, get_mean_of_list
from analyse.util.FilePathDefinition import OUTPUT_FILE, EXPORT_SESSION_SUMMARY, EXCEL_SUFFIX, TEST_OUTPUT_FILE
from util import ExcelUtil


# 获取每个用户session每天数量与session的平均长度的散点图原数据
# session平均长度：用户A所有的Session Length总和 / 用户A所有的Session Count
# session每天数量：用户A所有Session数量 / 记录实验天数
def get_mean_session_length_vs_session_count_per_day_of_every_user():
    dirName = TEST_OUTPUT_FILE
    allUserName = get_all_user_name_from_dir(dirName)
    sessionCountVsMeanSessionLengthOfUser = []
    if allUserName:
        with alive_bar(len(allUserName), ctrl_c=True, force_tty=True, title=f'分析进度') as bar:
            for userName in allUserName:
                dataOfEveryDay = iter_idx_data_from_file_in_every_day(dirName, userName,
                                                                      EXPORT_SESSION_SUMMARY + EXCEL_SUFFIX,
                                                                      [SS_APP_OPEN_NUM_IDX, SS_SESSION_LENGTH_IDX])
                dayNum = len(dataOfEveryDay.keys())
                if isinstance(dataOfEveryDay, dict):
                    # 所有天数里，[3, 2]索引的数据，是一个dict
                    # 将不同天里的所有数据整合在一起
                    allSessionsPerDay = []
                    for idx, data in enumerate(dataOfEveryDay.values()):
                        interactSessionsInSingleDay = []
                        for session_idx, session_app_num in enumerate(data[0]):
                            # 过滤弹消息的情况
                            if float(session_app_num) != 0:
                                interactSessionsInSingleDay.append(float(data[1][session_idx]))
                        allSessionsPerDay.extend(interactSessionsInSingleDay)
                    # 取平均
                    result = []
                    # [...]
                    meanSessionLength = get_mean_of_list(allSessionsPerDay)
                    sessionCountPerDay = round(len(allSessionsPerDay) / dayNum + 0.5)
                    result.append(meanSessionLength)
                    result.append(sessionCountPerDay)
                    sessionCountVsMeanSessionLengthOfUser.append(result)
                bar()
    if sessionCountVsMeanSessionLengthOfUser:
        ExcelUtil.write_to_excel(sessionCountVsMeanSessionLengthOfUser, dirName,
                                 GRAPH_mean_session_length_vs_session_count_per_day_of_every_user)


get_mean_session_length_vs_session_count_per_day_of_every_user()
