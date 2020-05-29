import sys
sys.path.append('../')

from caanalyzer import id_finder
from caanalyzer import lib_finder
from caanalyzer import comment_finder

comments = comment_finder.find_comments("ex.java", lang='java')
print(comments)
libs = lib_finder.find_libs("ex.java", lang='java')
print(libs)
id_finder.find_ids("ex.java", 'java', verbose=1)
