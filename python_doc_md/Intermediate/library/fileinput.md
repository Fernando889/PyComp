# `!fileinput`{.interpreted-text role="mod"} \-\-- Iterate over lines from multiple input streams

::: {.module synopsis="Loop over standard input or a list of files."}
fileinput
:::

**Source code:** `Lib/fileinput.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

This module implements a helper class and functions to quickly write a loop over standard input or a list of files. If you just want to read or write one file see `open`{.interpreted-text role="func"}.

The typical use is:

    import fileinput
    for line in fileinput.input(encoding="utf-8"):
        process(line)

This iterates over the lines of all files listed in `sys.argv[1:]`, defaulting to `sys.stdin` if the list is empty. If a filename is `'-'`, it is also replaced by `sys.stdin` and the optional arguments *mode* and *openhook* are ignored. To specify an alternative list of filenames, pass it as the first argument to `.input`{.interpreted-text role="func"}. A single file name is also allowed.

All files are opened in text mode by default, but you can override this by specifying the *mode* parameter in the call to `.input`{.interpreted-text role="func"} or `FileInput`{.interpreted-text role="class"}. If an I/O error occurs during opening or reading a file, `OSError`{.interpreted-text role="exc"} is raised.

::: versionchanged
3.3 `IOError`{.interpreted-text role="exc"} used to be raised; it is now an alias of `OSError`{.interpreted-text role="exc"}.
:::

If `sys.stdin` is used more than once, the second and further use will return no lines, except perhaps for interactive use, or if it has been explicitly reset (e.g. using `sys.stdin.seek(0)`).

Empty files are opened and immediately closed; the only time their presence in the list of filenames is noticeable at all is when the last file opened is empty.

Lines are returned with any newlines intact, which means that the last line in a file may not have one.

You can control how files are opened by providing an opening hook via the *openhook* parameter to `fileinput.input`{.interpreted-text role="func"} or `FileInput`{.interpreted-text role="func"}. The hook must be a function that takes two arguments, *filename* and *mode*, and returns an accordingly opened file-like object. If *encoding* and/or *errors* are specified, they will be passed to the hook as additional keyword arguments. This module provides a `hook_compressed`{.interpreted-text role="func"} to support compressed files.

The following function is the primary interface of this module:

:::::: function
input(files=None, inplace=False, backup=\'\', \*, mode=\'r\', openhook=None, encoding=None, errors=None)

Create an instance of the `FileInput`{.interpreted-text role="class"} class. The instance will be used as global state for the functions of this module, and is also returned to use during iteration. The parameters to this function will be passed along to the constructor of the `FileInput`{.interpreted-text role="class"} class.

The `FileInput`{.interpreted-text role="class"} instance can be used as a context manager in the `with`{.interpreted-text role="keyword"} statement. In this example, *input* is closed after the `!with`{.interpreted-text role="keyword"} statement is exited, even if an exception occurs:

    with fileinput.input(files=('spam.txt', 'eggs.txt'), encoding="utf-8") as f:
        for line in f:
            process(line)

::: versionchanged
3.2 Can be used as a context manager.
:::

::: versionchanged
3.8 The keyword parameters *mode* and *openhook* are now keyword-only.
:::

::: versionchanged
3.10 The keyword-only parameter *encoding* and *errors* are added.
:::
::::::

The following functions use the global state created by `fileinput.input`{.interpreted-text role="func"}; if there is no active state, `RuntimeError`{.interpreted-text role="exc"} is raised.

::: function
filename()

Return the name of the file currently being read. Before the first line has been read, returns `None`.
:::

::: function
fileno()

Return the integer \"file descriptor\" for the current file. When no file is opened (before the first line and between files), returns `-1`.
:::

::: function
lineno()

Return the cumulative line number of the line that has just been read. Before the first line has been read, returns `0`. After the last line of the last file has been read, returns the line number of that line.
:::

::: function
filelineno()

Return the line number in the current file. Before the first line has been read, returns `0`. After the last line of the last file has been read, returns the line number of that line within the file.
:::

::: function
isfirstline()

Return `True` if the line just read is the first line of its file, otherwise return `False`.
:::

::: function
isstdin()

Return `True` if the last line was read from `sys.stdin`, otherwise return `False`.
:::

::: function
nextfile()

Close the current file so that the next iteration will read the first line from the next file (if any); lines not read from the file will not count towards the cumulative line count. The filename is not changed until after the first line of the next file has been read. Before the first line has been read, this function has no effect; it cannot be used to skip the first file. After the last line of the last file has been read, this function has no effect.
:::

::: function
close()

Close the sequence.
:::

The class which implements the sequence behavior provided by the module is available for subclassing as well:

::::::: {.FileInput(files=None, .inplace=False, .backup='', .*, .mode='r', .openhook=None, .encoding=None, .errors=None)}
Class `FileInput`{.interpreted-text role="class"} is the implementation; its methods `filename`{.interpreted-text role="meth"}, `fileno`{.interpreted-text role="meth"}, `lineno`{.interpreted-text role="meth"}, `filelineno`{.interpreted-text role="meth"}, `isfirstline`{.interpreted-text role="meth"}, `isstdin`{.interpreted-text role="meth"}, `nextfile`{.interpreted-text role="meth"} and `close`{.interpreted-text role="meth"} correspond to the functions of the same name in the module. In addition it is `iterable`{.interpreted-text role="term"} and has a `~io.TextIOBase.readline`{.interpreted-text role="meth"} method which returns the next input line. The sequence must be accessed in strictly sequential order; random access and `~io.TextIOBase.readline`{.interpreted-text role="meth"} cannot be mixed.

With *mode* you can specify which file mode will be passed to `open`{.interpreted-text role="func"}. It must be one of `'r'` and `'rb'`.

The *openhook*, when given, must be a function that takes two arguments, *filename* and *mode*, and returns an accordingly opened file-like object. You cannot use *inplace* and *openhook* together.

You can specify *encoding* and *errors* that is passed to `open`{.interpreted-text role="func"} or *openhook*.

A `FileInput`{.interpreted-text role="class"} instance can be used as a context manager in the `with`{.interpreted-text role="keyword"} statement. In this example, *input* is closed after the `!with`{.interpreted-text role="keyword"} statement is exited, even if an exception occurs:

    with FileInput(files=('spam.txt', 'eggs.txt')) as input:
        process(input)

::: versionchanged
3.2 Can be used as a context manager.
:::

::: versionchanged
3.8 The keyword parameter *mode* and *openhook* are now keyword-only.
:::

::: versionchanged
3.10 The keyword-only parameter *encoding* and *errors* are added.
:::

::: versionchanged
3.11 The `'rU'` and `'U'` modes and the `!__getitem__`{.interpreted-text role="meth"} method have been removed.
:::
:::::::

**Optional in-place filtering:** if the keyword argument `inplace=True` is passed to `fileinput.input`{.interpreted-text role="func"} or to the `FileInput`{.interpreted-text role="class"} constructor, the file is moved to a backup file and standard output is directed to the input file (if a file of the same name as the backup file already exists, it will be replaced silently). This makes it possible to write a filter that rewrites its input file in place. If the *backup* parameter is given (typically as `backup='.<some extension>'`), it specifies the extension for the backup file, and the backup file remains around; by default, the extension is `'.bak'` and it is deleted when the output file is closed. In-place filtering is disabled when standard input is read.

The two following opening hooks are provided by this module:

:::: function
hook_compressed(filename, mode, \*, encoding=None, errors=None)

Transparently opens files compressed with gzip and bzip2 (recognized by the extensions `'.gz'` and `'.bz2'`) using the `gzip`{.interpreted-text role="mod"} and `bz2`{.interpreted-text role="mod"} modules. If the filename extension is not `'.gz'` or `'.bz2'`, the file is opened normally (ie, using `open`{.interpreted-text role="func"} without any decompression).

The *encoding* and *errors* values are passed to `io.TextIOWrapper`{.interpreted-text role="class"} for compressed files and open for normal files.

Usage example: `fi = fileinput.FileInput(openhook=fileinput.hook_compressed, encoding="utf-8")`

::: versionchanged
3.10 The keyword-only parameter *encoding* and *errors* are added.
:::
::::

::::: function
hook_encoded(encoding, errors=None)

Returns a hook which opens each file with `open`{.interpreted-text role="func"}, using the given *encoding* and *errors* to read the file.

Usage example: `fi = fileinput.FileInput(openhook=fileinput.hook_encoded("utf-8", "surrogateescape"))`

::: versionchanged
3.6 Added the optional *errors* parameter.
:::

::: deprecated
3.10 This function is deprecated since `fileinput.input`{.interpreted-text role="func"} and `FileInput`{.interpreted-text role="class"} now have *encoding* and *errors* parameters.
:::
:::::
