"""CodeAnalytics Analyzer

A set of tools to gather metrics about code repositories, files, or 
individual lines that can be used to compare code projects. Given a 
repository, file, or line, produces a static analysis of the visual 
structure of the code within, such as use of whitespace, line length, 
and distribution of code elements, such as tokens, methods, and classes.

Notes
--------------------------------------------------------------------------
    Initialize an instance of Repo or File with a filepath, or one of Line
    with a string, to gather analytics on that source.
    
    Supply an ignorefile to exclude files and directories from analysis.

    Retrieve results as a serializable dictionary by calling the export()
    method.
"""

import os
import lizard
import parso
import json
import re
import sys
from .class_finder import find_classes
from .lib_finder import find_libs
from .comment_finder import find_comments
from .id_finder import find_ids
from .py_func_arg_finder import find_methods_and_args
from cadistributor import log

SUPPORTED_FILETYPES = ["c", "cpp", "h", "java", "js", "py"]
"""Extensions of supported filetypes (list of str)."""

ESC_SEP = re.escape(os.sep)
"""Regex-escaped os separator."""

class Repo:
    """Generates analytics for a code repository.

    Parameters
    ----------------------------------------------------------------------
    input_path : str
        Path to repository to analyse.
    ignorefile : str, optional
        Path to file specifying rules for excluding files from analysis.
        (None by default.)
    tabsize : int, optional
        The number of spaces with which to represent a tab character. (4
        by default.)
    
    Attributes
    ----------------------------------------------------------------------
    file_objs : list of dict
        List of dictionaries containing analytics for each file within
        the repo.
    file_exts : set of str
        A set of each file extension appearing within the repo.
    num_dirs : int
        Total number of directories within the repo, excluding the 
        top-level directory.
    num_files : int
        Total number of files within the repo.
    num_lines : int
        Total number of lines of code within the repo.
    max_depth : int
        Maximum directory depth of the repo. (The top level is depth 0.)
    avg_file_length : float
        Average number of lines between files in the repo.
    """

    def _format_pattern(self, esc_path, pattern):
        """Internal method.
        """
        if re.match(re.escape(ESC_SEP), pattern) != None:
            return esc_path + pattern
        return esc_path + ESC_SEP + pattern

    def _ignore(self, f, root, esc_path, ignore, negate):
        """Internal method.
        """
        return not (any(re.fullmatch(p, f) != None
                    for p in negate)
            or any(re.fullmatch(self._format_pattern(esc_path, p),
                    root + os.sep + f) != None
                    for p in negate)
            or (all(re.fullmatch(p, f) == None
                    for p in ignore)
            and all(re.fullmatch(self._format_pattern(esc_path, p),
                    root + os.sep + f) == None
                    for p in ignore)))

    def __init__(self, input_path, ignorefile=None, tabsize=4):
        self.input_path = input_path
        self.ignorefile = ignorefile
        self.tabsize    = tabsize

        self.file_objs = []
        self.file_exts = set()
        self.num_dirs  = 0
        self.num_files = 0
        self.num_lines = 0
        self.max_depth = 0
        self.avg_file_length = 0

        # ----------------------------------------------------------------
        # Ignorefile
        # ----------------------------------------------------------------
        # Escaped os separator and path for use in ignorefile regex
        esc_path = re.escape(input_path)

        # The following dictionary translates ignorefile expressions
        # into standard regular expressions for filtering files and dirs
        ignorefile_trans = {
            r"([^\\]|^)#.*" : "",
            r"^!.*" : "",
            r"/" : ESC_SEP,
            r"\\#" : "#",
            r"\\!" : "!",
            r"\." : r"\.",
            r"\?" : "[^{}]{}".format(ESC_SEP, r"{1}"),
            r"\*" : "[^{}]*".format(ESC_SEP)
        }
        reg = re.compile(r'(%s)' % "|".join(ignorefile_trans.keys()))

        if ignorefile:
            with open(ignorefile, "r") as f:
                lines = [l for l in (line.strip() for line in f) if l]
        else:
            lines = []

        # Negated patterns (don't ignore files/dirs specified by these).
        # TODO: Improve performance, and finish making it match gitignore
        #  syntax. (Currently, leading '/' does nothing.)
        neg_dirs  = [l for l in (reg.sub(lambda m:
                        ignorefile_trans[
                            [k for k in ignorefile_trans if 
                                re.search(k, m.string[m.start():m.end()])
                            ][0]], line.lstrip()[1:]) for line in lines
                            if re.match(r"!", line))]
        
        neg_files = [l for l in (reg.sub(lambda m:
                        ignorefile_trans[
                            [k for k in ignorefile_trans if 
                                re.search(k, m.string[m.start():m.end()])
                            ][0]], line.lstrip()[1:]) for line in lines
                            if re.fullmatch(r"!.*[^/]", line))]

        # Ignored patterns (ignore files/dirs specified by these).
        # NOTE: Patterns with a / at the end match only directories
        ig_dirs  = [l for l in (reg.sub(lambda m:
                        ignorefile_trans[
                            [k for k in ignorefile_trans if 
                                re.search(k, m.string[m.start():m.end()])
                            ][0]], re.sub(r"/$", "", line))
                        for line in lines)
                        if l]

        ig_files = [l for l in (reg.sub(lambda m:
                        ignorefile_trans[
                            [k for k in ignorefile_trans if 
                                re.search(k, m.string[m.start():m.end()])
                            ][0]], line.strip())
                        for line in lines
                        if re.fullmatch(r".*[^/]", line))
                        if l]

        # Walk through each file, directory by directory.
        for root, dirs, files in os.walk(input_path):
            # Exclude files and directories specified in ignorefile
            files   = [f for f in files if not self._ignore(f, root,
                                        esc_path, ig_files, neg_files)]
            dirs[:] = [d for d in dirs if not self._ignore(d, root,
                                        esc_path, ig_dirs, neg_dirs)]

            # Update running max depth
            self.max_depth = max(self.max_depth, root.count(os.sep))

            # Tally directories
            self.num_dirs  += len(dirs)
            self.num_files += len(files)

            for f in files:
                file_path = os.path.join(root, f)
                file_ext  = file_path.split('.')[-1]

                # Ignore unsupported filetypes.
                if file_ext not in SUPPORTED_FILETYPES:
                    continue

                # Register file extension in the set of observed exts.
                self.file_exts.add(file_ext)

                try:
                    is_minified = False
                    if file_ext == 'js':
                        with open(file_path, 'r') as jsf:
                            jsf_lines = jsf.readlines()
                            no_news = True
                            if len(jsf_lines) > 1:
                                no_news = False
                            if no_news or ' ' not in jsf_lines[0][:50]:
                                is_minified = True
                                log.error(file_path + ' is minified')
                    if not is_minified:
                        file_obj = File(file_path, file_ext, tabsize)
                except (RecursionError, IOError) as e:
                    continue

                # Add file analytics to repo analytics
                self.num_lines += file_obj.num_lines
                self.file_objs.append(file_obj.export())

        # ----------------------------------------------------------------
        # Overall Repo Analytics
        # ----------------------------------------------------------------
        # Adjust max depth, where the top level of the repo is depth 0
        self.max_depth -= input_path.count(os.sep)

    def export(self, output_path=None):
        """Output chosen analytics for the repo.

        TODO: Implement options to exclude certain analytics. (Hence, 
        "chosen analytics".)

        Parameters
        ------------------------------------------------------------------
        output_path : str, optional
            Path at which to output analytics json. (None by default. In
            this case, it still returns a dictionary but does not write to
            a file.)

        Returns
        ------------------------------------------------------------------
        dict
            Serializable dictionary of chosen analytics.
        """
        if self.num_files > 0:
            self.avg_file_length = self.num_lines / self.num_files

        repo_obj = {
            "file_objs" : self.file_objs,
            "file_exts" : self.file_exts,
            "num_dirs"  : self.num_dirs,
            "num_files" : self.num_files,
            "num_lines" : self.num_lines,
            "max_depth" : self.max_depth,
            "avg_file_length" : self.avg_file_length
        }

        if output_path:
            try:
                with open(output_path, 'w') as out:
                    json.dump(repo_obj, out, 0)

            except IOError: 
                log.error("Could not write to file: " + output_path)

        return repo_obj

