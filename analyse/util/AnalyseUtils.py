# fileName contains the element temp filterList, being taken.
import os

import numpy as np


def filter_file_fun(fileName: str, filterList: []) -> bool:
    if len(filterList) == 0:
        return True

    for element in filterList:
        if element in fileName:
            return True
        else:
            return False


def filter_list_fun(originList: [], filterList: []) -> bool:
    if (len(filterList)) == 0:
        return True

    for item in originList:
        for filter_element in filterList:
            if filter_element in item:
                return True
            else:
                return False


# 最多支持二维列表，返回也是二维列表
# 二维时返回的是一个列表，一维返回一个浮点数
def get_mean_of_list(data: []):
    if is_list_two_dimensional(data):
        # 二维，但第二维只有一个元素，当一维处理
        if len(data) == 1:
            f_value = list(map(float, data[0]))
            return float(np.mean(f_value))
        else:
            res = []
            for value in data:
                f_value = list(map(float, value))
                t_res = float(np.mean(f_value))
                res.append(t_res)
            return res
    elif data:
        f_value = list(map(float, data))
        return float(np.mean(f_value))
    else:
        return 0.0


# 最多支持二维列表，返回也是二维列表
# 二维时返回的是一个列表，一维返回一个浮点数
def get_standard_deviation_of_list(data: []):
    if is_list_two_dimensional(data):
        # 二维，但第二维只有一个元素，当一维处理
        if len(data) == 1:
            f_value = list(map(float, data[0]))
            return float(np.std(f_value))
        else:
            res = []
            for value in data:
                f_value = list(map(float, value))
                t_res = float(np.std(f_value))
                res.append(t_res)
            return res
    elif data:
        f_value = list(map(float, data))
        return float(np.std(f_value))
    else:
        return 0.0


def get_upper_end_of_std(data: []) -> float:
    return get_mean_of_list(data) + get_standard_deviation_of_list(data)


def get_lower_end_of_std(data: []) -> float:
    return get_mean_of_list(data) - get_standard_deviation_of_list(data)


def get_mean_of_dict(dic: {}) -> []:
    if dic:
        res = []
        for values in dic.values():
            if values:
                mean = get_mean_of_list(values)
                res.append(mean)
            else:
                continue
        return res
    else:
        return []


def get_standard_deviation_of_dict(dic: {}) -> []:
    if dic:
        res = []
        for values in dic.values():
            if values:
                std = get_standard_deviation_of_list(values)
                res.append(std)
            else:
                continue
        return res
    else:
        return []


def get_all_user_name_from_dir(dirName: str) -> []:
    if os.path.exists(dirName):
        allUserName = []
        # 该路径下所有目录及文件(不包含子目录)
        files = os.listdir(dirName)
        for file in files:
            # 过滤目录文件
            if os.path.isdir(os.path.join(dirName, file)):
                allUserName.append(file)
        allUserName.sort()
        return allUserName
    else:
        return []


# 判断一个列表是否为二维列表
def is_list_two_dimensional(lst: []) -> bool:
    if not lst:
        return False

    # 检查列表中的每个元素是否为列表
    for element in lst:
        if not isinstance(element, list):
            return False
    return True
