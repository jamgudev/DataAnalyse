from alive_progress import alive_bar

from analyse.graph.GrapgNameSapce import AS_APP_NAME, AS_UNIT_CS_TOTAL, AS_APP_CATEGORY, \
    GRAPH_app_category_consumption
from analyse.graph.application.AppCategory import get_all_app_categories
from analyse.graph.base.__EveryDayAnalyseFromOutput import iter_idx_data_from_file_in_every_day
from analyse.util.AnalyseUtils import get_all_user_name_from_dir
from analyse.util.FilePathDefinition import EXCEL_SUFFIX, OUTPUT_FILE, EXPORT_APP_SUMMARY_USAGES
from util import JLog, ExcelUtil


# 所有用户，在各个app使用的时间占用户各自总使用时间的占比
def app_category_consumption():
    dirName = OUTPUT_FILE
    allUserName = get_all_user_name_from_dir(dirName)
    if allUserName:
        allUserData = []
        with alive_bar(len(allUserName), ctrl_c=True, force_tty=True, title=f'分析进度') as bar:
            allAppCategories = get_all_app_categories(dirName)
            for userName in allUserName:
                unitsUsages = {}
                totalConsumption = 0.0
                dataOfEveryDay = iter_idx_data_from_file_in_every_day(dirName, userName,
                                                                      EXPORT_APP_SUMMARY_USAGES + EXCEL_SUFFIX,
                                                                      [AS_APP_NAME, AS_APP_CATEGORY,
                                                                       AS_UNIT_CS_TOTAL])
                if isinstance(dataOfEveryDay, dict):
                    # 遍历每天数据
                    for idx, data in enumerate(dataOfEveryDay.values()):
                        try:
                            # 遍历一天中的所有数据
                            for app_usage_idx, app_usage_name in enumerate(data[0]):
                                category = data[1][app_usage_idx]
                                categoryConsumption = float(data[2][app_usage_idx])
                                if category not in unitsUsages:
                                    unitsUsages[category] = 0.0
                                unitsUsages[category] += categoryConsumption
                                totalConsumption += categoryConsumption
                        except Exception as e:
                            JLog.e("mean_active_time_per_day_with_std_of_every_user_pure",
                                   f"error: userName:{userName}, idx[{idx}], data:{data}, e:{e}")
                    for ctg in allAppCategories:
                        if ctg in unitsUsages:
                            allUserData.append([userName, ctg, unitsUsages[ctg], unitsUsages[ctg] / totalConsumption])
                        else:
                            allUserData.append([userName, ctg, 0.0, 0.0])
                bar()
            allUserData.insert(0, ["用户名", "app类别", "消耗的功耗", "功耗占比"])
            ExcelUtil.write_to_excel(allUserData, dirName,
                                     GRAPH_app_category_consumption)


app_category_consumption()
