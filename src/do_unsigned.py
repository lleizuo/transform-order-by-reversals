import subprocess
import sys
import ast
import time

def skeleton():
	raw_list = sys.argv[1:]
	start_time = time.time()
	result = subprocess.run(["python3","unsigned.py"] + raw_list,capture_output=True).stdout
	end_time = time.time()
	decode_result = result.decode("utf-8")
	flagpos = decode_result.find("dictflag")
	flagpos2 = decode_result.find("operflag")
	parse_result = [int(num) for num in decode_result[:flagpos].split()]
	detaildict = ast.literal_eval(decode_result[flagpos+9:flagpos2])
	detailoper = ast.literal_eval(decode_result[flagpos2+9:])
	print("List : "+str(raw_list))
	print("Elapsed time : "+str(end_time-start_time))
	print("Number of clauses : "+str(parse_result[0]))
	print("Number of operations : "+str(parse_result[1]))
	print("Running time of SAT instances : ")
	for elem in detaildict:
		print("    "+str(elem)+" "+str(TFtoSAT(detaildict[elem][0]))+" "+str(detaildict[elem][1]))
	if len(detailoper) > 0:
		optimal_solution = detailoper[min(detailoper)]
		print("Optimal solution : "+str(optimal_solution))



def TFtoSAT(truefalse):
	if truefalse:
		return "satisfiable"
	else:
		return "unsatisfiable"


skeleton()