from analyse.util.FilePathDefinition import POWER_PARAMS_LIST
from util import ExcelUtil


def get_phone_brand_dir_dict() -> dict:
    paramsListDF = ExcelUtil.read_excel(POWER_PARAMS_LIST)
    if len(paramsListDF) == 0:
        raise FileNotFoundError(f"filePath:[{POWER_PARAMS_LIST}] not found.")
    else:
        rows = paramsListDF.shape[0]
        paramsDict = {}
        for row in range(rows):
            userName = paramsListDF.iloc[row, 0]
            paramsDirName = paramsListDF.iloc[row, 1]
            paramsDict[str(userName)] = paramsDirName

        return paramsDict


def get_phone_brand_by_user_name(user_name: str) -> str:
    paramsDict = get_phone_brand_dir_dict()
    if user_name in paramsDict:
        return paramsDict[user_name]
    else:
        # raise ValueError(f"user_name:[{user_name}] has not been registered in file:[{POWER_PARAMS_LIST}]")
        return ""

