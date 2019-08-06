import sys
import subprocess
import itertools
import math
import time

sat_instances = {}
operation_lists = {}

def skeleton():
	# input parsing
	perm_duo = sys.argv[1:]
	correct_flag = False
	if len(perm_duo) == 2:
		if all([i in {'A','C','G','T'} for i in perm_duo[0]]):
			if all([i in {'A','C','G','T'} for i in perm_duo[1]]):
				if len(perm_duo[0]) == len(perm_duo[1]):
					correct_flag = True
	if not correct_flag:
		print("Input error.")
		return 
	start_perm = perm_duo[0]
	end_perm = perm_duo[1]
	n = len(start_perm)
	# possible breakpoints
	# creating the cnf file
	cnf_path = 'temp_extension.cnf'
	cnf_file = open(cnf_path,'x')
	cnf_file.close()
	num_of_lines = 0
	num_of_lines += f1(start_perm,end_perm,cnf_path)
	num_of_lines += f2(start_perm,end_perm,cnf_path)
	print(num_of_lines,end=" ")
	header(start_perm,end_perm,cnf_path,num_of_lines+1)



def f1(start_perm,end_perm,cnf_path): # NOP + Sigma R = 1
	n = len(start_perm)
	cnf_file = open(cnf_path,'a')
	clause_count = 0
	for k in range(1,n):
		var_list = []
		var_list.append(NOP(k,n))
		for p in range(1,n):
			for q in range(p+1,n+1):
				var_list.append(R(p,q,k,n))
		for elem in var_list:
			cnf_file.write(str(elem)+" ")
		cnf_file.write("0\n")
		clause_count += 1
		for pair in itertools.combinations(var_list,2):
			cnf_file.write("-"+str(pair[0])+" -"+str(pair[1])+" 0\n")
			clause_count += 1
		cnf_file.close()
		return clause_count


def f2(start_perm,end_perm,cnf_path): 
	n = len(start_perm)
	cnf_file = open(cnf_path,'a')
	clause_count = 0
	for k in range(1,n+1):
		for t in range(1,n+1):
			var_list = []
			var_list.append(A(t,k,n))
			var_list.append(C(t,k,n))
			var_list.append(G(t,k,n))
			var_list.append(T(t,k,n))
			for elem in var_list:
				cnf_file.write(str(elem)+" ")
			cnf_file.write("0\n")
			clause_count += 1
			for pair in itertools.combinations(var_list,2):
				cnf_file.write("-"+str(pair[0])+" -"+str(pair[1])+" 0\n")
				clause_count += 1
	cnf_file.close()
	return clause_count




def header(start_perm,end_perm,cnf_path,num_of_clauses):
	n = len(start_perm)
	num_of_vars = 0
	# A [t : 1 to n][k : 1 to n]
	num_of_vars += pow(n,2)
	# C [t : 1 to n][k : 1 to n]
	num_of_vars += pow(n,2)
	# G [t : 1 to n][k : 1 to n]
	num_of_vars += pow(n,2)
	# T [t : 1 to n][k : 1 to n]
	num_of_vars += pow(n,2)
	# R [p : 1 to n][q : 1 to n][k : 1 to n-1]
	num_of_vars += pow(n,3) - pow(n,2)
	# NOP : 1 to n-1
	num_of_vars += n - 1


def line_prepender(cnf_path, line):
    # https://stackoverflow.com/questions/5914627/prepend-line-to-beginning-of-a-file
    with open(cnf_path, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)


def A(t,k,n):
	return (t-1)*n + k


def C(t,k,n):
	return (t-1)*n + k + pow(n,2)


def G(t,k,n):
	return (t-1)*n + k + pow(n,2)*2


def T(t,k,n):
	return (t-1)*n + k + pow(n,2)*3


def R(p,q,k,n):
	return (p-1)*(n*n-n) + (q-1)*(n-1) + k + pow(n,2)*4


def NOP(k,n):
	return k + pow(n,2)*3 + pow(n,3)



skeleton()