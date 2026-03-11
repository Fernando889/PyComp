# `!glob`{.interpreted-text role="mod"} \-\-- Unix style pathname pattern expansion

::: {.module synopsis="Unix shell style pathname pattern expansion."}
glob
:::

**Source code:** `Lib/glob.py`{.interpreted-text role="source"}

::: index
single: filenames; pathname expansion
:::

------------------------------------------------------------------------

::: index
single: \* (asterisk); in glob-style wildcards single: ? (question mark); in glob-style wildcards single: \[\] (square brackets); in glob-style wildcards single: ! (exclamation); in glob-style wildcards single: - (minus); in glob-style wildcards single: . (dot); in glob-style wildcards
:::

The `!glob`{.interpreted-text role="mod"} module finds pathnames using pattern matching rules similar to the Unix shell. No tilde expansion is done, but `*`, `?`, and character ranges expressed with `[]` will be correctly matched. This is done by using the `os.scandir`{.interpreted-text role="func"} and `fnmatch.fnmatch`{.interpreted-text role="func"} functions in concert, and not by actually invoking a subshell.

:::: note
::: title
Note
:::

The pathnames are returned in no particular order. If you need a specific order, sort the results.
::::

Files beginning with a dot (`.`) can only be matched by patterns that also start with a dot, unlike `fnmatch.fnmatch`{.interpreted-text role="func"} or `pathlib.Path.glob`{.interpreted-text role="func"}. For tilde and shell variable expansion, use `os.path.expanduser`{.interpreted-text role="func"} and `os.path.expandvars`{.interpreted-text role="func"}.

For a literal match, wrap the meta-characters in brackets. For example, `'[?]'` matches the character `'?'`.

The `!glob`{.interpreted-text role="mod"} module defines the following functions:

::::::::::::: function
glob(pathname, \*, root_dir=None, dir_fd=None, recursive=False, include_hidden=False)

Return a possibly empty list of path names that match *pathname*, which must be a string containing a path specification. *pathname* can be either absolute (like `/usr/src/Python-1.5/Makefile`{.interpreted-text role="file"}) or relative (like `../../Tools/\*/\*.gif`{.interpreted-text role="file"}), and can contain shell-style wildcards. Broken symlinks are included in the results (as in the shell). Whether or not the results are sorted depends on the file system. If a file that satisfies conditions is removed or added during the call of this function, whether a path name for that file will be included is unspecified.

If *root_dir* is not `None`, it should be a `path-like object`{.interpreted-text role="term"} specifying the root directory for searching. It has the same effect on `!glob`{.interpreted-text role="func"} as changing the current directory before calling it. If *pathname* is relative, the result will contain paths relative to *root_dir*.

This function can support `paths relative to directory descriptors
<dir_fd>`{.interpreted-text role="ref"} with the *dir_fd* parameter.

::: index
single: \*\*; in glob-style wildcards
:::

If *recursive* is true, the pattern \"`**`\" will match any files and zero or more directories, subdirectories and symbolic links to directories. If the pattern is followed by an `os.sep`{.interpreted-text role="data"} or `os.altsep`{.interpreted-text role="data"} then files will not match.

If *include_hidden* is true, \"`**`\" pattern will match hidden directories.

::: audit-event
glob.glob pathname,recursive glob.glob
:::

::: audit-event
glob.glob/2 pathname,recursive,root_dir,dir_fd glob.glob
:::

:::: note
::: title
Note
:::

Using the \"`**`\" pattern in large directory trees may consume an inordinate amount of time.
::::

:::: note
::: title
Note
:::

This function may return duplicate path names if *pathname* contains multiple \"`**`\" patterns and *recursive* is true.
::::

::: versionchanged
3.5 Support for recursive globs using \"`**`\".
:::

::: versionchanged
3.10 Added the *root_dir* and *dir_fd* parameters.
:::

::: versionchanged
3.11 Added the *include_hidden* parameter.
:::
:::::::::::::

:::::::::: function
iglob(pathname, \*, root_dir=None, dir_fd=None, recursive=False, include_hidden=False)

