# `!mmap`{.interpreted-text role="mod"} \-\-- Memory-mapped file support

::: {.module synopsis="Interface to memory-mapped files for Unix and Windows."}
mmap
:::

------------------------------------------------------------------------

::: availability
not WASI.

This module does not work or is not available on WebAssembly. See `wasm-availability`{.interpreted-text role="ref"} for more information.
:::

Memory-mapped file objects behave like both `bytearray`{.interpreted-text role="class"} and like `file objects <file object>`{.interpreted-text role="term"}. You can use mmap objects in most places where `bytearray`{.interpreted-text role="class"} are expected; for example, you can use the `re`{.interpreted-text role="mod"} module to search through a memory-mapped file. You can also change a single byte by doing `obj[index] = 97`, or change a subsequence by assigning to a slice: `obj[i1:i2] = b'...'`. You can also read and write data starting at the current file position, and `seek`{.interpreted-text role="meth"} through the file to different positions.

A memory-mapped file is created by the `~mmap.mmap`{.interpreted-text role="class"} constructor, which is different on Unix and on Windows. In either case you must provide a file descriptor for a file opened for update. If you wish to map an existing Python file object, use its `~io.IOBase.fileno`{.interpreted-text role="meth"} method to obtain the correct value for the *fileno* parameter. Otherwise, you can open the file using the `os.open`{.interpreted-text role="func"} function, which returns a file descriptor directly (the file still needs to be closed when done).

:::: note
::: title
Note
:::

If you want to create a memory-mapping for a writable, buffered file, you should `~io.IOBase.flush`{.interpreted-text role="func"} the file first. This is necessary to ensure that local modifications to the buffers are actually available to the mapping.
::::

For both the Unix and Windows versions of the constructor, *access* may be specified as an optional keyword parameter. *access* accepts one of four values: `ACCESS_READ`{.interpreted-text role="const"}, `ACCESS_WRITE`{.interpreted-text role="const"}, or `ACCESS_COPY`{.interpreted-text role="const"} to specify read-only, write-through or copy-on-write memory respectively, or `ACCESS_DEFAULT`{.interpreted-text role="const"} to defer to *prot*. *access* can be used on both Unix and Windows. If *access* is not specified, Windows mmap returns a write-through mapping. The initial memory values for all three access types are taken from the specified file. Assignment to an `ACCESS_READ`{.interpreted-text role="const"} memory map raises a `TypeError`{.interpreted-text role="exc"} exception. Assignment to an `ACCESS_WRITE`{.interpreted-text role="const"} memory map affects both memory and the underlying file. Assignment to an `ACCESS_COPY`{.interpreted-text role="const"} memory map affects memory but does not update the underlying file.

::: versionchanged
3.7 Added `ACCESS_DEFAULT`{.interpreted-text role="const"} constant.
:::

To map anonymous memory, -1 should be passed as the fileno along with the length.

::::: {.mmap(fileno, .length, .tagname=None, .\\ .access=ACCESS_DEFAULT, .offset=0, .*, .trackfd=True)}
**(Windows version)** Maps *length* bytes from the file specified by the file descriptor *fileno*, and creates a mmap object. If *length* is larger than the current size of the file, the file is extended to contain *length* bytes. If *length* is `0`, the maximum length of the map is the current size of the file, except that if the file is empty Windows raises an exception (you cannot create an empty mapping on Windows).

*tagname*, if specified and not `None`, is a string giving a tag name for the mapping. Windows allows you to have many different mappings against the same file. If you specify the name of an existing tag, that tag is opened, otherwise a new tag of this name is created. If this parameter is omitted or `None`, the mapping is created without a name. Avoiding the use of the *tagname* parameter will assist in keeping your code portable between Unix and Windows.

*offset* may be specified as a non-negative integer offset. mmap references will be relative to the offset from the beginning of the file. *offset* defaults to 0. *offset* must be a multiple of the `ALLOCATIONGRANULARITY`{.interpreted-text role="const"}.

If *trackfd* is `False`, the file handle corresponding to *fileno* will not be duplicated, and the resulting `!mmap`{.interpreted-text role="class"} object will not be associated with the map\'s underlying file. This means that the `~mmap.mmap.size`{.interpreted-text role="meth"} and `~mmap.mmap.resize`{.interpreted-text role="meth"} methods will fail. This mode is useful to limit the number of open file handles. The original file can be renamed (but not deleted) after closing *fileno*.

::: versionchanged
3.15 The *trackfd* parameter was added.
:::

::: audit-event
mmap.\_\_new\_\_ fileno,length,access,offset mmap.mmap
:::
:::::

