#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
from git import *
import copy
import csv

#repo = Repo(r'C:\Users\Win\Desktop\ku\linux-stable')

def Regit(addr,version):
    repo=Repo(addr)
    git=repo.git
    data=git.log(version)
    return git,data

#git=repo.git
git,data=Regit(r'C:\Users\Win\Desktop\ku\linux-stable',-1000)#加载git库地址,加载数据

#data=git.log(['v4.4'])
#git.rev_parse('a561ce00b09e')

l=[]    #存储每项commit那一大段字符
length=6    #"commit"字符长度为6
count=0     #计数
a=True  #判断是否没有下一个commit了，即所有commit字符都已经找完

#按"commit "进行划分

while a:
    num=data.find("commit ",count)
    if num==-1:
        a=False
    else:
        l.append(num)
        count=num+length

i=0
com=[]
while i < len(l)-1:
    com.append(data[l[i]:l[i+1]])
    i+=1

com1=[]
for k in com:
    if k.find("Author:")==-1:
        pass
    else:
        dic={}
        dic['Origion']=k
        s=k.split('\n')
        s=[j for j in s if j !='' ]
        try:
            for i in s:
                if i.find("Author:") != -1:
                    email=i.find("<")
                    dic['Author']=i[8:email]
                    dic['Email']=i[email:]
                elif i.find("commit ") != -1:
                    dic['Commit']=i.split()[1][1:]
                elif i.find("Merge:") != -1:
                    dic['Merge']=i.split(':')[1][1:]
                elif i.find("Date:") != -1:
                    date=i[i.find(":")+1:]
                    dic['Date']=date[3:27]
                    dic['Area']=date[27:]
                elif i.find("Fixes:") != -1:
                    dic['Fixes']=i
                    try:
                        addr=i[11:]
                        fix=addr.split('(')[0]
                        dic['Addr']=fix[:-1].split()[0]
                        dic['Long']=git.rev_parse(dic['Addr'])
                        dic['Commit2']=git.log(dic['Addr'],-1)
                    except Exception as err:
                        print(err)
                        pass
                    try:
                        Com2=copy.copy(dic['Commit2'])
                        Com2li=Com2.split('\n')
                        for m in Com2li:
                            if m.find("Author:") != -1:
                                email2=m.find("<")
                                dic['Author2']=m[8:email2]
                                dic['Email2']=m[email2:]
                            elif m.find("commit ") != -1:
                                dic['Commit2_Com']=m.split()[1][1:]
                            elif m.find("Date:") != -1:
                                date2=m[m.find(":")+1:]
                                dic['Date2']=date2[3:27]
                                dic['Area2']=date2[27:]
                    except Exception as err:
                        print(err)
                        pass
                else:
                    try:
                        dic['Others']+= '/n'+i
                    except:
                        dic['Others']=i 
        except Exception as err:
            print(err,s)
            pass
        com1.append(dic)

headers = ['Origion','Commit','Merge','Author','Email','Date','Area','Fixes','Addr','Long','Commit2','Commit2_Com','Author2','Email2','Date2','Area2','Others']
with open('C:\\Users\\Win\\Desktop\\test2.csv', 'a+',newline='',encoding = 'gb18030')as f:
    f_csv = csv.DictWriter(f,headers)
    f_csv.writeheader()
    for i in com1:
        try:
            f_csv.writerow(i)
        except:
            try:
                i['Others']=i['Others'].encode('utf-8')
                f_csv.writerow(i)
            except:
                try:
                    i['Others']=i['Others'].replace(chr(0xa0),'')
                    i['Others']=i['Others'].encode('utf-8')
                    f_csv.writerow(i)
                except Exception as e:
                    print(e)
                    pass