Return an `iterator`{.interpreted-text role="term"} which yields the same values as `glob`{.interpreted-text role="func"} without actually storing them all simultaneously.

::: audit-event
glob.glob pathname,recursive glob.iglob
:::

::: audit-event
glob.glob/2 pathname,recursive,root_dir,dir_fd glob.iglob
:::

:::: note
::: title
Note
:::

This function may return duplicate path names if *pathname* contains multiple \"`**`\" patterns and *recursive* is true.
::::

::: versionchanged
3.5 Support for recursive globs using \"`**`\".
:::

::: versionchanged
3.10 Added the *root_dir* and *dir_fd* parameters.
:::

::: versionchanged
3.11 Added the *include_hidden* parameter.
:::
::::::::::

:::: function
escape(pathname)

Escape all special characters (`'?'`, `'*'` and `'['`). This is useful if you want to match an arbitrary literal string that may have special characters in it. Special characters in drive/UNC sharepoints are not escaped, e.g. on Windows `escape('//?/c:/Quo vadis?.txt')` returns `'//?/c:/Quo vadis[?].txt'`.

::: versionadded
3.4
:::
::::

::::: function
translate(pathname, \*, recursive=False, include_hidden=False, seps=None)

Convert the given path specification to a regular expression for use with `re.match`{.interpreted-text role="func"}. The path specification can contain shell-style wildcards.

For example:

> \>\>\> import glob, re \>\>\> \>\>\> regex = glob.translate(\'\*\*/\*.txt\', recursive=True, include_hidden=True) \>\>\> regex \'(?s:(?:.+/)?\[\^/\]\*\\.txt)\\z\' \>\>\> reobj = re.compile(regex) \>\>\> reobj.match(\'foo/bar/baz.txt\') \<re.Match object; span=(0, 15), match=\'foo/bar/baz.txt\'\>

Path separators and segments are meaningful to this function, unlike `fnmatch.translate`{.interpreted-text role="func"}. By default wildcards do not match path separators, and `*` pattern segments match precisely one path segment.

If *recursive* is true, the pattern segment \"`**`\" will match any number of path segments.

If *include_hidden* is true, wildcards can match path segments that start with a dot (`.`).

A sequence of path separators may be supplied to the *seps* argument. If not given, `os.sep`{.interpreted-text role="data"} and `~os.altsep`{.interpreted-text role="data"} (if available) are used.

::: seealso
`pathlib.PurePath.full_match`{.interpreted-text role="meth"} and `pathlib.Path.glob`{.interpreted-text role="meth"} methods, which call this function to implement pattern matching and globbing.
:::

::: versionadded
3.13
:::
:::::

## Examples

Consider a directory containing the following files: `1.gif`{.interpreted-text role="file"}, `2.txt`{.interpreted-text role="file"}, `card.gif`{.interpreted-text role="file"} and a subdirectory `sub`{.interpreted-text role="file"} which contains only the file `3.txt`{.interpreted-text role="file"}. `glob`{.interpreted-text role="func"} will produce the following results. Notice how any leading components of the path are preserved. :

    >>> import glob
    >>> glob.glob('./[0-9].*')
    ['./1.gif', './2.txt']
    >>> glob.glob('*.gif')
    ['1.gif', 'card.gif']
    >>> glob.glob('?.gif')
    ['1.gif']
    >>> glob.glob('**/*.txt', recursive=True)
    ['2.txt', 'sub/3.txt']
    >>> glob.glob('./**/', recursive=True)
    ['./', './sub/']

If the directory contains files starting with `.` they won\'t be matched by default. For example, consider a directory containing `card.gif`{.interpreted-text role="file"} and `.card.gif`{.interpreted-text role="file"}:

    >>> import glob
    >>> glob.glob('*.gif')
    ['card.gif']
    >>> glob.glob('.c*')
    ['.card.gif']

::: seealso
The `fnmatch`{.interpreted-text role="mod"} module offers shell-style filename (not path) expansion.
:::

::: seealso
The `pathlib`{.interpreted-text role="mod"} module offers high-level path objects.
:::
