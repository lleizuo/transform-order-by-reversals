import sys
import subprocess
import itertools
import time
import pandas as pd
import random
import ast

def skeleton():
    raw_list = sys.argv[1:]
    if len(raw_list) != 2:
        print("Enter only one number to run corresponding data.")
        return
    n = 0
    data_num = 0
    try:
        n = int(raw_list[0])
        data_num = int(raw_list[1])
    except ValueError:
        print("Please enter two INTEGERs!")
        return
    if n <= 2:
        print("Please enter an integer larger than 2.")
        return
    if data_num < 1:
        print("Please enter a number of data that is larger than 0.")
        return
    #perm = [ list(j) for j in list(itertools.permutations([str(i) for i in range(1,n+1)]))]
    rand_select = []
    order_list = [str(i) for i in range(1,n+1)]
    for i in range(0,data_num):
        rand_select.append(random.sample(order_list,len(order_list)))
    #print(rand_select)
    data_list = []
    for work_list in rand_select:
        print(work_list)
        start_time = time.time()
        result = subprocess.run(["python3","unsigned.py"] + work_list,capture_output=True).stdout
        end_time = time.time()
        decode_result = result.decode("utf-8")
        flagpos = decode_result.find("dictflag")
        flagpos2 = decode_result.find("operflag")
        parse_result = [int(num) for num in decode_result[:flagpos].split()]
        detaildict = ast.literal_eval(decode_result[flagpos+9:flagpos2])
        detailoper = ast.literal_eval(decode_result[flagpos2+9:])
        data_list.append({'list':work_list,'elapsed_time':end_time-start_time,'num_of_clauses':parse_result[0],'num_of_operations':parse_result[1],"details":detaildict,"operations":detailoper})
    pd.DataFrame(data_list).to_csv("../data2/p_unsigned_"+str(n)+"_"+str(data_num)+".csv")


skeleton()
