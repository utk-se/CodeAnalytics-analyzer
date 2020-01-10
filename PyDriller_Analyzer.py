#! /usr/bin/env python

import argparse 
import os
import lizard
import json
from pydriller import RepositoryMining, GitRepository

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

def calculate_num_lines(file):

	with open(file) as f:
		nlines = 0
		i = 0
		for i,l in enumerate(f):
			pass
	nlines = i+1
	return nlines

def handle_py_file(file):
	
	ftype = "Python"
	list_of_imports = []

	with open(file) as f:
		for line in f:
			if line.split(' ', len(line))[0] == 'import' or line.split(' ', len(line))[0] == 'from':
				list_of_imports.append(line.split(' ', len(line))[1])
				if(list_of_imports[-1].find(',') > -1):
					list_of_imports[-1] = list_of_imports[-1].replace(',', '')
					list_of_imports.append(line.split(' ', len(line))[2])

	num_dependencies = len(list_of_imports)
	list_of_imports = list(map(str.strip, list_of_imports))
	return ftype, num_dependencies, list_of_imports

def handle_c_file(file):

	ftype = "C"
	return ftype

def handle_js_file(file):

	ftype = "Javascript"
	return ftype

def handle_java_file(file):

	ftype = "Java"
	return ftype

def main_function():

	files = GitRepository(args.p).files()
	for file in files:
		cpp = file.endswith('.cpp')
		c = file.endswith('.c')
		py = file.endswith('.py')
		js = file.endswith('.js')
		java = file.endswith('.java')
		
		if cpp or py or js or java:
	
			nlines = calculate_num_lines(file)

			if py: 
				ftype, num_dependencies, import_list = handle_py_file(file)
			elif cpp or c: 
				ftype = handle_c_file(file)
			elif js: 
				ftype = handle_js_file(file)
			else: 
				ftype = handle_java_file(file)

			print("Filename: " + str(file))
			print("Language: " + str(ftype))
			print("numlines: " + str(nlines))
			print("Imports: ", import_list)
			print("Number of Dependencies: " + str(num_dependencies))
			print("\n")
		
if __name__ == "__main__":
    main_function()