:::::::::::::::::::::::::::::::::::::::: {.mmap(fileno, .length, .flags=MAP_SHARED, .prot=PROT_WRITE|PROT_READ, .\\ .access=ACCESS_DEFAULT, .offset=0, .*, .trackfd=True) noindex=""}
**(Unix version)** Maps *length* bytes from the file specified by the file descriptor *fileno*, and returns a mmap object. If *length* is `0`, the maximum length of the map will be the current size of the file when `~mmap.mmap`{.interpreted-text role="class"} is called.

*flags* specifies the nature of the mapping. `MAP_PRIVATE`{.interpreted-text role="const"} creates a private copy-on-write mapping, so changes to the contents of the mmap object will be private to this process, and `MAP_SHARED`{.interpreted-text role="const"} creates a mapping that\'s shared with all other processes mapping the same areas of the file. The default value is `MAP_SHARED`{.interpreted-text role="const"}. Some systems have additional possible flags with the full list specified in `MAP_* constants <map-constants>`{.interpreted-text role="ref"}.

*prot*, if specified, gives the desired memory protection; the two most useful values are `PROT_READ`{.interpreted-text role="const"} and `PROT_WRITE`{.interpreted-text role="const"}, to specify that the pages may be read or written. *prot* defaults to `PROT_READ \| PROT_WRITE`{.interpreted-text role="const"}.

*access* may be specified in lieu of *flags* and *prot* as an optional keyword parameter. It is an error to specify both *flags*, *prot* and *access*. See the description of *access* above for information on how to use this parameter.

*offset* may be specified as a non-negative integer offset. mmap references will be relative to the offset from the beginning of the file. *offset* defaults to 0. *offset* must be a multiple of `ALLOCATIONGRANULARITY`{.interpreted-text role="const"} which is equal to `PAGESIZE`{.interpreted-text role="const"} on Unix systems.

If *trackfd* is `False`, the file descriptor specified by *fileno* will not be duplicated, and the resulting `!mmap`{.interpreted-text role="class"} object will not be associated with the map\'s underlying file. This means that the `~mmap.mmap.size`{.interpreted-text role="meth"} and `~mmap.mmap.resize`{.interpreted-text role="meth"} methods will fail. This mode is useful to limit the number of open file descriptors.

To ensure validity of the created memory mapping the file specified by the descriptor *fileno* is internally automatically synchronized with the physical backing store on macOS.

::: versionchanged
3.13 The *trackfd* parameter was added.
:::

This example shows a simple way of using `~mmap.mmap`{.interpreted-text role="class"}:

    import mmap

    # write a simple example file
    with open("hello.txt", "wb") as f:
        f.write(b"Hello Python!\n")

    with open("hello.txt", "r+b") as f:
        # memory-map the file, size 0 means whole file
        mm = mmap.mmap(f.fileno(), 0)
        # read content via standard file methods
        print(mm.readline())  # prints b"Hello Python!\n"
        # read content via slice notation
        print(mm[:5])  # prints b"Hello"
        # update content using slice notation;
        # note that new content must have same size
        mm[6:] = b" world!\n"
        # ... and read again using standard file methods
        mm.seek(0)
        print(mm.readline())  # prints b"Hello  world!\n"
        # close the map
        mm.close()

`~mmap.mmap`{.interpreted-text role="class"} can also be used as a context manager in a `with`{.interpreted-text role="keyword"} statement:

    import mmap

    with mmap.mmap(-1, 13) as mm:
        mm.write(b"Hello world!")

::: versionadded
3.2 Context manager support.
:::

The next example demonstrates how to create an anonymous map and exchange data between the parent and child processes:

    import mmap
    import os

    mm = mmap.mmap(-1, 13)
    mm.write(b"Hello world!")

    pid = os.fork()

    if pid == 0:  # In a child process
        mm.seek(0)
        print(mm.readline())

        mm.close()

::: audit-event
mmap.\_\_new\_\_ fileno,length,access,offset mmap.mmap
:::

Memory-mapped file objects support the following methods:

::: method
close()

Closes the mmap. Subsequent calls to other methods of the object will result in a ValueError exception being raised. This will not close the open file.
:::

:::: attribute
closed

`True` if the file is closed.

::: versionadded
3.2
:::
::::

:::: method
find(sub\[, start\[, end\]\])

Returns the lowest index in the object where the subsequence *sub* is found, such that *sub* is contained in the range \[*start*, *end*\]. Optional arguments *start* and *end* are interpreted as in slice notation. Returns `-1` on failure.

::: versionchanged
3.5 Writable `bytes-like object`{.interpreted-text role="term"} is now accepted.
:::
::::

:::::: method
flush(\[offset\[, size\]\], \*, flags=MS_SYNC)

Flushes changes made to the in-memory copy of a file back to disk. Without use of this call there is no guarantee that changes are written back before the object is destroyed. If *offset* and *size* are specified, only changes to the given range of bytes will be flushed to disk; otherwise, the whole extent of the mapping is flushed. *offset* must be a multiple of the `PAGESIZE`{.interpreted-text role="const"} or `ALLOCATIONGRANULARITY`{.interpreted-text role="const"}.

