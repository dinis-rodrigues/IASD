from search import *
from solution import *

def main():
	file = sys.argv[1]

	fh = open(file, "r")
	print("0")
		
	problem = ASARProblem()
	problem.load(fh)
	print("1")

	solution = astar_search(problem, problem.heuristic)
	print("2")

	fs = open("sol.txt", "w")
	if(solution != None):
		problem.save(fs, solution.state)
		print("done")
	else:
		problem.save(fs, None)
		print("not done")



main()
