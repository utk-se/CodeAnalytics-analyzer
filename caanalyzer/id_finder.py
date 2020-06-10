import re
from cadistributor import log

c_plusplus_keywords = ['asm', 'else', 'new', 'this', 'auto', 'enum', 'operator', 'throw', 'bool', 'explicit',
                       'private', 'true', 'break', 'export', 'protected', 'try', 'case', 'extern', 'public', 'typedef',
                       'catch', 'false', 'register', 'typeid', 'char', 'float', 'reinterpret_cast', 'typename', 'class',
                       'for', 'return', 'union', 'const', 'friend', 'short', 'unsigned', 'const_cast', 'goto', 'signed',
                       'using',
                       'continue', 'if', 'sizeof', 'virtual', 'default', 'inline', 'static', 'void', 'delete', 'int',
                       'static_cast', 'volatile', 'do', 'long', 'struct', 'wchar_t', 'double', 'mutable', 'switch',
                       'while',
                       'dynamic_cast', 'namespace', 'template', 'And', 'bitor', 'not_eq', 'xor', 'and_eq', 'compl',
                       'or',
                       'xor_eq', 'bitand', 'not', 'or_eq']

c_plusplus_ops = ['equal', 'plus', 'minus', 'star', 'slash', 'percent', 'amp', 'pipe', 'caret', 'greater', 'less',
                  'exclaim']


