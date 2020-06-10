import re
from cadistributor import log


def space_counter(string):  # counts num spaces before class keyword
    space_count = 0
    for char in string:
        if char == ' ':
            space_count += 1
        else:
            break
    return space_count


def find_classes(content, lang, verbose=0):
    class_tuples = []
    if lang == '.py':
        import ast
        my_ast = ast.parse(''.join(content))
        for each in my_ast.body:
            if type(each).__name__ == 'ClassDef':
                class_tuples.append(tuple([each.lineno - 1, each.body[len(each.body)-1].lineno - 1, 0, 1]))

    elif lang == '.js':
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
                        class_tuples.append(tuple([each.loc.start.line - 1, each2.loc.start.line - 1, 0, 1]))
                        break

    elif lang == '.java':
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
                        class_tuples.append(tuple([each[2][0] - 1, each2[2][0] - 1, 0, 1]))
                        break

    elif lang == '.c' or lang == '.cpp' or lang == '.h':
        pattern = re.compile(r"\s*(class|struct)\s\w*\s*{?\n")
        pattern2 = re.compile(r"\s*(class|struct)\s\w*\n")
        pattern3 = re.compile(r"\s*{")
        for line_no_start, line in enumerate(content):
            if pattern.match(line) is not None or pattern2.match(line) is not None:
                if pattern2.match(line) is not None:
                    if pattern3.match(content[line_no_start + 1]) is not None:
                        if verbose:
                            log.info("found class at line # " + str(line_no_start + 1))
                        # finding end of class
                        left_curly_count = 1
                        right_curly_count = 0
                        for line_no_end, line2 in enumerate(content[line_no_start + 2:]):
                            line_no_end += line_no_start + 2
                            if '{' in line2:
                                left_curly_count += 1
                            if '}' in line2:
                                right_curly_count += 1
                            if left_curly_count == right_curly_count:
                                class_tuples.append(
                                    # tuple([line_no_start, line_no_end]))
                                    tuple([line_no_start, line_no_end, 0, 1]))
                                if verbose:
                                    log.info(
                                        'found end of class at line # ' + str(line_no_end + 1))
                                break
                else:
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
                                tuple([line_no_start, line_no_end + 1, 0, 1]))
                            if verbose:
                                log.info('found end of class at line # ' + str(line_no_end + 2))
                            break

    else:
        log.err(lang + " not supported yet")

    return class_tuples
