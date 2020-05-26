import id_finder
import lib_finder
import comment_finder

#comments = comment_finder.find_comments("ex.js", lang='js', verbose=0)
#print(comments)
libs = lib_finder.find_libs("ex.java", lang='java')
print(libs)
#id_finder.find_ids("ex.js", 'js', verbose=1)
