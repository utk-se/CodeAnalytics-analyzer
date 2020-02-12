import re

def space_counter(string): # counts num spaces before class keyword
    space_count = 0
    for char in string:
        if char == ' ':
            space_count += 1
        else:
            break
    return space_count

def find_classes(path, verbose=0, lang='python'):
    with open(path, 'r') as f:
        class_tuples = []
        content = f.readlines()
        if lang == 'python':
            pattern = re.compile("\s*class [^\s]*:\n")
            for line_no_start, line in enumerate(content):
                if pattern.match(line) is not None:
                    if verbose:
                        print("found class at line #", line_no_start + 1)
                    # finding end of class
                    space_count_1 = space_counter(line)
                    if verbose:
                        print('space count', space_count_1)
                    eof_bool = True
                    for line_no_end, line2 in enumerate(content[line_no_start + 1:]):
                        line_no_end += line_no_start
                        if space_count_1 == space_counter(line2):
                            eof_bool = False
                            if verbose:
                                print("found end of class at line #", line_no_end + 1)
                            class_tuples.append(tuple([line_no_start, line_no_end]))
                            break
                    if eof_bool:
                        if verbose:
                            print('found end of class at eof line #', line_no_end + 2)
                        class_tuples.append(tuple([line_no_start, line_no_end + 1]))
        elif lang == 'java':
            pattern = re.compile("\s*public class [^\s]*\s*{")
            for line_no_start, line in enumerate(content):
                if pattern.match(line) is not None:
                    if verbose:
                        print("found class at line #", line_no_start + 1)
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
                            class_tuples.append(tuple([line_no_start, line_no_end + 1]))
                            if verbose:
                                print('found end of class at line #', line_no_end + 2)
                            break
        elif lang == 'c++':
            pattern = re.compile("\s*(class|struct) [^\s]*\s*{")
            pattern2 = re.compile("\s*(class|struct) [^\s]*\s*")
            for line_no_start, line in enumerate(content):
                if pattern.match(line) is not None or \
                (pattern2.match(line) is not None and '{' in content[line_no_start + 1]):
                    if verbose:
                        print("found class at line #", line_no_start + 1)
                    # finding end of class
                    for line_no_end, line2 in enumerate(content[line_no_start + 1:]):
                        line_no_end += line_no_start
                        if '};' in line2:
                            quote_position = line2.find('"')
                            end_class_position = line2.find("};")
                            next_quote_position = line2.find('"', quote_position)
                            if not ((quote_position >= 0 and quote_position < end_class_position)
                            and (next_quote_position >= 0 and next_quote_position > end_class_position)
                            and line2.count('"') % 2 == 0):
                                class_tuples.append(tuple([line_no_start, line_no_end + 1]))
                                if verbose:
                                    print('found end of class at line #', line_no_end + 2)
                                break
        elif lang == 'c':
            pattern = re.compile("\s*struct [^\s]*\s*{")
            pattern2 = re.compile("\s*struct [^\s]*\s*")
            for line_no_start, line in enumerate(content):
                if pattern.match(line) is not None or \
                (pattern2.match(line) is not None and '{' in content[line_no_start+1]):
                    if verbose:
                        print("found class at line #", line_no_start + 1)
                    # finding end of class
                    for line_no_end, line2 in enumerate(content[line_no_start + 1:]):
                        line_no_end += line_no_start
                        if '};' in line2:
                            quote_position = line2.find('"')
                            end_class_position = line2.find("};")
                            next_quote_position = line2.find('"', quote_position)
                            if not ((quote_position >= 0 and quote_position < end_class_position)
                            and (next_quote_position >= 0 and next_quote_position > end_class_position)
                            and line2.count('"') % 2 == 0):
                                class_tuples.append(tuple([line_no_start, line_no_end + 1]))
                                if verbose:
                                    print('found end of class at line #', line_no_end + 2)
                                break
        return class_tuples

