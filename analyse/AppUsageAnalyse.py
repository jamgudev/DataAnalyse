import pandas as pd
from util import TimeUtils, ExcelUtil
import warnings
from pandas import DataFrame

from analyse.FilePathDefinition import CF_ACTIVITY_DIR, INPUT_FILE, EXPORT_APP_DETAIL_USAGES, EXCEL_SUFFIX, EXPORT_APP_SUMMARY_USAGES

warnings.filterwarnings('ignore')

# app_usage 格式
# com.xingin.xhs	com.xingin.xhs.index.v2.IndexActivityV2	20230602(18_37_04_105)	20230602(18_37_08_100)	00_00_03_995	3995

__app_name_idx = 0
__app_page_name_idx = 1
__app_page_start_time_idx = 2
__app_page_end_time_idx = 3
__app_page_duration_time_idx = 5
__power_time_idx = 0
__power_network_speed_idx = 12


__filter_screen_on = "Screen On"
__filter_screen_off = "Screen Off"
__filter_user_present = "User Present"
__filter_app_usage = "com."
__filter_session_summery = "Session Summarize"


# app在一个session内使用的详细记录，包括各个页面的使用详情
class AppDetailUsage:

    __detail_usage_app_name_idx = 0
    __detail_usage_page_name_idx = 1
    __detail_usage_page_start_time_idx = 2
    __detail_usage_page_duration_idx = 3
    __detail_usage_page_network_spent_idx = 4

    # app_name      包名
    # class_name    页面名
    # use_time      这个页面在一天中的什么时间被浏览
    # duration      在这个页面累计停留时间
    # network_spent 在这个页面消耗的流量
    def __init__(self,
                 app_name: str,
                 page_name: str,
                 start_time: str,
                 duration: int,
                 network_spent: float):
        self.app_name = app_name
        self.page_name = page_name
        self.start_time = start_time
        self.duration = duration
        self.network_spent = network_spent

    def to_excel_list(self) -> []:
        return [self.app_name, self.page_name, self.start_time, self.duration, self.network_spent]

    @staticmethod
    def from_list(detailUsageList: []):
        if len(detailUsageList) == 5:
            detailUsage = AppDetailUsage(detailUsageList[0], detailUsageList[1],
                                         detailUsageList[2], detailUsageList[3],
                                         detailUsageList[4])
            return detailUsage
        return None

    @staticmethod
    def excel_header() -> []:
        return ["包名", "页面名", "这个页面在一天中的什么时间被浏览", "在这个页面累计停留时间", "在这个页面消耗的流量"]


# app 在一个session内使用的概览
class AppSummeryUsage:

    # app_name                      应用包名
    # app_open_times                app累计打开次数
    # page_open_set                 累计打开的所有页面
    # page_stay_longest_name        停留最长时间的页面
    # page_stay_longest_duration    最长页面停留的时长
    # page_stay_shortest_name       停留最短时间的页面
    # page_stay_shortest_duration   最短页面停留的时长
    # page_stay_longest_network     停留最长时间的页面消耗的流量
    # page_stay_shortest_network    停留最短时间的页面消耗的流量
    # app_stay_duration             APP累计停留时间
    # app_network_spent             APP累计消耗的流量
    def __init__(self,
                 app_name: str,
                 app_open_times: int,
                 page_open_set: set,
                 page_stay_longest_name: str,
                 page_stay_longest_duration: int,
                 page_stay_shortest_name: str,
                 page_stay_shortest_duration: int,
                 page_stay_longest_network: float,
                 page_stay_shortest_network: float,
                 app_stay_duration: int,
                 app_network_spent: float):
        self.app_name = app_name
        self.app_open_times = app_open_times
        self.page_open_set = page_open_set
        self.page_stay_longest_name = page_stay_longest_name
        self.page_stay_longest_duration = page_stay_longest_duration
        self.page_stay_shortest_name = page_stay_shortest_name
        self.page_stay_shortest_duration = page_stay_shortest_duration
        self.page_stay_longest_network = page_stay_longest_network
        self.page_stay_shortest_network = page_stay_shortest_network
        self.app_stay_duration = app_stay_duration
        self.app_network_spent = app_network_spent

    def to_excel_list(self) -> []:
        return [self.app_name, self.app_open_times, len(self.page_open_set), self.page_stay_longest_name,
                self.page_stay_longest_duration, self.page_stay_shortest_name, self.page_stay_shortest_duration,
                self.page_stay_longest_network, self.page_stay_shortest_network, self.app_stay_duration,
                self.app_network_spent]

    @staticmethod
    def from_list(fromList: []):
        if len(fromList) == 11:
            appSummary = AppSummeryUsage(
                fromList[0], fromList[1], fromList[2],
                fromList[3], fromList[4], fromList[5],
                fromList[6], fromList[7], fromList[8],
                fromList[9], fromList[10]
            )
            return appSummary

        return None

    @staticmethod
    def excel_header() -> []:
        return ["应用包名", "app累计打开次数", "累计打开的所有页面", "停留最长时间的页面", "最长页面停留的时长",
                "停留最短时间的页面", "最短页面停留的时长", "停留最长时间的页面消耗的流量", "停留最短时间的页面消耗的流量",
                "APP累计停留时间", "APP累计消耗的流量"]

