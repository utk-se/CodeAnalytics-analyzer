# CodeAnalytics-analyzer

Aiden and Jonathan:

 - Given the path to a repo of code
 - Run analysis for all data points specified in metrics points (look at [lizard](https://github.com/terryyin/lizard))
 - Return results in a file based parseable format

## Pip Dependencies

To install, type: pip install -r requirements.txt

* lizard - https://github.com/terryyin/lizard
* PyDriller - https://github.com/ishepard/pydriller
* argparse

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

## Other Dependencies
* Git
* Python3
