import pandas as pd
from util import TimeUtils, ExcelUtil
import warnings
from pandas import DataFrame

from analyse.FilePathDefinition import CF_ACTIVITY_DIR, INPUT_FILE, EXPORT_APP_DETAIL_USAGES, EXCEL_SUFFIX, EXPORT_APP_SUMMARY_USAGES, \
    EXPORT_SESSION_SUMMARY

warnings.filterwarnings('ignore')

# app_usage 格式
# com.xingin.xhs	com.xingin.xhs.index.v2.IndexActivityV2	20230602(18_37_04_105)	20230602(18_37_08_100)	00_00_03_995	3995

__screen_on_time_idx = 1
__app_name_idx = 0
__app_page_name_idx = 1
__app_page_start_time_idx = 2
__app_page_end_time_idx = 3
__app_page_duration_time_idx = 5
__power_time_idx = 0
__power_network_speed_idx = 12
__session_total_duration_idx = 4


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

    # @staticmethod
    # def from_list(fromList: []):
    #     if len(fromList) == 11:
    #         appSummary = AppSummeryUsage(
    #             fromList[0], fromList[1], fromList[2],
    #             fromList[3], fromList[4], fromList[5],
    #             fromList[6], fromList[7], fromList[8],
    #             fromList[9], fromList[10]
    #         )
    #         return appSummary
    #
    #     return None

    @staticmethod
    def excel_header() -> []:
        return ["应用包名", "app累计打开次数", "累计打开的所有页面", "停留最长时间的页面", "最长页面停留的时长",
                "停留最短时间的页面", "最短页面停留的时长", "停留最长时间的页面消耗的流量", "停留最短时间的页面消耗的流量",
                "APP累计停留时间", "APP累计消耗的流量"]


class SessionSummery:
    # app_open_set                      session期间不同App打开数量
    # app_page_open_set                 session期间不同页面打开数量
    # session_start_time                session开始时间
    # session_duration                  session持续时间
    # session_network_spent             session期间使用了多少流量
    # app_open_most_frequently_name     app被打开最多次的名称
    # app_open_most_frequently_times    同个app被打开最多的次数
    # app_open_least_frequently_name    app被打开最少次的名称
    # app_open_least_frequently_times   同个app被打开最少的次数
    # app_stay_longest_name             session期间使用最久的App名
    # app_stay_longest_duration         session期间在某个APP停留的最长时间
    # app_stay_shortest_name            session期间使用时间最短的App名
    # app_stay_shortest_duration        session期间在某个APP停留的最短时间
    # app_stay_longest_network          使用最久的APP所消耗的流量
    # app_stay_shortest_network         使用最短的APP所消耗的流量
    def __init__(self,
                 app_open_set: set,
                 app_page_open_set: set,
                 session_start_time: str,
                 session_duration: int,
                 session_network_spent: float,
                 app_open_most_frequently_name: str,
                 app_open_most_frequently_times: int,
                 app_open_least_frequently_name: str,
                 app_open_least_frequently_times: int,
                 app_stay_longest_name: str,
                 app_stay_longest_duration: int,
                 app_stay_shortest_name: str,
                 app_stay_shortest_duration: int,
                 app_stay_longest_network: float,
                 app_stay_shortest_network: float):
        self.app_open_set = app_open_set
        self.app_page_open_set = app_page_open_set
        self.session_start_time = session_start_time
        self.session_duration = session_duration
        self.session_network_spent = session_network_spent
        self.app_open_most_frequently_name = app_open_most_frequently_name
        self.app_open_most_frequently_times = app_open_most_frequently_times
        self.app_open_least_frequently_name = app_open_least_frequently_name
        self.app_open_least_frequently_times = app_open_least_frequently_times
        self.app_stay_longest_name = app_stay_longest_name
        self.app_stay_longest_duration = app_stay_longest_duration
        self.app_stay_shortest_name = app_stay_shortest_name
        self.app_stay_shortest_duration = app_stay_shortest_duration
        self.app_stay_longest_network = app_stay_longest_network
        self.app_stay_shortest_network = app_stay_shortest_network

    def to_excel_list(self) -> []:
        return [len(self.app_open_set), len(self.app_page_open_set), self.session_start_time, self.session_duration,
                self.session_network_spent, self.app_open_most_frequently_name, self.app_open_most_frequently_times,
                self.app_open_least_frequently_name, self.app_open_least_frequently_times, self.app_stay_longest_name,
                self.app_stay_longest_duration, self.app_stay_shortest_name, self.app_stay_shortest_duration,
                self.app_stay_longest_network, self.app_stay_shortest_network]

    @staticmethod
    def excel_header() -> []:
        return ["session期间不同App打开数量", "session期间不同页面打开数量", "session开始时间", "session持续时间",
                "session期间使用了多少流量", "app被打开最多次的名称", "同个app被打开最多的次数", "app被打开最少次的名称",
                "同个app被打开最少的次数", "session期间使用最久的App名", "session期间在某个APP停留的最长时间",
                "session期间使用时间最短的App名", "session期间在某个APP停留的最短时间", "使用最久的APP所消耗的流量",
                "使用最短的APP所消耗的流量"]

    # @staticmethod
    # def from_list(fromList: []):
    #     if len(fromList) == 14:
    #         summaryUsage = SessionSummery(
    #             fromList[0], fromList[1], fromList[2], fromList[3],
    #             fromList[4], fromList[5], fromList[6], fromList[7],
    #             fromList[8], fromList[9], fromList[10], fromList[11],
    #             fromList[12], fromList[13], fromList[14])
    #         return summaryUsage


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
def __summarize_detail_usage(detailUsages: [], outputRootDir: str) -> []:
    if detailUsages:
        tempUsages = detailUsages.copy()
        appSummaryUsagesDict = {}
        lastAppName = ""
        for detailUsage in tempUsages:
            # detailUsage = AppDetailUsage.from_list(detailUsage)
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

            return appSummaryUsagesDict.values()


