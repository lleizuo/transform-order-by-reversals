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
	int_raw_list = []
	try:
		int_raw_list = [int(i) for i in raw_list]
	except ValueError:
		print("Please enter an integer list.")
		return
	if set(range(1,len(raw_list)+1)) != set([abs(i) for i in int_raw_list]):
		print("Your destination list is not valid.")
		return
	

skeleton()