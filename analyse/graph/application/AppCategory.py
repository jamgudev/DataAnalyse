import os

import pandas as pd
from pandas import DataFrame

from analyse.graph.GrapgNameSapce import GRAPH_app_usage_in_all_users, GRAPH_app_categories
from util import ExcelUtil


def export_app_category(dirName: str):
    # 读取Excel文件
    filePath = dirName + "/" + GRAPH_app_usage_in_all_users
    df = ExcelUtil.read_excel(filePath)[1:]

    all_unique_app_name = df.iloc[:, 1].unique()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    categoriesFilePath = current_dir + "/" + GRAPH_app_categories
    if not (os.path.exists(categoriesFilePath)):
        oldDf = DataFrame()
    else:
        oldDf = ExcelUtil.read_excel(categoriesFilePath)[1:]

    oldAppPkgNames = list(oldDf.iloc[:, 0])
    oldAppCategories = list(oldDf.iloc[:, 1])
    oldAppNames = list(oldDf.iloc[:, 2])
    newCategoryData = []
    for newAppName in list(all_unique_app_name):
        if newAppName not in oldAppPkgNames:
            newCategoryData.append([newAppName, "", ""])

    rows = df.shape[0]
    cols = df.shape[1]
    if cols < 4:
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
    df.to_excel(filePath, index=False, header=False)

    # 备份
    newCategoryData.insert(0, ["包名", "所属分类", "app名"])
    newCategoryData.extend(oldDf.values)
    ExcelUtil.write_to_excel(newCategoryData, current_dir, GRAPH_app_categories)
    ExcelUtil.write_to_excel(newCategoryData, dirName, GRAPH_app_categories)

    return


def get_app_category_dict(dirName: str) -> dict:
    path = dirName + "/" + GRAPH_app_categories
    if not (os.path.exists(dirName + "/" + GRAPH_app_categories)):
        # 定义源文件路径和目标文件路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = current_dir + "/" + GRAPH_app_categories
    categoryDf = ExcelUtil.read_excel(path)[1:]
    rows = categoryDf.shape[0]
    categoryDict = {}
    for row in range(rows):
        pkgName = categoryDf.iloc[row, 0]
        appCategory = categoryDf.iloc[row, 1]
        categoryDict[pkgName] = appCategory

    return categoryDict


def get_app_category(dirName: str, pkgName: str, appCategoryDict: dict = None) -> str:
    if appCategoryDict is None:
        appCategoryDict = get_app_category_dict(dirName)
    if pkgName in appCategoryDict:
        return appCategoryDict[pkgName]
    else:
        raise ValueError(f"pkgName:{pkgName} has not yet been classified.")


def get_all_app_categories(dirName: str) -> list:
    path = dirName + "/" + GRAPH_app_categories
    if not (os.path.exists(dirName + "/" + GRAPH_app_categories)):
        # 定义源文件路径和目标文件路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = current_dir + "/" + GRAPH_app_categories
    categoryDf = ExcelUtil.read_excel(path)[1:]
    return list(categoryDf.iloc[:, 1].unique())
