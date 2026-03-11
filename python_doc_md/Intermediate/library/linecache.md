# `!linecache`{.interpreted-text role="mod"} \-\-- Random access to text lines

::: {.module synopsis="Provides random access to individual lines from text files."}
linecache
:::

**Source code:** `Lib/linecache.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

The `!linecache`{.interpreted-text role="mod"} module allows one to get any line from a Python source file, while attempting to optimize internally, using a cache, the common case where many lines are read from a single file. This is used by the `traceback`{.interpreted-text role="mod"} module to retrieve source lines for inclusion in the formatted traceback.

The `tokenize.open`{.interpreted-text role="func"} function is used to open files. This function uses `tokenize.detect_encoding`{.interpreted-text role="func"} to get the encoding of the file; in the absence of an encoding token, the file encoding defaults to UTF-8.

The `!linecache`{.interpreted-text role="mod"} module defines the following functions:

::::: function
getline(filename, lineno, module_globals=None)

Get line *lineno* from file named *filename*. This function will never raise an exception \-\-- it will return `''` on errors (the terminating newline character will be included for lines that are found).

::: index
triple: module; search; path
:::

If *filename* indicates a frozen module (starting with `'<frozen '`), the function will attempt to get the real file name from `module_globals['__file__']` if *module_globals* is not `None`.

If a file named *filename* is not found, the function first checks for a `302`{.interpreted-text role="pep"} `__loader__` in *module_globals*. If there is such a loader and it defines a `get_source` method, then that determines the source lines (if `get_source()` returns `None`, then `''` is returned). Finally, if *filename* is a relative filename, it is looked up relative to the entries in the module search path, `sys.path`.

::: versionchanged
3.14

Support *filename* of frozen modules.
:::
:::::

::: function
clearcache()

Clear the cache. Use this function if you no longer need lines from files previously read using `getline`{.interpreted-text role="func"}.
:::

::: function
checkcache(filename=None)

Check the cache for validity. Use this function if files in the cache may have changed on disk, and you require the updated version. If *filename* is omitted, it will check all the entries in the cache.
:::

:::: function
lazycache(filename, module_globals)

Capture enough detail about a non-file-based module to permit getting its lines later via `getline`{.interpreted-text role="func"} even if *module_globals* is `None` in the later call. This avoids doing I/O until a line is actually needed, without having to carry the module globals around indefinitely.

::: versionadded
3.5
:::
::::

Example:

    >>> import linecache
    >>> linecache.getline(linecache.__file__, 8)
    'import sys\n'
