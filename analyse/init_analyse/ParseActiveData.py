import os
# 去掉UserWarning: Workbook contains no default style, apply openpyxl's default
import warnings
from multiprocessing import Pool

import pandas as pd
from alive_progress import alive_bar

from analyse.init_analyse import AppUsageAnalyse
from analyse.init_analyse.power_params import PowerParamsUtil
from analyse.util.AnalyseUtils import filter_file_fun
from analyse.util.FilePathDefinition import CF_OUTPUT_POWER_USAGE, \
    EXCEL_SUFFIX, POWER_PARAMS_THETA_IDX, POWER_PARAMS_SIGMA_IDX, POWER_PARAMS_MU_IDX, EXPORT_UNITS_POWER, PP_HEADERS, \
    CF_ACTIVITY_DIR, POWER_PARAMS_MAT, INPUT, OUTPUT, POWER, POWER_PARAMS_LIST, POWER_PARAMS_DIR
from util import JLog, ExcelUtil, StringUtil
from util.StringUtil import get_user_name, get_mobile_number_start_pos

warnings.filterwarnings('ignore')

# Filter
__CF_APP_USAGE_FILTER = "session_app_usage_"
__CF_POWER_USAGE_FILTER = "session_power_usage_"

__TAG = "ParseActiveData"


# pool_size，最大并发数量
def mutil_process_iter_files(dirName: str, mutil_num: int = os.cpu_count() - 4):
    if mutil_num <= 0:
        mutil_num = os.cpu_count() / 2

    if os.path.exists(dirName):
        with alive_bar(100, manual=True, ctrl_c=True, title=f'分析进度') as bar:
            allUserName = []
            # 该路径下所有目录及文件(不包含子目录)
            files = os.listdir(dirName)
            for file in files:
                # 过滤目录文件
                if os.path.isdir(os.path.join(dirName, file)):
                    allUserName.append(file)
            bar(0.2)
            if allUserName:
                pool = Pool(mutil_num)
                for idx, name in enumerate(allUserName):
                    # callback=lambda x: bar(0.2 + (((idx + 1) * 1.0 / len(allUserName)) * 0.8))
                    pool.apply_async(iter_files, (dirName, name, True),
                                     callback=lambda x: bar(0.2 + 1.0 / len(allUserName) * 0.7))
                # 不再接受新任务
                pool.close()
                # 等待所有线程池完成任务
                pool.join()
                bar(1)
            else:
                bar(1)
                return
    else:
        JLog.t(__TAG, f"mutil_process_iter_files, input_file_path error, file{dirName} not exists.")


def single_process_iter_files(dirName: str):
    if os.path.exists(dirName):
        allUserName = []
        # 该路径下所有目录及文件(不包含子目录)
        files = os.listdir(dirName)
        for file in files:
            # 过滤目录文件
            if os.path.isdir(os.path.join(dirName, file)):
                allUserName.append(file)
        if allUserName:
            for userName in allUserName:
                iter_files(dirName, userName, False)
    else:
        JLog.t(__TAG, f"mutil_process_iter_files, input_file_path error, file{dirName} not exists.")


def iter_files(filePath: str, user_name: str, multi_process: bool = False):
    path = f"{filePath}/{user_name}/{CF_ACTIVITY_DIR}"
    __iter_files(path, multi_process)


# 遍历文件夹
def __iter_files(rootDir, multi_process: bool = False):
    # 遍历根目录
    for root, dirs, files in os.walk(rootDir):

        dirs.sort()
        for sub_dir in dirs:
            __iter_files(sub_dir)

        if files:
            iter_data(root, files, multi_process)


