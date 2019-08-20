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
	print(start_perm)
	print(end_perm)
	n = len(start_perm)
	# possible breakpoints
	# creating the cnf file
	cnf_path = 'temp_extension.cnf'
	cnf_file = open(cnf_path,'x')
	cnf_file.close()
	num_of_lines = 0
	num_of_lines += f1(start_perm,end_perm,cnf_path)
	num_of_lines += f2(start_perm,end_perm,cnf_path)
	num_of_lines += f3(start_perm,end_perm,cnf_path)
	num_of_lines += f4(start_perm,end_perm,cnf_path)
	num_of_lines += f5(start_perm,end_perm,cnf_path)
	num_of_lines += f6(start_perm,end_perm,cnf_path)
	print(num_of_lines,end=" ")
	header(start_perm,end_perm,cnf_path,num_of_lines+1)
	#nop_k(2,n,cnf_path)



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


def f2(start_perm,end_perm,cnf_path): # A + C + G + T = 1
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


def f3(start_perm,end_perm,cnf_path):  # level 1
	n = len(start_perm)
	cnf_file = open(cnf_path,'a')
	clause_count = 0
	for t in range(1,n+1):
		if start_perm[t-1] == 'A':
			cnf_file.write(str(A(t,1,n))+" 0\n")
		if start_perm[t-1] == 'C':
			cnf_file.write(str(C(t,1,n))+" 0\n")
		if start_perm[t-1] == 'G':
			cnf_file.write(str(G(t,1,n))+" 0\n")
		if start_perm[t-1] == 'T':
			cnf_file.write(str(T(t,1,n))+" 0\n")
		clause_count += 1
	cnf_file.close()
	return clause_count


def f4(start_perm,end_perm,cnf_path):  # level n 
	n = len(start_perm)
	cnf_file = open(cnf_path,'a')
	clause_count = 0 
	for t in range(1,n+1):
		if end_perm[t-1] == 'A':
			cnf_file.write(str(A(t,n,n))+" 0\n")
		if end_perm[t-1] == 'C':
			cnf_file.write(str(C(t,n,n))+" 0\n")
		if end_perm[t-1] == 'G':
			cnf_file.write(str(G(t,n,n))+" 0\n")
		if end_perm[t-1] == 'T':
			cnf_file.write(str(T(t,n,n))+" 0\n")
		clause_count += 1
	cnf_file.close()
	return clause_count


def f5(start_perm,end_perm,cnf_path): # R -> (A -> A) y3 | ~y1 | ~y2
	n = len(start_perm)
	cnf_file = open(cnf_path,'a')
	clause_count = 0
	for k in range(1,n):
		for p in range(1,n):
			for q in range(p+1,n+1):
				for t in range(1,n+1):
					if t < p or t > q:
						cnf_file.write(str(A(t,k+1,n))+" -"+str(R(p,q,k,n))+" -"+str(A(t,k,n))+" 0\n")
						cnf_file.write(str(C(t,k+1,n))+" -"+str(R(p,q,k,n))+" -"+str(C(t,k,n))+" 0\n")
						cnf_file.write(str(G(t,k+1,n))+" -"+str(R(p,q,k,n))+" -"+str(G(t,k,n))+" 0\n")
						cnf_file.write(str(T(t,k+1,n))+" -"+str(R(p,q,k,n))+" -"+str(T(t,k,n))+" 0\n")
					if p <= t and t <= q:
						cnf_file.write(str(A(p+q-t,k+1,n))+" -"+str(R(p,q,k,n))+" -"+str(A(t,k,n))+" 0\n")
						cnf_file.write(str(C(p+q-t,k+1,n))+" -"+str(R(p,q,k,n))+" -"+str(C(t,k,n))+" 0\n")
						cnf_file.write(str(G(p+q-t,k+1,n))+" -"+str(R(p,q,k,n))+" -"+str(G(t,k,n))+" 0\n")
						cnf_file.write(str(T(p+q-t,k+1,n))+" -"+str(R(p,q,k,n))+" -"+str(T(t,k,n))+" 0\n")
					clause_count += 4
	cnf_file.close()
	return clause_count


def f5(start_perm,end_perm,cnf_path): # NOP -> (A -> A) y3 | ~y1 | ~y2
	n = len(start_perm)
	cnf_file = open(cnf_path,'a')
	clause_count = 0
	for k in range(1,n):
		for t in range(1,n+1):
			cnf_file.write(str(A(t,k+1,n))+" -"+str(NOP(k,n))+" -"+str(A(t,k,n))+" 0\n")
			cnf_file.write(str(C(t,k+1,n))+" -"+str(NOP(k,n))+" -"+str(C(t,k,n))+" 0\n")
			cnf_file.write(str(G(t,k+1,n))+" -"+str(NOP(k,n))+" -"+str(G(t,k,n))+" 0\n")
			cnf_file.write(str(T(t,k+1,n))+" -"+str(NOP(k,n))+" -"+str(T(t,k,n))+" 0\n")
			clause_count += 4
	cnf_file.close()
	return clause_count


def f6(start_perm,end_perm,cnf_path):
	n = len(start_perm)
	cnf_file = open(cnf_path,'a')
	for k in range(1,n-1):
		cnf_file.write(str(NOP(k+1,n))+" -"+str(NOP(k,n))+" 0\n")
	cnf_file.close()
	return n-2


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
	line_prepender(cnf_path,"p cnf "+str(num_of_vars)+" "+str(num_of_clauses))


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


def nop_k(k,n,cnf_path):
	subprocess.run(["cp","temp_extension.cnf","temp_extension_ongoing.cnf"])
	cnf_file = open("temp_extension_ongoing.cnf",'a')
	cnf_file.write(str(NOP(k,n))+" 0\n")
	cnf_file.close()
	result = subprocess.run(["../sat_solver/lingeling","temp_extension_ongoing.cnf"],capture_output=True).stdout
	print(result.decode("utf-8"))


skeleton()