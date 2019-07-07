import sys
import subprocess
import itertools
import time
import pandas as pd
import random

def skeleton():
    raw_list = sys.argv[1:]
    if len(raw_list) != 1:
        print("Enter only one number to run corresponding data.")
        return
    n = 0
    try:
        n = int(raw_list[0])
    except ValueError:
        print("Please enter one INTEGER!")
        return
    if n <= 2:
        print("Please enter an integer larger than 2.")
        return
    #perm = [ list(j) for j in list(itertools.permutations([str(i) for i in range(1,n+1)]))]
    rand_select = []
    order_list = [str(i) for i in range(1,n+1)]
    for i in range(0,1):
        rand_select.append(random.sample(order_list,len(order_list)))
    #print(rand_select)
    data_list = []
    for work_list in rand_select:
        start_time = time.time()
        result = subprocess.run(["python3","main.py"] + work_list,capture_output=True).stdout
        end_time = time.time()
        decode_result = result.decode("utf-8")
        parse_result = [int(num) for num in decode_result.split()]
        data_list.append({'list':work_list,'elapsed_time':end_time-start_time,'num_of_clauses':parse_result[0],'num_of_operations':parse_result[1]})
    pd.DataFrame(data_list).to_csv("../data/"+str(n)+"_select_noperm.csv")


skeleton()
