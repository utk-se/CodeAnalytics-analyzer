import re


class LangNotSupportedError(Exception):
    """Raised when user tries to parse an unsupported language"""
    pass


def find_comments(content, path, lang):
    comments = []
    if lang == 'py':
        import tokenize
        with open(path, 'rb') as f:
            tokens = tokenize.tokenize(f.readline)
            for token in tokens:
                if tokenize.tok_name[token.type] == 'COMMENT':
                    # comments.append([token.string, token.start, token.end])
                    #print(token.start[0])
                    #print(token.start[1])
                    #print(token.end[0])
                    #print(token.end[1])
                    comments.append([token.start[0] - 1, token.end[0] - 1, token.start[1], token.end[1]])

    # comments format: [comment name, [start line, start offset], [end line, end offset]]
    #                                           OR
    #                  [comment name, line, offset]
    elif lang == 'c' or lang == 'java' or lang == 'js' or lang == 'cpp' or lang == 'h':
        single_line = re.compile(
            r"^[^(\")]*((\")[^(\")]*(\")[^(\")]*)*\/\/")
        one_line_block = re.compile(
            r"^[^(\")]*((\")[^(\")]*(\")[^(\")]*)*\/[*].*[*]\/")
        begin_block = re.compile(
            r"^[^(\")]*((\")[^(\")]*(\")[^(\")]*)*\/[*]")
        end_block = re.compile(r"^[^(\")]*((\")[^(\")]*(\")[^(\")]*)*[*]\/")
        skip_lines = []
        for num, line in enumerate(content):
            if one_line_block.match(line):
                skip_lines.append(num)
                offset = len(re.search(r"(.*)\/[*].*[*]\/", line).group(1))
                # comment = re.search(r".*\/[*](.*)[*]\/", line).group(1)
                # comments.append([comment.strip(), num, offset])
                comments.append([num, num, offset, len(line)])

        for num, line in enumerate(content):
            if num not in skip_lines and begin_block.match(line):
                skip_lines.append(num)
                offset = len(re.search(r"(.*)\/[*]", line).group(1))
                # comment = re.search(r".*\/[*](.*)", line).group(1)
                for num2, line2 in enumerate(content[num + 1:]):
                    num2 += (num + 1)
                    skip_lines.append(num2)
                    if end_block.match(line2):
                        l_offset = len(
                            re.search(r"(.*)[*]\/", line2).group(1))
                        # comment += re.search(r"(.*)[*]\/", line2).group(1)
                        # comments.append(
                        #     [comment.strip(), [num, offset], [num2, l_offset]])
                        comments.append(
                            [num, num2, offset, l_offset])
                        break
                    else:
                        pass
                        # comment += line2

        for num, line in enumerate(content):
            if num not in skip_lines:
                if single_line.match(line):
                    offset = len(re.search(r"(.*)\/\/", line).group(1))
                    # comment = re.search(r".*\/\/(.*)", line).group(1)
                    # comments.append([comment.strip(), num, offset])
                    comments.append([num, num, offset, len(line)])

    else:
        raise LangNotSupportedError(lang + " not supported yet")

    return comments
