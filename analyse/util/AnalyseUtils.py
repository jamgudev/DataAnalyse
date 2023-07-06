# fileName contains the element in filterList, being taken.
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


def get_mean_of_list(data: []) -> float:
    if data:
        return float(np.mean(data))
    else:
        return 0.0


def get_standard_deviation_of_list(data: []) -> float:
    if data:
        return float(np.std(data))
    else:
        return 0.0


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


def get_standard_deviation_of_dic(dic: {}) -> []:
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