def __analyse_app_detail_usage(appUsageData: DataFrame, powerData: DataFrame, outputRootDir: str) -> []:
    appUsageRows = appUsageData.shape[0]

    appDetailUsages = []
    outAppDetailUsages = []
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
            outAppDetailUsages.append(appDetailUsage)
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

    return outAppDetailUsages


# 解析Session概括
def __analyse_session_usage(summaryUsages: [], startTime: str, sessionDuration: int, outputRootDir: str):
    if summaryUsages:
        tempSummaryUsages = list(summaryUsages)
        appOpenSet = set()
        appPageOpenSet = set()
        sessionNetworkSpent = 0
        appOpenMostFrequentlyName = ""
        appOpenMostFrequentlyTimes = 0
        appOpenLessFrequentlyName = ""
        appOpenLessFrequentlyTimes = 0
        appStayLongestName = ""
        appStayLongestDuration = 0
        appStayShortestName = ""
        appStayShortestDuration = 0
        appStayLongestNetworkSpent = 0.0
        appStayShortestNetworkSpent = 0.0
        for summaryUsage in tempSummaryUsages:
            appName = summaryUsage.app_name
            pageOpenSet = summaryUsage.page_open_set
            appNetWorkSpent = summaryUsage.app_network_spent
            openTimes = summaryUsage.app_open_times
            stayDuration = summaryUsage.app_stay_duration

            appOpenSet.add(appName)
            # TODO bugfix pageOpenSet返回为空
            appPageOpenSet.union(pageOpenSet)
            sessionNetworkSpent += appNetWorkSpent
            if appOpenMostFrequentlyTimes < openTimes:
                appOpenMostFrequentlyName = appName
                appOpenMostFrequentlyTimes = openTimes
            if appOpenLessFrequentlyTimes > openTimes:
                appOpenLessFrequentlyName = appName
                appOpenLessFrequentlyTimes = openTimes
            if appStayLongestDuration < stayDuration:
                appStayLongestName = appName
                appStayLongestNetworkSpent = appNetWorkSpent
                appStayLongestDuration = stayDuration
            if appStayShortestDuration > stayDuration:
                appStayShortestName = appName
                appStayShortestDuration = stayDuration
                appStayShortestNetworkSpent = appNetWorkSpent

        sessionUsage = SessionSummery(appOpenSet, appPageOpenSet, startTime, sessionDuration, sessionNetworkSpent,
                                      appOpenMostFrequentlyName, appOpenMostFrequentlyTimes, appOpenLessFrequentlyName,
                                      appOpenLessFrequentlyTimes, appStayLongestName, appStayLongestDuration,
                                      appStayShortestName, appStayShortestDuration, appStayLongestNetworkSpent,
                                      appStayShortestNetworkSpent)
        toExcelData = [sessionUsage.to_excel_list()]
        toExcelData.insert(0, SessionSummery.excel_header())
        exportSessionSummaryPath = outputRootDir + "/" + EXPORT_SESSION_SUMMARY + EXCEL_SUFFIX
        ExcelUtil.write_to_excel(toExcelData, exportSessionSummaryPath)


def analyse(appUsageFilePath: str, powerDataFilePath: str, outputRootDir: str):
    appUsageData = pd.read_excel(appUsageFilePath, header=None)
    powerData = pd.read_excel(powerDataFilePath, header=None)

    # 解析App使用详细数据
    appDetailUsages = __analyse_app_detail_usage(appUsageData, powerData, outputRootDir)

    # 得到app使用概括
    summaryUsages = __summarize_detail_usage(appDetailUsages, outputRootDir)

    # 解析Session使用概括
    startTime = appUsageData.iloc[0, __screen_on_time_idx]
    appUsageDataRows = appUsageData.shape[0]
    sessionDuration = appUsageData.iloc[appUsageDataRows - 1, __session_total_duration_idx]
    __analyse_session_usage(summaryUsages, startTime, sessionDuration, outputRootDir)

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
powerFile = outputDir + "/session_power_usage.xlsx"

longOutputDir = "./output/13266826670_三星/" + CF_ACTIVITY_DIR + "/20230405/20230405(19_14_11_149)$$20230405(19_43_10_373)"
longPowerFile = longOutputDir + "/session_power_usage.xlsx"
# analyse(appUsageFile, powerFile, outputDir)
analyse(longAppUsageFile, longPowerFile, longOutputDir)
