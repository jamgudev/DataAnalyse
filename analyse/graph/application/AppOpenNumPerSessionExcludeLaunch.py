from alive_progress import alive_bar

from analyse.graph.GrapgNameSapce import SS_APP_OPEN_NUM_IDX, \
    GRAPH_app_open_num_per_session, SS_APP_OPEN_HAS_LAUNCH_IDX, GRAPH_app_open_num_exclude_launch_per_session
from analyse.graph.base.__EveryDayAnalyseFromOutput import iter_idx_data_from_file_in_every_day
from analyse.util.AnalyseUtils import get_all_user_name_from_dir
from analyse.util.FilePathDefinition import EXPORT_SESSION_SUMMARY, EXCEL_SUFFIX, TEST_OUTPUT_FILE, OUTPUT_FILE
from util import ExcelUtil


# 获取每个session里打开不同app数量的分布情况数据
def app_open_num_exclude_launch_per_session():
    dirName = TEST_OUTPUT_FILE
    allUserName = get_all_user_name_from_dir(dirName)
    result = []
    if allUserName:
        with alive_bar(len(allUserName), ctrl_c=True, force_tty=True, title=f'分析进度') as bar:
            # 每个session里，都打开了多少个app
            # key: app_open_num, val: session_num
            appsOpenPerSession = {}
            maxNum = -1
            for userName in allUserName:
                dataOfEveryDay = iter_idx_data_from_file_in_every_day(dirName, userName,
                                                                      EXPORT_SESSION_SUMMARY + EXCEL_SUFFIX,
                                                                      [SS_APP_OPEN_NUM_IDX, SS_APP_OPEN_HAS_LAUNCH_IDX])
                if isinstance(dataOfEveryDay, dict):
                    for idx, data in enumerate(dataOfEveryDay.values()):
                        for session_idx, session_app_num in enumerate(data[0]):
                            # 过滤弹消息的情况
                            session_app_num = int(session_app_num)
                            has_launch = int(data[1][session_idx])
                            if session_app_num != 0:
                                # 过滤只有launch页记录的情况
                                if session_app_num == 1 and has_launch == 1:
                                    continue
                                # app open数量减掉launch页
                                session_app_num -= 1
                                if session_app_num in appsOpenPerSession:
                                    sessionNum = appsOpenPerSession.get(session_app_num)
                                    appsOpenPerSession[session_app_num] = sessionNum + 1
                                else:
                                    appsOpenPerSession[session_app_num] = 1
                                maxNum = max(maxNum, session_app_num)
                bar()
                
            if appsOpenPerSession:
                for i in range(1, maxNum + 1):
                    if i in appsOpenPerSession:
                        result.append([i, appsOpenPerSession.get(i)])
                    else:
                        result.append([i, 0])
    if result:
        result.insert(0, ['不同app打开数量', 'session数量'])
        ExcelUtil.write_to_excel(result, dirName,
                                 GRAPH_app_open_num_exclude_launch_per_session)


app_open_num_exclude_launch_per_session()