def iter_data(rootPath: str, files: [], mutil_process: bool = False):
    # 非多进程用进度条追踪进度
    if not mutil_process:
        with alive_bar(100, manual=True, ctrl_c=True, title=f'{StringUtil.get_user_name(rootPath)} '
                                                            f'{StringUtil.get_short_file_name_for_print(rootPath)}') as bar:
            # 对文件名做一个排序，防止power数据错乱
            files.sort()
            bar(0.05)
            # 过滤出想要的文件
            powerUsageFiles = filter(filter_power_data_fun, files)
            bar(0.10)
            # 合并同文件夹下所有powerUsageFile
            outputRootPath = rootPath.replace(INPUT, OUTPUT)
            powerDataOutputPath = merge_all_power_data(rootPath, powerUsageFiles)
            bar(0.35)
            # 计算各部件分别的功耗
            unitsPowerDataPath = export_units_power(rootPath, powerDataOutputPath)
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
                    AppUsageAnalyse.analyse(appUsageFilePath, powerDataOutputPath, unitsPowerDataPath, outputRootPath)
                    bar(0.5 + (((idx + 1) * 1.0 / fileNum) * 0.5))
    else:
        # 对文件名做一个排序，防止power数据错乱
        files.sort()
        # 过滤出想要的文件
        powerUsageFiles = filter(filter_power_data_fun, files)
        # 合并同文件夹下所有powerUsageFile
        outputRootPath = rootPath.replace(INPUT, OUTPUT)
        powerDataOutputPath = merge_all_power_data(rootPath, powerUsageFiles)
        # 计算各部件分别的功耗
        unitsPowerDataPath = export_units_power(rootPath, powerDataOutputPath)
        # 过滤出 session_app_usage_ 文件
        appUsageFiles = list(filter(filter_app_usage_fun, files))
        fileNum = len(appUsageFiles)
        if fileNum == 0:
            return
        else:
            for idx, file in enumerate(appUsageFiles):
                appUsageFilePath = os.path.join(rootPath, file)
                AppUsageAnalyse.analyse(appUsageFilePath, powerDataOutputPath, unitsPowerDataPath, outputRootPath)


# 过滤app_usage文件
def filter_app_usage_fun(fileName) -> bool:
    return filter_file_fun(fileName, [__CF_APP_USAGE_FILTER])


def filter_power_data_fun(fileName) -> bool:
    return filter_file_fun(fileName, [__CF_POWER_USAGE_FILTER])


# 合并所有power_data文件
def merge_all_power_data(intputRootPath: str, fileNames: filter) -> str:
    try:
        outputRootPath = intputRootPath.replace(INPUT, POWER)
        outputFilePath = outputRootPath + "/" + CF_OUTPUT_POWER_USAGE + EXCEL_SUFFIX
        if os.path.exists(outputFilePath):
            JLog.i(__TAG, f"merge_all_power_data, userName[{StringUtil.get_user_name(intputRootPath)}], "
                          f"power file {StringUtil.get_short_file_name_for_print(outputFilePath)} already exist, skipped.")
            return outputFilePath

        powerData = []
        # 为了获取filter的长度
        for fileName in fileNames:
            absolutePath = os.path.join(intputRootPath, fileName)
            # 文件可读
            if os.access(absolutePath, os.R_OK):
                data = pd.read_excel(absolutePath, header=None)
                # 获取行数
                rows = data.shape[0]
                for lineNum in range(rows):
                    # 跳过表头
                    if lineNum == 0:
                        continue

                    # 到network_spend
                    singleLine = data.iloc[lineNum,
                        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 21, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 24, 25, 26]]
                    powerData.append(singleLine)
            else:
                JLog.d(__TAG, f"merge_all_power_data, userName[{StringUtil.get_user_name(intputRootPath)}], "
                              f"file[{fileName}] dir[{intputRootPath}] unreadable, skipped.")

        if powerData:
            ExcelUtil.write_to_excel(powerData, outputRootPath, CF_OUTPUT_POWER_USAGE + EXCEL_SUFFIX)
            return outputFilePath
    except Exception as e:
        JLog.e(__TAG, f"merge_all_power_data, userName[{StringUtil.get_user_name(intputRootPath)}], "
                      f"merge_all_power_data err happens: e = {e}")
    return ""


