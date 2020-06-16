#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
"""
Firstly, we manually found all the versions in the level of 3.x,4.x,5.x, then we use git tag
to grab all the sorted subversions for every 3.x,4.x,5.x. After looking at the commit time,
our group use weeks as time units. In this file, in the function create_dataframe(), the
commit time of v3.0-rc1 is used as base time, we will plot the graph with all versions.
However, the graph is messy because there are too many versions. Therefore, we plot other
three graphs for separated 3.x versions(v3.0-rc1 as base time),4.x versions(v4.0-rc1 as
base time) and v5.x versions(v5.0-rc1). And store the three dataframe into separated files.

Something to explain
1. The reason for choosing v3.0-rc1 as base time is that the time of v3.0-rc1 is the earliest
released version in v3.x, after checking the time (for v3.0,v3.0-rc1 and so on).
2. At first, we use days as time units, but this will make the timeline too long, the graph
cannot show the useful trend, And after trying using weeks and months as units, finally we
decided use weeks, because the graph using weeks is smoother(when using months, some versions
may have the same month, so the graph have straight lines, not show the details thoroughly).
3.There are too many yticks, showing them will mess up the graph(and we even cannot see the
version clearly), so we will not show them in the ylabel
"""

__author__ = "Group03"
__copyright__ = "Copyright 2019, OpenTech Research"
__credits__ = ["Group03"]
__version__ = "1"
__maintainer__ = "Linux maintainer"
__email__ = "zhaizhy18@lzu.edu.com"
__status__ = "Experimental"

import matplotlib
# Ubuntu in windows install without GUI, this just to make sure the graph can be plotted in Ubuntu without exceptions
matplotlib.use('Agg')
import sys
import matplotlib.pyplot as plt
import subprocess
import pandas as pd


class ContentException(BaseException):
    def __str__(self):
        wrong = 'Find nothing, please check your git and the address!'
        return wrong


class PlotVersionHour:

    def __init__(self):
        version3 = ["v3." + str(x) for x in range(20)]  # v3.0-v3.19
        version4 = ["v4." + str(x) for x in range(21)]  # v4.0-v4.20
        version5 = ["v5." + str(x) for x in range(7)]  # v5.0-v5.6
        self.all_version = version3 + version4 + version5
        self.versionlist = []
        self.count = 0
        self.week_x = []
        self.subversion_y = []
        self.main()

    def sorted_version(self):  # using git tag command to get sorted version
        for version in self.all_version:
            getversion = "git tag | grep " + version + " | sort -n -k3 -t\".\""
            get_version = subprocess.Popen(getversion, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
            self.subversion = get_version.communicate()[0]
            for line in self.subversion.decode("utf-8").split("\n"):  # do nothing for the empty string
                if line == '':
                    break
                self.versionlist.append(line)
        return self.versionlist

    def get_base_time(self, v):  # get the base time for v3.0, v4.0, v5.0
        gettimestamp = "git log -1 --pretty=format:\"%ct\" " + v
        get_time = subprocess.Popen(gettimestamp, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
        self.basetime = int(get_time.communicate()[0].decode())

    def get_version_week(self, git_cmd, base):  # choose weeks as time units

        try:
            seconds = git_cmd.communicate()[0]
            secperweek = 3600*24*7
            if seconds == 0:
                raise ContentException
        except ContentException as err:
            print(err)
            sys.exit(2)

        return (int(seconds) - base) // secperweek

    def store_csv(self):  # store the dataframe in csv file
        self.df.to_csv("Test.csv", encoding="utf-8-sig", mode="a", header=True, index=True)
        return 'Test.csv'

    def create_dataframe(self):  # calculate the time for each version and store them into dataframe and set the index
        self.df = pd.DataFrame(columns=('weeks', 'all versions'))
        self.sorted_version()
        for subversion in self.versionlist:
            self.get_base_time('v3.0-rc1')
            gittag = "git log -1 --pretty=format:\"%ct\" " + subversion
            git_tag_week = subprocess.Popen(gittag, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
            weeks = self.get_version_week(git_tag_week, self.basetime)
            self.count += 1
            self.df = self.df.append([{'count': self.count, 'weeks': weeks, 'all versions': subversion}], ignore_index=True)
        self.df = self.df.set_index("count")

    def main(self):  # read the csv file and plot the graph for all versions
        self.create_dataframe()
        file = self.store_csv()
        df = pd.read_table(file, sep=',')  # read csv file with comma separator
        for i in range(1, df.index[-1]+2):  # put two elements with the same row into list of x_axis and y_axis
            week_ele = self.df.loc[i, 'weeks']
            subversion_ele = self.df.loc[i, 'all versions']
            self.week_x.append(week_ele)
            self.subversion_y.append(subversion_ele)
        # plot the line chart to show the relation between versions and weeks
        plt.plot(self.week_x, self.subversion_y)
        plt.yticks([])  # too many yticks so we will not show them in the graph
        plt.title("development of v3.x, v4.x, v5.x versions over weeks")
        plt.ylabel("all sorted versions of v3.x, v4.x, v5.x")
        plt.xlabel("weeks")
        plt.savefig("weeks_versions.png")
        plt.clf()


if __name__ == '__main__':
    plottime = PlotVersionHour()

