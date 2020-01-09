from pydriller import RepositoryMining, GitRepository
import argparse 
import os
import lizard
import json

'''
List of dependencies: 
	pydriller
	lizard
	git
	python3
'''

#-------------------Setting/getting the args---------------------------------------------
parser = argparse.ArgumentParser(description="Arguments for CodeAnalytics-analyzer")
parser.add_argument('-p', type=str, required=True, 
    help='Required. The path to a repo containing code.')
args = parser.parse_args()
#-------------------Done setting/getting args--------------------------------------------

def main_function():

	files = GitRepository(args.p).files()
	for file in files:
		cpp = file.endswith('.cpp')
		py = file.endswith('.py')
		js = file.endswith('.js')
		java = file.endswith('.java')
		
		if cpp or py or js or java:
	
			with open(file) as f:
				nlines = 0
				i = 0
				for i,l in enumerate(f):
					pass
			nlines = i+1
			if py: ftype = "Python"
			elif cpp: ftype = "C++"
			elif js: ftype = "Javascript"
			else: ftype = "Java"
			print("File: " + str(file))
			print("File type: " + str(ftype))
			print('{:>10}'.format("numlines: ") + str(nlines))
		
if __name__ == "__main__":
    main_function()