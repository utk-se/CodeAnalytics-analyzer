import os

import lizard
import numpy as np
import pandas as pd
from cadistributor import log
from typing import Optional, Collection, Union
from pandas.api.extensions import ExtensionDtype
from .exceptions import UnsupportedLanguageException, MalformedDataFrameException
from .util import get_file_extension, flatten_list, tokenizer_keys_to_instances
from hashlib import md5
from typing import List, Callable, Union, Tuple
from pathlib import Path

Num = Union[int, float]

'''
Container for code repository.
TODO: consider minor refactor to become pandas extension
https://pandas.pydata.org/pandas-docs/stable/development/extending.html
ie, df.index_repo(), df.mean() versus repo.df.mean(), repo.index()
'''


class CodeRepo:
    # TODO: type annotate this
    def __init__(self, input_path, dataframe=pd.DataFrame(), languages=['.py', '.cpp', '.js', '.h', '.java']):

        self.supported_filetypes = set(
            ['.py', '.cpp', '.js', '.h', '.java']) & set(languages)

        # make sure that specified languages are supported
        for extension in languages:
            if extension not in self.supported_filetypes:
                raise UnsupportedLanguageException(
                    '{} is not a supported file extension. Supported file extensions include {}'.format(extension, self.supported_filetypes))

        self.register_path(input_path, append=False)

        self.default_columns = ['line_start', 'line_end', 'char_start',
                                'char_end']

        # get intersection of specified languages and existing languages
        log.info('languages found: {}'.format(self.languages))
        log.info('number of valid files found: {}'.format(len(self.file_paths)))

        self.indexed = False
        # TODO: robustness: check for malformed input dataframes
        self.tokenizers = None
        self.metrics = None
        self.tokenizer_names = []
        self.metric_names = []

    '''
    For now, only track one path at a time. The code is developed
    in such a way that it should straightforward to track multiple.
    Append = true: Collect stats and add files to index from a new repository
    as well as old.
    '''

    def register_path(self, input_path, append=True):
        if not append:
            self.file_paths = []
            self.file_extensions = []
            self.num_directories = 0
            self.num_extensions = 0
            self.max_depth = 0
            self.num_files = 0

        self.root_path = input_path

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
                file_path = Path(file_path)

                # get file extension
                file_extension = file_path.suffix
                file_extensions.add(file_extension)

                if file_extension not in languages:
                    continue

                self.file_paths.append(str(file_path))
                self.file_extensions.append(file_extension)

        self.num_extensions = len(list(file_extensions))
        self.languages = set(self.languages) & file_extensions
        # self.df = dataframe

    def unprocessed_tokens(self):
        if self.tokenizers is None:
            return []
        elif not df.empty:
            return set(flatten_list(self.tokenizer_names)) - \
                set(self.df.index.get_level_values('token_type').unique())
        else:
            return flatten_list(self.tokenizer_names)

    '''
    return metrics present in the index
    '''

    def unprocessed_metrics(self):
        if self.metrics is None:
            return []
        elif not df.empty:
            return set(self.metric_names) - set(self.df.columns)
        else:
            return self.metric_names

    '''
    return files that have been indexed
    '''

    def unprocessed_files(self):
        if not df.empty:
            return set(self.file_paths) - set(
                self.df.index.get_level_values('file_path').unique())
        else:
            return self.file_paths

    '''
    Retrieve previously processed filenames.
    if intersection=True, return only filenames that exist 
    within the scope of the current repository
    '''

    def processed_files(self, intersection=False):
        if self.df.empty:
            return []
        elif intersection:
            return set(self.file_paths) & set(
                self.df.index.get_level_values('file_path').unique())
        else:
            return self.df.index.get_level_values('file_path').unique()

    def processed_metrics(self, intersection=False):
        if self.df.empty:
            return []
        elif intersection:
            return set(
                self.df.columns) & set(self.metric_names)
        else:
            return list(self.df.columns)

    '''
    return true if a repository has been indexed
    '''

    def indexed(self):
        return self.indexed
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

    Skip other files: If filepaths from outside the repo are found in the dataframe,
    do not attempt to load them. Keep this 'True' if you don't intend 
    to mix data from multiple repositories.
    '''

    def index(self, tokenizers, metrics: List[Callable[[str], Num]]):
        # TODO: verify language support from tokenizers
        self.tokenizers = tokenizers
        self.metrics = metrics

        log.info('Indexing this repository...')

        self.tokenizer_names = []
        for tokenizer in self.tokenizers:
            self.tokenizer_names.append(tokenizer.keys())

        self.metric_names = list(self.metrics.keys())

        # determine non-preexisting metrics to save time if reindexing or
        # provided dataframe at initialization

        new_tokenizers = self.unprocessed_tokens()
        new_metrics = self.unprocessed_metrics()
        new_files = self.unprocessed_files()
        existing_files = self.processed_files()
        existing_metrics = self.existing_metrics()

        # iterate through existing files and calculate any new metrics
        # if we have new tokenizers or new metrics we will have to revisit all files
        # New
        if len(new_tokenizers) != 0:

            # if we have existing files, process these first with
            # the updated metrics
            for input_path, lang in zip(list(existing_files), [get_file_extension(fp) for fp in existing_files]):

                # check that the file exists
                if not os.path.exists(input_path):
                    log.warn('Previously indexed file {} not found. This may result in NaN values'.format(
                        input_path))
                    continue
                with open(input_path) as fin:
                    codestr = fin.read()
                    codestr_lines = codestr.split('\n')
                    df_dict = {}

                    # Apply any new code parsers, don't calc new metrics yet
                    for tkzr in tokenizer_keys_to_instances(self.tokenizers, new_tokenizers):
                        out = tkzr.tokenize(codestr, lang)
                        for k, v in out.items():
                            mv = []

                            # apply existing metrics to the new rows
                            for row in v:
                                line_start, line_end, char_start, char_end = tuple(
                                    row)
                                substr = '\n'.join(codestr_lines[line_start:line_end])[
                                    char_start:char_end]
                                mv.append([self.metrics[mm](substr)
                                           for mm in new_metrics])

                            # TODO: ensure that columns for metrics are passed the correct values
                            df_dict[(lang, input_path, k)] = np.concatenate(
                                (v, np.array(mv)), axis=1)

        # process new metrics for all files
        if len(new_metrics != 0):
            pass

        # process new files (metrics and tokenizers)

        mi = pd.MultiIndex.from_product([self.languages, self.file_paths, flatten_list(self.tokenizer_names)], names=[
            'language', 'file_path', 'token_type'])
        self.df = self.df.reindex(
            index=mi, columns=self.default_columns + self.metric_names)

        self.indexed = True
        log.info('Repository {} indexed for analysis'.format(self.root_path))


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
