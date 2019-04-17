# -*- coding: UTF-8-*-

"""
@Project: change osd
@Author: CheneyJin
@Time: 2018/7/11 13:26
"""

import sys
import datetime as dt
import math

input_file = ""
output_file = ""
stamp = 0
encode = "gb18030"
arrow: str = " --> "


# 将变更时间的大小改为秒级，多余的部分任然为纳秒
def mod_stamp(st):
    decimal, s = math.modf(st / 1000)
    n_s = int(round(decimal * 1000))
    return s, n_s


def anal_sub_time(string_time):
    t = string_time.split(",")
    sub_t = dt.datetime.strptime(t[0], '%H:%M:%S')
    # 时间戳的秒数和纳秒数
    ss, sns = mod_stamp(stamp)
    return t, sub_t, ss, sns


# 修改字幕显示的时间
def change_subtitle_stamp(string):
    sub = string.split(arrow)
    # 修正开始时间
    if plus:
        start_time = plus_time(sub[0])
        end_time = plus_time(sub[1])
    else:
        start_time = minus_time(sub[0])
        end_time = minus_time(sub[1])
    return start_time + arrow + end_time + "\n"


def minus_time(string_time):
    t, sub_t, stamp_s, stamp_nanos = anal_sub_time(string_time)
    nanos = int(t[1]) - stamp_nanos
    if nanos < 0:
        nanos = 999 - abs(nanos)
        sub_t = sub_t - dt.timedelta(seconds=int(stamp_s + 1))
    else:
        sub_t = sub_t - dt.timedelta(seconds=int(stamp_s))
    return str(sub_t.time()) + "," + str(nanos).zfill(3)


def plus_time(string_time):
    t, sub_t, stamp_s, stamp_nanos = anal_sub_time(string_time)
    nanos = int(t[1]) + stamp_nanos
    if nanos > 999:
        s, nanos = mod_stamp(nanos)
        sub_t = sub_t + dt.timedelta(seconds=int(stamp_s + s))
    else:
        sub_t = sub_t + dt.timedelta(seconds=int(stamp_s))
    return str(sub_t.time()) + "," + str(nanos).zfill(3)


def main():
    global file_object, writer
    index = 0
    try:
        file_object = open(input_file, encoding=encode)
    except IOError:
        print("file not found!")
        exit(0)
    new_srt = []
    lines = file_object.readlines()
    total = 0
    for i in reversed(lines):
        i = i.strip()
        if i.isdigit():
            total = int(i)
            break
    for line in lines:
        # 判断当前行是不是时间戳
        if line.startswith("0") and line.find(arrow):
            line = change_subtitle_stamp(line)
            index = index + 1
            progress(index, total)
        new_srt.append(line)
    file_object.close()
    try:
        writer = open(output_file, 'w', encoding=encode)
    except IOError:
        print("file can not be created!")
        exit(0)
    writer.write(''.join(new_srt))
    writer.close()
    progress(index, total)


def progress(i, t):
    percent = int((i / t) * 100)
    thunk = int(percent / 4)
    sys.stdout.write('▉' * thunk + '%d%%\r' % percent)
    sys.stdout.flush()


if __name__ == "__main__":
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print('''params not correct!
        params should accord with follows details:
        1. input file name.
        2. output file name.
        3. stamp, this is nanosecond, it used to change the time of subtitle display.
        4. file content encoding, such as 'gb18030','gbk','utf-8'...
        \n
        e.g.: python changeosd.py input.srt out.srt 300 gb18030
        i.e.: this util will make subtitle move forward by 300 nanoseconds. 
            if 300 become -300 that means move backward.''')
        exit()
    input_file = sys.argv[1]
    if len(input_file) <= 0:
        print("input file name is null!")
        exit(0)
    output_file = sys.argv[2]
    if len(output_file) <= 0:
        print("output file name is null!")
        exit(0)
    stamp_string = sys.argv[3]
    if not stamp_string.lstrip('-').isdigit():
        print("stamp is a number, one second is 1000!")
        exit(0)
    else:
        stamp = int(stamp_string)
        if stamp < -10000:
            print("warning: subtitle will move back more than 10 seconds.")
        plus = stamp > 0
        stamp = abs(stamp)
    if len(sys.argv) == 4:
        print("using default encode 'gb18030'. ")
    else:
        input_encode = sys.argv[4]
    main()
