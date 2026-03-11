# `!fcntl`{.interpreted-text role="mod"} \-\-- The `fcntl` and `ioctl` system calls

::: {.module synopsis="The fcntl() and ioctl() system calls."}
fcntl
:::

::: index
pair: UNIX; file control pair: UNIX; I/O control
:::

------------------------------------------------------------------------

This module performs file and I/O control on file descriptors. It is an interface to the `fcntl`{.interpreted-text role="c:func"} and `ioctl`{.interpreted-text role="c:func"} Unix routines. See the `fcntl(2)`{.interpreted-text role="manpage"} and `ioctl(2)`{.interpreted-text role="manpage"} Unix manual pages for full details.

::: availability
Unix, not WASI.
:::

All functions in this module take a file descriptor *fd* as their first argument. This can be an integer file descriptor, such as returned by `sys.stdin.fileno()`, or an `io.IOBase`{.interpreted-text role="class"} object, such as `sys.stdin` itself, which provides a `~io.IOBase.fileno`{.interpreted-text role="meth"} that returns a genuine file descriptor.

::: versionchanged
3.3 Operations in this module used to raise an `IOError`{.interpreted-text role="exc"} where they now raise an `OSError`{.interpreted-text role="exc"}.
:::

::: versionchanged
3.8 The `!fcntl`{.interpreted-text role="mod"} module now contains `F_ADD_SEALS`, `F_GET_SEALS`, and `F_SEAL_*` constants for sealing of `os.memfd_create`{.interpreted-text role="func"} file descriptors.
:::

::: versionchanged
3.9 On macOS, the `!fcntl`{.interpreted-text role="mod"} module exposes the `F_GETPATH` constant, which obtains the path of a file from a file descriptor. On Linux(\>=3.15), the `!fcntl`{.interpreted-text role="mod"} module exposes the `F_OFD_GETLK`, `F_OFD_SETLK` and `F_OFD_SETLKW` constants, which are used when working with open file description locks.
:::

::: versionchanged
3.10 On Linux \>= 2.6.11, the `!fcntl`{.interpreted-text role="mod"} module exposes the `F_GETPIPE_SZ` and `F_SETPIPE_SZ` constants, which allow to check and modify a pipe\'s size respectively.
:::

::: versionchanged
3.11 On FreeBSD, the `!fcntl`{.interpreted-text role="mod"} module exposes the `F_DUP2FD` and `F_DUP2FD_CLOEXEC` constants, which allow to duplicate a file descriptor, the latter setting `FD_CLOEXEC` flag in addition.
:::

::: versionchanged
3.12 On Linux \>= 4.5, the `!fcntl`{.interpreted-text role="mod"} module exposes the `FICLONE` and `FICLONERANGE` constants, which allow to share some data of one file with another file by reflinking on some filesystems (e.g., btrfs, OCFS2, and XFS). This behavior is commonly referred to as \"copy-on-write\".
:::

::: versionchanged
3.13 On Linux \>= 2.6.32, the `!fcntl`{.interpreted-text role="mod"} module exposes the `F_GETOWN_EX`, `F_SETOWN_EX`, `F_OWNER_TID`, `F_OWNER_PID`, `F_OWNER_PGRP` constants, which allow to direct I/O availability signals to a specific thread, process, or process group. On Linux \>= 4.13, the `!fcntl`{.interpreted-text role="mod"} module exposes the `F_GET_RW_HINT`, `F_SET_RW_HINT`, `F_GET_FILE_RW_HINT`, `F_SET_FILE_RW_HINT`, and `RWH_WRITE_LIFE_*` constants, which allow to inform the kernel about the relative expected lifetime of writes on a given inode or via a particular open file description. On Linux \>= 5.1 and NetBSD, the `!fcntl`{.interpreted-text role="mod"} module exposes the `F_SEAL_FUTURE_WRITE` constant for use with `F_ADD_SEALS` and `F_GET_SEALS` operations. On FreeBSD, the `!fcntl`{.interpreted-text role="mod"} module exposes the `F_READAHEAD`, `F_ISUNIONSTACK`, and `F_KINFO` constants. On macOS and FreeBSD, the `!fcntl`{.interpreted-text role="mod"} module exposes the `F_RDAHEAD` constant. On NetBSD and AIX, the `!fcntl`{.interpreted-text role="mod"} module exposes the `F_CLOSEM` constant. On NetBSD, the `!fcntl`{.interpreted-text role="mod"} module exposes the `F_MAXFD` constant. On macOS and NetBSD, the `!fcntl`{.interpreted-text role="mod"} module exposes the `F_GETNOSIGPIPE` and `F_SETNOSIGPIPE` constant.
:::

