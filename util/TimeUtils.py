import datetime
import time

from util import JLog

__TAG = "TimeUtils"


# 支持这两种格式的字符串时间比较:
# 20230405(17_34_11_713), 20230405(17_34_11)
# return 大于0 表 time_a 比 time_b 要大
def compare_time(time_a: str, time_b: str) -> int:
    timeMillsPattern = '%Y%m%d(%H_%M_%S_%f)'
    secondPattern = '%Y%m%d(%H_%M_%S)'

    tryStartTime = time_a
    tryEndTime = time_b
    try:
        tryStartTime = time.mktime(time.strptime(time_a, timeMillsPattern))
    except ValueError:
        tryStartTime = time.mktime(time.strptime(time_a, secondPattern))
    finally:
        time_a = tryStartTime

    try:
        tryEndTime = time.mktime(time.strptime(time_b, timeMillsPattern))
    except ValueError:
        tryEndTime = time.mktime(time.strptime(time_b, secondPattern))
    finally:
        time_b = tryEndTime

    return int(time_a) - int(time_b)


# result = compare_time('20230405(17_34_2)', '20230405(17_34_3_713)')
# print('the compare result is:', result)

# 满足 '%Y%m%d(%H_%M_%S_%f)' 格式, temp second
def time_duration_with_mills(end_time: str, start_time: str) -> int:
    timeMillsPattern = '%Y%m%d(%H_%M_%S_%f)'
    tryStartTime = end_time
    tryEndTime = start_time
    try:
        tryStartTime = time.mktime(time.strptime(end_time, timeMillsPattern))
    except ValueError as e:
        JLog.e(__TAG, str(e))
    finally:
        end_time = tryStartTime

    try:
        tryEndTime = time.mktime(time.strptime(start_time, timeMillsPattern))
    except ValueError as e:
        JLog.e(__TAG, str(e))
    finally:
        start_time = tryEndTime

    return int(end_time) - int(start_time)


def get_today_of_date() -> str:
    today = datetime.date.today()
    return today.strftime("%Y%m%d")


def get_day_of_date_str(date: str) -> str:
    supportLen = len(get_today_of_date())
    if (not isinstance(date, str)) or len(date) < supportLen:
        JLog.e(__TAG, f"compare_is_same_day failed, len of time_a[{date}] not longer than {supportLen}.")
        return ""
    else:
        return date[0:supportLen]


# 传进来的时间字符串格式至少为20170203，否则会返回false，甚至报格式错误
# print(compare_is_same_day("20170203(17_24_39)", "2017020"))
def compare_is_same_day(time_a: str, time_b: str) -> bool:
    # 获取一般日期的长度
    supportLen = len(get_today_of_date())
    if (not isinstance(time_a, str)) or len(time_a) < supportLen \
            or (not isinstance(time_b, str)) or len(time_b) < supportLen:
        JLog.e(__TAG, f"compare_is_same_day failed, len of time_a[{time_a}] or time_b[{time_b}] not longer than {supportLen}.")
        return False

    a = time_a[0:supportLen]
    b = time_b[0:supportLen]
    pattern = '%Y%m%d'

    return time.mktime(time.strptime(a, pattern)) == time.mktime(time.strptime(b, pattern))


