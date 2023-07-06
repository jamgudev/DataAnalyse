import os

import pandas as pd

from analyse.util import AnalyseUtils
from analyse.util.FilePathDefinition import CF_ACTIVITY_DIR, OUTPUT_FILE, INPUT_FILE
from util import StringUtil, JLog
__TAG = "EveryDayAnalyseFromOutput"


# 从用户名根目录开始遍历，按每天的数据文件进行遍历，并根据参数遍历该文件数据中某一列的数据，并整理成dict返回
# 比如: ./13266826670/HWStatistics/active/20230509
# data = iter_idx_data_from_file_in_every_day("13266826670", "session_summary.xlsx", 3)
# for key in data.keys():
#     dayData = data[key]
#     dataStr = ""
#     for d in dayData:
#         dataStr += str(d) + ", "
#     print(f"{key}: {dataStr}, size = {len(dayData)}")
def iter_idx_data_from_file_in_every_day(user_name: str, data_file_name: str, data_idx: int) -> {}:
    fileDict = iter_file_in_every_day(user_name, data_file_name)
    dataOfEveryDay = {}
    for day_key in fileDict.keys():
        files = fileDict[day_key]
        idxData = []
        for file in files:
            if os.path.exists(file):
                dataFrame = pd.read_excel(file, header=None)
                rows = dataFrame.shape[0]
                cols = dataFrame.shape[1]
                if cols <= data_idx:
                    JLog.t(__TAG, f"iter_idx_data_from_file_in_every_day: data_idx[{data_idx}] out of range[{cols}]")
                else:
                    for row in range(rows):
                        # 跳过表头
                        if row == 0:
                            continue
                        targetData = str(dataFrame.iloc[row, data_idx])
                        if targetData.isdigit():
                            idxData.append(float(targetData))
                        else:
                            idxData.append(targetData)
            else:
                JLog.t(__TAG, f"iter_idx_data_from_file_in_every_day: file[{file}] not exists.")

        if day_key in dataOfEveryDay:
            dataOfEveryDay[day_key].extend(idxData)
        else:
            dataOfEveryDay[day_key] = idxData

    return dataOfEveryDay


# iter_file_in_every_day("13266826670", "session_summary.xlsx")
def iter_file_in_every_day(user_name: str, data_file_name: str) -> {}:
    fileDict = {}
    rootDir = OUTPUT_FILE + "/" + user_name + "/" + CF_ACTIVITY_DIR
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

            if dateOfDay in fileDict:
                filesOfDay = fileDict[dateOfDay]
                filesOfDay.extend(paths)
            else:
                fileDict[dateOfDay] = paths


# 解析这种格式的字符串：/Users/JAMGU_1/PycharmProjects/pythonProject/analyse/output/13266826670/HWStatistics/active/20230626
def __get_date_from_dir_name(dir_name: str) -> str:
    if not isinstance(dir_name, str) or len(dir_name) == 0:
        return ""
    else:
        return StringUtil.get_short_file_name_for_print(dir_name)

