import csv
with open('/home/liuyz/桌面/test2(4).csv', encoding='gb18030') as f:

    f_csv = csv.reader(f)
    au={}
    ca={}
    for row in f_csv:
        if row[6] != None:
            if row[2] in au.keys():
                l=au.get(row[2])
                l.append(row[6])
                au[row[2]]=l
            else:
                l=[]
                l.append(row[6])
                au[row[2]]=l
            
            
    for key in au:
        l=[]
        v=au.get(key)
        l.append(len(v))
        l.append(len(set(v)))
        ca[key]=l
print('作者：[此人总共fix的次数，此人fix过提交的种类数]'+'\n',ca)


headers=['作者','总数','种类数']
rows=[]
for key in au:
    r=[]
    v=au.get(key)
    r.append(key)
    r.append(len(v))
    r.append(len(set(v)))
    rows.append(r)
with open('/home/liuyz/桌面/data2.csv','a+',encoding='gb18030') as d:
    f_csv = csv.writer(d)
    f_csv.writerow(headers)
    f_csv.writerows(rows)
    
