import pandas as pd
import os
import pandas as pd
import os 
import re

checker_list=[',','...','[',']','\\','\'','\"']
data_desc_set=set()

def delay():
    pass
        
def parser_text(s):
    dummy_list =list(s)
    s=list(s)
    string_one=''
    lo=[]
    l=0
    #for k in range(len(s)):
    for i in range(len(s)):
        if str(s[i]).isalpha():
            string_one+=s[i]
        else:
            if len(string_one)!=0:
                data_desc_set.add(string_one.lower())
                string_one=''
            else:
                continue


for i 
data_skill = data.iloc[:,5:6]
data_skill = data_skill.values.tolist()

for i in data_skill:
    if i is None:
        continue
    else:
        dummy = str(i)
        dummy = re.split("\s* | [!@#$%^&*;:'\",.?/-/[]]* | \d* ",dummy)
        dummy = ''.join(dummy)
        parser_text(dummy)
        
print (len(data_desc_set))
main_data=pd.DataFrame.from_dict(main_data,orient='index')
writer = pd.ExcelWriter('main_skill2.xlsx', engine='xlsxwriter')
main_data.to_excel(writer)
print ('done firdt')
print (main_data)
writer.save()
writer.close()
print ('done last')

    
