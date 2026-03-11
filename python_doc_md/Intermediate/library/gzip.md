# `!gzip`{.interpreted-text role="mod"} \-\-- Support for `gzip`{.interpreted-text role="program"} files

::: {.module synopsis="Interfaces for gzip compression and decompression using file objects."}
gzip
:::

**Source code:** `Lib/gzip.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

This module provides a simple interface to compress and decompress files just like the GNU programs `gzip`{.interpreted-text role="program"} and `gunzip`{.interpreted-text role="program"} would.

This is an `optional module`{.interpreted-text role="term"}. If it is missing from your copy of CPython, look for documentation from your distributor (that is, whoever provided Python to you). If you are the distributor, see `optional-module-requirements`{.interpreted-text role="ref"}.

The data compression is provided by the `zlib`{.interpreted-text role="mod"} module.

The `!gzip`{.interpreted-text role="mod"} module provides the `GzipFile`{.interpreted-text role="class"} class, as well as the `.open`{.interpreted-text role="func"}, `compress`{.interpreted-text role="func"} and `decompress`{.interpreted-text role="func"} convenience functions. The `GzipFile`{.interpreted-text role="class"} class reads and writes `gzip`{.interpreted-text role="program"}-format files, automatically compressing or decompressing the data so that it looks like an ordinary `file object`{.interpreted-text role="term"}.

Note that additional file formats which can be decompressed by the `gzip`{.interpreted-text role="program"} and `gunzip`{.interpreted-text role="program"} programs, such as those produced by `compress`{.interpreted-text role="program"} and `pack`{.interpreted-text role="program"}, are not supported by this module.

The module defines the following items:

::::::: function
open(filename, mode=\'rb\', compresslevel=6, encoding=None, errors=None, newline=None)

Open a gzip-compressed file in binary or text mode, returning a `file
object`{.interpreted-text role="term"}.

The *filename* argument can be an actual filename (a `str`{.interpreted-text role="class"} or `bytes`{.interpreted-text role="class"} object), or an existing file object to read from or write to.

The *mode* argument can be any of `'r'`, `'rb'`, `'a'`, `'ab'`, `'w'`, `'wb'`, `'x'` or `'xb'` for binary mode, or `'rt'`, `'at'`, `'wt'`, or `'xt'` for text mode. The default is `'rb'`.

The *compresslevel* argument is an integer from 0 to 9, as for the `GzipFile`{.interpreted-text role="class"} constructor.

For binary mode, this function is equivalent to the `GzipFile`{.interpreted-text role="class"} constructor: `GzipFile(filename, mode, compresslevel)`. In this case, the *encoding*, *errors* and *newline* arguments must not be provided.

For text mode, a `GzipFile`{.interpreted-text role="class"} object is created, and wrapped in an `io.TextIOWrapper`{.interpreted-text role="class"} instance with the specified encoding, error handling behavior, and line ending(s).

::: versionchanged
3.3 Added support for *filename* being a file object, support for text mode, and the *encoding*, *errors* and *newline* arguments.
:::

::: versionchanged
3.4 Added support for the `'x'`, `'xb'` and `'xt'` modes.
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"}.
:::

::: versionchanged
3.15 The default compression level was reduced to 6 (down from 9). It is the default level used by most compression tools and a better tradeoff between speed and performance.
:::
:::::::

:::: exception
BadGzipFile

An exception raised for invalid gzip files. It inherits from `OSError`{.interpreted-text role="exc"}. `EOFError`{.interpreted-text role="exc"} and `zlib.error`{.interpreted-text role="exc"} can also be raised for invalid gzip files.

::: versionadded
3.8
:::
::::

:::::::::::::::::::: {.GzipFile(filename=None, .mode=None, .compresslevel=6, .fileobj=None, .mtime=None)}
Constructor for the `GzipFile`{.interpreted-text role="class"} class, which simulates most of the methods of a `file object`{.interpreted-text role="term"}, with the exception of the `~io.IOBase.truncate`{.interpreted-text role="meth"} method. At least one of *fileobj* and *filename* must be given a non-trivial value.

The new class instance is based on *fileobj*, which can be a regular file, an `io.BytesIO`{.interpreted-text role="class"} object, or any other object which simulates a file. It defaults to `None`, in which case *filename* is opened to provide a file object.

When *fileobj* is not `None`, the *filename* argument is only used to be included in the `gzip`{.interpreted-text role="program"} file header, which may include the original filename of the uncompressed file. It defaults to the filename of *fileobj*, if discernible; otherwise, it defaults to the empty string, and in this case the original filename is not included in the header.

The *mode* argument can be any of `'r'`, `'rb'`, `'a'`, `'ab'`, `'w'`, `'wb'`, `'x'`, or `'xb'`, depending on whether the file will be read or written. The default is the mode of *fileobj* if discernible; otherwise, the default is `'rb'`. In future Python releases the mode of *fileobj* will not be used. It is better to always specify *mode* for writing.

Note that the file is always opened in binary mode. To open a compressed file in text mode, use `.open`{.interpreted-text role="func"} (or wrap your `GzipFile`{.interpreted-text role="class"} with an `io.TextIOWrapper`{.interpreted-text role="class"}).

The *compresslevel* argument is an integer from `0` to `9` controlling the level of compression; `1` is fastest and produces the least compression, and `9` is slowest and produces the most compression. `0` is no compression. The default is `9`.

The optional *mtime* argument is the timestamp requested by gzip. The time is in Unix format, i.e., seconds since 00:00:00 UTC, January 1, 1970. If *mtime* is omitted or `None`, the current time is used. Use *mtime* = 0 to generate a compressed stream that does not depend on creation time.

See below for the `mtime`{.interpreted-text role="attr"} attribute that is set when decompressing.

Calling a `GzipFile`{.interpreted-text role="class"} object\'s `!close`{.interpreted-text role="meth"} method does not close *fileobj*, since you might wish to append more material after the compressed data. This also allows you to pass an `io.BytesIO`{.interpreted-text role="class"} object opened for writing as *fileobj*, and retrieve the resulting memory buffer using the `io.BytesIO`{.interpreted-text role="class"} object\'s `~io.BytesIO.getvalue`{.interpreted-text role="meth"} method.

`GzipFile`{.interpreted-text role="class"} supports the `io.BufferedIOBase`{.interpreted-text role="class"} interface, including iteration and the `with`{.interpreted-text role="keyword"} statement. Only the `~io.IOBase.truncate`{.interpreted-text role="meth"} method isn\'t implemented.

`GzipFile`{.interpreted-text role="class"} also provides the following method and attribute:

:::::: method
peek(n)

Read *n* uncompressed bytes without advancing the file position. The number of bytes returned may be more or less than requested.

:::: note
::: title
Note
:::

While calling `peek`{.interpreted-text role="meth"} does not change the file position of the `GzipFile`{.interpreted-text role="class"}, it may change the position of the underlying file object (e.g. if the `GzipFile`{.interpreted-text role="class"} was constructed with the *fileobj* parameter).
::::

::: versionadded
3.2
:::
::::::

:::: attribute
mode

`'rb'` for reading and `'wb'` for writing.

::: versionchanged
3.13 In previous versions it was an integer `1` or `2`.
:::
::::

::: attribute
mtime

When decompressing, this attribute is set to the last timestamp in the most recently read header. It is an integer, holding the number of seconds since the Unix epoch (00:00:00 UTC, January 1, 1970). The initial value before reading any headers is `None`.
:::

::: attribute
name

The path to the gzip file on disk, as a `str`{.interpreted-text role="class"} or `bytes`{.interpreted-text role="class"}. Equivalent to the output of `os.fspath`{.interpreted-text role="func"} on the original input path, with no other normalization, resolution or expansion.
:::

::: versionchanged
3.1 Support for the `with`{.interpreted-text role="keyword"} statement was added, along with the *mtime* constructor argument and `mtime`{.interpreted-text role="attr"} attribute.
:::

::: versionchanged
3.2 Support for zero-padded and unseekable files was added.
:::

::: versionchanged
3.3 The `io.BufferedIOBase.read1`{.interpreted-text role="meth"} method is now implemented.
:::

::: versionchanged
3.4 Added support for the `'x'` and `'xb'` modes.
:::

::: versionchanged
3.5 Added support for writing arbitrary `bytes-like objects <bytes-like object>`{.interpreted-text role="term"}. The `~io.BufferedIOBase.read`{.interpreted-text role="meth"} method now accepts an argument of `None`.
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"}.
:::

::: deprecated
3.9 Opening `GzipFile`{.interpreted-text role="class"} for writing without specifying the *mode* argument is deprecated.
:::

::: versionchanged
3.12 Remove the `filename` attribute, use the `~GzipFile.name`{.interpreted-text role="attr"} attribute instead.
:::

::: versionchanged
3.15 The default compression level was reduced to 6 (down from 9). It is the default level used by most compression tools and a better tradeoff between speed and performance.
:::
::::::::::::::::::::

::::::::: function
compress(data, compresslevel=6, \*, mtime=0)

Compress the *data*, returning a `bytes`{.interpreted-text role="class"} object containing the compressed data. *compresslevel* and *mtime* have the same meaning as in the `GzipFile`{.interpreted-text role="class"} constructor above, but *mtime* defaults to 0 for reproducible output.

::: versionadded
3.2
:::

::: versionchanged
3.8 Added the *mtime* parameter for reproducible output.
:::

::: versionchanged
3.11 Speed is improved by compressing all data at once instead of in a streamed fashion. Calls with *mtime* set to `0` are delegated to `zlib.compress`{.interpreted-text role="func"} for better speed. In this situation the output may contain a gzip header \"OS\" byte value other than 255 \"unknown\" as supplied by the underlying zlib implementation.
:::

::: versionchanged
3.13 The gzip header OS byte is guaranteed to be set to 255 when this function is used as was the case in 3.10 and earlier.
:::

::: versionchanged
3.14 The *mtime* parameter now defaults to 0 for reproducible output. For the previous behaviour of using the current time, pass `None` to *mtime*.
:::

::: versionchanged
3.15 The default compression level was reduced to 6 (down from 9). It is the default level used by most compression tools and a better tradeoff between speed and performance.
:::
:::::::::

::::: function
decompress(data)

Decompress the *data*, returning a `bytes`{.interpreted-text role="class"} object containing the uncompressed data. This function is capable of decompressing multi-member gzip data (multiple gzip blocks concatenated together). When the data is certain to contain only one member the `zlib.decompress`{.interpreted-text role="func"} function with *wbits* set to 31 is faster.

::: versionadded
3.2
:::

::: versionchanged
3.11 Speed is improved by decompressing members at once in memory instead of in a streamed fashion.
:::
:::::

## Examples of usage {#gzip-usage-examples}

Example of how to read a compressed file:

    import gzip
    with gzip.open('/home/joe/file.txt.gz', 'rb') as f:
        file_content = f.read()

Example of how to create a compressed GZIP file:

    import gzip
    content = b"Lots of content here"
    with gzip.open('/home/joe/file.txt.gz', 'wb') as f:
        f.write(content)

Example of how to GZIP compress an existing file:

    import gzip
    import shutil
    with open('/home/joe/file.txt', 'rb') as f_in:
        with gzip.open('/home/joe/file.txt.gz', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

Example of how to GZIP compress a binary string:

    import gzip
    s_in = b"Lots of content here"
    s_out = gzip.compress(s_in)

::: seealso

Module `zlib`{.interpreted-text role="mod"}

:   The basic data compression module needed to support the `gzip`{.interpreted-text role="program"} file format.

In case gzip (de)compression is a bottleneck, the [python-isal](https://github.com/pycompression/python-isal) package speeds up (de)compression with a mostly compatible API.
:::

::: program
gzip
:::

## Command-line interface {#gzip-cli}

The `!gzip`{.interpreted-text role="mod"} module provides a simple command line interface to compress or decompress files.

Once executed the `!gzip`{.interpreted-text role="mod"} module keeps the input file(s).

::: versionchanged
3.8

Add a new command line interface with a usage. By default, when you will execute the CLI, the default compression level is 6.
:::

### Command-line options

::: option
file

If *file* is not specified, read from `sys.stdin`{.interpreted-text role="data"}.
:::

::: option

`--fast`

:   

Indicates the fastest compression method (less compression).
:::

::: option

`--best`

:   

Indicates the slowest compression method (best compression).
:::

::: option

`-d, --decompress`

:   

Decompress the given file.
:::

::: option

`-h, --help`

:   

Show the help message.
:::
