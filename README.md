#### 模型训练
1. 用HV POWER MONITOR设备连接改装好后的手机，在手机上安装HWStatistic软件，
分参数收集训练样本，比如收集屏幕参数的训练样本，就在收集数据期间，只改变屏幕亮度（收集两次，一次为屏幕最大值，一次为最小值，一次大概200秒）
2. 所有参数的样本都收集好后，筛选出变化稳定的数据，每个参数筛选相同数量的样本（最少200秒每样本），
将筛选好后的样本汇总成一个xlsx文件，放入到本工程的/depart_test_case/input/目录下，运行DepartTestCase脚本，将原始数据分成训练样本跟测试样本。
3. 将训练样本跟测试样本，放到matlab工程中的以下路径，运行exc.m，得到合适的模型参数
    ```text
   # all_train为训练样本 
   filename = 'files/test/all_train.xlsx';
   # all_test为测试样本 
   verifyFile = 'files/test/all_test.xlsx';
    ```
4. 模型准确率满意后，模型系数会输出到matlab工程的/out/params_mat.csv文件中，这时候需要手动将.csv文件中的数据拷贝到一个新建的.xlsx文件内
并调整csv文件中第V列数据的位置，将第V列数据插入到第M列之后（将bluetooth的系数，调整到CPU系数之前），然后保存新建的.xlsx文件，命名为params_mat.xlsx
   > 为什么要调位置？因为ParseActiveData.py在做数据分析的时候，问在合并HWS收集到的所有power_usage_data.xlsx数据之前，对数据进行调位，方便后续的数据分析。
   > 详情请看ParseActiveData#merge_all_power_data()方法。
5. 记住训练手机的型号（比如p50pro），并将对应型号的params_mat.xlsx文件保存到本工程的/analyse/init_analyse/power_params/p50pro/目录下（已有则覆盖）。
下一步，检查/p50pro上一级目录/power_params/下的params_list.xlsx文件，看p50pro型号对应的手机号是否注册正确，params_list里注册的型号，需与外部的型号目录名完全一致
#### 数据预分析
6. 能耗系数文件准备好后，就可以执行脚本进行数据预分析。
    - 将原始数据拷贝到本工程的analyse/test/input/目录下
    - 执行/analyse/init_analyse/Analyse.py脚本，默认6进程并发执行数据分析，如果需要调试，则切换为单线程运行模式进行断点。
    - 数据分析结束后，分析结果文件会存储在/analyse/test/output/目录下
    - 如果需要改动数据分析脚本，建议将一部分数据拷贝到/analyse/input/目录下，并修改/analyse/init_analyse/Analyse.py目录中的环境路径
      为INPUT_FILE，最终调试的结果文件会存储在/analyse/output/目录中。
#### 图表分析
7. 数据预分析结果最终会存在output目录下，下一步进行图表分析，执行对应的图表分析脚本。
   - 比如进行用户行为的图表分析，进到/analyse/graph/interaction/目录下
   - 执行某个图表分析脚本，比如ISCDF.py，确保脚本内的数据源路径正确
   - 也就是确认这个路径 dirName = TEST_OUTPUT_FILE，是否指向了数据预分析的output目录。
   - ISCDF.py执行完后，会生成图表展示所需的数据，该数据的路径已经被定义好，一般无需修改，直接执行同目录下/draw/ISCDFDraw.py脚本
   - 脚本执行完后，就会有图表呈现出来。
