import re
from cadistributor import log


def find_comments(content, path, lang):
    comments = []
    if lang == 'py':
        import tokenize
        with open(path, 'rb') as f:
            tokens = tokenize.tokenize(f.readline)
            for token in tokens:
                if tokenize.tok_name[token.type] == 'COMMENT':
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
                        start_offsets = [offset]
                        start_offsets.extend([len(k) - len(k.lstrip()) for k in content[num+1:num2+1]])
                        end_offsets = [len(k) for k in content[num:num2]]
                        end_offsets.append(l_offset)
                        comments.append([num, num2, start_offsets, end_offsets])
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
        log.err(lang + " not supported yet")

    return comments
