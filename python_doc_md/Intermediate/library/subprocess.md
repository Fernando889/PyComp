# `!subprocess`{.interpreted-text role="mod"} \-\-- Subprocess management

::: {.module synopsis="Subprocess management."}
subprocess
:::

**Source code:** `Lib/subprocess.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

The `!subprocess`{.interpreted-text role="mod"} module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes. This module intends to replace several older modules and functions:

    os.system
    os.spawn*

Information about how the `!subprocess`{.interpreted-text role="mod"} module can be used to replace these modules and functions can be found in the following sections.

::: seealso
`324`{.interpreted-text role="pep"} \-- PEP proposing the subprocess module
:::

::: availability
not Android, not iOS, not WASI.

This module is not supported on `mobile platforms <mobile-availability>`{.interpreted-text role="ref"} or `WebAssembly platforms <wasm-availability>`{.interpreted-text role="ref"}.
:::

## Using the `!subprocess`{.interpreted-text role="mod"} Module

The recommended approach to invoking subprocesses is to use the `run`{.interpreted-text role="func"} function for all use cases it can handle. For more advanced use cases, the underlying `Popen`{.interpreted-text role="class"} interface can be used directly.

::::::: function
run(args, *, stdin=None, input=None, stdout=None, stderr=None,capture_output=False, shell=False, cwd=None, timeout=None, check=False, encoding=None, errors=None, text=None, env=None, universal_newlines=None,*\*other_popen_kwargs)

Run the command described by *args*. Wait for command to complete, then return a `CompletedProcess`{.interpreted-text role="class"} instance.

The arguments shown above are merely the most common ones, described below in `frequently-used-arguments`{.interpreted-text role="ref"} (hence the use of keyword-only notation in the abbreviated signature). The full function signature is largely the same as that of the `Popen`{.interpreted-text role="class"} constructor - most of the arguments to this function are passed through to that interface. (*timeout*, *input*, *check*, and *capture_output* are not.)

If *capture_output* is true, stdout and stderr will be captured. When used, the internal `Popen`{.interpreted-text role="class"} object is automatically created with *stdout* and *stderr* both set to `~subprocess.PIPE`{.interpreted-text role="data"}. The *stdout* and *stderr* arguments may not be supplied at the same time as *capture_output*. If you wish to capture and combine both streams into one, set *stdout* to `~subprocess.PIPE`{.interpreted-text role="data"} and *stderr* to `~subprocess.STDOUT`{.interpreted-text role="data"}, instead of using *capture_output*.

A *timeout* may be specified in seconds, it is internally passed on to `Popen.communicate`{.interpreted-text role="meth"}. If the timeout expires, the child process will be killed and waited for. The `TimeoutExpired`{.interpreted-text role="exc"} exception will be re-raised after the child process has terminated. The initial process creation itself cannot be interrupted on many platform APIs so you are not guaranteed to see a timeout exception until at least after however long process creation takes.

The *input* argument is passed to `Popen.communicate`{.interpreted-text role="meth"} and thus to the subprocess\'s stdin. If used it must be a byte sequence, or a string if *encoding* or *errors* is specified or *text* is true. When used, the internal `Popen`{.interpreted-text role="class"} object is automatically created with *stdin* set to `~subprocess.PIPE`{.interpreted-text role="data"}, and the *stdin* argument may not be used as well.

If *check* is true, and the process exits with a non-zero exit code, a `CalledProcessError`{.interpreted-text role="exc"} exception will be raised. Attributes of that exception hold the arguments, the exit code, and stdout and stderr if they were captured.

If *encoding* or *errors* are specified, or *text* is true, file objects for stdin, stdout and stderr are opened in text mode using the specified *encoding* and *errors* or the `io.TextIOWrapper`{.interpreted-text role="class"} default. The *universal_newlines* argument is equivalent to *text* and is provided for backwards compatibility. By default, file objects are opened in binary mode.

If *env* is not `None`, it must be a mapping that defines the environment variables for the new process; these are used instead of the default behavior of inheriting the current process\' environment. It is passed directly to `Popen`{.interpreted-text role="class"}. This mapping can be str to str on any platform or bytes to bytes on POSIX platforms much like `os.environ`{.interpreted-text role="data"} or `os.environb`{.interpreted-text role="data"}.

Examples:

    >>> subprocess.run(["ls", "-l"])  # doesn't capture output
    CompletedProcess(args=['ls', '-l'], returncode=0)

    >>> subprocess.run("exit 1", shell=True, check=True)
    Traceback (most recent call last):
      ...
    subprocess.CalledProcessError: Command 'exit 1' returned non-zero exit status 1

    >>> subprocess.run(["ls", "-l", "/dev/null"], capture_output=True)
    CompletedProcess(args=['ls', '-l', '/dev/null'], returncode=0,
    stdout=b'crw-rw-rw- 1 root root 1, 3 Jan 23 16:23 /dev/null\n', stderr=b'')

::: versionadded
3.5
:::

::: versionchanged
3.6

Added *encoding* and *errors* parameters
:::

::: versionchanged
3.7

Added the *text* parameter, as a more understandable alias of *universal_newlines*. Added the *capture_output* parameter.
:::

::: versionchanged
3.12

Changed Windows shell search order for `shell=True`. The current directory and `%PATH%` are replaced with `%COMSPEC%` and `%SystemRoot%\System32\cmd.exe`. As a result, dropping a malicious program named `cmd.exe` into a current directory no longer works.
:::
:::::::

::::::::: CompletedProcess
The return value from `run`{.interpreted-text role="func"}, representing a process that has finished.

::: attribute
args

The arguments used to launch the process. This may be a list or a string.
:::

::: attribute
returncode

Exit status of the child process. Typically, an exit status of 0 indicates that it ran successfully.

A negative value `-N` indicates that the child was terminated by signal `N` (POSIX only).
:::

::: attribute
stdout

Captured stdout from the child process. A bytes sequence, or a string if `run`{.interpreted-text role="func"} was called with an encoding, errors, or text=True. `None` if stdout was not captured.

If you ran the process with `stderr=subprocess.STDOUT`, stdout and stderr will be combined in this attribute, and `stderr`{.interpreted-text role="attr"} will be `None`.
:::

::: attribute
stderr

Captured stderr from the child process. A bytes sequence, or a string if `run`{.interpreted-text role="func"} was called with an encoding, errors, or text=True. `None` if stderr was not captured.
:::

::: method
check_returncode()

If `returncode`{.interpreted-text role="attr"} is non-zero, raise a `CalledProcessError`{.interpreted-text role="exc"}.
:::

::: versionadded
3.5
:::
:::::::::

:::: data
DEVNULL

Special value that can be used as the *stdin*, *stdout* or *stderr* argument to `Popen`{.interpreted-text role="class"} and indicates that the special file `os.devnull`{.interpreted-text role="data"} will be used.

::: versionadded
3.3
:::
::::

::: data
PIPE

Special value that can be used as the *stdin*, *stdout* or *stderr* argument to `Popen`{.interpreted-text role="class"} and indicates that a pipe to the standard stream should be opened. Most useful with `Popen.communicate`{.interpreted-text role="meth"}.
:::

::: data
STDOUT

Special value that can be used as the *stderr* argument to `Popen`{.interpreted-text role="class"} and indicates that standard error should go into the same handle as standard output.
:::

:::: exception
SubprocessError

Base class for all other exceptions from this module.

::: versionadded
3.3
:::
::::

:::::::::: exception
TimeoutExpired

Subclass of `SubprocessError`{.interpreted-text role="exc"}, raised when a timeout expires while waiting for a child process.

::: attribute
cmd

Command that was used to spawn the child process.
:::

::: attribute
timeout

Timeout in seconds.
:::

::: attribute
output

Output of the child process if it was captured by `run`{.interpreted-text role="func"} or `check_output`{.interpreted-text role="func"}. Otherwise, `None`. This is always `bytes`{.interpreted-text role="class"} when any output was captured regardless of the `text=True` setting. It may remain `None` instead of `b''` when no output was observed.
:::

::: attribute
stdout

Alias for output, for symmetry with `stderr`{.interpreted-text role="attr"}.
:::

::: attribute
stderr

Stderr output of the child process if it was captured by `run`{.interpreted-text role="func"}. Otherwise, `None`. This is always `bytes`{.interpreted-text role="class"} when stderr output was captured regardless of the `text=True` setting. It may remain `None` instead of `b''` when no stderr output was observed.
:::

::: versionadded
3.3
:::

::: versionchanged
3.5 *stdout* and *stderr* attributes added
:::
::::::::::

::::::::: exception
CalledProcessError

Subclass of `SubprocessError`{.interpreted-text role="exc"}, raised when a process run by `check_call`{.interpreted-text role="func"}, `check_output`{.interpreted-text role="func"}, or `run`{.interpreted-text role="func"} (with `check=True`) returns a non-zero exit status.

::: attribute
returncode

Exit status of the child process. If the process exited due to a signal, this will be the negative signal number.
:::

::: attribute
cmd

Command that was used to spawn the child process.
:::

::: attribute
output

Output of the child process if it was captured by `run`{.interpreted-text role="func"} or `check_output`{.interpreted-text role="func"}. Otherwise, `None`.
:::

::: attribute
stdout

Alias for output, for symmetry with `stderr`{.interpreted-text role="attr"}.
:::

::: attribute
stderr

Stderr output of the child process if it was captured by `run`{.interpreted-text role="func"}. Otherwise, `None`.
:::

::: versionchanged
3.5 *stdout* and *stderr* attributes added
:::
:::::::::

### Frequently Used Arguments

To support a wide variety of use cases, the `Popen`{.interpreted-text role="class"} constructor (and the convenience functions) accept a large number of optional arguments. For most typical use cases, many of these arguments can be safely left at their default values. The arguments that are most commonly needed are:

> *args* is required for all calls and should be a string, or a sequence of program arguments. Providing a sequence of arguments is generally preferred, as it allows the module to take care of any required escaping and quoting of arguments (e.g. to permit spaces in file names). If passing a single string, either *shell* must be `True`{.interpreted-text role="const"} (see below) or else the string must simply name the program to be executed without specifying any arguments.
>
> *stdin*, *stdout* and *stderr* specify the executed program\'s standard input, standard output and standard error file handles, respectively. Valid values are `None`, `PIPE`{.interpreted-text role="data"}, `DEVNULL`{.interpreted-text role="data"}, an existing file descriptor (a positive integer), and an existing `file object`{.interpreted-text role="term"} with a valid file descriptor. With the default settings of `None`, no redirection will occur. `PIPE`{.interpreted-text role="data"} indicates that a new pipe to the child should be created. `DEVNULL`{.interpreted-text role="data"} indicates that the special file `os.devnull`{.interpreted-text role="data"} will be used. Additionally, *stderr* can be `STDOUT`{.interpreted-text role="data"}, which indicates that the stderr data from the child process should be captured into the same file handle as for *stdout*.
>
> ::: index
> single: universal newlines; subprocess module
> :::
>
> If *encoding* or *errors* are specified, or *text* (also known as *universal_newlines*) is true, the file objects *stdin*, *stdout* and *stderr* will be opened in text mode using the *encoding* and *errors* specified in the call or the defaults for `io.TextIOWrapper`{.interpreted-text role="class"}.
>
> For *stdin*, line ending characters `'\n'` in the input will be converted to the default line separator `os.linesep`{.interpreted-text role="data"}. For *stdout* and *stderr*, all line endings in the output will be converted to `'\n'`. For more information see the documentation of the `io.TextIOWrapper`{.interpreted-text role="class"} class when the *newline* argument to its constructor is `None`.
>
> If text mode is not used, *stdin*, *stdout* and *stderr* will be opened as binary streams. No encoding or line ending conversion is performed.
>
> ::: versionchanged
> 3.6 Added the *encoding* and *errors* parameters.
> :::
>
> ::: versionchanged
> 3.7 Added the *text* parameter as an alias for *universal_newlines*.
> :::
>
> :::: note
> ::: title
> Note
> :::
>
> The newlines attribute of the file objects `Popen.stdin`{.interpreted-text role="attr"}, `Popen.stdout`{.interpreted-text role="attr"} and `Popen.stderr`{.interpreted-text role="attr"} are not updated by the `Popen.communicate`{.interpreted-text role="meth"} method.
> ::::
>
> If *shell* is `True`, the specified command will be executed through the shell. This can be useful if you are using Python primarily for the enhanced control flow it offers over most system shells and still want convenient access to other shell features such as shell pipes, filename wildcards, environment variable expansion, and expansion of `~` to a user\'s home directory. However, note that Python itself offers implementations of many shell-like features (in particular, `glob`{.interpreted-text role="mod"}, `fnmatch`{.interpreted-text role="mod"}, `os.walk`{.interpreted-text role="func"}, `os.path.expandvars`{.interpreted-text role="func"}, `os.path.expanduser`{.interpreted-text role="func"}, and `shutil`{.interpreted-text role="mod"}).
>
> ::: versionchanged
> 3.3 When *universal_newlines* is `True`, the class uses the encoding `locale.getpreferredencoding(False) <locale.getpreferredencoding>`{.interpreted-text role="func"} instead of `locale.getpreferredencoding()`. See the `io.TextIOWrapper`{.interpreted-text role="class"} class for more information on this change.
> :::
>
> :::: note
> ::: title
> Note
> :::
>
> Read the [Security Considerations](#security-considerations) section before using `shell=True`.
> ::::

These options, along with all of the other options, are described in more detail in the `Popen`{.interpreted-text role="class"} constructor documentation.

### Popen Constructor

The underlying process creation and management in this module is handled by the `Popen`{.interpreted-text role="class"} class. It offers a lot of flexibility so that developers are able to handle the less common cases not covered by the convenience functions.

:::::::::::::::::::::::::::::::::::::::::::::::: {.Popen(args, .bufsize=-1, .executable=None, .stdin=None, .stdout=None, .\\ .stderr=None, .preexec_fn=None, .close_fds=True, .shell=False, .\\ .cwd=None, .env=None, .universal_newlines=None, .\\ .startupinfo=None, .creationflags=0, .restore_signals=True, .\\ .start_new_session=False, .pass_fds=(), .*, .group=None, .\\ .extra_groups=None, .user=None, .umask=-1, .\\ .encoding=None, .errors=None, .text=None, .pipesize=-1, .\\ .process_group=None)}
Execute a child program in a new process. On POSIX, the class uses `os.execvpe`{.interpreted-text role="meth"}-like behavior to execute the child program. On Windows, the class uses the Windows `CreateProcess()` function. The arguments to `Popen`{.interpreted-text role="class"} are as follows.

*args* should be a sequence of program arguments or else a single string or `path-like object`{.interpreted-text role="term"}. By default, the program to execute is the first item in *args* if *args* is a sequence. If *args* is a string, the interpretation is platform-dependent and described below. See the *shell* and *executable* arguments for additional differences from the default behavior. Unless otherwise stated, it is recommended to pass *args* as a sequence.

:::: warning
::: title
Warning
:::

For maximum reliability, use a fully qualified path for the executable. To search for an unqualified name on `PATH`{.interpreted-text role="envvar"}, use `shutil.which`{.interpreted-text role="meth"}. On all platforms, passing `sys.executable`{.interpreted-text role="data"} is the recommended way to launch the current Python interpreter again, and use the `-m` command-line format to launch an installed module.

Resolving the path of *executable* (or the first item of *args*) is platform dependent. For POSIX, see `os.execvpe`{.interpreted-text role="meth"}, and note that when resolving or searching for the executable path, *cwd* overrides the current working directory and *env* can override the `PATH` environment variable. For Windows, see the documentation of the `lpApplicationName` and `lpCommandLine` parameters of WinAPI `CreateProcess`, and note that when resolving or searching for the executable path with `shell=False`, *cwd* does not override the current working directory and *env* cannot override the `PATH` environment variable. Using a full path avoids all of these variations.
::::

An example of passing some arguments to an external program as a sequence is:

    Popen(["/usr/bin/git", "commit", "-m", "Fixes a bug."])

On POSIX, if *args* is a string, the string is interpreted as the name or path of the program to execute. However, this can only be done if not passing arguments to the program.

:::: note
::: title
Note
:::

It may not be obvious how to break a shell command into a sequence of arguments, especially in complex cases. `shlex.split`{.interpreted-text role="meth"} can illustrate how to determine the correct tokenization for *args*:

    >>> import shlex, subprocess
    >>> command_line = input()
    /bin/vikings -input eggs.txt -output "spam spam.txt" -cmd "echo '$MONEY'"
    >>> args = shlex.split(command_line)
    >>> print(args)
    ['/bin/vikings', '-input', 'eggs.txt', '-output', 'spam spam.txt', '-cmd', "echo '$MONEY'"]
    >>> p = subprocess.Popen(args) # Success!

Note in particular that options (such as *-input*) and arguments (such as *eggs.txt*) that are separated by whitespace in the shell go in separate list elements, while arguments that need quoting or backslash escaping when used in the shell (such as filenames containing spaces or the *echo* command shown above) are single list elements.
::::

On Windows, if *args* is a sequence, it will be converted to a string in a manner described in `converting-argument-sequence`{.interpreted-text role="ref"}. This is because the underlying `CreateProcess()` operates on strings.

::: versionchanged
3.6 *args* parameter accepts a `path-like object`{.interpreted-text role="term"} if *shell* is `False` and a sequence containing path-like objects on POSIX.
:::

::: versionchanged
3.8 *args* parameter accepts a `path-like object`{.interpreted-text role="term"} if *shell* is `False` and a sequence containing bytes and path-like objects on Windows.
:::

The *shell* argument (which defaults to `False`) specifies whether to use the shell as the program to execute. If *shell* is `True`, it is recommended to pass *args* as a string rather than as a sequence.

On POSIX with `shell=True`, the shell defaults to `/bin/sh`{.interpreted-text role="file"}. If *args* is a string, the string specifies the command to execute through the shell. This means that the string must be formatted exactly as it would be when typed at the shell prompt. This includes, for example, quoting or backslash escaping filenames with spaces in them. If *args* is a sequence, the first item specifies the command string, and any additional items will be treated as additional arguments to the shell itself. That is to say, `Popen`{.interpreted-text role="class"} does the equivalent of:

    Popen(['/bin/sh', '-c', args[0], args[1], ...])

On Windows with `shell=True`, the `COMSPEC`{.interpreted-text role="envvar"} environment variable specifies the default shell. The only time you need to specify `shell=True` on Windows is when the command you wish to execute is built into the shell (e.g. `dir`{.interpreted-text role="command"} or `copy`{.interpreted-text role="command"}). You do not need `shell=True` to run a batch file or console-based executable.

:::: note
::: title
Note
:::

Read the [Security Considerations](#security-considerations) section before using `shell=True`.
::::

*bufsize* will be supplied as the corresponding argument to the `open`{.interpreted-text role="func"} function when creating the stdin/stdout/stderr pipe file objects:

- `0` means unbuffered (read and write are one system call and can return short)
- `1` means line buffered (only usable if `text=True` or `universal_newlines=True`)
- any other positive value means use a buffer of approximately that size
- negative bufsize (the default) means the system default of io.DEFAULT_BUFFER_SIZE will be used.

::: versionchanged
3.3.1 *bufsize* now defaults to -1 to enable buffering by default to match the behavior that most code expects. In versions prior to Python 3.2.4 and 3.3.1 it incorrectly defaulted to `0` which was unbuffered and allowed short reads. This was unintentional and did not match the behavior of Python 2 as most code expected.
:::

The *executable* argument specifies a replacement program to execute. It is very seldom needed. When `shell=False`, *executable* replaces the program to execute specified by *args*. However, the original *args* is still passed to the program. Most programs treat the program specified by *args* as the command name, which can then be different from the program actually executed. On POSIX, the *args* name becomes the display name for the executable in utilities such as `ps`{.interpreted-text role="program"}. If `shell=True`, on POSIX the *executable* argument specifies a replacement shell for the default `/bin/sh`{.interpreted-text role="file"}.

::: versionchanged
3.6 *executable* parameter accepts a `path-like object`{.interpreted-text role="term"} on POSIX.
:::

::: versionchanged
3.8 *executable* parameter accepts a bytes and `path-like object`{.interpreted-text role="term"} on Windows.
:::

::: versionchanged
3.12

Changed Windows shell search order for `shell=True`. The current directory and `%PATH%` are replaced with `%COMSPEC%` and `%SystemRoot%\System32\cmd.exe`. As a result, dropping a malicious program named `cmd.exe` into a current directory no longer works.
:::

*stdin*, *stdout* and *stderr* specify the executed program\'s standard input, standard output and standard error file handles, respectively. Valid values are `None`, `PIPE`{.interpreted-text role="data"}, `DEVNULL`{.interpreted-text role="data"}, an existing file descriptor (a positive integer), and an existing `file object`{.interpreted-text role="term"} with a valid file descriptor. With the default settings of `None`, no redirection will occur. `PIPE`{.interpreted-text role="data"} indicates that a new pipe to the child should be created. `DEVNULL`{.interpreted-text role="data"} indicates that the special file `os.devnull`{.interpreted-text role="data"} will be used. Additionally, *stderr* can be `STDOUT`{.interpreted-text role="data"}, which indicates that the stderr data from the applications should be captured into the same file handle as for *stdout*.

If *preexec_fn* is set to a callable object, this object will be called in the child process just before the child is executed. (POSIX only)

:::: warning
::: title
Warning
:::

The *preexec_fn* parameter is NOT SAFE to use in the presence of threads in your application. The child process could deadlock before exec is called.
::::

:::: note
::: title
Note
:::

If you need to modify the environment for the child use the *env* parameter rather than doing it in a *preexec_fn*. The *start_new_session* and *process_group* parameters should take the place of code using *preexec_fn* to call `os.setsid`{.interpreted-text role="func"} or `os.setpgid`{.interpreted-text role="func"} in the child.
::::

::: versionchanged
3.8

The *preexec_fn* parameter is no longer supported in subinterpreters. The use of the parameter in a subinterpreter raises `RuntimeError`{.interpreted-text role="exc"}. The new restriction may affect applications that are deployed in mod_wsgi, uWSGI, and other embedded environments.
:::

If *close_fds* is true, all file descriptors except `0`, `1` and `2` will be closed before the child process is executed. Otherwise when *close_fds* is false, file descriptors obey their inheritable flag as described in `fd_inheritance`{.interpreted-text role="ref"}.

On Windows, if *close_fds* is true then no handles will be inherited by the child process unless explicitly passed in the `handle_list` element of `STARTUPINFO.lpAttributeList`{.interpreted-text role="attr"}, or by standard handle redirection.

::: versionchanged
3.2 The default for *close_fds* was changed from `False`{.interpreted-text role="const"} to what is described above.
:::

::: versionchanged
3.7 On Windows the default for *close_fds* was changed from `False`{.interpreted-text role="const"} to `True`{.interpreted-text role="const"} when redirecting the standard handles. It\'s now possible to set *close_fds* to `True`{.interpreted-text role="const"} when redirecting the standard handles.
:::

*pass_fds* is an optional sequence of file descriptors to keep open between the parent and child. Providing any *pass_fds* forces *close_fds* to be `True`{.interpreted-text role="const"}. (POSIX only)

::: versionchanged
3.2 The *pass_fds* parameter was added.
:::

If *cwd* is not `None`, the function changes the working directory to *cwd* before executing the child. *cwd* can be a string, bytes or `path-like <path-like object>`{.interpreted-text role="term"} object. On POSIX, the function looks for *executable* (or for the first item in *args*) relative to *cwd* if the executable path is a relative path.

::: versionchanged
3.6 *cwd* parameter accepts a `path-like object`{.interpreted-text role="term"} on POSIX.
:::

::: versionchanged
3.7 *cwd* parameter accepts a `path-like object`{.interpreted-text role="term"} on Windows.
:::

::: versionchanged
3.8 *cwd* parameter accepts a bytes object on Windows.
:::

If *restore_signals* is true (the default) all signals that Python has set to SIG_IGN are restored to SIG_DFL in the child process before the exec. Currently this includes the SIGPIPE, SIGXFZ and SIGXFSZ signals. (POSIX only)

::: versionchanged
3.2 *restore_signals* was added.
:::

If *start_new_session* is true the `setsid()` system call will be made in the child process prior to the execution of the subprocess.

::: availability
POSIX
:::

::: versionchanged
3.2 *start_new_session* was added.
:::

If *process_group* is a non-negative integer, the `setpgid(0, value)` system call will be made in the child process prior to the execution of the subprocess.

::: availability
POSIX
:::

::: versionchanged
3.11 *process_group* was added.
:::

If *group* is not `None`, the setregid() system call will be made in the child process prior to the execution of the subprocess. If the provided value is a string, it will be looked up via `grp.getgrnam`{.interpreted-text role="func"} and the value in `gr_gid` will be used. If the value is an integer, it will be passed verbatim. (POSIX only)

::: availability
POSIX
:::

::: versionadded
3.9
:::

If *extra_groups* is not `None`, the setgroups() system call will be made in the child process prior to the execution of the subprocess. Strings provided in *extra_groups* will be looked up via `grp.getgrnam`{.interpreted-text role="func"} and the values in `gr_gid` will be used. Integer values will be passed verbatim. (POSIX only)

::: availability
POSIX
:::

::: versionadded
3.9
:::

If *user* is not `None`, the setreuid() system call will be made in the child process prior to the execution of the subprocess. If the provided value is a string, it will be looked up via `pwd.getpwnam`{.interpreted-text role="func"} and the value in `pw_uid` will be used. If the value is an integer, it will be passed verbatim. (POSIX only)

::: availability
POSIX
:::

::: versionadded
3.9
:::

If *umask* is not negative, the umask() system call will be made in the child process prior to the execution of the subprocess.

::: availability
POSIX
:::

::: versionadded
3.9
:::

If *env* is not `None`, it must be a mapping that defines the environment variables for the new process; these are used instead of the default behavior of inheriting the current process\' environment. This mapping can be str to str on any platform or bytes to bytes on POSIX platforms much like `os.environ`{.interpreted-text role="data"} or `os.environb`{.interpreted-text role="data"}.

:::: note
::: title
Note
:::

If specified, *env* must provide any variables required for the program to execute. On Windows, in order to run a [side-by-side assembly](https://en.wikipedia.org/wiki/Side-by-Side_Assembly) the specified *env* **must** include a valid `%SystemRoot%`.
::::

If *encoding* or *errors* are specified, or *text* is true, the file objects *stdin*, *stdout* and *stderr* are opened in text mode with the specified *encoding* and *errors*, as described above in `frequently-used-arguments`{.interpreted-text role="ref"}. The *universal_newlines* argument is equivalent to *text* and is provided for backwards compatibility. By default, file objects are opened in binary mode.

::: versionadded
3.6 *encoding* and *errors* were added.
:::

::: versionadded
3.7 *text* was added as a more readable alias for *universal_newlines*.
:::

If given, *startupinfo* will be a `STARTUPINFO`{.interpreted-text role="class"} object, which is passed to the underlying `CreateProcess` function.

If given, *creationflags*, can be one or more of the following flags:

- `CREATE_NEW_CONSOLE`{.interpreted-text role="data"}
- `CREATE_NEW_PROCESS_GROUP`{.interpreted-text role="data"}
- `ABOVE_NORMAL_PRIORITY_CLASS`{.interpreted-text role="data"}
- `BELOW_NORMAL_PRIORITY_CLASS`{.interpreted-text role="data"}
- `HIGH_PRIORITY_CLASS`{.interpreted-text role="data"}
- `IDLE_PRIORITY_CLASS`{.interpreted-text role="data"}
- `NORMAL_PRIORITY_CLASS`{.interpreted-text role="data"}
- `REALTIME_PRIORITY_CLASS`{.interpreted-text role="data"}
- `CREATE_NO_WINDOW`{.interpreted-text role="data"}
- `DETACHED_PROCESS`{.interpreted-text role="data"}
- `CREATE_DEFAULT_ERROR_MODE`{.interpreted-text role="data"}
- `CREATE_BREAKAWAY_FROM_JOB`{.interpreted-text role="data"}

*pipesize* can be used to change the size of the pipe when `PIPE`{.interpreted-text role="data"} is used for *stdin*, *stdout* or *stderr*. The size of the pipe is only changed on platforms that support this (only Linux at this time of writing). Other platforms will ignore this parameter.

::: versionchanged
3.10 Added the *pipesize* parameter.
:::

Popen objects are supported as context managers via the `with`{.interpreted-text role="keyword"} statement: on exit, standard file descriptors are closed, and the process is waited for. :

    with Popen(["ifconfig"], stdout=PIPE) as proc:
        log.write(proc.stdout.read())

::: audit-event
subprocess.Popen executable,args,cwd,env subprocess.Popen

Popen and the other functions in this module that use it raise an `auditing event <auditing>`{.interpreted-text role="ref"} `subprocess.Popen` with arguments `executable`, `args`, `cwd`, and `env`. The value for `args` may be a single string or a list of strings, depending on platform.
:::

::: versionchanged
3.2 Added context manager support.
:::

::: versionchanged
3.6 Popen destructor now emits a `ResourceWarning`{.interpreted-text role="exc"} warning if the child process is still running.
:::

::: versionchanged
3.8 Popen can use `os.posix_spawn`{.interpreted-text role="func"} in some cases for better performance. On Windows Subsystem for Linux and QEMU User Emulation, Popen constructor using `os.posix_spawn`{.interpreted-text role="func"} no longer raise an exception on errors like missing program, but the child process fails with a non-zero `~Popen.returncode`{.interpreted-text role="attr"}.
:::
::::::::::::::::::::::::::::::::::::::::::::::::

### Exceptions

Exceptions raised in the child process, before the new program has started to execute, will be re-raised in the parent.

The most common exception raised is `OSError`{.interpreted-text role="exc"}. This occurs, for example, when trying to execute a non-existent file. Applications should prepare for `OSError`{.interpreted-text role="exc"} exceptions. Note that, when `shell=True`, `OSError`{.interpreted-text role="exc"} will be raised by the child only if the selected shell itself was not found. To determine if the shell failed to find the requested application, it is necessary to check the return code or output from the subprocess.

A `ValueError`{.interpreted-text role="exc"} will be raised if `Popen`{.interpreted-text role="class"} is called with invalid arguments.

`check_call`{.interpreted-text role="func"} and `check_output`{.interpreted-text role="func"} will raise `CalledProcessError`{.interpreted-text role="exc"} if the called process returns a non-zero return code.

All of the functions and methods that accept a *timeout* parameter, such as `run`{.interpreted-text role="func"} and `Popen.communicate`{.interpreted-text role="meth"} will raise `TimeoutExpired`{.interpreted-text role="exc"} if the timeout expires before the process exits.

Exceptions defined in this module all inherit from `SubprocessError`{.interpreted-text role="exc"}.

::: versionadded
3.3 The `SubprocessError`{.interpreted-text role="exc"} base class was added.
:::

## Security Considerations {#subprocess-security}

Unlike some other popen functions, this library will not implicitly choose to call a system shell. This means that all characters, including shell metacharacters, can safely be passed to child processes. If the shell is invoked explicitly, via `shell=True`, it is the application\'s responsibility to ensure that all whitespace and metacharacters are quoted appropriately to avoid [shell injection](https://en.wikipedia.org/wiki/Shell_injection#Shell_injection) vulnerabilities. On `some platforms <shlex-quote-warning>`{.interpreted-text role="ref"}, it is possible to use `shlex.quote`{.interpreted-text role="func"} for this escaping.

On Windows, batch files (`*.bat`{.interpreted-text role="file"} or `*.cmd`{.interpreted-text role="file"}) may be launched by the operating system in a system shell regardless of the arguments passed to this library. This could result in arguments being parsed according to shell rules, but without any escaping added by Python. If you are intentionally launching a batch file with arguments from untrusted sources, consider passing `shell=True` to allow Python to escape special characters. See `114539`{.interpreted-text role="gh"} for additional discussion.

## Popen Objects

Instances of the `Popen`{.interpreted-text role="class"} class have the following methods:

::: method
Popen.poll()

Check if child process has terminated. Set and return `~Popen.returncode`{.interpreted-text role="attr"} attribute. Otherwise, returns `None`.
:::

::::::::::: method
Popen.wait(timeout=None)

Wait for child process to terminate. Set and return `~Popen.returncode`{.interpreted-text role="attr"} attribute.

If the process does not terminate after *timeout* seconds, raise a `TimeoutExpired`{.interpreted-text role="exc"} exception. It is safe to catch this exception and retry the wait.

:::: note
::: title
Note
:::

This will deadlock when using `stdout=PIPE` or `stderr=PIPE` and the child process generates enough output to a pipe such that it blocks waiting for the OS pipe buffer to accept more data. Use `Popen.communicate`{.interpreted-text role="meth"} when using pipes to avoid that.
::::

:::: note
::: title
Note
:::

When `timeout` is not `None` and the platform supports it, an efficient event-driven mechanism is used to wait for process termination:

- Linux \>= 5.3 uses `os.pidfd_open`{.interpreted-text role="func"} + `select.poll`{.interpreted-text role="func"}
- macOS and other BSD variants use `select.kqueue`{.interpreted-text role="func"} + `KQ_FILTER_PROC` + `KQ_NOTE_EXIT`
- Windows uses `WaitForSingleObject`

If none of these mechanisms are available, the function falls back to a busy loop (non-blocking call and short sleeps).
::::

:::: note
::: title
Note
:::

Use the `asyncio`{.interpreted-text role="mod"} module for an asynchronous wait: see `asyncio.create_subprocess_exec`{.interpreted-text role="class"}.
::::

::: versionchanged
3.3 *timeout* was added.
:::

::: versionchanged
3.15 if *timeout* is not `None`, use efficient event-driven implementation on Linux \>= 5.3 and macOS / BSD.
:::
:::::::::::

:::::: method
Popen.communicate(input=None, timeout=None)

Interact with process: Send data to stdin. Read data from stdout and stderr, until end-of-file is reached. Wait for process to terminate and set the `~Popen.returncode`{.interpreted-text role="attr"} attribute. The optional *input* argument should be data to be sent to the child process, or `None`, if no data should be sent to the child. If streams were opened in text mode, *input* must be a string. Otherwise, it must be bytes.

`communicate`{.interpreted-text role="meth"} returns a tuple `(stdout_data, stderr_data)`. The data will be strings if streams were opened in text mode; otherwise, bytes.

Note that if you want to send data to the process\'s stdin, you need to create the Popen object with `stdin=PIPE`. Similarly, to get anything other than `None` in the result tuple, you need to give `stdout=PIPE` and/or `stderr=PIPE` too.

If the process does not terminate after *timeout* seconds, a `TimeoutExpired`{.interpreted-text role="exc"} exception will be raised. Catching this exception and retrying communication will not lose any output. Supplying *input* to a subsequent post-timeout `communicate`{.interpreted-text role="meth"} call is in undefined behavior and may become an error in the future.

The child process is not killed if the timeout expires, so in order to cleanup properly a well-behaved application should kill the child process and finish communication:

    proc = subprocess.Popen(...)
    try:
        outs, errs = proc.communicate(timeout=15)
    except TimeoutExpired:
        proc.kill()
        outs, errs = proc.communicate()

After a call to `~Popen.communicate`{.interpreted-text role="meth"} raises `TimeoutExpired`{.interpreted-text role="exc"}, do not call `~Popen.wait`{.interpreted-text role="meth"}. Use an additional `~Popen.communicate`{.interpreted-text role="meth"} call to finish handling pipes and populate the `~Popen.returncode`{.interpreted-text role="attr"} attribute.

:::: note
::: title
Note
:::

The data read is buffered in memory, so do not use this method if the data size is large or unlimited.
::::

::: versionchanged
3.3 *timeout* was added.
:::
::::::

::::: method
Popen.send_signal(signal)

Sends the signal *signal* to the child.

Do nothing if the process completed.

:::: note
::: title
Note
:::

On Windows, SIGTERM is an alias for `terminate`{.interpreted-text role="meth"}. CTRL_C_EVENT and CTRL_BREAK_EVENT can be sent to processes started with a *creationflags* parameter which includes `CREATE_NEW_PROCESS_GROUP`.
::::
:::::

::: method
Popen.terminate()

Stop the child. On POSIX OSs the method sends `~signal.SIGTERM`{.interpreted-text role="py:const"} to the child. On Windows the Win32 API function `!TerminateProcess`{.interpreted-text role="c:func"} is called to stop the child.
:::

::: method
Popen.kill()

Kills the child. On POSIX OSs the function sends SIGKILL to the child. On Windows `kill`{.interpreted-text role="meth"} is an alias for `terminate`{.interpreted-text role="meth"}.
:::

The following attributes are also set by the class for you to access. Reassigning them to new values is unsupported:

:::: attribute
Popen.args

The *args* argument as it was passed to `Popen`{.interpreted-text role="class"} \-- a sequence of program arguments or else a single string.

::: versionadded
3.3
:::
::::

::: attribute
Popen.stdin

If the *stdin* argument was `PIPE`{.interpreted-text role="data"}, this attribute is a writeable stream object as returned by `open`{.interpreted-text role="func"}. If the *encoding* or *errors* arguments were specified or the *text* or *universal_newlines* argument was `True`, the stream is a text stream, otherwise it is a byte stream. If the *stdin* argument was not `PIPE`{.interpreted-text role="data"}, this attribute is `None`.
:::

::: attribute
Popen.stdout

If the *stdout* argument was `PIPE`{.interpreted-text role="data"}, this attribute is a readable stream object as returned by `open`{.interpreted-text role="func"}. Reading from the stream provides output from the child process. If the *encoding* or *errors* arguments were specified or the *text* or *universal_newlines* argument was `True`, the stream is a text stream, otherwise it is a byte stream. If the *stdout* argument was not `PIPE`{.interpreted-text role="data"}, this attribute is `None`.
:::

::: attribute
Popen.stderr

If the *stderr* argument was `PIPE`{.interpreted-text role="data"}, this attribute is a readable stream object as returned by `open`{.interpreted-text role="func"}. Reading from the stream provides error output from the child process. If the *encoding* or *errors* arguments were specified or the *text* or *universal_newlines* argument was `True`, the stream is a text stream, otherwise it is a byte stream. If the *stderr* argument was not `PIPE`{.interpreted-text role="data"}, this attribute is `None`.
:::

:::: warning
::: title
Warning
:::

Use `~Popen.communicate`{.interpreted-text role="meth"} rather than `.stdin.write <Popen.stdin>`{.interpreted-text role="attr"}, `.stdout.read <Popen.stdout>`{.interpreted-text role="attr"} or `.stderr.read <Popen.stderr>`{.interpreted-text role="attr"} to avoid deadlocks due to any of the other OS pipe buffers filling up and blocking the child process.
::::

::: attribute
Popen.pid

The process ID of the child process.

Note that if you set the *shell* argument to `True`, this is the process ID of the spawned shell.
:::

::: attribute
Popen.returncode

The child return code. Initially `None`, `returncode`{.interpreted-text role="attr"} is set by a call to the `poll`{.interpreted-text role="meth"}, `wait`{.interpreted-text role="meth"}, or `communicate`{.interpreted-text role="meth"} methods if they detect that the process has terminated.

A `None` value indicates that the process hadn\'t yet terminated at the time of the last method call.

A negative value `-N` indicates that the child was terminated by signal `N` (POSIX only).
:::

## Windows Popen Helpers

The `STARTUPINFO`{.interpreted-text role="class"} class and following constants are only available on Windows.

::::::::::: {.STARTUPINFO(*, .dwFlags=0, .hStdInput=None, .hStdOutput=None, .\\ .hStdError=None, .wShowWindow=0, .lpAttributeList=None)}
Partial support of the Windows [STARTUPINFO](https://msdn.microsoft.com/en-us/library/ms686331(v=vs.85).aspx) structure is used for `Popen`{.interpreted-text role="class"} creation. The following attributes can be set by passing them as keyword-only arguments.

::: versionchanged
3.7 Keyword-only argument support was added.
:::

::: attribute
dwFlags

A bit field that determines whether certain `STARTUPINFO`{.interpreted-text role="class"} attributes are used when the process creates a window. :

    si = subprocess.STARTUPINFO()
    si.dwFlags = subprocess.STARTF_USESTDHANDLES | subprocess.STARTF_USESHOWWINDOW
:::

::: attribute
hStdInput

If `dwFlags`{.interpreted-text role="attr"} specifies `STARTF_USESTDHANDLES`{.interpreted-text role="data"}, this attribute is the standard input handle for the process. If `STARTF_USESTDHANDLES`{.interpreted-text role="data"} is not specified, the default for standard input is the keyboard buffer.
:::

::: attribute
hStdOutput

If `dwFlags`{.interpreted-text role="attr"} specifies `STARTF_USESTDHANDLES`{.interpreted-text role="data"}, this attribute is the standard output handle for the process. Otherwise, this attribute is ignored and the default for standard output is the console window\'s buffer.
:::

::: attribute
hStdError

If `dwFlags`{.interpreted-text role="attr"} specifies `STARTF_USESTDHANDLES`{.interpreted-text role="data"}, this attribute is the standard error handle for the process. Otherwise, this attribute is ignored and the default for standard error is the console window\'s buffer.
:::

::: attribute
wShowWindow

If `dwFlags`{.interpreted-text role="attr"} specifies `STARTF_USESHOWWINDOW`{.interpreted-text role="data"}, this attribute can be any of the values that can be specified in the `nCmdShow` parameter for the [ShowWindow](https://msdn.microsoft.com/en-us/library/ms633548(v=vs.85).aspx) function, except for `SW_SHOWDEFAULT`. Otherwise, this attribute is ignored.

`SW_HIDE`{.interpreted-text role="data"} is provided for this attribute. It is used when `Popen`{.interpreted-text role="class"} is called with `shell=True`.
:::

:::: attribute
lpAttributeList

A dictionary of additional attributes for process creation as given in `STARTUPINFOEX`, see [UpdateProcThreadAttribute](https://msdn.microsoft.com/en-us/library/windows/desktop/ms686880(v=vs.85).aspx).

Supported attributes:

**handle_list**

:   Sequence of handles that will be inherited. *close_fds* must be true if non-empty.

    The handles must be temporarily made inheritable by `os.set_handle_inheritable`{.interpreted-text role="func"} when passed to the `Popen`{.interpreted-text role="class"} constructor, else `OSError`{.interpreted-text role="class"} will be raised with Windows error `ERROR_INVALID_PARAMETER` (87).

    :::: warning
    ::: title
    Warning
    :::

    In a multithreaded process, use caution to avoid leaking handles that are marked inheritable when combining this feature with concurrent calls to other process creation functions that inherit all handles such as `os.system`{.interpreted-text role="func"}. This also applies to standard handle redirection, which temporarily creates inheritable handles.
    ::::

::: versionadded
3.7
:::
::::
:::::::::::

### Windows Constants

The `!subprocess`{.interpreted-text role="mod"} module exposes the following constants.

::: data
STD_INPUT_HANDLE

The standard input device. Initially, this is the console input buffer, `CONIN$`.
:::

::: data
STD_OUTPUT_HANDLE

The standard output device. Initially, this is the active console screen buffer, `CONOUT$`.
:::

::: data
STD_ERROR_HANDLE

The standard error device. Initially, this is the active console screen buffer, `CONOUT$`.
:::

::: data
SW_HIDE

Hides the window. Another window will be activated.
:::

::: data
STARTF_USESTDHANDLES

Specifies that the `STARTUPINFO.hStdInput`{.interpreted-text role="attr"}, `STARTUPINFO.hStdOutput`{.interpreted-text role="attr"}, and `STARTUPINFO.hStdError`{.interpreted-text role="attr"} attributes contain additional information.
:::

::: data
STARTF_USESHOWWINDOW

Specifies that the `STARTUPINFO.wShowWindow`{.interpreted-text role="attr"} attribute contains additional information.
:::

:::: data
STARTF_FORCEONFEEDBACK

A `STARTUPINFO.dwFlags`{.interpreted-text role="attr"} parameter to specify that the *Working in Background* mouse cursor will be displayed while a process is launching. This is the default behavior for GUI processes.

::: versionadded
3.13
:::
::::

:::: data
STARTF_FORCEOFFFEEDBACK

A `STARTUPINFO.dwFlags`{.interpreted-text role="attr"} parameter to specify that the mouse cursor will not be changed when launching a process.

::: versionadded
3.13
:::
::::

::: data
CREATE_NEW_CONSOLE

The new process has a new console, instead of inheriting its parent\'s console (the default).
:::

::: data
CREATE_NEW_PROCESS_GROUP

A `Popen`{.interpreted-text role="class"} `creationflags` parameter to specify that a new process group will be created. This flag is necessary for using `os.kill`{.interpreted-text role="func"} on the subprocess.

This flag is ignored if `CREATE_NEW_CONSOLE`{.interpreted-text role="data"} is specified.
:::

:::: data
ABOVE_NORMAL_PRIORITY_CLASS

A `Popen`{.interpreted-text role="class"} `creationflags` parameter to specify that a new process will have an above average priority.

::: versionadded
3.7
:::
::::

:::: data
BELOW_NORMAL_PRIORITY_CLASS

A `Popen`{.interpreted-text role="class"} `creationflags` parameter to specify that a new process will have a below average priority.

::: versionadded
3.7
:::
::::

:::: data
HIGH_PRIORITY_CLASS

A `Popen`{.interpreted-text role="class"} `creationflags` parameter to specify that a new process will have a high priority.

::: versionadded
3.7
:::
::::

:::: data
IDLE_PRIORITY_CLASS

A `Popen`{.interpreted-text role="class"} `creationflags` parameter to specify that a new process will have an idle (lowest) priority.

::: versionadded
3.7
:::
::::

:::: data
NORMAL_PRIORITY_CLASS

A `Popen`{.interpreted-text role="class"} `creationflags` parameter to specify that a new process will have a normal priority. (default)

::: versionadded
3.7
:::
::::

:::: data
REALTIME_PRIORITY_CLASS

A `Popen`{.interpreted-text role="class"} `creationflags` parameter to specify that a new process will have realtime priority. You should almost never use REALTIME_PRIORITY_CLASS, because this interrupts system threads that manage mouse input, keyboard input, and background disk flushing. This class can be appropriate for applications that \"talk\" directly to hardware or that perform brief tasks that should have limited interruptions.

::: versionadded
3.7
:::
::::

:::: data
CREATE_NO_WINDOW

A `Popen`{.interpreted-text role="class"} `creationflags` parameter to specify that a new process will not create a window.

::: versionadded
3.7
:::
::::

:::: data
DETACHED_PROCESS

A `Popen`{.interpreted-text role="class"} `creationflags` parameter to specify that a new process will not inherit its parent\'s console. This value cannot be used with CREATE_NEW_CONSOLE.

::: versionadded
3.7
:::
::::

:::: data
CREATE_DEFAULT_ERROR_MODE

A `Popen`{.interpreted-text role="class"} `creationflags` parameter to specify that a new process does not inherit the error mode of the calling process. Instead, the new process gets the default error mode. This feature is particularly useful for multithreaded shell applications that run with hard errors disabled.

::: versionadded
3.7
:::
::::

:::: data
CREATE_BREAKAWAY_FROM_JOB

A `Popen`{.interpreted-text role="class"} `creationflags` parameter to specify that a new process is not associated with the job.

::: versionadded
3.7
:::
::::

## Older high-level API {#call-function-trio}

Prior to Python 3.5, these three functions comprised the high level API to subprocess. You can now use `run`{.interpreted-text role="func"} in many cases, but lots of existing code calls these functions.

::::::: function
call(args, *, stdin=None, stdout=None, stderr=None, shell=False, cwd=None, timeout=None,*\*other_popen_kwargs)

Run the command described by *args*. Wait for command to complete, then return the `~Popen.returncode`{.interpreted-text role="attr"} attribute.

Code needing to capture stdout or stderr should use `run`{.interpreted-text role="func"} instead:

    run(...).returncode

To suppress stdout or stderr, supply a value of `DEVNULL`{.interpreted-text role="data"}.

The arguments shown above are merely some common ones. The full function signature is the same as that of the `Popen`{.interpreted-text role="class"} constructor - this function passes all supplied arguments other than *timeout* directly through to that interface.

:::: note
::: title
Note
:::

Do not use `stdout=PIPE` or `stderr=PIPE` with this function. The child process will block if it generates enough output to a pipe to fill up the OS pipe buffer as the pipes are not being read from.
::::

::: versionchanged
3.3 *timeout* was added.
:::

::: versionchanged
3.12

Changed Windows shell search order for `shell=True`. The current directory and `%PATH%` are replaced with `%COMSPEC%` and `%SystemRoot%\System32\cmd.exe`. As a result, dropping a malicious program named `cmd.exe` into a current directory no longer works.
:::
:::::::

::::::: function
check_call(args, *, stdin=None, stdout=None, stderr=None, shell=False, cwd=None, timeout=None,*\*other_popen_kwargs)

Run command with arguments. Wait for command to complete. If the return code was zero then return, otherwise raise `CalledProcessError`{.interpreted-text role="exc"}. The `CalledProcessError`{.interpreted-text role="exc"} object will have the return code in the `~CalledProcessError.returncode`{.interpreted-text role="attr"} attribute. If `check_call`{.interpreted-text role="func"} was unable to start the process it will propagate the exception that was raised.

Code needing to capture stdout or stderr should use `run`{.interpreted-text role="func"} instead:

    run(..., check=True)

To suppress stdout or stderr, supply a value of `DEVNULL`{.interpreted-text role="data"}.

The arguments shown above are merely some common ones. The full function signature is the same as that of the `Popen`{.interpreted-text role="class"} constructor - this function passes all supplied arguments other than *timeout* directly through to that interface.

:::: note
::: title
Note
:::

Do not use `stdout=PIPE` or `stderr=PIPE` with this function. The child process will block if it generates enough output to a pipe to fill up the OS pipe buffer as the pipes are not being read from.
::::

::: versionchanged
3.3 *timeout* was added.
:::

::: versionchanged
3.12

Changed Windows shell search order for `shell=True`. The current directory and `%PATH%` are replaced with `%COMSPEC%` and `%SystemRoot%\System32\cmd.exe`. As a result, dropping a malicious program named `cmd.exe` into a current directory no longer works.
:::
:::::::

::::::::: function
check_output(args, *, stdin=None, stderr=None, shell=False, cwd=None, encoding=None, errors=None, universal_newlines=None, timeout=None, text=None,*\*other_popen_kwargs)

Run command with arguments and return its output.

If the return code was non-zero it raises a `CalledProcessError`{.interpreted-text role="exc"}. The `CalledProcessError`{.interpreted-text role="exc"} object will have the return code in the `~CalledProcessError.returncode`{.interpreted-text role="attr"} attribute and any output in the `~CalledProcessError.output`{.interpreted-text role="attr"} attribute.

This is equivalent to:

    run(..., check=True, stdout=PIPE).stdout

The arguments shown above are merely some common ones. The full function signature is largely the same as that of `run`{.interpreted-text role="func"} - most arguments are passed directly through to that interface. One API deviation from `run`{.interpreted-text role="func"} behavior exists: passing `input=None` will behave the same as `input=b''` (or `input=''`, depending on other arguments) rather than using the parent\'s standard input file handle.

By default, this function will return the data as encoded bytes. The actual encoding of the output data may depend on the command being invoked, so the decoding to text will often need to be handled at the application level.

This behaviour may be overridden by setting *text*, *encoding*, *errors*, or *universal_newlines* to `True` as described in `frequently-used-arguments`{.interpreted-text role="ref"} and `run`{.interpreted-text role="func"}.

To also capture standard error in the result, use `stderr=subprocess.STDOUT`:

    >>> subprocess.check_output(
    ...     "ls non_existent_file; exit 0",
    ...     stderr=subprocess.STDOUT,
    ...     shell=True)
    'ls: non_existent_file: No such file or directory\n'

::: versionadded
3.1
:::

::: versionchanged
3.3 *timeout* was added.
:::

::: versionchanged
3.4 Support for the *input* keyword argument was added.
:::

::: versionchanged
3.6 *encoding* and *errors* were added. See `run`{.interpreted-text role="func"} for details.
:::

::: versionadded
3.7 *text* was added as a more readable alias for *universal_newlines*.
:::

::: versionchanged
3.12

Changed Windows shell search order for `shell=True`. The current directory and `%PATH%` are replaced with `%COMSPEC%` and `%SystemRoot%\System32\cmd.exe`. As a result, dropping a malicious program named `cmd.exe` into a current directory no longer works.
:::
:::::::::

## Replacing Older Functions with the `!subprocess`{.interpreted-text role="mod"} Module {#subprocess-replacements}

In this section, \"a becomes b\" means that b can be used as a replacement for a.

:::: note
::: title
Note
:::

All \"a\" functions in this section fail (more or less) silently if the executed program cannot be found; the \"b\" replacements raise `OSError`{.interpreted-text role="exc"} instead.

In addition, the replacements using `check_output`{.interpreted-text role="func"} will fail with a `CalledProcessError`{.interpreted-text role="exc"} if the requested operation produces a non-zero return code. The output is still available as the `~CalledProcessError.output`{.interpreted-text role="attr"} attribute of the raised exception.
::::

In the following examples, we assume that the relevant functions have already been imported from the `!subprocess`{.interpreted-text role="mod"} module.

### Replacing `/bin/sh`{.interpreted-text role="program"} shell command substitution

``` bash
output=$(mycmd myarg)
```

becomes:

    output = check_output(["mycmd", "myarg"])

### Replacing shell pipeline

``` bash
output=$(dmesg | grep hda)
```

becomes:

    p1 = Popen(["dmesg"], stdout=PIPE)
    p2 = Popen(["grep", "hda"], stdin=p1.stdout, stdout=PIPE)
    p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
    output = p2.communicate()[0]

The `p1.stdout.close()` call after starting the p2 is important in order for p1 to receive a SIGPIPE if p2 exits before p1.

Alternatively, for trusted input, the shell\'s own pipeline support may still be used directly:

``` bash
output=$(dmesg | grep hda)
```

becomes:

    output = check_output("dmesg | grep hda", shell=True)

### Replacing `os.system`{.interpreted-text role="func"}

    sts = os.system("mycmd" + " myarg")
    # becomes
    retcode = call("mycmd" + " myarg", shell=True)

Notes:

- Calling the program through the shell is usually not required.
- The `call`{.interpreted-text role="func"} return value is encoded differently to that of `os.system`{.interpreted-text role="func"}.
- The `os.system`{.interpreted-text role="func"} function ignores SIGINT and SIGQUIT signals while the command is running, but the caller must do this separately when using the `!subprocess`{.interpreted-text role="mod"} module.

A more realistic example would look like this:

    try:
        retcode = call("mycmd" + " myarg", shell=True)
        if retcode < 0:
            print("Child was terminated by signal", -retcode, file=sys.stderr)
        else:
            print("Child returned", retcode, file=sys.stderr)
    except OSError as e:
        print("Execution failed:", e, file=sys.stderr)

### Replacing the `os.spawn <os.spawnl>`{.interpreted-text role="func"} family

P_NOWAIT example:

    pid = os.spawnlp(os.P_NOWAIT, "/bin/mycmd", "mycmd", "myarg")
    ==>
    pid = Popen(["/bin/mycmd", "myarg"]).pid

P_WAIT example:

    retcode = os.spawnlp(os.P_WAIT, "/bin/mycmd", "mycmd", "myarg")
    ==>
    retcode = call(["/bin/mycmd", "myarg"])

Vector example:

    os.spawnvp(os.P_NOWAIT, path, args)
    ==>
    Popen([path] + args[1:])

Environment example:

    os.spawnlpe(os.P_NOWAIT, "/bin/mycmd", "mycmd", "myarg", env)
    ==>
    Popen(["/bin/mycmd", "myarg"], env={"PATH": "/usr/bin"})

### Replacing `os.popen`{.interpreted-text role="func"}

Return code handling translates as follows:

    pipe = os.popen(cmd, 'w')
    ...
    rc = pipe.close()
    if rc is not None and rc >> 8:
        print("There were some errors")
    ==>
    process = Popen(cmd, stdin=PIPE)
    ...
    process.stdin.close()
    if process.wait() != 0:
        print("There were some errors")

## Legacy Shell Invocation Functions

This module also provides the following legacy functions from the 2.x `commands` module. These operations implicitly invoke the system shell and none of the guarantees described above regarding security and exception handling consistency are valid for these functions.

:::::: function
getstatusoutput(cmd, \*, encoding=None, errors=None)

Return `(exitcode, output)` of executing *cmd* in a shell.

Execute the string *cmd* in a shell with `check_output`{.interpreted-text role="func"} and return a 2-tuple `(exitcode, output)`. *encoding* and *errors* are used to decode output; see the notes on `frequently-used-arguments`{.interpreted-text role="ref"} for more details.

A trailing newline is stripped from the output. The exit code for the command can be interpreted as the return code of subprocess. Example:

    >>> subprocess.getstatusoutput('ls /bin/ls')
    (0, '/bin/ls')
    >>> subprocess.getstatusoutput('cat /bin/junk')
    (1, 'cat: /bin/junk: No such file or directory')
    >>> subprocess.getstatusoutput('/bin/junk')
    (127, 'sh: /bin/junk: not found')
    >>> subprocess.getstatusoutput('/bin/kill $$')
    (-15, '')

::: availability
Unix, Windows.
:::

::: versionchanged
3.3.4 Windows support was added.

The function now returns (exitcode, output) instead of (status, output) as it did in Python 3.3.3 and earlier. exitcode has the same value as `~Popen.returncode`{.interpreted-text role="attr"}.
:::

::: versionchanged
3.11 Added the *encoding* and *errors* parameters.
:::
::::::

:::::: function
getoutput(cmd, \*, encoding=None, errors=None)

Return output (stdout and stderr) of executing *cmd* in a shell.

Like `getstatusoutput`{.interpreted-text role="func"}, except the exit code is ignored and the return value is a string containing the command\'s output. Example:

    >>> subprocess.getoutput('ls /bin/ls')
    '/bin/ls'

::: availability
Unix, Windows.
:::

::: versionchanged
3.3.4 Windows support added
:::

::: versionchanged
3.11 Added the *encoding* and *errors* parameters.
:::
::::::

## Notes

### Timeout Behavior {#subprocess-timeout-behavior}

When using the `timeout` parameter in functions like `run`{.interpreted-text role="func"}, `Popen.wait`{.interpreted-text role="meth"}, or `Popen.communicate`{.interpreted-text role="meth"}, users should be aware of the following behaviors:

1.  **Process Creation Delay**: The initial process creation itself cannot be interrupted on many platform APIs. This means that even when specifying a timeout, you are not guaranteed to see a timeout exception until at least after however long process creation takes.
2.  **Extremely Small Timeout Values**: Setting very small timeout values (such as a few milliseconds) may result in almost immediate `TimeoutExpired`{.interpreted-text role="exc"} exceptions because process creation and system scheduling inherently require time.

### Converting an argument sequence to a string on Windows {#converting-argument-sequence}

On Windows, an *args* sequence is converted to a string that can be parsed using the following rules (which correspond to the rules used by the MS C runtime):

1.  Arguments are delimited by white space, which is either a space or a tab.
2.  A string surrounded by double quotation marks is interpreted as a single argument, regardless of white space contained within. A quoted string can be embedded in an argument.
3.  A double quotation mark preceded by a backslash is interpreted as a literal double quotation mark.
4.  Backslashes are interpreted literally, unless they immediately precede a double quotation mark.
5.  If backslashes immediately precede a double quotation mark, every pair of backslashes is interpreted as a literal backslash. If the number of backslashes is odd, the last backslash escapes the next double quotation mark as described in rule 3.

::: seealso

`shlex`{.interpreted-text role="mod"}

:   Module which provides function to parse and escape command lines.
:::

### Disable use of `posix_spawn()` {#disable_posix_spawn}

On Linux, `!subprocess`{.interpreted-text role="mod"} defaults to using the `vfork()` system call internally when it is safe to do so rather than `fork()`. This greatly improves performance.

    subprocess._USE_POSIX_SPAWN = False  # See CPython issue gh-NNNNNN.

It is safe to set this to false on any Python version. It will have no effect on older or newer versions where unsupported. Do not assume the attribute is available to read. Despite the name, a true value does not indicate the corresponding function will be used, only that it may be.

Please file issues any time you have to use these private knobs with a way to reproduce the issue you were seeing. Link to that issue from a comment in your code.

::: versionadded
3.8 `_USE_POSIX_SPAWN`
:::