#
# class __SessionSummery:
#     def __init__(self,
#                  ):


def get_page_network_spent(powerData: DataFrame, pageStartTime: str, pageEndTime: str):
    powerDataRows = powerData.shape[0]
    networkSpent = 0
    for row in range(powerDataRows):
        time = powerData.iloc[row, __power_time_idx]
        networkSpeed = powerData.iloc[row, __power_network_speed_idx]
        if TimeUtils.compare_time(time, pageStartTime) >= 0:
            networkSpent += networkSpeed
        if TimeUtils.compare_time(time, pageEndTime) == 0:
            networkSpent += networkSpeed
            break

    return networkSpent


# 从app使用的详细记录里，总结出概括
def summarize_detail_usage(detailUsages: [], outputRootDir: str):
    if detailUsages:
        tempUsages = detailUsages.copy()
        appSummaryUsagesDict = {}
        lastAppName = ""
        for detailUsage in tempUsages:
            detailUsage = AppDetailUsage.from_list(detailUsage)
            appName = detailUsage.app_name
            networkSpent = detailUsage.network_spent
            pageName = detailUsage.page_name
            pageDuration = detailUsage.duration
            if appName in appSummaryUsagesDict:
                appSummaryUsage = appSummaryUsagesDict.get(appName)
                # 如果上一个打开的app不是这个app，说明又打开了一次
                if lastAppName != appName:
                    appSummaryUsage.app_open_times += 1
                # 累加流量消耗
                appSummaryUsage.app_network_spent += networkSpent
                # 累加app停留时间
                appSummaryUsage.app_stay_duration += pageDuration
                # 添加打开的页面
                appSummaryUsage.page_open_set.add(pageName)
                # 更新停留时长最久的页面及对应时间、流量消耗
                if appSummaryUsage.page_stay_longest_duration < pageDuration:
                    appSummaryUsage.page_stay_longest_duration = pageDuration
                    appSummaryUsage.page_stay_longest_name = pageName
                    appSummaryUsage.page_stay_longest_network = networkSpent
                # 更新停留时长最短的页面及对应时间、流量消耗
                if appSummaryUsage.page_stay_shortest_duration > pageDuration:
                    appSummaryUsage.page_stay_shortest_duration = pageDuration
                    appSummaryUsage.page_stay_shortest_name = pageName
                    appSummaryUsage.page_stay_shortest_network = networkSpent

            else:
                pageNameSet = set()
                pageNameSet.add(pageName)
                appSummaryUsage = AppSummeryUsage(appName, 1, pageNameSet,
                                                  pageName, pageDuration, pageName,
                                                  pageDuration, networkSpent, networkSpent,
                                                  pageDuration, networkSpent)
                appSummaryUsagesDict[appName] = appSummaryUsage

            lastAppName = appName

        # 输出summary_usage成excel
        if appSummaryUsagesDict:
            appSummaryUsages = []
            for summaryUsage in appSummaryUsagesDict.values():
                appSummaryUsages.append(summaryUsage.to_excel_list())

            if appSummaryUsages:
                toExcelData = appSummaryUsages.copy()
                toExcelData.insert(0, AppSummeryUsage.excel_header())
                exportAppSummaryUsagePath = outputRootDir + "/" + EXPORT_APP_SUMMARY_USAGES + EXCEL_SUFFIX
                ExcelUtil.write_to_excel(toExcelData, exportAppSummaryUsagePath)


