import os.path

import pandas as pd

io = "./depart_test_case/input/all.xlsx"  # 目标文件
data = pd.read_excel(io, header=None)

rows = data.shape[0]  # 获取行数 shape[1]获取列数
cols_list = []
test_rows = []
training_rows = []

for i in range(rows):
    temp = data.iloc[i]

    if len(temp) == 0:
        continue

    if (i % 4) == 0:
        test_rows.append(temp)
    else:
        training_rows.append(temp)

# 输出test数据
outDir = "./depart_test_case/output/"
testDir = outDir + "all_test.xlsx"
trainDir = outDir + "all_train.xlsx"
print(testDir)
print(trainDir)
if not os.path.exists(outDir):
    os.makedirs(outDir)
testDF = pd.DataFrame(test_rows)
testDF.to_excel(testDir, header=None, index=False)
trainDF = pd.DataFrame(training_rows)
trainDF.to_excel(trainDir, header=None, index=False)
