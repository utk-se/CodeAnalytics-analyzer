# format: line start, line end, offset start, offset end
def find_libs(content, path, lang, py2=0):
    if not py2:
        from cadistributor import log
    else:
        content = open(path).readlines()
        content = [line[:-2]+'\n' for line in content if line.endswith('\r\n')]
    libs = []
    if lang == 'py':
        import astpretty
        import ast
        try:
            my_ast = ast.parse(''.join(content))
        except SyntaxError:
            # PYTHON 2
            if py2:  # getting in here means python2 still gives syntax errors
                return []
            import subprocess
            import os
            python2_name = 'python2'
            process = subprocess.check_output([python2_name,  # python2 may not be the command on your machine
                                               os.path.abspath(__file__),
                                               ''.join(content), path, 'py', '1'])
            p_result = eval(process.decode())

            return p_result

        def lib_recurse(body):
            for x in range(len(body)):
                ast_piece = astpretty.pformat(body[x])
                if ast_piece.startswith("Import"):
                    # libs.append([my_ast.body[x].names[0].name, my_ast.body[x].lineno, my_ast.body[x].col_offset])
                    libs.append([body[x].lineno - 1, body[x].lineno - 1,
                                 body[x].col_offset, len(content[body[x].lineno - 1])])
                if 'body' in dir(body[x]):
                    lib_recurse(body[x].body)

        lib_recurse(my_ast.body)

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


if __name__ == "__main__":
    import sys
    sys.path.append('..')
    print(find_libs(content=sys.argv[1], path=sys.argv[2], lang=sys.argv[3], py2=int(sys.argv[4])))
