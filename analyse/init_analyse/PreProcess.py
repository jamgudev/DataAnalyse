import os

from analyse.util.AnalyseUtils import get_all_user_name_from_dir
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE, CF_ACTIVITY_DIR
from util import ExcelUtil

__TAG = "PreProcess"


# 检索每个用户每天的session数量，并输出成文件
def iter_data_pre_process_check_sessions_in_every():
    dirName = TEST_OUTPUT_FILE
    allUsers = get_all_user_name_from_dir(dirName)
    dateOutPut = [[]]
    for user_name in allUsers:
        rootDir = dirName + "/" + user_name + "/" + CF_ACTIVITY_DIR
        dateDirs = []
        for dateDir in os.scandir(rootDir):
            dateDirs.append(dateDir.name)
        if dateDirs:
            dateDirs.sort()
            for dateDir in dateDirs:
                singleUserData = []
                dir_num = count_directories(rootDir + "/" + dateDir)
                singleUserData.append(user_name)
                singleUserData.append(dateDir)
                singleUserData.append(dir_num)
                dateOutPut.append(singleUserData)
        dateOutPut.append([])
    if dateOutPut:
        current_directory = os.path.dirname(os.path.abspath(__file__))
        ExcelUtil.write_to_excel(dateOutPut, current_directory, "iter_data_pre_process_check_sessions_in_every.xlsx")


def count_directories(directory):
    count = 0
    for entry in os.scandir(directory):
        if entry.is_dir():
            count += 1
    return count


iter_data_pre_process_check_sessions_in_every()
