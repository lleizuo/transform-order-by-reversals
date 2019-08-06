import pandas as pd
import sys
import ast
import subprocess
import time

def skeleton():
	if len(sys.argv) <= 1:
		print("Input error.")
		return
	if not sys.argv[1] in {"signed","unsigned"}:
		print("Input error.")
		return 
	if not sys.argv[2].isdigit():
		print("Input error.")
		return
	if int(sys.argv[2]) <= 2:
		print("No")
		return
	if not sys.argv[3].isdigit():
		print("Input error.")
		return
	sat_data = pd.read_csv("../data2/"+sys.argv[1]+"_"+sys.argv[2]+"_"+sys.argv[3]+".csv",index_col=0)
	ilp_time = []
	for index,row in sat_data.iterrows():
		li = ast.literal_eval(row['list'])
		li_str = ""
		for elem in li:
			li_str += elem + " "
		li_str = li_str.strip()
		file_path = 'listfile'
		li_file = open(file_path,'x')
		li_file.write(li_str)
		li_file.close()
		subprocess.run(["perl","../ilp/breversals.pl",sys.argv[1],file_path])
		start_time = time.time()
		subprocess.run(["gurobi_cl","Rlistfile.lp"])
		end_time = time.time()
		ilp_time.append(end_time - start_time)
		subprocess.run(["rm","listfile"])
		subprocess.run(["rm","gurobi.log"]) 
		subprocess.run(["rm","Rlistfile.lp"])
	sat_data['time_ilp'] = ilp_time
	sat_data = sat_data.drop(columns=['details','num_of_clauses'])
	sat_data = sat_data.rename(columns={'elapsed_time':'time_sat'})
	cols = sat_data.columns.tolist()
	cols = cols[-1:] + cols[:-1]
	sat_data = sat_data[cols]
	sat_data.to_csv("../cmp_data/cmp_"+sys.argv[1]+".csv")


skeleton()