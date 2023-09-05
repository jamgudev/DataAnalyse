from alive_progress import alive_bar

from analyse.graph.GrapgNameSapce import AS_APP_NAME, AS_APP_DURATION, GRAPH_app_usage_in_all_users
from analyse.graph.base.__EveryDayAnalyseFromOutput import iter_idx_data_from_file_in_every_day
from analyse.util.AnalyseUtils import get_all_user_name_from_dir
from analyse.util.FilePathDefinition import EXCEL_SUFFIX, OUTPUT_FILE, \
    EXPORT_APP_SUMMARY_USAGES, TEST_OUTPUT_FILE
from util import JLog, ExcelUtil


# 所有用户，在各个app使用的时间占用户各自总使用时间的占比
def app_usage_in_all_users():
    dirName = TEST_OUTPUT_FILE
    allUserName = get_all_user_name_from_dir(dirName)
    if allUserName:
        allUserData = []
        with alive_bar(len(allUserName), ctrl_c=True, force_tty=True, title=f'分析进度') as bar:
            for userName in allUserName:
                dataOfEveryDay = iter_idx_data_from_file_in_every_day(dirName, userName,
                                                                      EXPORT_APP_SUMMARY_USAGES + EXCEL_SUFFIX,
                                                                      [AS_APP_NAME, AS_APP_DURATION])
                if isinstance(dataOfEveryDay, dict):
                    appUsageDict = {}
                    # 遍历每天数据
                    for idx, data in enumerate(dataOfEveryDay.values()):
                        try:
                            # 遍历一天中的所有数据
                            for app_usage_idx, app_usage_name in enumerate(data[0]):
                                appStayDuration = float(data[1][app_usage_idx])
                                if app_usage_name in appUsageDict:
                                    appUsageDict[app_usage_name] += appStayDuration
                                else:
                                    appUsageDict[app_usage_name] = appStayDuration
                        except Exception as e:
                            JLog.e("mean_active_time_per_day_with_std_of_every_user_pure",
                                   f"error: userName:{userName}, idx[{idx}], data:{data}, e:{e}")
                    for key in appUsageDict.keys():
                        allUserData.append([userName, key, appUsageDict[key]])
                bar()
            allUserData.insert(0, ["用户名", "用户使用的app名",
                                   "用户在该App停留多长时间"])
            ExcelUtil.write_to_excel(allUserData, dirName,
                                     GRAPH_app_usage_in_all_users)


app_usage_in_all_users()