The *flags* parameter specifies the synchronization behavior. *flags* must be one of the `MS_* constants <ms-constants>`{.interpreted-text role="ref"} available on the system.

On Windows, the *flags* parameter is ignored.

`None` is returned to indicate success. An exception is raised when the call failed.

::: versionchanged
3.8 Previously, a nonzero value was returned on success; zero was returned on error under Windows. A zero value was returned on success; an exception was raised on error under Unix.
:::

::: versionchanged
3.15 Allow specifying *offset* without *size*. Previously, both *offset* and *size* parameters were required together. Now *offset* can be specified alone, and the flush operation will extend from *offset* to the end of the mmap.
:::

::: versionchanged
3.15 Added *flags* parameter to control synchronization behavior.
:::
::::::

:::: method
madvise(option\[, start\[, length\]\])

Send advice *option* to the kernel about the memory region beginning at *start* and extending *length* bytes. *option* must be one of the `MADV_* constants <madvise-constants>`{.interpreted-text role="ref"} available on the system. If *start* and *length* are omitted, the entire mapping is spanned. On some systems (including Linux), *start* must be a multiple of the `PAGESIZE`{.interpreted-text role="const"}.

Availability: Systems with the `madvise()` system call.

::: versionadded
3.8
:::
::::

::: method
move(dest, src, count)

Copy the *count* bytes starting at offset *src* to the destination index *dest*. If the mmap was created with `ACCESS_READ`{.interpreted-text role="const"}, then calls to move will raise a `TypeError`{.interpreted-text role="exc"} exception.
:::

:::: method
read(\[n\])

Return a `bytes`{.interpreted-text role="class"} containing up to *n* bytes starting from the current file position. If the argument is omitted, `None` or negative, return all bytes from the current file position to the end of the mapping. The file position is updated to point after the bytes that were returned.

::: versionchanged
3.3 Argument can be omitted or `None`.
:::
::::

::: method
read_byte()

Returns a byte at the current file position as an integer, and advances the file position by 1.
:::

::: method
readline()

Returns a single line, starting at the current file position and up to the next newline. The file position is updated to point after the bytes that were returned.
:::

:::: method
resize(newsize)

Resizes the map and the underlying file, if any.

Resizing a map created with *access* of `ACCESS_READ`{.interpreted-text role="const"} or `ACCESS_COPY`{.interpreted-text role="const"}, will raise a `TypeError`{.interpreted-text role="exc"} exception. Resizing a map created with *trackfd* set to `False`, will raise a `ValueError`{.interpreted-text role="exc"} exception.

**On Windows**: Resizing the map will raise an `OSError`{.interpreted-text role="exc"} if there are other maps against the same named file. Resizing an anonymous map (ie against the pagefile) will silently create a new map with the original data copied over up to the length of the new size.

Availability: Windows and systems with the `mremap()` system call.

::: versionchanged
3.11 Correctly fails if attempting to resize when another map is held Allows resize against an anonymous map on Windows
:::
::::

:::: method
rfind(sub\[, start\[, end\]\])

Returns the highest index in the object where the subsequence *sub* is found, such that *sub* is contained in the range \[*start*, *end*\]. Optional arguments *start* and *end* are interpreted as in slice notation. Returns `-1` on failure.

::: versionchanged
3.5 Writable `bytes-like object`{.interpreted-text role="term"} is now accepted.
:::
::::

:::: method
seek(pos\[, whence\])

Set the file\'s current position. *whence* argument is optional and defaults to `os.SEEK_SET` or `0` (absolute file positioning); other values are `os.SEEK_CUR` or `1` (seek relative to the current position) and `os.SEEK_END` or `2` (seek relative to the file\'s end).

::: versionchanged
3.13 Return the new absolute position instead of `None`.
:::
::::

:::: method
seekable()

Return whether the file supports seeking, and the return value is always `True`.

::: versionadded
3.13
:::
::::

::::: method
set_name(name, /)

Annotate the memory mapping with the given *name* for easier identification in `/proc/<pid>/maps` if the kernel supports the feature and `-X dev <-X>`{.interpreted-text role="option"} is passed to Python or if Python is built in `debug mode <debug-build>`{.interpreted-text role="ref"}. The length of *name* must not exceed 67 bytes including the `'\0'` terminator.

::: availability
Linux \>= 5.17 (kernel built with `CONFIG_ANON_VMA_NAME` option)
:::

::: versionadded
3.15
:::
:::::

:::: method
size()

Return the length of the file, which can be larger than the size of the memory-mapped area. For an anonymous mapping, return its size.

::: versionchanged
3.15 Anonymous mappings are now supported on Unix.
:::
::::

::: method
tell()

