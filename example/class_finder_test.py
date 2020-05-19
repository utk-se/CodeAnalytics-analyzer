import class_finder

print("JAVASCRIPT")
result = class_finder.find_classes('ex.txt', verbose=1, lang='js')
print(result)
print()

print("C")
result = class_finder.find_classes('ex.txt', verbose=1, lang='c')
print(result)
print()

print("JAVA")
result = class_finder.find_classes('ex.txt', verbose=1, lang='java')
print(result)
print()

print("PYTHON")
result = class_finder.find_classes('ex.txt', verbose=1, lang='python')
print(result)
print()