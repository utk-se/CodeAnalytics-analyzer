# Empty output objects to be populated & dumped
repo_obj = {
    "file_objs": [],
    "num_lines": None,
    "num_files": 0
}

file_obj = {
    "num_lines": None,
    "file_extension": None,
    "methods": [],  #  Pair/Tuples with start and end lines of methods/classes
    "classes": [],
    "lines": []
}

line_obj = {
    # Proposed usage: [var, func call, loop, conditional, return,
    # assignment, include/import]
    # 'is' subject to change. These could be used for different heatmat 'colors'
    "is": [None, None, None, None, None, None, None],
    "start_index": None,  # int specifying where line starts
    "has_tabs": None,  # boolean for existence
    "end_index": None  # int specifying where line ends
}

supported_filetypes = ['py', 'cpp', 'js', 'h', 'java']
