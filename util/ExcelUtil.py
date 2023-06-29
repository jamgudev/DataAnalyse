import os.path

import pandas as pd


def write_to_excel(data: [], outDir: str, fileName: str):
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    detailUsageDF = pd.DataFrame(data)
    detailUsageDF.to_excel(outDir + fileName, header=None, index=None)