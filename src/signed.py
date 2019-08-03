import sys
import subprocess
import itertools
import math
import time


sat_instances = {}
operation_lists = {}


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
	num_of_lines += f_sign(sign_list,cnf_path,n,upper_bound)
	print(num_of_lines,end=" ")
	header(cnf_path,num_of_lines+1,n,upper_bound)
	# optimization on search
	if nop_k(1,cnf_path,n,upper_bound):
		print(0,end=" ")
	else:
		if not nop_k(upper_bound,cnf_path,n,upper_bound):
			print(upper_bound,end=" ")
		else:
			k = search_k(max(lower_bound-1,1),upper_bound,cnf_path,n,upper_bound)
			nop_k(k+1,cnf_path,n,upper_bound)
			print(k,end=" ")
	subprocess.run(["rm","temp_signed.cnf"])
	print("dictflag",end=" ")
	print(sat_instances,end=" ")
	print("operflag",end=" ")
	print(operation_lists,end=" ")


def header(cnf_path,num_of_clauses,n,upper_bound):
    num_of_vars = 0
    # X[k : 1 to upper_bound][i : 1 to n][p : 1 to n][q : 1 to n]
    num_of_vars += pow(n,3) * upper_bound
    # R[p : 1 to n][q : 1 to n][k : 1 to upper_bound]
    num_of_vars += pow(n,2) * upper_bound
    # NOP : 1 to upper_bound
    num_of_vars += upper_bound
    # S[l : 1 to upper_bound+1][i : 1 to n]
    num_of_vars += n * (upper_bound+1)
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
		for p in range(1,n+1):
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
			for p in range(1,n+1):
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


def f_sign(sign_list,cnf_path,n,upper_bound):
	cnf_file = open(cnf_path,'a')
	clause_count = 0
	for i in range(1,n+1):
		if sign_list[i-1]:
			cnf_file.write(str(s_index(upper_bound+1,i,n,upper_bound))+" 0\n")
			clause_count += 1
		else:
			cnf_file.write("-"+str(s_index(upper_bound+1,i,n,upper_bound))+" 0\n")
			clause_count += 1
	for i in range(1,n+1):
		cnf_file.write(str(s_index(1,i,n,upper_bound))+" 0\n")
		clause_count += 1
	for l in range(1,upper_bound+1):
		for p in range(1,n+1):
			for q in range(p,n+1):
				for offset in range(0,q-p+1):
					i = p + offset
					j = q - offset
					s1 = "-"+str(r_index(p,q,l,n,upper_bound))+" -"+str(s_index(l+1,i,n,upper_bound))+" -"+str(s_index(l,j,n,upper_bound))
					s2 = "-"+str(r_index(p,q,l,n,upper_bound))+" "+str(s_index(l+1,i,n,upper_bound))+" "+str(s_index(l,j,n,upper_bound))
					cnf_file.write(s1+" 0\n")
					cnf_file.write(s2+" 0\n")
					clause_count += 2
				for i in range(1,p):
					cnf_file.write("-"+str(r_index(p,q,l,n,upper_bound))+" "+str(s_index(l+1,i,n,upper_bound))+" -"+str(s_index(l,i,n,upper_bound))+" 0\n")
					cnf_file.write("-"+str(r_index(p,q,l,n,upper_bound))+" -"+str(s_index(l+1,i,n,upper_bound))+" "+str(s_index(l,i,n,upper_bound))+" 0\n")
					clause_count += 2
				for i in range(q+1,n+1):
					cnf_file.write("-"+str(r_index(p,q,l,n,upper_bound))+" "+str(s_index(l+1,i,n,upper_bound))+" -"+str(s_index(l,i,n,upper_bound))+" 0\n")
					cnf_file.write("-"+str(r_index(p,q,l,n,upper_bound))+" -"+str(s_index(l+1,i,n,upper_bound))+" "+str(s_index(l,i,n,upper_bound))+" 0\n")
					clause_count += 2
		for i in range(1,n+1):
			cnf_file.write("-"+str(nop_index(l,n,upper_bound))+" "+str(s_index(l+1,i,n,upper_bound))+" -"+str(s_index(l,i,n,upper_bound))+" 0\n")
			cnf_file.write("-"+str(nop_index(l,n,upper_bound))+" -"+str(s_index(l+1,i,n,upper_bound))+" "+str(s_index(l,i,n,upper_bound))+" 0\n")
			clause_count += 2
	cnf_file.close()
	return clause_count


def search_k(start,end,cnf_path,n,upper_bound):
	if end - start == 2:
		if (not nop_k(start,cnf_path,n,upper_bound)) and nop_k(start+1,cnf_path,n,upper_bound):
			return start
		else:
			return start + 1
	if end - start == 1:
		return start
	left_one = nop_k(int((start+end)/2),cnf_path,n,upper_bound)
	right_one = nop_k(int((start+end)/2)+1,cnf_path,n,upper_bound)
	if left_one == False and right_one == True:
		return int((start+end)/2)
	if left_one == False and right_one == False:
		return search_k(int((start+end)/2)+1,end,cnf_path,n,upper_bound)
	if left_one == True and right_one == True:
		return search_k(start,int((start+end)/2),cnf_path,n,upper_bound)
	print("Should not get here.")
	return "Nothing"


def nop_k(k,cnf_path,n,upper_bound):
	if k in sat_instances:
		return sat_instances[k][0]
	subprocess.run(["cp","temp_signed.cnf","temp_signed_ongoing.cnf"])
	cnf_file = open("temp_signed_ongoing.cnf",'a')
	cnf_file.write(str(nop_index(k,n,upper_bound))+" 0\n")
	cnf_file.close()
	start_time = time.time()
	result = subprocess.run(["../sat_solver/lingeling","temp_signed_ongoing.cnf"],capture_output=True).stdout
	end_time = time.time()
	subprocess.run(["rm","temp_signed_ongoing.cnf"])
	if b'UNSATISFIABLE' in result:
		sat_instances[k] = (False,end_time-start_time)
		return False
	else:
		sat_instances[k] = (True,end_time-start_time)
		new_result = result.decode("utf-8")
		sat_index = new_result.find("SATISFIABLE")
		start_index = new_result[sat_index:].find("v")
		end_index = new_result[sat_index:].find(" 0")
		r_list = []
		for num in new_result[sat_index+start_index:sat_index+end_index].split():
			if not num == 'v':
				if int(num) > 0:
					if int(num) > pow(n,3) * upper_bound and int(num) <= (pow(n,3)+pow(n,2)) * upper_bound:
						num_we_use = int(num) - pow(n,3) * upper_bound
						p = int(num_we_use / (n*upper_bound)) + 1
						q = int((num_we_use - (p-1)*n*upper_bound)/upper_bound) + 1
						kk = num_we_use - (p-1)*n*upper_bound - (q-1)*upper_bound
						r_list.append((p,q,kk))
		operation_lists[len(r_list)] = r_list
		return True


skeleton()