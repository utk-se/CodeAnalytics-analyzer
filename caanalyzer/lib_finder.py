# format: lib name, line number
def find_libs(path, lang):
    with open(path, 'r') as f:
        libs = []
        content = f.readlines()
        if lang == 'py':
            import astpretty
            import ast
            my_ast = ast.parse(''.join(content))
            for x in range(len(my_ast.body)):
                ast_piece = astpretty.pformat(my_ast.body[x])
                if ast_piece.startswith("Import"):
                    libs.append([my_ast.body[x].names[0].name, my_ast.body[x].lineno, my_ast.body[x].col_offset])
        elif lang == 'c' or lang == 'c++':
            import re
            pattern = re.compile("#include(.*)")
            for x, line in enumerate(content):
                if line.strip().startswith("#include"):
                    res = re.fullmatch(pattern, line.strip()).group(1).strip()
                    libs.append([res[1:-1], x])
        elif lang == 'java':
            import re
            for x, line in enumerate(content):
                if line.strip().startswith("import"):
                    broken_line = line.strip().split()
                    lib_name = broken_line[len(broken_line)-1]
                    lib_name = lib_name[:len(lib_name)-1]
                    libs.append([lib_name, x])
        elif lang == 'js':
            import re
            pattern1 = re.compile("import(.*)from(.*);")
            pattern2 = re.compile("import(.*);")
            pattern3 = re.compile(".*import\((.*)\);")
            for x, line in enumerate(content):
                res1 = re.fullmatch(pattern1, line.strip())
                res2 = re.fullmatch(pattern2, line.strip())
                res3 = re.fullmatch(pattern3, line.strip())
                if res1 is not None:
                    res1 = res1.group(1).strip()
                    libs.append([res1, x])
                elif res2 is not None:
                    res2 = res2.group(1).strip()[1:-1]
                    libs.append([res2, x])
                elif res3 is not None:
                    res3 = res3.group(1).strip()[1:-1]
                    libs.append([res3, x])
        else:
            print(lang, "not supported yet")
            exit()
    return libs
