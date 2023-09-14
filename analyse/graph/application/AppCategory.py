import os

import pandas as pd
from pandas import DataFrame

from analyse.graph.GrapgNameSapce import GRAPH_app_usage_in_all_users, GRAPH_app_categories
from analyse.util.FilePathDefinition import TEST_OUTPUT_FILE
from util import ExcelUtil


def export_app_category():
    # 读取Excel文件
    dirName = TEST_OUTPUT_FILE + "/" + GRAPH_app_usage_in_all_users
    df = ExcelUtil.read_excel(dirName)[1:]

    all_unique_app_name = df.iloc[:, 1].unique()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    categoriesFilePath = current_dir + "/" + GRAPH_app_categories
    if not (os.path.exists(categoriesFilePath)):
        oldDf = DataFrame()
    else:
        oldDf = ExcelUtil.read_excel(categoriesFilePath)

    oldAppPkgNames = list(oldDf.iloc[:, 0])
    oldAppCategories = list(oldDf.iloc[:, 1])
    oldAppNames = list(oldDf.iloc[:, 2])
    exportCategoryData = []
    for newAppName in list(all_unique_app_name):
        if newAppName in oldAppPkgNames:
            index = oldAppPkgNames.index(newAppName)
            exportCategoryData.append([newAppName, oldAppCategories[index], oldAppNames[index]])
        else:
            exportCategoryData.append([newAppName])

    rows = df.shape[0]
    categoriesData = []
    for row in range(rows):
        appPkgName = df.iloc[row, 1]
        if appPkgName in oldAppPkgNames:
            index = oldAppPkgNames.index(appPkgName)
            categoriesData.append(oldAppCategories[index])
        else:
            raise ValueError(f"pkgName: {appPkgName} has not yet been classified.")
    # 将分类添加到GRAPH_app_usage_in_all_users文件中
    df['app分类'] = categoriesData

    # 插入headers
    headers = ["用户名", "用户使用的app名", "用户在该App停留多长时间", "app的分类"]
    # 将列表转换为DataFrame
    new_row_df = pd.DataFrame([headers], columns=df.columns)
    # 使用 concat 方法将新行数据插入到原始 DataFrame 的顶部
    df = pd.concat([new_row_df, df], ignore_index=True)
    df.to_excel(dirName, index=False, header=False)

    # 备份
    exportCategoryData.insert(0, ["包名", "所属分类", "app名"])
    ExcelUtil.write_to_excel(exportCategoryData, current_dir, GRAPH_app_categories)
    ExcelUtil.write_to_excel(exportCategoryData, TEST_OUTPUT_FILE, GRAPH_app_categories)

    return

