import os.path

from alive_progress import alive_bar

from analyse.graph.GrapgNameSapce import AS_APP_NAME, AS_APP_DURATION, GRAPH_user_mean_active_time_per_day_vs_total_mean_active_time_per_day, \
    AS_APP_CATEGORY, GRAPH_app_category_usage_in_diff_group_users
from analyse.graph.application.AppCategory import get_all_app_categories
from analyse.graph.base.__EveryDayAnalyseFromOutput import iter_idx_data_from_file_in_every_day
from analyse.graph.interaction.ISRate import user_mean_active_time_per_day_vs_total_mean_active_time_per_day
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE, EXPORT_APP_SUMMARY_USAGES, EXCEL_SUFFIX
from util import ExcelUtil, JLog


# 不同类型app在不同人群用户（手机重度用户及轻度用户）中的使用分布情况
def app_category_usage_in_diff_group_users():
    dirName = TEST_OUTPUT_FILE
    filePath = dirName + "/" + GRAPH_user_mean_active_time_per_day_vs_total_mean_active_time_per_day
    if not os.path.exists(filePath):
        JLog.d("app_category_usage_in_diff_group_users", f"excel file:{filePath} not exist,"
                                                         f" do user_mean_active_time_per_day_vs_total_mean_active_time_per_day() first.")
        user_mean_active_time_per_day_vs_total_mean_active_time_per_day(dirName)

    df = ExcelUtil.read_excel(filePath)[1:]
    # 按 is length 升序排序
    df = df.sort_values(df.columns[1], ascending=True)
    allUserName = list(df.iloc[:, 4])
    if allUserName:
        allUserData = []
        allAppCategories = get_all_app_categories(dirName)
        with alive_bar(len(allUserName), ctrl_c=True, force_tty=True, title=f'分析进度') as bar:
            userLen = len(allUserName)
            for name_id, userName in enumerate(allUserName):
                groupUsage = {}
                dataOfEveryDay = iter_idx_data_from_file_in_every_day(dirName, userName,
                                                                      EXPORT_APP_SUMMARY_USAGES + EXCEL_SUFFIX,
                                                                      [AS_APP_NAME, AS_APP_CATEGORY, AS_APP_DURATION])
                if isinstance(dataOfEveryDay, dict):
                    # 遍历每天数据
                    for idx, data in enumerate(dataOfEveryDay.values()):
                        try:
                            # 遍历一天中的所有数据
                            for app_category_id, app_category in enumerate(data[1]):
                                appStayDuration = float(data[2][app_category_id])
                                if app_category in groupUsage:
                                    groupUsage[app_category] += appStayDuration
                                else:
                                    groupUsage[app_category] = appStayDuration
                        except Exception as e:
                            JLog.e("app_category_usage_in_diff_group_users",
                                   f"error: userName:{userName}, idx[{idx}], data:{data}, e:{e}")
                    if name_id <= int((userLen - 1) / 2):
                        groupType = "light"
                    else:
                        groupType = "heavy"
                    for category in allAppCategories:
                        if category in groupUsage:
                            allUserData.append([groupType, userName, category, groupUsage[category]])
                        else:
                            allUserData.append([groupType, userName, category, 0])
                bar()

            if allUserData:
                allUserData.insert(0, ["分组名", "用户名", "分组使用的app名",
                                       "分组在该App停留多长时间"])
                ExcelUtil.write_to_excel(allUserData, dirName,
                                         GRAPH_app_category_usage_in_diff_group_users)


app_category_usage_in_diff_group_users()
