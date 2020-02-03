#! /usr/bin/env python

import argparse 
import os
import lizard
import json

class Repo:
    def __init__(self):
        self.repo = {
            "file_objs": [],
            "num_lines": 0,
            "num_files": 0
        }

class File:
    def __init__(self, file_extension, file_path):
        self.file = {
            "num_lines": 0,
            "file_extension": file_extension,
            "file_name": file_path,
            "methods": [],  #  Pair/Tuples with start and end lines of methods/classes
            "classes": [],
            "line_objs": [],
            "nloc": None,
            "token_count": 0
        }
        
class Line:
    def __init__(self, line_num):
        self.line = {
            "index": line_num,
            "start_index": None,  # int specifying where line starts
            "num_tabs": 0,  # boolean for existence
            "end_index": None,  # int specifying where line ends
            "num_spaces": 0,
            "len": 0
        }

class Analyzer:
    '''
    Provided a repository, uses static code analysis to output data about 
    the shape of code. ie, it outputs information regarding the use of 
    whitespace, and the placement of code elements within a file.

    ignorefile: path to file containing rules for files to exclude from analysis. 
    Think of  a gitignore. # TODO: implement
    expand_tabs: This argument expects an int, representing the number of spaces 
    to represent tabs as.
    output_raw: Enabling this flag will add information about each line to the output
    json. This may significantly increase RAM usage and output size.
    Debug: This flag enables debug statements to be printed. # TODO: Use logger
    '''
    def __init__(self, , ignorefile=None, expand_tabs=4, output_raw=True, 
        debug=False):

        self.input_path = input_path
        self.output_path = output_path
        self.ignorefile = ignorefile
        self.expand_tabs = expand_tabs
        self.output_raw = output_raw
        self.debug = debug
        self.supported_filetypes = ['py', 'cpp', 'js', 'h', 'java']

        self.repo_obj = None

    ''' 
    returns the serializable dictionary that can be outputted as a json file
    Required argument: input_path - The path to a repo containing code.
    Optional arguments: output_path, the name/path to the output json file.
    '''
    def analyzeFile(self, input_path, output_path=None):
    
    '''
    repo_obj = {
        "file_objs": [],
        "num_lines": 0,
        "num_files": 0
    }
    '''
        repo_obj = Repo()
        '''
        TODO: instead of storing info about each line, we can store 
        one obj w/ a 'median file' object, which has metrics including 
        line-by-line data that is based off the other files.
        ? One for each lang? Potential issue: summing entire repo into 1 file
        seems overly reductive.
        median method
        first most likely positions for method, second.
        For each line, frequency of method declaration or body
        For file-level data: record avgs
        For line-level info - store frequency (ie, freq_newlines @ lineno x)
        ''' 

    # Walk through all files
    for subdir, dirs, files in os.walk(self.input_path):  # go through every file within a given directory
        # Exclude hidden files/directories 
        # (see https://stackoverflow.com/questions/13454164/os-walk-without-hidden-folders)
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']

        for filep in files:
        
            file_path = subdir + os.sep + filep
            file_extension = file_path.split('.')[-1]

            # For each file check file type
            if file_extension not in self.supported_filetypes:
                continue

            repo_obj["num_files"] += 1
            file_obj = {
                "num_lines": 0,
                "file_extension": file_extension,
                "file_name": file_path,
                "methods": [],  #  Pair/Tuples with start and end lines of methods/classes
                "classes": [],
                "line_objs": [],
                "nloc": None,
                "token_count": 0
            }

            i = lizard.analyze_file(file_path)

            file_obj["token_count"] = i.token_count

            # Append info about methods
            for func_dict in i.function_list:
                file_obj["methods"].append(func_dict.__dict__)

            # Go thru each line in the file
            with open(file_path) as file:
                for line_num, line in enumerate(file):
                    file_obj["num_lines"] += 1
                    # Don't bother with lines that are just a newline
                    if line == '\n':
                        continue

                    line_obj = {
                        "index": line_num,
                        "start_index": None,  # int specifying where line starts
                        "num_tabs": 0,  # boolean for existence
                        "end_index": None,  # int specifying where line ends
                        "num_spaces": 0,
                        "len": 0
                    }
                    # detect tabs & spaces
                    line_obj["num_tabs"] = line.count('\t')
                    line_obj["num_spaces"] = line.count(' ')
                    line_obj["len"] = len(line)
                    line = line.expandtabs(args.e)

                    # detect start & end index
                    line_obj["start_index"] = len(line) - len(line.lstrip())
                    line_obj["end_index"] = len(line.rstrip())
                    # TODO: detecting imports

                    # Add line obj to file obj
                    file_obj["line_objs"].append(line_obj)
            
            # Add file obj to repo obj
            repo_obj["file_objs"].append(file_obj)

    # Sum linecount
    for obj in repo_obj["file_objs"]:
        repo_obj["num_lines"] += obj["num_lines"]
    # Write the repo object to json
    with open(args.o, 'w') as outfile:
        json.dump(repo_obj, outfile, indent=2)


if __name__ == "__main__":
    main()