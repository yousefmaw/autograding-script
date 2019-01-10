import os
import sys
import fileinput
import subprocess
import pandas as pd
import time
import re
import shutil
'''''
command = 'iverilog dff.v seq_23003.v seq_tb.v'
os.system(command)
os.system('vvp a.out')
os.system('gtkwave dump.vcd')
'''''
####### function to make module name const
def change_module (str, dir):
    f = open(dir,'r')
    filedata = f.read()
    f.close()
    newdata = re.sub(r"seq_23[0-9]{3}",'SEQ_DETECTOR',filedata)
    f = open(dir,'w')
    f.write(newdata)
    f.close()
####################
########function to change the module name in the tb direct
def change_tb(BN):
        f = open('tb_validator.v','r')
        filedata = f.read()
        f.close()
        newdata = re.sub(r"seq_23[0-9]{3}",'seq_'+BN,filedata)
        f = open('tb_validator.v','w')
        f.write(newdata)
        f.close()
### function to convert the BN to BCD to pass it to the TB

def BNtoBCD(BN):
    return "".join(["{0:{fill}4b}".format(int(i), fill='0') for i in str(BN)[2:]])
##############
####
### function for running the test ench task on a specific file
def CHECK_SUBMISSION(BN):
    bcd = BNtoBCD(BN)
    bcd = "12'b" + bcd
    module_dir = os.path.abspath("submissions/submissions/{0}/seq_{0}.v".format(BN))
    out = subprocess.Popen(["run_me.bat", bcd, module_dir],
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT)
    out.wait()
    stdout,stderr = out.communicate()
    res = (stdout.decode("utf-8").split("\r\n")[-4:-1])
    return [(i=="PASS", i) for i in res]

#### main function for grading

def passorfail(strBN,intBCD):   
    result = []
    result.append(int(strBN))
    change_tb(strBN) 
    grade = CHECK_SUBMISSION(strBN)
    result.append(grade)
    if grade ==[(True, 'PASS'), (True, 'PASS'), (True, 'PASS')]:
            result.append(4)
    elif grade[1] == (True, 'PASS') :
            result.append(3)
    else:
            result.append(-1)

    print(result)
    return result
#########################################
#main lock too run
#################################
dir = "submissions\\submissions"
data = []
subfolders = os.listdir(dir) 
for i in subfolders:
    #change_module(i,dir+"\\"+i+"\\"+"seq_"+i+".v") #needed to be ran once

    result = passorfail(i,BNtoBCD(i))
    data.append(result)
    if result [2]==-1:
            shutil.copytree(dir+"\\"+i, "wrong\\"+i, symlinks=False, ignore=None)
right=0
wrong =0
for i in range (0,len(data)):
        if data[i][2] == 4:
                right= right +1
        if data[i][2] == -1:
                wrong = wrong +1
        

print("number of right submissions is",right)
print("number of wrong submissions is",wrong)
print ("number of semi wrong submissions is",len(data)-right -wrong)
name =  'result' + str(time.time())+ '.xlsx'
df = pd.DataFrame(data,columns=['BN','pass or fail','grade']) 
excel = pd.ExcelWriter(name)
df.to_excel(excel,'Sheet1')
excel.save()

