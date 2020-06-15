from subprocess import Popen, PIPE, DEVNULL
import re
import matplotlib.pyplot as plt

class Hypothesis():
    def __init__(self):
        self.bug = "git log | grep -m 50 'Fixes:'"
        self.normal = "git --no-pager log -50 --pretty=format:'%H'"
        with open("record.txt", encoding="utf-8") as f:
            self.fixset = f.read()
        f.close()
        self.choose()
    
    def choose(self):
        option = eval(input("""Choose whether you want to compare the
corresponding bug with a fix or use 
the previous commit of the fix to 
compare with the fix.
(1:bug  2:fix~)\n"""))
        if option == 1:
            cmd = "'git diff --numstat ' + fixbug[bugno] + '..' + fixbug[fixno]"
            self.aver_fix_changes = self.GetFixChanges(cmd, 1)
        elif option == 2:
            cmd = "'git diff --numstat ' + fixbug[fixno] + '~..' + fixbug[fixno]"
            self.aver_fix_changes = self.GetFixChanges(cmd, 2)
        else:
            print("Warning!There are only 2 choices.")
            return
        self.aver_bug_changes = self.GetBugChanges()
        self.aver_normal_changes = self.GetNormalChanges()
        self.compare()
        
    def GetBugChanges(self):
        get_bugs = Popen(self.bug, stdout=PIPE, stderr=DEVNULL, shell=True)
        bugset = get_bugs.communicate()[0].decode("utf-8")
        bugs = re.findall("Fixes: (.*?) \(", bugset)
        bc = 0
        self.graph_bug = []
        for i in bugs:
            cmd = "git diff --numstat " + i + "~.." + i
            bug_diff = Popen(cmd, stdout=PIPE, stderr=DEVNULL, shell=True)
            bug_changes = bug_diff.communicate()[0].decode("utf-8")
            listbc = bug_changes.split("\n")
            bc = bc + len(listbc)
            self.graph_bug.append(len(listbc))
        aver_bc = bc/len(bugs)
        return aver_bc
        
    def GetNormalChanges(self):
        get_normal = Popen(self.normal, stdout=PIPE, stderr=DEVNULL, shell=True)
        normalset = get_normal.communicate()[0].decode("utf-8") 
        normals = normalset.split("\n")
        nc = 0
        for i in normals:
            i = eval(i)
            cmd = "git diff --numstat " + i + "~.." + i
            normal_diff = Popen(cmd, stdout=PIPE, stderr=DEVNULL, shell=True)
            normal_changes = normal_diff.communicate()[0].decode("utf-8")
            listnc = normal_changes.split("\n")
            nc = nc + len(listnc)
        aver_nc = nc/len(normals)
        return aver_nc
        
    def GetFixChanges(self, pre_method, opt):
        fix = re.findall("commit (.*?)\nAuthor|Fixes: (.*?) \(", self.fixset)
        fixbug = []
        for i in fix:
            for j in i:
                if j != "":
                    fixbug.append(j)
        if opt == 1:
            pointer = 0
            while True:
                next = pointer + 1
                if next < len(fixbug) and len(fixbug[pointer]) ==40 and len(fixbug[next]) < 40:
                    pointer = pointer + 2
                    continue
                elif next >= len(fixbug):
                    break
                else:
                    fixbug.remove(fixbug[pointer])
                    next = next - 1
                    continue
            for i in range(len(fixbug)):
                if len(fixbug[i]) < 40:
                    treat = "git rev-parse " + fixbug[i]
                    cptbug = Popen(treat, stdout=PIPE, stderr=DEVNULL, shell=True)
                    fixbug[i] = cptbug.communicate()[0].decode("utf-8").strip("\n")
                else:
                    pass
        else:
            pass
        fc = 0
        fixno = 0
        self.graph_fix = []
        while True:
            bugno = fixno + 1
            if bugno <= len(fixbug):
                method = eval(pre_method)
                fix_diff = Popen(method, stdout=PIPE, stderr=DEVNULL, shell=True)
                fix_changes = fix_diff.communicate()[0].decode("utf-8")
                listfc = fix_changes.split("\n")
                fc = fc + len(listfc)
                self.graph_fix.append(len(listfc))
                fixno = bugno + 1
                continue
            else:
                aver_fc = fc/(len(fixbug)/2)
                break
        return aver_fc
    
    def compare(self):
        bfnlt = [self.aver_bug_changes, self.aver_fix_changes, self.aver_normal_changes]
        bfnlt.sort()
        print("The average number of bug changes is " + str(self.aver_bug_changes))
        print("The average number of fix changes is " + str(self.aver_fix_changes))
        print("The average number of normal changes is " + str(self.aver_normal_changes))
        print("\n" + str(bfnlt[0]) + " < " + str(bfnlt[1]) + " < " + str(bfnlt[2]))
        self.DrawPicture()
        
    def DrawPicture(self):
        x = self.graph_bug
        y = self.graph_fix[:len(self.graph_bug)]
        p = plt.scatter(x,y,marker='x',color='g',label='change',s=30)
        plt.xlabel('bug_changes')
        plt.ylabel('fix_changes')
        plt.title('The comparison between Fix Changes and bug Changes.')
        plt.legend(loc='upper right')
        plt.xticks(x)
        plt.show()
        
        
if __name__ == "__main__":
    Hypothesis()