def find_ids(content, path, lang, verbose=0):
    id_counter = 0
    op_counter = 0
    lit_counter = 0
    ids = list()
    ops = list()
    lits = list()
    unique_ops = set()  # list of operators with starting line and starting position
    unique_lits = set()  # list of literals with starting line and starting position
    unique_ids = set()  # list of identifiers with starting line and starting position

    if lang == 'py':
        import astpretty
        import ast
        my_ast = ast.parse(''.join(content))
        pattern = re.compile(r".*op=.*\(\),.*")
        pattern2 = re.compile(r".*Num\(.*\).*")
        pattern3 = re.compile(r".*Str\(.*\).*")
        pattern4 = re.compile(r".*Name\(.*\).*")
        for x in range(len(my_ast.body)):
            ast_piece = astpretty.pformat(my_ast.body[x])
            # print(ast_piece)
            # print('#################')
            ast_piece_split = ast_piece.split('\n')
            if 'Assign(' in ast_piece:
                for i, each in enumerate(ast_piece_split):
                    if each.strip().startswith("Assign"):
                        op_counter += 1
                        # ops.append(['=', ast_piece_split[1].strip()[7:len(ast_piece_split[1].strip()) - 1],
                        #             ast_piece_split[2].strip()[11:len(ast_piece_split[2].strip()) - 1]])
                        ops.append([int(ast_piece_split[i+1].strip()[7:len(ast_piece_split[i+1].strip()) - 1]) - 1,
                                    int(ast_piece_split[i+1].strip()[7:len(ast_piece_split[i+1].strip()) - 1]) - 1,
                                    int(ast_piece_split[i+2].strip()[11:len(ast_piece_split[i+2].strip()) - 1]),
                                    int(ast_piece_split[i+2].strip()[11:len(ast_piece_split[i+2].strip()) - 1]) + 1])
                        unique_ops.add('=')
            for i, each in enumerate(ast_piece_split):
                if bool(re.fullmatch(pattern4, each)):
                    id_counter += 1
                    info = re.search(r".*Name\((.*)\).*", each).group(1)
                    info = info.split()
                    # ids.append([info[2][4:len(info[2]) - 2], info[0][7:len(info[0]) - 1], info[1][11:len(info[1]) - 1]])
                    ids.append([int(info[0][7:len(info[0]) - 1]) - 1,
                                int(info[0][7:len(info[0]) - 1]) - 1,
                                int(info[1][11:len(info[1]) - 1]),
                                int(info[1][11:len(info[1]) - 1]) + len(info[2][4:len(info[2]) - 2])])
                    unique_ids.add(info[2][4:len(info[2]) - 2])
                if bool(re.fullmatch(pattern2, each)):
                    lit_counter += 1
                    info = re.search(r".*Num\((.*)\).*", each).group(1)
                    info = info.split(', ')
                    # lits.append([info[2][2:], info[0][7:], info[1][11:]])
                    lits.append([int(info[0][7:]) - 1,
                                 int(info[0][7:]) - 1,
                                 int(info[1][11:]),
                                 int(info[1][11:]) + len(info[2][2:])])
                    unique_lits.add(info[2][2:])
                if bool(re.fullmatch(pattern3, each)):
                    info = re.search(r".*Str\((.*)\).*", each).group(1)
                    # print(info)
                    info_split = []
                    info_split.append(re.search("lineno=(\d+), col_offset=\-?\d+, s=.*", info).group(1))
                    info_split.append(re.search("lineno=\d+, col_offset=(\-?\d+), s=.*", info).group(1))
                    info_split.append(re.search("lineno=\d+, col_offset=\-?\d+, s=(\"|\')(.*)(\"|\')", info).group(2))
                    # print(info_split)
                    # print('##############')
                    # info = re.split("(, (?=(?:[^\']*\'[^\']*\')*[^\']*$))|(, (?=(?:[^\"]*\"[^\"]*\")*[^\"]*$))", info)
                    # lits.append([info[2][3:len(info[2]) - 1], info[0][7:], info[1][11:]])
                    # print(info)
                    # print('##############')
                    # print(info[0][7:])
                    # print(info[1][11:])
                    # print(info[2][3:len(info[2]) - 1])
                    # print('##############')
                    # lits.append([int(info[0][7:]),
                    #              int(info[0][7:]),
                    #              int(info[1][11:]),
                    #              int(info[1][11:]) + len(info[2][3:len(info[2]) - 1])])
                    lits.append([int(info_split[0]) - 1,
                                int(info_split[0]) - 1,
                                int(info_split[1]),
                                int(info_split[1]) + len(info_split[2]) - 1])
                    unique_lits.add(info[2][3:len(info[2]) - 1])
                if bool(re.fullmatch(pattern, each)):
                    op_counter += 1
                    num_spaces = len(re.search("(.*)op=.*", each).group(1))
                    raw_op = ''
                    try:
                        raw_op = re.search(r'.*op=(.*)\(\).*', each).group(1)
                    except AttributeError as e:
                        log.error(e)
                    found = False
                    rev_i = i - 1
                    while not found:
                        if bool(re.fullmatch(r'\s{' + str(num_spaces) + r'}col_offset=.*', ast_piece_split[rev_i])):
                            found = True
                            # ops.append([raw_op,
                            #             ast_piece_split[rev_i - 1].strip()[7:len(ast_piece_split[rev_i - 1].strip()) - 1],
                            #             ast_piece_split[rev_i].strip()[11:len(ast_piece_split[rev_i].strip()) - 1]])
                            ops.append([int(ast_piece_split[rev_i - 1].strip()[7:len(ast_piece_split[rev_i - 1].strip()) - 1]) - 1,
                                        int(ast_piece_split[rev_i - 1].strip()[7:len(ast_piece_split[rev_i - 1].strip()) - 1]) - 1,
                                        int(ast_piece_split[rev_i].strip()[11:len(ast_piece_split[rev_i].strip()) - 1]),
                                        int(ast_piece_split[rev_i].strip()[11:len(ast_piece_split[rev_i].strip()) - 1]) + 1])
                            unique_ops.add(raw_op)
                        rev_i -= 1

    elif lang == 'c':
        from pycparser import parse_file
        import json
        import sys
        import os
        sys.path.extend(['.', '..'])
        os.chdir(os.path.dirname(__file__))
        RE_CHILD_ARRAY = re.compile(r'(.*)\[(.*)\]')
        RE_INTERNAL_ATTR = re.compile('__.*__')

        class CJsonError(Exception):
            pass

        def memodict(fn):
            """ Fast memoization decorator for a function taking a single argument """

            class memodict(dict):
                def __missing__(self, key):
                    ret = self[key] = fn(key)
                    return ret

            return memodict().__getitem__

        @memodict
        def child_attrs_of(klass):
            """
            Given a Node class, get a set of child attrs.
            Memoized to avoid highly repetitive string manipulation
            """
            non_child_attrs = set(klass.attr_names)
            all_attrs = set([i for i in klass.__slots__ if not RE_INTERNAL_ATTR.match(i)])
            return all_attrs - non_child_attrs

        def to_dict(node):
            """ Recursively convert an ast into dict representation. """
            klass = node.__class__

            result = {}

            # Metadata
            result['_nodetype'] = klass.__name__

            # Local node attributes
            for attr in klass.attr_names:
                result[attr] = getattr(node, attr)

            # Coord object
            if node.coord:
                result['coord'] = str(node.coord)
            else:
                result['coord'] = None

            # Child attributes
            for child_name, child in node.children():
                # Child strings are either simple (e.g. 'value') or arrays (e.g. 'block_items[1]')
                match = RE_CHILD_ARRAY.match(child_name)
                if match:
                    array_name, array_index = match.groups()
                    array_index = int(array_index)
                    # arrays come in order, so we verify and append.
                    result[array_name] = result.get(array_name, [])
                    if array_index != len(result[array_name]):
                        raise CJsonError('Internal ast error. Array {} out of order. '
                                         'Expected index {}, got {}'.format(
                            array_name, len(result[array_name]), array_index))
                    result[array_name].append(to_dict(child))
                else:
                    result[child_name] = to_dict(child)

            # Any child attributes that were missing need "None" values in the json.
            for child_attr in child_attrs_of(klass):
                if child_attr not in result:
                    result[child_attr] = None

            return result

        def to_json(node, **kwargs):
            """ Convert ast node to json string """
            return json.dumps(to_dict(node), **kwargs)

        if os.name == 'nt':
            log.error("THIS PART MAY NOT WORK SINCE IT'S ON WINDOWS")
            # ast = parse_file(os.getcwd() + "\\" + path, use_cpp=True, cpp_args=r'-Ifake_libc_include')
            ast = parse_file(path, use_cpp=True, cpp_args=r'-Ifake_libc_include')
        else:
            include_path = r'-I' + os.getcwd() + r'/../fake_libc_include'
            # ast = parse_file(os.getcwd() + '/../example/' + path, use_cpp=True, cpp_args=include_path)
            ast = parse_file(path, use_cpp=True, cpp_args=include_path)

        pattern = re.compile(".*\"_nodetype\"\: \"Decl\".*")
        pattern2 = re.compile(".*\"_nodetype\"\: \"ID\".*")
        pattern3 = re.compile(".*\"_nodetype\"\: \"Constant\".*")
        pattern4 = re.compile(".*\"op\"\: \".*\".*")
        conv = json.loads(to_json(ast))
        ast = json.dumps(conv, indent=4, sort_keys=True)
        ast = str(ast)
        l_ast = str(ast).split('\n')
        for i, ast_line in enumerate(l_ast):
            if bool(re.search(pattern, ast_line)):
                id_counter += 1
                num_spaces = len(re.search("(.*)\"_nodetype.*", ast_line).group(1))
                regex = r'.{' + str(num_spaces) + r'}\"name\"\: \".*\".*'
                location = []
                raw_id = ''
                for j, line in enumerate(l_ast[i + 1:]):
                    if bool(re.fullmatch(r'\s{' + str(num_spaces) + r'}"coord": ".*:(\d+:\d+)".*', line)):
                        location = re.fullmatch(r'\s{' + str(num_spaces) + r'}\"coord\"\: \".*\:(\d+\:\d+)\".*',
                                                line).group(1)
                    if line.strip().startswith('"init"') and line.strip() != '"init": null,':
                        for init_line in l_ast[i + j + 1:]:
                            if init_line.strip().startswith('"coord"'):
                                init_loc = re.fullmatch(r'.*"coord": ".*:(\d+:\d+)".*', init_line).group(1)
                                init_offset = int(location.split(":")[1]) + int((int(init_loc.split(":")[1]) -
                                                                                 int(location.split(":")[1])) / 2)
                                # ops.append(['=', int(init_loc.split(":")[0]), init_offset])
                                ops.append([int(init_loc.split(":")[0]), int(init_loc.split(":")[0]),
                                            init_offset, init_offset + 1])
                                op_counter += 1
                                unique_ops.add('=')
                            if init_line.strip().startswith('}'):
                                break
                    if bool(re.fullmatch(regex, line)):
                        try:
                            raw_id = re.search(r'.*\"name\"\: "(.*)".*', line).group(1)
                        except AttributeError:
                            raw_id = ''
                        break
                # ids.append([raw_id, int(location.split(":")[0]), int(location.split(":")[1])])
                ids.append([int(location.split(":")[0]), int(location.split(":")[0]),
                            int(location.split(":")[1]), int(location.split(":")[1]) + len(raw_id)])
                unique_ids.add(raw_id)
            if bool(re.search(pattern2, ast_line)):
                id_counter += 1
                try:
                    raw_id = re.search('.*\"name\"\: "(.*)".*', l_ast[i + 2]).group(1)
                except AttributeError:
                    raw_id = ''
                location = re.search('.*\"coord\"\: \".*\:(\d+\:\d+)\".*', l_ast[i + 1]).group(1)
                # ids.append([raw_id, int(location.split(":")[0]), int(location.split(":")[1])])
                ids.append([int(location.split(":")[0]), int(location.split(":")[0]),
                            int(location.split(":")[1]), int(location.split(":")[1]) + len(raw_id)])
                unique_ids.add(raw_id)
            if bool(re.search(pattern3, ast_line)):
                lit_counter += 1
                num_spaces = len(re.search("(.*)\"_nodetype.*", ast_line).group(1))
                regex = r'.{' + str(num_spaces) + r'}\"value\"\: \".*\".*'
                location = []
                raw_lit = ''
                for line in l_ast[i + 1:]:
                    if bool(re.fullmatch(r'\s{' + str(num_spaces) + r'}"coord": ".*:(\d+:\d+)".*', line)):
                        location = re.fullmatch(r'\s{' + str(num_spaces) + r'}\"coord\"\: \".*\:(\d+\:\d+)\".*',
                                                line).group(1)
                    if bool(re.fullmatch(regex, line)):
                        try:
                            raw_lit = re.search(r'.*\"value\"\: "(.*)".*', line).group(1)
                            raw_lit = raw_lit.strip()
                            try:
                                raw_lit = int(raw_lit)
                            except ValueError:
                                try:
                                    raw_lit = float(raw_lit)
                                except ValueError:
                                    raw_lit = bytes(raw_lit, "utf-8").decode("unicode_escape")
                                    raw_lit = bytes(raw_lit, "utf-8").decode("unicode_escape")
                                    raw_lit = raw_lit[1:len(raw_lit) - 1]
                        except AttributeError:
                            raw_lit = ''
                        break
                # lits.append([raw_lit, int(location.split(":")[0]), int(location.split(":")[1])])
                lits.append([int(location.split(":")[0]), int(location.split(":")[0]),
                             int(location.split(":")[1]), int(location.split(":")[1]) + len(str(raw_lit))])
                unique_lits.add(raw_lit)
            if bool(re.search(pattern4, ast_line)):
                op_counter += 1
                raw_op = ''
                try:
                    raw_op = re.search(r'.*\"op\"\: "(.*)".*', ast_line).group(1)
                except AttributeError as e:
                    log.error(e)
                num_spaces = len(re.search("(.*)\"op.*", ast_line).group(1))
                regex = r'.{' + str(num_spaces) + r'}\"coord\"\: \".*\".*'
                location = []
                found = False
                rev_i = i - 1
                while not found:
                    if bool(re.fullmatch(regex, l_ast[rev_i])):
                        location = re.fullmatch(r'\s{' + str(num_spaces) + r'}\"coord\"\: \".*\:(\d+\:\d+)\".*',
                                                l_ast[rev_i]).group(1)
                        found = True
                    rev_i -= 1
                # ops.append([raw_op, int(location.split(":")[0]), int(location.split(":")[1])])
                ops.append([int(location.split(":")[0]), int(location.split(":")[0]),
                            int(location.split(":")[1]), int(location.split(":")[1]) + len(raw_op)])
                unique_ops.add(raw_op)

    elif lang == 'cpp':
        import subprocess
        import os
        # cwd = os.path.dirname(__file__)
        if os.name != 'nt':
            filename = path
        else:
            log.error("IF WE HAVE TO RUN THIS ON WINDOWS THEN I'LL HAVE TO FIX THIS PART")
        cmd = 'clang++ -cc1 -std=c++11 -stdlib=libstdc++ -I/usr/include/c++/7 -I/usr/include/c++/7.5.0 -I/usr/include/x86_64-linux-gnu/c++/7 -I/usr/include/x86_64-linux-gnu/c++/7.5.0 -dump-raw-tokens ' + filename + ' 2>&1'
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        p.wait()
        (ast_str, err) = p.communicate()
        ast_str = ast_str.decode('utf-8')
        if ast_str.startswith("error"):
            log.error(ast_str)
        l_ast = ast_str.split('\n')
        for ast_line in l_ast:
            if ast_line.startswith(tuple(c_plusplus_ops)):
                raw_op = ast_line.split()[1][1:len(ast_line.split()[1]) - 1]
                op_counter += 1
                if bool(re.search(r"Loc\=\<.*\.cpp\:(.*)\>", ast_line)):
                    location = re.search(r"Loc\=\<.*\.cpp\:(.*)\>", ast_line).group(1)
                    # ops.append([raw_op, int(location.split(':')[0]), int(location.split(':')[1])])
                    ops.append([int(location.split(':')[0]), int(location.split(':')[0]),
                                int(location.split(':')[1]), int(location.split(':')[1]) + len(raw_op)])
                    unique_ops.add(raw_op)
            if ast_line.startswith('numeric_constant') or ast_line.startswith('string_literal'):
                raw_lit = ast_line.split()[1][1:len(ast_line.split()[1]) - 1]
                lit_counter += 1
                if bool(re.search(r"Loc\=\<.*\.cpp\:(.*)\>", ast_line)):
                    location = re.search(r"Loc\=\<.*\.cpp\:(.*)\>", ast_line).group(1)
                    # lits.append([raw_lit, int(location.split(':')[0]), int(location.split(':')[1])])
                    lits.append([int(location.split(':')[0]), int(location.split(':')[0]),
                                 int(location.split(':')[1]), int(location.split(':')[1]) + len(raw_lit)])
                    unique_lits.add(raw_lit)
            if bool(re.search(r"raw\_identifier.*", ast_line)):
                try:
                    raw_id = re.search(r"raw_identifier '(.*)'", ast_line).group(1)
                except AttributeError:
                    raw_id = ''
                if raw_id == "'true'" or raw_id == "'false'":
                    lit_counter += 1
                    if bool(re.search(r"Loc\=\<.*\.cpp\:(.*)\>", ast_line)):
                        location = re.search(r"Loc\=\<.*\.cpp\:(.*)\>", ast_line).group(1)
                        # lits.append([raw_id, int(location.split(':')[0]), int(location.split(':')[1])])
                        lits.append([int(location.split(':')[0]), int(location.split(':')[0]),
                                     int(location.split(':')[1]), int(location.split(':')[1]) + len(raw_id)])
                        unique_lits.add(raw_id)
                if raw_id not in c_plusplus_keywords:
                    id_counter += 1
                    # find line location
                    if bool(re.search(r"Loc\=\<.*\.cpp\:(.*)\>", ast_line)):
                        location = re.search(r"Loc\=\<.*\.cpp\:(.*)\>", ast_line).group(1)
                        # ids.append([raw_id, int(location.split(':')[0]), int(location.split(':')[1])])
                        ids.append([int(location.split(':')[0]), int(location.split(':')[0]),
                                    int(location.split(':')[1]), int(location.split(':')[1]) + len(raw_id)])
                        unique_ids.add(raw_id)

    # format: [id/lit/op, [start line, end line], [start offset, end offset]]
    elif lang == 'js':
        import esprima
        js_ops = ['=', '+=', '-=', '*=', '**=', '/=', '%=', '<<=', '>>=', '>>>=',
                  '&=', '|=', '^=', ',', '+', '-', '*', '**', '/', '%', '++', '--', '<<', '>>', '>>>', '&',
                  '|', '^', '!', '~', '&&', '||', '?', ':', '===', '==', '>=',
                  '<=', '<', '>', '!=', '!==']
        items = list(esprima.tokenize(''.join(content), options={'loc': True}))
        for each in items:
            if each.type == 'Identifier':
                id_counter += 1
                # ids.append([each.value, [each.loc.start.line, each.loc.end.line],
                #             each.loc.start.column, each.loc.end.column])
                ids.append([each.loc.start.line, each.loc.end.line,
                            each.loc.start.column, each.loc.end.column])
                unique_ids.add(each.value)
            if each.type == 'Punctuator' and each.value in js_ops:
                op_counter += 1
                # ops.append([each.value, [each.loc.start.line, each.loc.end.line],
                #             each.loc.start.column, each.loc.end.column])
                ops.append([each.loc.start.line, each.loc.end.line,
                            each.loc.start.column, each.loc.end.column])
                unique_ops.add(each.value)
            if each.type == 'String' or each.type == 'Numeric':
                lit_counter += 1
                # lits.append([each.value, [each.loc.start.line, each.loc.end.line],
                #              each.loc.start.column, each.loc.end.column])
                lits.append([each.loc.start.line, each.loc.end.line,
                            each.loc.start.column, each.loc.end.column])
                unique_lits.add(each.value)

    # format: [id/lit/op, [start line, end line], [start offset, end offset]]
    elif lang == 'java':
        import javac_parser
        java_ops = ['+', '-', '*', '/', '%', '+', '--', '++', '=', '!', '==', '!=', '>', '>=', '<', '<=', '&&',
                    '||', '?:', 'instanceof', '~', '<<', '>>', '>>>', '&', '^', '|']
        java = javac_parser.Java()
        for each in java.lex(''.join(content)):
            if each[0] == 'IDENTIFIER':
                id_counter += 1
                # ids.append([each[1], [each[2][0], each[3][0]],
                #             [each[2][1], each[3][1]]])
                ids.append([each[2][0], each[3][0],
                            each[2][1], each[3][1]])
                unique_ids.add(each[1])
            if each[0] == 'INTLITERAL':
                lit_counter += 1
                # lits.append([each[1], [each[2][0], each[3][0]],
                #              [each[2][1], each[3][1]]])
                lits.append([each[2][0], each[3][0],
                             each[2][1], each[3][1]])
                unique_lits.add(each[1])
            if each[0] == 'STRINGLITERAL':
                lit_counter += 1
                # lits.append([each[1][1:len(each[1]) - 1], [each[2][0], each[3][0]],
                #              [each[2][1], each[3][1]]])
                lits.append([each[2][0], each[3][0],
                             each[2][1], each[3][1]])
                unique_lits.add(each[1][1:len(each[1]) - 1])
            if each[1] in java_ops:
                op_counter += 1
                # ops.append([each[1], [each[2][0], each[3][0]],
                #             [each[2][1], each[3][1]]])
                ops.append([each[2][0], each[3][0],
                            each[2][1], each[3][1]])
                unique_ops.add(each[1])

    if verbose:
        # log.info('\n')
        log.info("IDENTIFIERS")
        log.info(ids)
        log.info(unique_ids)
        log.info("num ids found: " + str(id_counter))
        log.info("unique ids: " + str(len(unique_ids)))
        # log.info('\n')
        log.info("LITERALS")
        log.info(lits)
        log.info(unique_lits)
        log.info("num ops found: " + str(lit_counter))
        log.info("unique ops: " + str(len(unique_lits)))
        # log.info('\n')
        log.info("OPERATORS")
        log.info(ops)
        log.info(unique_ops)
        log.info("num ops found: " + str(op_counter))
        log.info("unique ops: " + str(len(unique_ops)))
    # return all above in a tuple in the same order printed above without unique count since
    # it can be obtained by calling len()
    return tuple([ids, unique_ids, id_counter, lits, unique_lits, lit_counter, ops, unique_ops, op_counter])
