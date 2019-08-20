# transform-order-by-reversals
Generate SAT-solver data then use a pipeline to solve the `sort by reversal` problem.

## SAT solver

The SAT solver can be found [here](https://github.com/arminbiere/lingeling). `lingeling` and `plingeling` are included in `/sat_solver`. Note that the `plingeling` uses one process.


## Running the scirpts
*Python Version == 3.7.3*  

## Unsigned version

`src/do_unsigned.py` takes an unsigned list as input and gives details about sat solving. Note that it uses `../sat_solver/plingeling` as the relative path. Taking the Cabbage data as an example,
	
	python3 do_unsigned.py 1 10 4 5 2 6 3 9 8 7
Output will be like:

	-----------------------------------------------------------
	List : ['1', '10', '4', '5', '2', '6', '3', '9', '8', '7']
	Elapsed time : 6.29525899887085
	Number of clauses : 827412
	Number of operations : 4
	Number of cycles : 4
	Running time of SAT instances :
    	NOP(9) satisfiable 1.7658510208129883
    	NOP(5) satisfiable 1.0251471996307373
    	NOP(6) satisfiable 1.2119133472442627
    	NOP(4) unsatisfiable 1.0366451740264893
	Optimal solution : [(2, 6, 2), (2, 10, 4), (4, 9, 1), (6, 7, 3)]
	-----------------------------------------------------------

## Signed version	

`src/do_signed.py` takes a signed list as input and gives details about sat solving, similarly. For example,

	python3 do_signed.py 5 -7 4 -1 6 2 -3
	
Output will be like:

	-----------------------------------------------------------
	List : ['5', '-7', '4', '-1', '6', '2', '-3']
	Elapsed time : 41.71333909034729
	Number of clauses : 239651
	Number of operations : 7
	Number of cycles : 1
	Number of positive / negative numbers : 4 / 3
	Running time of SAT instances :
    	NOP(1) unsatisfiable 0.37849879264831543
    	NOP(14) satisfiable 7.265217065811157
    	NOP(8) satisfiable 4.694403886795044
    	NOP(9) satisfiable 0.6392860412597656
    	NOP(5) unsatisfiable 0.6038990020751953
    	NOP(6) unsatisfiable 2.4456682205200195
    	NOP(7) unsatisfiable 24.897839784622192
	Optimal solution : [(1, 2, 2), (1, 6, 6), (2, 5, 4), (2, 6, 5), (3, 4, 3), (3, 5, 7), (3, 7, 1)]
	-----------------------------------------------------------
	
## Stats of unsigned version	
	
`src/stats2_unsigned.py` generates random unsigned lists, then solve them and put the statistics in an csv file. The number and length of list is based on the input. Usage: 

	python3 stats2_unsigned.py [length_of_list] [number_of_list]
	
For exmaple,

	python3 stats2_unsigned.py 7 10
	
It generates 10 lists with 7 numbers. Then the stats will be in `../data2/p_unsigned_7_10.csv`. `p` means that it uses `plingeling` instead of `lingeling`. 

	
`src/stats2_signed.py` generates random signed lists, similarly, then solve them and put the statistics in an csv file. The number and length of list is based on the input. Usage: 

	python3 stats2_signed.py [length_of_list] [number_of_list]
	
For exmaple,

	python3 stats2_signed.py 8 10
	
It generates 10 lists with 7 numbers. Then the stats will be in `../data2/p_signed_8_10.csv`. `p` means that it uses `plingeling` instead of `lingeling`. 


`cmp_src/sat_vs_ilp.py` takes the stats of SAT solver as input and run gurobi (integer linear programming, ilp) on the corresponding list. The comparison result is put in `cmp_data`. Usage:

	python3 sat_vs_ilp.py [version] [length_of_list] [number of list]

For example, 

	python3 sat_vs_ilp.py unsigned 8 10

It takes `/data2/p_unsigned_8_10.csv` as input. Then the output will be in `cmp_data/p_cmp_8_10.csv`. 
	
	

whrgrew


	


