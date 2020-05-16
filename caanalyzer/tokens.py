import lizard
import numpy as np
from .util import findnth, splitWithIndices

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

dict output
{
    'tokenizer/column keys 1' : [linestart, linestop, charstart, charend]
}
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
    def tokenize(self, codestr):
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

    def tokenize(self, codestr):
        return super().tokenize(self, codestr)


'''
return token indices for a file
'''


class FileTokenizer(BaseTokenizer):

    @staticmethod
    def get_supported_filetypes():
        return ['py', 'cpp', 'js', 'h', 'java']

    @staticmethod
    def keys():
        return ['file']

    @staticmethod
    def tokenize(self, codestr):
        return np.array([0, len(codestr)-1])


class LineTokenizer(BaseTokenizer):

    @staticmethod
    def get_supported_filetypes():
        return ['py', 'cpp', 'js', 'h', 'java']

    @staticmethod
    def keys():
        return ['newline']

    @staticmethod
    def tokenize(codestr, lang):
        return np.array(splitWithIndices(codestr, '\n'))


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
    def tokenize(codestr, lang):
        i = lizard.analyze_file.analyze_source_code(lang, codestr)
        codestr_split = codestr.split('\n')
        rv = {}
        for key in keys():
            # rv[key] = {
            #     'line_start': [],
            #     'line_end': [],
            #     'char_start': [],
            #     'char_end': []
            # }
            rv[key] = np.zeros((len(i.function_list), 4))

        for j, func in enumerate(i.function_list):
            rv['method'][j][0] = func.start_line-1
            rv['method'][j][1] = func.end_line - 1
            line = codestr_split[func.start_line-1]
            rv['method'][j][2] = len(line) - len(line.lstrip())
            line = codestr_split[func.end_line-1]
            rv['method'][j][3] = len(line) - len(line.lstrip())

        return rv


class NewlineTokenizer(BaseTokenizer):

    @staticmethod
    def get_supported_filetypes():
        return ['py', 'cpp', 'js', 'h', 'java']

    @staticmethod
    def keys():
        return ['newline']

    @staticmethod
    def tokenize(codestr, lang):
        codestr = codestr.split('\n')
        rv = {}
        for key in keys():
            # rv[key] = {
            #     'line_start': [range(len(codestr))],
            #     'line_end': [range(len(codestr))],
            #     'char_start': [len(line) - len(line.lstrip()) for line in codestr],
            #     'char_end': [len(line.rstrip()) for line in codestr]
            # }
            rv[key] = np.array([[range(len(codestr))], [range(len(codestr))], [
                               len(line) - len(line.lstrip()) for line in codestr],
                [len(line.rstrip()) for line in codestr]])

        return rv


class ClassTokenizer(BaseTokenizer):
    @staticmethod
    def get_supported_filetypes():
        return ['py', 'cpp', 'js', 'h', 'java']

    @staticmethod
    def keys():
        return ['class']

    # @staticmethod
    # def tokenize(self, codestr):
