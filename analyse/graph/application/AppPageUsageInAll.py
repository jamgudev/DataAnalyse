from alive_progress import alive_bar

from analyse.graph.GrapgNameSapce import AS_APP_NAME, AS_APP_DURATION, GRAPH_app_usage_in_all_users, AD_APP_PAGE_NAME, AD_APP_DURATION, \
    AD_APP_PKG_NAME, GRAPH_app_categories, GRAPH_app_page_usage_in_sns, AD_APP_START_TIME, GRAPH_app_page_usage_in_all
from analyse.graph.application import AppCategory
from analyse.graph.base.__EveryDayAnalyseFromOutput import iter_idx_data_from_file_in_every_day
from analyse.util.AnalyseUtils import get_all_user_name_from_dir
from analyse.util.FilePathDefinition import EXCEL_SUFFIX, TEST_OUTPUT_FILE, EXPORT_APP_DETAIL_USAGES, OUTPUT_FILE
from util import JLog, ExcelUtil

# 依赖test/output/app_categories文件，执行前需保证这个文件存在，执行AppUsageInAllUsers会生成。


# 所有用户，在各个app使用的时间占用户各自总使用时间的占比
def app_page_usage_in_all():
    dirName = TEST_OUTPUT_FILE
    allUserName = get_all_user_name_from_dir(dirName)
    if allUserName:
        appCategoryDict = AppCategory.get_app_category_dict(dirName)
        allUserData = []
        appPageUsages = {}
        with alive_bar(len(allUserName), ctrl_c=True, force_tty=True, title=f'分析进度') as bar:
            for userName in allUserName:
                dataOfEveryDay = iter_idx_data_from_file_in_every_day(dirName, userName,
                                                                      EXPORT_APP_DETAIL_USAGES + EXCEL_SUFFIX,
                                                                      [AD_APP_PKG_NAME, AD_APP_PAGE_NAME,
                                                                       AD_APP_DURATION])
                if isinstance(dataOfEveryDay, dict):
                    # 遍历每天数据
                    for idx, data in enumerate(dataOfEveryDay.values()):
                        try:
                            # 遍历一天中的所有数据
                            for pkg_idx, pkg_name in enumerate(data[0]):
                                appPageName = data[1][pkg_idx]
                                appPageDuration = float(data[2][pkg_idx])
                                if appPageDuration <= 0:
                                    continue
                                # 找到app对应的snsPages
                                if pkg_name in appPageUsages:
                                    appPages = appPageUsages[pkg_name]
                                else:
                                    appPages = {}
                                    appPageUsages[pkg_name] = appPages
                                if appPageName in appPages:
                                    appPages[appPageName] += appPageDuration
                                else:
                                    appPages[appPageName] = appPageDuration
                        except Exception as e:
                            JLog.e("app_page_usage_in_all",
                                   f"error: userName:{userName}, idx[{idx}], data:{data}, e:{e}")
                bar()
            for pkgName in appPageUsages.keys():
                appPageUsage = appPageUsages[pkgName]
                for pageName in appPageUsage.keys():
                    pageDuration = appPageUsage[pageName]
                    category = AppCategory.get_app_category(dirName, pkgName, appCategoryDict)
                    allUserData.append([category, pkgName, pageName, pageDuration])
            allUserData.insert(0, ["app类别", "app包名", "app Page名",
                                   "app page duration"])
            ExcelUtil.write_to_excel(allUserData, dirName,
                                     GRAPH_app_page_usage_in_all)


app_page_usage_in_all()

