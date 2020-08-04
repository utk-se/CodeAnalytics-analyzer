import os
from itertools import groupby
from typing import List
import logging
import json
import time
from tqdm import tqdm
import io

# https://stackoverflow.com/questions/14897756/python-progress-bar-through-logging-module


class TqdmToLogger(io.StringIO):
    """
        Output stream for TQDM which will output to logger module instead of
        the StdOut.
    """
    logger = None
    level = None
    buf = ''

    def __init__(self, logger, level=None):
        super(TqdmToLogger, self).__init__()
        self.logger = logger
        self.level = level or logging.INFO

    def write(self, buf):
        self.buf = buf.strip('\r\n\t ')

    def flush(self):
        self.logger.log(self.level, self.buf)


# https://www.tutorialspoint.com/How-to-find-the-nth-occurrence-of-substring-in-a-string-in-Python

def findnth(string, substring, n):
    parts = string.split(substring, n + 1)
    if len(parts) <= n + 1:
        return -1
    return len(string) - len(parts[-1]) - len(substring)

# https://stackoverflow.com/questions/13734451/string-split-with-indices-in-python


def line_start(line):
    return len(line) - len(line.lstrip())


def line_end(line):
    return len(line.rstrip())


def splitWithIndices(s, c=' '):
    p = 0
    for k, g in groupby(s, lambda x: x == c):
        q = p + sum(1 for i in g)
        if not k:
            yield p, q
        p = q


def get_file_extension(file_path):
    file_extension = file_path.split(os.sep)[-1].split('.')[-1]
    if len(file_extension) <= 1:
        file_extension = ''
    return file_extension


def flatten_list(lst: List[List[str]]) -> List[str]:
    return [y for x in lst for y in x]


def tokenizer_keys_to_instances(available_tokenizers, keys):
    keys = set(keys)
    rv = []
    for tokenizer in available_tokenizers:
        tks = set(tokenizer.keys())
        if tks.issubset(keys):
            keys -= tks
            rv.append(tokenizer)
    return rv


'''
return the mode of a list
'''


def mode(lst):
    l_dict = {}
    # count frequencies
    for n in lst:
        if n in l_dict:
            l_dict[n] += 1
        else:
            l_dict[n] = 1

    # get item with highest frequency
    max_f = 0
    rv = 0
    for k, v in l_dict.items():
        if v > max_f:
            max_f = v
            rv = k

    return rv
