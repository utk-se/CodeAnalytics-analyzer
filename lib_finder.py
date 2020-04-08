def find_libs(path, lang):
    with open(path, 'r') as f:
        lines = []
        content = f.readlines()
        if lang == 'py':
            for x, line in enumerate(content):
                if line.startswith("from") or line.startswith("import") or " import " in line:
                    lines.append(x)
        elif lang == 'c':
            for x, line in enumerate(content):
                if line.startswith("#include"):
                    lines.append(x)
        elif lang == 'java':
            for x, line in enumerate(content):
                if line.startswith("import"):
                    lines.append(x)
        elif lang == 'js':
            for x, line in enumerate(content):
                if line.startswith("import") or " import(" in line:
                    lines.append(x)
        else:
            print(lang, "not supported yet")
            exit()
    return lines