class File:
    """Stores analytics for a file.

    Parameters
    ----------------------------------------------------------------------
    file_path : str
        The path to the file.
    file_ext : str
        The file extension.

    Attributes
    ----------------------------------------------------------------------
    file_path : str
        The path to the file.
    file_ext : str
        The file extension.
    line_objs : list of dict
        List of dictionaries containing analytics for each line of code
        within the file.
    num_lines : int
        Total number of lines of code within the file.
    methods : list of 4-tuples
        List of tuples containing the indices of the first and last lines
        of methods within the file, as well as the leading whitespace and
        the length of the first line.
    parameters : list of 3-tuples
        List of tuples containing the line index and, relative to that
        line, the indices of the first and last characters of method 
        parameters within the file.
    classes : tuple of lists of 3 integers and 1 list of integers
        Tuple of lists of starting line, ending line, starting offset, and a list of endings offset of classes.
        If the list of ending offsets is just an integer then that means the class only spanned one line.
    libs : list of lists of 4 integers
        List of lists of starting line, ending line, starting offset, and ending offset of libraries.
    comments : list of lists of 4 integers
        List of lists of starting line, ending line, starting offset, and ending offset of comments.
    ids : list of lists of 4 integers
        List of lists of starting line, ending line, starting offset, and ending offset of identifiers.
    literals : list of lists of 4 integers
        List of lists of starting line, ending line, starting offset, and ending offset of literals.
    operators : list of lists of 4 integers
        List of lists of starting line, ending line, starting offset, and ending offset of operators.
    num_tokens : int
        Total number of code tokens within the file.
    """

    def __init__(self, file_path, file_ext, tabsize=4):
        self.file_path  = file_path
        self.file_ext   = file_ext
        self.line_objs  = []
        self.methods    = []
        self.parameters = []
        self.classes    = []
        self.libs       = []
        self.comments   = []
        self.ids        = []
        self.literals   = []
        self.operators  = []

        lines = []
        log.info(file_path)

        try:
            analysis = lizard.analyze_file(file_path)

        except RecursionError:
            # Log the error, then raise it for the caller. This 
            # allows File to be used alone or as part of Repo.
            log.error("Error with lizard analysis.")
            raise RecursionError

        # ----------------------------------------------------------------
        # Tokens
        # ----------------------------------------------------------------
        self.num_tokens = analysis.token_count

        # ----------------------------------------------------------------
        # Lines
        # ----------------------------------------------------------------
        try:
            # Analyze each line in the file
            with open(file_path, errors='replace') as f:
                lines = f.readlines()
                self.num_lines = len(lines)
                for index, line in enumerate(f):
                    line_obj = Line(index, line, tabsize)
                    self.line_objs.append(line_obj.export())
            
        except IOError:
            log.error("Could not read file: " + file_path)
            raise IOError

        # ----------------------------------------------------------------
        # Methods and Paramaters
        # ----------------------------------------------------------------
        def count_newlines(string, char_offset):
            char_index = char_offset
            ret = 0
            while char_index >= 0:
                if string[char_index] == '\n':
                    ret += 1
                char_index -= 1
            return ret

        if file_ext != 'py':
            for func in analysis.function_list:
                start_index = func.__dict__["start_line"] - 1
                length      = len(lines[start_index])
                lead_wspace = length - len(lines[start_index].lstrip())

                method = (start_index, func.__dict__["end_line"] - 1,
                          lead_wspace, length)
                self.methods.append(method)

                # parameter format: (line num, offset, end offset)
                i = start_index
                for param in func.full_parameters:
                    param = param.lstrip('\\').lstrip().lstrip('\\').lstrip()
                    param_split = [re.escape(one)+r'\s*(<.*>)*(\(.*\))*' for one in param.split()]
                    p = "\s*".join(param_split)
                    # Match and determine span of parameter in line
                    m = re.compile(r"\(?(.+,\s*)*({})\s*(\/\*.*\*\/\s*)*\s*([,:=].*|.*\)|\/\*.*)".format(p), re.DOTALL)
                    spans_multiple_lines = False
                    start_l = start_index
                    start_offset = 0
                    end_l = func.__dict__["end_line"] - 1
                    end_offset = 0
                    while True:
                        try:
                            match = m.search(lines[i])
                        except IndexError:
                            spans_multiple_lines = True
                            func_lines = [func_line for func_line in lines[start_index:func.__dict__["end_line"]]]
                            func_lines = ''.join(func_lines)
                            match = m.search(func_lines)
                            if match is None:
                                log.error("Can't find'", param, "'!")
                                exit()
                            else:
                                start_l = start_index + count_newlines(func_lines, match.start(2))
                                start_offset = match.start(2)
                                end_l = start_index + count_newlines(func_lines, match.end(2))
                                sum_lengths = 0
                                for param_line in lines[start_l:end_l]:
                                    sum_lengths += len(param_line)
                                end_offset = match.end(2) - sum_lengths
                                break
                        if match is None:
                            i += 1
                        else:
                            break
                    if spans_multiple_lines:
                        func_lines = list(range(start_l, end_l+1))
                        start_offsets = []
                        end_offsets = []
                        start_offsets.append(start_offset)
                        end_offsets.append(len(lines[start_l]))
                        for func_line in lines[start_l+1:end_l]:
                            start_offsets.append(len(func_line) - len(func_line.lstrip()))
                            end_offsets.append(len(func_line))
                        start_offsets.append(len(lines[end_l]) - len(lines[end_l].lstrip()))
                        end_offsets.append(end_offset)
                        parameter = (func_lines, start_offsets, end_offsets)
                        self.parameters.append(parameter)
                    else:
                        offset = match.span(2)
                        parameter = (start_index, offset[0], offset[1]-1)
                        self.parameters.append(parameter)
        else:
            with open(file_path, errors='replace') as s:
                parser = parso.parse(s.read())
                mags = find_methods_and_args(parser.children, lines)
                self.methods = mags[0]
                self.parameters = mags[1]
        log.info('finished methods and parameters')
        # ----------------------------------------------------------------
        # Classes
        # ----------------------------------------------------------------
        self.classes = find_classes(lines, file_path, file_ext)
        log.info('finished classes')
        # ----------------------------------------------------------------
        # Libraries
        # ----------------------------------------------------------------
        self.libs = find_libs(lines, file_path, file_ext)
        log.info('finished libs')
        # ----------------------------------------------------------------
        # Comments
        # ----------------------------------------------------------------
        self.comments = find_comments(lines, file_path, file_ext)
        log.info('finished comments')
        # ----------------------------------------------------------------
        # Identifiers, Literals, and Operators
        # ----------------------------------------------------------------
        ids = find_ids(lines, file_path, file_ext)
        self.ids = ids[0]
        self.literals = ids[3]
        self.operators = ids[6]
        log.info('finished ids')

    def export(self, output_path=None):
        """Output chosen analytics for the file.

        TODO: Implement options to exclude certain analytics. (Hence, 
        "chosen analytics".)

        Parameters
        ------------------------------------------------------------------
        output_path : str, optional
            Path at which to output analytics json. (None by default. In
            this case, it still returns a dictionary but does not write to
            a file.)
        
        Returns
        ------------------------------------------------------------------
        dict
            Serializable dictionary of chosen analytics.
        """
        file_obj = {
            "file_path": self.file_path,
            "file_ext": self.file_ext,
            "line_objs": self.line_objs,
            "num_lines": self.num_lines,
            "methods": self.methods,
            "parameters": self.parameters,
            "classes": self.classes,
            "libs": self.libs,
            "comments": self.comments,
            "ids": self.ids,
            "literals": self.literals,
            "operators": self.operators,
            "num_tokens": self.num_tokens
        }

        if output_path:
            try:
                with open(output_path, 'w') as out:
                    json.dump(file_obj, out, 0)

            except IOError: 
                log.error("Could not write to file: " + output_path)

        return file_obj

