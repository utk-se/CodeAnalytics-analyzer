from cadistributor import log
import os
import lizard
import numpy as np
'''
Provide root dir; gets the metrics
provide list of  to track
frequency()
Repo r = repoobj(repopath or list of filenames)
repo would turn files into codeblocks
codeblock is given a set of lines and converts to nparrays
repoobj.methods.frequency(list of metrics, list of languages) - set of codeblocks would be 3d array
numpy good
'''

'''
given a line, return this
'''


class LineMetric:
    pass


'''
provide the path
repo is collection of codeblocks

'''


class CodeRepo:

    def __init__(self, input_path, debug=False):
        self.debug = debug
        self.root_path = input_path
        self.supported_filetypes = ['py', 'cpp', 'js', 'h', 'java']
        # TODO: support input_path being a list of files
        self.file_paths = []
        self.num_directories = 0
        self.num_extensions = 0
        self.max_depth = 0

        if not os.path.exists(input_path):
            raise FileNotFoundError('{} does not exist'.format(input_path))

        # retrieve filenames and get directory metrics
        depth = 0
        file_extensions = set()
        for subdir, dirs, files in os.walk(input_path):
            for filep in files:
                file_path = subdir + os.sep + filep

                # get file extension
                file_extension = file_path.split(os.sep)[-1].split('.')[-1]
                if len(file_extension) <= 1:
                    file_extension = ''
                file_extensions.add(file_extension)

                # get max depth
                depth = file_path.count(os.sep)
                if depth > self.max_depth:
                    self.max_depth = depth

                # get num directories
                self.num_directories += len(dirs)

                if file_extension not in self.supported_filetypes:
                    continue

                file_paths.append(file_path)

        self.num_extensions = len(list(file_extensions))

        # retrieve contents of paths


'''
Set of raw characters. Uses a function to get character begin and end
'''


class CodeFile(CodeRepo):
    def __init__(self, pathid):
        # read in the file


class CodeBlock:
    # np.array()
    def __init__(self, parent, ):
        # super().__init__()

        pass

    self.lang = None
    self.type = None


if __name__ == '__main__':
    repo = CodeRepo('path')
    t = CustomType
    # Custom codeblock types: should iterate over File and return set of start & end indices
    # CommentBlock
    # optionally add a list
    repo.track(types=['method', 'class', 'token'])
    # examples
    # get method ids
    # get total line of code
    repo.count()
    repo.split()
    # get total line of python code
    len(repo.where(type='method', lang='py').count('\n'))
    # get total line of python code inside classes
    # number of methods
    # splitby
    repo.where(types='method').count()
    # number of files

    # ben's map
    arr_import = repo.where(types=  # implement

    # average width of function
    repo.where(type='function').splitby('newline').average(metrics='length')
