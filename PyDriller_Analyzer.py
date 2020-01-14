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
	pyminifier? -- Might potentially use this for analyzing python code, such as examing imports and etc.
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

def handle_py_file(file, numlines):
	
	ftype = "Python"
	list_of_imports = []
	list_of_functions = []
	list_of_vars = []
	num_funcs = 0
	total_width = 0
	total_funct_width = 0
	total_funct_height = 0
	avg_width = 0
	avg_funct_height = 0
	avg_funct_width = 0
	num_vars = 0
	funct_flag = False

	# Open the file
	with open(file) as f:
		for line in f:
			total_width += len(line)
			# determine the number of variables
			if(line.find("=") > -1):
				parsed_line = line.split(' ', 20)
				for i in range(len(parsed_line)):
					if parsed_line[i] == '=':
						# modify any variables that indicate the index due to the fact we only want the variable name
						if parsed_line[i-1].find("["):
							parsed_line[i-1] = parsed_line[i-1].rsplit('[', 1)[0]
						# verify if the variable is already in the list
						if parsed_line[i-1].replace('\t', '') not in list_of_vars:
							list_of_vars.append(parsed_line[i-1].replace('\t', ''))
							num_vars += 1
			
			# determine the average height and width of functions
			if funct_flag == True:
				if line is "":
					pass
				elif (len(line) - len(line.lstrip())) == 0:
					funct_flag = False
				else:
					total_funct_height += 1
					total_funct_width += len(line.rstrip())

			# determine the number of functions
			if len(line.split()) > 1 and line.split(' ', 1)[0] == 'def':
				funct_flag = True
				num_funcs += 1
				list_of_functions.append(line.split(' ', 1)[1].replace(':', ''))

			# determine the number of imports
			if line.split(' ', len(line))[0] == 'import' or line.split(' ', len(line))[0] == 'from':
				list_of_imports.append(line.split(' ', len(line))[1])
				if(list_of_imports[-1].find(',') > -1):
					list_of_imports[-1] = list_of_imports[-1].replace(',', '')
					list_of_imports.append(line.split(' ', len(line))[2])

	num_dependencies = len(list_of_imports)
	# remove extra characters from lists such as tabs and new lines
	list_of_vars = list(map(str.strip, list_of_vars))
	list_of_imports = list(map(str.strip, list_of_imports))
	list_of_functions = list(map(str.strip, list_of_functions))

	avg_width = int(total_width / numlines) # calculate average width of entire file
	avg_funct_width = int(total_funct_width / total_funct_height) # calculate average function width
	avg_funct_height = int(total_funct_height / num_funcs) # calculate average function height

	return ftype, num_dependencies, list_of_imports, avg_width, num_funcs, list_of_functions, num_vars, list_of_vars, avg_funct_height, avg_funct_width

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
				ftype, num_dependencies, import_list, avg_width, num_funcs, funcs_list, num_vars, vars_list, avg_func_height, avg_func_width = handle_py_file(file, nlines)
			elif cpp or c: 
				ftype = handle_c_file(file)
			elif js: 
				ftype = handle_js_file(file)
			else: 
				ftype = handle_java_file(file)

			print("Filename: " + str(file))
			print("Language: " + str(ftype))
			print("numlines: " + str(nlines))
			print("Average width of file: " + str(int(avg_width)))
			print("Number of functions: " + (str(num_funcs)))
			print("Function list: ", funcs_list)
			print("Average function height: ", avg_func_height)
			print("Average function width: ", avg_func_width)
			print("Number of Dependencies: " + str(num_dependencies))
			print("Imports: ", import_list)
			print("Number of variables: " + str(num_vars))
			print("List of variables: ", vars_list)
			print("\n")
		
if __name__ == "__main__":
    main_function()