::: versionchanged
3.14 On Linux \>= 6.1, the `!fcntl`{.interpreted-text role="mod"} module exposes the `F_DUPFD_QUERY` to query a file descriptor pointing to the same file.
:::

The module defines the following functions:

:::::::: function
fcntl(fd, cmd, arg=0, /)

Perform the operation *cmd* on file descriptor *fd* (file objects providing a `~io.IOBase.fileno`{.interpreted-text role="meth"} method are accepted as well). The values used for *cmd* are operating system dependent, and are available as constants in the `!fcntl`{.interpreted-text role="mod"} module, using the same names as used in the relevant C header files. The argument *arg* can either be an integer value, a `bytes-like object`{.interpreted-text role="term"}, or a string. The type and size of *arg* must match the type and size of the argument of the operation as specified in the relevant C documentation.

When *arg* is an integer, the function returns the integer return value of the C `fcntl`{.interpreted-text role="c:func"} call.

When the argument is bytes-like object, it represents a binary structure, for example, created by `struct.pack`{.interpreted-text role="func"}. A string value is encoded to binary using the UTF-8 encoding. The binary data is copied to a buffer whose address is passed to the C `fcntl`{.interpreted-text role="c:func"} call. The return value after a successful call is the contents of the buffer, converted to a `bytes`{.interpreted-text role="class"} object. The length of the returned object will be the same as the length of the *arg* argument.

If the `fcntl`{.interpreted-text role="c:func"} call fails, an `OSError`{.interpreted-text role="exc"} is raised.

:::: note
::: title
Note
:::

If the type or size of *arg* does not match the type or size of the operation\'s argument (for example, if an integer is passed when a pointer is expected, or the information returned in the buffer by the operating system is larger than the size of *arg*), this is most likely to result in a segmentation violation or a more subtle data corruption.
::::

::: audit-event
fcntl.fcntl fd,cmd,arg fcntl.fcntl
:::

::: versionchanged
3.14 Add support of arbitrary `bytes-like objects <bytes-like object>`{.interpreted-text role="term"}, not only `bytes`{.interpreted-text role="class"}.
:::

::: versionchanged
3.15 The size of bytes-like objects is no longer limited to 1024 bytes.
:::
::::::::

:::::::: function
ioctl(fd, request, arg=0, mutate_flag=True, /)

This function is identical to the `~fcntl.fcntl`{.interpreted-text role="func"} function, except that the argument handling is even more complicated.

The *request* parameter is limited to values that can fit in 32-bits or 64-bits, depending on the platform. Additional constants of interest for use as the *request* argument can be found in the `termios`{.interpreted-text role="mod"} module, under the same names as used in the relevant C header files.

The parameter *arg* can be an integer, a `bytes-like object`{.interpreted-text role="term"}, or a string. The type and size of *arg* must match the type and size of the argument of the operation as specified in the relevant C documentation.

If *arg* does not support the read-write buffer interface or the *mutate_flag* is false, behavior is as for the `~fcntl.fcntl`{.interpreted-text role="func"} function.

If *arg* supports the read-write buffer interface (like `bytearray`{.interpreted-text role="class"}) and *mutate_flag* is true (the default), then the buffer is (in effect) passed to the underlying `!ioctl`{.interpreted-text role="c:func"} system call, the latter\'s return code is passed back to the calling Python, and the buffer\'s new contents reflect the action of the `ioctl`{.interpreted-text role="c:func"}. This is a slight simplification, because if the supplied buffer is less than 1024 bytes long it is first copied into a static buffer 1024 bytes long which is then passed to `ioctl`{.interpreted-text role="func"} and copied back into the supplied buffer.

If the `ioctl`{.interpreted-text role="c:func"} call fails, an `OSError`{.interpreted-text role="exc"} exception is raised.

:::: note
::: title
Note
:::

If the type or size of *arg* does not match the type or size of the operation\'s argument (for example, if an integer is passed when a pointer is expected, or the information returned in the buffer by the operating system is larger than the size of *arg*), this is most likely to result in a segmentation violation or a more subtle data corruption.
::::