# 输出功耗文件，并返回路径
def export_units_power(dirName: str, powerDataPath: str) -> str:
    if isinstance(powerDataPath, str) and powerDataPath == "" or (not os.path.exists(powerDataPath)):
        JLog.e(__TAG, f"export_units_power failed: dirName[{dirName}], "
                      f"file from powerDataPath[{powerDataPath}] not exists, skipped.")
        return ""

    powerParamFilePath = ""
    try:
        outputDir = dirName.replace(INPUT, POWER)
        outputFileName = EXPORT_UNITS_POWER + EXCEL_SUFFIX
        unitAbsFileName = os.path.join(outputDir, outputFileName)
        if os.path.exists(unitAbsFileName):
            JLog.i(__TAG, f"export_units_power: userName[{get_user_name(dirName)}], power file {outputFileName} already exist, skipped.")
            return unitAbsFileName

        powerData = ExcelUtil.read_excel(powerDataPath, 1)
        userName = get_user_name(outputDir)
        dirName = dirName[0: get_mobile_number_start_pos(dirName) - 1]
        userPowerParamsFileDirName = PowerParamsUtil.get_phone_brand_by_user_name(userName)
        powerParamFilePath = POWER_PARAMS_DIR + "/" + userPowerParamsFileDirName + "/" + POWER_PARAMS_MAT
        paramsData = ExcelUtil.read_excel(powerParamFilePath, 2)
        if not powerData.empty:
            powerDataRows = powerData.shape[0]
            powerDataCols = powerData.shape[1]
            unitPowerData = []
            for row in range(powerDataRows):
                unitPower = []
                totalPower = 0.0
                for col in range(powerDataCols):
                    matrixData = powerData.iloc[row, col]
                    # 跳过时间戳
                    if col == 0:
                        # 添加基础功耗
                        base = float(paramsData.iloc[POWER_PARAMS_THETA_IDX, col])
                        totalPower += base
                        unitPower.append(matrixData)
                        unitPower.append(base)
                        continue
                    else:
                        # 计算各部件功耗并添加
                        theta = float(paramsData.iloc[POWER_PARAMS_THETA_IDX, col])
                        mu = float(paramsData.iloc[POWER_PARAMS_MU_IDX, col])
                        sigma = float(paramsData.iloc[POWER_PARAMS_SIGMA_IDX, col])
                        featureNormalizeVal = __feature_normalize("max", mu, sigma, float(matrixData))
                        powerConsumption = featureNormalizeVal * theta
                        totalPower += powerConsumption
                        unitPower.append(powerConsumption)
                unitPower.append(totalPower)
                unitPowerData.append(unitPower)
            if unitPowerData:
                exportData = unitPowerData.copy()
                exportData.insert(0, PP_HEADERS)
                ExcelUtil.write_to_excel(exportData, outputDir, outputFileName)
                return unitAbsFileName
            else:
                return ""
        else:
            return ""
    except Exception as e:
        JLog.e(__TAG, f"export_units_power err, dirName = {dirName},"
                      f" powerParamFilePath = {powerParamFilePath}, e = {e}")
    return ""


def __feature_normalize(pattern: str, a: float, b: float, data: float) -> float:
    if pattern == "mean":
        mu = a
        sigma = b
        if sigma == 0:
            return 0.0
        else:
            return (data - mu) / sigma
    elif pattern == "max":
        minV = a
        maxV = b
        divider = maxV - minV
        if divider == 0:
            return 0.0
        return abs(data - minV) / divider
    else:
        raise ValueError(f"pattern[{pattern}] not specified or un-known.")

# USER_NAME = INPUT_FILE + "/13266826670"
# activeRootPath = USER_NAME + "/" + CF_ACTIVITY_DIR
# appUsageFile = activeRootPath + "/20230405/20230405(17_34_11_713)$$20230405(17_34_51_612)/session_app_usage_39899.xlsx"
# longAppUsageFile = activeRootPath + "/20230513/20230513(13_05_57_720)$$20230513(13_06_07_938)/session_app_usage_10218.xlsx"
# iter_files(activeRootPath + "/20230513")
