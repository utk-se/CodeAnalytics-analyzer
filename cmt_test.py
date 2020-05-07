import id_finder
import lib_finder
import comment_finder

skip_lines = comment_finder.find_comments("ex.txt", lang='c')
skip_lines.extend(lib_finder.find_libs("ex.txt", lang='c'))
print('skipping:', end=' ')
print(skip_lines)
id_finder.find_ids("ex.txt", 'c', skip_lines=skip_lines, verbose=1)
