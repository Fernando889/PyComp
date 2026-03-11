# `!posix`{.interpreted-text role="mod"} \-\-- The most common POSIX system calls

::: {.module synopsis="The most common POSIX system calls (normally used via module os)."}
posix
:::

------------------------------------------------------------------------

This module provides access to operating system functionality that is standardized by the C Standard and the POSIX standard (a thinly disguised Unix interface).

::: availability
Unix.
:::

::: index
pair: module; os
:::

**Do not import this module directly.** Instead, import the module `os`{.interpreted-text role="mod"}, which provides a *portable* version of this interface. On Unix, the `os`{.interpreted-text role="mod"} module provides a superset of the `!posix`{.interpreted-text role="mod"} interface. On non-Unix operating systems the `!posix`{.interpreted-text role="mod"} module is not available, but a subset is always available through the `os`{.interpreted-text role="mod"} interface. Once `os`{.interpreted-text role="mod"} is imported, there is *no* performance penalty in using it instead of `!posix`{.interpreted-text role="mod"}. In addition, `os`{.interpreted-text role="mod"} provides some additional functionality, such as automatically calling `~os.putenv`{.interpreted-text role="func"} when an entry in `os.environ` is changed.

Errors are reported as exceptions; the usual exceptions are given for type errors, while errors reported by the system calls raise `OSError`{.interpreted-text role="exc"}.

## Large File Support {#posix-large-files}

::: index
single: large files single: file; large files
:::

Several operating systems (including AIX and Solaris) provide support for files that are larger than 2 GiB from a C programming model where `int`{.interpreted-text role="c:expr"} and `long`{.interpreted-text role="c:expr"} are 32-bit values. This is typically accomplished by defining the relevant size and offset types as 64-bit values. Such files are sometimes referred to as `large files`{.interpreted-text role="dfn"}.

Large file support is enabled in Python when the size of an `off_t`{.interpreted-text role="c:type"} is larger than a `long`{.interpreted-text role="c:expr"} and the `long long`{.interpreted-text role="c:expr"} is at least as large as an `off_t`{.interpreted-text role="c:type"}. It may be necessary to configure and compile Python with certain compiler flags to enable this mode. For example, with Solaris 2.6 and 2.7 you need to do something like:

    CFLAGS="`getconf LFS_CFLAGS`" OPT="-g -O2 $CFLAGS" \
            ./configure

On large-file-capable Linux systems, this might work:

    CFLAGS='-D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64' OPT="-g -O2 $CFLAGS" \
            ./configure

## Notable Module Contents {#posix-contents}

In addition to many functions described in the `os`{.interpreted-text role="mod"} module documentation, `!posix`{.interpreted-text role="mod"} defines the following data item:

:::::: data
environ

A dictionary representing the string environment at the time the interpreter was started. Keys and values are bytes on Unix and str on Windows. For example, `environ[b'HOME']` (`environ['HOME']` on Windows) is the pathname of your home directory, equivalent to `getenv("HOME")` in C.

Modifying this dictionary does not affect the string environment passed on by `~os.execv`{.interpreted-text role="func"}, `~os.popen`{.interpreted-text role="func"} or `~os.system`{.interpreted-text role="func"}; if you need to change the environment, pass `environ` to `~os.execve`{.interpreted-text role="func"} or add variable assignments and export statements to the command string for `~os.system`{.interpreted-text role="func"} or `~os.popen`{.interpreted-text role="func"}.

::: versionchanged
3.2 On Unix, keys and values are bytes.
:::

:::: note
::: title
Note
:::

The `os`{.interpreted-text role="mod"} module provides an alternate implementation of `environ` which updates the environment on modification. Note also that updating `os.environ`{.interpreted-text role="data"} will render this dictionary obsolete. Use of the `os`{.interpreted-text role="mod"} module version of this is recommended over direct access to the `!posix`{.interpreted-text role="mod"} module.
::::
::::::
