import time


def current_time(type='sec'):

    # 数字显示格式化
    t = time.localtime()
    if t.tm_hour < 10:
        hour = '0' + str(t.tm_hour)
    else:
        hour = str(t.tm_hour)
    if t.tm_min < 10:
        min = '0' + str(t.tm_min)
    else:
        min = str(t.tm_min)
    if t.tm_sec < 10:
        sec = '0' + str(t.tm_sec)
    else:
        sec = str(t.tm_sec)

    if type == 'sec':
        time_stamp = str(t.tm_mon) + "." + str(t.tm_mday) + " " + hour + ":" + min + ":" + sec
        return time_stamp
    elif type == 'min':
        time_stamp = str(t.tm_mon) + "." + str(t.tm_mday) + " " + hour + ":" + min
    elif type == 'file_name':
        time_stamp = str(t.tm_mon) + "." + str(t.tm_mday) + " " + hour + "." + min
        return time_stamp
    else:
        time_stamp = 'no time stamp'
        return time_stamp