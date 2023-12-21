from alive_progress import alive_bar

from analyse.graph.GrapgNameSapce import SS_SESSION_NIS_CONSUMPTION_IDX, SS_SESSION_TOTAL_CONSUMPTION_IDX, GRAPH_user_nis_consumption
from analyse.graph.base.__EveryDayAnalyseFromOutput import iter_idx_data_from_file_in_every_day
from analyse.init_analyse.power_params import PowerParamsUtil
from analyse.util.AnalyseUtils import get_all_user_name_from_dir
from analyse.util.FilePathDefinition import EXCEL_SUFFIX, TEST_OUTPUT_FILE, EXPORT_SESSION_SUMMARY
from util import JLog, ExcelUtil


# 不同元部件在不同用户各自的功耗占比分布
def user_NIS_consumption():
    dirName = TEST_OUTPUT_FILE
    allUserName = get_all_user_name_from_dir(dirName)
    if allUserName:
        allUserData = []
        brandData = {}
        with alive_bar(len(allUserName), ctrl_c=True, force_tty=True, title=f'分析进度') as bar:
            for user_idx, userName in enumerate(allUserName):
                brand = PowerParamsUtil.get_phone_brand_by_user_name(userName)
                if brand == "":
                    bar()
                    continue
                nisConsumption = 0.0
                totalConsumption = 0.0
                dataOfEveryDay = iter_idx_data_from_file_in_every_day(dirName, userName,
                                                                      EXPORT_SESSION_SUMMARY + EXCEL_SUFFIX,
                                                                      [SS_SESSION_NIS_CONSUMPTION_IDX,
                                                                       SS_SESSION_TOTAL_CONSUMPTION_IDX])
                if isinstance(dataOfEveryDay, dict):
                    # 遍历每天数据
                    for idx, data in enumerate(dataOfEveryDay.values()):
                        try:
                            # 遍历一天中的所有数据
                            for session_id, session_nis_consumption in enumerate(data[0]):
                                nisConsumption += float(session_nis_consumption)
                                totalConsumption += float(data[1][session_id])
                        except Exception as e:
                            JLog.e("user_NIS_consumption",
                                   f"error: userName:{userName}, idx[{idx}], data:{data}, e:{e}")
                userData = [userName, brand, nisConsumption, totalConsumption, nisConsumption / totalConsumption]
                if brand in brandData:
                    usersData = brandData[brand]
                else:
                    usersData = {}
                usersData[userName] = userData
                brandData[brand] = usersData
                bar()

            user_idx = 1
            for brand in brandData:
                usersData = brandData[brand]
                for user_name in usersData.keys():
                    user_data = usersData[user_name]
                    allUserData.append([str(user_idx)] + user_data[:])
                    user_idx += 1

            allUserData.insert(0, ["用户ID", "用户名", "手机型号", "NIS总功耗", "总功耗", "消耗的功耗占比"])
            ExcelUtil.write_to_excel(allUserData, dirName,
                                     GRAPH_user_nis_consumption)


user_NIS_consumption()
