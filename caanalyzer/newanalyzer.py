from cadistributor import log
import os
import lizard
import numpy as np
import pandas as pd
from .util import get_file_extension
from .exceptions import UnsupportedLanguageException


class CodeRepo:

    def __init__(self, input_path, languages=['py', 'cpp', 'js', 'h', 'java'], debug=False):
        self.debug = debug
        self.root_path = input_path
        self.supported_filetypes = ['py', 'cpp', 'js', 'h', 'java']

        # make sure that specified languages are supported
        for extension in languages:
            if extension not in self.supported_filetypes:
                raise UnsupportedLanguageException(
                    '{} is not a supported file extension. Supported file extensions include {}'.format(extension, self.supported_filetypes))

        # TODO: support input_path being a list of files
        self.file_paths = []
        self.num_directories = 0
        self.num_extensions = 0
        self.max_depth = 0
        self.num_files = 0
        self.token_index = None

        if not os.path.exists(input_path):
            raise FileNotFoundError('{} does not exist'.format(input_path))

        # retrieve filenames and get directory metrics
        depth = 0
        file_extensions = set()
        for subdir, dirs, files in os.walk(input_path):

            # get num directories and num files
            self.num_directories += len(dirs)
            self.num_files += len(files)

            # get max depth
            depth = subdir.count(os.sep)
            if depth > self.max_depth:
                self.max_depth = depth

            for filep in files:
                file_path = subdir + os.sep + filep

                # get file extension
                file_extension = get_file_extension(file_path)
                file_extensions.add(file_extension)

                if file_extension not in self.supported_filetypes:
                    continue

                self.file_paths.append(file_path)

        self.num_extensions = len(list(file_extensions))

    '''
    For each file, and each type of token
    retrieve the start and end indices for this
    TODO: developing as O(n^2) until better understanding of ast parsing
    '''

    def construct_index(self, token_types, metrics):
        raise NotImplementedError

    '''
    convienience functions / wrappers for common metrics,
    querying dataframe, statistical methods
    '''

    def where(self, **kwargs):
        raise NotImplementedError

    def split(self, token_types):
        raise NotImplementedError

    def median(self, metric):
        raise NotImplementedError

    def mode(self, metric):
        raise NotImplementedError

    def average(self, metric):
        raise NotImplementedError

    def value(self, metric):
        raise NotImplementedError

    def count(self):
        raise NotImplementedError

    def to_dataframe(self, outfile=None):
        raise NotImplementedError


'''


Set of raw characters. Uses a function to get character begin and end
'''


class CodeFile(CodeRepo):
    def __init__(self, path):
        # read in the file
        pass


class CodeBlock:
    # np.array()
    def __init__(self, parent):
        # super().__init__()

        pass

        self.lang = None
        self.type = None


if __name__ == '__main__':
    '''
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
    arr_import = repo.where(types=# implement

    # average width of function
    repo.where(type='function').splitby('newline').average(metrics='length')
    '''
    repo = CodeRepo('.')
