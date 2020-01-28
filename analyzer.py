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

class repo_obj:
	def __init__(self):
		self.file_objs = []
		self.num_lines = None
		self.num_files = 0
	
	def update_num_files(self):
		self.num_files += 1

class file_obj:
	def __init__(self):
		self.file_name = None
		self.file_extension = None
		self.num_lines = None
		self.methods = []  # Pair/Tuples with start and end lines of methods/classes
		self.classes = []
		self.lines = []

	def calculate_num_lines(self, file):

		with open(file) as f:
			self.num_lines = 0
			i = 0
			for i,l in enumerate(f):
				pass
		self.num_lines = i+1
		return self.num_lines

class line_obj:
	def __init__(self):
		# Proposed usage: [var, func call, loop, conditional, return,
    	# assignment, include/import]
		# or is = 0...7 to indicate which it is
    	# 'is' subject to change. These could be used for different heatmap 'colors'
		self.line_type = None
		self.start_index = None  # int specifying where line starts
		self.has_tabs = None  # boolean for existence
		self.end_index = None  # int specifying where line ends

	def find_start_index(self, line):
		self.start_index = len(line) - len(line.lstrip())

	def find_end_index(self, line):
		self.end_index = len(line)

#-------------------Setting/getting the args---------------------------------------------
parser = argparse.ArgumentParser(description="Arguments for CodeAnalytics-analyzer")
parser.add_argument('-p', type=str, required=True, 
    help='Required. The path to a repo.')
args = parser.parse_args()
#-------------------Done setting/getting args--------------------------------------------

def handle_py_file(file, new_file):
	
	with open(file) as f:
		for line in f:
			new_line = line_obj()
			if line.startswith('\t'):
				new_line.has_tabs = True
			new_line.find_start_index(line)
			new_line.find_end_index(line)

			if (line.find('class') != -1 or line.find('Class') != -1) and line.find(':') != -1:
				parsed_line = line.split(' ', 2)
				#new_file.classes.append(parsed_line[1])
			new_file.lines.append(new_line)
	ftype = "Python"
	return ftype

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

	new_repo = repo_obj()

	file_types = ['.cpp', '.c', '.py', '.js', '.java']
	files = GitRepository(args.p).files()
	for file in files:
		
		new_repo.update_num_files()

		extension = os.path.splitext(file)[1] # get the file extension

		new_file = file_obj() # instantiate a new file object
		new_file.file_name = file
		new_file.file_extension = extension
		new_file.calculate_num_lines(file)

		if extension in file_types:

			if extension == '.py': 
				ftype = handle_py_file(file, new_file)
			elif extension == '.cpp' or extension == '.c': 
				ftype = handle_c_file(file)
			elif extension == '.js': 
				ftype = handle_js_file(file)
			else: 
				ftype = handle_java_file(file)

		print("Filename: " + str(new_file.file_name))
		print("Extension: " + str(new_file.file_extension))
		print("Numlines: " + str(new_file.num_lines))
		new_repo.file_objs.append(new_file)
	with open('data.json', 'w') as f:
		data = json.dumps(new_repo, default=lambda o: o.__dict__, indent=4)
		f.write(data)

if __name__ == "__main__":
    main_function()