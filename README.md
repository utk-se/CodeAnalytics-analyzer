# CodeAnalytics-analyzer

CodeAnalytics is a framework comprised of both an analyzer and distributor module for the purpose of aggregating github repository information given a cloned repo (i.e number of files, length of files, popularity of the repo, and mch more). Using the information gathered by these modules, it is possible to observe the general shape/structure of code for each unique repo.

## Supported File Types

- Java
- Python
- C++/C
- JavaScript

## Output Format

The output of this analyzer will follow this format in a json file for a given repo:

```py
    # Empty output objects to be populated & dumped
    repo_obj = {
        "file_objs": [],
        "num_lines": None,
        "num_files": 0
    }

    file_obj = {
        "num_lines": None,
        "file_extension": None,
        "methods": [],  #  Tuples w/ start and end lines of methods/classes
        "classes": [],
        "lines": []
    }

    line_obj = {
        # [var, func call, loop, conditional, return,
        #  assignment, include/import]
        # 'is' subject to change due to lizard's capabilities
        "is": [None, None, None, None, None, None, None],
        "start_index": None,  # int specifying where line starts
        "has_tabs": None,  # boolean for existence
        "end_index": None  # int specifying where line ends
    }

```

## List of Dependencies

To install, type: pip install -r requirements.txt

* lizard - https://github.com/terryyin/lizard
* PyDriller - https://github.com/ishepard/pydriller
* Git
* Python3

## Pip Installation

> IN PROGRESS
