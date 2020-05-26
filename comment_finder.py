import re

def find_comments(path, lang, verbose=0):
    with open(path, 'r') as f:
        content = f.readlines()
        comments = []
        if lang == 'py':
            import tokenize
            with open(path, 'rb') as f:
                tokens = tokenize.tokenize(f.readline)
                for token in tokens:
                    if tokenize.tok_name[token.type] == 'COMMENT':
                        comments.append([token.string, token.start, token.end])
            # for comment in comments:
            #     print(comment)
            '''
            double_quote_hash = re.compile("^[^(\")]*((\")[^(\")]*(\")[^(\")]*)*\#.*?")
            single_quote_hash = re.compile("^[^(\')]*((\')[^(\')]*(\')[^(\')]*)*\#.*")
            single_quote_one_line_block1 = re.compile("^[^(\")]*((\")[^(\")]*(\")[^(\")]*)*\'{3}.*\'{3}")
            single_quote_one_line_block2 = re.compile("^[^(\')]*((\')[^(\')]*(\')[^(\')]*)*\'{3}.*\'{3}")
            double_quote_one_line_block1 = re.compile("^[^(\")]*((\")[^(\")]*(\")[^(\")]*)*\"{3}.*\"{3}")
            double_quote_one_line_block2 = re.compile("^[^(\')]*((\')[^(\')]*(\')[^(\')]*)*\"{3}.*\"{3}")
            single_quote_begin_block1 = re.compile("^[^(\")]*((\")[^(\")]*(\")[^(\")]*)*\'{3}")
            single_quote_begin_block2 = re.compile("^[^(\')]*((\')[^(\')]*(\')[^(\')]*)*\'{3}")
            double_quote_begin_block1 = re.compile("^[^(\")]*((\")[^(\")]*(\")[^(\")]*)*\"{3}")
            double_quote_begin_block2 = re.compile("^[^(\')]*((\')[^(\')]*(\')[^(\')]*)*\"{3}")
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
                if num not in skip_lines and \
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
            '''

        # comments format: [comment name, [start line, start offset], [end line, end offset]]
        #                                           OR
        #                  [comment name, line, offset]
        elif lang == 'c' or lang == 'java' or lang == 'js' or lang == 'c++':
            # from comment_parser import comment_parser
            # import magic
            # mime = magic.Magic(mime=True)
            # com_obj = comment_parser.extract_comments_from_str(''.join(content), mime=mime.from_file(path))
            # print(com_obj)

            single_line = re.compile("^[^(\")]*((\")[^(\")]*(\")[^(\")]*)*\/\/")
            one_line_block = re.compile("^[^(\")]*((\")[^(\")]*(\")[^(\")]*)*\/[*].*[*]\/")
            begin_block = re.compile("^[^(\")]*((\")[^(\")]*(\")[^(\")]*)*\/[*]")
            end_block = re.compile("^[^(\")]*((\")[^(\")]*(\")[^(\")]*)*[*]\/")
            skip_lines = []
            for num, line in enumerate(content):
                if one_line_block.match(line):
                    skip_lines.append(num)
                    offset = len(re.search(r"(.*)\/[*].*[*]\/", line).group(1))
                    comment = re.search(r".*\/[*](.*)[*]\/", line).group(1)
                    comments.append([comment.strip(), num, offset])
                    if verbose:
                        print("block on", num + 1)
            if verbose:
                print("DONE ONE LINE BLOCKS")

            for num, line in enumerate(content):
                if num not in skip_lines and begin_block.match(line):
                    skip_lines.append(num)
                    offset = len(re.search(r"(.*)\/[*]", line).group(1))
                    comment = re.search(r".*\/[*](.*)", line).group(1)
                    if verbose:
                        print("block on", num + 1)
                    for num2, line2 in enumerate(content[num + 1:]):
                        num2 += (num + 1)
                        skip_lines.append(num2)
                        if verbose:
                            print("block on", num2 + 1)
                        if end_block.match(line2):
                            l_offset = len(re.search(r"(.*)[*]\/", line2).group(1))
                            comment += re.search(r"(.*)[*]\/", line2).group(1)
                            comments.append([comment.strip(), [num, offset], [num2, l_offset]])
                            break
                        else:
                            comment += line2
            if verbose:
                print("DONE COMMENT BLOCKS")
            for num, line in enumerate(content):
                if num not in skip_lines:
                    if single_line.match(line):
                        offset = len(re.search(r"(.*)\/\/", line).group(1))
                        #com_len = len(re.search(r".*(\/\/.*)", line).group(1))
                        comment = re.search(r".*\/\/(.*)", line).group(1)
                        comments.append([comment.strip(), num, offset])
                        if verbose:
                            print("slashes on", num + 1)
            if verbose:
                print("DONE SLASHES")

        else:
            print(lang, "not supported yet")
            exit()
    return comments
