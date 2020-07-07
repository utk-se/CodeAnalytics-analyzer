import sys
sys.path.append('..')
from caanalyzer import class_finder
from caanalyzer import comment_finder
from caanalyzer import id_finder
from caanalyzer import lib_finder

path = '../example/ex.c'
content = open(path).readlines()
result = class_finder.find_classes(content, verbose=0, lang='c')
print(result)
print()
print()
result = comment_finder.find_comments(content, path=path, lang='c')
print(result)
print()
print()
result = id_finder.find_ids(content, path=path, verbose=0, lang='c')
print(result)
print()
print()
result = lib_finder.find_libs(content, path=path, lang='c')
print(result)
print()
