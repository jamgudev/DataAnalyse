import os.path

import pandas as pd
from pandas import DataFrame

from util import JLog

__TAG = "ExcelUtil"


def write_to_excel(data: [], outDir: str, fileName: str):
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    detailUsageDF = pd.DataFrame(data)
    detailUsageDF.to_excel(os.path.join(outDir, fileName), header=None, index=None)


# skipOrThrow: 1, skipped(default), 2, throws when error
def read_excel(path: str, skipOrThrow: int = 1) -> DataFrame:
    if not (os.path.exists(path)):
        JLog.e(__TAG, f"file[{path}] does not exist!")
        if skipOrThrow == 1:
            return DataFrame()
        elif skipOrThrow == 2:
            raise RuntimeError(f"file[{path}] does not exist!, throws error")
    return pd.read_excel(path, header=None)
