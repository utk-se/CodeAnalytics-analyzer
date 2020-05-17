import lizard
import numpy as np
from .util import findnth, splitWithIndices, line_start, line_end
from cadistributor import log

'''
Base tokenizer class. Implement one yourself.
How do I know when to implement a tokenizer?
If you can represent your desired item as a code segment
with a start and end index, you should use this.

If you are instead calculating a scalar or aggregated metric from a code
segment or collection of code segments, use a metric. (See metrics.py)

Default Tokenizer: FileTokenizer

Tokenizers todo:
TODO: ClassDeclaration
TODO: MethodDeclaration
TODO: Tokenizer (non whitespace)
TODO: ImportTokenizer
TODO: AssignmentTokenizer
TODO: CommentTokenizer
TODO: IdentifierTokenizer
TODO: make lines newline separated by default

TODO: AST can process many tokens at once: MultiTokenizer
TODO: Tokenizer merging
'''


class BaseTokenizer:

    # return the filetypes currently supported
    @staticmethod
    def get_supported_filetypes():
        raise NotImplementedError

    # unique identifier for shorthand use
    @staticmethod
    def keys():
        raise NotImplementedError
    '''
    return a list of start & end indexes
    '''
    @staticmethod
    # List[Callable[[str], List[Tuple[int, int, int, int]]]]
    def tokenize(self, lines):
        raise NotImplementedError('Use a subclass')


'''
Use this class to parse multiple token types in one sweep of the input.
(n_token_types, n_tokens, start:endinfo)
'''


class MultiTokenizer(BaseTokenizer):
    @staticmethod
    def get_supported_filetypes():
        raise NotImplementedError

    # unique identifier for shorthand use
    @staticmethod
    def keys():
        raise NotImplementedError

    def tokenize(self, lines):
        raise NotImplementedError


'''
return token indices for a file
'''


class Tokenizer(BaseTokenizer):

    @staticmethod
    def get_supported_filetypes():
        return ['py', 'cpp', 'js', 'h', 'java']

    @staticmethod
    def keys():
        return ['token']

    @staticmethod
    def tokenize(lines, **kwargs):
        rv = {}
        rv['token'] = []

        bigline = ' '.join(lines)
        # log.info(list(splitWithIndices(bigline)))
        for i, line in enumerate(lines):
            for token_start, token_end in splitWithIndices(line):
                rv['token'].append([i, i+1, token_start, token_end])
        return rv


class FileTokenizer(BaseTokenizer):

    @staticmethod
    def get_supported_filetypes():
        return ['py', 'cpp', 'js', 'h', 'java']

    @staticmethod
    def keys():
        return ['file']

    @staticmethod
    def tokenize(lines, **kwargs):
        rv = {}
        # log.info('lines: {}'.format(lines))
        rv['file'] = np.array(
            [[0, len(lines), line_start(lines[0]), line_end(lines[-1])]], dtype=np.int)

        return rv


'''
return all tokens matching patterns for methods

C/C++ (works with C++14)
Java
C# (C Sharp)
JavaScript (With ES6 and JSX)
Objective-C
Swift
Python
Ruby
TTCN-3
PHP
Scala
GDScript
Golang
Lua
Rust

'''


class MethodTokenizer(BaseTokenizer):

    @staticmethod
    def get_supported_filetypes():
        return ['py', 'cpp', 'js', 'h', 'java']

    @staticmethod
    def keys():
        return ['method']

    # this method assumes that method starts at start of line
    # and it's probably pretty slow
    # consider replacing with regex?
    # https://stackoverflow.com/questions/68633/regex-that-will-match-a-java-method-declaration

    @staticmethod
    def tokenize(lines, **kwargs):
        # potentially refactor to return set of strings, use yield statement
        # for reduced memory footprint
        lang = kwargs['lang']
        i = lizard.analyze_file.analyze_source_code(lang, '\n'.join(lines))
        rv = {}
        # TODO: don't output as np array; output as tuple
        for key in MethodTokenizer.keys():
            rv[key] = np.zeros((len(i.function_list), 4), dtype=np.int)

        for j, func in enumerate(i.function_list):
            rv['method'][j][0] = func.start_line-1
            rv['method'][j][1] = func.end_line
            line = lines[func.start_line-1]
            rv['method'][j][2] = line_start(line)
            line = lines[func.end_line-1]
            rv['method'][j][3] = line_end(line)+1

        return rv


class LineTokenizer(BaseTokenizer):

    @staticmethod
    def get_supported_filetypes():
        return ['py', 'cpp', 'js', 'h', 'java']

    @staticmethod
    def keys():
        return ['newline']

    @staticmethod
    def tokenize(lines, **kwargs):
        rv = {}
        for key in LineTokenizer.keys():
            # rv[key] = {
            #     'line_start': [range(len(lines))],
            #     'line_end': [range(len(lines))],
            #     'char_start': [len(line) - len(line.lstrip()) for line in lines],
            #     'char_end': [len(line.rstrip()) for line in lines]
            # }
            rv[key] = np.array([list(range(len(lines))), list(range(1, len(lines)+1)), [
                line_start(line) for line in lines],
                [line_end(line)+1 for line in lines]], dtype=np.int).T

        return rv


class ClassTokenizer(BaseTokenizer):
    @staticmethod
    def get_supported_filetypes():
        return ['py', 'cpp', 'js', 'h', 'java']

    @staticmethod
    def keys():
        return ['class']

    # @staticmethod
    # def tokenize(self, lines):
