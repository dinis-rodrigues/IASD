from search import *
from ana import *
import time

start = time.time()





def main():
	file = 'example.txt'

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
		fs.close()
	else:
		problem.save(fs, None)
		#print("not done")
		end = time.time()
		print(end - start)
		fs.close()




main()
