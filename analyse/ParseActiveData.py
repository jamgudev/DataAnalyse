from analyse.FilePathDefinition import CF_ACTIVITY_DIR, CF_APP_USAGE_FILTER, CF_POWER_USAGE_FILTER, INPUT_FILE, OUTPUT_FILE
import os

USER_NAME = "./" + INPUT_FILE + "/13266826670_三星"

activeRootPath = USER_NAME + "/" + CF_ACTIVITY_DIR


# 遍历文件夹
def iter_files(rootDir):
    # 遍历根目录
    for root, dirs, files in os.walk(rootDir):

        for sub_dir in dirs:
            iter_files(sub_dir)

        # 过滤出想要的文件
        powerUsageFiles = filter(filter_power_data_fun, files)
        # 合并同文件夹下所有powerUsageFile
        mergeAllPowerData(root, powerUsageFiles)

        appUsageFiles = filter(filter_app_usage_fun, files)
        for file in appUsageFiles:
            fileAbsoluteName = os.path.join(root, file)
            print(fileAbsoluteName)



# 过滤app_usage文件
def filter_app_usage_fun(fileName) -> bool:
    return __filter_file_fun(fileName, [CF_APP_USAGE_FILTER])


def filter_power_data_fun(fileName) -> bool:
    return __filter_file_fun(fileName, [CF_POWER_USAGE_FILTER])


# fileName contains the element in filterList, being taken.
def __filter_file_fun(fileName: str, filterList: []) -> bool:
    if len(filterList) == 0:
        return False

    for element in filterList:
        if element in fileName:
            return True
        else:
            return False


# 分析每个app_usage_file得到我们想要的数据
def analyse_app_usage_file(intputRootPath, file_name):
    outputRootPath = intputRootPath.replace(INPUT_FILE, OUTPUT_FILE)
    print(outputRootPath)
    if not os.path.exists(outputRootPath):
        os.makedirs(outputRootPath)


def mergeAllPowerData(intputRootPath: str, fileNames: []):
    outputRootPath = intputRootPath.replace(INPUT_FILE, OUTPUT_FILE)
    if not os.path.exists(outputRootPath):
        os.makedirs(outputRootPath)





iter_files(activeRootPath)
