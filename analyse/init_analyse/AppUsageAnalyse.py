import math
import os.path
import re
import warnings

import pandas as pd
from pandas import DataFrame

from analyse.graph.application import AppCategory
from analyse.util.FilePathDefinition import EXPORT_APP_DETAIL_USAGES, EXCEL_SUFFIX, EXPORT_APP_SUMMARY_USAGES, \
    EXPORT_SESSION_SUMMARY, PP_HEADERS, PP_SUMMARY_HEADERS
from util import TimeUtils, ExcelUtil, JLog, StringUtil

warnings.filterwarnings('ignore')

# app_usage 格式
# com.xingin.xhs	com.xingin.xhs.index.v2.IndexActivityV2	20230602(18_37_04_105)	20230602(18_37_08_100)	00_00_03_995	3995

__TAG = "AppUsageAnalyse"
__screen_on_time_idx = 1
__app_name_idx = 0
__app_page_name_idx = 1
__app_page_start_time_idx = 2
__app_page_end_time_idx = 3
__app_page_duration_time_idx = 5
__power_time_idx = 0
__power_network_speed_idx = 12
__session_for_search_row = "Session"
__session_total_duration_idx = 4

__filter_screen_on = "Screen On"
__filter_screen_off = "Screen Off"
__filter_user_present = "User Present"
__filter_app_usage_pattern = r'^[a-zA-Z][a-zA-Z0-9_]*(\.[a-zA-Z][a-zA-Z0-9_]*)*$'
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
    def __init__(self,
                 app_name: str,
                 category: str,
                 page_name: str,
                 start_time: str,
                 duration: int,
                 network_spent: float):
        self.app_name = app_name
        self.category = category
        self.page_name = page_name
        self.start_time = start_time
        self.duration = duration
        self.network_spent = network_spent
        self.units_base = 0.0
        self.units_screen_brightness = 0.0
        self.units_music_on = 0.0
        self.units_phone_ring = 0.0
        self.units_phone_off_hook = 0.0
        self.units_wifi_network = 0.0
        self.units_2g_network = 0.0
        self.units_3g_network = 0.0
        self.units_4g_network = 0.0
        self.units_5g_network = 0.0
        self.units_other_network = 0.0
        self.units_is_wifi_enable = 0.0
        self.units_network_speed = 0.0
        self.units_bluetooth = 0.0
        self.units_cpu0 = 0.0
        self.units_cpu1 = 0.0
        self.units_cpu2 = 0.0
        self.units_cpu3 = 0.0
        self.units_cpu4 = 0.0
        self.units_cpu5 = 0.0
        self.units_cpu6 = 0.0
        self.units_cpu7 = 0.0
        self.units_mem_available = 0.0
        self.units_mem_active = 0.0
        self.units_mem_dirty = 0.0
        self.units_mem_anonPages = 0.0
        self.units_mem_mapped = 0.0
        self.total_power_consumption = 0.0
        self.all_units_power = []
    # network_spent 在这个页面消耗的流量

    def to_excel_list(self) -> []:
        return [self.app_name, self.category, self.page_name, self.start_time, self.duration, self.network_spent,
                self.units_base, self.units_screen_brightness, self.units_music_on, self.units_phone_ring,
                self.units_phone_off_hook, self.units_wifi_network, self.units_2g_network, self.units_3g_network,
                self.units_4g_network, self.units_5g_network, self.units_other_network, self.units_is_wifi_enable,
                self.units_network_speed,
                self.units_bluetooth,
                self.units_cpu0, self.units_cpu1, self.units_cpu2,
                self.units_cpu3, self.units_cpu4, self.units_cpu5, self.units_cpu6, self.units_cpu7,
                self.units_mem_available,
                self.units_mem_active,
                self.units_mem_dirty,
                self.units_mem_anonPages,
                self.units_mem_mapped,
                self.total_power_consumption]

    @staticmethod
    def excel_header() -> []:
        unit_headers = PP_HEADERS[1:len(PP_HEADERS)]
        app_usages_headers = ["包名", "类名", "页面名", "这个页面在一天中的什么时间被浏览", "在这个页面累计停留时间", "在这个页面消耗的流量"]
        app_usages_headers.extend(unit_headers)
        return app_usages_headers

    def add_unit_pw(self, unit_pws: []):
        if len(unit_pws) < 23:
            JLog.i("AppDetailUsage", f"add_unit_pw failed: list [unit_pw] len {len(unit_pws)} less than 23, skipped.")
            return
        # 跳过第一个，是时间戳
        self.units_base = unit_pws[1]
        self.units_screen_brightness = unit_pws[2]
        self.units_music_on = unit_pws[3]
        self.units_phone_ring = unit_pws[4]
        self.units_phone_off_hook = unit_pws[5]
        self.units_wifi_network = unit_pws[6]
        self.units_2g_network = unit_pws[7]
        self.units_3g_network = unit_pws[8]
        self.units_4g_network = unit_pws[9]
        self.units_5g_network = unit_pws[10]
        self.units_other_network = unit_pws[11]
        self.units_is_wifi_enable = unit_pws[12]
        self.units_network_speed = unit_pws[13]
        self.units_bluetooth = 0.0
        self.units_cpu0 = unit_pws[15]
        self.units_cpu1 = unit_pws[16]
        self.units_cpu2 = unit_pws[17]
        self.units_cpu3 = unit_pws[18]
        self.units_cpu4 = unit_pws[19]
        self.units_cpu5 = unit_pws[20]
        self.units_cpu6 = unit_pws[21]
        self.units_cpu7 = unit_pws[22]
        self.units_mem_available = unit_pws[23]
        self.units_mem_active = unit_pws[24]
        self.units_mem_dirty = unit_pws[25]
        self.units_mem_anonPages = unit_pws[26]
        self.units_mem_mapped = unit_pws[27]
        self.total_power_consumption += unit_pws[28]
        self.all_units_power = unit_pws


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
                 app_category: str,
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
        self.app_category = app_category
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
        self.units_base = 0.0
        self.units_screen_brightness = 0.0
        self.units_media = 0.0
        self.units_network = 0.0
        self.units_bluetooth = 0.0
        self.units_cpu = 0.0
        # self.units_mem_available = 0.0
        self.units_mem = 0.0
        self.total_power_consumption = 0.0
        self.all_units_power = []

    def to_excel_list(self) -> []:
        return [self.app_name, self.app_category, self.app_open_times, len(self.page_open_set), self.page_stay_longest_name,
                self.page_stay_longest_duration, self.page_stay_shortest_name, self.page_stay_shortest_duration,
                self.page_stay_longest_network, self.page_stay_shortest_network, self.app_stay_duration,
                self.app_network_spent, self.units_base, self.units_screen_brightness, self.units_media,
                self.units_network, self.units_bluetooth, self.units_cpu, self.units_mem,
                self.total_power_consumption]

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
        unit_headers = PP_SUMMARY_HEADERS[1:len(PP_SUMMARY_HEADERS)]
        app_summary_headers = ["应用包名", "应用类名", "app累计打开次数", "累计打开的所有页面", "停留最长时间的页面", "最长页面停留的时长",
                               "停留最短时间的页面", "最短页面停留的时长", "停留最长时间的页面消耗的流量", "停留最短时间的页面消耗的流量",
                               "APP累计停留时间", "APP累计消耗的流量"]
        app_summary_headers.extend(unit_headers)
        return app_summary_headers

    def add_up_units_power(self, detailUsage: AppDetailUsage):
        self.units_base += detailUsage.units_base
        self.units_screen_brightness += detailUsage.units_screen_brightness
        self.units_media += detailUsage.units_music_on
        self.units_media += detailUsage.units_phone_ring
        self.units_media += detailUsage.units_phone_off_hook
        self.units_network += detailUsage.units_wifi_network
        self.units_network += detailUsage.units_2g_network
        self.units_network += detailUsage.units_3g_network
        self.units_network += detailUsage.units_4g_network
        self.units_network += detailUsage.units_5g_network
        self.units_network += detailUsage.units_other_network
        self.units_network += detailUsage.units_is_wifi_enable
        self.units_network += detailUsage.units_network_speed
        self.units_bluetooth += detailUsage.units_bluetooth
        self.units_cpu += detailUsage.units_cpu0
        self.units_cpu += detailUsage.units_cpu1
        self.units_cpu += detailUsage.units_cpu2
        self.units_cpu += detailUsage.units_cpu3
        self.units_cpu += detailUsage.units_cpu4
        self.units_cpu += detailUsage.units_cpu5
        self.units_cpu += detailUsage.units_cpu6
        self.units_cpu += detailUsage.units_cpu7
        self.units_mem += detailUsage.units_mem_available
        self.units_mem += detailUsage.units_mem_active
        self.units_mem += detailUsage.units_mem_dirty
        self.units_mem += detailUsage.units_mem_anonPages
        self.units_mem += detailUsage.units_mem_mapped
        self.total_power_consumption += detailUsage.total_power_consumption

    # def __get_total_power_consumption(self):
    #     total = self.units_screen_brightness
    #     total += self.units_music_on
    #     total += self.units_phone_ring
    #     total += self.units_phone_off_hook
    #     total += self.units_wifi_network
    #     total += self.units_2g_network
    #     total += self.units_3g_network
    #     total += self.units_4g_network
    #     total += self.units_5g_network
    #     total += self.units_other_network
    #     total += self.units_is_wifi_enable
    #     total += self.units_network_speed
    #     total += self.units_cpu0
    #     total += self.units_cpu1
    #     total += self.units_cpu2
    #     total += self.units_cpu3
    #     total += self.units_cpu4
    #     total += self.units_cpu5
    #     total += self.units_cpu6
    #     total += self.units_cpu7
    #     total += self.units_bluetooth
    #     total += self.units_mem_available
    #     total += self.units_mem_active
    #     total += self.units_mem_anonPages
    #     total += self.units_mem_dirty
    #     total += self.units_mem_mapped
    #     self.total_power_consumption = total


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
    def __init__(self):
        self.app_open_set = set()
        self.app_page_open_set = set()
        self.session_start_time = ""
        self.session_duration = 0
        self.session_network_spent = 0.0
        self.app_open_most_frequently_name = ""
        self.app_open_most_frequently_times = 0
        self.app_open_least_frequently_name = ""
        self.app_open_least_frequently_times = 0
        self.app_stay_longest_name = ""
        self.app_stay_longest_duration = 0
        self.app_stay_shortest_name = ""
        self.app_stay_shortest_duration = 0
        self.app_stay_longest_network = 0.0
        self.app_stay_shortest_network = 0.0
        self.units_base = 0.0
        self.units_screen_brightness = 0.0
        self.units_media = 0.0
        self.units_network = 0.0
        self.units_bluetooth = 0.0
        self.units_cpu = 0.0
        self.units_mem = 0.0
        self.total_power_consumption = 0.0
        self.all_units_power = []

    def to_excel_list(self) -> []:
        return [len(self.app_open_set), len(self.app_page_open_set), self.session_start_time, self.session_duration,
                self.session_network_spent, self.app_open_most_frequently_name, self.app_open_most_frequently_times,
                self.app_open_least_frequently_name, self.app_open_least_frequently_times, self.app_stay_longest_name,
                self.app_stay_longest_duration, self.app_stay_shortest_name, self.app_stay_shortest_duration,
                self.app_stay_longest_network, self.app_stay_shortest_network, self.units_base, self.units_screen_brightness,
                self.units_media, self.units_network, self.units_bluetooth, self.units_cpu, self.units_mem,
                self.total_power_consumption]

    @staticmethod
    def empty_session(start_time: str, duration: int):
        session = SessionSummery()
        session.set_app_usage(set(), set(), start_time, duration, 0, "", 0, "", 0, "", 0, "", 0, 0, 0)
        return session

    @staticmethod
    def excel_header() -> []:
        unit_headers = PP_SUMMARY_HEADERS[1:len(PP_SUMMARY_HEADERS)]
        headers = ["session期间不同App打开数量", "session期间不同页面打开数量", "session开始时间", "session持续时间",
                "session期间使用了多少流量", "app被打开最多次的名称", "同个app被打开最多的次数", "app被打开最少次的名称",
                "同个app被打开最少的次数", "session期间使用最久的App名", "session期间在某个APP停留的最长时间",
                "session期间使用时间最短的App名", "session期间在某个APP停留的最短时间", "使用最久的APP所消耗的流量",
                "使用最短的APP所消耗的流量"]
        headers.extend(unit_headers)
        return headers

    def set_app_usage(self,
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

    def add_up_units_power(self, summaryUsage: AppSummeryUsage):
        self.units_base += summaryUsage.units_base
        self.units_screen_brightness += summaryUsage.units_screen_brightness
        self.units_media += summaryUsage.units_media
        self.units_network += summaryUsage.units_network
        self.units_bluetooth += summaryUsage.units_bluetooth
        self.units_cpu += summaryUsage.units_cpu
        self.units_mem += summaryUsage.units_mem
        self.total_power_consumption += summaryUsage.total_power_consumption
        # self.__get_total_power_consumption()

    # @staticmethod
    # def from_list(fromList: []):
    #     if len(fromList) == 14:
    #         summaryUsage = SessionSummery(
    #             fromList[0], fromList[1], fromList[2], fromList[3],
    #             fromList[4], fromList[5], fromList[6], fromList[7],
    #             fromList[8], fromList[9], fromList[10], fromList[11],
    #             fromList[12], fromList[13], fromList[14])
    #         return summaryUsage


# class EveryDaySummery:
#     def __init__(self):


def get_page_network_spent(powerData: DataFrame, pageStartTime: str, pageEndTime: str):
    powerDataRows = powerData.shape[0]
    if powerDataRows == 0:
        return 0
    else:
        networkSpent = 0
        for row in range(powerDataRows):
            time = powerData.iloc[row, __power_time_idx]
            networkSpeed = powerData.iloc[row, __power_network_speed_idx]
            if TimeUtils.compare_time(time, pageEndTime) > 0:
                break
            if TimeUtils.compare_time(time, pageStartTime) >= 0:
                networkSpent += networkSpeed

        return networkSpent


def get_unit_consumption(unitPowerData: DataFrame, pageStartTime: str, pageEndTime: str) -> []:
    unitDataRows = unitPowerData.shape[0]
    if unitDataRows == 0:
        return []
    else:
        unitPowers = []
        for row in range(unitDataRows):
            # 跳过表头
            if row == 0:
                continue
            time = unitPowerData.iloc[row, __power_time_idx]
            # 当前时间已经超过结束时间
            if TimeUtils.compare_time(time, pageEndTime) > 0:
                break
            if TimeUtils.compare_time(time, pageStartTime) >= 0:
                if len(unitPowers) == 0:
                    unitPowers = unitPowerData.iloc[row]
                else:
                    # 累加
                    for idx, unit in enumerate(unitPowers):
                        # 跳过时间戳
                        if idx != 0:
                            unitPowers[idx] += unitPowerData.iloc[row, idx]

        return unitPowers


# 从app使用的详细记录里，总结出概括
def __summarize_detail_usage(detailUsages: [], outputRootDir: str) -> []:
    if detailUsages:
        tempUsages = detailUsages.copy()
        appSummaryUsagesDict = {}
        lastAppName = ""
        for detailUsage in tempUsages:
            # detailUsage = AppDetailUsage.from_list(detailUsage)
            appName = detailUsage.app_name
            category = detailUsage.category
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
                # 累加部件功耗
                appSummaryUsage.add_up_units_power(detailUsage)
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
                appSummaryUsage = AppSummeryUsage(appName, category, 1, pageNameSet,
                                                  pageName, pageDuration, pageName,
                                                  pageDuration, networkSpent, networkSpent,
                                                  pageDuration, networkSpent)
                appSummaryUsage.add_up_units_power(detailUsage)
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
                ExcelUtil.write_to_excel(toExcelData, outputRootDir, EXPORT_APP_SUMMARY_USAGES + EXCEL_SUFFIX)

            return appSummaryUsagesDict.values()
    return []


def __analyse_app_detail_usage(appUsageData: DataFrame, powerData: DataFrame, unitsPowerData: DataFrame, outputRootDir: str) -> []:
    appUsageRows = appUsageData.shape[0]

    appDetailUsages = []
    outAppDetailUsages = []
    appCategoryDict = AppCategory.get_app_category_dict(outputRootDir)
    for i in range(appUsageRows):
        lineHeader = appUsageData.iloc[i, 0]
        if __filter_session_summery in lineHeader:
            break
        elif bool(re.match(__filter_app_usage_pattern, lineHeader)):
            appName = appUsageData.iloc[i, __app_name_idx]
            category = AppCategory.get_app_category(outputRootDir, appName, appCategoryDict)
            appPage = appUsageData.iloc[i, __app_page_name_idx]
            startTime = appUsageData.iloc[i, __app_page_start_time_idx]
            endTime = appUsageData.iloc[i, __app_page_end_time_idx]
            pageDuration = appUsageData.iloc[i, __app_page_duration_time_idx]
            # 出现错误的时候，可能会出现 endTime 为 ERROR:Activity Resume Event Unfinished的情况
            # 这里做个兼容
            if math.isnan(pageDuration):
                pageDuration = 0
                endTime = startTime
            pageNetworkSpent = get_page_network_spent(powerData, startTime, endTime)
            appDetailUsage = AppDetailUsage(appName, category, appPage, startTime, pageDuration, pageNetworkSpent)
            appDetailUsage.add_unit_pw(get_unit_consumption(unitsPowerData, startTime, endTime))
            appDetailUsages.append(appDetailUsage.to_excel_list())
            outAppDetailUsages.append(appDetailUsage)
        else:
            continue

    # 输出app_detail_usage到文件
    if appDetailUsages:
        toExcelData = appDetailUsages.copy()
        toExcelData.insert(0, AppDetailUsage.excel_header())
        ExcelUtil.write_to_excel(toExcelData, outputRootDir, EXPORT_APP_DETAIL_USAGES + EXCEL_SUFFIX)

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
        sessionUsage = SessionSummery()
        for summaryUsage in tempSummaryUsages:
            appName = summaryUsage.app_name
            pageOpenSet = summaryUsage.page_open_set
            appNetWorkSpent = summaryUsage.app_network_spent
            openTimes = summaryUsage.app_open_times
            stayDuration = summaryUsage.app_stay_duration

            appOpenSet.add(appName)
            appPageOpenSet = appPageOpenSet.union(pageOpenSet)
            sessionNetworkSpent += appNetWorkSpent
            if appOpenMostFrequentlyTimes < openTimes:
                appOpenMostFrequentlyName = appName
                appOpenMostFrequentlyTimes = openTimes
            if appOpenLessFrequentlyTimes == 0 or appOpenLessFrequentlyTimes > openTimes:
                appOpenLessFrequentlyName = appName
                appOpenLessFrequentlyTimes = openTimes

            if appStayLongestDuration < stayDuration:
                appStayLongestName = appName
                appStayLongestNetworkSpent = appNetWorkSpent
                appStayLongestDuration = stayDuration
            if appStayShortestDuration == 0 or appStayShortestDuration > stayDuration:
                appStayShortestName = appName
                appStayShortestDuration = stayDuration
                appStayShortestNetworkSpent = appNetWorkSpent
            # 累加部件功耗
            sessionUsage.add_up_units_power(summaryUsage)
        sessionUsage.set_app_usage(appOpenSet, appPageOpenSet, startTime, sessionDuration, sessionNetworkSpent,
                                   appOpenMostFrequentlyName, appOpenMostFrequentlyTimes, appOpenLessFrequentlyName,
                                   appOpenLessFrequentlyTimes, appStayLongestName, appStayLongestDuration,
                                   appStayShortestName, appStayShortestDuration, appStayLongestNetworkSpent,
                                   appStayShortestNetworkSpent)
    else:
        sessionUsage = SessionSummery.empty_session(startTime, sessionDuration)

    toExcelData = [sessionUsage.to_excel_list()]
    toExcelData.insert(0, SessionSummery.excel_header())
    ExcelUtil.write_to_excel(toExcelData, outputRootDir, EXPORT_SESSION_SUMMARY + EXCEL_SUFFIX)


# noinspection DuplicatedCode
def analyse(appUsageFilePath: str, powerDataFilePath: str, unitsPowerDataPath: str, outputRootDir: str):
    try:
        if (not isinstance(appUsageFilePath, str)) or (not os.path.exists(appUsageFilePath)):
            JLog.e(__TAG, f"analyse, appUsageFilePath: [{StringUtil.get_short_file_name_for_print(appUsageFilePath)}] "
                          f"is not str or file does not exist, outputRootDir: {StringUtil.get_short_file_name_for_print(outputRootDir)}")
            return
        else:
            appUsageData = pd.read_excel(appUsageFilePath, header=None)

        if (not isinstance(powerDataFilePath, str)) or (not os.path.exists(powerDataFilePath)):
            JLog.i(__TAG, f"analyse, powerDataFilePath: [{StringUtil.get_short_file_name_for_print(powerDataFilePath)}] "
                          f"is not str or file does not exist, outputRootDir: {StringUtil.get_short_file_name_for_print(outputRootDir)}")
            powerData = DataFrame()
            # return
        else:
            powerData = pd.read_excel(powerDataFilePath, header=None)

        if (not isinstance(unitsPowerDataPath, str)) or (not os.path.exists(unitsPowerDataPath)):
            JLog.i(__TAG, f"analyse unitsPowerDataPath: [{StringUtil.get_short_file_name_for_print(unitsPowerDataPath)}] "
                          f"is not str or file does not exist, outputRootDir: {StringUtil.get_short_file_name_for_print(outputRootDir)}")
            unitsPowerData = DataFrame()
        else:
            unitsPowerData = pd.read_excel(unitsPowerDataPath, header=None)

        # 解析App使用详细数据
        appDetailUsages = __analyse_app_detail_usage(appUsageData, powerData, unitsPowerData, outputRootDir)

        # 得到app使用概括
        summaryUsages = __summarize_detail_usage(appDetailUsages, outputRootDir)

        # 解析Session使用概括
        startTime = appUsageData.iloc[0, __screen_on_time_idx]
        # 寻找第一列Session所在的行号
        sessionRowIdx = list(appUsageData.index[appUsageData.iloc[:, 0] == __session_for_search_row])
        if len(sessionRowIdx) == 0:
            JLog.t(__TAG, f"analyse: can not find Session's row index. found: {sessionRowIdx}")
            return
        sessionDuration = appUsageData.iloc[sessionRowIdx[0], __session_total_duration_idx]
        __analyse_session_usage(summaryUsages, startTime, sessionDuration, outputRootDir)
    except Exception as e:
        JLog.e(__TAG, f"analyse err happens: e = {e}, appUsageFilePath: {appUsageFilePath}, "
                      f"powerDataFilePath: {powerDataFilePath}, unitsPowerDataPath: {unitsPowerDataPath}")

    # 还是同一个app
    # if lastAppName == appName:
    #     # 这个页面出现过
    #     if appPage temp appClassMap:
    #         classUseCount = appClassMap[appName]
    #         appClassMap[appPage] = classUseCount + 1
    #         appDetailUsages[appPage]

#
# USER_NAME = INPUT_FILE + "/13266826670"
# activeRootPath = USER_NAME + "/" + CF_ACTIVITY_DIR
# appUsageFile = activeRootPath + "/20230405/20230405(17_34_11_713)$$20230405(17_34_51_612)/session_app_usage_39899.xlsx"
# longAppUsageFile = activeRootPath + "/20230513/20230513(13_05_57_720)$$20230513(13_06_07_938)/session_app_usage_10218.xlsx"
#
# outputDir = "./output/13266826670_三星/" + CF_ACTIVITY_DIR + "/20230405/20230405(17_34_11_713)$$20230405(17_34_51_612)"
# powerFile = outputDir + "/session_power_usage.xlsx"
#
# longOutputDir = "./output/13266826670/" + CF_ACTIVITY_DIR + "/20230513/20230513(13_05_57_720)$$20230513(13_06_07_938)"
# longPowerFile = longOutputDir + "/session_power_usage.xlsx"
# # analyse(appUsageFile, powerFile, outputDir)
# analyse(longAppUsageFile, longPowerFile, "", longOutputDir)
#
