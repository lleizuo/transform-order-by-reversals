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





skeleton()