class Line:
    """Stores analytics for a line.
    
    Parameters
    ----------------------------------------------------------------------
    index : int
        The index of the line within the file.
    line  : str
        The contents of the line
    tabsize : int, optional
        The number of spaces with which to represent a tab character. (4
        by default.)

    Attributes
    ----------------------------------------------------------------------
    index : int
        The index of the line within the file.
    start : int
        The index of the first non-whitespace character within the line.
    end : int
        The index of the last non-whitespace character within the line.
    length : int
        The number of characters in the line (with tabs expanded).
    num_tabs : int
        The number of tab characters in the line.
    num_spaces : int
        The number of space characters in the line.
    """

    def __init__(self, index, line, tabsize=4):
        self.index = index

        self.num_tabs   = line.count('\t')
        self.num_spaces = line.count(' ')

        line = line.expandtabs(tabsize)

        self.length = len(line)
        self.start  = self.length - len(line.lstrip())
        self.end    = len(line.rstrip()) - 1

    def export(self, output_path=None):
        """Output chosen analytics for the line.
        
        TODO: Implement options to exclude certain analytics. (Hence, 
        "chosen analytics".)

        Parameters
        ------------------------------------------------------------------
        output_path : str, optional
            Path at which to output analytics json. (None by default. In
            this case, it still returns a dictionary but does not write to
            a file.)

        Returns
        ------------------------------------------------------------------
        dict
            Serializable dictionary of chosen analytics.
        """
        line_obj = {
            "index": self.index,
            "start": self.start,
            "end": self.end,
            "length": self.length,
            "num_tabs": self.num_tabs,
            "num_spaces": self.num_spaces
        }

        if output_path:
            try:
                with open(output_path, 'w') as out:
                    json.dump(line_obj, out, 0)

            except IOError: 
                log.error("Could not write to file: " + output_path)

        return line_obj