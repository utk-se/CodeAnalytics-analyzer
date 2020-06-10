import sys
sys.path.append('../')

from caanalyzer import id_finder
from caanalyzer import lib_finder
from caanalyzer import comment_finder
from caanalyzer import class_finder

lang = '.py'

with open("ex"+lang, 'r') as f:
    content = f.readlines()
    #print(content)
    #classes = class_finder.find_classes(content, lang=lang, verbose=0)
    #print(classes)
    #comments = comment_finder.find_comments(content, path="ex"+lang, lang=lang)
    #print(comments)
    #libs = lib_finder.find_libs(content, lang=lang)
    #print(libs)
    ids = id_finder.find_ids(content, path="ex"+lang, lang=lang, verbose=0)
    print(ids)
