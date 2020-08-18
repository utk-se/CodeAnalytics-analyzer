# CodeAnalytics-analyzer

# CodeAnalytics

Gathers metrics and analyzes code repositories.

## Features

- Retrieve information about file count, languages, depth of a code repository, etc.
- Has customized lexers and AST parsers for Java, JavaScript, C, C++, and Python
- Extract metrics from code segments with simple user-defined functions
- Visualize code metrics using heatmaps

## Data Format

Methods: starting line, ending line, starting line offsets, ending line offsets 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; OR line, starting offset, ending offset 

Parameters: starting line, ending line, starting line offsets, ending line offsets 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; OR line, starting offset, ending offset

Classes: starting line, ending line, starting line offsets, ending line offsets 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; OR line, starting offset, ending offset

Libraries: line, starting offset, ending offset

Comments: line, starting offset, ending offset

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; OR starting line, ending line, starting offsets, ending offsets

Identifiers, Literals, and Operators: line, starting offset, ending offset

## Installation

pip install caanalyzer
