from alive_progress import alive_bar

from analyse.graph.GrapgNameSapce import AS_APP_NAME, AS_UNIT_CS_SCREEN, \
    AS_UNIT_CS_MEDIA, AS_UNIT_CS_NETWORK, AS_UNIT_CS_BLUETOOTH, AS_UNIT_CS_CPU, AS_UNIT_CS_MEM, AS_UNIT_CS_TOTAL, AS_APP_CATEGORY, \
    GRAPH_units_consumption
from analyse.graph.base.__EveryDayAnalyseFromOutput import iter_idx_data_from_file_in_every_day
from analyse.util.AnalyseUtils import get_all_user_name_from_dir
from analyse.util.FilePathDefinition import EXCEL_SUFFIX, TEST_OUTPUT_FILE, EXPORT_SESSION_SUMMARY, OUTPUT_FILE, EXPORT_APP_SUMMARY_USAGES
from util import JLog, ExcelUtil


# 所有用户，在各个app使用的时间占用户各自总使用时间的占比
def units_consumption():
    dirName = OUTPUT_FILE
    allUserName = get_all_user_name_from_dir(dirName)
    if allUserName:
        allUserData = []
        unitsUsages = {}
        totalConsumption = 0.0
        with alive_bar(len(allUserName), ctrl_c=True, force_tty=True, title=f'分析进度') as bar:
            for userName in allUserName:
                dataOfEveryDay = iter_idx_data_from_file_in_every_day(dirName, userName,
                                                                      EXPORT_APP_SUMMARY_USAGES + EXCEL_SUFFIX,
                                                                      [AS_APP_NAME, AS_APP_CATEGORY,
                                                                       AS_UNIT_CS_SCREEN, AS_UNIT_CS_MEDIA,
                                                                       AS_UNIT_CS_NETWORK, AS_UNIT_CS_BLUETOOTH,
                                                                       AS_UNIT_CS_CPU, AS_UNIT_CS_MEM,
                                                                       AS_UNIT_CS_TOTAL])
                if isinstance(dataOfEveryDay, dict):
                    # 遍历每天数据
                    for idx, data in enumerate(dataOfEveryDay.values()):
                        try:
                            # 遍历一天中的所有数据
                            for app_usage_idx, app_usage_name in enumerate(data[0]):
                                screenConsumption = float(data[2][app_usage_idx])
                                mediaConsumption = float(data[3][app_usage_idx])
                                networkConsumption = float(data[4][app_usage_idx])
                                bluetoothConsumption = float(data[5][app_usage_idx])
                                cpuConsumption = float(data[6][app_usage_idx])
                                memConsumption = float(data[7][app_usage_idx])
                                totalConsumption += float(data[8][app_usage_idx])
                                if "screen" not in unitsUsages:
                                    unitsUsages["screen"] = 0.0
                                if "media" not in unitsUsages:
                                    unitsUsages["media"] = 0.0
                                if "network" not in unitsUsages:
                                    unitsUsages["network"] = 0.0
                                if "bluetooth" not in unitsUsages:
                                    unitsUsages["bluetooth"] = 0.0
                                if "cpu" not in unitsUsages:
                                    unitsUsages["cpu"] = 0.0
                                if "memory" not in unitsUsages:
                                    unitsUsages["memory"] = 0.0
                                unitsUsages["screen"] += screenConsumption
                                unitsUsages["media"] += mediaConsumption
                                unitsUsages["network"] += networkConsumption
                                unitsUsages["bluetooth"] += bluetoothConsumption
                                unitsUsages["cpu"] += cpuConsumption
                                unitsUsages["memory"] += memConsumption
                        except Exception as e:
                            JLog.e("mean_active_time_per_day_with_std_of_every_user_pure",
                                   f"error: userName:{userName}, idx[{idx}], data:{data}, e:{e}")
                bar()
            for key in unitsUsages.keys():
                allUserData.append([key, unitsUsages[key] / totalConsumption])
            allUserData.insert(0, ["部件名", "消耗的功耗占比"])
            ExcelUtil.write_to_excel(allUserData, dirName,
                                     GRAPH_units_consumption)


units_consumption()
