# transform-order-by-reversals
Generate SAT-solver data then use a pipeline to solve the `sort by reversal` problem.

Note that the `plingeling` uses one process.


## File structure & running the scirpts:
*Python Version == 3.7.3*  

`do_unsigned.py` takes an unsigned list as input and gives details about sat solving. Taking the Cabbage data as an example,
	
	python3 do_unsigned.py 1 10 4 5 2 6 3 9 8 7
Output will be like:

	List : ['1', '10', '4', '5', '2', '6', '3', '9', '8', '7']
	Elapsed time : 6.29525899887085
	Number of clauses : 827412
	Number of operations : 4
	Running time of SAT instances :
    	NOP(9) satisfiable 1.7658510208129883
    	NOP(5) satisfiable 1.0251471996307373
    	NOP(6) satisfiable 1.2119133472442627
    	NOP(4) unsatisfiable 1.0366451740264893
	Optimal solution : [(2, 6, 2), (2, 10, 4), (4, 9, 1), (6, 7, 3)]
`do_signed.py` takes a signed list as input and gives details about sat solving, similarly. For example,

	python3 do_signed.py 5 -7 4 -1 6 2 -3
	
`stats2_unsigned.py` generates random unsigned lists, then solve them and put the statistics in an csv file. The number and length of list is based on the input. Usage: 

	python3 stats2_unsigned.py [length_of_list] [number_of_list]
	
For exmaple,

	python3 stats2_unsigned.py 7 10
	
It generates 10 lists with 7 numbers.
	
	
ww


	


