import pandas as pd


def write_to_excel(data: [], outPath: str):
    detailUsageDF = pd.DataFrame(data)
    detailUsageDF.to_excel(outPath, header=None, index=None)