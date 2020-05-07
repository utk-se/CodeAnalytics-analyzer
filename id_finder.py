import re

c_keywords = ['auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 'double', 'else',
              'enum', 'extern', 'float', 'for', 'goto', 'if', 'int', 'long', 'register', 'return',
              'short', 'signed', 'sizeof', 'static', 'struct', 'switch', 'typedef', 'union',
              'unsigned', 'void', 'volatile', 'while']

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

java_keywords = ['abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 'char', 'class', 'continue',
                 'const',
                 'default', 'do', 'double', 'else', 'enum', 'exports', 'extends', 'final', 'finally', 'float', 'for',
                 'goto',
                 'if', 'implements', 'import', 'instanceof', 'int', 'interface', 'long', 'module', 'native', 'new',
                 'package', 'private', 'protected', 'public', 'requires', 'return', 'short', 'static', 'strictfp',
                 'super',
                 'switch', 'synchronized', 'this', 'throw', 'throws', 'transient', 'try', 'var', 'void', 'volatile',
                 'while']


def find_ids(path, lang, skip_lines=[], verbose=0):
    with open(path, 'r') as f:
        content = f.readlines()
        id_counter = 0
        unique_ids = set()
        final_unique = set()
        if lang == 'py':
            pass
        elif lang == 'c':
            id_pattern = re.compile('\**[a-zA-Z_][a-zA-Z0-9_]*(;|,|\[.*\]|=.*)*')
            func_pattern = re.compile('([a-zA-Z_][a-zA-Z0-9_]*\.)*[a-zA-Z_][a-zA-Z0-9_]*(\(.*\))')
            for num in range(len(content)):
                if num not in skip_lines:
                    # find strings in line
                    restart = True
                    while restart:
                        restart = False
                        for char_i in range(len(content[num])):
                            if content[num][char_i] == '"':
                                for char_j in range(char_i + 1, len(content[num])):
                                    if content[num][char_j] == '"':
                                        content[num] = content[num][:char_i] + content[num][char_j + 1:]
                                        restart = True
                                        break
                                if restart:
                                    break
                    matches = set()
                    funcs = func_pattern.search(content[num])
                    if funcs is not None:
                        matches.add(funcs.group())
                        id_counter += 1
                        content[num] = content[num][:funcs.start()] + content[num][funcs.end() + 1:]
                    split_line = content[num].split()
                    for each in split_line:
                        if id_pattern.fullmatch(each) and each not in c_keywords:
                            matches.add(each)
                            id_counter += 1
                    unique_ids.update(list(matches))
            print(unique_ids)
            print("num ids:", id_counter)
        elif lang == 'c++':
            id_pattern = re.compile('[a-zA-Z_][a-zA-Z0-9_]*')
            func_pattern = re.compile('([a-zA-Z_][a-zA-Z0-9_]*\.)*[a-zA-Z_][a-zA-Z0-9_]*(\(.*\))')
            for num in range(len(content)):
                if num not in skip_lines:
                    # find strings in line
                    restart = True
                    while restart:
                        restart = False
                        for char_i in range(len(content[num])):
                            if content[num][char_i] == '"':
                                for char_j in range(char_i + 1, len(content[num])):
                                    if content[num][char_j] == '"':
                                        content[num] = content[num][:char_i] + content[num][char_j + 1:]
                                        restart = True
                                        break
                                if restart:
                                    break
                    matches = set()
                    funcs = func_pattern.search(content[num])
                    if funcs is not None:
                        matches.add(funcs.group())
                        id_counter += 1
                        content[num] = content[num][:funcs.start()] + content[num][funcs.end() + 1:]
                    split_line = content[num].split()
                    for each in split_line:
                        if id_pattern.fullmatch(each) and each not in c_plusplus_keywords:
                            matches.add(each)
                            id_counter += 1
                    unique_ids.update(list(matches))
            print(unique_ids)
            print("num ids:", id_counter)
        elif lang == 'java':
            id_pattern = re.compile('[a-zA-Z_][a-zA-Z0-9_]*')
            func_pattern = re.compile('([a-zA-Z_][a-zA-Z0-9_]*\.)*[a-zA-Z_][a-zA-Z0-9_]*(\(.*\))')
            for num in range(len(content)):
                if num not in skip_lines:
                    # find strings in line
                    restart = True
                    while restart:
                        restart = False
                        for char_i in range(len(content[num])):
                            if content[num][char_i] == '"':
                                for char_j in range(char_i + 1, len(content[num])):
                                    if content[num][char_j] == '"':
                                        content[num] = content[num][:char_i] + content[num][char_j + 1:]
                                        restart = True
                                        break
                                if restart:
                                    break
                    matches = set()
                    funcs = func_pattern.search(content[num])
                    if funcs is not None:
                        matches.add(funcs.group())
                        id_counter += 1
                        content[num] = content[num][:funcs.start()] + content[num][funcs.end() + 1:]
                    split_line = content[num].split()
                    for each in split_line:
                        if id_pattern.fullmatch(each) and each not in java_keywords:
                            matches.add(each)
                            id_counter += 1
                    unique_ids.update(list(matches))
            print(unique_ids)
            print("num ids found:", id_counter)

        for one_id in unique_ids:
            if one_id.startswith('*') or one_id.startswith('&'):
                one_id = one_id[1:]
            if one_id.startswith('++') or one_id.startswith('--'):
                one_id = one_id[2:]
            if one_id.endswith('++') or one_id.endswith('--'):
                one_id = one_id[:len(one_id)-2]
            if one_id.endswith(',') or one_id.endswith(';'):
                one_id = one_id[:len(one_id)-1]
            final_unique.add(one_id)

        print("unique ids:", len(final_unique))