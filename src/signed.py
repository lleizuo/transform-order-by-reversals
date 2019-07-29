import sys
import subprocess
import itertools
import math
import time

sat_instances = {}

def skeleton():
	raw_list = sys.argv[1:]
	if len(raw_list) in {0,1,2}:
		print("Please enter a destination list of more than 2 integers.")
		return
	dest_list = []
	try:
		dest_list = [int(i) for i in raw_list]
	except ValueError:
		print("Please enter an integer list.")
		return
	if set(range(1,len(raw_list)+1)) != set([abs(i) for i in dest_list]):
		print("Your destination list is not valid.")
		return
	n = len(dest_list)
	# seperate the list
	perm_list = [abs(i) for i in dest_list]
	sign_list = [ 1 if i > 0 else 0 for i in dest_list]
	# calculating breakpoints to get bounds
	breakpoints = 0
	bp_list = perm_list
	bp_list = [0] + bp_list
	bp_list.append(n+1)
	for i in range(n+1):
		if abs(bp_list[i+1]-bp_list[i]) != 1:
			breakpoints += 1
	# creating the cnf file
	cnf_path = 'temp_signed.cnf'
	cnf_file = open(cnf_path,'x')
	cnf_file.close()
	num_of_lines = 0
	num_of_lines += f1(cnf_path,n)
	# ......
	header(cnf_path,num_of_lines + 1)
	subprocess.run(["rm","temp_signed.cnf"])


def header(cnf_path,num_of_clauses):
    n = len(dest_list)
    num_of_vars = 0
    # X[k : 1 to n-1][i : 1 to n][p : 1 to n][q : 1 to n]
    num_of_vars += pow(n,4)-pow(n,3)
    # R[p : 1 to n][q : 1 to n][k : 1 to n-1]
    num_of_vars += pow(n,3)-pow(n,2)
    # NOP : 1 to n-1
    num_of_vars += n - 1
    # S[l : 1 to n-1][i : 1 to n]
    num_of_vars += n * (n - 1)
    line_prepender(cnf_path,"p cnf "+str(num_of_vars)+" "+str(num_of_clauses))


def line_prepender(cnf_path, line):
    # https://stackoverflow.com/questions/5914627/prepend-line-to-beginning-of-a-file
    with open(cnf_path, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)


def x_index(k,i,p,q,n):
	return (k-1)*pow(n,3) + (i-1)*pow(n,2) + (p-1)*n + q


def r_index(p,q,k,n):
	return (p-1)*(n*n-n) + (q-1)*(n-1) + k + pow(n,4)-pow(n,3)


def nop_index(k,n):
	return pow(n,4) - pow(n,2) + k


def s_index(l,i,n):
	return (l-1)*n + i + (pow(n,4) - pow(n,2) + n - 1) 


def f1(cnf_path,n):
	cnf_file = open(cnf_path,'a')
	clause_count = 0
	for k in range(1,n):
		var_list = []
		var_list.append(nop_index(k,n))
		for p in range(1,n):
			for q in range(p,n+1): # CHANGED
				var_list.append(r_index(p,q,k,n))
		for elem in var_list:
			cnf_file.write(str(elem)+" ")
		cnf_file.write("0\n")
		clause_count += 1
		for pair in itertools.combinations(var_list,2):
			cnf_file.write("-"+str(pair[0])+" -"+str(pair[1])+" 0\n")
			clause_count +=1
	cnf_file.close()
	return clause_count


def f2(cnf_path,n):
	cnf_file = open(cnf_path,'a')
	clause_count = 0
	for i in range(1,n+1):
		var_list = []
		for q in range(1,n+1):
			var_list.append(x_index(1,i,i,q,n))
		for elem in var_list:
			cnf_file.write(str(elem)+" ")
		cnf_file.write("0\n")
		clause_count += 1
		for pair in itertools.combinations(var_list,2):
			cnf_file.write("-"+str(pair[0])+" -"+str(pair[1])+" 0\n")
			clause_count += 1
	cnf_file.close()
	return clause_count


def f3(perm_list,cnf_path,n):
	cnf_file = open(cnf_path,'a')
	clause_count = 0
	for i in range(1,n+1):
		var_list = []
		for p in range(1,n+1):
			var_list.append(x_index(2n-1,i,p,perm_list.index(i)+1),n)
		for elem in var_list:
			cnf_file.write(str(elem)+" ")
		cnf_file.write("0\n")
		clause_count += 1
		for pair in itertools.combinations(var_list,2):
			cnf_file.write("-"+str(pair[0])+" -"+str(pair[1])+" 0\n")
			clause_count += 1
	cnf_file.close()
	return clause_count


def f4(cnf_path,n):
	return 



skeleton()