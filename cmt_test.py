import comment_finder

lines = comment_finder.find_comments("caanalyzer/analyzer.py", 'py', verbose=0)
print(lines)