#! /usr/bin/env python

import argparse 
import os
import lizard
import json
from pydriller import RepositoryMining, GitRepository

#-------------------Setting/getting the args---------------------------------------------
parser = argparse.ArgumentParser(description="Arguments for CodeAnalytics-analyzer")

parser.add_argument('-p', type=str, required=True, 
    help='Required. The path to a repo containing code.')

# TODO: replace if statements with logger
parser.add_argument('-d', action='store_true', help='Enable debugging')
args = parser.parse_args()
#-------------------Done setting/getting args--------------------------------------------

def main():
    
    repo_obj = {
        "file_objs": [],
        "num_lines": 0,
        "num_files": 0
    }

    supported_filetypes = ['py', 'cpp', 'js', 'h', 'java']
    # Walk through all files
    for subdir, dirs, files in os.walk(args.p):  # go through every file within a given directory
        for file in files:
            file_path = subdir + os.sep + file
            file_extension = file_path.split('.')[-1]
            # For each file check file type
            if file_extension in supported_filetypes:
                repo_obj["num_files"] += 1
                file_obj = {
                    "num_lines": 0,
                    "file_extension": file_extension,
                    "file_name": file_path,
                    "methods": [],  #  Pair/Tuples with start and end lines of methods/classes
                    "classes": [],
                    "lines": [],
                    "nloc": None
                }

                i = lizard.analyze_file(file_path)
                # what's in i?
                if args.d:
                    print(i.function_list)
                    print(i.token_count)
                    print(i.nloc)

                # Go thru each line in the file
                for line in file:
                    file_obj["num_lines"] += 1

                    line_obj = {
                        "is": [None, None, None, None, None, None, None],
                        "start_index": None,  # int specifying where line starts
                        "has_tabs": None,  # boolean for existence
                        "end_index": None  # int specifying where line ends
                    }
                    
                    # detecting imports

                    # Add line obj to file obj
                    file_obj["line_objs"].append(line_obj)
                # Add file obj to repo obj
                repo_obj["file_objs"].append(file_obj)
if __name__ == "__main__":
    main()