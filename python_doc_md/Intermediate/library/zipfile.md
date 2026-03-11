# `!zipfile`{.interpreted-text role="mod"} \-\-- Work with ZIP archives

::: {.module synopsis="Read and write ZIP-format archive files."}
zipfile
:::

**Source code:** `Lib/zipfile/`{.interpreted-text role="source"}

------------------------------------------------------------------------

The ZIP file format is a common archive and compression standard. This module provides tools to create, read, write, append, and list a ZIP file. Any advanced use of this module will require an understanding of the format, as defined in [PKZIP Application Note](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT).

This module does not handle multipart ZIP files. It can handle ZIP files that use the ZIP64 extensions (that is ZIP files that are more than 4 GiB in size). It supports decryption of encrypted files in ZIP archives, but it cannot create an encrypted file. Decryption is extremely slow as it is implemented in native Python rather than C.

Handling compressed archives requires `optional modules <optional module>`{.interpreted-text role="term"} such as `zlib`{.interpreted-text role="mod"}, `bz2`{.interpreted-text role="mod"}, `lzma`{.interpreted-text role="mod"}, and `compression.zstd`{.interpreted-text role="mod"}. If any of them are missing from your copy of CPython, look for documentation from your distributor (that is, whoever provided Python to you). If you are the distributor, see `optional-module-requirements`{.interpreted-text role="ref"}.

The module defines the following items:

:::: exception
BadZipFile

The error raised for bad ZIP files.

::: versionadded
3.2
:::
::::

:::: exception
BadZipfile

Alias of `BadZipFile`{.interpreted-text role="exc"}, for compatibility with older Python versions.

::: deprecated
3.2
:::
::::

::: exception
LargeZipFile

The error raised when a ZIP file would require ZIP64 functionality but that has not been enabled.
:::

::: {.ZipFile noindex=""}
The class for reading and writing ZIP files. See section `zipfile-objects`{.interpreted-text role="ref"} for constructor details.
:::

:::: {.Path noindex=""}
Class that implements a subset of the interface provided by `pathlib.Path`{.interpreted-text role="class"}, including the full `importlib.resources.abc.Traversable`{.interpreted-text role="class"} interface.

::: versionadded
3.8
:::
::::

::: {.PyZipFile noindex=""}
Class for creating ZIP archives containing Python libraries.
:::

:::::: {.ZipInfo(filename='NoName', .date_time=(1980,1,1,0,0,0))}
Class used to represent information about a member of an archive. Instances of this class are returned by the `.getinfo`{.interpreted-text role="meth"} and `.infolist`{.interpreted-text role="meth"} methods of `ZipFile`{.interpreted-text role="class"} objects. Most users of the `!zipfile`{.interpreted-text role="mod"} module will not need to create these, but only use those created by this module. *filename* should be the full name of the archive member, and *date_time* should be a tuple containing six fields which describe the time of the last modification to the file; the fields are described in section `zipinfo-objects`{.interpreted-text role="ref"}.

::: versionchanged
3.13 A public `!compress_level`{.interpreted-text role="attr"} attribute has been added to expose the formerly protected `!_compresslevel`{.interpreted-text role="attr"}. The older protected name continues to work as a property for backwards compatibility.
:::

