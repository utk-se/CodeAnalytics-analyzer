import re

def find_comments(path, lang, verbose=0):
    with open(path, 'r') as f:
        lines = []
        content = f.readlines()
        if lang == 'py':
            double_quote_hash = re.compile("^[^(\")]*((\")[^(\")]*(\")[^(\")]*)*\#.*?")
            single_quote_hash = re.compile("^[^(\')]*((\')[^(\')]*(\')[^(\')]*)*\#.*?")
            single_quote_one_line_block1 = re.compile("^[^(\")]*((\")[^(\")]*(\")[^(\")]*)*\'{3}.*\'{3}?")
            single_quote_one_line_block2 = re.compile("^[^(\')]*((\')[^(\')]*(\')[^(\')]*)*\'{3}.*\'{3}?")
            double_quote_one_line_block1 = re.compile("^[^(\")]*((\")[^(\")]*(\")[^(\")]*)*\"{3}.*\"{3}?")
            double_quote_one_line_block2 = re.compile("^[^(\')]*((\')[^(\')]*(\')[^(\')]*)*\"{3}.*\"{3}?")
            single_quote_begin_block1 = re.compile("^[^(\")]*((\")[^(\")]*(\")[^(\")]*)*\'{3}?")
            single_quote_begin_block2 = re.compile("^[^(\')]*((\')[^(\')]*(\')[^(\')]*)*\'{3}?")
            double_quote_begin_block1 = re.compile("^[^(\")]*((\")[^(\")]*(\")[^(\")]*)*\"{3}?")
            double_quote_begin_block2 = re.compile("^[^(\')]*((\')[^(\')]*(\')[^(\')]*)*\"{3}?")
            single_quote_end_block = re.compile(".*\'{3}")
            double_quote_end_block = re.compile(".*\"{3}")
            skip_lines = []
            for num, line in enumerate(content):
                if single_quote_one_line_block1.match(line) or single_quote_one_line_block2.match(line)\
                        or double_quote_one_line_block1.match(line) or double_quote_one_line_block2.match(line):
                    lines.append(num)
                    skip_lines.append(num)
                    if verbose:
                        print("block on", num+1)
            if verbose:
                print("DONE ONE LINE BLOCKS")
            # single quote begin block
            for num, line in enumerate(content):
                if num not in skip_lines and\
                        (single_quote_begin_block1.match(line) or single_quote_begin_block2.match(line)):
                    lines.append(num)
                    skip_lines.append(num)
                    if verbose:
                        print("block on", num+1)
                    for num2, line2 in enumerate(content[num + 1:]):
                        num2 += (num + 1)
                        lines.append(num2)
                        skip_lines.append(num2)
                        if verbose:
                            print("block on", num2+1)
                        if single_quote_end_block.match(line2):
                            break
            if verbose:
                print("DONE SINGLE QUOTE BLOCKS")
            # double quote begin block
            for num, line in enumerate(content):
                if num not in skip_lines and\
                        (double_quote_begin_block1.match(line) or double_quote_begin_block2.match(line)):
                    lines.append(num)
                    skip_lines.append(num)
                    if verbose:
                        print("block on", num+1)
                    for num2, line2 in enumerate(content[num + 1:]):
                        num2 += (num + 1)
                        lines.append(num2)
                        skip_lines.append(num2)
                        if verbose:
                            print("block on", num2+1)
                        if double_quote_end_block.match(line2):
                            break
            if verbose:
                print("DONE DOUBLE QUOTE BLOCKS")
            for num, line in enumerate(content):
                if num not in skip_lines:
                    if double_quote_hash.match(line) or single_quote_hash.match(line):
                        lines.append(num)
                        if verbose:
                            print("hash on", num+1)
            if verbose:
                print("DONE HASH")
        ####################################################################################################
        elif lang == 'c' or lang == 'java' or lang == 'js':
            single_line = re.compile("^[^(\")]*((\")[^(\")]*(\")[^(\")]*)*\/\/?")
            one_line_block = re.compile("^[^(\")]*((\")[^(\")]*(\")[^(\")]*)*\/[*]{1}.*[*]{1}\/?")
            begin_block = re.compile("^[^(\")]*((\")[^(\")]*(\")[^(\")]*)*\/[*]{1}?")
            end_block = re.compile("^[^(\")]*((\")[^(\")]*(\")[^(\")]*)*[*]{1}\/?")
            skip_lines = []
            for num, line in enumerate(content):
                if one_line_block.match(line):
                    lines.append(num)
                    skip_lines.append(num)
                    if verbose:
                        print("block on", num + 1)
            if verbose:
                print("DONE ONE LINE BLOCKS")
            for num, line in enumerate(content):
                if num not in skip_lines and begin_block.match(line):
                    lines.append(num)
                    skip_lines.append(num)
                    if verbose:
                        print("block on", num + 1)
                    for num2, line2 in enumerate(content[num + 1:]):
                        num2 += (num + 1)
                        lines.append(num2)
                        skip_lines.append(num2)
                        if verbose:
                            print("block on", num2 + 1)
                        if end_block.match(line2):
                            break
            if verbose:
                print("DONE COMMENT BLOCKS")
            for num, line in enumerate(content):
                if num not in skip_lines:
                    if single_line.match(line):
                        lines.append(num)
                        if verbose:
                            print("slashes on", num + 1)
            if verbose:
                print("DONE SLASHES")
        ####################################################################################################
        else:
            print(lang, "not supported yet")
            exit()
    lines.sort()
    return lines
