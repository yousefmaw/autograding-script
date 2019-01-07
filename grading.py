import os
import sys
import fileinput
import subprocess
import pandas as pd
import time
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
    newdata = filedata.replace('module seq_'+str+'(output out, input seq, input clk, input clear);','module SEQ_DETECTOR(output out, input seq, input clk, input clear);')
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
    CHECK_SUBMISSION(strBN)
    result.append(CHECK_SUBMISSION(strBN))
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
for i in range (0,len(data)):
    if [(True, 'PASS'), (True, 'PASS'), (True, 'PASS')] in data[i]:
        right= right +1
print("number of right submissions is",right)
print("number of wrong submissions is",len(data)-right)
name =  'result' + str(time.time())+ '.xlsx'
df = pd.DataFrame(data,columns=['BN','pass or fail']) 
excel = pd.ExcelWriter(name)
df.to_excel(excel,'Sheet1')
excel.save()