#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
from git import *
import copy
import csv

#repo = Repo(r'C:\Users\Win\Desktop\ku\linux-stable')
class gitOp(object):
    #git operation, include git.log,git.rev_parse
    #for convenience, we just write normalize() to change the data into pieces
    def Regit(self,addr,num):
        repo=Repo(addr)
        git=repo.git
        data=git.log(num)
        return git,data
        #git=repo.git
        #data=git.log(['v4.4'])
    def CommitCutter(self,data):
        l=[]    #Store the large character of each commit
        length=6    #"commit" character length is 6
        count=0
        a=True  #Determine whether there is no next commit, that is, whether all commit characters have been found
        #Divide by "commit"
        while a:
            num=data.find("commit ",count)
            if num==-1:
                a=False #There is no next commit. Exit the loop
            else:
                l.append(num)
                count=num+length    #l stores the digital subscript of "commit"
        i=0
        com=[]
        while i < len(l)-1:
            com.append(data[l[i]:l[i+1]])   #The middle part of the front and back corner marks is the information of each commit
            i+=1
        return com
    def normalize(self,dataliat):
        com1=[] #Used to store cutting results
        for k in dataliat:
            #Document cutting operation
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
                                dic['Long']=self.git.rev_parse(dic['Addr'])
                                dic['Commit2']=self.git.log(dic['Addr'],-1)
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
        return com1
    def csv(self,addr,headers,datadic):
        #Save results as CSV file export
        with open(addr, 'a+',newline='',encoding = 'gb18030')as f:
            f_csv = csv.DictWriter(f,headers)
            f_csv.writeheader()
            for i in datadic:
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
    def __init__(self):
        self.headers=['Origion','Commit','Merge','Author','Email','Date','Area','Fixes','Addr','Long','Commit2','Commit2_Com','Author2','Email2','Date2','Area2','Others']
        self.git,data=self.Regit(r'C:\Users\Win\Desktop\ku\linux-stable',-10000)#加载git库地址,加载数据,用的是绝对地址
        partli=self.CommitCutter(data)
        datadic=self.normalize(partli)
        addr='C:\\Users\\Win\\Desktop\\test2.csv'
        self.csv(addr,self.headers,datadic)

A=gitOp()