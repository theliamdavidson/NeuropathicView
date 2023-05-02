
import pandas as pd
import shutil
from random import randint
import datetime 
 
# makes a copy of the template file, reads the vessels from the data page
# and 

patient_name = "Nicole_Davidson"
date=datetime.datetime.now().strftime("%d-%m-%y_%I-%M")
print(date)
file_name = 'output/'+patient_name+'.xlsx'
shutil.copyfile('excel/NVI.xlsx', file_name)
raw_data = pd.read_excel(file_name,'Raw.donate',header=None)
vs_list = []


long_list = raw_data.values.T.tolist()
for i in range(len(long_list)):
    for j in range(len(long_list[i])):
        try:
            print(long_list[i][j] + " is a vessel")
            vs_list.append([long_list[i][j],[i,j]])
        except TypeError:
            pass
for i in range(len(vs_list)): #
    for index, vessels in enumerate(vs_list):
        if vessels[1][1] == i:
            print(vessels[0])
            print(vessels[1])
            vs_list[index].append([randint(0,425)/14,randint(0,425)/14,randint(0,425)/14,randint(0,425)/14])
            
print(vs_list)
for items in vs_list:
    #print(items[1][0])
    print(long_list[items[1][0]][items[1][1]])
    if items[1][1] == 0:
        long_list[items[1][0]][items[1][1]+2] = items[2][0]         # PI Upper
        long_list[items[1][0]+1][items[1][1]+2] = items[2][2]       # VF Upper
        long_list[items[1][0]][items[1][1]+3] = items[2][1]         # PI Lower
        long_list[items[1][0]+1][items[1][1]+3] = items[2][3]       # VF Lower
    else:
        long_list[items[1][0]][items[1][1]+1] = items[2][0]         # PI Upper
        long_list[items[1][0]+1][items[1][1]+1] = items[2][2]       # VF Upper
        long_list[items[1][0]][items[1][1]+2] = items[2][1]         # PI Lower
        long_list[items[1][0]+1][items[1][1]+2] = items[2][3]       # VF Lower
df = pd.DataFrame(long_list)
df = df.T
print(df)
print("outputting values...")
b4_time = datetime.datetime.now()
print(b4_time.strftime("%I:%M:%S"))
with pd.ExcelWriter(file_name, engine='openpyxl', mode='a',if_sheet_exists='replace') as writer: #
     df.to_excel(writer,'Raw.donate',startrow=0, index=False, header=False)

print("done!")
cur_time = datetime.datetime.now()
print(cur_time.strftime("%I:%M:%S"))
print("time to compute",cur_time-b4_time)