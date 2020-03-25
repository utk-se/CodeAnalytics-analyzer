def find_libs(path, lang):
    with open(path, 'r') as f:
        num_libs = 0
        content = f.readlines()
        if lang == 'py':
            for line in content:
                if line.startswith("from") or line.startswith("import") or " import " in line:
                    num_libs += 1
        elif lang == 'c':
            for line in content:
                if line.startswith("#include"):
                    num_libs += 1
        elif lang == 'java':
            for line in content:
                if line.startswith("import"):
                    num_libs += 1
        elif lang == 'js':
            for line in content:
                if line.startswith("import") or " import(" in line:
                    num_libs += 1
        else:
            print(lang, "not supported yet")
            exit()
    return num_libs
