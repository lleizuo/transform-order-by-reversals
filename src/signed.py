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
	# calculating the bounds
	lower_bound = int((breakpoints/2) + 0.6)
	upper_bound = breakpoints + n
	# creating the cnf file
	cnf_path = 'temp_signed.cnf'
	cnf_file = open(cnf_path,'x')
	cnf_file.close()
	num_of_lines = 0
	num_of_lines += f1(cnf_path,n,upper_bound)
	num_of_lines += f2(cnf_path,n)
	num_of_lines += f3(perm_list,cnf_path,n,upper_bound)
	num_of_lines += f4(cnf_path,n,upper_bound)
	num_of_lines += f5(cnf_path,n,upper_bound)
	num_of_lines += f6(cnf_path,n,upper_bound)
	num_of_lines += f7(cnf_path,n,upper_bound)
	num_of_lines += f8(cnf_path,n,upper_bound)
	num_of_lines += f9(cnf_path,n,upper_bound)
	# signed restrictions
	# ......
	header(cnf_path,num_of_lines,n,upper_bound)
	#subprocess.run(["rm","temp_signed.cnf"])


def header(cnf_path,num_of_clauses,n,upper_bound):
    num_of_vars = 0
    # X[k : 1 to upper_bound][i : 1 to n][p : 1 to n][q : 1 to n]
    num_of_vars += pow(n,3) * upper_bound
    # R[p : 1 to n][q : 1 to n][k : 1 to upper_bound]
    num_of_vars += pow(n,2) * upper_bound
    # NOP : 1 to upper_bound
    num_of_vars += upper_bound
    # S[l : 1 to upper_bound][i : 1 to n]
    num_of_vars += n * upper_bound
    line_prepender(cnf_path,"p cnf "+str(num_of_vars)+" "+str(num_of_clauses))


def line_prepender(cnf_path, line):
    # https://stackoverflow.com/questions/5914627/prepend-line-to-beginning-of-a-file
    with open(cnf_path, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)


def x_index(k,i,p,q,n):
	return (k-1)*pow(n,3) + (i-1)*pow(n,2) + (p-1)*n + q


def r_index(p,q,k,n,upper_bound):
	return (p-1)*n*upper_bound + (q-1)*upper_bound + k + pow(n,3) * upper_bound


def nop_index(k,n,upper_bound):
	return pow(n,3) * upper_bound + pow(n,2) * upper_bound + k


def s_index(l,i,n,upper_bound):
	return (l-1)*n + i + pow(n,3) * upper_bound + pow(n,2) * upper_bound + upper_bound


def f1(cnf_path,n,upper_bound):
	cnf_file = open(cnf_path,'a')
	clause_count = 0
	for k in range(1,upper_bound+1):
		var_list = []
		var_list.append(nop_index(k,n,upper_bound))
		for p in range(1,n):
			for q in range(p,n+1): # CHANGED
				var_list.append(r_index(p,q,k,n,upper_bound))
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


def f3(perm_list,cnf_path,n,upper_bound):
	cnf_file = open(cnf_path,'a')
	clause_count = 0
	for i in range(1,n+1):
		var_list = []
		for p in range(1,n+1):
			var_list.append(x_index(upper_bound,i,p,perm_list.index(i)+1,n))
		for elem in var_list:
			cnf_file.write(str(elem)+" ")
		cnf_file.write("0\n")
		clause_count += 1
		for pair in itertools.combinations(var_list,2):
			cnf_file.write("-"+str(pair[0])+" -"+str(pair[1])+" 0\n")
			clause_count += 1
	cnf_file.close()
	return clause_count


def f4(cnf_path,n,upper_bound):
	cnf_file = open(cnf_path,'a')
	clause_count = 0
	for k in range(2,upper_bound+1):
		for q in range(1,n+1):
			var_list = []
			for p in range(1,n+1):
				for i in range(1,n+1):
					var_list.append(x_index(k-1,i,p,q,n))
			for elem in var_list:
				cnf_file.write(str(elem)+" ")
			cnf_file.write("0\n")
			clause_count +=1
			for pair in itertools.combinations(var_list,2):
				cnf_file.write("-"+str(pair[0])+" -"+str(pair[1])+" 0\n")
				clause_count += 1
	cnf_file.close()
	return clause_count


