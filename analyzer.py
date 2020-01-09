import argparse 
import os
import lizard
import json

#-------------------Setting/getting the args---------------------------------------------
parser = argparse.ArgumentParser(description="Arguments for CodeAnalytics-analyzer")
parser.add_argument('-p', type=str, required=True, 
    help='Required. The path to a repo containing code.')
args = parser.parse_args()
#-------------------Done setting/getting args--------------------------------------------

def main_function():
    arr = [] # array containing every analyzed file
    for subdir, dirs, files in os.walk(args.p): # go through every file within a given directory
        for file in files:
            file_path = subdir + os.sep + file
            if file_path.endswith('.cpp') or file_path.endswith('.py') or file_path.endswith('.js') or file_path.endswith('.java'):
                i = lizard.analyze_file(file_path)
                #print(i.function_list[0].__dict__)
                my_json = json.dumps(i.function_list[0].__dict__, indent=4)
                arr.append(my_json)

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