import numpy as np
from hashlib import md5

'''
Metrics calculate a scalar value based on a given code segment.
How do I know when to implement a metric? 
If you want to calculate something, given an input string, use this

TODO: Use multi-indexing for non-scalar metrics

TODO: length
TODO: num tokens
TODO: num tabs
TODO: num spaces
TODO: first token index (ie, start of a line)
TODO: num newlines
TODO: md5hash
'''

# TODO: width, height could be calculated from already existing columns


def width(s):
    return max([len(sl) for sl in s])


def height(s):
    return len(s)


def num_tokens(s):
    return sum([len(line.split()) for line in s])


class BaseMetric:
    pass


class MultiMetric:
    pass
