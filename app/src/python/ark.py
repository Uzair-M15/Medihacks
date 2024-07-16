import os
import json

def reference(line):
    ref = line[1:21]
    ref = ref.replace(':','')       
    new = ''
    if ref:
        for x in range(13,-1,-2):
            new += ref[x-1] + ref[x]
    return new

def sort(sent , received , out_path):
    received_dict = {}
    sent_list = []
    cnt = cnt1 = 0

    if os.path.exists(sent) and os.path.exists(received):
        with open(received) as file:
            for i in file:    
                received_dict.update({reference(i):i})            
            received_dict = dict(sorted(received_dict.items()))

            with open(sent) as file1:
                for x in file1:
                    sent_list.append(reference(x)+x)  

        with open(f'{out_path}/sorted.txt','w') as file1:
            try:
                for i in range(len(sent_list) + len(list(received_dict.keys()))):  
                    if cnt != len(sent_list):
                        if cnt1 != len(list(received_dict.keys())):
                            if int(sent_list[cnt][:14]) > int(list(received_dict.keys())[cnt1]):
                                file1.write(list(received_dict.values())[cnt])
                                cnt1 += 1
                            else:
                                file1.write(sent_list[cnt1-1][14:])
                                cnt += 1
                        else:
                            for i in range(len(sent_list) + len(list(received_dict.keys())) -  cnt1):
                                file1.write(sent_list[cnt1-1][14:])
                                cnt1 += 1
                    else:
                        for i in range(len(sent_list) + len(list(received_dict.keys())) -  cnt):
                            file1.write(list(received_dict.values())[cnt])
                            cnt += 1
            except IndexError:
                pass        
    else:
        print('File not found!')