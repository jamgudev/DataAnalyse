from alive_progress import alive_bar

from analyse.graph.GrapgNameSapce import AS_APP_NAME, AS_UNIT_CS_TOTAL, AS_APP_CATEGORY, \
    GRAPH_app_category_consumption, AD_APP_PKG_NAME, AD_APP_PAGE_NAME, AD_APP_TOTAL_CONSUMPTION, GRAPH_app_page_consumption
from analyse.graph.base.__EveryDayAnalyseFromOutput import iter_idx_data_from_file_in_every_day
from analyse.util.AnalyseUtils import get_all_user_name_from_dir
from analyse.util.FilePathDefinition import EXCEL_SUFFIX, OUTPUT_FILE, EXPORT_APP_DETAIL_USAGES
from util import JLog, ExcelUtil


# 所有用户，在各个app使用的时间占用户各自总使用时间的占比
def app_page_consumption():
    dirName = OUTPUT_FILE
    allUserName = get_all_user_name_from_dir(dirName)
    if allUserName:
        allUserData = []
        pageConsumptions = {}
        appTotalConsumptions = {}
        with alive_bar(len(allUserName), ctrl_c=True, force_tty=True, title=f'分析进度') as bar:
            for userName in allUserName:
                dataOfEveryDay = iter_idx_data_from_file_in_every_day(dirName, userName,
                                                                      EXPORT_APP_DETAIL_USAGES + EXCEL_SUFFIX,
                                                                      [AD_APP_PKG_NAME, AD_APP_PAGE_NAME,
                                                                       AD_APP_TOTAL_CONSUMPTION])
                if isinstance(dataOfEveryDay, dict):
                    # 遍历每天数据
                    for idx, data in enumerate(dataOfEveryDay.values()):
                        try:
                            # 遍历一天中的所有数据
                            for app_usage_idx, app_pkg_name in enumerate(data[0]):
                                appPageName = data[1][app_usage_idx]
                                pageConsumption = float(data[2][app_usage_idx])
                                # 找到app对应的snsPages
                                if app_pkg_name in pageConsumptions:
                                    appPages = pageConsumptions[app_pkg_name]
                                else:
                                    appPages = {}
                                    pageConsumptions[app_pkg_name] = appPages
                                if appPageName in appPages:
                                    appPages[appPageName] += pageConsumption
                                else:
                                    appPages[appPageName] = pageConsumption

                                if app_pkg_name not in appTotalConsumptions:
                                    appTotalConsumptions[app_pkg_name] = pageConsumption
                                else:
                                    appTotalConsumptions[app_pkg_name] += pageConsumption
                        except Exception as e:
                            JLog.e("mean_active_time_per_day_with_std_of_every_user_pure",
                                   f"error: userName:{userName}, idx[{idx}], data:{data}, e:{e}")
                bar()
            for pkgName in pageConsumptions.keys():
                appPageConsumption = pageConsumptions[pkgName]
                for pageName in appPageConsumption.keys():
                    pageConsumption = appPageConsumption[pageName]
                    allUserData.append([pkgName, pageName, pageConsumption / appTotalConsumptions[pkgName]])
            allUserData.insert(0, ["app包名", "app页面名", "app page消耗占app总消耗的比重"])
            ExcelUtil.write_to_excel(allUserData, dirName,
                                     GRAPH_app_page_consumption)


app_page_consumption()