Returns the current position of the file pointer.
:::

::::: method
write(bytes)

Write the bytes in *bytes* into memory at the current position of the file pointer and return the number of bytes written (never less than `len(bytes)`, since if the write fails, a `ValueError`{.interpreted-text role="exc"} will be raised). The file position is updated to point after the bytes that were written. If the mmap was created with `ACCESS_READ`{.interpreted-text role="const"}, then writing to it will raise a `TypeError`{.interpreted-text role="exc"} exception.

::: versionchanged
3.5 Writable `bytes-like object`{.interpreted-text role="term"} is now accepted.
:::

::: versionchanged
3.6 The number of bytes written is now returned.
:::
:::::

::: method
write_byte(byte)

Write the integer *byte* into memory at the current position of the file pointer; the file position is advanced by `1`. If the mmap was created with `ACCESS_READ`{.interpreted-text role="const"}, then writing to it will raise a `TypeError`{.interpreted-text role="exc"} exception.
:::
::::::::::::::::::::::::::::::::::::::::

## [MADV]()\* Constants {#madvise-constants}

:::: data
MADV_NORMAL MADV_RANDOM MADV_SEQUENTIAL MADV_WILLNEED MADV_DONTNEED MADV_REMOVE MADV_DONTFORK MADV_DOFORK MADV_HWPOISON MADV_MERGEABLE MADV_UNMERGEABLE MADV_SOFT_OFFLINE MADV_HUGEPAGE MADV_NOHUGEPAGE MADV_DONTDUMP MADV_DODUMP MADV_FREE MADV_NOSYNC MADV_AUTOSYNC MADV_NOCORE MADV_CORE MADV_PROTECT MADV_FREE_REUSABLE MADV_FREE_REUSE

These options can be passed to `mmap.madvise`{.interpreted-text role="meth"}. Not every option will be present on every system.

Availability: Systems with the madvise() system call.

::: versionadded
3.8
:::
::::

## [MAP]()\* Constants

::::::: data
MAP_SHARED MAP_PRIVATE MAP_32BIT MAP_ALIGNED_SUPER MAP_ANON MAP_ANONYMOUS MAP_CONCEAL MAP_DENYWRITE MAP_EXECUTABLE MAP_HASSEMAPHORE MAP_JIT MAP_NOCACHE MAP_NOEXTEND MAP_NORESERVE MAP_POPULATE MAP_RESILIENT_CODESIGN MAP_RESILIENT_MEDIA MAP_STACK MAP_TPRO MAP_TRANSLATED_ALLOW_EXECUTE MAP_UNIX03

These are the various flags that can be passed to `mmap.mmap`{.interpreted-text role="meth"}. `MAP_ALIGNED_SUPER`{.interpreted-text role="data"} is only available at FreeBSD and `MAP_CONCEAL`{.interpreted-text role="data"} is only available at OpenBSD. Note that some options might not be present on some systems.

::: versionchanged
3.10 Added `MAP_POPULATE`{.interpreted-text role="data"} constant.
:::

::: versionadded
3.11 Added `MAP_STACK`{.interpreted-text role="data"} constant.
:::

::: versionadded
3.12 Added `MAP_ALIGNED_SUPER`{.interpreted-text role="data"} and `MAP_CONCEAL`{.interpreted-text role="data"} constants.
:::

::: versionadded
3.13 Added `MAP_32BIT`{.interpreted-text role="data"}, `MAP_HASSEMAPHORE`{.interpreted-text role="data"}, `MAP_JIT`{.interpreted-text role="data"}, `MAP_NOCACHE`{.interpreted-text role="data"}, `MAP_NOEXTEND`{.interpreted-text role="data"}, `MAP_NORESERVE`{.interpreted-text role="data"}, `MAP_RESILIENT_CODESIGN`{.interpreted-text role="data"}, `MAP_RESILIENT_MEDIA`{.interpreted-text role="data"}, `MAP_TPRO`{.interpreted-text role="data"}, `MAP_TRANSLATED_ALLOW_EXECUTE`{.interpreted-text role="data"}, and `MAP_UNIX03`{.interpreted-text role="data"} constants.
:::
:::::::

## [MS]()\* Constants

:::: data
MS_SYNC MS_ASYNC MS_INVALIDATE

These flags control the synchronization behavior for `mmap.flush`{.interpreted-text role="meth"}:

- `MS_SYNC`{.interpreted-text role="data"} - Synchronous flush: writes are scheduled and the call blocks until they are physically written to storage.
- `MS_ASYNC`{.interpreted-text role="data"} - Asynchronous flush: writes are scheduled but the call returns immediately without waiting for completion.
- `MS_INVALIDATE`{.interpreted-text role="data"} - Invalidate cached data: invalidates other mappings of the same file so they can see the changes.

::: versionadded
3.15
:::
::::
