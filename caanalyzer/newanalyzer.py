import os

import lizard
import numpy as np
import pandas as pd
from cadistributor import log
from typing import Optional, Collection, Union
from pandas.api.extensions import ExtensionDtype
from .exceptions import UnsupportedLanguageException
from .util import get_file_extension
from hashlib import md5
from typing import List, Callable, Union, Tuple
from pathlib import Path

Num = Union[int, float]


class CodeRepo:
    # TODO: type annotate this
    def __init__(self, input_path, tokenizers, metrics: List[Callable[[str], Num]], dataframe=None, languages=['.py', '.cpp', '.js', '.h', '.java'],
                 debug=False):

        # self.debug = debug
        self.root_path = input_path
        self.supported_filetypes = ['.py', '.cpp', '.js', '.h', '.java']
        hasher = md5()
        # make sure that specified languages are supported
        for extension in languages:
            if extension not in self.supported_filetypes:
                raise UnsupportedLanguageException(
                    '{} is not a supported file extension. Supported file extensions include {}'.format(extension, self.supported_filetypes))

        self.file_paths = []
        self.num_directories = 0
        self.num_extensions = 0
        self.max_depth = 0
        self.num_files = 0

        # TODO: verify language support from tokenizers
        self.tokenizers = tokenizers
        self.metrics = metrics

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
                file_extension = Path(file_path).suffix
                file_extensions.add(file_extension)

                if file_extension not in languages:
                    continue

                self.file_paths.append(file_path)

        self.num_extensions = len(list(file_extensions))
        self.df = dataframe

        # get intersection of specified languages and existing languages
        self.languages = set(languages) & file_extensions
        log.info('languages found: {}'.format(self.languages))
        log.info('number of valid files found: {}'.format(len(self.file_paths)))
        # if the dataframe is empty; set up initial columns and insert file data
        # TODO: robustness: check for malformed input dataframes

        self.tokenizer_names = []
        for tokenizer in self.tokenizers:
            self.tokenizer_names.extend(tokenizer.keys())

        self.metric_names = ['line_start', 'char_start',
                             'line_end', 'char_end']
        self.metric_names.extend(list(self.metrics.keys()))

        log.info('Tokenizers: {}\n Metrics: {}'.format(
            self.tokenizer_names, self.metric_names))
        if self.df is None:
            mi = pd.MultiIndex.from_product([self.languages, self.file_paths, self.tokenizer_names], names=[
                'language', 'file_path', 'token_type'])
            self.df = pd.DataFrame(index=mi, columns=self.metric_names)

        print(self.df.head())

    '''
    Index the code repository into a dataframe for metric gathering
    For each file, and each type of token
    retrieve the start and end indices for this
    # TODO: tokenizer merging
    # TODO: each tokentype get its own table?
    any
    columns: filename, md5hash?, is_file, <is_tokentype>, <token_start>, <token_stop>

    case matrix        no new columns new columns
    no new files       do nothing     add & populate columns, no new rows
    new/modified files add new rows   do above, then add new rows
    '''

    def index(self):

        # any existing files with missing token columns need to be updated

        token_columns.extend(
            ['line_start', 'char_start', 'line_end', 'char_end'])

        # get difference between existing columns and current columns
        new_token_cols = token_columns - set(self.df.columns)

        # for each new column, calculate the values
        # get all current files
        # exception case: old files are not available: fill na
        self.df.reindex(columns=columns)

        # for any new files, process tokens

        # construct rows with new files for indexing

        # calculate metrics for all metrics with na values
    '''
    convienience functions / wrappers for common metrics,
    querying dataframe, statistical methods
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


'''

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
    arr_import = repo.where(types=# implement
'''
# average width of java function
# repo.where(type='function', lang='java').groupby(
#     'line').average(metric='length')