:::: method
[for_archive]{#for_archive}(archive)

Resolve the date_time, compression attributes, and external attributes to suitable defaults as used by `ZipFile.writestr`{.interpreted-text role="meth"}.

Returns self for chaining.

::: versionadded
3.14
:::
::::
::::::

:::: function
is_zipfile(filename)

Returns `True` if *filename* is a valid ZIP file based on its magic number, otherwise returns `False`. *filename* may be a file or file-like object too.

::: versionchanged
3.1 Support for file and file-like objects.
:::
::::

::: data
ZIP_STORED

The numeric constant for an uncompressed archive member.
:::

::: data
ZIP_DEFLATED

The numeric constant for the usual ZIP compression method. This requires the `zlib`{.interpreted-text role="mod"} module.
:::

:::: data
ZIP_BZIP2

The numeric constant for the BZIP2 compression method. This requires the `bz2`{.interpreted-text role="mod"} module.

::: versionadded
3.3
:::
::::

:::: data
ZIP_LZMA

The numeric constant for the LZMA compression method. This requires the `lzma`{.interpreted-text role="mod"} module.

::: versionadded
3.3
:::
::::

:::::: data
ZIP_ZSTANDARD

The numeric constant for Zstandard compression. This requires the `compression.zstd`{.interpreted-text role="mod"} module.

:::: note
::: title
Note
:::

In APPNOTE 6.3.7, the method ID `20` was assigned to Zstandard compression. This was changed in APPNOTE 6.3.8 to method ID `93` to avoid conflicts, with method ID `20` being deprecated. For compatibility, the `!zipfile`{.interpreted-text role="mod"} module reads both method IDs but will only write data with method ID `93`.
::::

::: versionadded
3.14
:::
::::::

:::: note
::: title
Note
:::

The ZIP file format specification has included support for bzip2 compression since 2001, for LZMA compression since 2006, and Zstandard compression since 2020. However, some tools (including older Python releases) do not support these compression methods, and may either refuse to process the ZIP file altogether, or fail to extract individual files.
::::

::: seealso

[PKZIP Application Note](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)

:   Documentation on the ZIP file format by Phil Katz, the creator of the format and algorithms used.

[Info-ZIP Home Page](https://infozip.sourceforge.net/)

:   Information about the Info-ZIP project\'s ZIP archive programs and development libraries.
:::

## ZipFile objects

:::::::::::::: {.ZipFile(file, .mode='r', .compression=ZIP_STORED, .allowZip64=True, .\\ .compresslevel=None, .*, .strict_timestamps=True, .\\ .metadata_encoding=None)}
Open a ZIP file, where *file* can be a path to a file (a string), a file-like object or a `path-like object`{.interpreted-text role="term"}.

The *mode* parameter should be `'r'` to read an existing file, `'w'` to truncate and write a new file, `'a'` to append to an existing file, or `'x'` to exclusively create and write a new file. If *mode* is `'x'` and *file* refers to an existing file, a `FileExistsError`{.interpreted-text role="exc"} will be raised. If *mode* is `'a'` and *file* refers to an existing ZIP file, then additional files are added to it. If *file* does not refer to a ZIP file, then a new ZIP archive is appended to the file. This is meant for adding a ZIP archive to another file (such as `python.exe`{.interpreted-text role="file"}). If *mode* is `'a'` and the file does not exist at all, it is created. If *mode* is `'r'` or `'a'`, the file should be seekable.

*compression* is the ZIP compression method to use when writing the archive, and should be `ZIP_STORED`{.interpreted-text role="const"}, `ZIP_DEFLATED`{.interpreted-text role="const"}, `ZIP_BZIP2`{.interpreted-text role="const"}, `ZIP_LZMA`{.interpreted-text role="const"}, or `ZIP_ZSTANDARD`{.interpreted-text role="const"}; unrecognized values will cause `NotImplementedError`{.interpreted-text role="exc"} to be raised. If `ZIP_DEFLATED`{.interpreted-text role="const"}, `ZIP_BZIP2`{.interpreted-text role="const"}, `ZIP_LZMA`{.interpreted-text role="const"}, or `ZIP_ZSTANDARD`{.interpreted-text role="const"} is specified but the corresponding module (`zlib`{.interpreted-text role="mod"}, `bz2`{.interpreted-text role="mod"}, `lzma`{.interpreted-text role="mod"}, or `compression.zstd`{.interpreted-text role="mod"}) is not available, `RuntimeError`{.interpreted-text role="exc"} is raised. The default is `ZIP_STORED`{.interpreted-text role="const"}.

If *allowZip64* is `True` (the default) zipfile will create ZIP files that use the ZIP64 extensions when the zipfile is larger than 4 GiB. If it is `false` `!zipfile`{.interpreted-text role="mod"} will raise an exception when the ZIP file would require ZIP64 extensions.

The *compresslevel* parameter controls the compression level to use when writing files to the archive. When using `ZIP_STORED`{.interpreted-text role="const"} or `ZIP_LZMA`{.interpreted-text role="const"} it has no effect. When using `ZIP_DEFLATED`{.interpreted-text role="const"} integers `0` through `9` are accepted (see `zlib <zlib.compressobj>`{.interpreted-text role="class"} for more information). When using `ZIP_BZIP2`{.interpreted-text role="const"} integers `1` through `9` are accepted (see `bz2 <bz2.BZ2File>`{.interpreted-text role="class"} for more information). When using `ZIP_ZSTANDARD`{.interpreted-text role="const"} integers `-131072` through `22` are commonly accepted (see `CompressionParameter.compression_level <compression.zstd.CompressionParameter.compression_level>`{.interpreted-text role="attr"} for more on retrieving valid values and their meaning).

The *strict_timestamps* argument, when set to `False`, allows to zip files older than 1980-01-01 at the cost of setting the timestamp to 1980-01-01. Similar behavior occurs with files newer than 2107-12-31, the timestamp is also set to the limit.

When mode is `'r'`, *metadata_encoding* may be set to the name of a codec, which will be used to decode metadata such as the names of members and ZIP comments.

If the file is created with mode `'w'`, `'x'` or `'a'` and then `closed <close>`{.interpreted-text role="meth"} without adding any files to the archive, the appropriate ZIP structures for an empty archive will be written to the file.

ZipFile is also a context manager and therefore supports the `with`{.interpreted-text role="keyword"} statement. In the example, *myzip* is closed after the `!with`{.interpreted-text role="keyword"} statement\'s suite is finished\-\--even if an exception occurs:

    with ZipFile('spam.zip', 'w') as myzip:
        myzip.write('eggs.txt')

:::: note
::: title
Note
:::

*metadata_encoding* is an instance-wide setting for the ZipFile. It is not possible to set this on a per-member basis.

This attribute is a workaround for legacy implementations which produce archives with names in the current locale encoding or code page (mostly on Windows). According to the .ZIP standard, the encoding of metadata may be specified to be either IBM code page (default) or UTF-8 by a flag in the archive header. That flag takes precedence over *metadata_encoding*, which is a Python-specific extension.
::::

::: versionchanged
3.2 Added the ability to use `ZipFile`{.interpreted-text role="class"} as a context manager.
:::

::: versionchanged
3.3 Added support for `bzip2 <bz2>`{.interpreted-text role="mod"} and `lzma`{.interpreted-text role="mod"} compression.
:::

::: versionchanged
3.4 ZIP64 extensions are enabled by default.
:::

::: versionchanged
3.5 Added support for writing to unseekable streams. Added support for the `'x'` mode.
:::

::: versionchanged
3.6 Previously, a plain `RuntimeError`{.interpreted-text role="exc"} was raised for unrecognized compression values.
:::

::: versionchanged
3.6.2 The *file* parameter accepts a `path-like object`{.interpreted-text role="term"}.
:::

::: versionchanged
3.7 Add the *compresslevel* parameter.
:::

::: versionchanged
3.8 The *strict_timestamps* keyword-only parameter.
:::

::: versionchanged
3.11 Added support for specifying member name encoding for reading metadata in the zipfile\'s directory and file headers.
:::
::::::::::::::

::: method
ZipFile.close()

Close the archive file. You must call `close`{.interpreted-text role="meth"} before exiting your program or essential records will not be written.
:::

::: method
ZipFile.getinfo(name)

Return a `ZipInfo`{.interpreted-text role="class"} object with information about the archive member *name*. Calling `getinfo`{.interpreted-text role="meth"} for a name not currently contained in the archive will raise a `KeyError`{.interpreted-text role="exc"}.
:::

::: method
ZipFile.infolist()

Return a list containing a `ZipInfo`{.interpreted-text role="class"} object for each member of the archive. The objects are in the same order as their entries in the actual ZIP file on disk if an existing archive was opened.
:::

::: method
ZipFile.namelist()

Return a list of archive members by name.
:::

::::::::: method
ZipFile.open(name, mode=\'r\', pwd=None, \*, force_zip64=False)

Access a member of the archive as a binary file-like object. *name* can be either the name of a file within the archive or a `ZipInfo`{.interpreted-text role="class"} object. The *mode* parameter, if included, must be `'r'` (the default) or `'w'`. *pwd* is the password used to decrypt encrypted ZIP files as a `bytes`{.interpreted-text role="class"} object.

`~ZipFile.open`{.interpreted-text role="meth"} is also a context manager and therefore supports the `with`{.interpreted-text role="keyword"} statement:

    with ZipFile('spam.zip') as myzip:
        with myzip.open('eggs.txt') as myfile:
            print(myfile.read())

With *mode* `'r'` the file-like object (`ZipExtFile`) is read-only and provides the following methods: `~io.BufferedIOBase.read`{.interpreted-text role="meth"}, `~io.IOBase.readline`{.interpreted-text role="meth"}, `~io.IOBase.readlines`{.interpreted-text role="meth"}, `~io.IOBase.seek`{.interpreted-text role="meth"}, `~io.IOBase.tell`{.interpreted-text role="meth"}, `~container.__iter__`{.interpreted-text role="meth"}, `~iterator.__next__`{.interpreted-text role="meth"}. These objects can operate independently of the ZipFile.

With `mode='w'`, a writable file handle is returned, which supports the `~io.BufferedIOBase.write`{.interpreted-text role="meth"} method. While a writable file handle is open, attempting to read or write other files in the ZIP file will raise a `ValueError`{.interpreted-text role="exc"}.

In both cases the file-like object has also attributes `!name`{.interpreted-text role="attr"}, which is equivalent to the name of a file within the archive, and `!mode`{.interpreted-text role="attr"}, which is `'rb'` or `'wb'` depending on the input mode.

When writing a file, if the file size is not known in advance but may exceed 2 GiB, pass `force_zip64=True` to ensure that the header format is capable of supporting large files. If the file size is known in advance, construct a `ZipInfo`{.interpreted-text role="class"} object with `~ZipInfo.file_size`{.interpreted-text role="attr"} set, and use that as the *name* parameter.

:::: note
::: title
Note
:::

The `.open`{.interpreted-text role="meth"}, `read`{.interpreted-text role="meth"} and `extract`{.interpreted-text role="meth"} methods can take a filename or a `ZipInfo`{.interpreted-text role="class"} object. You will appreciate this when trying to read a ZIP file that contains members with duplicate names.
::::

::: versionchanged
3.6 Removed support of `mode='U'`. Use `io.TextIOWrapper`{.interpreted-text role="class"} for reading compressed text files in `universal newlines`{.interpreted-text role="term"} mode.
:::

::: versionchanged
3.6 `ZipFile.open`{.interpreted-text role="meth"} can now be used to write files into the archive with the `mode='w'` option.
:::

::: versionchanged
3.6 Calling `.open`{.interpreted-text role="meth"} on a closed ZipFile will raise a `ValueError`{.interpreted-text role="exc"}. Previously, a `RuntimeError`{.interpreted-text role="exc"} was raised.
:::

::: versionchanged
3.13 Added attributes `!name`{.interpreted-text role="attr"} and `!mode`{.interpreted-text role="attr"} for the writeable file-like object. The value of the `!mode`{.interpreted-text role="attr"} attribute for the readable file-like object was changed from `'r'` to `'rb'`.
:::
:::::::::

::::::: method
ZipFile.extract(member, path=None, pwd=None)

Extract a member from the archive to the current working directory; *member* must be its full name or a `ZipInfo`{.interpreted-text role="class"} object. Its file information is extracted as accurately as possible. *path* specifies a different directory to extract to. *member* can be a filename or a `ZipInfo`{.interpreted-text role="class"} object. *pwd* is the password used for encrypted files as a `bytes`{.interpreted-text role="class"} object.

Returns the normalized path created (a directory or new file).

:::: note
::: title
Note
:::

If a member filename is an absolute path, a drive/UNC sharepoint and leading (back)slashes will be stripped, e.g.: `///foo/bar` becomes `foo/bar` on Unix, and `C:\foo\bar` becomes `foo\bar` on Windows. And all `".."` components in a member filename will be removed, e.g.: `../../foo../../ba..r` becomes `foo../ba..r`. On Windows illegal characters (`:`, `<`, `>`, `|`, `"`, `?`, and `*`) replaced by underscore (`_`).
::::

::: versionchanged
3.6 Calling `extract`{.interpreted-text role="meth"} on a closed ZipFile will raise a `ValueError`{.interpreted-text role="exc"}. Previously, a `RuntimeError`{.interpreted-text role="exc"} was raised.
:::

::: versionchanged
3.6.2 The *path* parameter accepts a `path-like object`{.interpreted-text role="term"}.
:::
:::::::

::::::: method
ZipFile.extractall(path=None, members=None, pwd=None)

Extract all members from the archive to the current working directory. *path* specifies a different directory to extract to. *members* is optional and must be a subset of the list returned by `namelist`{.interpreted-text role="meth"}. *pwd* is the password used for encrypted files as a `bytes`{.interpreted-text role="class"} object.

:::: warning
::: title
Warning
:::

Never extract archives from untrusted sources without prior inspection. It is possible that files are created outside of *path*, e.g. members that have absolute filenames starting with `"/"` or filenames with two dots `".."`. This module attempts to prevent that. See `extract`{.interpreted-text role="meth"} note.
::::

::: versionchanged
3.6 Calling `extractall`{.interpreted-text role="meth"} on a closed ZipFile will raise a `ValueError`{.interpreted-text role="exc"}. Previously, a `RuntimeError`{.interpreted-text role="exc"} was raised.
:::

::: versionchanged
3.6.2 The *path* parameter accepts a `path-like object`{.interpreted-text role="term"}.
:::
:::::::

::: method
ZipFile.printdir()

Print a table of contents for the archive to `sys.stdout`.
:::

::: method
ZipFile.setpassword(pwd)

Set *pwd* (a `bytes`{.interpreted-text role="class"} object) as default password to extract encrypted files.
:::

:::: method
ZipFile.read(name, pwd=None)

Return the bytes of the file *name* in the archive. *name* is the name of the file in the archive, or a `ZipInfo`{.interpreted-text role="class"} object. The archive must be open for read or append. *pwd* is the password used for encrypted files as a `bytes`{.interpreted-text role="class"} object and, if specified, overrides the default password set with `setpassword`{.interpreted-text role="meth"}. Calling `read`{.interpreted-text role="meth"} on a ZipFile that uses a compression method other than `ZIP_STORED`{.interpreted-text role="const"}, `ZIP_DEFLATED`{.interpreted-text role="const"}, `ZIP_BZIP2`{.interpreted-text role="const"}, `ZIP_LZMA`{.interpreted-text role="const"}, or `ZIP_ZSTANDARD`{.interpreted-text role="const"} will raise a `NotImplementedError`{.interpreted-text role="exc"}. An error will also be raised if the corresponding compression module is not available.

::: versionchanged
3.6 Calling `read`{.interpreted-text role="meth"} on a closed ZipFile will raise a `ValueError`{.interpreted-text role="exc"}. Previously, a `RuntimeError`{.interpreted-text role="exc"} was raised.
:::
::::

:::: method
ZipFile.testzip()

Read all the files in the archive and check their CRC\'s and file headers. Return the name of the first bad file, or else return `None`.

::: versionchanged
3.6 Calling `testzip`{.interpreted-text role="meth"} on a closed ZipFile will raise a `ValueError`{.interpreted-text role="exc"}. Previously, a `RuntimeError`{.interpreted-text role="exc"} was raised.
:::
::::

:::::::::::: method
ZipFile.write(filename, arcname=None, compress_type=None, compresslevel=None)

Write the file named *filename* to the archive, giving it the archive name *arcname* (by default, this will be the same as *filename*, but without a drive letter and with leading path separators removed). If given, *compress_type* overrides the value given for the *compression* parameter to the constructor for the new entry. Similarly, *compresslevel* will override the constructor if given. The archive must be open with mode `'w'`, `'x'` or `'a'`.

:::: note
::: title
Note
:::

The ZIP file standard historically did not specify a metadata encoding, but strongly recommended CP437 (the original IBM PC encoding) for interoperability. Recent versions allow use of UTF-8 (only). In this module, UTF-8 will automatically be used to write the member names if they contain any non-ASCII characters. It is not possible to write member names in any encoding other than ASCII or UTF-8.
::::

:::: note
::: title
Note
:::

Archive names should be relative to the archive root, that is, they should not start with a path separator.
::::

:::: note
::: title
Note
:::

If `arcname` (or `filename`, if `arcname` is not given) contains a null byte, the name of the file in the archive will be truncated at the null byte.
::::

:::: note
::: title
Note
:::

A leading slash in the filename may lead to the archive being impossible to open in some zip programs on Windows systems.
::::

::: versionchanged
3.6 Calling `write`{.interpreted-text role="meth"} on a ZipFile created with mode `'r'` or a closed ZipFile will raise a `ValueError`{.interpreted-text role="exc"}. Previously, a `RuntimeError`{.interpreted-text role="exc"} was raised.
:::
::::::::::::

::::::: method
ZipFile.writestr(zinfo_or_arcname, data, compress_type=None, compresslevel=None)

Write a file into the archive. The contents is *data*, which may be either a `str`{.interpreted-text role="class"} or a `bytes`{.interpreted-text role="class"} instance; if it is a `str`{.interpreted-text role="class"}, it is encoded as UTF-8 first. *zinfo_or_arcname* is either the file name it will be given in the archive, or a `ZipInfo`{.interpreted-text role="class"} instance. If it\'s an instance, at least the filename, date, and time must be given. If it\'s a name, the date and time is set to the current date and time. The archive must be opened with mode `'w'`, `'x'` or `'a'`.

If given, *compress_type* overrides the value given for the *compression* parameter to the constructor for the new entry, or in the *zinfo_or_arcname* (if that is a `ZipInfo`{.interpreted-text role="class"} instance). Similarly, *compresslevel* will override the constructor if given.

:::: note
::: title
Note
:::

When passing a `ZipInfo`{.interpreted-text role="class"} instance as the *zinfo_or_arcname* parameter, the compression method used will be that specified in the *compress_type* member of the given `ZipInfo`{.interpreted-text role="class"} instance. By default, the `ZipInfo`{.interpreted-text role="class"} constructor sets this member to `ZIP_STORED`{.interpreted-text role="const"}.
::::

::: versionchanged
3.2 The *compress_type* argument.
:::

::: versionchanged
3.6 Calling `writestr`{.interpreted-text role="meth"} on a ZipFile created with mode `'r'` or a closed ZipFile will raise a `ValueError`{.interpreted-text role="exc"}. Previously, a `RuntimeError`{.interpreted-text role="exc"} was raised.
:::
:::::::

:::: method
ZipFile.mkdir(zinfo_or_directory, mode=511)

Create a directory inside the archive. If *zinfo_or_directory* is a string, a directory is created inside the archive with the mode that is specified in the *mode* argument. If, however, *zinfo_or_directory* is a `ZipInfo`{.interpreted-text role="class"} instance then the *mode* argument is ignored.

The archive must be opened with mode `'w'`, `'x'` or `'a'`.

::: versionadded
3.11
:::
::::

The following data attributes are also available:

::: attribute
ZipFile.filename

Name of the ZIP file.
:::

::: attribute
ZipFile.debug

The level of debug output to use. This may be set from `0` (the default, no output) to `3` (the most output). Debugging information is written to `sys.stdout`.
:::

::: attribute
ZipFile.comment

The comment associated with the ZIP file as a `bytes`{.interpreted-text role="class"} object. If assigning a comment to a `ZipFile`{.interpreted-text role="class"} instance created with mode `'w'`, `'x'` or `'a'`, it should be no longer than 65535 bytes. Comments longer than this will be truncated.
:::

## Path objects

::::: {.Path(root, .at='')}
Construct a Path object from a `root` zipfile (which may be a `ZipFile`{.interpreted-text role="class"} instance or `file` suitable for passing to the `ZipFile`{.interpreted-text role="class"} constructor).

`at` specifies the location of this Path within the zipfile, e.g. \'dir/file.txt\', \'dir/\', or \'\'. Defaults to the empty string, indicating the root.

:::: note
::: title
Note
:::

The `Path`{.interpreted-text role="class"} class does not sanitize filenames within the ZIP archive. Unlike the `ZipFile.extract`{.interpreted-text role="meth"} and `ZipFile.extractall`{.interpreted-text role="meth"} methods, it is the caller\'s responsibility to validate or sanitize filenames to prevent path traversal vulnerabilities (e.g., filenames containing \"..\" or absolute paths). When handling untrusted archives, consider resolving filenames using `os.path.abspath`{.interpreted-text role="func"} and checking against the target directory with `os.path.commonpath`{.interpreted-text role="func"}.
::::
:::::

Path objects expose the following features of `pathlib.Path`{.interpreted-text role="mod"} objects:

Path objects are traversable using the `/` operator or `joinpath`.

::: attribute
Path.name

The final path component.
:::

::::: method
Path.open(mode=\'r\', *, pwd,*\*)

Invoke `ZipFile.open`{.interpreted-text role="meth"} on the current path. Allows opening for read or write, text or binary through supported modes: \'r\', \'w\', \'rb\', \'wb\'. Positional and keyword arguments are passed through to `io.TextIOWrapper`{.interpreted-text role="class"} when opened as text and ignored otherwise. `pwd` is the `pwd` parameter to `ZipFile.open`{.interpreted-text role="meth"}.

::: versionchanged
3.9 Added support for text and binary modes for open. Default mode is now text.
:::

::: versionchanged
3.11.2 The `encoding` parameter can be supplied as a positional argument without causing a `TypeError`{.interpreted-text role="exc"}. As it could in 3.9. Code needing to be compatible with unpatched 3.10 and 3.11 versions must pass all `io.TextIOWrapper`{.interpreted-text role="class"} arguments, `encoding` included, as keywords.
:::
:::::

::: method
Path.iterdir()

Enumerate the children of the current directory.
:::

::: method
Path.is_dir()

Return `True` if the current context references a directory.
:::

::: method
Path.is_file()

Return `True` if the current context references a file.
:::

::::: method
Path.is_symlink()

Return `True` if the current context references a symbolic link.

::: versionadded
3.12
:::

::: versionchanged
3.13 Previously, `is_symlink` would unconditionally return `False`.
:::
:::::

::: method
Path.exists()

Return `True` if the current context references a file or directory in the zip file.
:::

:::: data
Path.suffix

The last dot-separated portion of the final component, if any. This is commonly called the file extension.

::: versionadded
3.11 Added `Path.suffix`{.interpreted-text role="data"} property.
:::
::::

:::: data
Path.stem

The final path component, without its suffix.

::: versionadded
3.11 Added `Path.stem`{.interpreted-text role="data"} property.
:::
::::

:::: data
Path.suffixes

A list of the path's suffixes, commonly called file extensions.

::: versionadded
3.11 Added `Path.suffixes`{.interpreted-text role="data"} property.
:::
::::

:::: method
Path.read_text(*,*\*)

Read the current file as unicode text. Positional and keyword arguments are passed through to `io.TextIOWrapper`{.interpreted-text role="class"} (except `buffer`, which is implied by the context).

::: versionchanged
3.11.2 The `encoding` parameter can be supplied as a positional argument without causing a `TypeError`{.interpreted-text role="exc"}. As it could in 3.9. Code needing to be compatible with unpatched 3.10 and 3.11 versions must pass all `io.TextIOWrapper`{.interpreted-text role="class"} arguments, `encoding` included, as keywords.
:::
::::

::: method
Path.read_bytes()

Read the current file as bytes.
:::

:::: method
Path.joinpath(\*other)

Return a new Path object with each of the *other* arguments joined. The following are equivalent:

    >>> Path(...).joinpath('child').joinpath('grandchild')
    >>> Path(...).joinpath('child', 'grandchild')
    >>> Path(...) / 'child' / 'grandchild'

::: versionchanged
3.10 Prior to 3.10, `joinpath` was undocumented and accepted exactly one parameter.
:::
::::

The `zipp`{.interpreted-text role="pypi"} project provides backports of the latest path object functionality to older Pythons. Use `zipp.Path` in place of `zipfile.Path` for early access to changes.

## PyZipFile objects

The `PyZipFile`{.interpreted-text role="class"} constructor takes the same parameters as the `ZipFile`{.interpreted-text role="class"} constructor, and one additional parameter, *optimize*.

::::::::: {.PyZipFile(file, .mode='r', .compression=ZIP_STORED, .allowZip64=True, .\\ .optimize=-1)}
::: versionchanged
3.2 Added the *optimize* parameter.
:::

::: versionchanged
3.4 ZIP64 extensions are enabled by default.
:::

Instances have one method in addition to those of `ZipFile`{.interpreted-text role="class"} objects:

:::::: method
PyZipFile.writepy(pathname, basename=\'\', filterfunc=None)

Search for files `\*.py`{.interpreted-text role="file"} and add the corresponding file to the archive.

If the *optimize* parameter to `PyZipFile`{.interpreted-text role="class"} was not given or `-1`, the corresponding file is a `\*.pyc`{.interpreted-text role="file"} file, compiling if necessary.

If the *optimize* parameter to `PyZipFile`{.interpreted-text role="class"} was `0`, `1` or `2`, only files with that optimization level (see `compile`{.interpreted-text role="func"}) are added to the archive, compiling if necessary.

If *pathname* is a file, the filename must end with `.py`{.interpreted-text role="file"}, and just the (corresponding `\*.pyc`{.interpreted-text role="file"}) file is added at the top level (no path information). If *pathname* is a file that does not end with `.py`{.interpreted-text role="file"}, a `RuntimeError`{.interpreted-text role="exc"} will be raised. If it is a directory, and the directory is not a package directory, then all the files `\*.pyc`{.interpreted-text role="file"} are added at the top level. If the directory is a package directory, then all `\*.pyc`{.interpreted-text role="file"} are added under the package name as a file path, and if any subdirectories are package directories, all of these are added recursively in sorted order.

*basename* is intended for internal use only.

*filterfunc*, if given, must be a function taking a single string argument. It will be passed each path (including each individual full file path) before it is added to the archive. If *filterfunc* returns a false value, the path will not be added, and if it is a directory its contents will be ignored. For example, if our test files are all either in `test` directories or start with the string `test_`, we can use a *filterfunc* to exclude them:

    >>> zf = PyZipFile('myprog.zip')
    >>> def notests(s):
    ...     fn = os.path.basename(s)
    ...     return (not (fn == 'test' or fn.startswith('test_')))
    ...
    >>> zf.writepy('myprog', filterfunc=notests)

The `writepy`{.interpreted-text role="meth"} method makes archives with file names like this:

    string.pyc                   # Top level name
    test/__init__.pyc            # Package directory
    test/testall.pyc             # Module test.testall
    test/bogus/__init__.pyc      # Subpackage directory
    test/bogus/myfile.pyc        # Submodule test.bogus.myfile

::: versionchanged
3.4 Added the *filterfunc* parameter.
:::

::: versionchanged
3.6.2 The *pathname* parameter accepts a `path-like object`{.interpreted-text role="term"}.
:::

::: versionchanged
3.7 Recursion sorts directory entries.
:::
::::::
:::::::::

## ZipInfo objects

Instances of the `ZipInfo`{.interpreted-text role="class"} class are returned by the `.getinfo`{.interpreted-text role="meth"} and `.infolist`{.interpreted-text role="meth"} methods of `ZipFile`{.interpreted-text role="class"} objects. Each object stores information about a single member of the ZIP archive.

There is one classmethod to make a `ZipInfo`{.interpreted-text role="class"} instance for a filesystem file:

:::::: classmethod
ZipInfo.from_file(filename, arcname=None, \*, strict_timestamps=True)

Construct a `ZipInfo`{.interpreted-text role="class"} instance for a file on the filesystem, in preparation for adding it to a zip file.

*filename* should be the path to a file or directory on the filesystem.

If *arcname* is specified, it is used as the name within the archive. If *arcname* is not specified, the name will be the same as *filename*, but with any drive letter and leading path separators removed.

The *strict_timestamps* argument, when set to `False`, allows to zip files older than 1980-01-01 at the cost of setting the timestamp to 1980-01-01. Similar behavior occurs with files newer than 2107-12-31, the timestamp is also set to the limit.

::: versionadded
3.6
:::

::: versionchanged
3.6.2 The *filename* parameter accepts a `path-like object`{.interpreted-text role="term"}.
:::

::: versionchanged
3.8 Added the *strict_timestamps* keyword-only parameter.
:::
::::::

Instances have the following methods and attributes:

:::: method
ZipInfo.is_dir()

Return `True` if this archive member is a directory.

This uses the entry\'s name: directories should always end with `/`.

::: versionadded
3.6
:::
::::

::: attribute
ZipInfo.filename

Name of the file in the archive.
:::

::::: attribute
ZipInfo.date_time

The time and date of the last modification to the archive member. This is a tuple of six values representing the \"last \[modified\] file time\" and \"last \[modified\] file date\" fields from the ZIP file\'s central directory.

The tuple contains:

  ----------------------------------
  Index   Value
  ------- --------------------------
  `0`     Year (\>= 1980)

  `1`     Month (one-based)

  `2`     Day of month (one-based)

  `3`     Hours (zero-based)

  `4`     Minutes (zero-based)

  `5`     Seconds (zero-based)
  ----------------------------------

:::: note
::: title
Note
:::

The ZIP format supports multiple timestamp fields in different locations (central directory, extra fields for NTFS/UNIX systems, etc.). This attribute specifically returns the timestamp from the central directory. The central directory timestamp format in ZIP files does not support timestamps before 1980. While some extra field formats (such as UNIX timestamps) can represent earlier dates, this attribute only returns the central directory timestamp.

The central directory timestamp is interpreted as representing local time, rather than UTC time, to match the behavior of other zip tools.
::::
:::::

::: attribute
ZipInfo.compress_type

Type of compression for the archive member.
:::

::: attribute
ZipInfo.comment

Comment for the individual archive member as a `bytes`{.interpreted-text role="class"} object.
:::

::: attribute
ZipInfo.extra

Expansion field data. The [PKZIP Application Note](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT) contains some comments on the internal structure of the data contained in this `bytes`{.interpreted-text role="class"} object.
:::

::: attribute
ZipInfo.create_system

System which created ZIP archive.
:::

::: attribute
ZipInfo.create_version

PKZIP version which created ZIP archive.
:::

::: attribute
ZipInfo.extract_version

PKZIP version needed to extract archive.
:::

::: attribute
ZipInfo.reserved

Must be zero.
:::

::: attribute
ZipInfo.flag_bits

ZIP flag bits.
:::

::: attribute
ZipInfo.volume

Volume number of file header.
:::

::: attribute
ZipInfo.internal_attr

Internal attributes.
:::

::: attribute
ZipInfo.external_attr

External file attributes.
:::

::: attribute
ZipInfo.header_offset

Byte offset to the file header.
:::

::: attribute
ZipInfo.CRC

CRC-32 of the uncompressed file.
:::

::: attribute
ZipInfo.compress_size

Size of the compressed data.
:::

::: attribute
ZipInfo.file_size

Size of the uncompressed file.
:::

## Command-line interface

The `!zipfile`{.interpreted-text role="mod"} module provides a simple command-line interface to interact with ZIP archives.

If you want to create a new ZIP archive, specify its name after the `-c`{.interpreted-text role="option"} option and then list the filename(s) that should be included:

``` shell-session
$ python -m zipfile -c monty.zip spam.txt eggs.txt
```

Passing a directory is also acceptable:

``` shell-session
$ python -m zipfile -c monty.zip life-of-brian_1979/
```

If you want to extract a ZIP archive into the specified directory, use the `-e`{.interpreted-text role="option"} option:

``` shell-session
$ python -m zipfile -e monty.zip target-dir/
```

For a list of the files in a ZIP archive, use the `-l`{.interpreted-text role="option"} option:

``` shell-session
$ python -m zipfile -l monty.zip
```

### Command-line options

::: option

`-l <zipfile>`

:   

`--list <zipfile>`

:   

List files in a zipfile.
:::

::: option
-c \<zipfile\> \<source1\> \... \<sourceN\> \--create \<zipfile\> \<source1\> \... \<sourceN\>

Create zipfile from source files.
:::

::: option
-e \<zipfile\> \<output_dir\> \--extract \<zipfile\> \<output_dir\>

Extract zipfile into target directory.
:::

::: option

`-t <zipfile>`

:   

`--test <zipfile>`

:   

Test whether the zipfile is valid or not.
:::

:::: option

`--metadata-encoding <encoding>`

:   

Specify encoding of member names for `-l`{.interpreted-text role="option"}, `-e`{.interpreted-text role="option"} and `-t`{.interpreted-text role="option"}.

::: versionadded
3.11
:::
::::

## Decompression pitfalls

The extraction in zipfile module might fail due to some pitfalls listed below.

### From file itself

Decompression may fail due to incorrect password / CRC checksum / ZIP format or unsupported compression method / decryption.

### File system limitations

Exceeding limitations on different file systems can cause decompression failed. Such as allowable characters in the directory entries, length of the file name, length of the pathname, size of a single file, and number of files, etc.

### Resources limitations {#zipfile-resources-limitations}

The lack of memory or disk volume would lead to decompression failed. For example, decompression bombs (aka [ZIP bomb](https://en.wikipedia.org/wiki/Zip_bomb)) apply to zipfile library that can cause disk volume exhaustion.

### Interruption

Interruption during the decompression, such as pressing control-C or killing the decompression process may result in incomplete decompression of the archive.

### Default behaviors of extraction

Not knowing the default extraction behaviors can cause unexpected decompression results. For example, when extracting the same archive twice, it overwrites files without asking.
