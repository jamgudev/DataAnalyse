from alive_progress import alive_bar

from analyse.graph.GrapgNameSapce import SS_SESSION_LENGTH_IDX, SS_APP_OPEN_NUM_IDX, GRAPH_all_interactions_cdf
from analyse.graph.base.__EveryDayAnalyseFromOutput import iter_idx_data_from_file_in_every_day
from analyse.util.AnalyseUtils import get_all_user_name_from_dir
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE, EXPORT_SESSION_SUMMARY, EXCEL_SUFFIX
from util import JLog, ExcelUtil


def all_interactions_cdf():
    dirName = TEST_OUTPUT_FILE
    allUserName = get_all_user_name_from_dir(dirName)
    if allUserName:
        allInteractionData = []
        with alive_bar(len(allUserName), ctrl_c=True, force_tty=True, title=f'分析进度') as bar:
            for userName in allUserName:
                dataOfEveryDay = iter_idx_data_from_file_in_every_day(dirName, userName,
                                                                      EXPORT_SESSION_SUMMARY + EXCEL_SUFFIX,
                                                                      [SS_APP_OPEN_NUM_IDX, SS_SESSION_LENGTH_IDX])
                if isinstance(dataOfEveryDay, dict):
                    # 每个小时内，有app记录的mean session length
                    for idx, data in enumerate(dataOfEveryDay.values()):
                        try:
                            for session_idx, session_app_num in enumerate(data[0]):
                                # 过滤无app的情况
                                if float(session_app_num) != 0:
                                    allInteractionData.append(float(data[1][session_idx]))
                        except Exception as e:
                            JLog.e("mean_active_time_per_day_with_std_of_every_user_pure",
                                   f"error: userName:{userName}, idx[{idx}], data:{data}, e:{e}")
                bar()
            allInteractionData.insert(0, "IS Session Length")
            ExcelUtil.write_to_excel(allInteractionData, dirName, GRAPH_all_interactions_cdf)


all_interactions_cdf()
