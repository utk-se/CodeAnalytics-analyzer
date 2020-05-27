# CodeAnalytics

Extends the functionality of pandas for analyzing code repositories.

## Features

- Retrieve information about file count, languages, depth of a code repository
- Index a repository based on language, file, and scopes
- Use provided lexers, AST parsers or easily add your own to configure scopes and languages being tracked
- Extract metrics from code segments with simple user-defined functions
- Visualize code metrics using heatmaps
- Perform performant slicing, grouping, and filtering operations as provided by pandas for concise and powerful analysis
- Save and load results in wide variety of tabular and compressed formats supported by pandas, including csv, sql, hdf5, json, feather, and more
- [See pandas](https://github.com/pandas-dev/pandas/blob/master/README.md)

## Installation

pip install caanalyzer

## Example Usage

See test.ipynb under examples for example usage.

```py
# Import the class as well as provided
from caanalyzer import CodeRepo
from caanalyzer.tokens import MethodTokenizer, FileTokenizer, LineTokenizer, Tokenizer
from caanalyzer.metrics import width, height, num_tokens

repo = CodeRepo('path')


repo.index([FileTokenizer, LineTokenizer, MethodTokenizer], {'size' : len, 'width': width, 'height' : height, 'num_tokens': num_tokens})

# get statistics about each scope
repo.df.groupby('token_type').mean()

# get only info about python files
repo.df.xs(('.py'), level=('lang'))

# save
repo.df.to_hdf('output/clang_index.h5', key='df', mode='w')
```
