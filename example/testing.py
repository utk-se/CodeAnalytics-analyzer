import sys
sys.path.append('..')
from caanalyzer import class_finder
from caanalyzer import comment_finder
from caanalyzer import id_finder
from caanalyzer import lib_finder

content = open('ex.txt').readlines()
result = class_finder.find_classes(content, verbose=1, lang='py')
print(result)
print()
print()
result = comment_finder.find_comments(content, path='ex.txt', lang='py')
print(result)
print()
print()
result = id_finder.find_ids(content, path='ex.txt', verbose=0, lang='py')
print(result)
print()
print()
result = lib_finder.find_libs(content, path='ex.txt', lang='py')
print(result)
print()
