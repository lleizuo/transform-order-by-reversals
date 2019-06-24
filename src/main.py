import sys
import subprocess

def skeleton():
    # input parsing for only P2 now
    raw_list = sys.argv[1:]
    if len(raw_list) == 0 or len(raw_list) == 1:
        print("Please enter a destination list of integers.")
        return
    if set([str(i) for i in list(range(1,len(raw_list)+1))]) != set(raw_list):
        print("Your destination list is not valid.")
        return
    dest_list = [int(i) for i in raw_list]
    cnf_path = 'temp.cnf'
    cnf_file = open(cnf_path,'r+')
    cnf_file.write("1 0 1")
    cnf_file.close()



skeleton()
