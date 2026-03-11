# `!os`{.interpreted-text role="mod"} \-\-- Miscellaneous operating system interfaces

::: {.module synopsis="Miscellaneous operating system interfaces."}
os
:::

**Source code:** `Lib/os.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

This module provides a portable way of using operating system dependent functionality. If you just want to read or write a file see `open`{.interpreted-text role="func"}, if you want to manipulate paths, see the `os.path`{.interpreted-text role="mod"} module, and if you want to read all the lines in all the files on the command line see the `fileinput`{.interpreted-text role="mod"} module. For creating temporary files and directories see the `tempfile`{.interpreted-text role="mod"} module, and for high-level file and directory handling see the `shutil`{.interpreted-text role="mod"} module.

Notes on the availability of these functions:

- The design of all built-in operating system dependent modules of Python is such that as long as the same functionality is available, it uses the same interface; for example, the function `os.stat(path)` returns stat information about *path* in the same format (which happens to have originated with the POSIX interface).
- Extensions peculiar to a particular operating system are also available through the `!os`{.interpreted-text role="mod"} module, but using them is of course a threat to portability.
- All functions accepting path or file names accept both bytes and string objects, and result in an object of the same type, if a path or file name is returned.
- On VxWorks, os.popen, os.fork, os.execv and os.spawn\*p\* are not supported.
- On WebAssembly platforms, Android and iOS, large parts of the `!os`{.interpreted-text role="mod"} module are not available or behave differently. APIs related to processes (e.g. `~os.fork`{.interpreted-text role="func"}, `~os.execve`{.interpreted-text role="func"}) and resources (e.g. `~os.nice`{.interpreted-text role="func"}) are not available. Others like `~os.getuid`{.interpreted-text role="func"} and `~os.getpid`{.interpreted-text role="func"} are emulated or stubs. WebAssembly platforms also lack support for signals (e.g. `~os.kill`{.interpreted-text role="func"}, `~os.wait`{.interpreted-text role="func"}).

:::: note
::: title
Note
:::

All functions in this module raise `OSError`{.interpreted-text role="exc"} (or subclasses thereof) in the case of invalid or inaccessible file names and paths, or other arguments that have the correct type, but are not accepted by the operating system.
::::

::: exception
error

An alias for the built-in `OSError`{.interpreted-text role="exc"} exception.
:::

:::: data
name

The name of the operating system dependent module imported. The following names have currently been registered: `'posix'`, `'nt'`, `'java'`.

::: seealso
`sys.platform`{.interpreted-text role="data"} has a finer granularity. `os.uname`{.interpreted-text role="func"} gives system-dependent version information.

The `platform`{.interpreted-text role="mod"} module provides detailed checks for the system\'s identity.
:::
::::

## File Names, Command Line Arguments, and Environment Variables[]{#os-filenames} {#filesystem-encoding}

In Python, file names, command line arguments, and environment variables are represented using the string type. On some systems, decoding these strings to and from bytes is necessary before passing them to the operating system. Python uses the `filesystem encoding and error handler`{.interpreted-text role="term"} to perform this conversion (see `sys.getfilesystemencoding`{.interpreted-text role="func"}).

The `filesystem encoding and error handler`{.interpreted-text role="term"} are configured at Python startup by the `PyConfig_Read`{.interpreted-text role="c:func"} function: see `~PyConfig.filesystem_encoding`{.interpreted-text role="c:member"} and `~PyConfig.filesystem_errors`{.interpreted-text role="c:member"} members of `PyConfig`{.interpreted-text role="c:type"}.

::: versionchanged
3.1 On some systems, conversion using the file system encoding may fail. In this case, Python uses the `surrogateescape encoding error handler
<surrogateescape>`{.interpreted-text role="ref"}, which means that undecodable bytes are replaced by a Unicode character U+DC*xx* on decoding, and these are again translated to the original byte on encoding.
:::

The `file system encoding <filesystem encoding and error handler>`{.interpreted-text role="term"} must guarantee to successfully decode all bytes below 128. If the file system encoding fails to provide this guarantee, API functions can raise `UnicodeError`{.interpreted-text role="exc"}.

See also the `locale encoding`{.interpreted-text role="term"}.

## Python UTF-8 Mode {#utf8-mode}

::: versionadded
3.7 See `540`{.interpreted-text role="pep"} for more details.
:::

::: versionchanged
3.15

Python UTF-8 mode is now enabled by default (`686`{.interpreted-text role="pep"}). It may be disabled by setting `PYTHONUTF8=0 <PYTHONUTF8>`{.interpreted-text role="envvar"} as an environment variable or by using the `-X utf8=0 <-X>`{.interpreted-text role="option"} command line option.
:::

The Python UTF-8 Mode ignores the `locale encoding`{.interpreted-text role="term"} and forces the usage of the UTF-8 encoding:

- Use UTF-8 as the `filesystem encoding <filesystem encoding and error
  handler>`{.interpreted-text role="term"}.
- `sys.getfilesystemencoding`{.interpreted-text role="func"} returns `'utf-8'`.
- `locale.getpreferredencoding`{.interpreted-text role="func"} returns `'utf-8'` (the *do_setlocale* argument has no effect).
- `sys.stdin`{.interpreted-text role="data"}, `sys.stdout`{.interpreted-text role="data"}, and `sys.stderr`{.interpreted-text role="data"} all use UTF-8 as their text encoding, with the `surrogateescape` `error handler <error-handlers>`{.interpreted-text role="ref"} being enabled for `sys.stdin`{.interpreted-text role="data"} and `sys.stdout`{.interpreted-text role="data"} (`sys.stderr`{.interpreted-text role="data"} continues to use `backslashreplace` as it does in the default locale-aware mode)
- On Unix, `os.device_encoding`{.interpreted-text role="func"} returns `'utf-8'` rather than the device encoding.

Note that the standard stream settings in UTF-8 mode can be overridden by `PYTHONIOENCODING`{.interpreted-text role="envvar"} (just as they can be in the default locale-aware mode).

As a consequence of the changes in those lower level APIs, other higher level APIs also exhibit different default behaviours:

- Command line arguments, environment variables and filenames are decoded to text using the UTF-8 encoding.
- `os.fsdecode`{.interpreted-text role="func"} and `os.fsencode`{.interpreted-text role="func"} use the UTF-8 encoding.
- `open`{.interpreted-text role="func"}, `io.open`{.interpreted-text role="func"}, and `codecs.open`{.interpreted-text role="func"} use the UTF-8 encoding by default. However, they still use the strict error handler by default so that attempting to open a binary file in text mode is likely to raise an exception rather than producing nonsense data.

The `Python UTF-8 Mode <utf8-mode>`{.interpreted-text role="ref"} is enabled by default. It can be disabled using the `-X utf8=0 <-X>`{.interpreted-text role="option"} command line option or the `PYTHONUTF8=0 <PYTHONUTF8>`{.interpreted-text role="envvar"} environment variable. The Python UTF-8 Mode can only be disabled at Python startup. Its value can be read from `sys.flags.utf8_mode <sys.flags>`{.interpreted-text role="data"}.

If the UTF-8 mode is disabled, the interpreter defaults to using the current locale settings, *unless* the current locale is identified as a legacy ASCII-based locale (as described for `PYTHONCOERCECLOCALE`{.interpreted-text role="envvar"}), and locale coercion is either disabled or fails. In such legacy locales, the interpreter will default to enabling UTF-8 mode unless explicitly instructed not to do so.

See also the `UTF-8 mode on Windows <win-utf8-mode>`{.interpreted-text role="ref"} and the `filesystem encoding and error handler`{.interpreted-text role="term"}.

## Process Parameters {#os-procinfo}

These functions and data items provide information and operate on the current process and user.

:::: function
ctermid()

Return the filename corresponding to the controlling terminal of the process.

::: availability
Unix, not WASI.
:::
::::

::::::::: data
environ

A `mapping`{.interpreted-text role="term"} object where keys and values are strings that represent the process environment. For example, `environ['HOME']` is the pathname of your home directory (on some platforms), and is equivalent to `getenv("HOME")` in C.

This mapping is captured the first time the `!os`{.interpreted-text role="mod"} module is imported, typically during Python startup as part of processing `site.py`{.interpreted-text role="file"}. Changes to the environment made after this time are not reflected in `os.environ`{.interpreted-text role="data"}, except for changes made by modifying `os.environ`{.interpreted-text role="data"} directly.

This mapping may be used to modify the environment as well as query the environment. `putenv`{.interpreted-text role="func"} will be called automatically when the mapping is modified.

On Unix, keys and values use `sys.getfilesystemencoding`{.interpreted-text role="func"} and `'surrogateescape'` error handler. Use `environb`{.interpreted-text role="data"} if you would like to use a different encoding.

On Windows, the keys are converted to uppercase. This also applies when getting, setting, or deleting an item. For example, `environ['monty'] = 'python'` maps the key `'MONTY'` to the value `'python'`.

:::: note
::: title
Note
:::

Calling `putenv`{.interpreted-text role="func"} directly does not change `os.environ`{.interpreted-text role="data"}, so it\'s better to modify `os.environ`{.interpreted-text role="data"}.
::::

:::: note
::: title
Note
:::

On some platforms, including FreeBSD and macOS, setting `environ` may cause memory leaks. Refer to the system documentation for `!putenv`{.interpreted-text role="c:func"}.
::::

You can delete items in this mapping to unset environment variables. `unsetenv`{.interpreted-text role="func"} will be called automatically when an item is deleted from `os.environ`{.interpreted-text role="data"}, and when one of the `~dict.pop`{.interpreted-text role="meth"} or `~dict.clear`{.interpreted-text role="meth"} methods is called.

::: seealso
The `os.reload_environ`{.interpreted-text role="func"} function.
:::

::: versionchanged
3.9 Updated to support `584`{.interpreted-text role="pep"}\'s merge (`|`) and update (`|=`) operators.
:::
:::::::::

::::: data
environb

Bytes version of `environ`{.interpreted-text role="data"}: a `mapping`{.interpreted-text role="term"} object where both keys and values are `bytes`{.interpreted-text role="class"} objects representing the process environment. `environ`{.interpreted-text role="data"} and `environb`{.interpreted-text role="data"} are synchronized (modifying `environb`{.interpreted-text role="data"} updates `environ`{.interpreted-text role="data"}, and vice versa).

`environb`{.interpreted-text role="data"} is only available if `supports_bytes_environ`{.interpreted-text role="const"} is `True`.

::: versionadded
3.2
:::

::: versionchanged
3.9 Updated to support `584`{.interpreted-text role="pep"}\'s merge (`|`) and update (`|=`) operators.
:::
:::::

:::::: function
reload_environ()

The `os.environ`{.interpreted-text role="data"} and `os.environb`{.interpreted-text role="data"} mappings are a cache of environment variables at the time that Python started. As such, changes to the current process environment are not reflected if made outside Python, or by `os.putenv`{.interpreted-text role="func"} or `os.unsetenv`{.interpreted-text role="func"}. Use `!os.reload_environ`{.interpreted-text role="func"} to update `os.environ`{.interpreted-text role="data"} and `os.environb`{.interpreted-text role="data"} with any such changes to the current process environment.

:::: warning
::: title
Warning
:::

This function is not thread-safe. Calling it while the environment is being modified in another thread is an undefined behavior. Reading from `os.environ`{.interpreted-text role="data"} or `os.environb`{.interpreted-text role="data"}, or calling `os.getenv`{.interpreted-text role="func"} while reloading, may return an empty result.
::::

::: versionadded
3.14
:::
::::::

::: {.function noindex=""}
chdir(path) fchdir(fd) getcwd()

These functions are described in `os-file-dir`{.interpreted-text role="ref"}.
:::

::::: function
fsencode(filename)

Encode `path-like <path-like object>`{.interpreted-text role="term"} *filename* to the `filesystem encoding and error handler`{.interpreted-text role="term"}; return `bytes`{.interpreted-text role="class"} unchanged.

`fsdecode`{.interpreted-text role="func"} is the reverse function.

::: versionadded
3.2
:::

::: versionchanged
3.6 Support added to accept objects implementing the `os.PathLike`{.interpreted-text role="class"} interface.
:::
:::::

::::: function
fsdecode(filename)

Decode the `path-like <path-like object>`{.interpreted-text role="term"} *filename* from the `filesystem encoding and error handler`{.interpreted-text role="term"}; return `str`{.interpreted-text role="class"} unchanged.

`fsencode`{.interpreted-text role="func"} is the reverse function.

::: versionadded
3.2
:::

::: versionchanged
3.6 Support added to accept objects implementing the `os.PathLike`{.interpreted-text role="class"} interface.
:::
:::::

:::: function
fspath(path)

Return the file system representation of the path.

If `str`{.interpreted-text role="class"} or `bytes`{.interpreted-text role="class"} is passed in, it is returned unchanged. Otherwise `~os.PathLike.__fspath__`{.interpreted-text role="meth"} is called and its value is returned as long as it is a `str`{.interpreted-text role="class"} or `bytes`{.interpreted-text role="class"} object. In all other cases, `TypeError`{.interpreted-text role="exc"} is raised.

::: versionadded
3.6
:::
::::

::::: PathLike
An `abstract base class`{.interpreted-text role="term"} for objects representing a file system path, e.g. `pathlib.PurePath`{.interpreted-text role="class"}.

::: versionadded
3.6
:::

::: {.method abstractmethod=""}
\_\_fspath\_\_()

Return the file system path representation of the object.

The method should only return a `str`{.interpreted-text role="class"} or `bytes`{.interpreted-text role="class"} object, with the preference being for `str`{.interpreted-text role="class"}.
:::
:::::

:::: function
getenv(key, default=None)

Return the value of the environment variable *key* as a string if it exists, or *default* if it doesn\'t. *key* is a string. Note that since `getenv`{.interpreted-text role="func"} uses `os.environ`{.interpreted-text role="data"}, the mapping of `getenv`{.interpreted-text role="func"} is similarly also captured on import, and the function may not reflect future environment changes.

On Unix, keys and values are decoded with `sys.getfilesystemencoding`{.interpreted-text role="func"} and `'surrogateescape'` error handler. Use `os.getenvb`{.interpreted-text role="func"} if you would like to use a different encoding.

::: availability
Unix, Windows.
:::
::::

::::: function
getenvb(key, default=None)

Return the value of the environment variable *key* as bytes if it exists, or *default* if it doesn\'t. *key* must be bytes. Note that since `getenvb`{.interpreted-text role="func"} uses `os.environb`{.interpreted-text role="data"}, the mapping of `getenvb`{.interpreted-text role="func"} is similarly also captured on import, and the function may not reflect future environment changes.

`getenvb`{.interpreted-text role="func"} is only available if `supports_bytes_environ`{.interpreted-text role="const"} is `True`.

::: availability
Unix.
:::

::: versionadded
3.2
:::
:::::

:::: function
get_exec_path(env=None)

Returns the list of directories that will be searched for a named executable, similar to a shell, when launching a process. *env*, when specified, should be an environment variable dictionary to lookup the PATH in. By default, when *env* is `None`, `environ`{.interpreted-text role="data"} is used.

::: versionadded
3.2
:::
::::

:::: function
getegid()

Return the effective group id of the current process. This corresponds to the \"set id\" bit on the file being executed in the current process.

::: availability
Unix, not WASI.
:::
::::

::::: function
geteuid()

::: index
single: user; effective id
:::

Return the current process\'s effective user id.

::: availability
Unix, not WASI.
:::
:::::

::::: function
getgid()

::: index
single: process; group
:::

Return the real group id of the current process.

::: availability
Unix.

The function is a stub on WASI, see `wasm-availability`{.interpreted-text role="ref"} for more information.
:::
:::::

::::: function
getgrouplist(user, group, /)

Return list of group ids that *user* belongs to. If *group* is not in the list, it is included; typically, *group* is specified as the group ID field from the password record for *user*, because that group ID will otherwise be potentially omitted.

::: availability
Unix, not WASI.
:::

::: versionadded
3.3
:::
:::::

:::::: function
getgroups()

Return list of supplemental group ids associated with the current process.

::: availability
Unix, not WASI.
:::

:::: note
::: title
Note
:::

On macOS, `getgroups`{.interpreted-text role="func"} behavior differs somewhat from other Unix platforms. If the Python interpreter was built with a deployment target of `10.5` or earlier, `getgroups`{.interpreted-text role="func"} returns the list of effective group ids associated with the current user process; this list is limited to a system-defined number of entries, typically 16, and may be modified by calls to `setgroups`{.interpreted-text role="func"} if suitably privileged. If built with a deployment target greater than `10.5`, `getgroups`{.interpreted-text role="func"} returns the current group access list for the user associated with the effective user id of the process; the group access list may change over the lifetime of the process, it is not affected by calls to `setgroups`{.interpreted-text role="func"}, and its length is not limited to 16. The deployment target value can be obtained with `sysconfig.get_config_var('MACOSX_DEPLOYMENT_TARGET') <sysconfig.get_config_var>`{.interpreted-text role="func"}.
::::
::::::

:::: function
getlogin()

Return the name of the user logged in on the controlling terminal of the process. For most purposes, it is more useful to use `getpass.getuser`{.interpreted-text role="func"} since the latter checks the environment variables `LOGNAME`{.interpreted-text role="envvar"} or `USERNAME`{.interpreted-text role="envvar"} to find out who the user is, and falls back to `pwd.getpwuid(os.getuid())[0]` to get the login name of the current real user id.

::: availability
Unix, Windows, not WASI.
:::
::::

:::: function
getpgid(pid)

Return the process group id of the process with process id *pid*. If *pid* is 0, the process group id of the current process is returned.

::: availability
Unix, not WASI.
:::
::::

::::: function
getpgrp()

::: index
single: process; group
:::

Return the id of the current process group.

::: availability
Unix, not WASI.
:::
:::::

:::: function
getpid()

::: index
single: process; id
:::

Return the current process id.

The function is a stub on WASI, see `wasm-availability`{.interpreted-text role="ref"} for more information.
::::

:::::: function
getppid()

::: index
single: process; id of parent
:::

Return the parent\'s process id. When the parent process has exited, on Unix the id returned is the one of the init process (1), on Windows it is still the same id, which may be already reused by another process.

::: availability
Unix, Windows, not WASI.
:::

::: versionchanged
3.2 Added support for Windows.
:::
::::::

:::::: function
getpriority(which, who)

::: index
single: process; scheduling priority
:::

Get program scheduling priority. The value *which* is one of `PRIO_PROCESS`{.interpreted-text role="const"}, `PRIO_PGRP`{.interpreted-text role="const"}, or `PRIO_USER`{.interpreted-text role="const"}, and *who* is interpreted relative to *which* (a process identifier for `PRIO_PROCESS`{.interpreted-text role="const"}, process group identifier for `PRIO_PGRP`{.interpreted-text role="const"}, and a user ID for `PRIO_USER`{.interpreted-text role="const"}). A zero value for *who* denotes (respectively) the calling process, the process group of the calling process, or the real user ID of the calling process.

::: availability
Unix, not WASI.
:::

::: versionadded
3.3
:::
::::::

::::: data
PRIO_PROCESS PRIO_PGRP PRIO_USER

Parameters for the `getpriority`{.interpreted-text role="func"} and `setpriority`{.interpreted-text role="func"} functions.

::: availability
Unix, not WASI.
:::

::: versionadded
3.3
:::
:::::

::::: data
PRIO_DARWIN_THREAD PRIO_DARWIN_PROCESS PRIO_DARWIN_BG PRIO_DARWIN_NONUI

Parameters for the `getpriority`{.interpreted-text role="func"} and `setpriority`{.interpreted-text role="func"} functions.

::: availability
macOS
:::

::: versionadded
3.12
:::
:::::

::::: function
getresuid()

Return a tuple (ruid, euid, suid) denoting the current process\'s real, effective, and saved user ids.

::: availability
Unix, not WASI.
:::

::: versionadded
3.2
:::
:::::

::::: function
getresgid()

Return a tuple (rgid, egid, sgid) denoting the current process\'s real, effective, and saved group ids.

::: availability
Unix, not WASI.
:::

::: versionadded
3.2
:::
:::::

::::: function
getuid()

::: index
single: user; id
:::

Return the current process\'s real user id.

::: availability
Unix.

The function is a stub on WASI, see `wasm-availability`{.interpreted-text role="ref"} for more information.
:::
:::::

::::: function
initgroups(username, gid, /)

Call the system `initgroups()` to initialize the group access list with all of the groups of which the specified username is a member, plus the specified group id.

::: availability
Unix, not WASI, not Android.
:::

::: versionadded
3.2
:::
:::::

:::::::: function
putenv(key, value, /)

::: index
single: environment variables; setting
:::

Set the environment variable named *key* to the string *value*. Such changes to the environment affect subprocesses started with `os.system`{.interpreted-text role="func"}, `popen`{.interpreted-text role="func"} or `fork`{.interpreted-text role="func"} and `execv`{.interpreted-text role="func"}.

Assignments to items in `os.environ`{.interpreted-text role="data"} are automatically translated into corresponding calls to `putenv`{.interpreted-text role="func"}; however, calls to `putenv`{.interpreted-text role="func"} don\'t update `os.environ`{.interpreted-text role="data"}, so it is actually preferable to assign to items of `os.environ`{.interpreted-text role="data"}. This also applies to `getenv`{.interpreted-text role="func"} and `getenvb`{.interpreted-text role="func"}, which respectively use `os.environ`{.interpreted-text role="data"} and `os.environb`{.interpreted-text role="data"} in their implementations.

See also the `os.reload_environ`{.interpreted-text role="func"} function.

:::: note
::: title
Note
:::

On some platforms, including FreeBSD and macOS, setting `environ` may cause memory leaks. Refer to the system documentation for `!putenv`{.interpreted-text role="c:func"}.
::::

::: audit-event
os.putenv key,value os.putenv
:::

::: versionchanged
3.9 The function is now always available.
:::
::::::::

:::: function
setegid(egid, /)

Set the current process\'s effective group id.

::: availability
Unix, not WASI, not Android.
:::
::::

:::: function
seteuid(euid, /)

Set the current process\'s effective user id.

::: availability
Unix, not WASI, not Android.
:::
::::

:::: function
setgid(gid, /)

Set the current process\' group id.

::: availability
Unix, not WASI, not Android.
:::
::::

:::::: function
setgroups(groups, /)

Set the list of supplemental group ids associated with the current process to *groups*. *groups* must be a sequence, and each element must be an integer identifying a group. This operation is typically available only to the superuser.

::: availability
Unix, not WASI.
:::

:::: note
::: title
Note
:::

On macOS, the length of *groups* may not exceed the system-defined maximum number of effective group ids, typically 16. See the documentation for `getgroups`{.interpreted-text role="func"} for cases where it may not return the same group list set by calling setgroups().
::::
::::::

:::::: function
setns(fd, nstype=0)

Reassociate the current thread with a Linux namespace. See the `setns(2)`{.interpreted-text role="manpage"} and `namespaces(7)`{.interpreted-text role="manpage"} man pages for more details.

If *fd* refers to a `/proc/{pid}/ns/`{.interpreted-text role="file"} link, `setns()` reassociates the calling thread with the namespace associated with that link, and *nstype* may be set to one of the `CLONE_NEW* constants <os-unshare-clone-flags>`{.interpreted-text role="ref"} to impose constraints on the operation (`0` means no constraints).

Since Linux 5.8, *fd* may refer to a PID file descriptor obtained from `~os.pidfd_open`{.interpreted-text role="func"}. In this case, `setns()` reassociates the calling thread into one or more of the same namespaces as the thread referred to by *fd*. This is subject to any constraints imposed by *nstype*, which is a bit mask combining one or more of the `CLONE_NEW* constants <os-unshare-clone-flags>`{.interpreted-text role="ref"}, e.g. `setns(fd, os.CLONE_NEWUTS | os.CLONE_NEWPID)`. The caller\'s memberships in unspecified namespaces are left unchanged.

*fd* can be any object with a `~io.IOBase.fileno`{.interpreted-text role="meth"} method, or a raw file descriptor.

This example reassociates the thread with the `init` process\'s network namespace:

    fd = os.open("/proc/1/ns/net", os.O_RDONLY)
    os.setns(fd, os.CLONE_NEWNET)
    os.close(fd)

::: availability
Linux \>= 3.0 with glibc \>= 2.14.
:::

::: versionadded
3.12
:::

::: seealso
The `~os.unshare`{.interpreted-text role="func"} function.
:::
::::::

:::: function
setpgrp()

Call the system call `!setpgrp`{.interpreted-text role="c:func"} or `setpgrp(0, 0)` depending on which version is implemented (if any). See the Unix manual for the semantics.

::: availability
Unix, not WASI.
:::
::::

:::: function
setpgid(pid, pgrp, /)

Call the system call `!setpgid`{.interpreted-text role="c:func"} to set the process group id of the process with id *pid* to the process group with id *pgrp*. See the Unix manual for the semantics.

::: availability
Unix, not WASI.
:::
::::

:::::: function
setpriority(which, who, priority)

::: index
single: process; scheduling priority
:::

Set program scheduling priority. The value *which* is one of `PRIO_PROCESS`{.interpreted-text role="const"}, `PRIO_PGRP`{.interpreted-text role="const"}, or `PRIO_USER`{.interpreted-text role="const"}, and *who* is interpreted relative to *which* (a process identifier for `PRIO_PROCESS`{.interpreted-text role="const"}, process group identifier for `PRIO_PGRP`{.interpreted-text role="const"}, and a user ID for `PRIO_USER`{.interpreted-text role="const"}). A zero value for *who* denotes (respectively) the calling process, the process group of the calling process, or the real user ID of the calling process. *priority* is a value in the range -20 to 19. The default priority is 0; lower priorities cause more favorable scheduling.

::: availability
Unix, not WASI.
:::

::: versionadded
3.3
:::
::::::

:::: function
setregid(rgid, egid, /)

Set the current process\'s real and effective group ids.

::: availability
Unix, not WASI, not Android.
:::
::::

::::: function
setresgid(rgid, egid, sgid, /)

Set the current process\'s real, effective, and saved group ids.

::: availability
Unix, not WASI, not Android.
:::

::: versionadded
3.2
:::
:::::

::::: function
setresuid(ruid, euid, suid, /)

Set the current process\'s real, effective, and saved user ids.

::: availability
Unix, not WASI, not Android.
:::

::: versionadded
3.2
:::
:::::

:::: function
setreuid(ruid, euid, /)

Set the current process\'s real and effective user ids.

::: availability
Unix, not WASI, not Android.
:::
::::

:::: function
getsid(pid, /)

Call the system call `!getsid`{.interpreted-text role="c:func"}. See the Unix manual for the semantics.

::: availability
Unix, not WASI.
:::
::::

:::: function
setsid()

Call the system call `!setsid`{.interpreted-text role="c:func"}. See the Unix manual for the semantics.

::: availability
Unix, not WASI.
:::
::::

::::: function
setuid(uid, /)

::: index
single: user; id, setting
:::

Set the current process\'s user id.

::: availability
Unix, not WASI, not Android.
:::
:::::

::: function
strerror(code, /)

Return the error message corresponding to the error code in *code*. On platforms where `!strerror`{.interpreted-text role="c:func"} returns `NULL` when given an unknown error number, `ValueError`{.interpreted-text role="exc"} is raised.
:::

:::: data
supports_bytes_environ

`True` if the native OS type of the environment is bytes (eg. `False` on Windows).

::: versionadded
3.2
:::
::::

::: function
umask(mask, /)

Set the current numeric umask and return the previous umask.

The function is a stub on WASI, see `wasm-availability`{.interpreted-text role="ref"} for more information.
:::

:::::: function
uname()

::: index
single: gethostname() (in module socket) single: gethostbyaddr() (in module socket)
:::

Returns information identifying the current operating system. The return value is an object with five attributes:

- `sysname`{.interpreted-text role="attr"} - operating system name
- `nodename`{.interpreted-text role="attr"} - name of machine on network (implementation-defined)
- `release`{.interpreted-text role="attr"} - operating system release
- `version`{.interpreted-text role="attr"} - operating system version
- `machine`{.interpreted-text role="attr"} - hardware identifier

For backwards compatibility, this object is also iterable, behaving like a five-tuple containing `sysname`{.interpreted-text role="attr"}, `nodename`{.interpreted-text role="attr"}, `release`{.interpreted-text role="attr"}, `version`{.interpreted-text role="attr"}, and `machine`{.interpreted-text role="attr"} in that order.

Some systems truncate `nodename`{.interpreted-text role="attr"} to 8 characters or to the leading component; a better way to get the hostname is `socket.gethostname`{.interpreted-text role="func"} or even `socket.gethostbyaddr(socket.gethostname())`.

On macOS, iOS and Android, this returns the *kernel* name and version (i.e., `'Darwin'` on macOS and iOS; `'Linux'` on Android). `platform.uname`{.interpreted-text role="func"} can be used to get the user-facing operating system name and version on iOS and Android.

::: availability
Unix.
:::

::: versionchanged
3.3 Return type changed from a tuple to a tuple-like object with named attributes.
:::
::::::

:::::: function
unsetenv(key, /)

::: index
single: environment variables; deleting
:::

Unset (delete) the environment variable named *key*. Such changes to the environment affect subprocesses started with `os.system`{.interpreted-text role="func"}, `popen`{.interpreted-text role="func"} or `fork`{.interpreted-text role="func"} and `execv`{.interpreted-text role="func"}.

Deletion of items in `os.environ`{.interpreted-text role="data"} is automatically translated into a corresponding call to `unsetenv`{.interpreted-text role="func"}; however, calls to `unsetenv`{.interpreted-text role="func"} don\'t update `os.environ`{.interpreted-text role="data"}, so it is actually preferable to delete items of `os.environ`{.interpreted-text role="data"}.

See also the `os.reload_environ`{.interpreted-text role="func"} function.

::: audit-event
os.unsetenv key os.unsetenv
:::

::: versionchanged
3.9 The function is now always available and is also available on Windows.
:::
::::::

:::::: function
unshare(flags)

Disassociate parts of the process execution context, and move them into a newly created namespace. See the `unshare(2)`{.interpreted-text role="manpage"} man page for more details. The *flags* argument is a bit mask, combining zero or more of the `CLONE_* constants <os-unshare-clone-flags>`{.interpreted-text role="ref"}, that specifies which parts of the execution context should be unshared from their existing associations and moved to a new namespace. If the *flags* argument is `0`, no changes are made to the calling process\'s execution context.

::: availability
Linux \>= 2.6.16.
:::

::: versionadded
3.12
:::

::: seealso
The `~os.setns`{.interpreted-text role="func"} function.
:::
::::::

::: {#os-unshare-clone-flags}
Flags to the `unshare`{.interpreted-text role="func"} function, if the implementation supports them. See `unshare(2)`{.interpreted-text role="manpage"} in the Linux manual for their exact effect and availability.
:::

::: data
CLONE_FILES CLONE_FS CLONE_NEWCGROUP CLONE_NEWIPC CLONE_NEWNET CLONE_NEWNS CLONE_NEWPID CLONE_NEWTIME CLONE_NEWUSER CLONE_NEWUTS CLONE_SIGHAND CLONE_SYSVSEM CLONE_THREAD CLONE_VM
:::

## File Object Creation {#os-newstreams}

These functions create new `file objects <file object>`{.interpreted-text role="term"}. (See also `~os.open`{.interpreted-text role="func"} for opening file descriptors.)

::: function
fdopen(fd, *args,*\*kwargs)

Return an open file object connected to the file descriptor *fd*. This is an alias of the `open`{.interpreted-text role="func"} built-in function and accepts the same arguments. The only difference is that the first argument of `fdopen`{.interpreted-text role="func"} must always be an integer.
:::

## File Descriptor Operations {#os-fd-ops}

These functions operate on I/O streams referenced using file descriptors.

File descriptors are small integers corresponding to a file that has been opened by the current process. For example, standard input is usually file descriptor 0, standard output is 1, and standard error is 2. Further files opened by a process will then be assigned 3, 4, 5, and so forth. The name \"file descriptor\" is slightly deceptive; on Unix platforms, sockets and pipes are also referenced by file descriptors.

The `~io.IOBase.fileno`{.interpreted-text role="meth"} method can be used to obtain the file descriptor associated with a `file object`{.interpreted-text role="term"} when required. Note that using the file descriptor directly will bypass the file object methods, ignoring aspects such as internal buffering of data.

::::: function
close(fd)

Close file descriptor *fd*.

:::: note
::: title
Note
:::

This function is intended for low-level I/O and must be applied to a file descriptor as returned by `os.open`{.interpreted-text role="func"} or `pipe`{.interpreted-text role="func"}. To close a \"file object\" returned by the built-in function `open`{.interpreted-text role="func"} or by `popen`{.interpreted-text role="func"} or `fdopen`{.interpreted-text role="func"}, use its `~io.IOBase.close`{.interpreted-text role="meth"} method.
::::
:::::

::: function
closerange(fd_low, fd_high, /)

Close all file descriptors from *fd_low* (inclusive) to *fd_high* (exclusive), ignoring errors. Equivalent to (but much faster than):

    for fd in range(fd_low, fd_high):
        try:
            os.close(fd)
        except OSError:
            pass
:::

::::::: function
copy_file_range(src, dst, count, offset_src=None, offset_dst=None)

Copy *count* bytes from file descriptor *src*, starting from offset *offset_src*, to file descriptor *dst*, starting from offset *offset_dst*. If *offset_src* is `None`, then *src* is read from the current position; respectively for *offset_dst*.

In Linux kernel older than 5.3, the files pointed to by *src* and *dst* must reside in the same filesystem, otherwise an `OSError`{.interpreted-text role="exc"} is raised with `~OSError.errno`{.interpreted-text role="attr"} set to `errno.EXDEV`{.interpreted-text role="const"}.

This copy is done without the additional cost of transferring data from the kernel to user space and then back into the kernel. Additionally, some filesystems could implement extra optimizations, such as the use of reflinks (i.e., two or more inodes that share pointers to the same copy-on-write disk blocks; supported file systems include btrfs and XFS) and server-side copy (in the case of NFS).

The function copies bytes between two file descriptors. Text options, like the encoding and the line ending, are ignored.

The return value is the amount of bytes copied. This could be less than the amount requested.

:::: note
::: title
Note
:::

On Linux, `os.copy_file_range`{.interpreted-text role="func"} should not be used for copying a range of a pseudo file from a special filesystem like procfs and sysfs. It will always copy no bytes and return 0 as if the file was empty because of a known Linux kernel issue.
::::

::: availability
Linux \>= 4.5 with glibc \>= 2.27.
:::

::: versionadded
3.8
:::
:::::::

:::: function
device_encoding(fd)

Return a string describing the encoding of the device associated with *fd* if it is connected to a terminal; else return `None`{.interpreted-text role="const"}.

On Unix, if the `Python UTF-8 Mode <utf8-mode>`{.interpreted-text role="ref"} is enabled, return `'UTF-8'` rather than the device encoding.

::: versionchanged
3.10 On Unix, the function now implements the Python UTF-8 Mode.
:::
::::

::::: function
dup(fd, /)

Return a duplicate of file descriptor *fd*. The new file descriptor is `non-inheritable <fd_inheritance>`{.interpreted-text role="ref"}.

On Windows, when duplicating a standard stream (0: stdin, 1: stdout, 2: stderr), the new file descriptor is `inheritable
<fd_inheritance>`{.interpreted-text role="ref"}.

::: availability
not WASI.
:::

::: versionchanged
3.4 The new file descriptor is now non-inheritable.
:::
:::::

:::::: function
dup2(fd, fd2, inheritable=True)

Duplicate file descriptor *fd* to *fd2*, closing the latter first if necessary. Return *fd2*. The new file descriptor is `inheritable
<fd_inheritance>`{.interpreted-text role="ref"} by default or non-inheritable if *inheritable* is `False`.

::: availability
not WASI.
:::

::: versionchanged
3.4 Add the optional *inheritable* parameter.
:::

::: versionchanged
3.7 Return *fd2* on success. Previously, `None` was always returned.
:::
::::::

:::::: function
fchmod(fd, mode)

Change the mode of the file given by *fd* to the numeric *mode*. See the docs for `chmod`{.interpreted-text role="func"} for possible values of *mode*. As of Python 3.3, this is equivalent to `os.chmod(fd, mode)`.

::: audit-event
os.chmod path,mode,dir_fd os.fchmod
:::

::: availability
Unix, Windows.

The function is limited on WASI, see `wasm-availability`{.interpreted-text role="ref"} for more information.
:::

::: versionchanged
3.13 Added support on Windows.
:::
::::::

::::: function
fchown(fd, uid, gid)

Change the owner and group id of the file given by *fd* to the numeric *uid* and *gid*. To leave one of the ids unchanged, set it to -1. See `chown`{.interpreted-text role="func"}. As of Python 3.3, this is equivalent to `os.chown(fd, uid, gid)`.

::: audit-event
os.chown path,uid,gid,dir_fd os.fchown
:::

::: availability
Unix.

The function is limited on WASI, see `wasm-availability`{.interpreted-text role="ref"} for more information.
:::
:::::

:::::: function
fdatasync(fd)

Force write of file with filedescriptor *fd* to disk. Does not force update of metadata.

::: availability
Unix.
:::

:::: note
::: title
Note
:::

This function is not available on MacOS.
::::
::::::

:::: function
fpathconf(fd, name, /)

Return system configuration information relevant to an open file. *name* specifies the configuration value to retrieve; it may be a string which is the name of a defined system value; these names are specified in a number of standards (POSIX.1, Unix 95, Unix 98, and others). Some platforms define additional names as well. The names known to the host operating system are given in the `pathconf_names` dictionary. For configuration variables not included in that mapping, passing an integer for *name* is also accepted.

If *name* is a string and is not known, `ValueError`{.interpreted-text role="exc"} is raised. If a specific value for *name* is not supported by the host system, even if it is included in `pathconf_names`, an `OSError`{.interpreted-text role="exc"} is raised with `errno.EINVAL`{.interpreted-text role="const"} for the error number.

As of Python 3.3, this is equivalent to `os.pathconf(fd, name)`.

::: availability
Unix.
:::
::::

:::: function
fstat(fd)

Get the status of the file descriptor *fd*. Return a `stat_result`{.interpreted-text role="class"} object.

As of Python 3.3, this is equivalent to `os.stat(fd)`.

::: seealso
The `.stat`{.interpreted-text role="func"} function.
:::
::::

:::: function
fstatvfs(fd, /)

Return information about the filesystem containing the file associated with file descriptor *fd*, like `statvfs`{.interpreted-text role="func"}. As of Python 3.3, this is equivalent to `os.statvfs(fd)`.

::: availability
Unix.
:::
::::

:::: function
fsync(fd)

Force write of file with filedescriptor *fd* to disk. On Unix, this calls the native `!fsync`{.interpreted-text role="c:func"} function; on Windows, the MS `!_commit`{.interpreted-text role="c:func"} function.

If you\'re starting with a buffered Python `file object`{.interpreted-text role="term"} *f*, first do `f.flush()`, and then do `os.fsync(f.fileno())`, to ensure that all internal buffers associated with *f* are written to disk.

::: availability
Unix, Windows.
:::
::::

:::::: function
ftruncate(fd, length, /)

Truncate the file corresponding to file descriptor *fd*, so that it is at most *length* bytes in size. As of Python 3.3, this is equivalent to `os.truncate(fd, length)`.

::: audit-event
os.truncate fd,length os.ftruncate
:::

::: availability
Unix, Windows.
:::

::: versionchanged
3.5 Added support for Windows
:::
::::::

:::::: function
get_blocking(fd, /)

Get the blocking mode of the file descriptor: `False` if the `O_NONBLOCK`{.interpreted-text role="data"} flag is set, `True` if the flag is cleared.

See also `set_blocking`{.interpreted-text role="func"} and `socket.socket.setblocking`{.interpreted-text role="meth"}.

::: availability
Unix, Windows.

The function is limited on WASI, see `wasm-availability`{.interpreted-text role="ref"} for more information.

On Windows, this function is limited to pipes.
:::

::: versionadded
3.5
:::

::: versionchanged
3.12 Added support for pipes on Windows.
:::
::::::

::::: function
grantpt(fd, /)

Grant access to the slave pseudo-terminal device associated with the master pseudo-terminal device to which the file descriptor *fd* refers. The file descriptor *fd* is not closed upon failure.

Calls the C standard library function `grantpt`{.interpreted-text role="c:func"}.

::: availability
Unix, not WASI.
:::

::: versionadded
3.13
:::
:::::

::: function
isatty(fd, /)

Return `True` if the file descriptor *fd* is open and connected to a tty(-like) device, else `False`.
:::

:::::: function
lockf(fd, cmd, len, /)

Apply, test or remove a POSIX lock on an open file descriptor. *fd* is an open file descriptor. *cmd* specifies the command to use - one of `F_LOCK`{.interpreted-text role="data"}, `F_TLOCK`{.interpreted-text role="data"}, `F_ULOCK`{.interpreted-text role="data"} or `F_TEST`{.interpreted-text role="data"}. *len* specifies the section of the file to lock.

::: audit-event
os.lockf fd,cmd,len os.lockf
:::

::: availability
Unix.
:::

::: versionadded
3.3
:::
::::::

::::: data
F_LOCK F_TLOCK F_ULOCK F_TEST

Flags that specify what action `lockf`{.interpreted-text role="func"} will take.

::: availability
Unix.
:::

::: versionadded
3.3
:::
:::::

::::: function
login_tty(fd, /)

Prepare the tty of which fd is a file descriptor for a new login session. Make the calling process a session leader; make the tty the controlling tty, the stdin, the stdout, and the stderr of the calling process; close fd.

::: availability
Unix, not WASI.
:::

::: versionadded
3.11
:::
:::::

:::: function
lseek(fd, pos, whence, /)

Set the current position of file descriptor *fd* to position *pos*, modified by *whence*, and return the new position in bytes relative to the start of the file. Valid values for *whence* are:

- `SEEK_SET`{.interpreted-text role="const"} or `0` \-- set *pos* relative to the beginning of the file
- `SEEK_CUR`{.interpreted-text role="const"} or `1` \-- set *pos* relative to the current file position
- `SEEK_END`{.interpreted-text role="const"} or `2` \-- set *pos* relative to the end of the file
- `SEEK_HOLE`{.interpreted-text role="const"} \-- set *pos* to the next data location, relative to *pos*
- `SEEK_DATA`{.interpreted-text role="const"} \-- set *pos* to the next data hole, relative to *pos*

::: versionchanged
3.3

Add support for `!SEEK_HOLE`{.interpreted-text role="const"} and `!SEEK_DATA`{.interpreted-text role="const"}.
:::
::::

::: data
SEEK_SET SEEK_CUR SEEK_END

Parameters to the `lseek`{.interpreted-text role="func"} function and the `~io.IOBase.seek`{.interpreted-text role="meth"} method on `file-like objects <file object>`{.interpreted-text role="term"}, for whence to adjust the file position indicator.

`SEEK_SET`{.interpreted-text role="const"}

:   Adjust the file position relative to the beginning of the file.

`SEEK_CUR`{.interpreted-text role="const"}

:   Adjust the file position relative to the current file position.

`SEEK_END`{.interpreted-text role="const"}

:   Adjust the file position relative to the end of the file.

Their values are 0, 1, and 2, respectively.
:::

::::::: data
SEEK_HOLE SEEK_DATA

Parameters to the `lseek`{.interpreted-text role="func"} function and the `~io.IOBase.seek`{.interpreted-text role="meth"} method on `file-like objects <file object>`{.interpreted-text role="term"}, for seeking file data and holes on sparsely allocated files.

`!SEEK_DATA`{.interpreted-text role="data"}

:   Adjust the file offset to the next location containing data, relative to the seek position.

`!SEEK_HOLE`{.interpreted-text role="data"}

:   Adjust the file offset to the next location containing a hole, relative to the seek position. A hole is defined as a sequence of zeros.

:::: note
::: title
Note
:::

These operations only make sense for filesystems that support them.
::::

::: availability
Linux \>= 3.1, macOS, Unix
:::

::: versionadded
3.3
:::
:::::::

:::::::::: function
open(path, flags, mode=0o777, \*, dir_fd=None)

Open the file *path* and set various flags according to *flags* and possibly its mode according to *mode*. When computing *mode*, the current umask value is first masked out. Return the file descriptor for the newly opened file. The new file descriptor is `non-inheritable <fd_inheritance>`{.interpreted-text role="ref"}.

For a description of the flag and mode values, see the C run-time documentation; flag constants (like `O_RDONLY`{.interpreted-text role="const"} and `O_WRONLY`{.interpreted-text role="const"}) are defined in the `!os`{.interpreted-text role="mod"} module. In particular, on Windows adding `O_BINARY`{.interpreted-text role="const"} is needed to open files in binary mode.

This function can support `paths relative to directory descriptors
<dir_fd>`{.interpreted-text role="ref"} with the *dir_fd* parameter.

::: audit-event
open path,mode,flags os.open
:::

::: versionchanged
3.4 The new file descriptor is now non-inheritable.
:::

:::: note
::: title
Note
:::

This function is intended for low-level I/O. For normal usage, use the built-in function `open`{.interpreted-text role="func"}, which returns a `file object`{.interpreted-text role="term"} with `~file.read`{.interpreted-text role="meth"} and `~file.write`{.interpreted-text role="meth"} methods (and many more). To wrap a file descriptor in a file object, use `fdopen`{.interpreted-text role="func"}.
::::

::: versionchanged
3.3 Added the *dir_fd* parameter.
:::

::: versionchanged
3.5 If the system call is interrupted and the signal handler does not raise an exception, the function now retries the system call instead of raising an `InterruptedError`{.interpreted-text role="exc"} exception (see `475`{.interpreted-text role="pep"} for the rationale).
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"}.
:::
::::::::::

The following constants are options for the *flags* parameter to the `~os.open`{.interpreted-text role="func"} function. They can be combined using the bitwise OR operator `|`. Some of them are not available on all platforms. For descriptions of their availability and use, consult the `open(2)`{.interpreted-text role="manpage"} manual page on Unix or [the MSDN](https://msdn.microsoft.com/en-us/library/z0kc8e3z.aspx) on Windows.

::: data
O_RDONLY O_WRONLY O_RDWR O_APPEND O_CREAT O_EXCL O_TRUNC

The above constants are available on Unix and Windows.
:::

:::: data
O_DSYNC O_RSYNC O_SYNC O_NDELAY O_NONBLOCK O_NOCTTY O_CLOEXEC

The above constants are only available on Unix.

::: versionchanged
3.3 Add `O_CLOEXEC`{.interpreted-text role="data"} constant.
:::
::::

::: data
O_BINARY O_NOINHERIT O_SHORT_LIVED O_TEMPORARY O_RANDOM O_SEQUENTIAL O_TEXT

The above constants are only available on Windows.
:::

:::: data
O_EVTONLY O_FSYNC O_SYMLINK O_NOFOLLOW_ANY

The above constants are only available on macOS.

::: versionchanged
3.10 Add `O_EVTONLY`{.interpreted-text role="data"}, `O_FSYNC`{.interpreted-text role="data"}, `O_SYMLINK`{.interpreted-text role="data"} and `O_NOFOLLOW_ANY`{.interpreted-text role="data"} constants.
:::
::::

:::: data
O_ASYNC O_DIRECT O_DIRECTORY O_NOFOLLOW O_NOATIME O_PATH O_TMPFILE O_SHLOCK O_EXLOCK

The above constants are extensions and not present if they are not defined by the C library.

::: versionchanged
3.4 Add `O_PATH`{.interpreted-text role="data"} on systems that support it. Add `O_TMPFILE`{.interpreted-text role="data"}, only available on Linux Kernel 3.11 or newer.
:::
::::

:::::: function
openpty()

::: index
pair: module; pty
:::

Open a new pseudo-terminal pair. Return a pair of file descriptors `(master, slave)` for the pty and the tty, respectively. The new file descriptors are `non-inheritable <fd_inheritance>`{.interpreted-text role="ref"}. For a (slightly) more portable approach, use the `pty`{.interpreted-text role="mod"} module.

::: availability
Unix, not WASI.
:::

::: versionchanged
3.4 The new file descriptors are now non-inheritable.
:::
::::::

::::: function
pipe()

Create a pipe. Return a pair of file descriptors `(r, w)` usable for reading and writing, respectively. The new file descriptor is `non-inheritable <fd_inheritance>`{.interpreted-text role="ref"}.

::: availability
Unix, Windows.
:::

::: versionchanged
3.4 The new file descriptors are now non-inheritable.
:::
:::::

::::: function
pipe2(flags, /)

Create a pipe with *flags* set atomically. *flags* can be constructed by ORing together one or more of these values: `O_NONBLOCK`{.interpreted-text role="data"}, `O_CLOEXEC`{.interpreted-text role="data"}. Return a pair of file descriptors `(r, w)` usable for reading and writing, respectively.

::: availability
Unix, not WASI.
:::

::: versionadded
3.3
:::
:::::

::::: function
posix_fallocate(fd, offset, len, /)

Ensures that enough disk space is allocated for the file specified by *fd* starting from *offset* and continuing for *len* bytes.

::: availability
Unix.
:::

::: versionadded
3.3
:::
:::::

::::: function
posix_fadvise(fd, offset, len, advice, /)

Announces an intention to access data in a specific pattern thus allowing the kernel to make optimizations. The advice applies to the region of the file specified by *fd* starting at *offset* and continuing for *len* bytes. *advice* is one of `POSIX_FADV_NORMAL`{.interpreted-text role="data"}, `POSIX_FADV_SEQUENTIAL`{.interpreted-text role="data"}, `POSIX_FADV_RANDOM`{.interpreted-text role="data"}, `POSIX_FADV_NOREUSE`{.interpreted-text role="data"}, `POSIX_FADV_WILLNEED`{.interpreted-text role="data"} or `POSIX_FADV_DONTNEED`{.interpreted-text role="data"}.

::: availability
Unix.
:::

::: versionadded
3.3
:::
:::::

::::: data
POSIX_FADV_NORMAL POSIX_FADV_SEQUENTIAL POSIX_FADV_RANDOM POSIX_FADV_NOREUSE POSIX_FADV_WILLNEED POSIX_FADV_DONTNEED

Flags that can be used in *advice* in `posix_fadvise`{.interpreted-text role="func"} that specify the access pattern that is likely to be used.

::: availability
Unix.
:::

::: versionadded
3.3
:::
:::::

::::: function
pread(fd, n, offset, /)

Read at most *n* bytes from file descriptor *fd* at a position of *offset*, leaving the file offset unchanged.

Return a bytestring containing the bytes read. If the end of the file referred to by *fd* has been reached, an empty bytes object is returned.

::: availability
Unix.
:::

::: versionadded
3.3
:::
:::::

::::: function
posix_openpt(oflag, /)

Open and return a file descriptor for a master pseudo-terminal device.

Calls the C standard library function `posix_openpt`{.interpreted-text role="c:func"}. The *oflag* argument is used to set file status flags and file access modes as specified in the manual page of `posix_openpt`{.interpreted-text role="c:func"} of your system.

The returned file descriptor is `non-inheritable <fd_inheritance>`{.interpreted-text role="ref"}. If the value `O_CLOEXEC`{.interpreted-text role="data"} is available on the system, it is added to *oflag*.

::: availability
Unix, not WASI.
:::

::: versionadded
3.13
:::
:::::

::::: function
preadv(fd, buffers, offset, flags=0, /)

Read from a file descriptor *fd* at a position of *offset* into mutable `bytes-like objects <bytes-like object>`{.interpreted-text role="term"} *buffers*, leaving the file offset unchanged. Transfer data into each buffer until it is full and then move on to the next buffer in the sequence to hold the rest of the data.

The flags argument contains a bitwise OR of zero or more of the following flags:

- `RWF_HIPRI`{.interpreted-text role="data"}
- `RWF_NOWAIT`{.interpreted-text role="data"}
- `RWF_DONTCACHE`{.interpreted-text role="data"}

Return the total number of bytes actually read which can be less than the total capacity of all the objects.

The operating system may set a limit (`sysconf`{.interpreted-text role="func"} value `'SC_IOV_MAX'`) on the number of buffers that can be used.

Combine the functionality of `os.readv`{.interpreted-text role="func"} and `os.pread`{.interpreted-text role="func"}.

::: availability
Linux \>= 2.6.30, FreeBSD \>= 6.0, OpenBSD \>= 2.7, AIX \>= 7.1.

Using flags requires Linux \>= 4.6.
:::

::: versionadded
3.7
:::
:::::

::::: data
RWF_NOWAIT

Do not wait for data which is not immediately available. If this flag is specified, the system call will return instantly if it would have to read data from the backing storage or wait for a lock.

If some data was successfully read, it will return the number of bytes read. If no bytes were read, it will return `-1` and set errno to `errno.EAGAIN`{.interpreted-text role="const"}.

::: availability
Linux \>= 4.14.
:::

::: versionadded
3.7
:::
:::::

::::: data
RWF_HIPRI

High priority read/write. Allows block-based filesystems to use polling of the device, which provides lower latency, but may use additional resources.

Currently, on Linux, this feature is usable only on a file descriptor opened using the `O_DIRECT`{.interpreted-text role="data"} flag.

::: availability
Linux \>= 4.6.
:::

::: versionadded
3.7
:::
:::::

::::: data
RWF_DONTCACHE

Use uncached buffered IO.

::: availability
Linux \>= 6.14
:::

::: versionadded
3.15
:::
:::::

::::: data
RWF_ATOMIC

Write data atomically. Requires alignment to the device\'s atomic write unit.

::: availability
Linux \>= 6.11
:::

::: versionadded
3.15
:::
:::::

::::: function
ptsname(fd, /)

Return the name of the slave pseudo-terminal device associated with the master pseudo-terminal device to which the file descriptor *fd* refers. The file descriptor *fd* is not closed upon failure.

Calls the reentrant C standard library function `ptsname_r`{.interpreted-text role="c:func"} if it is available; otherwise, the C standard library function `ptsname`{.interpreted-text role="c:func"}, which is not guaranteed to be thread-safe, is called.

::: availability
Unix, not WASI.
:::

::: versionadded
3.13
:::
:::::

::::: function
pwrite(fd, str, offset, /)

Write the bytestring in *str* to file descriptor *fd* at position of *offset*, leaving the file offset unchanged.

Return the number of bytes actually written.

::: availability
Unix.
:::

::: versionadded
3.3
:::
:::::

::::: function
pwritev(fd, buffers, offset, flags=0, /)

Write the *buffers* contents to file descriptor *fd* at an offset *offset*, leaving the file offset unchanged. *buffers* must be a sequence of `bytes-like objects <bytes-like object>`{.interpreted-text role="term"}. Buffers are processed in array order. Entire contents of the first buffer is written before proceeding to the second, and so on.

The flags argument contains a bitwise OR of zero or more of the following flags:

- `RWF_DSYNC`{.interpreted-text role="data"}
- `RWF_SYNC`{.interpreted-text role="data"}
- `RWF_APPEND`{.interpreted-text role="data"}
- `RWF_DONTCACHE`{.interpreted-text role="data"}
- `RWF_ATOMIC`{.interpreted-text role="data"}

Return the total number of bytes actually written.

The operating system may set a limit (`sysconf`{.interpreted-text role="func"} value `'SC_IOV_MAX'`) on the number of buffers that can be used.

Combine the functionality of `os.writev`{.interpreted-text role="func"} and `os.pwrite`{.interpreted-text role="func"}.

::: availability
Linux \>= 2.6.30, FreeBSD \>= 6.0, OpenBSD \>= 2.7, AIX \>= 7.1.

Using flags requires Linux \>= 4.6.
:::

::: versionadded
3.7
:::
:::::

::::: data
RWF_DSYNC

Provide a per-write equivalent of the `O_DSYNC`{.interpreted-text role="data"} `os.open`{.interpreted-text role="func"} flag. This flag effect applies only to the data range written by the system call.

::: availability
Linux \>= 4.7.
:::

::: versionadded
3.7
:::
:::::

::::: data
RWF_SYNC

Provide a per-write equivalent of the `O_SYNC`{.interpreted-text role="data"} `os.open`{.interpreted-text role="func"} flag. This flag effect applies only to the data range written by the system call.

::: availability
Linux \>= 4.7.
:::

::: versionadded
3.7
:::
:::::

::::: data
RWF_APPEND

Provide a per-write equivalent of the `O_APPEND`{.interpreted-text role="data"} `os.open`{.interpreted-text role="func"} flag. This flag is meaningful only for `os.pwritev`{.interpreted-text role="func"}, and its effect applies only to the data range written by the system call. The *offset* argument does not affect the write operation; the data is always appended to the end of the file. However, if the *offset* argument is `-1`, the current file *offset* is updated.

::: availability
Linux \>= 4.16.
:::

::: versionadded
3.10
:::
:::::

:::::: function
read(fd, n, /)

Read at most *n* bytes from file descriptor *fd*.

Return a bytestring containing the bytes read. If the end of the file referred to by *fd* has been reached, an empty bytes object is returned.

:::: note
::: title
Note
:::

This function is intended for low-level I/O and must be applied to a file descriptor as returned by `os.open`{.interpreted-text role="func"} or `pipe`{.interpreted-text role="func"}. To read a \"file object\" returned by the built-in function `open`{.interpreted-text role="func"} or by `popen`{.interpreted-text role="func"} or `fdopen`{.interpreted-text role="func"}, or `sys.stdin`{.interpreted-text role="data"}, use its `~file.read`{.interpreted-text role="meth"} or `~file.readline`{.interpreted-text role="meth"} methods.
::::

::: versionchanged
3.5 If the system call is interrupted and the signal handler does not raise an exception, the function now retries the system call instead of raising an `InterruptedError`{.interpreted-text role="exc"} exception (see `475`{.interpreted-text role="pep"} for the rationale).
:::
::::::

:::::: function
readinto(fd, buffer, /)

Read from a file descriptor *fd* into a mutable `buffer object <bufferobjects>`{.interpreted-text role="ref"} *buffer*.

The *buffer* should be mutable and `bytes-like <bytes-like object>`{.interpreted-text role="term"}. On success, returns the number of bytes read. Less bytes may be read than the size of the buffer. The underlying system call will be retried when interrupted by a signal, unless the signal handler raises an exception. Other errors will not be retried and an error will be raised.

Returns 0 if *fd* is at end of file or if the provided *buffer* has length 0 (which can be used to check for errors without reading data). Never returns negative.

:::: note
::: title
Note
:::

This function is intended for low-level I/O and must be applied to a file descriptor as returned by `os.open`{.interpreted-text role="func"} or `os.pipe`{.interpreted-text role="func"}. To read a \"file object\" returned by the built-in function `open`{.interpreted-text role="func"}, or `sys.stdin`{.interpreted-text role="data"}, use its member functions, for example `io.BufferedIOBase.readinto`{.interpreted-text role="meth"}, `io.BufferedIOBase.read`{.interpreted-text role="meth"}, or `io.TextIOBase.read`{.interpreted-text role="meth"}
::::

::: versionadded
3.14
:::
::::::

:::::::: function
sendfile(out_fd, in_fd, offset, count) sendfile(out_fd, in_fd, offset, count, headers=(), trailers=(), flags=0)

Copy *count* bytes from file descriptor *in_fd* to file descriptor *out_fd* starting at *offset*. Return the number of bytes sent. When EOF is reached return `0`.

The first function notation is supported by all platforms that define `sendfile`{.interpreted-text role="func"}.

On Linux, if *offset* is given as `None`, the bytes are read from the current position of *in_fd* and the position of *in_fd* is updated.

The second case may be used on macOS and FreeBSD where *headers* and *trailers* are arbitrary sequences of buffers that are written before and after the data from *in_fd* is written. It returns the same as the first case.

On macOS and FreeBSD, a value of `0` for *count* specifies to send until the end of *in_fd* is reached.

All platforms support sockets as *out_fd* file descriptor, and some platforms allow other types (e.g. regular file, pipe) as well.

Cross-platform applications should not use *headers*, *trailers* and *flags* arguments.

::: availability
Unix, not WASI.
:::

:::: note
::: title
Note
:::

For a higher-level wrapper of `sendfile`{.interpreted-text role="func"}, see `socket.socket.sendfile`{.interpreted-text role="meth"}.
::::

::: versionadded
3.3
:::

::: versionchanged
3.9 Parameters *out* and *in* was renamed to *out_fd* and *in_fd*.
:::
::::::::

::::: data
SF_NODISKIO SF_MNOWAIT SF_SYNC

Parameters to the `sendfile`{.interpreted-text role="func"} function, if the implementation supports them.

::: availability
Unix, not WASI.
:::

::: versionadded
3.3
:::
:::::

::::: data
SF_NOCACHE

Parameter to the `sendfile`{.interpreted-text role="func"} function, if the implementation supports it. The data won\'t be cached in the virtual memory and will be freed afterwards.

::: availability
Unix, not WASI.
:::

::: versionadded
3.11
:::
:::::

:::::: function
set_blocking(fd, blocking, /)

Set the blocking mode of the specified file descriptor. Set the `O_NONBLOCK`{.interpreted-text role="data"} flag if blocking is `False`, clear the flag otherwise.

See also `get_blocking`{.interpreted-text role="func"} and `socket.socket.setblocking`{.interpreted-text role="meth"}.

::: availability
Unix, Windows.

The function is limited on WASI, see `wasm-availability`{.interpreted-text role="ref"} for more information.

On Windows, this function is limited to pipes.
:::

::: versionadded
3.5
:::

::: versionchanged
3.12 Added support for pipes on Windows.
:::
::::::

:::::: function
splice(src, dst, count, offset_src=None, offset_dst=None, flags=0)

Transfer *count* bytes from file descriptor *src*, starting from offset *offset_src*, to file descriptor *dst*, starting from offset *offset_dst*.

The splicing behaviour can be modified by specifying a *flags* value. Any of the following variables may used, combined using bitwise OR (the `|` operator):

- If `SPLICE_F_MOVE`{.interpreted-text role="const"} is specified, the kernel is asked to move pages instead of copying, but pages may still be copied if the kernel cannot move the pages from the pipe.
- If `SPLICE_F_NONBLOCK`{.interpreted-text role="const"} is specified, the kernel is asked to not block on I/O. This makes the splice pipe operations nonblocking, but splice may nevertheless block because the spliced file descriptors may block.
- If `SPLICE_F_MORE`{.interpreted-text role="const"} is specified, it hints to the kernel that more data will be coming in a subsequent splice.

At least one of the file descriptors must refer to a pipe. If *offset_src* is `None`, then *src* is read from the current position; respectively for *offset_dst*. The offset associated to the file descriptor that refers to a pipe must be `None`. The files pointed to by *src* and *dst* must reside in the same filesystem, otherwise an `OSError`{.interpreted-text role="exc"} is raised with `~OSError.errno`{.interpreted-text role="attr"} set to `errno.EXDEV`{.interpreted-text role="const"}.

This copy is done without the additional cost of transferring data from the kernel to user space and then back into the kernel. Additionally, some filesystems could implement extra optimizations. The copy is done as if both files are opened as binary.

Upon successful completion, returns the number of bytes spliced to or from the pipe. A return value of 0 means end of input. If *src* refers to a pipe, then this means that there was no data to transfer, and it would not make sense to block because there are no writers connected to the write end of the pipe.

::: seealso
The `splice(2)`{.interpreted-text role="manpage"} man page.
:::

::: availability
Linux \>= 2.6.17 with glibc \>= 2.5
:::

::: versionadded
3.10
:::
::::::

:::: data
SPLICE_F_MOVE SPLICE_F_NONBLOCK SPLICE_F_MORE

::: versionadded
3.10
:::
::::

::::: function
readv(fd, buffers, /)

Read from a file descriptor *fd* into a number of mutable `bytes-like
objects <bytes-like object>`{.interpreted-text role="term"} *buffers*. Transfer data into each buffer until it is full and then move on to the next buffer in the sequence to hold the rest of the data.

Return the total number of bytes actually read which can be less than the total capacity of all the objects.

The operating system may set a limit (`sysconf`{.interpreted-text role="func"} value `'SC_IOV_MAX'`) on the number of buffers that can be used.

::: availability
Unix.
:::

::: versionadded
3.3
:::
:::::

:::: function
tcgetpgrp(fd, /)

Return the process group associated with the terminal given by *fd* (an open file descriptor as returned by `os.open`{.interpreted-text role="func"}).

::: availability
Unix, not WASI.
:::
::::

:::: function
tcsetpgrp(fd, pg, /)

Set the process group associated with the terminal given by *fd* (an open file descriptor as returned by `os.open`{.interpreted-text role="func"}) to *pg*.

::: availability
Unix, not WASI.
:::
::::

:::: function
ttyname(fd, /)

Return a string which specifies the terminal device associated with file descriptor *fd*. If *fd* is not associated with a terminal device, an exception is raised.

::: availability
Unix.
:::
::::

::::: function
unlockpt(fd, /)

Unlock the slave pseudo-terminal device associated with the master pseudo-terminal device to which the file descriptor *fd* refers. The file descriptor *fd* is not closed upon failure.

Calls the C standard library function `unlockpt`{.interpreted-text role="c:func"}.

::: availability
Unix, not WASI.
:::

::: versionadded
3.13
:::
:::::

:::::: function
write(fd, str, /)

Write the bytestring in *str* to file descriptor *fd*.

Return the number of bytes actually written.

:::: note
::: title
Note
:::

This function is intended for low-level I/O and must be applied to a file descriptor as returned by `os.open`{.interpreted-text role="func"} or `pipe`{.interpreted-text role="func"}. To write a \"file object\" returned by the built-in function `open`{.interpreted-text role="func"} or by `popen`{.interpreted-text role="func"} or `fdopen`{.interpreted-text role="func"}, or `sys.stdout`{.interpreted-text role="data"} or `sys.stderr`{.interpreted-text role="data"}, use its `~file.write`{.interpreted-text role="meth"} method.
::::

::: versionchanged
3.5 If the system call is interrupted and the signal handler does not raise an exception, the function now retries the system call instead of raising an `InterruptedError`{.interpreted-text role="exc"} exception (see `475`{.interpreted-text role="pep"} for the rationale).
:::
::::::

::::: function
writev(fd, buffers, /)

Write the contents of *buffers* to file descriptor *fd*. *buffers* must be a sequence of `bytes-like objects <bytes-like object>`{.interpreted-text role="term"}. Buffers are processed in array order. Entire contents of the first buffer is written before proceeding to the second, and so on.

Returns the total number of bytes actually written.

The operating system may set a limit (`sysconf`{.interpreted-text role="func"} value `'SC_IOV_MAX'`) on the number of buffers that can be used.

::: availability
Unix.
:::

::: versionadded
3.3
:::
:::::

### Querying the size of a terminal {#terminal-size}

::: versionadded
3.3
:::

:::: function
get_terminal_size(fd=STDOUT_FILENO, /)

Return the size of the terminal window as `(columns, lines)`, tuple of type `terminal_size`{.interpreted-text role="class"}.

The optional argument `fd` (default `STDOUT_FILENO`, or standard output) specifies which file descriptor should be queried.

If the file descriptor is not connected to a terminal, an `OSError`{.interpreted-text role="exc"} is raised.

`shutil.get_terminal_size`{.interpreted-text role="func"} is the high-level function which should normally be used, `os.get_terminal_size` is the low-level implementation.

::: availability
Unix, Windows.
:::
::::

::::: terminal_size
A subclass of tuple, holding `(columns, lines)` of the terminal window size.

::: attribute
columns

Width of the terminal window in characters.
:::

::: attribute
lines

Height of the terminal window in characters.
:::
:::::

### Inheritance of File Descriptors {#fd_inheritance}

::: versionadded
3.4
:::

A file descriptor has an \"inheritable\" flag which indicates if the file descriptor can be inherited by child processes. Since Python 3.4, file descriptors created by Python are non-inheritable by default.

On UNIX, non-inheritable file descriptors are closed in child processes at the execution of a new program, other file descriptors are inherited. Note that non-inheritable file descriptors are still *inherited* by child processes on `os.fork`{.interpreted-text role="func"}.

On Windows, non-inheritable handles and file descriptors are closed in child processes, except for standard streams (file descriptors 0, 1 and 2: stdin, stdout and stderr), which are always inherited. Using `spawn\* <spawnl>`{.interpreted-text role="func"} functions, all inheritable handles and all inheritable file descriptors are inherited. Using the `subprocess`{.interpreted-text role="mod"} module, all file descriptors except standard streams are closed, and inheritable handles are only inherited if the *close_fds* parameter is `False`.

On WebAssembly platforms, the file descriptor cannot be modified.

::: function
get_inheritable(fd, /)

Get the \"inheritable\" flag of the specified file descriptor (a boolean).
:::

::: function
set_inheritable(fd, inheritable, /)

Set the \"inheritable\" flag of the specified file descriptor.
:::

:::: function
get_handle_inheritable(handle, /)

Get the \"inheritable\" flag of the specified handle (a boolean).

::: availability
Windows.
:::
::::

:::: function
set_handle_inheritable(handle, inheritable, /)

Set the \"inheritable\" flag of the specified handle.

::: availability
Windows.
:::
::::

## Files and Directories {#os-file-dir}

On some Unix platforms, many of these functions support one or more of these features:

::: {#path_fd}
- **specifying a file descriptor:** Normally the *path* argument provided to functions in the `!os`{.interpreted-text role="mod"} module must be a string specifying a file path. However, some functions now alternatively accept an open file descriptor for their *path* argument. The function will then operate on the file referred to by the descriptor. For POSIX systems, Python will call the variant of the function prefixed with `f` (e.g. call `fchdir` instead of `chdir`).

  You can check whether or not *path* can be specified as a file descriptor for a particular function on your platform using `os.supports_fd`{.interpreted-text role="data"}. If this functionality is unavailable, using it will raise a `NotImplementedError`{.interpreted-text role="exc"}.

  If the function also supports *dir_fd* or *follow_symlinks* arguments, it\'s an error to specify one of those when supplying *path* as a file descriptor.
:::

::: {#dir_fd}
- **paths relative to directory descriptors:** If *dir_fd* is not `None`, it should be a file descriptor referring to a directory, and the path to operate on should be relative; path will then be relative to that directory. If the path is absolute, *dir_fd* is ignored. For POSIX systems, Python will call the variant of the function with an `at` suffix and possibly prefixed with `f` (e.g. call `faccessat` instead of `access`).

  You can check whether or not *dir_fd* is supported for a particular function on your platform using `os.supports_dir_fd`{.interpreted-text role="data"}. If it\'s unavailable, using it will raise a `NotImplementedError`{.interpreted-text role="exc"}.
:::

::: {#follow_symlinks}
- **not following symlinks:** If *follow_symlinks* is `False`, and the last element of the path to operate on is a symbolic link, the function will operate on the symbolic link itself rather than the file pointed to by the link. For POSIX systems, Python will call the `l...` variant of the function.

  You can check whether or not *follow_symlinks* is supported for a particular function on your platform using `os.supports_follow_symlinks`{.interpreted-text role="data"}. If it\'s unavailable, using it will raise a `NotImplementedError`{.interpreted-text role="exc"}.
:::

::::::::: function
access(path, mode, \*, dir_fd=None, effective_ids=False, follow_symlinks=True)

Use the real uid/gid to test for access to *path*. Note that most operations will use the effective uid/gid, therefore this routine can be used in a suid/sgid environment to test if the invoking user has the specified access to *path*. *mode* should be `F_OK`{.interpreted-text role="const"} to test the existence of *path*, or it can be the inclusive OR of one or more of `R_OK`{.interpreted-text role="const"}, `W_OK`{.interpreted-text role="const"}, and `X_OK`{.interpreted-text role="const"} to test permissions. Return `True`{.interpreted-text role="const"} if access is allowed, `False`{.interpreted-text role="const"} if not. See the Unix man page `access(2)`{.interpreted-text role="manpage"} for more information.

This function can support specifying `paths relative to directory
descriptors <dir_fd>`{.interpreted-text role="ref"} and `not following symlinks <follow_symlinks>`{.interpreted-text role="ref"}.

If *effective_ids* is `True`, `access`{.interpreted-text role="func"} will perform its access checks using the effective uid/gid instead of the real uid/gid. *effective_ids* may not be supported on your platform; you can check whether or not it is available using `os.supports_effective_ids`{.interpreted-text role="data"}. If it is unavailable, using it will raise a `NotImplementedError`{.interpreted-text role="exc"}.

:::: note
::: title
Note
:::

Using `access`{.interpreted-text role="func"} to check if a user is authorized to e.g. open a file before actually doing so using `open`{.interpreted-text role="func"} creates a security hole, because the user might exploit the short time interval between checking and opening the file to manipulate it. It\'s preferable to use `EAFP`{.interpreted-text role="term"} techniques. For example:

    if os.access("myfile", os.R_OK):
        with open("myfile") as fp:
            return fp.read()
    return "some default data"

is better written as:

    try:
        fp = open("myfile")
    except PermissionError:
        return "some default data"
    else:
        with fp:
            return fp.read()
::::

:::: note
::: title
Note
:::

I/O operations may fail even when `access`{.interpreted-text role="func"} indicates that they would succeed, particularly for operations on network filesystems which may have permissions semantics beyond the usual POSIX permission-bit model.
::::

::: versionchanged
3.3 Added the *dir_fd*, *effective_ids*, and *follow_symlinks* parameters.
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"}.
:::
:::::::::

::: data
F_OK R_OK W_OK X_OK

Values to pass as the *mode* parameter of `access`{.interpreted-text role="func"} to test the existence, readability, writability and executability of *path*, respectively.
:::

::::::: function
chdir(path)

::: index
single: directory; changing
:::

Change the current working directory to *path*.

This function can support `specifying a file descriptor <path_fd>`{.interpreted-text role="ref"}. The descriptor must refer to an opened directory, not an open file.

This function can raise `OSError`{.interpreted-text role="exc"} and subclasses such as `FileNotFoundError`{.interpreted-text role="exc"}, `PermissionError`{.interpreted-text role="exc"}, and `NotADirectoryError`{.interpreted-text role="exc"}.

::: audit-event
os.chdir path os.chdir
:::

::: versionchanged
3.3 Added support for specifying *path* as a file descriptor on some platforms.
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"}.
:::
:::::::

::::::: function
chflags(path, flags, \*, follow_symlinks=True)

Set the flags of *path* to the numeric *flags*. *flags* may take a combination (bitwise OR) of the following values (as defined in the `stat`{.interpreted-text role="mod"} module):

- `stat.UF_NODUMP`{.interpreted-text role="const"}
- `stat.UF_IMMUTABLE`{.interpreted-text role="const"}
- `stat.UF_APPEND`{.interpreted-text role="const"}
- `stat.UF_OPAQUE`{.interpreted-text role="const"}
- `stat.UF_NOUNLINK`{.interpreted-text role="const"}
- `stat.UF_COMPRESSED`{.interpreted-text role="const"}
- `stat.UF_HIDDEN`{.interpreted-text role="const"}
- `stat.SF_ARCHIVED`{.interpreted-text role="const"}
- `stat.SF_IMMUTABLE`{.interpreted-text role="const"}
- `stat.SF_APPEND`{.interpreted-text role="const"}
- `stat.SF_NOUNLINK`{.interpreted-text role="const"}
- `stat.SF_SNAPSHOT`{.interpreted-text role="const"}

This function can support `not following symlinks <follow_symlinks>`{.interpreted-text role="ref"}.

::: audit-event
os.chflags path,flags os.chflags
:::

::: availability
Unix, not WASI.
:::

::: versionchanged
3.3 Added the *follow_symlinks* parameter.
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"}.
:::
:::::::

::::::::: function
chmod(path, mode, \*, dir_fd=None, follow_symlinks=True)

Change the mode of *path* to the numeric *mode*. *mode* may take one of the following values (as defined in the `stat`{.interpreted-text role="mod"} module) or bitwise ORed combinations of them:

- `stat.S_ISUID`{.interpreted-text role="const"}
- `stat.S_ISGID`{.interpreted-text role="const"}
- `stat.S_ENFMT`{.interpreted-text role="const"}
- `stat.S_ISVTX`{.interpreted-text role="const"}
- `stat.S_IREAD`{.interpreted-text role="const"}
- `stat.S_IWRITE`{.interpreted-text role="const"}
- `stat.S_IEXEC`{.interpreted-text role="const"}
- `stat.S_IRWXU`{.interpreted-text role="const"}
- `stat.S_IRUSR`{.interpreted-text role="const"}
- `stat.S_IWUSR`{.interpreted-text role="const"}
- `stat.S_IXUSR`{.interpreted-text role="const"}
- `stat.S_IRWXG`{.interpreted-text role="const"}
- `stat.S_IRGRP`{.interpreted-text role="const"}
- `stat.S_IWGRP`{.interpreted-text role="const"}
- `stat.S_IXGRP`{.interpreted-text role="const"}
- `stat.S_IRWXO`{.interpreted-text role="const"}
- `stat.S_IROTH`{.interpreted-text role="const"}
- `stat.S_IWOTH`{.interpreted-text role="const"}
- `stat.S_IXOTH`{.interpreted-text role="const"}

This function can support `specifying a file descriptor <path_fd>`{.interpreted-text role="ref"}, `paths relative to directory descriptors <dir_fd>`{.interpreted-text role="ref"} and `not
following symlinks <follow_symlinks>`{.interpreted-text role="ref"}.

:::: note
::: title
Note
:::

Although Windows supports `chmod`{.interpreted-text role="func"}, you can only set the file\'s read-only flag with it (via the `stat.S_IWRITE` and `stat.S_IREAD` constants or a corresponding integer value). All other bits are ignored. The default value of *follow_symlinks* is `False` on Windows.

The function is limited on WASI, see `wasm-availability`{.interpreted-text role="ref"} for more information.
::::

::: audit-event
os.chmod path,mode,dir_fd os.chmod
:::

::: versionchanged
3.3 Added support for specifying *path* as an open file descriptor, and the *dir_fd* and *follow_symlinks* arguments.
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"}.
:::

::: versionchanged
3.13 Added support for a file descriptor and the *follow_symlinks* argument on Windows.
:::
:::::::::

::::::: function
chown(path, uid, gid, \*, dir_fd=None, follow_symlinks=True)

Change the owner and group id of *path* to the numeric *uid* and *gid*. To leave one of the ids unchanged, set it to -1.

This function can support `specifying a file descriptor <path_fd>`{.interpreted-text role="ref"}, `paths relative to directory descriptors <dir_fd>`{.interpreted-text role="ref"} and `not
following symlinks <follow_symlinks>`{.interpreted-text role="ref"}.

See `shutil.chown`{.interpreted-text role="func"} for a higher-level function that accepts names in addition to numeric ids.

::: audit-event
os.chown path,uid,gid,dir_fd os.chown
:::

::: availability
Unix.

The function is limited on WASI, see `wasm-availability`{.interpreted-text role="ref"} for more information.
:::

::: versionchanged
3.3 Added support for specifying *path* as an open file descriptor, and the *dir_fd* and *follow_symlinks* arguments.
:::

::: versionchanged
3.6 Supports a `path-like object`{.interpreted-text role="term"}.
:::
:::::::

::::: function
chroot(path)

Change the root directory of the current process to *path*.

::: availability
Unix, not WASI, not Android.
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"}.
:::
:::::

::::: function
fchdir(fd)

Change the current working directory to the directory represented by the file descriptor *fd*. The descriptor must refer to an opened directory, not an open file. As of Python 3.3, this is equivalent to `os.chdir(fd)`.

::: audit-event
os.chdir path os.fchdir
:::

::: availability
Unix.
:::
:::::

::: function
getcwd()

Return a string representing the current working directory.
:::

:::: function
getcwdb()

Return a bytestring representing the current working directory.

::: versionchanged
3.8 The function now uses the UTF-8 encoding on Windows, rather than the ANSI code page: see `529`{.interpreted-text role="pep"} for the rationale. The function is no longer deprecated on Windows.
:::
::::

:::::: function
lchflags(path, flags)

Set the flags of *path* to the numeric *flags*, like `chflags`{.interpreted-text role="func"}, but do not follow symbolic links. As of Python 3.3, this is equivalent to `os.chflags(path, flags, follow_symlinks=False)`.

::: audit-event
os.chflags path,flags os.lchflags
:::

::: availability
Unix, not WASI.
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"}.
:::
::::::

::::::: function
lchmod(path, mode)

Change the mode of *path* to the numeric *mode*. If path is a symlink, this affects the symlink rather than the target. See the docs for `chmod`{.interpreted-text role="func"} for possible values of *mode*. As of Python 3.3, this is equivalent to `os.chmod(path, mode, follow_symlinks=False)`.

`lchmod()` is not part of POSIX, but Unix implementations may have it if changing the mode of symbolic links is supported.

::: audit-event
os.chmod path,mode,dir_fd os.lchmod
:::

::: availability
Unix, Windows, not Linux, FreeBSD \>= 1.3, NetBSD \>= 1.3, not OpenBSD
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"}.
:::

::: versionchanged
3.13 Added support on Windows.
:::
:::::::

:::::: function
lchown(path, uid, gid)

Change the owner and group id of *path* to the numeric *uid* and *gid*. This function will not follow symbolic links. As of Python 3.3, this is equivalent to `os.chown(path, uid, gid, follow_symlinks=False)`.

::: audit-event
os.chown path,uid,gid,dir_fd os.lchown
:::

::: availability
Unix.
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"}.
:::
::::::

:::::::: function
link(src, dst, \*, src_dir_fd=None, dst_dir_fd=None, follow_symlinks=True)

Create a hard link pointing to *src* named *dst*.

This function can support specifying *src_dir_fd* and/or *dst_dir_fd* to supply `paths relative to directory descriptors <dir_fd>`{.interpreted-text role="ref"}, and `not
following symlinks <follow_symlinks>`{.interpreted-text role="ref"}. The default value of *follow_symlinks* is `False` on Windows.

::: audit-event
os.link src,dst,src_dir_fd,dst_dir_fd os.link
:::

::: availability
Unix, Windows.
:::

::: versionchanged
3.2 Added Windows support.
:::

::: versionchanged
3.3 Added the *src_dir_fd*, *dst_dir_fd*, and *follow_symlinks* parameters.
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"} for *src* and *dst*.
:::
::::::::

:::::::::: function
listdir(path=\'.\')

Return a list containing the names of the entries in the directory given by *path*. The list is in arbitrary order, and does not include the special entries `'.'` and `'..'` even if they are present in the directory. If a file is removed from or added to the directory during the call of this function, whether a name for that file be included is unspecified.

*path* may be a `path-like object`{.interpreted-text role="term"}. If *path* is of type `bytes` (directly or indirectly through the `PathLike`{.interpreted-text role="class"} interface), the filenames returned will also be of type `bytes`; in all other circumstances, they will be of type `str`.

This function can also support `specifying a file descriptor
<path_fd>`{.interpreted-text role="ref"}; the file descriptor must refer to a directory.

::: audit-event
os.listdir path os.listdir
:::

:::: note
::: title
Note
:::

To encode `str` filenames to `bytes`, use `~os.fsencode`{.interpreted-text role="func"}.
::::

::: seealso
The `scandir`{.interpreted-text role="func"} function returns directory entries along with file attribute information, giving better performance for many common use cases.
:::

::: versionchanged
3.2 The *path* parameter became optional.
:::

::: versionchanged
3.3 Added support for specifying *path* as an open file descriptor.
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"}.
:::
::::::::::

:::::: function
listdrives()

Return a list containing the names of drives on a Windows system.

A drive name typically looks like `'C:\\'`. Not every drive name will be associated with a volume, and some may be inaccessible for a variety of reasons, including permissions, network connectivity or missing media. This function does not test for access.

May raise `OSError`{.interpreted-text role="exc"} if an error occurs collecting the drive names.

::: audit-event
os.listdrives \"\" os.listdrives
:::

::: availability
Windows
:::

::: versionadded
3.12
:::
::::::

:::::: function
listmounts(volume)

Return a list containing the mount points for a volume on a Windows system.

*volume* must be represented as a GUID path, like those returned by `os.listvolumes`{.interpreted-text role="func"}. Volumes may be mounted in multiple locations or not at all. In the latter case, the list will be empty. Mount points that are not associated with a volume will not be returned by this function.

The mount points return by this function will be absolute paths, and may be longer than the drive name.

Raises `OSError`{.interpreted-text role="exc"} if the volume is not recognized or if an error occurs collecting the paths.

::: audit-event
os.listmounts volume os.listmounts
:::

::: availability
Windows
:::

::: versionadded
3.12
:::
::::::

:::::: function
listvolumes()

Return a list containing the volumes in the system.

Volumes are typically represented as a GUID path that looks like `\\?\Volume{xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx}\`. Files can usually be accessed through a GUID path, permissions allowing. However, users are generally not familiar with them, and so the recommended use of this function is to retrieve mount points using `os.listmounts`{.interpreted-text role="func"}.

May raise `OSError`{.interpreted-text role="exc"} if an error occurs collecting the volumes.

::: audit-event
os.listvolumes \"\" os.listvolumes
:::

::: availability
Windows
:::

::: versionadded
3.12
:::
::::::

:::::::: function
lstat(path, \*, dir_fd=None)

Perform the equivalent of an `!lstat`{.interpreted-text role="c:func"} system call on the given path. Similar to `~os.stat`{.interpreted-text role="func"}, but does not follow symbolic links. Return a `stat_result`{.interpreted-text role="class"} object.

On platforms that do not support symbolic links, this is an alias for `~os.stat`{.interpreted-text role="func"}.

As of Python 3.3, this is equivalent to `os.stat(path, dir_fd=dir_fd, follow_symlinks=False)`.

This function can also support `paths relative to directory descriptors
<dir_fd>`{.interpreted-text role="ref"}.

::: seealso
The `.stat`{.interpreted-text role="func"} function.
:::

::: versionchanged
3.2 Added support for Windows 6.0 (Vista) symbolic links.
:::

::: versionchanged
3.3 Added the *dir_fd* parameter.
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"}.
:::

::: versionchanged
3.8 On Windows, now opens reparse points that represent another path (name surrogates), including symbolic links and directory junctions. Other kinds of reparse points are resolved by the operating system as for `~os.stat`{.interpreted-text role="func"}.
:::
::::::::

:::::::: function
mkdir(path, mode=0o777, \*, dir_fd=None)

Create a directory named *path* with numeric mode *mode*.

If the directory already exists, `FileExistsError`{.interpreted-text role="exc"} is raised. If a parent directory in the path does not exist, `FileNotFoundError`{.interpreted-text role="exc"} is raised.

::: {#mkdir_modebits}
On some systems, *mode* is ignored. Where it is used, the current umask value is first masked out. If bits other than the last 9 (i.e. the last 3 digits of the octal representation of the *mode*) are set, their meaning is platform-dependent. On some platforms, they are ignored and you should call `chmod`{.interpreted-text role="func"} explicitly to set them.
:::

On Windows, a *mode* of `0o700` is specifically handled to apply access control to the new directory such that only the current user and administrators have access. Other values of *mode* are ignored.

This function can also support `paths relative to directory descriptors
<dir_fd>`{.interpreted-text role="ref"}.

It is also possible to create temporary directories; see the `tempfile`{.interpreted-text role="mod"} module\'s `tempfile.mkdtemp`{.interpreted-text role="func"} function.

::: audit-event
os.mkdir path,mode,dir_fd os.mkdir
:::

::: versionchanged
3.3 Added the *dir_fd* parameter.
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"}.
:::

::: versionchanged
3.13 Windows now handles a *mode* of `0o700`.
:::
::::::::

::::::::::: function
makedirs(name, mode=0o777, exist_ok=False)

::: index
single: directory; creating single: UNC paths; and os.makedirs()
:::

Recursive directory creation function. Like `mkdir`{.interpreted-text role="func"}, but makes all intermediate-level directories needed to contain the leaf directory.

The *mode* parameter is passed to `mkdir`{.interpreted-text role="func"} for creating the leaf directory; see `the mkdir() description <mkdir_modebits>`{.interpreted-text role="ref"} for how it is interpreted. To set the file permission bits of any newly created parent directories you can set the umask before invoking `makedirs`{.interpreted-text role="func"}. The file permission bits of existing parent directories are not changed.

If *exist_ok* is `False` (the default), a `FileExistsError`{.interpreted-text role="exc"} is raised if the target directory already exists.

:::: note
::: title
Note
:::

`makedirs`{.interpreted-text role="func"} will become confused if the path elements to create include `pardir`{.interpreted-text role="data"} (eg. \"..\" on UNIX systems).
::::

This function handles UNC paths correctly.

::: audit-event
os.mkdir path,mode,dir_fd os.makedirs
:::

::: versionchanged
3.2 Added the *exist_ok* parameter.
:::

::: versionchanged
3.4.1

Before Python 3.4.1, if *exist_ok* was `True` and the directory existed, `makedirs`{.interpreted-text role="func"} would still raise an error if *mode* did not match the mode of the existing directory. Since this behavior was impossible to implement safely, it was removed in Python 3.4.1. See `21082`{.interpreted-text role="issue"}.
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"}.
:::

::: versionchanged
3.7 The *mode* argument no longer affects the file permission bits of newly created intermediate-level directories.
:::
:::::::::::

:::::: function
mkfifo(path, mode=0o666, \*, dir_fd=None)

Create a FIFO (a named pipe) named *path* with numeric mode *mode*. The current umask value is first masked out from the mode.

This function can also support `paths relative to directory descriptors
<dir_fd>`{.interpreted-text role="ref"}.

FIFOs are pipes that can be accessed like regular files. FIFOs exist until they are deleted (for example with `os.unlink`{.interpreted-text role="func"}). Generally, FIFOs are used as rendezvous between \"client\" and \"server\" type processes: the server opens the FIFO for reading, and the client opens it for writing. Note that `mkfifo`{.interpreted-text role="func"} doesn\'t open the FIFO \-\-- it just creates the rendezvous point.

::: availability
Unix, not WASI.
:::

::: versionchanged
3.3 Added the *dir_fd* parameter.
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"}.
:::
::::::

:::::: function
mknod(path, mode=0o600, device=0, \*, dir_fd=None)

Create a filesystem node (file, device special file or named pipe) named *path*. *mode* specifies both the permissions to use and the type of node to be created, being combined (bitwise OR) with one of `stat.S_IFREG`{.interpreted-text role="const"}, `stat.S_IFCHR`{.interpreted-text role="const"}, `stat.S_IFBLK`{.interpreted-text role="const"}, and `stat.S_IFIFO`{.interpreted-text role="const"}. For `stat.S_IFCHR`{.interpreted-text role="const"} and `stat.S_IFBLK`{.interpreted-text role="const"}, *device* defines the newly created device special file (probably using `os.makedev`{.interpreted-text role="func"}), otherwise it is ignored.

This function can also support `paths relative to directory descriptors
<dir_fd>`{.interpreted-text role="ref"}.

::: availability
Unix, not WASI.
:::

::: versionchanged
3.3 Added the *dir_fd* parameter.
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"}.
:::
::::::

::: function
major(device, /)

Extract the device major number from a raw device number (usually the `~stat_result.st_dev`{.interpreted-text role="attr"} or `~stat_result.st_rdev`{.interpreted-text role="attr"} field from `stat`{.interpreted-text role="c:struct"}).
:::

::: function
minor(device, /)

Extract the device minor number from a raw device number (usually the `~stat_result.st_dev`{.interpreted-text role="attr"} or `~stat_result.st_rdev`{.interpreted-text role="attr"} field from `stat`{.interpreted-text role="c:struct"}).
:::

::: function
makedev(major, minor, /)

Compose a raw device number from the major and minor device numbers.
:::

:::: data
NODEV

Non-existent device.

::: versionadded
3.15
:::
::::

::::: function
pathconf(path, name)

Return system configuration information relevant to a named file. *name* specifies the configuration value to retrieve; it may be a string which is the name of a defined system value; these names are specified in a number of standards (POSIX.1, Unix 95, Unix 98, and others). Some platforms define additional names as well. The names known to the host operating system are given in the `pathconf_names` dictionary. For configuration variables not included in that mapping, passing an integer for *name* is also accepted.

If *name* is a string and is not known, `ValueError`{.interpreted-text role="exc"} is raised. If a specific value for *name* is not supported by the host system, even if it is included in `pathconf_names`, an `OSError`{.interpreted-text role="exc"} is raised with `errno.EINVAL`{.interpreted-text role="const"} for the error number.

This function can support `specifying a file descriptor
<path_fd>`{.interpreted-text role="ref"}.

::: availability
Unix.
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"}.
:::
:::::

:::: data
pathconf_names

Dictionary mapping names accepted by `pathconf`{.interpreted-text role="func"} and `fpathconf`{.interpreted-text role="func"} to the integer values defined for those names by the host operating system. This can be used to determine the set of names known to the system.

::: availability
Unix.
:::
::::

:::::::: function
readlink(path, \*, dir_fd=None)

Return a string representing the path to which the symbolic link points. The result may be either an absolute or relative pathname; if it is relative, it may be converted to an absolute pathname using `os.path.join(os.path.dirname(path), result)`.

If the *path* is a string object (directly or indirectly through a `PathLike`{.interpreted-text role="class"} interface), the result will also be a string object, and the call may raise a UnicodeDecodeError. If the *path* is a bytes object (direct or indirectly), the result will be a bytes object.

This function can also support `paths relative to directory descriptors
<dir_fd>`{.interpreted-text role="ref"}.

When trying to resolve a path that may contain links, use `~os.path.realpath`{.interpreted-text role="func"} to properly handle recursion and platform differences.

::: availability
Unix, Windows.
:::

::: versionchanged
3.2 Added support for Windows 6.0 (Vista) symbolic links.
:::

::: versionchanged
3.3 Added the *dir_fd* parameter.
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"} on Unix.
:::

::: versionchanged
3.8 Accepts a `path-like object`{.interpreted-text role="term"} and a bytes object on Windows.

Added support for directory junctions, and changed to return the substitution path (which typically includes `\\?\` prefix) rather than the optional \"print name\" field that was previously returned.
:::
::::::::

:::::: function
remove(path, \*, dir_fd=None)

Remove (delete) the file *path*. If *path* is a directory, an `OSError`{.interpreted-text role="exc"} is raised. Use `rmdir`{.interpreted-text role="func"} to remove directories. If the file does not exist, a `FileNotFoundError`{.interpreted-text role="exc"} is raised.

This function can support `paths relative to directory descriptors
<dir_fd>`{.interpreted-text role="ref"}.

On Windows, attempting to remove a file that is in use causes an exception to be raised; on Unix, the directory entry is removed but the storage allocated to the file is not made available until the original file is no longer in use.

This function is semantically identical to `unlink`{.interpreted-text role="func"}.

::: audit-event
os.remove path,dir_fd os.remove
:::

::: versionchanged
3.3 Added the *dir_fd* parameter.
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"}.
:::
::::::

:::::: function
removedirs(name)

::: index
single: directory; deleting
:::

Remove directories recursively. Works like `rmdir`{.interpreted-text role="func"} except that, if the leaf directory is successfully removed, `removedirs`{.interpreted-text role="func"} tries to successively remove every parent directory mentioned in *path* until an error is raised (which is ignored, because it generally means that a parent directory is not empty). For example, `os.removedirs('foo/bar/baz')` will first remove the directory `'foo/bar/baz'`, and then remove `'foo/bar'` and `'foo'` if they are empty. Raises `OSError`{.interpreted-text role="exc"} if the leaf directory could not be successfully removed.

::: audit-event
os.remove path,dir_fd os.removedirs
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"}.
:::
::::::

:::::: function
rename(src, dst, \*, src_dir_fd=None, dst_dir_fd=None)

Rename the file or directory *src* to *dst*. If *dst* exists, the operation will fail with an `OSError`{.interpreted-text role="exc"} subclass in a number of cases:

On Windows, if *dst* exists a `FileExistsError`{.interpreted-text role="exc"} is always raised. The operation may fail if *src* and *dst* are on different filesystems. Use `shutil.move`{.interpreted-text role="func"} to support moves to a different filesystem.

On Unix, if *src* is a file and *dst* is a directory or vice-versa, an `IsADirectoryError`{.interpreted-text role="exc"} or a `NotADirectoryError`{.interpreted-text role="exc"} will be raised respectively. If both are directories and *dst* is empty, *dst* will be silently replaced. If *dst* is a non-empty directory, an `OSError`{.interpreted-text role="exc"} is raised. If both are files, *dst* will be replaced silently if the user has permission. The operation may fail on some Unix flavors if *src* and *dst* are on different filesystems. If successful, the renaming will be an atomic operation (this is a POSIX requirement).

This function can support specifying *src_dir_fd* and/or *dst_dir_fd* to supply `paths relative to directory descriptors <dir_fd>`{.interpreted-text role="ref"}.

If you want cross-platform overwriting of the destination, use `replace`{.interpreted-text role="func"}.

::: audit-event
os.rename src,dst,src_dir_fd,dst_dir_fd os.rename
:::

::: versionchanged
3.3 Added the *src_dir_fd* and *dst_dir_fd* parameters.
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"} for *src* and *dst*.
:::
::::::

::::::: function
renames(old, new)

Recursive directory or file renaming function. Works like `rename`{.interpreted-text role="func"}, except creation of any intermediate directories needed to make the new pathname good is attempted first. After the rename, directories corresponding to rightmost path segments of the old name will be pruned away using `removedirs`{.interpreted-text role="func"}.

:::: note
::: title
Note
:::

This function can fail with the new directory structure made if you lack permissions needed to remove the leaf directory or file.
::::

::: audit-event
os.rename src,dst,src_dir_fd,dst_dir_fd os.renames
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"} for *old* and *new*.
:::
:::::::

:::::: function
replace(src, dst, \*, src_dir_fd=None, dst_dir_fd=None)

Rename the file or directory *src* to *dst*. If *dst* is a non-empty directory, `OSError`{.interpreted-text role="exc"} will be raised. If *dst* exists and is a file, it will be replaced silently if the user has permission. The operation may fail if *src* and *dst* are on different filesystems. If successful, the renaming will be an atomic operation (this is a POSIX requirement).

This function can support specifying *src_dir_fd* and/or *dst_dir_fd* to supply `paths relative to directory descriptors <dir_fd>`{.interpreted-text role="ref"}.

::: audit-event
os.rename src,dst,src_dir_fd,dst_dir_fd os.replace
:::

::: versionadded
3.3
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"} for *src* and *dst*.
:::
::::::

:::::: function
rmdir(path, \*, dir_fd=None)

Remove (delete) the directory *path*. If the directory does not exist or is not empty, a `FileNotFoundError`{.interpreted-text role="exc"} or an `OSError`{.interpreted-text role="exc"} is raised respectively. In order to remove whole directory trees, `shutil.rmtree`{.interpreted-text role="func"} can be used.

This function can support `paths relative to directory descriptors
<dir_fd>`{.interpreted-text role="ref"}.

::: audit-event
os.rmdir path,dir_fd os.rmdir
:::

::: versionchanged
3.3 Added the *dir_fd* parameter.
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"}.
:::
::::::

::::::::::: function
scandir(path=\'.\')

Return an iterator of `os.DirEntry`{.interpreted-text role="class"} objects corresponding to the entries in the directory given by *path*. The entries are yielded in arbitrary order, and the special entries `'.'` and `'..'` are not included. If a file is removed from or added to the directory after creating the iterator, whether an entry for that file be included is unspecified.

Using `scandir`{.interpreted-text role="func"} instead of `listdir`{.interpreted-text role="func"} can significantly increase the performance of code that also needs file type or file attribute information, because `os.DirEntry`{.interpreted-text role="class"} objects expose this information if the operating system provides it when scanning a directory. All `os.DirEntry`{.interpreted-text role="class"} methods may perform a system call, but `~os.DirEntry.is_dir`{.interpreted-text role="func"} and `~os.DirEntry.is_file`{.interpreted-text role="func"} usually only require a system call for symbolic links; `os.DirEntry.stat`{.interpreted-text role="func"} always requires a system call on Unix but only requires one for symbolic links on Windows.

*path* may be a `path-like object`{.interpreted-text role="term"}. If *path* is of type `bytes` (directly or indirectly through the `PathLike`{.interpreted-text role="class"} interface), the type of the `~os.DirEntry.name`{.interpreted-text role="attr"} and `~os.DirEntry.path`{.interpreted-text role="attr"} attributes of each `os.DirEntry`{.interpreted-text role="class"} will be `bytes`; in all other circumstances, they will be of type `str`.

This function can also support `specifying a file descriptor
<path_fd>`{.interpreted-text role="ref"}; the file descriptor must refer to a directory.

::: audit-event
os.scandir path os.scandir
:::

The `scandir`{.interpreted-text role="func"} iterator supports the `context manager`{.interpreted-text role="term"} protocol and has the following method:

:::: method
scandir.close()

Close the iterator and free acquired resources.

This is called automatically when the iterator is exhausted or garbage collected, or when an error happens during iterating. However it is advisable to call it explicitly or use the `with`{.interpreted-text role="keyword"} statement.

::: versionadded
3.6
:::
::::

The following example shows a simple use of `scandir`{.interpreted-text role="func"} to display all the files (excluding directories) in the given *path* that don\'t start with `'.'`. The `entry.is_file()` call will generally not make an additional system call:

    with os.scandir(path) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_file():
                print(entry.name)

:::: note
::: title
Note
:::

On Unix-based systems, `scandir`{.interpreted-text role="func"} uses the system\'s [opendir()](https://pubs.opengroup.org/onlinepubs/009695399/functions/opendir.html) and [readdir()](https://pubs.opengroup.org/onlinepubs/009695399/functions/readdir_r.html) functions. On Windows, it uses the Win32 [FindFirstFileW](https://msdn.microsoft.com/en-us/library/windows/desktop/aa364418(v=vs.85).aspx) and [FindNextFileW](https://msdn.microsoft.com/en-us/library/windows/desktop/aa364428(v=vs.85).aspx) functions.
::::

::: versionadded
3.5
:::

::: versionchanged
3.6 Added support for the `context manager`{.interpreted-text role="term"} protocol and the `~scandir.close`{.interpreted-text role="func"} method. If a `scandir`{.interpreted-text role="func"} iterator is neither exhausted nor explicitly closed a `ResourceWarning`{.interpreted-text role="exc"} will be emitted in its destructor.

The function accepts a `path-like object`{.interpreted-text role="term"}.
:::

::: versionchanged
3.7 Added support for `file descriptors <path_fd>`{.interpreted-text role="ref"} on Unix.
:::
:::::::::::

::::::::::::::: DirEntry
Object yielded by `scandir`{.interpreted-text role="func"} to expose the file path and other file attributes of a directory entry.

`scandir`{.interpreted-text role="func"} will provide as much of this information as possible without making additional system calls. When a `stat()` or `lstat()` system call is made, the `os.DirEntry` object will cache the result.

`os.DirEntry` instances are not intended to be stored in long-lived data structures; if you know the file metadata has changed or if a long time has elapsed since calling `scandir`{.interpreted-text role="func"}, call `os.stat(entry.path)` to fetch up-to-date information.

Because the `os.DirEntry` methods can make operating system calls, they may also raise `OSError`{.interpreted-text role="exc"}. If you need very fine-grained control over errors, you can catch `OSError`{.interpreted-text role="exc"} when calling one of the `os.DirEntry` methods and handle as appropriate.

To be directly usable as a `path-like object`{.interpreted-text role="term"}, `os.DirEntry` implements the `PathLike`{.interpreted-text role="class"} interface.

Attributes and methods on a `os.DirEntry` instance are as follows:

::: attribute
name

The entry\'s base filename, relative to the `scandir`{.interpreted-text role="func"} *path* argument.

The `name`{.interpreted-text role="attr"} attribute will be `bytes` if the `scandir`{.interpreted-text role="func"} *path* argument is of type `bytes` and `str` otherwise. Use `~os.fsdecode`{.interpreted-text role="func"} to decode byte filenames.
:::

::: attribute
path

The entry\'s full path name: equivalent to `os.path.join(scandir_path, entry.name)` where *scandir_path* is the `scandir`{.interpreted-text role="func"} *path* argument. The path is only absolute if the `scandir`{.interpreted-text role="func"} *path* argument was absolute. If the `scandir`{.interpreted-text role="func"} *path* argument was a `file descriptor <path_fd>`{.interpreted-text role="ref"}, the `path`{.interpreted-text role="attr"} attribute is the same as the `name`{.interpreted-text role="attr"} attribute.

The `path`{.interpreted-text role="attr"} attribute will be `bytes` if the `scandir`{.interpreted-text role="func"} *path* argument is of type `bytes` and `str` otherwise. Use `~os.fsdecode`{.interpreted-text role="func"} to decode byte filenames.
:::

::: method
inode()

Return the inode number of the entry.

The result is cached on the `os.DirEntry` object. Use `os.stat(entry.path, follow_symlinks=False).st_ino` to fetch up-to-date information.

On the first, uncached call, a system call is required on Windows but not on Unix.
:::

::: method
is_dir(\*, follow_symlinks=True)

Return `True` if this entry is a directory or a symbolic link pointing to a directory; return `False` if the entry is or points to any other kind of file, or if it doesn\'t exist anymore.

If *follow_symlinks* is `False`, return `True` only if this entry is a directory (without following symlinks); return `False` if the entry is any other kind of file or if it doesn\'t exist anymore.

The result is cached on the `os.DirEntry` object, with a separate cache for *follow_symlinks* `True` and `False`. Call `os.stat`{.interpreted-text role="func"} along with `stat.S_ISDIR`{.interpreted-text role="func"} to fetch up-to-date information.

On the first, uncached call, no system call is required in most cases. Specifically, for non-symlinks, neither Windows or Unix require a system call, except on certain Unix file systems, such as network file systems, that return `dirent.d_type == DT_UNKNOWN`. If the entry is a symlink, a system call will be required to follow the symlink unless *follow_symlinks* is `False`.

This method can raise `OSError`{.interpreted-text role="exc"}, such as `PermissionError`{.interpreted-text role="exc"}, but `FileNotFoundError`{.interpreted-text role="exc"} is caught and not raised.
:::

::: method
is_file(\*, follow_symlinks=True)

Return `True` if this entry is a file or a symbolic link pointing to a file; return `False` if the entry is or points to a directory or other non-file entry, or if it doesn\'t exist anymore.

If *follow_symlinks* is `False`, return `True` only if this entry is a file (without following symlinks); return `False` if the entry is a directory or other non-file entry, or if it doesn\'t exist anymore.

The result is cached on the `os.DirEntry` object. Caching, system calls made, and exceptions raised are as per `~os.DirEntry.is_dir`{.interpreted-text role="func"}.
:::

::: method
is_symlink()

Return `True` if this entry is a symbolic link (even if broken); return `False` if the entry points to a directory or any kind of file, or if it doesn\'t exist anymore.

The result is cached on the `os.DirEntry` object. Call `os.path.islink`{.interpreted-text role="func"} to fetch up-to-date information.

On the first, uncached call, no system call is required in most cases. Specifically, neither Windows or Unix require a system call, except on certain Unix file systems, such as network file systems, that return `dirent.d_type == DT_UNKNOWN`.

This method can raise `OSError`{.interpreted-text role="exc"}, such as `PermissionError`{.interpreted-text role="exc"}, but `FileNotFoundError`{.interpreted-text role="exc"} is caught and not raised.
:::

:::: method
is_junction()

Return `True` if this entry is a junction (even if broken); return `False` if the entry points to a regular directory, any kind of file, a symlink, or if it doesn\'t exist anymore.

The result is cached on the `os.DirEntry` object. Call `os.path.isjunction`{.interpreted-text role="func"} to fetch up-to-date information.

::: versionadded
3.12
:::
::::

::: method
stat(\*, follow_symlinks=True)

Return a `stat_result`{.interpreted-text role="class"} object for this entry. This method follows symbolic links by default; to stat a symbolic link add the `follow_symlinks=False` argument.

On Unix, this method always requires a system call. On Windows, it only requires a system call if *follow_symlinks* is `True` and the entry is a reparse point (for example, a symbolic link or directory junction).

On Windows, the `st_ino`, `st_dev` and `st_nlink` attributes of the `stat_result`{.interpreted-text role="class"} are always set to zero. Call `os.stat`{.interpreted-text role="func"} to get these attributes.

The result is cached on the `os.DirEntry` object, with a separate cache for *follow_symlinks* `True` and `False`. Call `os.stat`{.interpreted-text role="func"} to fetch up-to-date information.
:::

Note that there is a nice correspondence between several attributes and methods of `os.DirEntry` and of `pathlib.Path`{.interpreted-text role="class"}. In particular, the `name` attribute has the same meaning, as do the `is_dir()`, `is_file()`, `is_symlink()`, `is_junction()`, and `stat()` methods.

::: versionadded
3.5
:::

::: versionchanged
3.6 Added support for the `~os.PathLike`{.interpreted-text role="class"} interface. Added support for `bytes`{.interpreted-text role="class"} paths on Windows.
:::

::: versionchanged
3.12 The `st_ctime` attribute of a stat result is deprecated on Windows. The file creation time is properly available as `st_birthtime`, and in the future `st_ctime` may be changed to return zero or the metadata change time, if available.
:::
:::::::::::::::

:::::::: function
stat(path, \*, dir_fd=None, follow_symlinks=True)

Get the status of a file or a file descriptor. Perform the equivalent of a `stat`{.interpreted-text role="c:func"} system call on the given path. *path* may be specified as either a string or bytes \-- directly or indirectly through the `PathLike`{.interpreted-text role="class"} interface \-- or as an open file descriptor. Return a `stat_result`{.interpreted-text role="class"} object.

This function normally follows symlinks; to stat a symlink add the argument `follow_symlinks=False`, or use `lstat`{.interpreted-text role="func"}.

This function can support `specifying a file descriptor <path_fd>`{.interpreted-text role="ref"} and `not following symlinks <follow_symlinks>`{.interpreted-text role="ref"}.

On Windows, passing `follow_symlinks=False` will disable following all name-surrogate reparse points, which includes symlinks and directory junctions. Other types of reparse points that do not resemble links or that the operating system is unable to follow will be opened directly. When following a chain of multiple links, this may result in the original link being returned instead of the non-link that prevented full traversal. To obtain stat results for the final path in this case, use the `os.path.realpath`{.interpreted-text role="func"} function to resolve the path name as far as possible and call `lstat`{.interpreted-text role="func"} on the result. This does not apply to dangling symlinks or junction points, which will raise the usual exceptions.

::: index
pair: module; stat
:::

Example:

    >>> import os
    >>> statinfo = os.stat('somefile.txt')
    >>> statinfo
    os.stat_result(st_mode=33188, st_ino=7876932, st_dev=234881026,
    st_nlink=1, st_uid=501, st_gid=501, st_size=264, st_atime=1297230295,
    st_mtime=1297230027, st_ctime=1297230027)
    >>> statinfo.st_size
    264

::: seealso
`fstat`{.interpreted-text role="func"} and `lstat`{.interpreted-text role="func"} functions.
:::

::: versionchanged
3.3 Added the *dir_fd* and *follow_symlinks* parameters, specifying a file descriptor instead of a path.
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"}.
:::

::: versionchanged
3.8 On Windows, all reparse points that can be resolved by the operating system are now followed, and passing `follow_symlinks=False` disables following all name surrogate reparse points. If the operating system reaches a reparse point that it is not able to follow, *stat* now returns the information for the original path as if `follow_symlinks=False` had been specified instead of raising an error.
:::
::::::::

:::::::::::::::::::::::::::::::::::::::::::: stat_result
Object whose attributes correspond roughly to the members of the `stat`{.interpreted-text role="c:struct"} structure. It is used for the result of `os.stat`{.interpreted-text role="func"}, `os.fstat`{.interpreted-text role="func"} and `os.lstat`{.interpreted-text role="func"}.

Attributes:

::: attribute
st_mode

File mode: file type and file mode bits (permissions).
:::

::: attribute
st_ino

Platform dependent, but if non-zero, uniquely identifies the file for a given value of `st_dev`. Typically:

- the inode number on Unix,
- the [file index](https://msdn.microsoft.com/en-us/library/aa363788) on Windows
:::

::: attribute
st_dev

Identifier of the device on which this file resides.
:::

::: attribute
st_nlink

Number of hard links.
:::

::: attribute
st_uid

User identifier of the file owner.
:::

::: attribute
st_gid

Group identifier of the file owner.
:::

::: attribute
st_size

Size of the file in bytes, if it is a regular file or a symbolic link. The size of a symbolic link is the length of the pathname it contains, without a terminating null byte.
:::

Timestamps:

::: attribute
st_atime

Time of most recent access expressed in seconds.
:::

::: attribute
st_mtime

Time of most recent content modification expressed in seconds.
:::

:::: attribute
st_ctime

Time of most recent metadata change expressed in seconds.

::: versionchanged
3.12 `st_ctime` is deprecated on Windows. Use `st_birthtime` for the file creation time. In the future, `st_ctime` will contain the time of the most recent metadata change, as for other platforms.
:::
::::

:::: attribute
st_atime_ns

Time of most recent access expressed in nanoseconds as an integer.

::: versionadded
3.3
:::
::::

:::: attribute
st_mtime_ns

Time of most recent content modification expressed in nanoseconds as an integer.

::: versionadded
3.3
:::
::::

::::: attribute
st_ctime_ns

Time of most recent metadata change expressed in nanoseconds as an integer.

::: versionadded
3.3
:::

::: versionchanged
3.12 `st_ctime_ns` is deprecated on Windows. Use `st_birthtime_ns` for the file creation time. In the future, `st_ctime` will contain the time of the most recent metadata change, as for other platforms.
:::
:::::

:::: attribute
st_birthtime

Time of file creation expressed in seconds. This attribute is not always available, and may raise `AttributeError`{.interpreted-text role="exc"}.

::: versionchanged
3.12 `st_birthtime` is now available on Windows.
:::
::::

:::: attribute
st_birthtime_ns

Time of file creation expressed in nanoseconds as an integer. This attribute is not always available, and may raise `AttributeError`{.interpreted-text role="exc"}.

::: versionadded
3.12
:::
::::

:::: note
::: title
Note
:::

The exact meaning and resolution of the `st_atime`{.interpreted-text role="attr"}, `st_mtime`{.interpreted-text role="attr"}, `st_ctime`{.interpreted-text role="attr"} and `st_birthtime`{.interpreted-text role="attr"} attributes depend on the operating system and the file system. For example, on Windows systems using the FAT32 file systems, `st_mtime`{.interpreted-text role="attr"} has 2-second resolution, and `st_atime`{.interpreted-text role="attr"} has only 1-day resolution. See your operating system documentation for details.

Similarly, although `st_atime_ns`{.interpreted-text role="attr"}, `st_mtime_ns`{.interpreted-text role="attr"}, `st_ctime_ns`{.interpreted-text role="attr"} and `st_birthtime_ns`{.interpreted-text role="attr"} are always expressed in nanoseconds, many systems do not provide nanosecond precision. On systems that do provide nanosecond precision, the floating-point object used to store `st_atime`{.interpreted-text role="attr"}, `st_mtime`{.interpreted-text role="attr"}, `st_ctime`{.interpreted-text role="attr"} and `st_birthtime`{.interpreted-text role="attr"} cannot preserve all of it, and as such will be slightly inexact. If you need the exact timestamps you should always use `st_atime_ns`{.interpreted-text role="attr"}, `st_mtime_ns`{.interpreted-text role="attr"}, `st_ctime_ns`{.interpreted-text role="attr"} and `st_birthtime_ns`{.interpreted-text role="attr"}.
::::

On some Unix systems (such as Linux), the following attributes may also be available:

::: attribute
st_blocks

Number of 512-byte blocks allocated for file. This may be smaller than `st_size`{.interpreted-text role="attr"}/512 when the file has holes.
:::

::: attribute
st_blksize

\"Preferred\" blocksize for efficient file system I/O. Writing to a file in smaller chunks may cause an inefficient read-modify-rewrite.
:::

::: attribute
st_rdev

Type of device if an inode device.
:::

::: attribute
st_flags

User defined flags for file.
:::

On other Unix systems (such as FreeBSD), the following attributes may be available (but may be only filled out if root tries to use them):

::: attribute
st_gen

File generation number.
:::

On Solaris and derivatives, the following attributes may also be available:

::: attribute
st_fstype

String that uniquely identifies the type of the filesystem that contains the file.
:::

On macOS systems, the following attributes may also be available:

::: attribute
st_rsize

Real size of the file.
:::

::: attribute
st_creator

Creator of the file.
:::

::: attribute
st_type

File type.
:::

On Windows systems, the following attributes are also available:

:::: attribute
st_file_attributes

Windows file attributes: `dwFileAttributes` member of the `BY_HANDLE_FILE_INFORMATION` structure returned by `!GetFileInformationByHandle`{.interpreted-text role="c:func"}. See the `!FILE_ATTRIBUTE_* <stat.FILE_ATTRIBUTE_ARCHIVE>`{.interpreted-text role="const"} constants in the `stat`{.interpreted-text role="mod"} module.

::: versionadded
3.5
:::
::::

::: attribute
st_reparse_tag

When `st_file_attributes`{.interpreted-text role="attr"} has the `~stat.FILE_ATTRIBUTE_REPARSE_POINT`{.interpreted-text role="const"} set, this field contains the tag identifying the type of reparse point. See the `IO_REPARSE_TAG_* <stat.IO_REPARSE_TAG_SYMLINK>`{.interpreted-text role="const"} constants in the `stat`{.interpreted-text role="mod"} module.
:::

The standard module `stat`{.interpreted-text role="mod"} defines functions and constants that are useful for extracting information from a `stat`{.interpreted-text role="c:struct"} structure. (On Windows, some items are filled with dummy values.)

For backward compatibility, a `stat_result`{.interpreted-text role="class"} instance is also accessible as a tuple of at least 10 integers giving the most important (and portable) members of the `stat`{.interpreted-text role="c:struct"} structure, in the order `st_mode`{.interpreted-text role="attr"}, `st_ino`{.interpreted-text role="attr"}, `st_dev`{.interpreted-text role="attr"}, `st_nlink`{.interpreted-text role="attr"}, `st_uid`{.interpreted-text role="attr"}, `st_gid`{.interpreted-text role="attr"}, `st_size`{.interpreted-text role="attr"}, `st_atime`{.interpreted-text role="attr"}, `st_mtime`{.interpreted-text role="attr"}, `st_ctime`{.interpreted-text role="attr"}. More items may be added at the end by some implementations. For compatibility with older Python versions, accessing `stat_result`{.interpreted-text role="class"} as a tuple always returns integers.

::: versionchanged
3.5 Windows now returns the file index as `st_ino`{.interpreted-text role="attr"} when available.
:::

::: versionchanged
3.7 Added the `st_fstype`{.interpreted-text role="attr"} member to Solaris/derivatives.
:::

::: versionchanged
3.8 Added the `st_reparse_tag`{.interpreted-text role="attr"} member on Windows.
:::

::: versionchanged
3.8 On Windows, the `st_mode`{.interpreted-text role="attr"} member now identifies special files as `~stat.S_IFCHR`{.interpreted-text role="const"}, `~stat.S_IFIFO`{.interpreted-text role="const"} or `~stat.S_IFBLK`{.interpreted-text role="const"} as appropriate.
:::

::: versionchanged
3.12 On Windows, `st_ctime`{.interpreted-text role="attr"} is deprecated. Eventually, it will contain the last metadata change time, for consistency with other platforms, but for now still contains creation time. Use `st_birthtime`{.interpreted-text role="attr"} for the creation time.

On Windows, `st_ino`{.interpreted-text role="attr"} may now be up to 128 bits, depending on the file system. Previously it would not be above 64 bits, and larger file identifiers would be arbitrarily packed.

On Windows, `st_rdev`{.interpreted-text role="attr"} no longer returns a value. Previously it would contain the same as `st_dev`{.interpreted-text role="attr"}, which was incorrect.

Added the `st_birthtime`{.interpreted-text role="attr"} member on Windows.
:::
::::::::::::::::::::::::::::::::::::::::::::

:::::: function
statx(path, mask, \*, flags=0, dir_fd=None, follow_symlinks=True)

Get the status of a file or file descriptor by performing a `!statx`{.interpreted-text role="c:func"} system call on the given path.

*path* is a `path-like object`{.interpreted-text role="term"} or an open file descriptor. *mask* is a combination of the module-level `STATX_* <STATX_TYPE>`{.interpreted-text role="const"} constants specifying the information to retrieve. *flags* is a combination of the module-level `AT_STATX_* <AT_STATX_FORCE_SYNC>`{.interpreted-text role="const"} constants and/or `AT_NO_AUTOMOUNT`{.interpreted-text role="const"}. Returns a `statx_result`{.interpreted-text role="class"} object whose `~os.statx_result.stx_mask`{.interpreted-text role="attr"} attribute specifies the information actually retrieved (which may differ from *mask*).

This function supports `specifying a file descriptor <path_fd>`{.interpreted-text role="ref"}, `paths relative to directory descriptors <dir_fd>`{.interpreted-text role="ref"}, and `not following symlinks <follow_symlinks>`{.interpreted-text role="ref"}.

::: seealso
The `statx(2)`{.interpreted-text role="manpage"} man page.
:::

::: availability
Linux \>= 4.11 with glibc \>= 2.28.
:::

::: versionadded
3.15
:::
::::::

::::::::::::::::::::::::::::::::::::::::::::::::: statx_result
Information about a file returned by `os.statx`{.interpreted-text role="func"}.

`!statx_result`{.interpreted-text role="class"} has the following attributes:

::: attribute
stx_atime

Time of most recent access expressed in seconds.

Equal to `None` if `STATX_ATIME`{.interpreted-text role="data"} is missing from `~statx_result.stx_mask`{.interpreted-text role="attr"}.
:::

::: attribute
stx_atime_ns

Time of most recent access expressed in nanoseconds as an integer.

Equal to `None` if `STATX_ATIME`{.interpreted-text role="data"} is missing from `~statx_result.stx_mask`{.interpreted-text role="attr"}.
:::

:::: attribute
stx_atomic_write_segments_max

Maximum iovecs for direct I/O with torn-write protection.

Equal to `None` if `STATX_WRITE_ATOMIC`{.interpreted-text role="data"} is missing from `~statx_result.stx_mask`{.interpreted-text role="attr"}.

::: availability
Linux \>= 4.11 with glibc \>= 2.28 and build-time kernel userspace API headers \>= 6.11.
:::
::::

:::: attribute
stx_atomic_write_unit_max

Maximum size for direct I/O with torn-write protection.

Equal to `None` if `STATX_WRITE_ATOMIC`{.interpreted-text role="data"} is missing from `~statx_result.stx_mask`{.interpreted-text role="attr"}.

::: availability
Linux \>= 4.11 with glibc \>= 2.28 and build-time kernel userspace API headers \>= 6.11.
:::
::::

:::: attribute
stx_atomic_write_unit_max_opt

Maximum optimized size for direct I/O with torn-write protection.

Equal to `None` if `STATX_WRITE_ATOMIC`{.interpreted-text role="data"} is missing from `~statx_result.stx_mask`{.interpreted-text role="attr"}.

::: availability
Linux \>= 4.11 with glibc \>= 2.28 and build-time kernel userspace API headers \>= 6.16.
:::
::::

:::: attribute
stx_atomic_write_unit_min

Minimum size for direct I/O with torn-write protection.

Equal to `None` if `STATX_WRITE_ATOMIC`{.interpreted-text role="data"} is missing from `~statx_result.stx_mask`{.interpreted-text role="attr"}.

::: availability
Linux \>= 4.11 with glibc \>= 2.28 and build-time kernel userspace API headers \>= 6.11.
:::
::::

::: attribute
stx_attributes

Bitmask of `STATX_ATTR_* <stat.STATX_ATTR_COMPRESSED>`{.interpreted-text role="const"} constants specifying the attributes of this file.
:::

::: attribute
stx_attributes_mask

A mask indicating which bits in `stx_attributes`{.interpreted-text role="attr"} are supported by the VFS and the filesystem.
:::

::: attribute
stx_blksize

\"Preferred\" blocksize for efficient file system I/O. Writing to a file in smaller chunks may cause an inefficient read-modify-rewrite.
:::

::: attribute
stx_blocks

Number of 512-byte blocks allocated for file. This may be smaller than `stx_size`{.interpreted-text role="attr"}/512 when the file has holes.

Equal to `None` if `STATX_BLOCKS`{.interpreted-text role="data"} is missing from `~statx_result.stx_mask`{.interpreted-text role="attr"}.
:::

::: attribute
stx_btime

Time of file creation expressed in seconds.

Equal to `None` if `STATX_BTIME`{.interpreted-text role="data"} is missing from `~statx_result.stx_mask`{.interpreted-text role="attr"}.
:::

::: attribute
stx_btime_ns

Time of file creation expressed in nanoseconds as an integer.

Equal to `None` if `STATX_BTIME`{.interpreted-text role="data"} is missing from `~statx_result.stx_mask`{.interpreted-text role="attr"}.
:::

::: attribute
stx_ctime

Time of most recent metadata change expressed in seconds.

Equal to `None` if `STATX_CTIME`{.interpreted-text role="data"} is missing from `~statx_result.stx_mask`{.interpreted-text role="attr"}.
:::

::: attribute
stx_ctime_ns

Time of most recent metadata change expressed in nanoseconds as an integer.

Equal to `None` if `STATX_CTIME`{.interpreted-text role="data"} is missing from `~statx_result.stx_mask`{.interpreted-text role="attr"}.
:::

::: attribute
stx_dev

Identifier of the device on which this file resides.
:::

::: attribute
stx_dev_major

Major number of the device on which this file resides.
:::

::: attribute
stx_dev_minor

Minor number of the device on which this file resides.
:::

:::: attribute
stx_dio_mem_align

Direct I/O memory buffer alignment requirement.

Equal to `None` if `STATX_DIOALIGN`{.interpreted-text role="data"} is missing from `~statx_result.stx_mask`{.interpreted-text role="attr"}.

::: availability
Linux \>= 4.11 with glibc \>= 2.28 and build-time kernel userspace API headers \>= 6.1.
:::
::::

:::: attribute
stx_dio_offset_align

Direct I/O file offset alignment requirement.

Equal to `None` if `STATX_DIOALIGN`{.interpreted-text role="data"} is missing from `~statx_result.stx_mask`{.interpreted-text role="attr"}.

::: availability
Linux \>= 4.11 with glibc \>= 2.28 and build-time kernel userspace API headers \>= 6.1.
:::
::::

:::: attribute
stx_dio_read_offset_align

Direct I/O file offset alignment requirement for reads.

Equal to `None` if `STATX_DIO_READ_ALIGN`{.interpreted-text role="data"} is missing from `~statx_result.stx_mask`{.interpreted-text role="attr"}.

::: availability
Linux \>= 4.11 with glibc \>= 2.28 and build-time kernel userspace API headers \>= 6.14.
:::
::::

::: attribute
stx_gid

Group identifier of the file owner.

Equal to `None` if `STATX_GID`{.interpreted-text role="data"} is missing from `~statx_result.stx_mask`{.interpreted-text role="attr"}.
:::

::: attribute
stx_ino

Inode number.

Equal to `None` if `STATX_INO`{.interpreted-text role="data"} is missing from `~statx_result.stx_mask`{.interpreted-text role="attr"}.
:::

::: attribute
stx_mask

Bitmask of `STATX_* <STATX_TYPE>`{.interpreted-text role="const"} constants specifying the information retrieved, which may differ from what was requested.
:::

:::: attribute
stx_mnt_id

Mount identifier.

Equal to `None` if `STATX_MNT_ID`{.interpreted-text role="data"} is missing from `~statx_result.stx_mask`{.interpreted-text role="attr"}.

::: availability
Linux \>= 4.11 with glibc \>= 2.28 and build-time kernel userspace API headers \>= 5.8.
:::
::::

::: attribute
stx_mode

File mode: file type and file mode bits (permissions).

Equal to `None` if `STATX_TYPE | STATX_MODE <STATX_TYPE>`{.interpreted-text role="data"} is missing from `~statx_result.stx_mask`{.interpreted-text role="attr"}.
:::

::: attribute
stx_mtime

Time of most recent content modification expressed in seconds.

Equal to `None` if `STATX_MTIME`{.interpreted-text role="data"} is missing from `~statx_result.stx_mask`{.interpreted-text role="attr"}.
:::

::: attribute
stx_mtime_ns

Time of most recent content modification expressed in nanoseconds as an integer.

Equal to `None` if `STATX_MTIME`{.interpreted-text role="data"} is missing from `~statx_result.stx_mask`{.interpreted-text role="attr"}.
:::

::: attribute
stx_nlink

Number of hard links.

Equal to `None` if `STATX_NLINK`{.interpreted-text role="data"} is missing from `~statx_result.stx_mask`{.interpreted-text role="attr"}.
:::

::: attribute
stx_rdev

Type of device if an inode device.
:::

::: attribute
stx_rdev_major

Major number of the device this file represents.
:::

::: attribute
stx_rdev_minor

Minor number of the device this file represents.
:::

::: attribute
stx_size

Size of the file in bytes, if it is a regular file or a symbolic link. The size of a symbolic link is the length of the pathname it contains, without a terminating null byte.

Equal to `None` if `STATX_SIZE`{.interpreted-text role="data"} is missing from `~statx_result.stx_mask`{.interpreted-text role="attr"}.
:::

:::: attribute
stx_subvol

Subvolume identifier.

Equal to `None` if `STATX_SUBVOL`{.interpreted-text role="data"} is missing from `~statx_result.stx_mask`{.interpreted-text role="attr"}.

::: availability
Linux \>= 4.11 with glibc \>= 2.28 and build-time kernel userspace API headers \>= 6.10.
:::
::::

::: attribute
stx_uid

User identifier of the file owner.

Equal to `None` if `STATX_UID`{.interpreted-text role="data"} is missing from `~statx_result.stx_mask`{.interpreted-text role="attr"}.
:::

::: seealso
The `statx(2)`{.interpreted-text role="manpage"} man page.
:::

::: availability
Linux \>= 4.11 with glibc \>= 2.28.
:::

::: versionadded
3.15
:::
:::::::::::::::::::::::::::::::::::::::::::::::::

::::: data
STATX_TYPE STATX_MODE STATX_NLINK STATX_UID STATX_GID STATX_ATIME STATX_MTIME STATX_CTIME STATX_INO STATX_SIZE STATX_BLOCKS STATX_BASIC_STATS STATX_BTIME STATX_MNT_ID STATX_DIOALIGN STATX_MNT_ID_UNIQUE STATX_SUBVOL STATX_WRITE_ATOMIC STATX_DIO_READ_ALIGN

Bitflags for use in the *mask* parameter to `os.statx`{.interpreted-text role="func"}. Some of these flags may be available even when their corresponding members in `statx_result`{.interpreted-text role="class"} are not available.

::: availability
Linux \>= 4.11 with glibc \>= 2.28.
:::

::: versionadded
3.15
:::
:::::

::::: data
AT_STATX_FORCE_SYNC

A flag for the `os.statx`{.interpreted-text role="func"} function. Requests that the kernel return up-to-date information even when doing so is expensive (for example, requiring a round trip to the server for a file on a network filesystem).

::: availability
Linux \>= 4.11 with glibc \>= 2.28.
:::

::: versionadded
3.15
:::
:::::

::::: data
AT_STATX_DONT_SYNC

A flag for the `os.statx`{.interpreted-text role="func"} function. Requests that the kernel return cached information if possible.

::: availability
Linux \>= 4.11 with glibc \>= 2.28.
:::

::: versionadded
3.15
:::
:::::

::::: data
AT_STATX_SYNC_AS_STAT

A flag for the `os.statx`{.interpreted-text role="func"} function. This flag is defined as `0`, so it has no effect, but it can be used to explicitly indicate neither `AT_STATX_FORCE_SYNC`{.interpreted-text role="data"} nor `AT_STATX_DONT_SYNC`{.interpreted-text role="data"} is being passed. In the absence of the other two flags, the kernel will generally return information as fresh as `os.stat`{.interpreted-text role="func"} would return.

::: availability
Linux \>= 4.11 with glibc \>= 2.28.
:::

::: versionadded
3.15
:::
:::::

::::: data
AT_NO_AUTOMOUNT

If the final component of a path is an automount point, operate on the automount point instead of performing the automount. On Linux, `os.stat`{.interpreted-text role="func"}, `os.fstat`{.interpreted-text role="func"} and `os.lstat`{.interpreted-text role="func"} always behave this way.

::: availability
Linux.
:::

::: versionadded
3.15
:::
:::::

::::::::: function
statvfs(path)

Perform a `!statvfs`{.interpreted-text role="c:func"} system call on the given path. The return value is an object whose attributes describe the filesystem on the given path, and correspond to the members of the `statvfs`{.interpreted-text role="c:struct"} structure, namely: `f_bsize`{.interpreted-text role="attr"}, `f_frsize`{.interpreted-text role="attr"}, `f_blocks`{.interpreted-text role="attr"}, `f_bfree`{.interpreted-text role="attr"}, `f_bavail`{.interpreted-text role="attr"}, `f_files`{.interpreted-text role="attr"}, `f_ffree`{.interpreted-text role="attr"}, `f_favail`{.interpreted-text role="attr"}, `f_flag`{.interpreted-text role="attr"}, `f_namemax`{.interpreted-text role="attr"}, `f_fsid`{.interpreted-text role="attr"}.

Two module-level constants are defined for the `f_flag`{.interpreted-text role="attr"} attribute\'s bit-flags: if `ST_RDONLY`{.interpreted-text role="const"} is set, the filesystem is mounted read-only, and if `ST_NOSUID`{.interpreted-text role="const"} is set, the semantics of setuid/setgid bits are disabled or not supported.

Additional module-level constants are defined for GNU/glibc based systems. These are `ST_NODEV`{.interpreted-text role="const"} (disallow access to device special files), `ST_NOEXEC`{.interpreted-text role="const"} (disallow program execution), `ST_SYNCHRONOUS`{.interpreted-text role="const"} (writes are synced at once), `ST_MANDLOCK`{.interpreted-text role="const"} (allow mandatory locks on an FS), `ST_WRITE`{.interpreted-text role="const"} (write on file/directory/symlink), `ST_APPEND`{.interpreted-text role="const"} (append-only file), `ST_IMMUTABLE`{.interpreted-text role="const"} (immutable file), `ST_NOATIME`{.interpreted-text role="const"} (do not update access times), `ST_NODIRATIME`{.interpreted-text role="const"} (do not update directory access times), `ST_RELATIME`{.interpreted-text role="const"} (update atime relative to mtime/ctime).

This function can support `specifying a file descriptor <path_fd>`{.interpreted-text role="ref"}.

::: availability
Unix.
:::

::: versionchanged
3.2 The `ST_RDONLY`{.interpreted-text role="const"} and `ST_NOSUID`{.interpreted-text role="const"} constants were added.
:::

::: versionchanged
3.3 Added support for specifying *path* as an open file descriptor.
:::

::: versionchanged
3.4 The `ST_NODEV`{.interpreted-text role="const"}, `ST_NOEXEC`{.interpreted-text role="const"}, `ST_SYNCHRONOUS`{.interpreted-text role="const"}, `ST_MANDLOCK`{.interpreted-text role="const"}, `ST_WRITE`{.interpreted-text role="const"}, `ST_APPEND`{.interpreted-text role="const"}, `ST_IMMUTABLE`{.interpreted-text role="const"}, `ST_NOATIME`{.interpreted-text role="const"}, `ST_NODIRATIME`{.interpreted-text role="const"}, and `ST_RELATIME`{.interpreted-text role="const"} constants were added.
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"}.
:::

::: versionchanged
3.7 Added the `f_fsid`{.interpreted-text role="attr"} attribute.
:::
:::::::::

:::: data
supports_dir_fd

A `set`{.interpreted-text role="class"} object indicating which functions in the `!os`{.interpreted-text role="mod"} module accept an open file descriptor for their *dir_fd* parameter. Different platforms provide different features, and the underlying functionality Python uses to implement the *dir_fd* parameter is not available on all platforms Python supports. For consistency\'s sake, functions that may support *dir_fd* always allow specifying the parameter, but will throw an exception if the functionality is used when it\'s not locally available. (Specifying `None` for *dir_fd* is always supported on all platforms.)

To check whether a particular function accepts an open file descriptor for its *dir_fd* parameter, use the `in` operator on `supports_dir_fd`. As an example, this expression evaluates to `True` if `os.stat`{.interpreted-text role="func"} accepts open file descriptors for *dir_fd* on the local platform:

    os.stat in os.supports_dir_fd

Currently *dir_fd* parameters only work on Unix platforms; none of them work on Windows.

::: versionadded
3.3
:::
::::

:::: data
supports_effective_ids

A `set`{.interpreted-text role="class"} object indicating whether `os.access`{.interpreted-text role="func"} permits specifying `True` for its *effective_ids* parameter on the local platform. (Specifying `False` for *effective_ids* is always supported on all platforms.) If the local platform supports it, the collection will contain `os.access`{.interpreted-text role="func"}; otherwise it will be empty.

This expression evaluates to `True` if `os.access`{.interpreted-text role="func"} supports `effective_ids=True` on the local platform:

    os.access in os.supports_effective_ids

Currently *effective_ids* is only supported on Unix platforms; it does not work on Windows.

::: versionadded
3.3
:::
::::

:::: data
supports_fd

A `set`{.interpreted-text role="class"} object indicating which functions in the `!os`{.interpreted-text role="mod"} module permit specifying their *path* parameter as an open file descriptor on the local platform. Different platforms provide different features, and the underlying functionality Python uses to accept open file descriptors as *path* arguments is not available on all platforms Python supports.

To determine whether a particular function permits specifying an open file descriptor for its *path* parameter, use the `in` operator on `supports_fd`. As an example, this expression evaluates to `True` if `os.chdir`{.interpreted-text role="func"} accepts open file descriptors for *path* on your local platform:

    os.chdir in os.supports_fd

::: versionadded
3.3
:::
::::

:::: data
supports_follow_symlinks

A `set`{.interpreted-text role="class"} object indicating which functions in the `!os`{.interpreted-text role="mod"} module accept `False` for their *follow_symlinks* parameter on the local platform. Different platforms provide different features, and the underlying functionality Python uses to implement *follow_symlinks* is not available on all platforms Python supports. For consistency\'s sake, functions that may support *follow_symlinks* always allow specifying the parameter, but will throw an exception if the functionality is used when it\'s not locally available. (Specifying `True` for *follow_symlinks* is always supported on all platforms.)

To check whether a particular function accepts `False` for its *follow_symlinks* parameter, use the `in` operator on `supports_follow_symlinks`. As an example, this expression evaluates to `True` if you may specify `follow_symlinks=False` when calling `os.stat`{.interpreted-text role="func"} on the local platform:

    os.stat in os.supports_follow_symlinks

::: versionadded
3.3
:::
::::

::::::::::: function
symlink(src, dst, target_is_directory=False, \*, dir_fd=None)

Create a symbolic link pointing to *src* named *dst*.

The *src* parameter refers to the target of the link (the file or directory being linked to), and *dst* is the name of the link being created.

On Windows, a symlink represents either a file or a directory, and does not morph to the target dynamically. If the target is present, the type of the symlink will be created to match. Otherwise, the symlink will be created as a directory if *target_is_directory* is `True` or a file symlink (the default) otherwise. On non-Windows platforms, *target_is_directory* is ignored.

This function can support `paths relative to directory descriptors
<dir_fd>`{.interpreted-text role="ref"}.

:::: note
::: title
Note
:::

On newer versions of Windows 10, unprivileged accounts can create symlinks if Developer Mode is enabled. When Developer Mode is not available/enabled, the *SeCreateSymbolicLinkPrivilege* privilege is required, or the process must be run as an administrator.

`OSError`{.interpreted-text role="exc"} is raised when the function is called by an unprivileged user.
::::

::: audit-event
os.symlink src,dst,dir_fd os.symlink
:::

::: availability
Unix, Windows.

The function is limited on WASI, see `wasm-availability`{.interpreted-text role="ref"} for more information.
:::

::: versionchanged
3.2 Added support for Windows 6.0 (Vista) symbolic links.
:::

::: versionchanged
3.3 Added the *dir_fd* parameter, and now allow *target_is_directory* on non-Windows platforms.
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"} for *src* and *dst*.
:::

::: versionchanged
3.8 Added support for unelevated symlinks on Windows with Developer Mode.
:::
:::::::::::

::::: function
sync()

Force write of everything to disk.

::: availability
Unix.
:::

::: versionadded
3.3
:::
:::::

:::::::: function
truncate(path, length)

Truncate the file corresponding to *path*, so that it is at most *length* bytes in size.

This function can support `specifying a file descriptor <path_fd>`{.interpreted-text role="ref"}.

::: audit-event
os.truncate path,length os.truncate
:::

::: availability
Unix, Windows.
:::

::: versionadded
3.3
:::

::: versionchanged
3.5 Added support for Windows
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"}.
:::
::::::::

:::::: function
unlink(path, \*, dir_fd=None)

Remove (delete) the file *path*. This function is semantically identical to `remove`{.interpreted-text role="func"}; the `unlink` name is its traditional Unix name. Please see the documentation for `remove`{.interpreted-text role="func"} for further information.

::: audit-event
os.remove path,dir_fd os.unlink
:::

::: versionchanged
3.3 Added the *dir_fd* parameter.
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"}.
:::
::::::

::::::: function
utime(path, times=None, \*\[, ns\], dir_fd=None, follow_symlinks=True)

Set the access and modified times of the file specified by *path*.

`utime`{.interpreted-text role="func"} takes two optional parameters, *times* and *ns*. These specify the times set on *path* and are used as follows:

- If *ns* is specified, it must be a 2-tuple of the form `(atime_ns, mtime_ns)` where each member is an int expressing nanoseconds.
- If *times* is not `None`, it must be a 2-tuple of the form `(atime, mtime)` where each member is a real number expressing seconds, rounded down to nanoseconds.
- If *times* is `None` and *ns* is unspecified, this is equivalent to specifying `ns=(atime_ns, mtime_ns)` where both times are the current time.

It is an error to specify tuples for both *times* and *ns*.

Note that the exact times you set here may not be returned by a subsequent `~os.stat`{.interpreted-text role="func"} call, depending on the resolution with which your operating system records access and modification times; see `~os.stat`{.interpreted-text role="func"}. The best way to preserve exact times is to use the *st_atime_ns* and *st_mtime_ns* fields from the `os.stat`{.interpreted-text role="func"} result object with the *ns* parameter to `utime`{.interpreted-text role="func"}.

This function can support `specifying a file descriptor <path_fd>`{.interpreted-text role="ref"}, `paths relative to directory descriptors <dir_fd>`{.interpreted-text role="ref"} and `not
following symlinks <follow_symlinks>`{.interpreted-text role="ref"}.

::: audit-event
os.utime path,times,ns,dir_fd os.utime
:::

::: versionchanged
3.3 Added support for specifying *path* as an open file descriptor, and the *dir_fd*, *follow_symlinks*, and *ns* parameters.
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"}.
:::

::: versionchanged
3.15 Accepts any real numbers as *times*, not only integers or floats.
:::
:::::::

::::::::::: function
walk(top, topdown=True, onerror=None, followlinks=False)

::: index
single: directory; walking single: directory; traversal
:::

Generate the file names in a directory tree by walking the tree either top-down or bottom-up. For each directory in the tree rooted at directory *top* (including *top* itself), it yields a 3-tuple `(dirpath, dirnames, filenames)`.

*dirpath* is a string, the path to the directory. *dirnames* is a list of the names of the subdirectories in *dirpath* (including symlinks to directories, and excluding `'.'` and `'..'`). *filenames* is a list of the names of the non-directory files in *dirpath*. Note that the names in the lists contain no path components. To get a full path (which begins with *top*) to a file or directory in *dirpath*, do `os.path.join(dirpath, name)`. Whether or not the lists are sorted depends on the file system. If a file is removed from or added to the *dirpath* directory during generating the lists, whether a name for that file be included is unspecified.

If optional argument *topdown* is `True` or not specified, the triple for a directory is generated before the triples for any of its subdirectories (directories are generated top-down). If *topdown* is `False`, the triple for a directory is generated after the triples for all of its subdirectories (directories are generated bottom-up). No matter the value of *topdown*, the list of subdirectories is retrieved before the tuples for the directory and its subdirectories are generated.

When *topdown* is `True`, the caller can modify the *dirnames* list in-place (perhaps using `del`{.interpreted-text role="keyword"} or slice assignment), and `walk`{.interpreted-text role="func"} will only recurse into the subdirectories whose names remain in *dirnames*; this can be used to prune the search, impose a specific order of visiting, or even to inform `walk`{.interpreted-text role="func"} about directories the caller creates or renames before it resumes `walk`{.interpreted-text role="func"} again. Modifying *dirnames* when *topdown* is `False` has no effect on the behavior of the walk, because in bottom-up mode the directories in *dirnames* are generated before *dirpath* itself is generated.

By default, errors from the `scandir`{.interpreted-text role="func"} call are ignored. If optional argument *onerror* is specified, it should be a function; it will be called with one argument, an `OSError`{.interpreted-text role="exc"} instance. It can report the error to continue with the walk, or raise the exception to abort the walk. Note that the filename is available as the `filename` attribute of the exception object.

By default, `walk`{.interpreted-text role="func"} will not walk down into symbolic links that resolve to directories. Set *followlinks* to `True` to visit directories pointed to by symlinks, on systems that support them.

:::: note
::: title
Note
:::

Be aware that setting *followlinks* to `True` can lead to infinite recursion if a link points to a parent directory of itself. `walk`{.interpreted-text role="func"} does not keep track of the directories it visited already.
::::

:::: note
::: title
Note
:::

If you pass a relative pathname, don\'t change the current working directory between resumptions of `walk`{.interpreted-text role="func"}. `walk`{.interpreted-text role="func"} never changes the current directory, and assumes that its caller doesn\'t either.
::::

This example displays the number of bytes taken by non-directory files in each directory under the starting directory, except that it doesn\'t look under any `__pycache__` subdirectory:

    import os
    from os.path import join, getsize
    for root, dirs, files in os.walk('python/Lib/xml'):
        print(root, "consumes", end=" ")
        print(sum(getsize(join(root, name)) for name in files), end=" ")
        print("bytes in", len(files), "non-directory files")
        if '__pycache__' in dirs:
            dirs.remove('__pycache__')  # don't visit __pycache__ directories

In the next example (simple implementation of `shutil.rmtree`{.interpreted-text role="func"}), walking the tree bottom-up is essential, `rmdir`{.interpreted-text role="func"} doesn\'t allow deleting a directory before the directory is empty:

    # Delete everything reachable from the directory named in "top",
    # assuming there are no symbolic links.
    # CAUTION:  This is dangerous!  For example, if top == '/', it
    # could delete all your disk files.
    import os
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(top)

::: audit-event
os.walk top,topdown,onerror,followlinks os.walk
:::

::: versionchanged
3.5 This function now calls `os.scandir`{.interpreted-text role="func"} instead of `os.listdir`{.interpreted-text role="func"}, making it faster by reducing the number of calls to `os.stat`{.interpreted-text role="func"}.
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"}.
:::
:::::::::::

::::::::::: function
fwalk(top=\'.\', topdown=True, onerror=None, \*, follow_symlinks=False, dir_fd=None)

::: index
single: directory; walking single: directory; traversal
:::

This behaves exactly like `walk`{.interpreted-text role="func"}, except that it yields a 4-tuple `(dirpath, dirnames, filenames, dirfd)`, and it supports `dir_fd`.

*dirpath*, *dirnames* and *filenames* are identical to `walk`{.interpreted-text role="func"} output, and *dirfd* is a file descriptor referring to the directory *dirpath*.

This function always supports `paths relative to directory descriptors
<dir_fd>`{.interpreted-text role="ref"} and `not following symlinks <follow_symlinks>`{.interpreted-text role="ref"}. Note however that, unlike other functions, the `fwalk`{.interpreted-text role="func"} default value for *follow_symlinks* is `False`.

:::: note
::: title
Note
:::

Since `fwalk`{.interpreted-text role="func"} yields file descriptors, those are only valid until the next iteration step, so you should duplicate them (e.g. with `dup`{.interpreted-text role="func"}) if you want to keep them longer.
::::

This example displays the number of bytes taken by non-directory files in each directory under the starting directory, except that it doesn\'t look under any `__pycache__` subdirectory:

    import os
    for root, dirs, files, rootfd in os.fwalk('python/Lib/xml'):
        print(root, "consumes", end=" ")
        print(sum([os.stat(name, dir_fd=rootfd).st_size for name in files]),
              end=" ")
        print("bytes in", len(files), "non-directory files")
        if '__pycache__' in dirs:
            dirs.remove('__pycache__')  # don't visit __pycache__ directories

In the next example, walking the tree bottom-up is essential: `rmdir`{.interpreted-text role="func"} doesn\'t allow deleting a directory before the directory is empty:

    # Delete everything reachable from the directory named in "top",
    # assuming there are no symbolic links.
    # CAUTION:  This is dangerous!  For example, if top == '/', it
    # could delete all your disk files.
    import os
    for root, dirs, files, rootfd in os.fwalk(top, topdown=False):
        for name in files:
            os.unlink(name, dir_fd=rootfd)
        for name in dirs:
            os.rmdir(name, dir_fd=rootfd)

::: audit-event
os.fwalk top,topdown,onerror,follow_symlinks,dir_fd os.fwalk
:::

::: availability
Unix.
:::

::: versionadded
3.3
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"}.
:::

::: versionchanged
3.7 Added support for `bytes`{.interpreted-text role="class"} paths.
:::
:::::::::::

::::: function
memfd_create(name\[, flags=os.MFD_CLOEXEC\])

Create an anonymous file and return a file descriptor that refers to it. *flags* must be one of the `os.MFD_*` constants available on the system (or a bitwise ORed combination of them). By default, the new file descriptor is `non-inheritable <fd_inheritance>`{.interpreted-text role="ref"}.

The name supplied in *name* is used as a filename and will be displayed as the target of the corresponding symbolic link in the directory `/proc/self/fd/`. The displayed name is always prefixed with `memfd:` and serves only for debugging purposes. Names do not affect the behavior of the file descriptor, and as such multiple files can have the same name without any side effects.

::: availability
Linux \>= 3.17 with glibc \>= 2.27.
:::

::: versionadded
3.8
:::
:::::

::::: data
MFD_CLOEXEC MFD_ALLOW_SEALING MFD_HUGETLB MFD_HUGE_SHIFT MFD_HUGE_MASK MFD_HUGE_64KB MFD_HUGE_512KB MFD_HUGE_1MB MFD_HUGE_2MB MFD_HUGE_8MB MFD_HUGE_16MB MFD_HUGE_32MB MFD_HUGE_256MB MFD_HUGE_512MB MFD_HUGE_1GB MFD_HUGE_2GB MFD_HUGE_16GB

These flags can be passed to `memfd_create`{.interpreted-text role="func"}.

::: availability
Linux \>= 3.17 with glibc \>= 2.27

The `MFD_HUGE*` flags are only available since Linux 4.14.
:::

::: versionadded
3.8
:::
:::::

::::: function
eventfd(initval\[, flags=os.EFD_CLOEXEC\])

Create and return an event file descriptor. The file descriptors supports raw `read`{.interpreted-text role="func"} and `write`{.interpreted-text role="func"} with a buffer size of 8, `~select.select`{.interpreted-text role="func"}, `~select.poll`{.interpreted-text role="func"} and similar. See man page `eventfd(2)`{.interpreted-text role="manpage"} for more information. By default, the new file descriptor is `non-inheritable <fd_inheritance>`{.interpreted-text role="ref"}.

*initval* is the initial value of the event counter. The initial value must be a 32 bit unsigned integer. Please note that the initial value is limited to a 32 bit unsigned int although the event counter is an unsigned 64 bit integer with a maximum value of 2^64^-2.

*flags* can be constructed from `EFD_CLOEXEC`{.interpreted-text role="const"}, `EFD_NONBLOCK`{.interpreted-text role="const"}, and `EFD_SEMAPHORE`{.interpreted-text role="const"}.

If `EFD_SEMAPHORE`{.interpreted-text role="const"} is specified and the event counter is non-zero, `eventfd_read`{.interpreted-text role="func"} returns 1 and decrements the counter by one.

If `EFD_SEMAPHORE`{.interpreted-text role="const"} is not specified and the event counter is non-zero, `eventfd_read`{.interpreted-text role="func"} returns the current event counter value and resets the counter to zero.

If the event counter is zero and `EFD_NONBLOCK`{.interpreted-text role="const"} is not specified, `eventfd_read`{.interpreted-text role="func"} blocks.

`eventfd_write`{.interpreted-text role="func"} increments the event counter. Write blocks if the write operation would increment the counter to a value larger than 2^64^-2.

Example:

    import os

    # semaphore with start value '1'
    fd = os.eventfd(1, os.EFD_SEMAPHORE | os.EFD_CLOEXEC)
    try:
        # acquire semaphore
        v = os.eventfd_read(fd)
        try:
            do_work()
        finally:
            # release semaphore
            os.eventfd_write(fd, v)
    finally:
        os.close(fd)

::: availability
Linux \>= 2.6.27 with glibc \>= 2.8
:::

::: versionadded
3.10
:::
:::::

::::: function
eventfd_read(fd)

Read value from an `eventfd`{.interpreted-text role="func"} file descriptor and return a 64 bit unsigned int. The function does not verify that *fd* is an `eventfd`{.interpreted-text role="func"}.

::: availability
Linux \>= 2.6.27
:::

::: versionadded
3.10
:::
:::::

::::: function
eventfd_write(fd, value)

Add value to an `eventfd`{.interpreted-text role="func"} file descriptor. *value* must be a 64 bit unsigned int. The function does not verify that *fd* is an `eventfd`{.interpreted-text role="func"}.

::: availability
Linux \>= 2.6.27
:::

::: versionadded
3.10
:::
:::::

::::: data
EFD_CLOEXEC

Set close-on-exec flag for new `eventfd`{.interpreted-text role="func"} file descriptor.

::: availability
Linux \>= 2.6.27
:::

::: versionadded
3.10
:::
:::::

::::: data
EFD_NONBLOCK

Set `O_NONBLOCK`{.interpreted-text role="const"} status flag for new `eventfd`{.interpreted-text role="func"} file descriptor.

::: availability
Linux \>= 2.6.27
:::

::: versionadded
3.10
:::
:::::

::::: data
EFD_SEMAPHORE

Provide semaphore-like semantics for reads from an `eventfd`{.interpreted-text role="func"} file descriptor. On read the internal counter is decremented by one.

::: availability
Linux \>= 2.6.30
:::

::: versionadded
3.10
:::
:::::

### Timer File Descriptors {#os-timerfd}

::: versionadded
3.13
:::

These functions provide support for Linux\'s *timer file descriptor* API. Naturally, they are all only available on Linux.

:::::: function
timerfd_create(clockid, /, \*, flags=0)

Create and return a timer file descriptor (*timerfd*).

The file descriptor returned by `timerfd_create`{.interpreted-text role="func"} supports:

- `read`{.interpreted-text role="func"}
- `~select.select`{.interpreted-text role="func"}
- `~select.poll`{.interpreted-text role="func"}

The file descriptor\'s `read`{.interpreted-text role="func"} method can be called with a buffer size of 8. If the timer has already expired one or more times, `read`{.interpreted-text role="func"} returns the number of expirations with the host\'s endianness, which may be converted to an `int`{.interpreted-text role="class"} by `int.from_bytes(x, byteorder=sys.byteorder)`.

`~select.select`{.interpreted-text role="func"} and `~select.poll`{.interpreted-text role="func"} can be used to wait until timer expires and the file descriptor is readable.

*clockid* must be a valid `clock ID <time-clock-id-constants>`{.interpreted-text role="ref"}, as defined in the `time`{.interpreted-text role="py:mod"} module:

- `time.CLOCK_REALTIME`{.interpreted-text role="const"}
- `time.CLOCK_MONOTONIC`{.interpreted-text role="const"}
- `time.CLOCK_BOOTTIME`{.interpreted-text role="const"} (Since Linux 3.15 for timerfd_create)

If *clockid* is `time.CLOCK_REALTIME`{.interpreted-text role="const"}, a settable system-wide real-time clock is used. If system clock is changed, timer setting need to be updated. To cancel timer when system clock is changed, see `TFD_TIMER_CANCEL_ON_SET`{.interpreted-text role="const"}.

If *clockid* is `time.CLOCK_MONOTONIC`{.interpreted-text role="const"}, a non-settable monotonically increasing clock is used. Even if the system clock is changed, the timer setting will not be affected.

If *clockid* is `time.CLOCK_BOOTTIME`{.interpreted-text role="const"}, same as `time.CLOCK_MONOTONIC`{.interpreted-text role="const"} except it includes any time that the system is suspended.

The file descriptor\'s behaviour can be modified by specifying a *flags* value. Any of the following variables may be used, combined using bitwise OR (the `|` operator):

- `TFD_NONBLOCK`{.interpreted-text role="const"}
- `TFD_CLOEXEC`{.interpreted-text role="const"}

If `TFD_NONBLOCK`{.interpreted-text role="const"} is not set as a flag, `read`{.interpreted-text role="func"} blocks until the timer expires. If it is set as a flag, `read`{.interpreted-text role="func"} doesn\'t block, but If there hasn\'t been an expiration since the last call to read, `read`{.interpreted-text role="func"} raises `OSError`{.interpreted-text role="class"} with `errno` is set to `errno.EAGAIN`{.interpreted-text role="const"}.

`TFD_CLOEXEC`{.interpreted-text role="const"} is always set by Python automatically.

The file descriptor must be closed with `os.close`{.interpreted-text role="func"} when it is no longer needed, or else the file descriptor will be leaked.

::: seealso
The `timerfd_create(2)`{.interpreted-text role="manpage"} man page.
:::

::: availability
Linux \>= 2.6.27 with glibc \>= 2.8
:::

::: versionadded
3.13
:::
::::::

:::::: function
timerfd_settime(fd, /, \*, flags=flags, initial=0.0, interval=0.0)

Alter a timer file descriptor\'s internal timer. This function operates the same interval timer as `timerfd_settime_ns`{.interpreted-text role="func"}.

*fd* must be a valid timer file descriptor.

The timer\'s behaviour can be modified by specifying a *flags* value. Any of the following variables may be used, combined using bitwise OR (the `|` operator):

- `TFD_TIMER_ABSTIME`{.interpreted-text role="const"}
- `TFD_TIMER_CANCEL_ON_SET`{.interpreted-text role="const"}

The timer is disabled by setting *initial* to zero (`0`). If *initial* is equal to or greater than zero, the timer is enabled. If *initial* is less than zero, it raises an `OSError`{.interpreted-text role="class"} exception with `errno` set to `errno.EINVAL`{.interpreted-text role="const"}

By default the timer will fire when *initial* seconds have elapsed. (If *initial* is zero, timer will fire immediately.)

However, if the `TFD_TIMER_ABSTIME`{.interpreted-text role="const"} flag is set, the timer will fire when the timer\'s clock (set by *clockid* in `timerfd_create`{.interpreted-text role="func"}) reaches *initial* seconds.

The timer\'s interval is set by the *interval* real number. If *interval* is zero, the timer only fires once, on the initial expiration. If *interval* is greater than zero, the timer fires every time *interval* seconds have elapsed since the previous expiration. If *interval* is less than zero, it raises `OSError`{.interpreted-text role="class"} with `errno` set to `errno.EINVAL`{.interpreted-text role="const"}

If the `TFD_TIMER_CANCEL_ON_SET`{.interpreted-text role="const"} flag is set along with `TFD_TIMER_ABSTIME`{.interpreted-text role="const"} and the clock for this timer is `time.CLOCK_REALTIME`{.interpreted-text role="const"}, the timer is marked as cancelable if the real-time clock is changed discontinuously. Reading the descriptor is aborted with the error ECANCELED.

Linux manages system clock as UTC. A daylight-savings time transition is done by changing time offset only and doesn\'t cause discontinuous system clock change.

Discontinuous system clock change will be caused by the following events:

- `settimeofday`
- `clock_settime`
- set the system date and time by `date` command

Return a two-item tuple of (`next_expiration`, `interval`) from the previous timer state, before this function executed.

::: seealso
`timerfd_create(2)`{.interpreted-text role="manpage"}, `timerfd_settime(2)`{.interpreted-text role="manpage"}, `settimeofday(2)`{.interpreted-text role="manpage"}, `clock_settime(2)`{.interpreted-text role="manpage"}, and `date(1)`{.interpreted-text role="manpage"}.
:::

::: availability
Linux \>= 2.6.27 with glibc \>= 2.8
:::

::: versionadded
3.13
:::
::::::

::::: function
timerfd_settime_ns(fd, /, \*, flags=0, initial=0, interval=0)

Similar to `timerfd_settime`{.interpreted-text role="func"}, but use time as nanoseconds. This function operates the same interval timer as `timerfd_settime`{.interpreted-text role="func"}.

::: availability
Linux \>= 2.6.27 with glibc \>= 2.8
:::

::: versionadded
3.13
:::
:::::

:::::: function
timerfd_gettime(fd, /)

Return a two-item tuple of floats (`next_expiration`, `interval`).

`next_expiration` denotes the relative time until the timer next fires, regardless of if the `TFD_TIMER_ABSTIME`{.interpreted-text role="const"} flag is set.

`interval` denotes the timer\'s interval. If zero, the timer will only fire once, after `next_expiration` seconds have elapsed.

::: seealso
`timerfd_gettime(2)`{.interpreted-text role="manpage"}
:::

::: availability
Linux \>= 2.6.27 with glibc \>= 2.8
:::

::: versionadded
3.13
:::
::::::

::::: function
timerfd_gettime_ns(fd, /)

Similar to `timerfd_gettime`{.interpreted-text role="func"}, but return time as nanoseconds.

::: availability
Linux \>= 2.6.27 with glibc \>= 2.8
:::

::: versionadded
3.13
:::
:::::

::::: data
TFD_NONBLOCK

A flag for the `timerfd_create`{.interpreted-text role="func"} function, which sets the `O_NONBLOCK`{.interpreted-text role="const"} status flag for the new timer file descriptor. If `TFD_NONBLOCK`{.interpreted-text role="const"} is not set as a flag, `read`{.interpreted-text role="func"} blocks.

::: availability
Linux \>= 2.6.27 with glibc \>= 2.8
:::

::: versionadded
3.13
:::
:::::

::::: data
TFD_CLOEXEC

A flag for the `timerfd_create`{.interpreted-text role="func"} function, If `TFD_CLOEXEC`{.interpreted-text role="const"} is set as a flag, set close-on-exec flag for new file descriptor.

::: availability
Linux \>= 2.6.27 with glibc \>= 2.8
:::

::: versionadded
3.13
:::
:::::

::::: data
TFD_TIMER_ABSTIME

A flag for the `timerfd_settime`{.interpreted-text role="func"} and `timerfd_settime_ns`{.interpreted-text role="func"} functions. If this flag is set, *initial* is interpreted as an absolute value on the timer\'s clock (in UTC seconds or nanoseconds since the Unix Epoch).

::: availability
Linux \>= 2.6.27 with glibc \>= 2.8
:::

::: versionadded
3.13
:::
:::::

::::: data
TFD_TIMER_CANCEL_ON_SET

A flag for the `timerfd_settime`{.interpreted-text role="func"} and `timerfd_settime_ns`{.interpreted-text role="func"} functions along with `TFD_TIMER_ABSTIME`{.interpreted-text role="const"}. The timer is cancelled when the time of the underlying clock changes discontinuously.

::: availability
Linux \>= 2.6.27 with glibc \>= 2.8
:::

::: versionadded
3.13
:::
:::::

### Linux extended attributes

::: versionadded
3.3
:::

These functions are all available on Linux only.

::::: function
getxattr(path, attribute, \*, follow_symlinks=True)

Return the value of the extended filesystem attribute *attribute* for *path*. *attribute* can be bytes or str (directly or indirectly through the `PathLike`{.interpreted-text role="class"} interface). If it is str, it is encoded with the filesystem encoding.

This function can support `specifying a file descriptor <path_fd>`{.interpreted-text role="ref"} and `not following symlinks <follow_symlinks>`{.interpreted-text role="ref"}.

::: audit-event
os.getxattr path,attribute os.getxattr
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"} for *path* and *attribute*.
:::
:::::

::::: function
listxattr(path=None, \*, follow_symlinks=True)

Return a list of the extended filesystem attributes on *path*. The attributes in the list are represented as strings decoded with the filesystem encoding. If *path* is `None`, `listxattr`{.interpreted-text role="func"} will examine the current directory.

This function can support `specifying a file descriptor <path_fd>`{.interpreted-text role="ref"} and `not following symlinks <follow_symlinks>`{.interpreted-text role="ref"}.

::: audit-event
os.listxattr path os.listxattr
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"}.
:::
:::::

::::: function
removexattr(path, attribute, \*, follow_symlinks=True)

Removes the extended filesystem attribute *attribute* from *path*. *attribute* should be bytes or str (directly or indirectly through the `PathLike`{.interpreted-text role="class"} interface). If it is a string, it is encoded with the `filesystem encoding and error handler`{.interpreted-text role="term"}.

This function can support `specifying a file descriptor <path_fd>`{.interpreted-text role="ref"} and `not following symlinks <follow_symlinks>`{.interpreted-text role="ref"}.

::: audit-event
os.removexattr path,attribute os.removexattr
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"} for *path* and *attribute*.
:::
:::::

::::::: function
setxattr(path, attribute, value, flags=0, \*, follow_symlinks=True)

Set the extended filesystem attribute *attribute* on *path* to *value*. *attribute* must be a bytes or str with no embedded NULs (directly or indirectly through the `PathLike`{.interpreted-text role="class"} interface). If it is a str, it is encoded with the `filesystem encoding and error handler`{.interpreted-text role="term"}. *flags* may be `XATTR_REPLACE`{.interpreted-text role="data"} or `XATTR_CREATE`{.interpreted-text role="data"}. If `XATTR_REPLACE`{.interpreted-text role="data"} is given and the attribute does not exist, `ENODATA` will be raised. If `XATTR_CREATE`{.interpreted-text role="data"} is given and the attribute already exists, the attribute will not be created and `EEXISTS` will be raised.

This function can support `specifying a file descriptor <path_fd>`{.interpreted-text role="ref"} and `not following symlinks <follow_symlinks>`{.interpreted-text role="ref"}.

:::: note
::: title
Note
:::

A bug in Linux kernel versions less than 2.6.39 caused the flags argument to be ignored on some filesystems.
::::

::: audit-event
os.setxattr path,attribute,value,flags os.setxattr
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"} for *path* and *attribute*.
:::
:::::::

::: data
XATTR_SIZE_MAX

The maximum size the value of an extended attribute can be. Currently, this is 64 KiB on Linux.
:::

::: data
XATTR_CREATE

This is a possible value for the flags argument in `setxattr`{.interpreted-text role="func"}. It indicates the operation must create an attribute.
:::

::: data
XATTR_REPLACE

This is a possible value for the flags argument in `setxattr`{.interpreted-text role="func"}. It indicates the operation must replace an existing attribute.
:::

## Process Management {#os-process}

These functions may be used to create and manage processes.

The various `exec\* <execl>`{.interpreted-text role="func"} functions take a list of arguments for the new program loaded into the process. In each case, the first of these arguments is passed to the new program as its own name rather than as an argument a user may have typed on a command line. For the C programmer, this is the `argv[0]` passed to a program\'s `main`{.interpreted-text role="c:func"}. For example, `os.execv('/bin/echo', ['foo', 'bar'])` will only print `bar` on standard output; `foo` will seem to be ignored.

::: function
abort()

Generate a `~signal.SIGABRT`{.interpreted-text role="const"} signal to the current process. On Unix, the default behavior is to produce a core dump; on Windows, the process immediately returns an exit code of `3`. Be aware that calling this function will not call the Python signal handler registered for `~signal.SIGABRT`{.interpreted-text role="const"} with `signal.signal`{.interpreted-text role="func"}.
:::

:::::: function
add_dll_directory(path)

Add a path to the DLL search path.

This search path is used when resolving dependencies for imported extension modules (the module itself is resolved through `sys.path`{.interpreted-text role="data"}), and also by `ctypes`{.interpreted-text role="mod"}.

Remove the directory by calling **close()** on the returned object or using it in a `with`{.interpreted-text role="keyword"} statement.

See the [Microsoft documentation](https://msdn.microsoft.com/44228cf2-6306-466c-8f16-f513cd3ba8b5) for more information about how DLLs are loaded.

::: audit-event
os.add_dll_directory path os.add_dll_directory
:::

::: availability
Windows.
:::

::: versionadded
3.8 Previous versions of CPython would resolve DLLs using the default behavior for the current process. This led to inconsistencies, such as only sometimes searching `PATH`{.interpreted-text role="envvar"} or the current working directory, and OS functions such as `AddDllDirectory` having no effect.

In 3.8, the two primary ways DLLs are loaded now explicitly override the process-wide behavior to ensure consistency. See the `porting notes <bpo-36085-whatsnew>`{.interpreted-text role="ref"} for information on updating libraries.
:::
::::::

::::::: function
execl(path, arg0, arg1, \...) execle(path, arg0, arg1, \..., env) execlp(file, arg0, arg1, \...) execlpe(file, arg0, arg1, \..., env) execv(path, args) execve(path, args, env) execvp(file, args) execvpe(file, args, env)

These functions all execute a new program, replacing the current process; they do not return. On Unix, the new executable is loaded into the current process, and will have the same process id as the caller. Errors will be reported as `OSError`{.interpreted-text role="exc"} exceptions.

The current process is replaced immediately. Open file objects and descriptors are not flushed, so if there may be data buffered on these open files, you should flush them using `sys.stdout.flush`{.interpreted-text role="func"} or `os.fsync`{.interpreted-text role="func"} before calling an `exec\* <execl>`{.interpreted-text role="func"} function.

The \"l\" and \"v\" variants of the `exec\* <execl>`{.interpreted-text role="func"} functions differ in how command-line arguments are passed. The \"l\" variants are perhaps the easiest to work with if the number of parameters is fixed when the code is written; the individual parameters simply become additional parameters to the `!execl\*`{.interpreted-text role="func"} functions. The \"v\" variants are good when the number of parameters is variable, with the arguments being passed in a list or tuple as the *args* parameter. In either case, the arguments to the child process should start with the name of the command being run, but this is not enforced.

The variants which include a \"p\" near the end (`execlp`{.interpreted-text role="func"}, `execlpe`{.interpreted-text role="func"}, `execvp`{.interpreted-text role="func"}, and `execvpe`{.interpreted-text role="func"}) will use the `PATH`{.interpreted-text role="envvar"} environment variable to locate the program *file*. When the environment is being replaced (using one of the `exec\*e <execl>`{.interpreted-text role="func"} variants, discussed in the next paragraph), the new environment is used as the source of the `PATH`{.interpreted-text role="envvar"} variable. The other variants, `execl`{.interpreted-text role="func"}, `execle`{.interpreted-text role="func"}, `execv`{.interpreted-text role="func"}, and `execve`{.interpreted-text role="func"}, will not use the `PATH`{.interpreted-text role="envvar"} variable to locate the executable; *path* must contain an appropriate absolute or relative path. Relative paths must include at least one slash, even on Windows, as plain names will not be resolved.

For `execle`{.interpreted-text role="func"}, `execlpe`{.interpreted-text role="func"}, `execve`{.interpreted-text role="func"}, and `execvpe`{.interpreted-text role="func"} (note that these all end in \"e\"), the *env* parameter must be a mapping which is used to define the environment variables for the new process (these are used instead of the current process\' environment); the functions `execl`{.interpreted-text role="func"}, `execlp`{.interpreted-text role="func"}, `execv`{.interpreted-text role="func"}, and `execvp`{.interpreted-text role="func"} all cause the new process to inherit the environment of the current process.

For `execve`{.interpreted-text role="func"} on some platforms, *path* may also be specified as an open file descriptor. This functionality may not be supported on your platform; you can check whether or not it is available using `os.supports_fd`{.interpreted-text role="data"}. If it is unavailable, using it will raise a `NotImplementedError`{.interpreted-text role="exc"}.

::: audit-event
os.exec path,args,env os.execl
:::

::: availability
Unix, Windows, not WASI, not Android, not iOS.
:::

::: versionchanged
3.3 Added support for specifying *path* as an open file descriptor for `execve`{.interpreted-text role="func"}.
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"}.
:::
:::::::

::::: function
[exit]{#exit}(n)

Exit the process with status *n*, without calling cleanup handlers, flushing stdio buffers, etc.

:::: note
::: title
Note
:::

The standard way to exit is `sys.exit(n) <sys.exit>`{.interpreted-text role="func"}. `!_exit`{.interpreted-text role="func"} should normally only be used in the child process after a `fork`{.interpreted-text role="func"}.
::::
:::::

The following exit codes are defined and can be used with `_exit`{.interpreted-text role="func"}, although they are not required. These are typically used for system programs written in Python, such as a mail server\'s external command delivery program.

:::: note
::: title
Note
:::

Some of these may not be available on all Unix platforms, since there is some variation. These constants are defined where they are defined by the underlying platform.
::::

:::: data
EX_OK

Exit code that means no error occurred. May be taken from the defined value of `EXIT_SUCCESS` on some platforms. Generally has a value of zero.

::: availability
Unix, Windows.
:::
::::

:::: data
EX_USAGE

Exit code that means the command was used incorrectly, such as when the wrong number of arguments are given.

::: availability
Unix, not WASI.
:::
::::

:::: data
EX_DATAERR

Exit code that means the input data was incorrect.

::: availability
Unix, not WASI.
:::
::::

:::: data
EX_NOINPUT

Exit code that means an input file did not exist or was not readable.

::: availability
Unix, not WASI.
:::
::::

:::: data
EX_NOUSER

Exit code that means a specified user did not exist.

::: availability
Unix, not WASI.
:::
::::

:::: data
EX_NOHOST

Exit code that means a specified host did not exist.

::: availability
Unix, not WASI.
:::
::::

:::: data
EX_UNAVAILABLE

Exit code that means that a required service is unavailable.

::: availability
Unix, not WASI.
:::
::::

:::: data
EX_SOFTWARE

Exit code that means an internal software error was detected.

::: availability
Unix, not WASI.
:::
::::

:::: data
EX_OSERR

Exit code that means an operating system error was detected, such as the inability to fork or create a pipe.

::: availability
Unix, not WASI.
:::
::::

:::: data
EX_OSFILE

Exit code that means some system file did not exist, could not be opened, or had some other kind of error.

::: availability
Unix, not WASI.
:::
::::

:::: data
EX_CANTCREAT

Exit code that means a user specified output file could not be created.

::: availability
Unix, not WASI.
:::
::::

:::: data
EX_IOERR

Exit code that means that an error occurred while doing I/O on some file.

::: availability
Unix, not WASI.
:::
::::

:::: data
EX_TEMPFAIL

Exit code that means a temporary failure occurred. This indicates something that may not really be an error, such as a network connection that couldn\'t be made during a retryable operation.

::: availability
Unix, not WASI.
:::
::::

:::: data
EX_PROTOCOL

Exit code that means that a protocol exchange was illegal, invalid, or not understood.

::: availability
Unix, not WASI.
:::
::::

:::: data
EX_NOPERM

Exit code that means that there were insufficient permissions to perform the operation (but not intended for file system problems).

::: availability
Unix, not WASI.
:::
::::

:::: data
EX_CONFIG

Exit code that means that some kind of configuration error occurred.

::: availability
Unix, not WASI.
:::
::::

:::: data
EX_NOTFOUND

Exit code that means something like \"an entry was not found\".

::: availability
Unix, not WASI.
:::
::::

::::::::::: function
fork()

Fork a child process. Return `0` in the child and the child\'s process id in the parent. If an error occurs `OSError`{.interpreted-text role="exc"} is raised.

Note that some platforms including FreeBSD \<= 6.3 and Cygwin have known issues when using `fork()` from a thread.

::: audit-event
os.fork \"\" os.fork
:::

:::: warning
::: title
Warning
:::

If you use TLS sockets in an application calling `fork()`, see the warning in the `ssl`{.interpreted-text role="mod"} documentation.
::::

:::: warning
::: title
Warning
:::

On macOS the use of this function is unsafe when mixed with using higher-level system APIs, and that includes using `urllib.request`{.interpreted-text role="mod"}.
::::

::: versionchanged
3.8 Calling `fork()` in a subinterpreter is no longer supported (`RuntimeError`{.interpreted-text role="exc"} is raised).
:::

::: versionchanged
3.12 If Python is able to detect that your process has multiple threads, `os.fork`{.interpreted-text role="func"} now raises a `DeprecationWarning`{.interpreted-text role="exc"}.

We chose to surface this as a warning, when detectable, to better inform developers of a design problem that the POSIX platform specifically notes as not supported. Even in code that *appears* to work, it has never been safe to mix threading with `os.fork`{.interpreted-text role="func"} on POSIX platforms. The CPython runtime itself has always made API calls that are not safe for use in the child process when threads existed in the parent (such as `malloc` and `free`).

Users of macOS or users of libc or malloc implementations other than those typically found in glibc to date are among those already more likely to experience deadlocks running such code.

See [this discussion on fork being incompatible with threads](https://discuss.python.org/t/33555) for technical details of why we\'re surfacing this longstanding platform compatibility problem to developers.
:::

::: availability
POSIX, not WASI, not Android, not iOS.
:::
:::::::::::

:::::::::: function
forkpty()

Fork a child process, using a new pseudo-terminal as the child\'s controlling terminal. Return a pair of `(pid, fd)`, where *pid* is `0` in the child, the new child\'s process id in the parent, and *fd* is the file descriptor of the master end of the pseudo-terminal. For a more portable approach, use the `pty`{.interpreted-text role="mod"} module. If an error occurs `OSError`{.interpreted-text role="exc"} is raised.

The returned file descriptor *fd* is `non-inheritable <fd_inheritance>`{.interpreted-text role="ref"}.

::: audit-event
os.forkpty \"\" os.forkpty
:::

:::: warning
::: title
Warning
:::

On macOS the use of this function is unsafe when mixed with using higher-level system APIs, and that includes using `urllib.request`{.interpreted-text role="mod"}.
::::

::: versionchanged
3.8 Calling `forkpty()` in a subinterpreter is no longer supported (`RuntimeError`{.interpreted-text role="exc"} is raised).
:::

::: versionchanged
3.12 If Python is able to detect that your process has multiple threads, this now raises a `DeprecationWarning`{.interpreted-text role="exc"}. See the longer explanation on `os.fork`{.interpreted-text role="func"}.
:::

::: versionchanged
3.15 The returned file descriptor is now made non-inheritable.
:::

::: availability
Unix, not WASI, not Android, not iOS.
:::
::::::::::

::::::: function
kill(pid, sig, /)

::: index
single: process; killing single: process; signalling
:::

Send signal *sig* to the process *pid*. Constants for the specific signals available on the host platform are defined in the `signal`{.interpreted-text role="mod"} module.

Windows: The `signal.CTRL_C_EVENT`{.interpreted-text role="const"} and `signal.CTRL_BREAK_EVENT`{.interpreted-text role="const"} signals are special signals which can only be sent to console processes which share a common console window, e.g., some subprocesses. Any other value for *sig* will cause the process to be unconditionally killed by the TerminateProcess API, and the exit code will be set to *sig*.

See also `signal.pthread_kill`{.interpreted-text role="func"}.

::: audit-event
os.kill pid,sig os.kill
:::

::: availability
Unix, Windows, not WASI, not iOS.
:::

::: versionchanged
3.2 Added Windows support.
:::
:::::::

:::::: function
killpg(pgid, sig, /)

::: index
single: process; killing single: process; signalling
:::

Send the signal *sig* to the process group *pgid*.

::: audit-event
os.killpg pgid,sig os.killpg
:::

::: availability
Unix, not WASI, not iOS.
:::
::::::

:::: function
nice(increment, /)

Add *increment* to the process\'s \"niceness\". Return the new niceness.

::: availability
Unix, not WASI.
:::
::::

:::::::: function
pidfd_open(pid, flags=0)

Return a file descriptor referring to the process *pid* with *flags* set. This descriptor can be used to perform process management without races and signals.

See the `pidfd_open(2)`{.interpreted-text role="manpage"} man page for more details.

::: availability
Linux \>= 5.3, Android \>= `build-time <sys.getandroidapilevel>`{.interpreted-text role="func"} API level 31
:::

::: versionadded
3.9
:::

::: data
PIDFD_NONBLOCK

This flag indicates that the file descriptor will be non-blocking. If the process referred to by the file descriptor has not yet terminated, then an attempt to wait on the file descriptor using `waitid(2)`{.interpreted-text role="manpage"} will immediately return the error `~errno.EAGAIN`{.interpreted-text role="const"} rather than blocking.
:::

::: availability
Linux \>= 5.10
:::

::: versionadded
3.12
:::
::::::::

:::: function
plock(op, /)

Lock program segments into memory. The value of *op* (defined in `<sys/lock.h>`) determines which segments are locked.

::: availability
Unix, not WASI, not iOS.
:::
::::

::::::: function
popen(cmd, mode=\'r\', buffering=-1)

Open a pipe to or from command *cmd*. The return value is an open file object connected to the pipe, which can be read or written depending on whether *mode* is `'r'` (default) or `'w'`. The *buffering* argument have the same meaning as the corresponding argument to the built-in `open`{.interpreted-text role="func"} function. The returned file object reads or writes text strings rather than bytes.

The `close` method returns `None`{.interpreted-text role="const"} if the subprocess exited successfully, or the subprocess\'s return code if there was an error. On POSIX systems, if the return code is positive it represents the return value of the process left-shifted by one byte. If the return code is negative, the process was terminated by the signal given by the negated value of the return code. (For example, the return value might be `- signal.SIGKILL` if the subprocess was killed.) On Windows systems, the return value contains the signed integer return code from the child process.

On Unix, `waitstatus_to_exitcode`{.interpreted-text role="func"} can be used to convert the `close` method result (exit status) into an exit code if it is not `None`. On Windows, the `close` method result is directly the exit code (or `None`).

This is implemented using `subprocess.Popen`{.interpreted-text role="class"}; see that class\'s documentation for more powerful ways to manage and communicate with subprocesses.

::: availability
not WASI, not Android, not iOS.
:::

:::: note
::: title
Note
:::

The `Python UTF-8 Mode <utf8-mode>`{.interpreted-text role="ref"} affects encodings used for *cmd* and pipe contents.

`popen`{.interpreted-text role="func"} is a simple wrapper around `subprocess.Popen`{.interpreted-text role="class"}. Use `subprocess.Popen`{.interpreted-text role="class"} or `subprocess.run`{.interpreted-text role="func"} to control options like encodings.
::::

::: deprecated
3.14 The function is `soft deprecated`{.interpreted-text role="term"} and should no longer be used to write new code. The `subprocess`{.interpreted-text role="mod"} module is recommended instead.
:::
:::::::

::::::::::: function
posix_spawn(path, argv, env, \*, file_actions=None, setpgroup=None, resetids=False, setsid=False, setsigmask=(), setsigdef=(), scheduler=None)

Wraps the `!posix_spawn`{.interpreted-text role="c:func"} C library API for use from Python.

Most users should use `subprocess.run`{.interpreted-text role="func"} instead of `posix_spawn`{.interpreted-text role="func"}.

The positional-only arguments *path*, *args*, and *env* are similar to `execve`{.interpreted-text role="func"}. *env* is allowed to be `None`, in which case current process\' environment is used.

The *path* parameter is the path to the executable file. The *path* should contain a directory. Use `posix_spawnp`{.interpreted-text role="func"} to pass an executable file without directory.

The *file_actions* argument may be a sequence of tuples describing actions to take on specific file descriptors in the child process between the C library implementation\'s `fork`{.interpreted-text role="c:func"} and `exec`{.interpreted-text role="c:func"} steps. The first item in each tuple must be one of the three type indicator listed below describing the remaining tuple elements:

::: data
POSIX_SPAWN_OPEN

(`os.POSIX_SPAWN_OPEN`, *fd*, *path*, *flags*, *mode*)

Performs `os.dup2(os.open(path, flags, mode), fd)`.
:::

::: data
POSIX_SPAWN_CLOSE

(`os.POSIX_SPAWN_CLOSE`, *fd*)

Performs `os.close(fd)`.
:::

::: data
POSIX_SPAWN_DUP2

(`os.POSIX_SPAWN_DUP2`, *fd*, *new_fd*)

Performs `os.dup2(fd, new_fd)`.
:::

::: data
POSIX_SPAWN_CLOSEFROM

(`os.POSIX_SPAWN_CLOSEFROM`, *fd*)

Performs `os.closerange(fd, INF)`.
:::

These tuples correspond to the C library `!posix_spawn_file_actions_addopen`{.interpreted-text role="c:func"}, `!posix_spawn_file_actions_addclose`{.interpreted-text role="c:func"}, `!posix_spawn_file_actions_adddup2`{.interpreted-text role="c:func"}, and `!posix_spawn_file_actions_addclosefrom_np`{.interpreted-text role="c:func"} API calls used to prepare for the `!posix_spawn`{.interpreted-text role="c:func"} call itself.

The *setpgroup* argument will set the process group of the child to the value specified. If the value specified is 0, the child\'s process group ID will be made the same as its process ID. If the value of *setpgroup* is not set, the child will inherit the parent\'s process group ID. This argument corresponds to the C library `!POSIX_SPAWN_SETPGROUP`{.interpreted-text role="c:macro"} flag.

If the *resetids* argument is `True` it will reset the effective UID and GID of the child to the real UID and GID of the parent process. If the argument is `False`, then the child retains the effective UID and GID of the parent. In either case, if the set-user-ID and set-group-ID permission bits are enabled on the executable file, their effect will override the setting of the effective UID and GID. This argument corresponds to the C library `!POSIX_SPAWN_RESETIDS`{.interpreted-text role="c:macro"} flag.

If the *setsid* argument is `True`, it will create a new session ID for `posix_spawn`. *setsid* requires `!POSIX_SPAWN_SETSID`{.interpreted-text role="c:macro"} or `!POSIX_SPAWN_SETSID_NP`{.interpreted-text role="c:macro"} flag. Otherwise, `NotImplementedError`{.interpreted-text role="exc"} is raised.

The *setsigmask* argument will set the signal mask to the signal set specified. If the parameter is not used, then the child inherits the parent\'s signal mask. This argument corresponds to the C library `!POSIX_SPAWN_SETSIGMASK`{.interpreted-text role="c:macro"} flag.

The *sigdef* argument will reset the disposition of all signals in the set specified. This argument corresponds to the C library `!POSIX_SPAWN_SETSIGDEF`{.interpreted-text role="c:macro"} flag.

The *scheduler* argument must be a tuple containing the (optional) scheduler policy and an instance of `sched_param`{.interpreted-text role="class"} with the scheduler parameters. A value of `None` in the place of the scheduler policy indicates that is not being provided. This argument is a combination of the C library `!POSIX_SPAWN_SETSCHEDPARAM`{.interpreted-text role="c:macro"} and `!POSIX_SPAWN_SETSCHEDULER`{.interpreted-text role="c:macro"} flags.

::: audit-event
os.posix_spawn path,argv,env os.posix_spawn
:::

::: versionadded
3.8
:::

::: versionchanged
3.13 *env* parameter accepts `None`. `os.POSIX_SPAWN_CLOSEFROM` is available on platforms where `!posix_spawn_file_actions_addclosefrom_np`{.interpreted-text role="c:func"} exists.
:::

::: availability
Unix, not WASI, not Android, not iOS.
:::
:::::::::::

:::::: function
posix_spawnp(path, argv, env, \*, file_actions=None, setpgroup=None, resetids=False, setsid=False, setsigmask=(), setsigdef=(), scheduler=None)

Wraps the `!posix_spawnp`{.interpreted-text role="c:func"} C library API for use from Python.

Similar to `posix_spawn`{.interpreted-text role="func"} except that the system searches for the *executable* file in the list of directories specified by the `PATH`{.interpreted-text role="envvar"} environment variable (in the same way as for `execvp(3)`).

::: audit-event
os.posix_spawn path,argv,env os.posix_spawnp
:::

::: versionadded
3.8
:::

::: availability
POSIX, not WASI, not Android, not iOS.

See `posix_spawn`{.interpreted-text role="func"} documentation.
:::
::::::

::::: function
register_at_fork(\*, before=None, after_in_parent=None, after_in_child=None)

Register callables to be executed when a new child process is forked using `os.fork`{.interpreted-text role="func"} or similar process cloning APIs. The parameters are optional and keyword-only. Each specifies a different call point.

- *before* is a function called before forking a child process.
- *after_in_parent* is a function called from the parent process after forking a child process.
- *after_in_child* is a function called from the child process.

These calls are only made if control is expected to return to the Python interpreter. A typical `subprocess`{.interpreted-text role="mod"} launch will not trigger them as the child is not going to re-enter the interpreter.

Functions registered for execution before forking are called in reverse registration order. Functions registered for execution after forking (either in the parent or in the child) are called in registration order.

Note that `fork`{.interpreted-text role="c:func"} calls made by third-party C code may not call those functions, unless it explicitly calls `PyOS_BeforeFork`{.interpreted-text role="c:func"}, `PyOS_AfterFork_Parent`{.interpreted-text role="c:func"} and `PyOS_AfterFork_Child`{.interpreted-text role="c:func"}.

There is no way to unregister a function.

::: availability
Unix, not WASI, not Android, not iOS.
:::

::: versionadded
3.7
:::
:::::

::::::: function
spawnl(mode, path, \...) spawnle(mode, path, \..., env) spawnlp(mode, file, \...) spawnlpe(mode, file, \..., env) spawnv(mode, path, args) spawnve(mode, path, args, env) spawnvp(mode, file, args) spawnvpe(mode, file, args, env)

Execute the program *path* in a new process.

(Note that the `subprocess`{.interpreted-text role="mod"} module provides more powerful facilities for spawning new processes and retrieving their results; using that module is preferable to using these functions. Check especially the `subprocess-replacements`{.interpreted-text role="ref"} section.)

If *mode* is `P_NOWAIT`{.interpreted-text role="const"}, this function returns the process id of the new process; if *mode* is `P_WAIT`{.interpreted-text role="const"}, returns the process\'s exit code if it exits normally, or `-signal`, where *signal* is the signal that killed the process. On Windows, the process id will actually be the process handle, so can be used with the `waitpid`{.interpreted-text role="func"} function.

Note on VxWorks, this function doesn\'t return `-signal` when the new process is killed. Instead it raises OSError exception.

The \"l\" and \"v\" variants of the `spawn\* <spawnl>`{.interpreted-text role="func"} functions differ in how command-line arguments are passed. The \"l\" variants are perhaps the easiest to work with if the number of parameters is fixed when the code is written; the individual parameters simply become additional parameters to the `!spawnl\*`{.interpreted-text role="func"} functions. The \"v\" variants are good when the number of parameters is variable, with the arguments being passed in a list or tuple as the *args* parameter. In either case, the arguments to the child process must start with the name of the command being run.

The variants which include a second \"p\" near the end (`spawnlp`{.interpreted-text role="func"}, `spawnlpe`{.interpreted-text role="func"}, `spawnvp`{.interpreted-text role="func"}, and `spawnvpe`{.interpreted-text role="func"}) will use the `PATH`{.interpreted-text role="envvar"} environment variable to locate the program *file*. When the environment is being replaced (using one of the `spawn\*e <spawnl>`{.interpreted-text role="func"} variants, discussed in the next paragraph), the new environment is used as the source of the `PATH`{.interpreted-text role="envvar"} variable. The other variants, `spawnl`{.interpreted-text role="func"}, `spawnle`{.interpreted-text role="func"}, `spawnv`{.interpreted-text role="func"}, and `spawnve`{.interpreted-text role="func"}, will not use the `PATH`{.interpreted-text role="envvar"} variable to locate the executable; *path* must contain an appropriate absolute or relative path.

For `spawnle`{.interpreted-text role="func"}, `spawnlpe`{.interpreted-text role="func"}, `spawnve`{.interpreted-text role="func"}, and `spawnvpe`{.interpreted-text role="func"} (note that these all end in \"e\"), the *env* parameter must be a mapping which is used to define the environment variables for the new process (they are used instead of the current process\' environment); the functions `spawnl`{.interpreted-text role="func"}, `spawnlp`{.interpreted-text role="func"}, `spawnv`{.interpreted-text role="func"}, and `spawnvp`{.interpreted-text role="func"} all cause the new process to inherit the environment of the current process. Note that keys and values in the *env* dictionary must be strings; invalid keys or values will cause the function to fail, with a return value of `127`.

As an example, the following calls to `spawnlp`{.interpreted-text role="func"} and `spawnvpe`{.interpreted-text role="func"} are equivalent:

    import os
    os.spawnlp(os.P_WAIT, 'cp', 'cp', 'index.html', '/dev/null')

    L = ['cp', 'index.html', '/dev/null']
    os.spawnvpe(os.P_WAIT, 'cp', L, os.environ)

::: audit-event
os.spawn mode,path,args,env os.spawnl
:::

::: availability
Unix, Windows, not WASI, not Android, not iOS.

`spawnlp`{.interpreted-text role="func"}, `spawnlpe`{.interpreted-text role="func"}, `spawnvp`{.interpreted-text role="func"} and `spawnvpe`{.interpreted-text role="func"} are not available on Windows. `spawnle`{.interpreted-text role="func"} and `spawnve`{.interpreted-text role="func"} are not thread-safe on Windows; we advise you to use the `subprocess`{.interpreted-text role="mod"} module instead.
:::

::: versionchanged
3.6 Accepts a `path-like object`{.interpreted-text role="term"}.
:::

::: deprecated
3.14 These functions are `soft deprecated`{.interpreted-text role="term"} and should no longer be used to write new code. The `subprocess`{.interpreted-text role="mod"} module is recommended instead.
:::
:::::::

:::: data
P_NOWAIT P_NOWAITO

Possible values for the *mode* parameter to the `spawn\* <spawnl>`{.interpreted-text role="func"} family of functions. If either of these values is given, the `spawn\* <spawnl>`{.interpreted-text role="func"} functions will return as soon as the new process has been created, with the process id as the return value.

::: availability
Unix, Windows.
:::
::::

:::: data
P_WAIT

Possible value for the *mode* parameter to the `spawn\* <spawnl>`{.interpreted-text role="func"} family of functions. If this is given as *mode*, the `spawn\* <spawnl>`{.interpreted-text role="func"} functions will not return until the new process has run to completion and will return the exit code of the process the run is successful, or `-signal` if a signal kills the process.

::: availability
Unix, Windows.
:::
::::

:::: data
P_DETACH P_OVERLAY

Possible values for the *mode* parameter to the `spawn\* <spawnl>`{.interpreted-text role="func"} family of functions. These are less portable than those listed above. `P_DETACH`{.interpreted-text role="const"} is similar to `P_NOWAIT`{.interpreted-text role="const"}, but the new process is detached from the console of the calling process. If `P_OVERLAY`{.interpreted-text role="const"} is used, the current process will be replaced; the `spawn\* <spawnl>`{.interpreted-text role="func"} function will not return.

::: availability
Windows.
:::
::::

::::::: function
startfile(path, \[operation\], \[arguments\], \[cwd\], \[show_cmd\])

Start a file with its associated application.

When *operation* is not specified, this acts like double-clicking the file in Windows Explorer, or giving the file name as an argument to the `start`{.interpreted-text role="program"} command from the interactive command shell: the file is opened with whatever application (if any) its extension is associated.

When another *operation* is given, it must be a \"command verb\" that specifies what should be done with the file. Common verbs documented by Microsoft are `'open'`, `'print'` and `'edit'` (to be used on files) as well as `'explore'` and `'find'` (to be used on directories).

When launching an application, specify *arguments* to be passed as a single string. This argument may have no effect when using this function to launch a document.

The default working directory is inherited, but may be overridden by the *cwd* argument. This should be an absolute path. A relative *path* will be resolved against this argument.

Use *show_cmd* to override the default window style. Whether this has any effect will depend on the application being launched. Values are integers as supported by the Win32 `!ShellExecute`{.interpreted-text role="c:func"} function.

`startfile`{.interpreted-text role="func"} returns as soon as the associated application is launched. There is no option to wait for the application to close, and no way to retrieve the application\'s exit status. The *path* parameter is relative to the current directory or *cwd*. If you want to use an absolute path, make sure the first character is not a slash (`'/'`) Use `pathlib`{.interpreted-text role="mod"} or the `os.path.normpath`{.interpreted-text role="func"} function to ensure that paths are properly encoded for Win32.

To reduce interpreter startup overhead, the Win32 `!ShellExecute`{.interpreted-text role="c:func"} function is not resolved until this function is first called. If the function cannot be resolved, `NotImplementedError`{.interpreted-text role="exc"} will be raised.

::: audit-event
os.startfile path,operation os.startfile
:::

::: audit-event
os.startfile/2 path,operation,arguments,cwd,show_cmd os.startfile
:::

::: availability
Windows.
:::

::: versionchanged
3.10 Added the *arguments*, *cwd* and *show_cmd* arguments, and the `os.startfile/2` audit event.
:::
:::::::

::::: function
system(command)

Execute the command (a string) in a subshell. This is implemented by calling the Standard C function `system`{.interpreted-text role="c:func"}, and has the same limitations. Changes to `sys.stdin`{.interpreted-text role="data"}, etc. are not reflected in the environment of the executed command. If *command* generates any output, it will be sent to the interpreter standard output stream. The C standard does not specify the meaning of the return value of the C function, so the return value of the Python function is system-dependent.

On Unix, the return value is the exit status of the process encoded in the format specified for `wait`{.interpreted-text role="func"}.

On Windows, the return value is that returned by the system shell after running *command*. The shell is given by the Windows environment variable `COMSPEC`{.interpreted-text role="envvar"}: it is usually `cmd.exe`{.interpreted-text role="program"}, which returns the exit status of the command run; on systems using a non-native shell, consult your shell documentation.

The `subprocess`{.interpreted-text role="mod"} module provides more powerful facilities for spawning new processes and retrieving their results; using that module is recommended to using this function. See the `subprocess-replacements`{.interpreted-text role="ref"} section in the `subprocess`{.interpreted-text role="mod"} documentation for some helpful recipes.

On Unix, `waitstatus_to_exitcode`{.interpreted-text role="func"} can be used to convert the result (exit status) into an exit code. On Windows, the result is directly the exit code.

::: audit-event
os.system command os.system
:::

::: availability
Unix, Windows, not WASI, not Android, not iOS.
:::
:::::

::::: function
times()

Returns the current global process times. The return value is an object with five attributes:

- `!user`{.interpreted-text role="attr"} - user time
- `!system`{.interpreted-text role="attr"} - system time
- `!children_user`{.interpreted-text role="attr"} - user time of all child processes
- `!children_system`{.interpreted-text role="attr"} - system time of all child processes
- `!elapsed`{.interpreted-text role="attr"} - elapsed real time since a fixed point in the past

For backwards compatibility, this object also behaves like a five-tuple containing `!user`{.interpreted-text role="attr"}, `!system`{.interpreted-text role="attr"}, `!children_user`{.interpreted-text role="attr"}, `!children_system`{.interpreted-text role="attr"}, and `!elapsed`{.interpreted-text role="attr"} in that order.

See the Unix manual page `times(2)`{.interpreted-text role="manpage"} and [times(3)](https://man.freebsd.org/cgi/man.cgi?time(3)) manual page on Unix or [the GetProcessTimes MSDN](https://docs.microsoft.com/windows/win32/api/processthreadsapi/nf-processthreadsapi-getprocesstimes) on Windows. On Windows, only `!user`{.interpreted-text role="attr"} and `!system`{.interpreted-text role="attr"} are known; the other attributes are zero.

::: availability
Unix, Windows.
:::

::: versionchanged
3.3 Return type changed from a tuple to a tuple-like object with named attributes.
:::
:::::

::::: function
wait()

Wait for completion of a child process, and return a tuple containing its pid and exit status indication: a 16-bit number, whose low byte is the signal number that killed the process, and whose high byte is the exit status (if the signal number is zero); the high bit of the low byte is set if a core file was produced.

If there are no children that could be waited for, `ChildProcessError`{.interpreted-text role="exc"} is raised.

`waitstatus_to_exitcode`{.interpreted-text role="func"} can be used to convert the exit status into an exit code.

::: availability
Unix, not WASI, not Android, not iOS.
:::

::: seealso
The other `!wait*`{.interpreted-text role="func"} functions documented below can be used to wait for the completion of a specific child process and have more options. `waitpid`{.interpreted-text role="func"} is the only one also available on Windows.
:::
:::::

:::::: function
waitid(idtype, id, options, /)

Wait for the completion of a child process.

*idtype* can be `P_PID`{.interpreted-text role="data"}, `P_PGID`{.interpreted-text role="data"}, `P_ALL`{.interpreted-text role="data"}, or (on Linux) `P_PIDFD`{.interpreted-text role="data"}. The interpretation of *id* depends on it; see their individual descriptions.

*options* is an OR combination of flags. At least one of `WEXITED`{.interpreted-text role="data"}, `WSTOPPED`{.interpreted-text role="data"} or `WCONTINUED`{.interpreted-text role="data"} is required; `WNOHANG`{.interpreted-text role="data"} and `WNOWAIT`{.interpreted-text role="data"} are additional optional flags.

The return value is an object representing the data contained in the `siginfo_t`{.interpreted-text role="c:type"} structure with the following attributes:

- `!si_pid`{.interpreted-text role="attr"} (process ID)
- `!si_uid`{.interpreted-text role="attr"} (real user ID of the child)
- `!si_signo`{.interpreted-text role="attr"} (always `~signal.SIGCHLD`{.interpreted-text role="const"})
- `!si_status`{.interpreted-text role="attr"} (the exit status or signal number, depending on `!si_code`{.interpreted-text role="attr"})
- `!si_code`{.interpreted-text role="attr"} (see `CLD_EXITED`{.interpreted-text role="data"} for possible values)

If `WNOHANG`{.interpreted-text role="data"} is specified and there are no matching children in the requested state, `None` is returned. Otherwise, if there are no matching children that could be waited for, `ChildProcessError`{.interpreted-text role="exc"} is raised.

::: availability
Unix, not WASI, not Android, not iOS.
:::

::: versionadded
3.3
:::

::: versionchanged
3.13 This function is now available on macOS as well.
:::
::::::

::::: function
waitpid(pid, options, /)

The details of this function differ on Unix and Windows.

On Unix: Wait for completion of a child process given by process id *pid*, and return a tuple containing its process id and exit status indication (encoded as for `wait`{.interpreted-text role="func"}). The semantics of the call are affected by the value of the integer *options*, which should be `0` for normal operation.

If *pid* is greater than `0`, `waitpid`{.interpreted-text role="func"} requests status information for that specific process. If *pid* is `0`, the request is for the status of any child in the process group of the current process. If *pid* is `-1`, the request pertains to any child of the current process. If *pid* is less than `-1`, status is requested for any process in the process group `-pid` (the absolute value of *pid*).

*options* is an OR combination of flags. If it contains `WNOHANG`{.interpreted-text role="data"} and there are no matching children in the requested state, `(0, 0)` is returned. Otherwise, if there are no matching children that could be waited for, `ChildProcessError`{.interpreted-text role="exc"} is raised. Other options that can be used are `WUNTRACED`{.interpreted-text role="data"} and `WCONTINUED`{.interpreted-text role="data"}.

On Windows: Wait for completion of a process given by process handle *pid*, and return a tuple containing *pid*, and its exit status shifted left by 8 bits (shifting makes cross-platform use of the function easier). A *pid* less than or equal to `0` has no special meaning on Windows, and raises an exception. The value of integer *options* has no effect. *pid* can refer to any process whose id is known, not necessarily a child process. The `spawn\* <spawnl>`{.interpreted-text role="func"} functions called with `P_NOWAIT`{.interpreted-text role="const"} return suitable process handles.

`waitstatus_to_exitcode`{.interpreted-text role="func"} can be used to convert the exit status into an exit code.

::: availability
Unix, Windows, not WASI, not Android, not iOS.
:::

::: versionchanged
3.5 If the system call is interrupted and the signal handler does not raise an exception, the function now retries the system call instead of raising an `InterruptedError`{.interpreted-text role="exc"} exception (see `475`{.interpreted-text role="pep"} for the rationale).
:::
:::::

:::: function
wait3(options)

Similar to `waitpid`{.interpreted-text role="func"}, except no process id argument is given and a 3-element tuple containing the child\'s process id, exit status indication, and resource usage information is returned. Refer to `resource.getrusage`{.interpreted-text role="func"} for details on resource usage information. The *options* argument is the same as that provided to `waitpid`{.interpreted-text role="func"} and `wait4`{.interpreted-text role="func"}.

`waitstatus_to_exitcode`{.interpreted-text role="func"} can be used to convert the exit status into an exitcode.

::: availability
Unix, not WASI, not Android, not iOS.
:::
::::

:::: function
wait4(pid, options)

Similar to `waitpid`{.interpreted-text role="func"}, except a 3-element tuple, containing the child\'s process id, exit status indication, and resource usage information is returned. Refer to `resource.getrusage`{.interpreted-text role="func"} for details on resource usage information. The arguments to `wait4`{.interpreted-text role="func"} are the same as those provided to `waitpid`{.interpreted-text role="func"}.

`waitstatus_to_exitcode`{.interpreted-text role="func"} can be used to convert the exit status into an exitcode.

::: availability
Unix, not WASI, not Android, not iOS.
:::
::::

:::::::: data
P_PID P_PGID P_ALL P_PIDFD

These are the possible values for *idtype* in `waitid`{.interpreted-text role="func"}. They affect how *id* is interpreted:

- `!P_PID`{.interpreted-text role="data"} - wait for the child whose PID is *id*.
- `!P_PGID`{.interpreted-text role="data"} - wait for any child whose progress group ID is *id*.
- `!P_ALL`{.interpreted-text role="data"} - wait for any child; *id* is ignored.
- `!P_PIDFD`{.interpreted-text role="data"} - wait for the child identified by the file descriptor *id* (a process file descriptor created with `pidfd_open`{.interpreted-text role="func"}).

::: availability
Unix, not WASI, not Android, not iOS.
:::

:::: note
::: title
Note
:::

`!P_PIDFD`{.interpreted-text role="data"} is only available on Linux \>= 5.4.
::::

::: versionadded
3.3
:::

::: versionadded
3.9 The `!P_PIDFD`{.interpreted-text role="data"} constant.
:::
::::::::

:::: data
WCONTINUED

This *options* flag for `waitpid`{.interpreted-text role="func"}, `wait3`{.interpreted-text role="func"}, `wait4`{.interpreted-text role="func"}, and `waitid`{.interpreted-text role="func"} causes child processes to be reported if they have been continued from a job control stop since they were last reported.

::: availability
Unix, not WASI, not Android, not iOS.
:::
::::

::::: data
WEXITED

This *options* flag for `waitid`{.interpreted-text role="func"} causes child processes that have terminated to be reported.

The other `wait*` functions always report children that have terminated, so this option is not available for them.

::: availability
Unix, not WASI, not Android, not iOS.
:::

::: versionadded
3.3
:::
:::::

::::: data
WSTOPPED

This *options* flag for `waitid`{.interpreted-text role="func"} causes child processes that have been stopped by the delivery of a signal to be reported.

This option is not available for the other `wait*` functions.

::: availability
Unix, not WASI, not Android, not iOS.
:::

::: versionadded
3.3
:::
:::::

:::: data
WUNTRACED

This *options* flag for `waitpid`{.interpreted-text role="func"}, `wait3`{.interpreted-text role="func"}, and `wait4`{.interpreted-text role="func"} causes child processes to also be reported if they have been stopped but their current state has not been reported since they were stopped.

This option is not available for `waitid`{.interpreted-text role="func"}.

::: availability
Unix, not WASI, not Android, not iOS.
:::
::::

:::: data
WNOHANG

This *options* flag causes `waitpid`{.interpreted-text role="func"}, `wait3`{.interpreted-text role="func"}, `wait4`{.interpreted-text role="func"}, and `waitid`{.interpreted-text role="func"} to return right away if no child process status is available immediately.

::: availability
Unix, not WASI, not Android, not iOS.
:::
::::

:::: data
WNOWAIT

This *options* flag causes `waitid`{.interpreted-text role="func"} to leave the child in a waitable state, so that a later `!wait*`{.interpreted-text role="func"} call can be used to retrieve the child status information again.

This option is not available for the other `wait*` functions.

::: availability
Unix, not WASI, not Android, not iOS.
:::
::::

:::::: data
CLD_EXITED CLD_KILLED CLD_DUMPED CLD_TRAPPED CLD_STOPPED CLD_CONTINUED

These are the possible values for `!si_code`{.interpreted-text role="attr"} in the result returned by `waitid`{.interpreted-text role="func"}.

::: availability
Unix, not WASI, not Android, not iOS.
:::

::: versionadded
3.3
:::

::: versionchanged
3.9 Added `CLD_KILLED`{.interpreted-text role="data"} and `CLD_STOPPED`{.interpreted-text role="data"} values.
:::
::::::

:::::: function
waitstatus_to_exitcode(status)

Convert a wait status to an exit code.

On Unix:

- If the process exited normally (if `WIFEXITED(status)` is true), return the process exit status (return `WEXITSTATUS(status)`): result greater than or equal to 0.
- If the process was terminated by a signal (if `WIFSIGNALED(status)` is true), return `-signum` where *signum* is the number of the signal that caused the process to terminate (return `-WTERMSIG(status)`): result less than 0.
- Otherwise, raise a `ValueError`{.interpreted-text role="exc"}.

On Windows, return *status* shifted right by 8 bits.

On Unix, if the process is being traced or if `waitpid`{.interpreted-text role="func"} was called with `WUNTRACED`{.interpreted-text role="data"} option, the caller must first check if `WIFSTOPPED(status)` is true. This function must not be called if `WIFSTOPPED(status)` is true.

::: seealso
`WIFEXITED`{.interpreted-text role="func"}, `WEXITSTATUS`{.interpreted-text role="func"}, `WIFSIGNALED`{.interpreted-text role="func"}, `WTERMSIG`{.interpreted-text role="func"}, `WIFSTOPPED`{.interpreted-text role="func"}, `WSTOPSIG`{.interpreted-text role="func"} functions.
:::

::: availability
Unix, Windows, not WASI, not Android, not iOS.
:::

::: versionadded
3.9
:::
::::::

The following functions take a process status code as returned by `system`{.interpreted-text role="func"}, `wait`{.interpreted-text role="func"}, or `waitpid`{.interpreted-text role="func"} as a parameter. They may be used to determine the disposition of a process.

:::: function
WCOREDUMP(status, /)

Return `True` if a core dump was generated for the process, otherwise return `False`.

This function should be employed only if `WIFSIGNALED`{.interpreted-text role="func"} is true.

::: availability
Unix, not WASI, not Android, not iOS.
:::
::::

:::: function
WIFCONTINUED(status)

Return `True` if a stopped child has been resumed by delivery of `~signal.SIGCONT`{.interpreted-text role="const"} (if the process has been continued from a job control stop), otherwise return `False`.

See `WCONTINUED`{.interpreted-text role="data"} option.

::: availability
Unix, not WASI, not Android, not iOS.
:::
::::

:::: function
WIFSTOPPED(status)

Return `True` if the process was stopped by delivery of a signal, otherwise return `False`.

`WIFSTOPPED`{.interpreted-text role="func"} only returns `True` if the `waitpid`{.interpreted-text role="func"} call was done using `WUNTRACED`{.interpreted-text role="data"} option or when the process is being traced (see `ptrace(2)`{.interpreted-text role="manpage"}).

::: availability
Unix, not WASI, not Android, not iOS.
:::
::::

:::: function
WIFSIGNALED(status)

Return `True` if the process was terminated by a signal, otherwise return `False`.

::: availability
Unix, not WASI, not Android, not iOS.
:::
::::

:::: function
WIFEXITED(status)

Return `True` if the process exited terminated normally, that is, by calling `exit()` or `_exit()`, or by returning from `main()`; otherwise return `False`.

::: availability
Unix, not WASI, not Android, not iOS.
:::
::::

:::: function
WEXITSTATUS(status)

Return the process exit status.

This function should be employed only if `WIFEXITED`{.interpreted-text role="func"} is true.

::: availability
Unix, not WASI, not Android, not iOS.
:::
::::

:::: function
WSTOPSIG(status)

Return the signal which caused the process to stop.

This function should be employed only if `WIFSTOPPED`{.interpreted-text role="func"} is true.

::: availability
Unix, not WASI, not Android, not iOS.
:::
::::

:::: function
WTERMSIG(status)

Return the number of the signal that caused the process to terminate.

This function should be employed only if `WIFSIGNALED`{.interpreted-text role="func"} is true.

::: availability
Unix, not WASI, not Android, not iOS.
:::
::::

## Interface to the scheduler

These functions control how a process is allocated CPU time by the operating system. They are only available on some Unix platforms. For more detailed information, consult your Unix manpages.

::: versionadded
3.3
:::

The following scheduling policies are exposed if they are supported by the operating system.

:::: {#os-scheduling-policy}
::: data
SCHED_OTHER

The default scheduling policy.
:::
::::

::: data
SCHED_BATCH

Scheduling policy for CPU-intensive processes that tries to preserve interactivity on the rest of the computer.
:::

:::: data
SCHED_DEADLINE

Scheduling policy for tasks with deadline constraints.

::: versionadded
3.14
:::
::::

::: data
SCHED_IDLE

Scheduling policy for extremely low priority background tasks.
:::

:::: data
SCHED_NORMAL

Alias for `SCHED_OTHER`{.interpreted-text role="data"}.

::: versionadded
3.14
:::
::::

::: data
SCHED_SPORADIC

Scheduling policy for sporadic server programs.
:::

::: data
SCHED_FIFO

A First In First Out scheduling policy.
:::

::: data
SCHED_RR

A round-robin scheduling policy.
:::

::: data
SCHED_RESET_ON_FORK

This flag can be OR\'ed with any other scheduling policy. When a process with this flag set forks, its child\'s scheduling policy and priority are reset to the default.
:::

:::: sched_param(sched_priority)
This class represents tunable scheduling parameters used in `sched_setparam`{.interpreted-text role="func"}, `sched_setscheduler`{.interpreted-text role="func"}, and `sched_getparam`{.interpreted-text role="func"}. It is immutable.

At the moment, there is only one possible parameter:

::: attribute
sched_priority

The scheduling priority for a scheduling policy.
:::
::::

::: function
sched_get_priority_min(policy)

Get the minimum priority value for *policy*. *policy* is one of the scheduling policy constants above.
:::

::: function
sched_get_priority_max(policy)

Get the maximum priority value for *policy*. *policy* is one of the scheduling policy constants above.
:::

::: function
sched_setscheduler(pid, policy, param, /)

Set the scheduling policy for the process with PID *pid*. A *pid* of 0 means the calling process. *policy* is one of the scheduling policy constants above. *param* is a `sched_param`{.interpreted-text role="class"} instance.
:::

::: function
sched_getscheduler(pid, /)

Return the scheduling policy for the process with PID *pid*. A *pid* of 0 means the calling process. The result is one of the scheduling policy constants above.
:::

::: function
sched_setparam(pid, param, /)

Set the scheduling parameters for the process with PID *pid*. A *pid* of 0 means the calling process. *param* is a `sched_param`{.interpreted-text role="class"} instance.
:::

::: function
sched_getparam(pid, /)

Return the scheduling parameters as a `sched_param`{.interpreted-text role="class"} instance for the process with PID *pid*. A *pid* of 0 means the calling process.
:::

::: function
sched_rr_get_interval(pid, /)

Return the round-robin quantum in seconds for the process with PID *pid*. A *pid* of 0 means the calling process.
:::

::: function
sched_yield()

Voluntarily relinquish the CPU. See `sched_yield(2)`{.interpreted-text role="manpage"} for details.
:::

::: function
sched_setaffinity(pid, mask, /)

Restrict the process with PID *pid* (or the current process if zero) to a set of CPUs. *mask* is an iterable of integers representing the set of CPUs to which the process should be restricted.
:::

::: function
sched_getaffinity(pid, /)

Return the set of CPUs the process with PID *pid* is restricted to.

If *pid* is zero, return the set of CPUs the calling thread of the current process is restricted to.

See also the `process_cpu_count`{.interpreted-text role="func"} function.
:::

## Miscellaneous System Information {#os-path}

:::: function
confstr(name, /)

Return string-valued system configuration values. *name* specifies the configuration value to retrieve; it may be a string which is the name of a defined system value; these names are specified in a number of standards (POSIX, Unix 95, Unix 98, and others). Some platforms define additional names as well. The names known to the host operating system are given as the keys of the `confstr_names` dictionary. For configuration variables not included in that mapping, passing an integer for *name* is also accepted.

If the configuration value specified by *name* isn\'t defined, `None` is returned.

If *name* is a string and is not known, `ValueError`{.interpreted-text role="exc"} is raised. If a specific value for *name* is not supported by the host system, even if it is included in `confstr_names`, an `OSError`{.interpreted-text role="exc"} is raised with `errno.EINVAL`{.interpreted-text role="const"} for the error number.

::: availability
Unix.
:::
::::

:::: data
confstr_names

Dictionary mapping names accepted by `confstr`{.interpreted-text role="func"} to the integer values defined for those names by the host operating system. This can be used to determine the set of names known to the system.

::: availability
Unix.
:::
::::

::::: function
cpu_count()

Return the number of logical CPUs in the **system**. Returns `None` if undetermined.

The `process_cpu_count`{.interpreted-text role="func"} function can be used to get the number of logical CPUs usable by the calling thread of the **current process**.

::: versionadded
3.4
:::

::: versionchanged
3.13 If `-X cpu_count <-X>`{.interpreted-text role="option"} is given or `PYTHON_CPU_COUNT`{.interpreted-text role="envvar"} is set, `cpu_count`{.interpreted-text role="func"} returns the override value *n*.
:::
:::::

:::: function
getloadavg()

Return the number of processes in the system run queue averaged over the last 1, 5, and 15 minutes or raises `OSError`{.interpreted-text role="exc"} if the load average was unobtainable.

::: availability
Unix.
:::
::::

:::: function
process_cpu_count()

Get the number of logical CPUs usable by the calling thread of the **current process**. Returns `None` if undetermined. It can be less than `cpu_count`{.interpreted-text role="func"} depending on the CPU affinity.

The `cpu_count`{.interpreted-text role="func"} function can be used to get the number of logical CPUs in the **system**.

If `-X cpu_count <-X>`{.interpreted-text role="option"} is given or `PYTHON_CPU_COUNT`{.interpreted-text role="envvar"} is set, `process_cpu_count`{.interpreted-text role="func"} returns the override value *n*.

See also the `sched_getaffinity`{.interpreted-text role="func"} function.

::: versionadded
3.13
:::
::::

:::: function
sysconf(name, /)

Return integer-valued system configuration values. If the configuration value specified by *name* isn\'t defined, `-1` is returned. The comments regarding the *name* parameter for `confstr`{.interpreted-text role="func"} apply here as well; the dictionary that provides information on the known names is given by `sysconf_names`.

::: availability
Unix.
:::
::::

::::: data
sysconf_names

Dictionary mapping names accepted by `sysconf`{.interpreted-text role="func"} to the integer values defined for those names by the host operating system. This can be used to determine the set of names known to the system.

::: availability
Unix.
:::

::: versionchanged
3.11 Add `'SC_MINSIGSTKSZ'` name.
:::
:::::

The following data values are used to support path manipulation operations. These are defined for all platforms.

Higher-level operations on pathnames are defined in the `os.path`{.interpreted-text role="mod"} module.

::: index
single: . (dot); in pathnames
:::

::: data
curdir

The constant string used by the operating system to refer to the current directory. This is `'.'` for Windows and POSIX. Also available via `os.path`{.interpreted-text role="mod"}.
:::

::: index
single: ..; in pathnames
:::

::: data
pardir

The constant string used by the operating system to refer to the parent directory. This is `'..'` for Windows and POSIX. Also available via `os.path`{.interpreted-text role="mod"}.
:::

::: index
single: / (slash); in pathnames
:::

::: index
single: (backslash); in pathnames (Windows)
:::

::: data
sep

The character used by the operating system to separate pathname components. This is `'/'` for POSIX and `'\\'` for Windows. Note that knowing this is not sufficient to be able to parse or concatenate pathnames \-\-- use `os.path.split`{.interpreted-text role="func"} and `os.path.join`{.interpreted-text role="func"} \-\-- but it is occasionally useful. Also available via `os.path`{.interpreted-text role="mod"}.
:::

::: index
single: / (slash); in pathnames
:::

::: data
altsep

An alternative character used by the operating system to separate pathname components, or `None` if only one separator character exists. This is set to `'/'` on Windows systems where `sep` is a backslash. Also available via `os.path`{.interpreted-text role="mod"}.
:::

::: index
single: . (dot); in pathnames
:::

::: data
extsep

The character which separates the base filename from the extension; for example, the `'.'` in `os.py`{.interpreted-text role="file"}. Also available via `os.path`{.interpreted-text role="mod"}.
:::

::: index
single: : (colon); path separator (POSIX) single: ; (semicolon)
:::

::: data
pathsep

The character conventionally used by the operating system to separate search path components (as in `PATH`{.interpreted-text role="envvar"}), such as `':'` for POSIX or `';'` for Windows. Also available via `os.path`{.interpreted-text role="mod"}.
:::

::: data
defpath

The default search path used by `exec\*p\* <execl>`{.interpreted-text role="func"} and `spawn\*p\* <spawnl>`{.interpreted-text role="func"} if the environment doesn\'t have a `'PATH'` key. Also available via `os.path`{.interpreted-text role="mod"}.
:::

::: data
linesep

The string used to separate (or, rather, terminate) lines on the current platform. This may be a single character, such as `'\n'` for POSIX, or multiple characters, for example, `'\r\n'` for Windows. Do not use *os.linesep* as a line terminator when writing files opened in text mode (the default); use a single `'\n'` instead, on all platforms.
:::

::: data
devnull

The file path of the null device. For example: `'/dev/null'` for POSIX, `'nul'` for Windows. Also available via `os.path`{.interpreted-text role="mod"}.
:::

:::: data
RTLD_LAZY RTLD_NOW RTLD_GLOBAL RTLD_LOCAL RTLD_NODELETE RTLD_NOLOAD RTLD_DEEPBIND

Flags for use with the `~sys.setdlopenflags`{.interpreted-text role="func"} and `~sys.getdlopenflags`{.interpreted-text role="func"} functions. See the Unix manual page `dlopen(3)`{.interpreted-text role="manpage"} for what the different flags mean.

::: versionadded
3.3
:::
::::

## Random numbers

::::: function
getrandom(size, flags=0)

Get up to *size* random bytes. The function can return less bytes than requested.

These bytes can be used to seed user-space random number generators or for cryptographic purposes.

`getrandom()` relies on entropy gathered from device drivers and other sources of environmental noise. Unnecessarily reading large quantities of data will have a negative impact on other users of the `/dev/random` and `/dev/urandom` devices.

The flags argument is a bit mask that can contain zero or more of the following values ORed together: `os.GRND_RANDOM`{.interpreted-text role="py:const"} and `GRND_NONBLOCK`{.interpreted-text role="py:data"}.

See also the [Linux getrandom() manual page](https://man7.org/linux/man-pages/man2/getrandom.2.html).

::: availability
Linux \>= 3.17.
:::

::: versionadded
3.6
:::
:::::

:::::::: function
urandom(size, /)

Return a bytestring of *size* random bytes suitable for cryptographic use.

This function returns random bytes from an OS-specific randomness source. The returned data should be unpredictable enough for cryptographic applications, though its exact quality depends on the OS implementation.

On Linux, if the `getrandom()` syscall is available, it is used in blocking mode: block until the system urandom entropy pool is initialized (128 bits of entropy are collected by the kernel). See the `524`{.interpreted-text role="pep"} for the rationale. On Linux, the `getrandom`{.interpreted-text role="func"} function can be used to get random bytes in non-blocking mode (using the `GRND_NONBLOCK`{.interpreted-text role="data"} flag) or to poll until the system urandom entropy pool is initialized.

On a Unix-like system, random bytes are read from the `/dev/urandom` device. If the `/dev/urandom` device is not available or not readable, the `NotImplementedError`{.interpreted-text role="exc"} exception is raised.

On Windows, it will use `BCryptGenRandom()`.

::: seealso
The `secrets`{.interpreted-text role="mod"} module provides higher level functions. For an easy-to-use interface to the random number generator provided by your platform, please see `random.SystemRandom`{.interpreted-text role="class"}.
:::

::: versionchanged
3.5 On Linux 3.17 and newer, the `getrandom()` syscall is now used when available. On OpenBSD 5.6 and newer, the C `getentropy()` function is now used. These functions avoid the usage of an internal file descriptor.
:::

::: versionchanged
3.5.2 On Linux, if the `getrandom()` syscall blocks (the urandom entropy pool is not initialized yet), fall back on reading `/dev/urandom`.
:::

::: versionchanged
3.6 On Linux, `getrandom()` is now used in blocking mode to increase the security.
:::

::: versionchanged
3.11 On Windows, `BCryptGenRandom()` is used instead of `CryptGenRandom()` which is deprecated.
:::
::::::::

:::: data
GRND_NONBLOCK

By default, when reading from `/dev/random`, `getrandom`{.interpreted-text role="func"} blocks if no random bytes are available, and when reading from `/dev/urandom`, it blocks if the entropy pool has not yet been initialized.

If the `GRND_NONBLOCK`{.interpreted-text role="py:data"} flag is set, then `getrandom`{.interpreted-text role="func"} does not block in these cases, but instead immediately raises `BlockingIOError`{.interpreted-text role="exc"}.

::: versionadded
3.6
:::
::::

:::: data
GRND_RANDOM

If this bit is set, then random bytes are drawn from the `/dev/random` pool instead of the `/dev/urandom` pool.

::: versionadded
3.6
:::
::::
