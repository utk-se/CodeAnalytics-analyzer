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
import json
import re
from cadistributor import log

SUPPORTED_FILETYPES = ["cpp", "h", "java", "js", "py"]
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
        (None by default.) #TODO: Implement ignorefile.

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
            or any(re.fullmatch(_format_pattern(esc_path, p),
                    root + os.sep + f) != None
                    for p in negate)
            or (all(re.fullmatch(p, f) == None
                    for p in ignore)
            and all(re.fullmatch(_format_pattern(esc_path, p),
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
            avg_file_length = self.num_lines / self.num_files

        repo_obj = {
            "file_objs" : self.file_objs,
            "file_exts" : self.file_exts,
            "num_dirs"  : self.num_dirs,
            "num_files" : self.num_files,
            "num_lines" : self.num_lines,
            "max_depth" : self.max_depth,
            "avg_file_length" : avg_file_length
        }

        if output_path:
            try:
                with open(output_path, 'w') as out:
                    json.dump(repo_obj, out, 0)

            except IOError: 
                log.err("Could not write to file: " + output_path)
                pass

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
    methods : list of pair
        List of pairs containing the indices of the first and last lines
        of methods within the file.
    classes : list of pair
        List of pairs containing the indices of the first and last lines
        of classes within the file.
    num_tokens : int
        Total number of code tokens within the file.
    """

    def __init__(self, file_path, file_ext, tabsize=4):
        self.file_path = file_path
        self.file_ext  = file_ext
        self.line_objs = []
        self.num_lines = 0
        self.methods   = []
        self.classes   = []
        self.libs      = []
        self.comments  = []
        self.ids       = []
        self.literals  = []
        self.operators = []

        try:
            analysis = lizard.analyze_file(file_path)

        except RecursionError:
            # Log the error, then raise it for the caller. This 
            # allows File to be used alone or as part of Repo.
            log.err("Error with lizard analysis.")
            raise RecursionError

        # --------------------------------------------------------
        # Tokens
        # --------------------------------------------------------
        self.num_tokens = analysis.token_count

        # --------------------------------------------------------
        # Lines
        # --------------------------------------------------------
        try:
            # Analyze each line in the file
            with open(file_path) as file:
                for index, line in enumerate(file):
                    self.num_lines += 1

                    line_obj = Line(index, line, tabsize)
                    self.line_objs.append(line_obj.export())
            
        except IOError:
            log.err("Could not read file: " + file_path)
            raise IOError

        # --------------------------------------------------------
        # Methods
        # --------------------------------------------------------
        for func in analysis.function_list:
            method = (func.__dict__["start_line"],
                        func.__dict__["end_line"])
            
            self.methods.append(method)

        # --------------------------------------------------------
        # TODO: Classes
        # --------------------------------------------------------

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
                log.err("Could not write to file: " + output_path)

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
                log.err("Could not write to file: " + output_path)

        return line_obj