def f5(cnf_path,n,upper_bound):
	cnf_file = open(cnf_path,'a')
	clause_count = 0
	for k in range(2,upper_bound+1):
		for p in range(1,n+1):
			var_list = []
			for q in range(1,n+1):
				for i in range(1,n+1):
					var_list.append(x_index(k,i,p,q,n))
			for elem in var_list:
				cnf_file.write(str(elem)+" ")
			cnf_file.write("0\n")
			clause_count += 1
			for pair in itertools.combinations(var_list,2):
				cnf_file.write("-"+str(pair[0])+" -"+str(pair[1])+" 0\n")
				clause_count += 1
	cnf_file.close()
	return clause_count


def f6(cnf_path,n,upper_bound):
	cnf_file = open(cnf_path,'a')
	clause_count = 0
	for k in range(2,upper_bound+1):
		for i in range(1,n+1):
			for p in range(1,n+1):
				var_list_1 = []
				var_list_2 = []
				for q in range(1,n+1):
					var_list_1.append(x_index(k-1,i,q,p,n))
					var_list_2.append(x_index(k,i,p,q,n))
				first_string = ""
				for var in var_list_1:
					first_string += str(var) + " "
				for var in var_list_2:
					cnf_file.write(first_string+" -"+str(var)+" 0\n")
					clause_count += 1
				second_string = ""
				for var in var_list_2:
					second_string += str(var) + " "
				for var in var_list_1:
					cnf_file.write(second_string+" -"+str(var)+" 0\n")
					clause_count += 1
	cnf_file.close()
	return clause_count


def f7(cnf_path,n,upper_bound):
	cnf_file = open(cnf_path,'a')
	clause_count = 0
	for k in range(1,upper_bound+1):
		for w in range(1,n+1):
			var_list_1 = []
			var_list_2 = []
			for i in range(1,n+1):
				var_list_1.append(x_index(k,i,w,w,n))
			var_list_2.append(nop_index(k,n,upper_bound))
			for p in range(1,n):
				for q in range(p,n+1):
					if 2 * w == p + q:
						var_list_2.append(r_index(p,q,k,n,upper_bound))
					if p < w and q < w:
						var_list_2.append(r_index(p,q,k,n,upper_bound))
					if p > w and q > w:
						var_list_2.append(r_index(p,q,k,n,upper_bound))
			second_string = ""
			for var in var_list_2:
				second_string += str(var) + " "
			for var in var_list_1:
				cnf_file.write(second_string+"-"+str(var)+" 0\n")
				clause_count += 1
	cnf_file.close()
	return clause_count


def f8(cnf_path,n,upper_bound):
	cnf_file = open(cnf_path,'a')
	clause_count = 0
	for k in range(1,upper_bound+1):
		for w in range(1,n+1):
			for z in range(1,n+1):
				if z == w:
					continue
				var_list_1 = []
				var_list_2 = []
				for i in range(1,n+1):
					var_list_1.append(x_index(k,i,w,z,n))
				a = min(w,z)
				b = max(w,z)
				c = min(a-1,n-b)
				for d in range(0,c+1):
					if a - d != b + d:
						var_list_2.append(r_index(a-d,b+d,k,n,upper_bound))
				second_string = ""
				for var in var_list_2:
					second_string += str(var) + " "
				for var in var_list_1:
					cnf_file.write(second_string+"-"+str(var)+" 0\n")
					clause_count += 1
	cnf_file.close()
	return clause_count


def f9(cnf_path,n,upper_bound):
	cnf_file = open(cnf_path,'a')
	for k in range(1,upper_bound):
		cnf_file.write(str(nop_index(k+1,n,upper_bound))+" -"+str(nop_index(k,n,upper_bound))+" 0\n")
	cnf_file.close()
	return upper_bound - 1


skeleton()