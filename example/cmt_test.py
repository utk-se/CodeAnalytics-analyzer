import id_finder
import lib_finder
import comment_finder

comments = comment_finder.find_comments("ex.c", lang='c', verbose=0)
print(comments)
libs = lib_finder.find_libs("ex.c", lang='c')
print(libs)
id_finder.find_ids("ex.c", 'c', verbose=1)
