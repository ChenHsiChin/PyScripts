# 导入python内置的os模块和sys模块
import os
import sys

zero = ["", "0", "00", "000"]
# 程序入口
if __name__ == "__main__":
    old_names = os.listdir()
    # 遍历目录下的文件名
    for old_name in old_names:
        # 跳过本脚本文件
        if old_name != sys.argv[0]:
            # 用新的文件名替换旧的文件名
            onarr = old_name.split('.')
            onlen = len(onarr[0])
            os.rename(old_name, zero[4 - onlen] + old_name)
