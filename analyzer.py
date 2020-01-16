import argparse 
import os
import lizard
import json
import CppHeaderParser

#-------------------Setting/getting the args---------------------------------------------
parser = argparse.ArgumentParser(description="Arguments for CodeAnalytics-analyzer")
parser.add_argument('-p', type=str, required=True, 
    help='Required. The path to a repo containing code.')
args = parser.parse_args()
#-------------------Done setting/getting args--------------------------------------------

def main_function():

    # Empty output objects to be populated & dumped
    repo_obj = {
        "file_objs": [],
        "commit-id": None,
        "repo-url": None,
        "num_lines": None,
        "date": None
    }

    file_obj = {
        "num_lines": None,
        "file_extension": None,
        "methods": [],
        "classes": []
    }

    method_obj = {
        "parent_file": None,
        "parent_class": None
    }

    supported_filetypes = ['py', 'cpp', 'js', 'h', 'java']
    arr = [] # array containing every analyzed file
    for subdir, dirs, files in os.walk(args.p): # go through every file within a given directory
        for file in files:
            file_path = subdir + os.sep + file
            file_extension = file_path.split('.')[-1]
            print(file_extension)
            if file_extension in supported_filetypes:

                # Lizard cyclomatic complexity analysis
                i = lizard.analyze_file(file_path)
                if len(i.function_list) > 0:
                    print(i.function_list[0].__dict__)

                    # Throw the lizard results into the json file
                    my_json = json.dumps(i.function_list[0].__dict__, indent=4)
                    arr.append(my_json)

                # Parse C/C++ from a header file
                # TODO: See if this works for .cpp files
                if file_extension is 'h':
                    header = CppHeaderParser.CppHeader(file_path)
                    print(header)
                    break

    with open('data.json', 'w') as outfile:
        outfile.write("[\n")
        first = True
        for item in arr:
            if first == True:
                first = False
            else:
                outfile.write(",\n")
            outfile.write(item)
        outfile.write("\n]")

if __name__ == "__main__":
    main_function()