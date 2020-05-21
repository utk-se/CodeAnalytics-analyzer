import id_finder
import lib_finder
import comment_finder

skip_lines = comment_finder.find_comments("ex.py", lang='py')
skip_lines.extend(lib_finder.find_libs("ex.py", lang='py'))
print('skipping:', end=' ')
print(skip_lines)
id_finder.find_ids("ex.py", 'py', skip_lines=skip_lines, verbose=1)
