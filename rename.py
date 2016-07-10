# coding=utf-8
__author__ = 'CheneyJin'

import sys
import os
import traceback


class PyRenameFiles(object):
    file_path = os.getcwd()
    file_list = list(os.listdir(file_path))
    index = 0
    default_used = 0
    custom_used = 0
    skip_used = 0
    command_default = "-d"
    command_custom = "-c"
    command_skip = "-s"
    s_name = []
    usr_input_list = []
    skip_name_list = []
    py_rename_files = str(sys.argv[0]).split('/')[-1].split('.')[0]

    def judge_command(self, input_value):
        input_value.remove(input_value[0])
        if len(self.file_list) == 1:
            help_info(1)
            return
        for every_item in input_value:
            if str(every_item) == self.command_default:
                self.default_used += 1
            elif str(every_item) == self.command_custom:
                self.custom_used += 1
            elif str(every_item) == self.command_skip:
                self.skip_used += 1
            else:
                if self.default_used >= 1 \
                        and self.custom_used >= 1:
                    help_info(2)
                    return
                if self.skip_used > 1:
                    help_info(2)
                    return
                if self.default_used < 1 \
                        and self.custom_used < 1 \
                        and self.skip_used < 1:
                    help_info(2)
                    return
            self.usr_input_list.append(every_item)
        if len(self.usr_input_list) == 0:
            help_info(0)
            return
        elif len(self.usr_input_list) == 1 \
                and (self.usr_input_list[0] == self.command_custom
                     or self.usr_input_list[0] == self.command_skip):
            help_info(2)
            return
        elif self.custom_used == 1 and len(self.usr_input_list) == 1:
            help_info(2)
            return
        else:
            self.make_name()
        self.start_rename(self.s_name)

    @staticmethod
    def split_name(parent_str, sub_str):
        f_len = len(sub_str)

        def position():
            for i, c in enumerate(parent_str):
                if c == sub_str[0] \
                        and parent_str[i:i+f_len] == sub_str:
                    yield i

        before_pos = 0
        sub_cus_name = []
        for sub_item in list(position()):
            sub_cus_name.append(parent_str[before_pos:sub_item])
            before_pos = sub_item + 4
        sub_cus_name.append(parent_str[before_pos:])
        return sub_cus_name

    def make_name(self):
        if self.command_skip in self.usr_input_list:
            pos_s = self.usr_input_list.index(self.command_skip)
            if pos_s != 0:
                if self.custom_used == 1 and pos_s == 2:
                    self.s_name = self.split_name(self.usr_input_list[1], "_%d_")
                    self.skip_name_list = self.usr_input_list[3:]
                else:
                    self.skip_name_list = self.usr_input_list[2:]
            else:
                if self.default_used == 1:
                    pos_default = self.usr_input_list.index(self.command_default)
                    self.skip_name_list = self.usr_input_list[1:pos_default]
                elif self.custom_used == 1:
                    pos_custom = self.usr_input_list.index(self.command_custom)
                    self.s_name = self.split_name(self.usr_input_list[pos_custom + 1], "_%d_")
                    self.skip_name_list = self.usr_input_list[1:pos_custom]
                else:
                    self.skip_name_list = self.usr_input_list[1:]
        else:
            if self.custom_used == 1:
                self.s_name = self.split_name(self.usr_input_list[1], "_%d_")

    def start_rename(self, s_name):
        if len(self.file_list) == 0:
            return
        file_item = self.file_list[0]
        if file_item.split('.')[0] != self.py_rename_files:
            if file_item not in self.skip_name_list:
                self.index += 1
                if len(s_name) >= 1:
                    temp_s_name = list(s_name)
                    for i in range(len(s_name) - 1):
                        temp_s_name[i] += str(self.index)
                    if len(file_item.split('.')) <= 1:
                        new_name = ''.join(temp_s_name)
                    else:
                        new_name = ''.join(temp_s_name) + '.' + file_item.split('.')[-1]
                    del temp_s_name[:]
                else:
                    if len(file_item.split('.')) <= 1:
                        new_name = str(self.index)
                    else:
                        new_name = str(self.index)+'.'+file_item.split('.')[-1]
            else:
                new_name = file_item

            try:
                os.rename(file_item, new_name)
                # print (file_item + ' => ' + new_name)
            except WindowsError:
                self.index -= 1
                print("WindowsError")
                print(traceback.format_exc()+"\nfile_item = "+file_item+"\nnew_name = "+new_name+"")
        self.file_list.remove(file_item)
        self.start_rename(self.s_name)


def help_info(help_value):
    print \
        """
        The command:
        1.default           Giving every file in this directory
                            with a meaningless name.

        2.custom            Naming the file like "custom_%d_".
                            e.g. -c custom_%d_   -c cus_%d_tom
                            The name will like custom1,custom2
                                            or cus1tom,cus2tom

        *.use skip          e.g. -s example.txt
                            or -d -s example1.txt example2.txt
                            or -c custom_%d_ -s example1.txt...
                            or -s example1.txt -d/-c custom_%d_
                            Then the example.txt will not be
                            changed.
        """
    if help_value == 0:
        print "Nothing input."
    if help_value == 1:
        print "There is only rename.py in this directory."
    if help_value == 2:
        print "Command error."


def main():
    PyRenameFiles().judge_command(sys.argv)

if __name__ == '__main__':
    main()
    print("Finish.")
