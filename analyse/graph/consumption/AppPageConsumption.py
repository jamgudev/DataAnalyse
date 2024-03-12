from alive_progress import alive_bar

from analyse.graph.GrapgNameSapce import AD_APP_PKG_NAME, AD_APP_PAGE_NAME, AD_APP_TOTAL_CONSUMPTION, GRAPH_app_page_consumption, AD_APP_DURATION
from analyse.graph.application.AppCategory import get_app_category_dict, get_app_category
from analyse.graph.base.__EveryDayAnalyseFromOutput import iter_idx_data_from_file_in_every_day
from analyse.init_analyse.power_params import PowerParamsUtil
from analyse.util.AnalyseUtils import get_all_user_name_from_dir
from analyse.util.FilePathDefinition import EXCEL_SUFFIX, EXPORT_APP_DETAIL_USAGES, TEST_OUTPUT_FILE
from util import JLog, ExcelUtil


# 所有用户使用的所有app里，不同app page占该app的功耗比重
def app_page_consumption():
    dirName = TEST_OUTPUT_FILE
    allUserName = get_all_user_name_from_dir(dirName)
    if allUserName:
        allUserData = []
        brandData = {}
        with alive_bar(len(allUserName), ctrl_c=True, force_tty=True, title=f'分析进度') as bar:
            allAppCategoriesDict = get_app_category_dict(dirName)
            for userName in allUserName:
                brand = PowerParamsUtil.get_phone_brand_by_user_name(userName)
                if brand == "":
                    bar()
                    continue

                pageConsumptionUsages = {}
                pageDurations = {}
                userTotalConsumption = 0.0
                userTotalDuration = 0.0
                dataOfEveryDay = iter_idx_data_from_file_in_every_day(dirName, userName,
                                                                      EXPORT_APP_DETAIL_USAGES + EXCEL_SUFFIX,
                                                                      [AD_APP_PKG_NAME, AD_APP_PAGE_NAME,
                                                                       AD_APP_DURATION,
                                                                       AD_APP_TOTAL_CONSUMPTION])
                if isinstance(dataOfEveryDay, dict):
                    # 遍历每天数据
                    for idx, data in enumerate(dataOfEveryDay.values()):
                        try:
                            # 遍历一天中的所有数据
                            for app_usage_idx, app_pkg_name in enumerate(data[0]):
                                appPageName = data[1][app_usage_idx]
                                pageDuration = float(data[2][app_usage_idx])
                                pageConsumption = float(data[3][app_usage_idx])

                                pageCombined = app_pkg_name + "$$" + appPageName
                                if pageCombined not in pageDurations:
                                    pageDurations[pageCombined] = 0.0
                                pageDurations[pageCombined] += pageDuration

                                if pageCombined not in pageConsumptionUsages:
                                    pageConsumptionUsages[pageCombined] = 0.0
                                pageConsumptionUsages[pageCombined] += pageConsumption
                                userTotalConsumption += pageConsumption
                                userTotalDuration += pageDuration
                        except Exception as e:
                            JLog.e("app_page_consumption",
                                   f"error: userName:{userName}, idx[{idx}], data:{data}, e:{e}")

                    userData = []
                    for combinedPageName in pageDurations:
                        parts = combinedPageName.split("$$")
                        appPkgName = parts[0]
                        pageName = parts[1]
                        appCategory = get_app_category("", appPkgName, allAppCategoriesDict)
                        # in min
                        pageTotalDuration = pageDurations[combinedPageName] / 60
                        pageTotalConsumption = pageConsumptionUsages[combinedPageName]
                        pageConsumptionRate = pageTotalConsumption / userTotalConsumption
                        pageConsumptionRatePerMin = pageConsumptionRate / pageTotalDuration
                        userData.append([brand, appCategory, appPkgName, pageName, pageTotalDuration,
                                         pageTotalDuration * 60 / userTotalDuration,
                                         pageConsumptionRate, pageConsumptionRatePerMin])

                    if brand in brandData:
                        usersData = brandData[brand]
                    else:
                        usersData = {}
                    usersData[userName] = userData
                    brandData[brand] = usersData
                bar()

            user_idx = 1
            for brand in brandData:
                usersData = brandData[brand]
                for user_name in usersData.keys():
                    for user_data in usersData[user_name]:
                        allUserData.append([str(user_idx), user_name] + user_data[:])
                    user_idx += 1

            allUserData.insert(0, ["用户名", "手机号", "手机型号", "app类别", "app名", "app页面名", "页面停留时长(分钟)",
                                   "页面停留时长占比(%)", "页面消耗的能耗百分比", "每分钟能耗百分比"])
            ExcelUtil.write_to_excel(allUserData, dirName,
                                     GRAPH_app_page_consumption)


app_page_consumption()
