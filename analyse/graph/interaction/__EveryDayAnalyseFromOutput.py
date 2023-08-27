import os

import pandas as pd

from analyse.util.FilePathDefinition import CF_ACTIVITY_DIR
from util import StringUtil, JLog

__TAG = "EveryDayAnalyseFromOutput"


# 从用户名根目录开始遍历，按每天的数据文件进行遍历，并根据参数遍历该文件数据中某一列的数据，并整理成dict返回
# 比如: ./13266826670/HWStatistics/active/20230509
# dayDatas = iter_idx_data_from_file_in_every_day(TEST_OUTPUT_FILE, "13266826670", "session_summary.xlsx", [2, 3])
# for key temp dayDatas.keys():
#     dayData = dayDatas[key]
#     for idx, data temp enumerate(dayData):
#         dataStr = f"{key}, id[{idx}] "
#         for d temp data:
#             dataStr += str(d) + ", "
#         print(dataStr)

# {"20230701": [[data_idx_1...], [data_idx_2...]], "20230702": [[data_idx_1...], [data_idx_2...]], }
def iter_idx_data_from_file_in_every_day(dirName: str, user_name: str, data_file_name: str, data_idxs: []) -> {}:
    fileDict = iter_file_in_every_day(dirName, user_name, data_file_name)
    dataOfEveryDay = {}
    # 取每天的文件
    for day_key in fileDict.keys():
        files = fileDict[day_key]
        # 存储 {"data_idx_1": [], "data_idx_2": [], ..}
        idxDataDict = {}
        # 遍历某天的所有文件
        for file in files:
            if os.path.exists(file):
                try:
                    dataFrame = pd.read_excel(file, header=None)
                except ValueError as e:
                    JLog.t(__TAG, f"iter_idx_data_from_file_in_every_day read_excel error: file[{file}], e[{e}]")
                    return dataOfEveryDay
                rows = dataFrame.shape[0]
                cols = dataFrame.shape[1]
                if data_idxs:
                    for row in range(rows):
                        # 遍历row行，data_idx列需要的索引数据
                        for data_idx in data_idxs:
                            if cols <= data_idx:
                                JLog.t(__TAG, f"iter_idx_data_from_file_in_every_day: "
                                              f"data_idx[{data_idx}] out of range[{cols}]")
                                return
                            # 跳过表头
                            if row == 0:
                                continue
                            # targetData为row行，data_idx列具体的数据
                            targetData = str(dataFrame.iloc[row, data_idx])
                            if data_idx in idxDataDict:
                                idxDataDict[data_idx].append(targetData)
                            else:
                                idxDataDict[data_idx] = [targetData]
                else:
                    JLog.t(__TAG, "iter_idx_data_from_file_in_every_day err, data_idxs is empty.")
                    return {}
            else:
                JLog.t(__TAG, f"iter_idx_data_from_file_in_every_day: file[{file}] not exists.")
                return {}

        if day_key in dataOfEveryDay:
            dayValues = dataOfEveryDay[day_key]
            for idx, value in enumerate(idxDataDict.values()):
                dayValues[idx].extend(value)
        else:
            dayValues = []
            # 按照data_idxs的索引顺序，将需要的数据按顺序存到新的[]
            # 不如参数data_idxs传进来是[3, 2]，存到dayValues后的顺序为：先存索引3的数据，然后存索引2的数据
            # dayValues是一个二维list，[[3_1, 3_2..], [2_1, 2_2..]]
            for idx, dayValue in enumerate(idxDataDict.values()):
                dayValues.append(dayValue)
            dataOfEveryDay[day_key] = dayValues

    return dataOfEveryDay


# iter_file_in_every_day("13266826670", "session_summary.xlsx")
def iter_file_in_every_day(dirName: str, user_name: str, data_file_name: str) -> {}:
    fileDict = {}
    rootDir = dirName + "/" + user_name + "/" + CF_ACTIVITY_DIR
    __inner_iter_file_in_every_day(rootDir, data_file_name, fileDict)
    return fileDict


def __inner_iter_file_in_every_day(rooDir: str, data_file_name: str, fileDict: {}):
    for root, dirs, files in os.walk(rooDir):
        dirs.sort()
        for sub_dir in dirs:
            __inner_iter_file_in_every_day(sub_dir, data_file_name, fileDict)

        if files:
            dateOfDay = __get_date_from_dir_name(os.path.dirname(root))
            paths = []
            for file in files:
                if file == data_file_name:
                    paths.append(os.path.join(root, file))

            if paths:
                if dateOfDay in fileDict:
                    filesOfDay = fileDict[dateOfDay]
                    filesOfDay.extend(paths)
                else:
                    fileDict[dateOfDay] = paths
    # 对paths升序排序
    for day in fileDict.keys():
        dayPaths = fileDict[day]
        dayPaths.sort()


# 解析这种格式的字符串：/Users/JAMGU_1/PycharmProjects/pythonProject/analyse/output/13266826670/HWStatistics/active/20230626
def __get_date_from_dir_name(dir_name: str) -> str:
    if not isinstance(dir_name, str) or len(dir_name) == 0:
        return ""
    else:
        return StringUtil.get_short_file_name_for_print(dir_name)

