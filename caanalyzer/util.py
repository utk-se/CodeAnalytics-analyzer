import os
from itertools import groupby
from Types import List
# https://www.tutorialspoint.com/How-to-find-the-nth-occurrence-of-substring-in-a-string-in-Python


def findnth(string, substring, n):
    parts = string.split(substring, n + 1)
    if len(parts) <= n + 1:
        return -1
    return len(string) - len(parts[-1]) - len(substring)

# https://stackoverflow.com/questions/13734451/string-split-with-indices-in-python


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


def flatten_list(lst: List[List]) -> List:
    [y for x in lst for y in x]


def tokenizer_keys_to_instances(self, available_tokenizers, keys):
    keys = set(keys)
    rv = []
    for tokenizer in available_tokenizers:
        tks = set(tokenizer.keys())
        if tks.issubset(keys):
            keys -= tks
            rv.append(tokenizer)
    return rv
