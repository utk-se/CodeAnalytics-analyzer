"""CodeAnalytics Analyzer

A set of tools to gather metrics about code repositories, files, or 
individual lines that can be used to compare code projects. Given a 
repository, file, or line, produces a static analysis of the visual 
structure of the code within, such as use of whitespace, line length, 
and distribution of code elements, such as tokens, methods, and classes.

Notes
--------------------------------------------------------------------------
    Initialize an instance of Repo or File with a filepath, or one of Line
    with a string, to gather analytics on that source.
    
    Supply an ignorefile to exclude files and directories from analysis.

    Retrieve results as a serializable dictionary by calling the export()
    method.
"""

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
import json
import codecs
from tqdm import tqdm
from .util import TqdmToLogger
import logging
tqdm_out = TqdmToLogger(log, level=logging.INFO)


Num = Union[int, float]

'''
Container for code repository.
TODO: refactor to become pandas extension
https://pandas.pydata.org/pandas-docs/stable/development/extending.html
ie, df.index_repo(), df.mean() versus repo.df.mean(), repo.index()
'''


class CodeRepo:
    # TODO: type annotate this
    def __init__(self, input_path, languages=['.py', '.cpp', '.js', '.h', '.java']):

        self.df = pd.DataFrame()
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
        self.file_paths = []
        self.file_extensions = []
        self.num_directories = 0
        self.num_extensions = 0
        self.max_depth = 0
        self.num_files = 0

        self.root_path = str(Path(input_path).absolute())

        if not os.path.exists(input_path):
            raise FileNotFoundError('{} does not exist'.format(input_path))
        if not os.path.isdir(input_path):
            raise NotADirectoryError(
                'Provided path {} is not a directory'.format(input_path))

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

                if file_extension not in self.supported_filetypes:
                    continue

                self.file_paths.append(str(file_path.absolute()))
                self.file_extensions.append(file_extension)

        self.num_extensions = len(list(file_extensions))
        self.languages = set(self.supported_filetypes) & file_extensions
        self.indexed = False

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
        if not self.metrics:
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
    TODO: implement
    Indexes a new tokenizer and appends the results to an existing table
    '''

    def add_tokenizers(self, tokenizers):
        raise NotImplementedError

    '''
    TODO: implement
    Indexes a new metric and appends the results to an existing table
    '''

    def add_metrics(self, metrics):
        raise NotImplementedError

    '''
    return true if a repository has been indexed
    '''

    def indexed(self):
        return self.indexed

    '''
    Index the code repository into a dataframe for metric gathering
    For each file, and each type of token
    retrieve the start and end indices for this
    if you want to join info for multiple repos, index multiple repos and perform a pandas join
    '''

    def index(self, tokenizers, metrics={}):
        if self.indexed:
            return

        # TODO: verify language support from tokenizers
        self.tokenizers = tokenizers
        self.metrics = metrics

        log.info('Indexing this repository...')

        self.tokenizer_names = []
        for tokenizer in self.tokenizers:
            self.tokenizer_names.append(tokenizer.keys())

        self.metric_names = list(self.metrics.keys())

        # if we have existing files, process these first with
        # the updated metrics
        df_dict = {}

        for input_path, lang in tqdm(zip(list(self.file_paths), self.file_extensions), total=len(self.file_paths)):

            # check that the file exists
            if not os.path.exists(input_path):
                log.warn('Previously indexed file {} not found.'.format(
                    input_path))
                continue

            with codecs.open(input_path, 'r', encoding='utf-8', errors='ignore') as fin:
                # log.info('Reading {}'.format(input_path))
                codestr_lines = fin.read().split('\n')

                # Apply any new code parsers, don't calc new metrics yet
                for tkzr in self.tokenizers:
                    out = tkzr.tokenize(codestr_lines, lang=lang)
                    # log.info('Applying tokenizer(s): {}'.format(tkzr.keys()))
                    for k, v in out.items():

                        # apply existing metrics to the new rows
                        for i, row in enumerate(v):
                            line_start, line_end, char_start, char_end = tuple(
                                row)

                            substr = codestr_lines[line_start: line_end]
                            substr[0] = substr[0][char_start:]
                            substr[-1] = substr[-1][:char_end]

                            mv = [mm(substr)
                                  for mm in self.metrics.values()]

                            combined_row = np.concatenate(
                                (row, np.array(mv)))
                            df_dict[(lang, input_path, k, i)] = combined_row

        log.info('Creating dataframe...')

        mi = pd.MultiIndex.from_tuples(
            df_dict.keys(), names=['lang', 'file_path', 'token_type', 'id'])

        self.df = pd.DataFrame(
            df_dict, columns=mi, index=self.default_columns + self.metric_names).T

        log.info('Repository {} indexed for analysis'.format(self.root_path))
