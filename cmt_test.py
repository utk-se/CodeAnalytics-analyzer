import comment_finder

lines = comment_finder.find_comments("ex.txt", 'c', verbose=1)
print(lines)