An example:

    >>> import array, fcntl, struct, termios, os
    >>> os.getpgrp()
    13341
    >>> struct.unpack('h', fcntl.ioctl(0, termios.TIOCGPGRP, "  "))[0]
    13341
    >>> buf = array.array('h', [0])
    >>> fcntl.ioctl(0, termios.TIOCGPGRP, buf, 1)
    0
    >>> buf
    array('h', [13341])

::: audit-event
fcntl.ioctl fd,request,arg fcntl.ioctl
:::

::: versionchanged
3.14 The GIL is always released during a system call. System calls failing with EINTR are automatically retried.
:::

::: versionchanged
3.15 The size of not mutated bytes-like objects is no longer limited to 1024 bytes.
:::
::::::::

:::: function
flock(fd, operation, /)

Perform the lock operation *operation* on file descriptor *fd* (file objects providing a `~io.IOBase.fileno`{.interpreted-text role="meth"} method are accepted as well). See the Unix manual `flock(2)`{.interpreted-text role="manpage"} for details. (On some systems, this function is emulated using `fcntl`{.interpreted-text role="c:func"}.)

If the `flock`{.interpreted-text role="c:func"} call fails, an `OSError`{.interpreted-text role="exc"} exception is raised.

::: audit-event
fcntl.flock fd,operation fcntl.flock
:::
::::

:::::::: function
lockf(fd, cmd, len=0, start=0, whence=0, /)

This is essentially a wrapper around the `~fcntl.fcntl`{.interpreted-text role="func"} locking calls. *fd* is the file descriptor (file objects providing a `~io.IOBase.fileno`{.interpreted-text role="meth"} method are accepted as well) of the file to lock or unlock, and *cmd* is one of the following values:

::: data
LOCK_UN

Release an existing lock.
:::

::: data
LOCK_SH

Acquire a shared lock.
:::

::: data
LOCK_EX

Acquire an exclusive lock.
:::

::: data
LOCK_NB

Bitwise OR with any of the other three `LOCK_*` constants to make the request non-blocking.
:::

If `!LOCK_NB`{.interpreted-text role="const"} is used and the lock cannot be acquired, an `OSError`{.interpreted-text role="exc"} will be raised and the exception will have an *errno* attribute set to `~errno.EACCES`{.interpreted-text role="const"} or `~errno.EAGAIN`{.interpreted-text role="const"} (depending on the operating system; for portability, check for both values). On at least some systems, `!LOCK_EX`{.interpreted-text role="const"} can only be used if the file descriptor refers to a file opened for writing.

*len* is the number of bytes to lock, *start* is the byte offset at which the lock starts, relative to *whence*, and *whence* is as with `io.IOBase.seek`{.interpreted-text role="func"}, specifically:

- `0` \-- relative to the start of the file (`os.SEEK_SET`{.interpreted-text role="const"})
- `1` \-- relative to the current buffer position (`os.SEEK_CUR`{.interpreted-text role="const"})
- `2` \-- relative to the end of the file (`os.SEEK_END`{.interpreted-text role="const"})

The default for *start* is 0, which means to start at the beginning of the file. The default for *len* is 0 which means to lock to the end of the file. The default for *whence* is also 0.

::: audit-event
fcntl.lockf fd,cmd,len,start,whence fcntl.lockf
:::
::::::::

Examples (all on a SVR4 compliant system):

    import struct, fcntl, os

    f = open(...)
    rv = fcntl.fcntl(f, fcntl.F_SETFL, os.O_NDELAY)

    lockdata = struct.pack('hhllhh', fcntl.F_WRLCK, 0, 0, 0, 0, 0)
    rv = fcntl.fcntl(f, fcntl.F_SETLKW, lockdata)

Note that in the first example the return value variable *rv* will hold an integer value; in the second example it will hold a `bytes`{.interpreted-text role="class"} object. The structure lay-out for the *lockdata* variable is system dependent \-\-- therefore using the `flock`{.interpreted-text role="func"} call may be better.

::: seealso

Module `os`{.interpreted-text role="mod"}

:   If the locking flags `~os.O_SHLOCK`{.interpreted-text role="const"} and `~os.O_EXLOCK`{.interpreted-text role="const"} are present in the `os`{.interpreted-text role="mod"} module (on BSD only), the `os.open`{.interpreted-text role="func"} function provides an alternative to the `lockf`{.interpreted-text role="func"} and `flock`{.interpreted-text role="func"} functions.
:::
