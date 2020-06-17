#!/usr/bin/env python3
# -*- coding:UTF-8 -*-

"""
This file try to verify or falsify the hypothesis1 using the pattern (- many file
changed, - many changes added == removed, - some added > removed).

In this file, the parameter for added==removed is 0.5(means in all file changes,
50 percent changes are added==removed) and using logical operator "and" to join
two conditions. However, in actual situation, we try different parameters and not
only using "and" operator(for data given in class, we use "and", for data found by
our group, we analyze two conditions separately). The results of different parameters
are stored in conclusion.txt.
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


class DiffCollect:
    def __init__(self, begin, totalnum):
        self.begin = begin  # version to start with
        self.totalnum = totalnum  # total number of versions to check
        self.end = self.begin + self.totalnum
        self.add = 0
        self.remove = 0
        self.numfile = 0
        self.refactorlist = []
        self.filename = []
        self.count = 0

    def get_num_changes(self, start, end):  # three info are shown by git diff, lines add,lines removed,filename
        getchanges = 'git diff --numstat HEAD~' + str(start) + '..HEAD~' + str(end)
        get_changes = subprocess.Popen(getchanges, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
        self.changes = get_changes.communicate()[0]  # grab the output in binary
        return self.changes

    def store_csv(self, order):  # store the dataframe of every commit diff into csv file
        filename = "commit_diff_" + str(order) + ".csv"
        # store csv file into a folder
        self.df.to_csv('/home/baobaozzy/project/linux-stable/test/' + filename, encoding="utf-8-sig", mode="a", header=True, index=True)
        return filename

    def create_df(self):
        for version in range(self.begin, self.end):  # iterate all target versions
            self.df = "df_" + str(version)  # create dataframe for different versions
            self.df = pd.DataFrame(columns=('add', 'remove', 'filename'))  # create the dataframe with three columns
            end_version = version + 1
            gitnum = self.get_num_changes(version, end_version)
            # self.linesadd.append("HEAD~" + str(version) + '..HEAD~' + str(end_version))  # git diff between two commits
            for line in gitnum.decode("UTF-8").split("\n"):  # split every diff record in one git diff
                if line == '':  # if the record is null, out of the loop
                    break
                part1,part2,part3 = line.split("\t", 2)  # put three elements of one record into dataframe
                # add these info into columns

                self.filename.append(part3)
                length = len(self.filename)
                for i in range(length):  # using the number of files to create the index
                    self.count = i
                self.df = self.df.append([{'count': self.count, 'add': part1, 'remove': part2, 'filename': part3}], ignore_index=True)
            self.filename = []
            self.df = self.df.set_index("count")
            self.store_csv(str(version) + "..." + str(end_version))

    def get_refactor(self):  # using the pattern to select the refactor file
        self.create_df()
        for start in range(self.begin, self.end):  # the range for comparing file
            equal = 0
            add_more_del = 0
            del_more_add = 0
            end = start + 1
            file = "commit_diff_" + str(start) + '...' + str(end) + ".csv"
            df = pd.read_table(file, sep=',')  # read the csv file
            if df.index[-1] == 0:  # our target is multiple file changes, not one
                pass
            else:
                for i in range(df.index[-1]+1):  # compare the number of linesadd and linesremove within one record
                    if df.loc[i, 'add'] == df.loc[i, 'remove']:  # linesadd == linesremove
                        equal += 1
                    elif df.loc[i, 'add'] > df.loc[i, 'remove']:  # linesadd > linesremove
                        add_more_del += 1
                    elif df.loc[i, 'add'] < df.loc[i, 'remove']:   # linesadd < linesremove
                        del_more_add += 1
                if equal >= int(df.index[-1] + 1)*0.5 and add_more_del > del_more_add:  # the pattern
                    self.refactorlist.append('HEAD~' + str(start) + '...' + 'HEAD~' + str(end))
                else:
                    pass


if __name__ == '__main__':
    refactor_list = DiffCollect(100, 100)
    refactor_list.get_refactor()
