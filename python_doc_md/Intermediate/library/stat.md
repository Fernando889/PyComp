# `!stat`{.interpreted-text role="mod"} \-\-- Interpreting `~os.stat`{.interpreted-text role="func"} results

::: {.module synopsis="Utilities for interpreting the results of os.stat(),
os.lstat() and os.fstat()."}
stat
:::

**Source code:** `Lib/stat.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

The `!stat`{.interpreted-text role="mod"} module defines constants and functions for interpreting the results of `os.stat`{.interpreted-text role="func"}, `os.fstat`{.interpreted-text role="func"} and `os.lstat`{.interpreted-text role="func"} (if they exist). For complete details about the `stat`{.interpreted-text role="c:func"}, `!fstat`{.interpreted-text role="c:func"} and `!lstat`{.interpreted-text role="c:func"} calls, consult the documentation for your system.

::: versionchanged
3.4 The stat module is backed by a C implementation.
:::

The `!stat`{.interpreted-text role="mod"} module defines the following functions to test for specific file types:

::: function
S_ISDIR(mode)

Return non-zero if the mode is from a directory.
:::

::: function
S_ISCHR(mode)

Return non-zero if the mode is from a character special device file.
:::

::: function
S_ISBLK(mode)

Return non-zero if the mode is from a block special device file.
:::

::: function
S_ISREG(mode)

Return non-zero if the mode is from a regular file.
:::

::: function
S_ISFIFO(mode)

Return non-zero if the mode is from a FIFO (named pipe).
:::

::: function
S_ISLNK(mode)

Return non-zero if the mode is from a symbolic link.
:::

::: function
S_ISSOCK(mode)

Return non-zero if the mode is from a socket.
:::

:::: function
S_ISDOOR(mode)

Return non-zero if the mode is from a door.

::: versionadded
3.4
:::
::::

:::: function
S_ISPORT(mode)

Return non-zero if the mode is from an event port.

::: versionadded
3.4
:::
::::

:::: function
S_ISWHT(mode)

Return non-zero if the mode is from a whiteout.

::: versionadded
3.4
:::
::::

Two additional functions are defined for more general manipulation of the file\'s mode:

::: function
S_IMODE(mode)

Return the portion of the file\'s mode that can be set by `os.chmod`{.interpreted-text role="func"}\-\--that is, the file\'s permission bits, plus the sticky bit, set-group-id, and set-user-id bits (on systems that support them).
:::

::: function
S_IFMT(mode)

Return the portion of the file\'s mode that describes the file type (used by the `!S_IS\*`{.interpreted-text role="func"} functions above).
:::

Normally, you would use the `!os.path.is\*`{.interpreted-text role="func"} functions for testing the type of a file; the functions here are useful when you are doing multiple tests of the same file and wish to avoid the overhead of the `stat`{.interpreted-text role="c:func"} system call for each test. These are also useful when checking for information about a file that isn\'t handled by `os.path`{.interpreted-text role="mod"}, like the tests for block and character devices.

Example:

    import os, sys
    from stat import *

    def walktree(top, callback):
        '''recursively descend the directory tree rooted at top,
           calling the callback function for each regular file'''

        for f in os.listdir(top):
            pathname = os.path.join(top, f)
            mode = os.lstat(pathname).st_mode
            if S_ISDIR(mode):
                # It's a directory, recurse into it
                walktree(pathname, callback)
            elif S_ISREG(mode):
                # It's a file, call the callback function
                callback(pathname)
            else:
                # Unknown file type, print a message
                print('Skipping %s' % pathname)

    def visitfile(file):
        print('visiting', file)

    if __name__ == '__main__':
        walktree(sys.argv[1], visitfile)

An additional utility function is provided to convert a file\'s mode in a human readable string:

::::: function
filemode(mode)

Convert a file\'s mode to a string of the form \'-rwxrwxrwx\'.

::: versionadded
3.3
:::

::: versionchanged
3.4 The function supports `S_IFDOOR`{.interpreted-text role="data"}, `S_IFPORT`{.interpreted-text role="data"} and `S_IFWHT`{.interpreted-text role="data"}.
:::
:::::

All the variables below are simply symbolic indexes into the 10-tuple returned by `os.stat`{.interpreted-text role="func"}, `os.fstat`{.interpreted-text role="func"} or `os.lstat`{.interpreted-text role="func"}.

::: data
ST_MODE

Inode protection mode.
:::

::: data
ST_INO

Inode number.
:::

::: data
ST_DEV

Device inode resides on.
:::

::: data
ST_NLINK

Number of links to the inode.
:::

::: data
ST_UID

User id of the owner.
:::

::: data
ST_GID

Group id of the owner.
:::

::: data
ST_SIZE

Size in bytes of a plain file; amount of data waiting on some special files.
:::

::: data
ST_ATIME

Time of last access.
:::

::: data
ST_MTIME

Time of last modification.
:::

::: data
ST_CTIME

The \"ctime\" as reported by the operating system. On some systems (like Unix) is the time of the last metadata change, and, on others (like Windows), is the creation time (see platform documentation for details).
:::

The interpretation of \"file size\" changes according to the file type. For plain files this is the size of the file in bytes. For FIFOs and sockets under most flavors of Unix (including Linux in particular), the \"size\" is the number of bytes waiting to be read at the time of the call to `os.stat`{.interpreted-text role="func"}, `os.fstat`{.interpreted-text role="func"}, or `os.lstat`{.interpreted-text role="func"}; this can sometimes be useful, especially for polling one of these special files after a non-blocking open. The meaning of the size field for other character and block devices varies more, depending on the implementation of the underlying system call.

The variables below define the flags used in the `ST_MODE`{.interpreted-text role="data"} field.

Use of the functions above is more portable than use of the first set of flags:

::: data
S_IFSOCK

Socket.
:::

::: data
S_IFLNK

Symbolic link.
:::

::: data
S_IFREG

Regular file.
:::

::: data
S_IFBLK

Block device.
:::

::: data
S_IFDIR

Directory.
:::

::: data
S_IFCHR

Character device.
:::

::: data
S_IFIFO

FIFO.
:::

:::: data
S_IFDOOR

Door.

::: versionadded
3.4
:::
::::

:::: data
S_IFPORT

Event port.

::: versionadded
3.4
:::
::::

:::: data
S_IFWHT

Whiteout.

::: versionadded
3.4
:::
::::

:::: note
::: title
Note
:::

`S_IFDOOR`{.interpreted-text role="data"}, `S_IFPORT`{.interpreted-text role="data"} or `S_IFWHT`{.interpreted-text role="data"} are defined as 0 when the platform does not have support for the file types.
::::

The following flags can also be used in the *mode* argument of `os.chmod`{.interpreted-text role="func"}:

::: data
S_ISUID

Set UID bit.
:::

::: data
S_ISGID

Set-group-ID bit. This bit has several special uses. For a directory it indicates that BSD semantics is to be used for that directory: files created there inherit their group ID from the directory, not from the effective group ID of the creating process, and directories created there will also get the `S_ISGID`{.interpreted-text role="data"} bit set. For a file that does not have the group execution bit (`S_IXGRP`{.interpreted-text role="data"}) set, the set-group-ID bit indicates mandatory file/record locking (see also `S_ENFMT`{.interpreted-text role="data"}).
:::

::: data
S_ISVTX

Sticky bit. When this bit is set on a directory it means that a file in that directory can be renamed or deleted only by the owner of the file, by the owner of the directory, or by a privileged process.
:::

::: data
S_IRWXU

Mask for file owner permissions.
:::

::: data
S_IRUSR

Owner has read permission.
:::

::: data
S_IWUSR

Owner has write permission.
:::

::: data
S_IXUSR

Owner has execute permission.
:::

::: data
S_IRWXG

Mask for group permissions.
:::

::: data
S_IRGRP

Group has read permission.
:::

::: data
S_IWGRP

Group has write permission.
:::

::: data
S_IXGRP

Group has execute permission.
:::

::: data
S_IRWXO

Mask for permissions for others (not in group).
:::

::: data
S_IROTH

Others have read permission.
:::

::: data
S_IWOTH

Others have write permission.
:::

::: data
S_IXOTH

Others have execute permission.
:::

::: data
S_ENFMT

System V file locking enforcement. This flag is shared with `S_ISGID`{.interpreted-text role="data"}: file/record locking is enforced on files that do not have the group execution bit (`S_IXGRP`{.interpreted-text role="data"}) set.
:::

::: data
S_IREAD

Unix V7 synonym for `S_IRUSR`{.interpreted-text role="data"}.
:::

::: data
S_IWRITE

Unix V7 synonym for `S_IWUSR`{.interpreted-text role="data"}.
:::

::: data
S_IEXEC

Unix V7 synonym for `S_IXUSR`{.interpreted-text role="data"}.
:::

The following flags can be used in the *flags* argument of `os.chflags`{.interpreted-text role="func"}:

:::: data
UF_SETTABLE

All user settable flags.

::: versionadded
3.13
:::
::::

::: data
UF_NODUMP

Do not dump the file.
:::

::: data
UF_IMMUTABLE

The file may not be changed.
:::

::: data
UF_APPEND

The file may only be appended to.
:::

::: data
UF_OPAQUE

The directory is opaque when viewed through a union stack.
:::

::: data
UF_NOUNLINK

The file may not be renamed or deleted.
:::

::: data
UF_COMPRESSED

The file is stored compressed (macOS 10.6+).
:::

:::: data
UF_TRACKED

Used for handling document IDs (macOS)

::: versionadded
3.13
:::
::::

:::: data
UF_DATAVAULT

The file needs an entitlement for reading or writing (macOS 10.13+)

::: versionadded
3.13
:::
::::

::: data
UF_HIDDEN

The file should not be displayed in a GUI (macOS 10.5+).
:::

:::: data
SF_SETTABLE

All super-user changeable flags

::: versionadded
3.13
:::
::::

::::: data
SF_SUPPORTED

All super-user supported flags

::: availability
macOS
:::

::: versionadded
3.13
:::
:::::

::::: data
SF_SYNTHETIC

All super-user read-only synthetic flags

::: availability
macOS
:::

::: versionadded
3.13
:::
:::::

::: data
SF_ARCHIVED

The file may be archived.
:::

::: data
SF_IMMUTABLE

The file may not be changed.
:::

::: data
SF_APPEND

The file may only be appended to.
:::

:::: data
SF_RESTRICTED

The file needs an entitlement to write to (macOS 10.13+)

::: versionadded
3.13
:::
::::

::: data
SF_NOUNLINK

The file may not be renamed or deleted.
:::

::: data
SF_SNAPSHOT

The file is a snapshot file.
:::

:::: data
SF_FIRMLINK

The file is a firmlink (macOS 10.15+)

::: versionadded
3.13
:::
::::

:::: data
SF_DATALESS

The file is a dataless object (macOS 10.15+)

::: versionadded
3.13
:::
::::

See the \*BSD or macOS systems man page `chflags(2)`{.interpreted-text role="manpage"} for more information.

On Windows, the following file attribute constants are available for use when testing bits in the `st_file_attributes` member returned by `os.stat`{.interpreted-text role="func"}. See the [Windows API documentation](https://msdn.microsoft.com/en-us/library/windows/desktop/gg258117.aspx) for more detail on the meaning of these constants.

:::: data
FILE_ATTRIBUTE_ARCHIVE FILE_ATTRIBUTE_COMPRESSED FILE_ATTRIBUTE_DEVICE FILE_ATTRIBUTE_DIRECTORY FILE_ATTRIBUTE_ENCRYPTED FILE_ATTRIBUTE_HIDDEN FILE_ATTRIBUTE_INTEGRITY_STREAM FILE_ATTRIBUTE_NORMAL FILE_ATTRIBUTE_NOT_CONTENT_INDEXED FILE_ATTRIBUTE_NO_SCRUB_DATA FILE_ATTRIBUTE_OFFLINE FILE_ATTRIBUTE_READONLY FILE_ATTRIBUTE_REPARSE_POINT FILE_ATTRIBUTE_SPARSE_FILE FILE_ATTRIBUTE_SYSTEM FILE_ATTRIBUTE_TEMPORARY FILE_ATTRIBUTE_VIRTUAL

::: versionadded
3.5
:::
::::

On Windows, the following constants are available for comparing against the `st_reparse_tag` member returned by `os.lstat`{.interpreted-text role="func"}. These are well-known constants, but are not an exhaustive list.

:::: data
IO_REPARSE_TAG_SYMLINK IO_REPARSE_TAG_MOUNT_POINT IO_REPARSE_TAG_APPEXECLINK

::: versionadded
3.8
:::
::::

On Linux, the following file attribute constants are available for use when testing bits in the `~os.statx_result.stx_attributes`{.interpreted-text role="attr"} and `~os.statx_result.stx_attributes_mask`{.interpreted-text role="attr"} members returned by `os.statx`{.interpreted-text role="func"}. See the `statx(2)`{.interpreted-text role="manpage"} man page for more detail on the meaning of these constants.

:::: data
STATX_ATTR_COMPRESSED STATX_ATTR_IMMUTABLE STATX_ATTR_APPEND STATX_ATTR_NODUMP STATX_ATTR_ENCRYPTED STATX_ATTR_AUTOMOUNT STATX_ATTR_MOUNT_ROOT STATX_ATTR_VERITY STATX_ATTR_DAX STATX_ATTR_WRITE_ATOMIC

::: versionadded
3.15
:::
::::
