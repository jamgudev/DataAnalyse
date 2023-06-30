import os
# 去掉UserWarning: Workbook contains no default style, apply openpyxl's default
import warnings

import pandas as pd
from alive_progress import alive_bar

from analyse.init_analyse import AppUsageAnalyse
from analyse.util.FilePathDefinition import CF_ACTIVITY_DIR, INPUT_FILE, OUTPUT_FILE, CF_OUTPUT_POWER_USAGE, \
    EXCEL_SUFFIX, POWER_PARAMS_PATH, POWER_PARAMS_THETA_IDX, POWER_PARAMS_SIGMA_IDX, POWER_PARAMS_MU_IDX, EXPORT_UNITS_POWER, PP_HEADERS
from analyse.util import StringUtil
from analyse.util.AnalyseUtils import filter_file_fun
from util import JLog, ExcelUtil

warnings.filterwarnings('ignore')

# Filter
__CF_APP_USAGE_FILTER = "session_app_usage_"
__CF_POWER_USAGE_FILTER = "session_power_usage_"

__TAG = "ParseActiveData"


# 遍历文件夹
def iter_files(rootDir):
    # 遍历根目录
    for root, dirs, files in os.walk(rootDir):

        dirs.sort()
        for sub_dir in dirs:
            iter_files(sub_dir)

        if files:
            iter_data(root, files)


def iter_data(rootPath: str, files: []):
    with alive_bar(100, manual=True, ctrl_c=True, title=f'分析进度 {StringUtil.get_short_file_name_for_print(rootPath)}') as bar:
        # 对文件名做一个排序，防止power数据错乱
        files.sort()
        bar(0.05)
        # 过滤出想要的文件
        powerUsageFiles = filter(filter_power_data_fun, files)
        bar(0.10)
        # 合并同文件夹下所有powerUsageFile
        outputRootPath = rootPath.replace(INPUT_FILE, OUTPUT_FILE)
        powerDataOutputPath = merge_all_power_data(rootPath, powerUsageFiles)
        bar(0.35)
        # 计算各部件分别的功耗
        unitsPowerData = export_units_power(powerDataOutputPath, outputRootPath)
        bar(0.45)
        # 过滤出 session_app_usage_ 文件
        appUsageFiles = list(filter(filter_app_usage_fun, files))
        bar(0.50)
        fileNum = len(appUsageFiles)
        if fileNum == 0:
            bar(1)
            return
        else:
            for idx, file in enumerate(appUsageFiles):
                appUsageFilePath = os.path.join(rootPath, file)
                AppUsageAnalyse.analyse(appUsageFilePath, powerDataOutputPath, outputRootPath)
                bar(0.5 + (((idx + 1) * 1.0 / fileNum) * 0.5))


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

    outputFilePath = outputRootPath + "/" + CF_OUTPUT_POWER_USAGE + EXCEL_SUFFIX
    if os.path.exists(outputFilePath):
        JLog.i(__TAG, f"power file {StringUtil.get_short_file_name_for_print(outputFilePath)} already exist, skipped.")
        return outputFilePath

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
        ExcelUtil.write_to_excel(powerData, outputRootPath, CF_OUTPUT_POWER_USAGE + EXCEL_SUFFIX)
        return outputFilePath

    return ""


# 输出功耗文件，并返回路径
def export_units_power(powerDataPath: str, outputDir: str) -> str:
    if not os.path.exists(powerDataPath):
        JLog.e(__TAG, f"calculate_units_power failed: file from powerDataPath[{powerDataPath}] not exists, skipped.")
        return ""

    powerData = ExcelUtil.read_excel(powerDataPath, 1)
    paramsData = ExcelUtil.read_excel(POWER_PARAMS_PATH, 2)
    if not powerData.empty:
        powerDataRows = powerData.shape[0]
        powerDataCols = powerData.shape[1]
        unitPowerData = []
        for row in range(powerDataRows):
            unitPower = []
            for col in range(powerDataCols):
                matrixData = powerData.iloc[row, col]
                # 跳过时间戳
                if col == 0:
                    unitPower.append(matrixData)
                    continue
                else:
                    theta = float(paramsData.iloc[POWER_PARAMS_THETA_IDX, col - 1])
                    mu = float(paramsData.iloc[POWER_PARAMS_MU_IDX, col - 1])
                    sigma = float(paramsData.iloc[POWER_PARAMS_SIGMA_IDX, col - 1])
                    if sigma == 0:
                        featureNormalizeVal = 0
                    else:
                        featureNormalizeVal = (float(matrixData) - mu) / sigma
                    powerConsumption = featureNormalizeVal * theta
                    unitPower.append(powerConsumption)
            unitPowerData.append(unitPower)
        if unitPowerData:
            exportData = unitPowerData.copy()
            exportData.insert(0, PP_HEADERS)
            ExcelUtil.write_to_excel(exportData, outputDir, EXPORT_UNITS_POWER + EXCEL_SUFFIX)
            return os.path.join(outputDir, EXPORT_UNITS_POWER + EXCEL_SUFFIX)
        else:
            return ""
    else:
        return ""
