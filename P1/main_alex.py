from search import *
from solution import *
import time

start = time.time()





def main():
	file = 'simple5.txt'

	fh = open(file, "r")
	# print("0")

	problem = ASARProblem()
	problem.load(fh)
	# print("1")

	solution = astar_search(problem, problem.heuristic)
	# print("2")

	fs = open("sol.txt", "w")
	if(solution != None):
		problem.save(fs, solution.state)
		#print("done")
		end = time.time()
		print(end - start)
		print('Number of generated nodes: ', problem.n_nodes)
		print('Number of legs+1: ', problem.n_legs +1)
		print('Node depth',solution.depth)
		fs.close()
	else:
		problem.save(fs, None)
		#print("not done")
		end = time.time()
		print(end - start)
		print('Number of generated nodes: ', problem.n_nodes)
		print('Number of legs+1: ', problem.n_legs +1)
		print('Node depth',solution.depth)
		fs.close()




main()
