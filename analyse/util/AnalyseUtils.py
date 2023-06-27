# fileName contains the element in filterList, being taken.
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
