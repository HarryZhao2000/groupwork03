#!/usr/bin/env python3
# -*- coding:UTF-8 -*-

"""
This file is taking the output of subprocess pipe into a dataframe and then store dataframe into csv file

Default start version is v4.4, and default number of lasting is 1, so the range will be v4.4..v4.5.
The dataframe will have four columns: commit_message, filename, total_change, change_details, and be stored
in output.csv file
"""

__author__ = "Group03"
__copyright__ = "Copyright 2019, OpenTech Research"
__credits__ = ["Group03"]
__version__ = "1"
__maintainer__ = "Linux maintainer"
__email__ = "zhaizhy18@lzu.edu.com"
__status__ = "Experimental"

import subprocess
import pandas as pd


class LogCollect:
    def __init__(self, start=4.4, num=1):
        self.start = start
        self.num = num
        self.end = self.start + self.num*0.1

    def store_csv(self):  # store the dataframe of every commit diff into csv file
        self.df.to_csv('Output.csv', encoding="utf-8-sig", mode="a", header=True, index=True)
        return 'Output.csv'

    def get_changes(self):
        start_version = 'v' + str(self.start)
        end_version = 'v' + str(self.end)
        gitcmd = 'git log --stat --oneline --follow ' + start_version + '..'+ end_version +' kernel/sched/core.c'
        git_cmd = subprocess.Popen(gitcmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
        self.changes= git_cmd.communicate()[0]  # grab the output in binary
        return self.changes

    def main(self):
        self.get_changes()
        count = 0
        row = []
        output = []
        for line in self.changes.decode("utf-8").split("\n"):
            part=line.split('|')
            for i in range(len(part)):
                ele = part[i]
                row.append(ele)
            count += 1
            if count == 3:
                output.append(row)
                row=[]
                count = 0
        self.df = pd.DataFrame(output)
        self.df.columns=['commit', 'filename', 'total_change', 'change_details']
        self.store_csv()


if __name__ == '__main__':
    example = LogCollect()
    example.main()
