import os

import pandas as pd

from analyse.graph.GrapgNameSapce import AD_APP_PKG_NAME
from analyse.graph.base.__EveryDayAnalyseFromOutput import iter_file_in_every_day, __TAG
from analyse.util.FilePathDefinition import EXPORT_APP_DETAIL_USAGES, EXCEL_SUFFIX
from util import JLog


def iter_idx_app_detail_data_from_file_in_every_day(dirName: str, user_name: str, data_idxs: []) -> {}:
    data_file_name = EXPORT_APP_DETAIL_USAGES + EXCEL_SUFFIX
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
                appUsagesDict = {}
                rows = dataFrame.shape[0]
                cols = dataFrame.shape[1]
                if data_idxs:
                    for row in range(rows):
                        str(dataFrame.iloc[row, AD_APP_PKG_NAME])
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