import pandas as pd
from util import TimeUtils
import warnings
from pandas import DataFrame

from analyse.FilePathDefinition import CF_ACTIVITY_DIR, INPUT_FILE, EXPORT_APP_DETAIL_USAGES, EXCEL_SUFFIX

warnings.filterwarnings('ignore')

# app_usage 格式
# com.xingin.xhs	com.xingin.xhs.index.v2.IndexActivityV2	20230602(18_37_04_105)	20230602(18_37_08_100)	00_00_03_995	3995

__app_name_idx = 0
__app_class_name_idx = 1
__app_class_start_time_idx = 2
__app_class_end_time_idx = 3
__app_class_duration_time_idx = 5
__power_time_idx = 0
__power_network_speed_idx = 12


__filter_screen_on = "Screen On"
__filter_screen_off = "Screen Off"
__filter_user_present = "User Present"
__filter_app_usage = "com."
__filter_session_summery = "Session Summarize"


# app在一个session内使用的详细记录，包括各个页面的使用详情
class __AppDetailUsage:

    # app_name      包名
    # class_name    页面名
    # use_time      这个页面在一天中的什么时间被浏览
    # duration      在这个页面累计停留时间
    # network_spent 在这个页面消耗的流量
    def __init__(self,
                 app_name: str,
                 page_name: str,
                 start_time: str,
                 duration: str,
                 network_spent: float):
        self.app_name = app_name
        self.page_name = page_name
        self.start_time = start_time
        self.duration = duration
        self.network_spent = network_spent

    def to_excel_list(self) -> []:
        return [self.app_name, self.page_name, self.start_time, self.duration, self.network_spent]


# app 在一个session内使用的概览
class __AppSummeryUsage:

    # app_name                      应用包名
    # app_open_times                app累计打开次数
    # page_open_num                 不同的页面累计打开了多少个
    # page_stay_longest             停留最长时间的页面
    # page_stay_longest_time        最长页面停留的时长
    # page_stay_shortest            停留最短时间的页面
    # page_stay_shortest_time       最短页面停留的时长
    # page_stay_longest_network     停留最长时间的页面消耗的流量
    # page_stay_shortest_network    停留最短时间的页面消耗的流量
    # app_stay_duration             APP累计停留时间
    # app_network_spent             APP累计消耗的流量
    def __init__(self,
                 app_name: str,
                 app_open_times: int,
                 page_open_num: int,
                 page_stay_longest: str,
                 page_stay_longest_time: int,
                 page_stay_shortest: str,
                 page_stay_shortest_time: int,
                 page_stay_longest_network: float,
                 page_stay_shortest_network: float,
                 app_stay_duration: int,
                 app_network_spent: float):
        self.app_name = app_name
        self.app_open_times = app_open_times
        self.page_open_num = page_open_num
        self.page_stay_longest = page_stay_longest
        self.page_stay_longest_time = page_stay_longest_time
        self.page_stay_shortest = page_stay_shortest
        self.page_stay_shortest_time = page_stay_shortest_time
        self.page_stay_longest_network = page_stay_longest_network
        self.page_stay_shortest_network = page_stay_shortest_network
        self.app_stay_duration = app_stay_duration
        self.app_network_spent = app_network_spent

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
            appPage = appUsageData.iloc[i, __app_class_name_idx]
            startTime = appUsageData.iloc[i, __app_class_start_time_idx]
            endTime = appUsageData.iloc[i, __app_class_end_time_idx]
            pageDuration = appUsageData.iloc[i, __app_class_duration_time_idx]
            pageNetworkSpent = get_page_network_spent(powerData, startTime, endTime)
            appDetailUsage = __AppDetailUsage(appName, appPage, startTime, pageDuration, pageNetworkSpent)
            appDetailUsages.append(appDetailUsage.to_excel_list())
        elif __filter_session_summery in lineHeader:
            break
        else:
            continue

    # 输出app_detail_usage到文件
    if appDetailUsages:
        exportAppDetailFilePath = outputRootDir + "/" + EXPORT_APP_DETAIL_USAGES + EXCEL_SUFFIX
        detailUsageDF = pd.DataFrame(appDetailUsages)
        detailUsageDF.to_excel(exportAppDetailFilePath, header=None, index=None)

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

outputDir = "./output/13266826670_三星/" + CF_ACTIVITY_DIR + "/20230405/20230405(17_34_11_713)$$20230405(17_34_51_612)"
powerFile = outputDir + "/session_power_usage_20230405(17_34_11).xlsx"
analyse(appUsageFile, powerFile, outputDir)