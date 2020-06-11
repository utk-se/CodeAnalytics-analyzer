from cadistributor import log

# format: line start, line end, offset start, offset end
def find_libs(content, lang):
    libs = []
    if lang == 'py':
        import astpretty
        import ast
        my_ast = ast.parse(''.join(content))
        for x in range(len(my_ast.body)):
            ast_piece = astpretty.pformat(my_ast.body[x])
            if ast_piece.startswith("Import"):
                # libs.append([my_ast.body[x].names[0].name, my_ast.body[x].lineno, my_ast.body[x].col_offset])
                libs.append([my_ast.body[x].lineno - 1, my_ast.body[x].lineno - 1, 0,
                             len(content[my_ast.body[x].lineno - 1])])

    elif lang == 'c' or lang == 'cpp' or lang == 'h':
        import re
        pattern = re.compile("#include(.*)")
        for x, line in enumerate(content):
            if line.strip().startswith("#include"):
                res = re.fullmatch(pattern, line.strip()).group(1).strip()
                # libs.append([res[1:-1], x])
                libs.append([x, x, 0, len(line)])

    elif lang == 'java':
        import re
        for x, line in enumerate(content):
            if line.strip().startswith("import"):
                broken_line = line.strip().split()
                lib_name = broken_line[len(broken_line) - 1]
                lib_name = lib_name[:len(lib_name) - 1]
                # libs.append([lib_name, x])
                libs.append([x, x, 0, len(line)])

    elif lang == 'js':
        import re
        pattern1 = re.compile("import(.*)from(.*);")
        pattern2 = re.compile("import(.*);")
        pattern3 = re.compile(r".*import\((.*)\);")
        for x, line in enumerate(content):
            res1 = re.fullmatch(pattern1, line.strip())
            res2 = re.fullmatch(pattern2, line.strip())
            res3 = re.fullmatch(pattern3, line.strip())
            if res1 is not None:
                res1 = res1.group(1).strip()
                # libs.append([res1, x])
                libs.append([x, x, 0, len(line)])
            elif res2 is not None:
                res2 = res2.group(1).strip()[1:-1]
                # libs.append([res2, x])
                libs.append([x, x, 0, len(line)])
            elif res3 is not None:
                res3 = res3.group(1).strip()[1:-1]
                # libs.append([res3, x])
                libs.append([x, x, 0, len(line)])

    else:
        log.error(lang + " not supported yet")

    return libs
