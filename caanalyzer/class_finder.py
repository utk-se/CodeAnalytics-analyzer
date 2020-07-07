import re

class StartOfClassNotFound(Exception):
    pass


def space_counter(string):  # counts num spaces before class keyword
    space_count = 0
    for char in string:
        if char == ' ':
            space_count += 1
        else:
            break
    return space_count


def find_classes(content, lang, verbose=0, py2=0):
    if not py2:
        from cadistributor import log
    class_tuples = []
    if lang == 'py':
        import ast
        try:
            if py2:
                my_ast = ast.parse(content)
            else:
                my_ast = ast.parse(''.join(content))
        except SyntaxError:
            # PYTHON 2
            if py2:  # getting in here means python2 still gives syntax errors
                return []
            import subprocess
            import os
            python2_name = 'python2'
            try:
                process = subprocess.check_output([python2_name,  # python2 may not be the command on your machine
                                                   os.path.abspath(__file__),
                                                   ''.join(content), 'py', '0', '1'],
                                                  stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as e:
                raise RuntimeError("\ncommand '{}'\n\nreturn with error (code {}):\n{}".format(e.cmd,
                                                                                               e.returncode,
                                                                                               e.output.decode()))

            p_result = eval(process.decode(errors='replace'))
            return p_result

        if py2:
            content = content.split('\n')

        for each in my_ast.body:
            if type(each).__name__ == 'ClassDef':
                class_tuples.append(tuple([each.lineno,
                                           each.body[len(each.body) - 1].lineno - 1,
                                           each.body[0].col_offset,
                                           [len(k)-1 for k in content[each.lineno:
                                                                      each.body[len(each.body)-1].lineno]]]))

    elif lang == 'js':
        import esprima
        items = list(esprima.tokenize(''.join(content), options={'loc': True}))
        l_brackets = 0
        r_brackets = 0
        end_check = False
        for i, each in enumerate(items):
            if each.type == 'Keyword' and each.value == 'class':
                if verbose:
                    log.info("found class at line # " + str(each.loc.start.line))
                for each2 in items[i+1:]:
                    if each2.type == 'Punctuator' and each2.value == '{':
                        l_brackets += 1
                        end_check = True
                    if each2.type == 'Punctuator' and each2.value == '}':
                        r_brackets += 1
                    if (l_brackets - r_brackets == 0) and end_check:
                        if verbose:
                            log.info("found end of class at line # " + str(each2.loc.start.line))
                        # class_tuples.append(tuple([each.loc.start.line - 1, each2.loc.start.line - 1]))
                        class_tuples.append(tuple([each.loc.start.line - 1,
                                                   each2.loc.start.line - 1,
                                                   each.loc.start.column,
                                                   [len(k)-1 for k in content[each.loc.start.line-1:
                                                                              each2.loc.start.line]]]))
                        break

    elif lang == 'java':
        import javac_parser
        java = javac_parser.Java()
        l_brackets = 0
        r_brackets = 0
        end_check = False
        for i, each in enumerate(java.lex(''.join(content))):
            if each[0] == 'CLASS':
                if verbose:
                    log.info("found class at line # " + str(each[2][0]))
                for each2 in java.lex(''.join(content))[i+1:]:
                    if each2[0] == 'LBRACE':
                        l_brackets += 1
                        end_check = True
                    if each2[0] == 'RBRACE':
                        r_brackets += 1
                    if (l_brackets - r_brackets == 0) and end_check:
                        if verbose:
                            log.info("found end of class at line # " + str(each2[2][0]))
                        # class_tuples.append(tuple([each[2][0] - 1, each2[2][0] - 1]))
                        class_tuples.append(tuple([each[2][0] - 1,
                                                   each2[2][0] - 1,
                                                   each[2][0],
                                                   [len(k)-1 for k in content[each[2][0]-1:
                                                                              each2[2][0]]]]))
                        break

    elif lang == 'c' or lang == 'cpp' or lang == 'h':
        pattern = re.compile(r"(\s*)(class|struct)\s*\w*\s*{\s*\n")
        pattern2 = re.compile(r"(\s*)(class|struct)\s*\w*\s*\n")
        pattern3 = re.compile(r"\s*{")
        pattern4 = re.compile(r'(\s*)(class|struct)\s*\w*\s*{(?:[^"]*"[^"]*")*[^"]*};\s*')
        pattern5 = re.compile(r"(\s*)(class|struct)\s*\w*\s*{(?:[^']*'[^']*')*[^']*};\s*")
        for line_no_start, line in enumerate(content):
            result_p4 = pattern4.match(line)
            result_p5 = pattern5.match(line)
            if result_p4 is not None:
                class_tuples.append(tuple([line_no_start,
                                           line_no_start,
                                           len(result_p4.group(1)),
                                           len(content[line_no_start])]))
            elif result_p5 is not None:
                class_tuples.append(tuple([line_no_start,
                                           line_no_start,
                                           len(result_p5.group(1)),
                                           len(content[line_no_start])]))
            elif pattern.match(line) is not None or pattern2.match(line) is not None:
                result_p2 = pattern2.match(line)
                if result_p2 is not None:
                    i = 1
                    result_p3 = None
                    while result_p3 is None:
                        try:
                            result_p3 = pattern3.match(content[line_no_start + i])
                        except IndexError:
                            break
                        i += 1
                    if result_p3 is not None:
                        if verbose:
                            log.info("found class at line # " + str(line_no_start + 1))
                        # finding end of class
                        left_curly_count = 1
                        right_curly_count = 0
                        for line_no_end, line2 in enumerate(content[line_no_start + (i+1):]):
                            line_no_end += line_no_start + (i+1)
                            if '{' in line2:
                                left_curly_count += 1
                            if '}' in line2:
                                right_curly_count += 1
                            if left_curly_count == right_curly_count:
                                class_tuples.append(
                                    # tuple([line_no_start, line_no_end]))
                                    tuple([line_no_start,
                                           line_no_end,
                                           len(result_p2.group(1)),
                                           [len(k)-1 for k in content[line_no_start:line_no_end+1]]]))
                                if verbose:
                                    log.info(
                                        'found end of class at line # ' + str(line_no_end + 1))
                                break
                else:
                    result_p = pattern.match(line)
                    if verbose:
                        log.info("found class at line # " + str(line_no_start + 1))
                    # finding end of class
                    left_curly_count = 1
                    right_curly_count = 0
                    for line_no_end, line2 in enumerate(content[line_no_start + 1:]):
                        line_no_end += line_no_start
                        if '{' in line2:
                            left_curly_count += 1
                        if '}' in line2:
                            right_curly_count += 1
                        if left_curly_count == right_curly_count:
                            class_tuples.append(
                                # tuple([line_no_start, line_no_end + 1]))
                                tuple([line_no_start,
                                       line_no_end + 1,
                                       len(result_p.group(1)),
                                       [len(k)-1 for k in content[line_no_start:line_no_end+2]]]))
                            if verbose:
                                log.info('found end of class at line # ' + str(line_no_end + 2))
                            break

    else:
        log.err(lang + " not supported yet")

    return class_tuples


if __name__ == "__main__":
    import sys
    sys.path.append('..')
    print(find_classes(content=sys.argv[1], lang=sys.argv[2], verbose=int(sys.argv[3]), py2=int(sys.argv[4])))
