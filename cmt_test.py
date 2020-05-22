import id_finder
import lib_finder
import comment_finder

skip_lines = comment_finder.find_comments("ex.java", lang='java')
skip_lines.extend(lib_finder.find_libs("ex.java", lang='java'))
print('skipping:', end=' ')
print(skip_lines)
id_finder.find_ids("ex.java", 'java', skip_lines=skip_lines, verbose=1)
