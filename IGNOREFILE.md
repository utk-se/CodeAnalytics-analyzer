# Ignorefile

An ignorefile specifies files and directories to be ignored during analysis. Each line of an ignorefile is a comment or specifies a pattern used to identify files and directories to ignore.

## Usage

Initialize `caanalyzer.Repo` with an ignorefile, like so:
```py
    repo = caanalyzer.Repo(path_to_repo, path_to_ignorefile)
```

An ignorefile is optional; if one is not supplied, then no files under the repository will be ignored.

## Pattern Syntax

- A blank line matches no files.
- A line beginning with `#` serves as a comment. The use of `#` within a pattern must be escaped using a backslash (`\`).
- The prefix `!` negates the following pattern, so as to un-ignore a file or directory ignored by another pattern. It is not possible to un-ignore a file if a parent directory of that file is ignored. The use of `!` at the beginning of a pattern must be escaped using a backslash (`\`).
- The slash `/` is used as the directory separator, regardless of operating system. 
    - A slash at the end of a pattern matches *only* directories. **Otherwise, patterns match both files and directories.**
    - A slash at the beginning or in the middle of a pattern matches files and directories relative to the top-level of the analysed repository.
    > ### For Example
    >
    >`/lorem/ipsum` is equivalent to `lorem/ipsum`, and both match the file or directory `/lorem/ipsum` but not `/dir/lorem/ipsum`.
    >
    >`ipsum` matches `/ipsum`, `/lorem/ipsum`, and `/dir/lorem/ipsum`.
    >
    >`ipsum/` matches `/ipsum`, `/lorem/ipsum`, and `/dir/lorem/ipsum` only if they are directories.
- An `*` matches anything (zero or more characters) except the directory separator.
- A `?` matches any one character except the directory separator.
- One or more ranges within brackets (e.g. `[a-zA-Z0-9]) match one character within those ranges.
- The sequence `**/` matches zero or more directories.
> ### For Example
>
> `**/ipsum` is equivalent to `ipsum`.
>
> `**/lorem/ipsum` matches `/lorem/ipsum` and `/dir/lorem/ipsum`.
>
> `**/x/**/y` matches `/x/y`, `/x/a/y`, and `/w/x/a/y`.