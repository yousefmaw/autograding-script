import os
import sys
import fileinput
import subprocess
import pandas as pd
import time
import re
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
    newdata = re.sub(r"^module seq_23[0-9]{3}\s?\(\s?output out\s?,\s?input seq\s?,\s?input clk\s?,\s?input clear\s?\);",'module SEQ_DETECTOR(output out, input seq, input clk, input clear);',filedata)
    f = open(dir,'w')
    f.write(newdata)
    f.close()
####################

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
    grade = CHECK_SUBMISSION(strBN)
    result.append(grade)
    if grade ==[(True, 'PASS'), (True, 'PASS'), (True, 'PASS')]:
            result.append(4)
    elif grade[1] == (True, 'PASS') :
            result.append(3)
    elif (grade[0] == (True, 'PASS') ) or (grade[2] == (True, 'PASS') ):
            result.append(1)
    else:
                    result.append(1)

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
right=0
notworking = 0 
for i in range (0,len(data)):
        if [(True, 'PASS'), (True, 'PASS'), (True, 'PASS')] in data[i]:
                right= right +1
        if (False, 'C:\\Users\\yousefmaw\\Desktop\\ass4>vvp a.out ') in data[i]:
                notworking= notworking +1
print("number of right submissions is",right)
print("number of wrong submissions is",len(data)-right)
print("number of not workin submissions is",notworking)
name =  'result' + str(time.time())+ '.xlsx'
df = pd.DataFrame(data,columns=['BN','pass or fail','grade']) 
excel = pd.ExcelWriter(name)
df.to_excel(excel,'Sheet1')
excel.save()
