#! /usr/bin/env python

import argparse 
import os
import lizard
import json

#-------------------Setting/getting the args---------------------------------------------
parser = argparse.ArgumentParser(description="Arguments for CodeAnalytics-analyzer")

parser.add_argument('-p', type=str, required=True, 
    help='Required. The path to a repo containing code.')

# TODO: replace if statements with logger
parser.add_argument('-d', action='store_true', help='Enable debugging')
# TODO: add ignore file
parser.add_argument('-i', type=str, help="Specifies an ignorefile. ")
# How much to expand tabs (default: off)
parser.add_argument('-e', type=int, default=4, help="Specifies number of spaces to represent tabs as.")
parser.add_argument('-o', type=str, default="outfile.json", help="Specify name of outfile")
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
        # Exclude hidden files/directories 
        # (see https://stackoverflow.com/questions/13454164/os-walk-without-hidden-folders)
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']

        for filep in files:
        
            file_path = subdir + os.sep + filep
            file_extension = file_path.split('.')[-1]

            # For each file check file type
            if file_extension not in supported_filetypes:
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
                try:
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
                
                except UnicodeDecodeError:
                    continue

            # Add file obj to repo obj
            repo_obj["file_objs"].append(file_obj)

    # Sum linecount
    for obj in repo_obj["file_objs"]:
        repo_obj["num_lines"] += obj["num_lines"]
    # Write the repo object to json
    with open(args.o, 'w') as outfile:
        json.dump(repo_obj, outfile)


if __name__ == "__main__":
    main()