def analyse(appUsageFilePath: str, powerDataFilePath: str, outputRootDir: str):
    appUsageData = pd.read_excel(appUsageFilePath, header=None)
    powerData = pd.read_excel(powerDataFilePath, header=None)

    appUsageRows = appUsageData.shape[0]
    lastAppName = ""
    lastAppClass = ""
    app_usage_summery = []
    appDetailUsages = []
    # app_usage_summery.append(["包名", "在这个app中打开了多少个页面", ""])
    appClassMap = {}
    appExportData = []
    for i in range(appUsageRows):
        lineHeader = appUsageData.iloc[i, 0]
        if __filter_app_usage in lineHeader:
            appName = appUsageData.iloc[i, __app_name_idx]
            appPage = appUsageData.iloc[i, __app_page_name_idx]
            startTime = appUsageData.iloc[i, __app_page_start_time_idx]
            endTime = appUsageData.iloc[i, __app_page_end_time_idx]
            pageDuration = appUsageData.iloc[i, __app_page_duration_time_idx]
            pageNetworkSpent = get_page_network_spent(powerData, startTime, endTime)
            appDetailUsage = AppDetailUsage(appName, appPage, startTime, pageDuration, pageNetworkSpent)
            appDetailUsages.append(appDetailUsage.to_excel_list())
        elif __filter_session_summery in lineHeader:
            break
        else:
            continue

    # 输出app_detail_usage到文件
    if appDetailUsages:
        toExcelData = appDetailUsages.copy()
        toExcelData.insert(0, AppDetailUsage.excel_header())
        exportAppDetailFilePath = outputRootDir + "/" + EXPORT_APP_DETAIL_USAGES + EXCEL_SUFFIX
        ExcelUtil.write_to_excel(toExcelData, exportAppDetailFilePath)

    # 得到app使用概括
    summarize_detail_usage(appDetailUsages, outputRootDir)
    # 还是同一个app
    # if lastAppName == appName:
    #     # 这个页面出现过
    #     if appPage in appClassMap:
    #         classUseCount = appClassMap[appName]
    #         appClassMap[appPage] = classUseCount + 1
    #         appDetailUsages[appPage]


USER_NAME = "./" + INPUT_FILE + "/13266826670_三星"
activeRootPath = USER_NAME + "/" + CF_ACTIVITY_DIR
appUsageFile = activeRootPath + "/20230405/20230405(17_34_11_713)$$20230405(17_34_51_612)/session_app_usage_39899.xlsx"
longAppUsageFile = activeRootPath + "/20230405/20230405(19_14_11_149)$$20230405(19_43_10_373)/session_app_usage_1739224.xlsx"

outputDir = "./output/13266826670_三星/" + CF_ACTIVITY_DIR + "/20230405/20230405(17_34_11_713)$$20230405(17_34_51_612)"
powerFile = outputDir + "/session_power_usage_20230405(17_34_11).xlsx"
longPowerFile = "./output/13266826670_三星/" + CF_ACTIVITY_DIR +\
                "/20230405/20230405(19_14_11_149)$$20230405(19_43_10_373)/session_power_usage_20230405(19_22_11).xlsx"
# analyse(appUsageFile, powerFile, outputDir)
analyse(longAppUsageFile, longPowerFile, outputDir)
