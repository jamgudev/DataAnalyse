import os
import time
# 去掉UserWarning: Workbook contains no default style, apply openpyxl's default
import warnings

import pandas as pd
import tqdm as tqdm
from alive_progress import alive_bar

from analyse import AppUsageAnalyse
from analyse.FilePathDefinition import CF_ACTIVITY_DIR, INPUT_FILE, OUTPUT_FILE, CF_OUTPUT_POWER_USAGE, \
    EXCEL_SUFFIX
from analyse.util.AnalyseUtils import filter_file_fun

warnings.filterwarnings('ignore')

# Filter
__CF_APP_USAGE_FILTER = "session_app_usage_"
__CF_POWER_USAGE_FILTER = "session_power_usage_"

USER_NAME = "./" + INPUT_FILE + "/13266826670_三星"
activeRootPath = USER_NAME + "/" + CF_ACTIVITY_DIR


# 遍历文件夹
def iter_files(rootDir):
    # 遍历根目录
    for root, dirs, files in os.walk(rootDir):

        for sub_dir in dirs:
            iter_files(sub_dir)

        if files:
            # 对文件名做一个排序，防止power数据错乱
            files.sort()
            iter_data(root, files)


def iter_data(rootPath: str, files: []):
    # 过滤出想要的文件
    powerUsageFiles = filter(filter_power_data_fun, files)
    # 合并同文件夹下所有powerUsageFile
    powerDataOutputPath = merge_all_power_data(rootPath, powerUsageFiles)

    appUsageFiles = filter(filter_app_usage_fun, files)

    outputRootPath = rootPath.replace(INPUT_FILE, OUTPUT_FILE)
    with alive_bar(100, ctrl_c=False, title=f'分析进度{rootPath}') as bar:
        for file in appUsageFiles:
            fileAbsoluteName = os.path.join(rootPath, file)
            AppUsageAnalyse.analyse(fileAbsoluteName, powerDataOutputPath, outputRootPath)
            bar()


# 过滤app_usage文件
def filter_app_usage_fun(fileName) -> bool:
    return filter_file_fun(fileName, [__CF_APP_USAGE_FILTER])


def filter_power_data_fun(fileName) -> bool:
    return filter_file_fun(fileName, [__CF_POWER_USAGE_FILTER])


# 分析每个app_usage_file得到我们想要的数据
def analyse_app_usage_file(input_root_path: str, app_usage_file_name: str, power_file_name: str):
    outputRootPath = input_root_path.replace(INPUT_FILE, OUTPUT_FILE)
    if not os.path.exists(outputRootPath):
        os.makedirs(outputRootPath)

    # load power data
    powerFile = os.path.join(outputRootPath, power_file_name)
    powerData = pd.read_excel(powerFile, header=None)

    # load app usage data
    appUsageFile = os.path.join(input_root_path, app_usage_file_name)
    appUsageData = pd.read_excel(appUsageFile, header=None)


def merge_all_power_data(intputRootPath: str, fileNames: filter) -> str:
    outputRootPath = intputRootPath.replace(INPUT_FILE, OUTPUT_FILE)
    if not os.path.exists(outputRootPath):
        os.makedirs(outputRootPath)

    powerData = []
    # 为了获取filter的长度
    for fileName in fileNames:
        absolutePath = os.path.join(intputRootPath, fileName)
        data = pd.read_excel(absolutePath, header=None)
        # 获取行数
        rows = data.shape[0]
        for lineNum in range(rows):
            # 跳过表头
            if lineNum == 0:
                continue

            singleLine = data.iloc[lineNum]
            powerData.append(singleLine)

    if powerData:
        outputFilePath = outputRootPath + "/" + CF_OUTPUT_POWER_USAGE + EXCEL_SUFFIX
        outputDF = pd.DataFrame(powerData)
        outputDF.to_excel(outputFilePath, header=None, index=False)
        return outputFilePath




iter_files(activeRootPath)
