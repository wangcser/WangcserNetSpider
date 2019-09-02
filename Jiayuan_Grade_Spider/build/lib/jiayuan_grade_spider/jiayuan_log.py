from jiayuan_grade_spider.jiayuan_time_stamp import current_time


def spider_log(log_data):
    # log spider info into txt.
    time_stamp = current_time('sec')
    f = open("E:/user_grade/user_grade_log.txt", "a")

    f.write("spider (" + time_stamp + " ): " + log_data + "\n")
    f.close()
    pass


