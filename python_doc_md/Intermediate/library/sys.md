# `!sys`{.interpreted-text role="mod"} \-\-- System-specific parameters and functions

::: {.module synopsis="Access system-specific parameters and functions."}
sys
:::

------------------------------------------------------------------------

This module provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter. It is always available. Unless explicitly noted otherwise, all variables are read-only.

:::::::: data
abi_info

::: versionadded
3.15
:::

An object containing information about the ABI of the currently running Python interpreter. It should include information that affect the CPython ABI in ways that require a specific build of the interpreter chosen from variants that can co-exist on a single machine. For example, it does not encode the base OS (Linux or Windows), but does include pointer size since some systems support both 32- and 64-bit builds. The available entries are the same on all platforms; e.g. *pointer_size* is available even on 64-bit-only architectures.

The following attributes are available:

::: attribute
abi_info.pointer_bits

The width of pointers in bits, as an integer, equivalent to `8 * sizeof(void *)`. Usually, this is `32` or `64`.
:::

::: attribute
abi_info.free_threaded

A Boolean indicating whether the interpreter was built with `free threading`{.interpreted-text role="term"} support. This reflects either the presence of the `--disable-gil`{.interpreted-text role="option"} `configure`{.interpreted-text role="file"} option (on Unix) or setting the `DisableGil` property (on Windows).
:::

::: attribute
abi_info.debug

A Boolean indicating whether the interpreter was built in `debug mode <debug-build>`{.interpreted-text role="ref"}. This reflects either the presence of the `--with-pydebug`{.interpreted-text role="option"} `configure`{.interpreted-text role="file"} option (on Unix) or the `Debug` configuration (on Windows).
:::

::: attribute
abi_info.byteorder

A string indicating the native byte order, either `'big'` or `'little'`. This is the same as the `byteorder`{.interpreted-text role="data"} attribute.
:::
::::::::

:::::: data
abiflags

On POSIX systems where Python was built with the standard `configure` script, this contains the ABI flags as specified by `3149`{.interpreted-text role="pep"}.

::: versionadded
3.2
:::

::: versionchanged
3.8 Default flags became an empty string (`m` flag for pymalloc has been removed).
:::

::: availability
Unix.
:::
::::::

::::::: function
addaudithook(hook)

Append the callable *hook* to the list of active auditing hooks for the current (sub)interpreter.

When an auditing event is raised through the `sys.audit`{.interpreted-text role="func"} function, each hook will be called in the order it was added with the event name and the tuple of arguments. Native hooks added by `PySys_AddAuditHook`{.interpreted-text role="c:func"} are called first, followed by hooks added in the current (sub)interpreter. Hooks can then log the event, raise an exception to abort the operation, or terminate the process entirely.

Note that audit hooks are primarily for collecting information about internal or otherwise unobservable actions, whether by Python or libraries written in Python. They are not suitable for implementing a \"sandbox\". In particular, malicious code can trivially disable or bypass hooks added using this function. At a minimum, any security-sensitive hooks must be added using the C API `PySys_AddAuditHook`{.interpreted-text role="c:func"} before initialising the runtime, and any modules allowing arbitrary memory modification (such as `ctypes`{.interpreted-text role="mod"}) should be completely removed or closely monitored.

::: audit-event
sys.addaudithook \"\" sys.addaudithook

Calling `sys.addaudithook`{.interpreted-text role="func"} will itself raise an auditing event named `sys.addaudithook` with no arguments. If any existing hooks raise an exception derived from `RuntimeError`{.interpreted-text role="class"}, the new hook will not be added and the exception suppressed. As a result, callers cannot assume that their hook has been added unless they control all existing hooks.
:::

See the `audit events table <audit-events>`{.interpreted-text role="ref"} for all events raised by CPython, and `578`{.interpreted-text role="pep"} for the original design discussion.

::: versionadded
3.8
:::

::: versionchanged
3.8.1

Exceptions derived from `Exception`{.interpreted-text role="class"} but not `RuntimeError`{.interpreted-text role="class"} are no longer suppressed.
:::

::: impl-detail
When tracing is enabled (see `settrace`{.interpreted-text role="func"}), Python hooks are only traced if the callable has a `__cantrace__` member that is set to a true value. Otherwise, trace functions will skip the hook.
:::
:::::::

::::: data
argv

The list of command line arguments passed to a Python script. `argv[0]` is the script name (it is operating system dependent whether this is a full pathname or not). If the command was executed using the `-c`{.interpreted-text role="option"} command line option to the interpreter, `argv[0]` is set to the string `'-c'`. If no script name was passed to the Python interpreter, `argv[0]` is the empty string.

To loop over the standard input, or the list of files given on the command line, see the `fileinput`{.interpreted-text role="mod"} module.

See also `sys.orig_argv`{.interpreted-text role="data"}.

:::: note
::: title
Note
:::

On Unix, command line arguments are passed by bytes from OS. Python decodes them with filesystem encoding and \"surrogateescape\" error handler. When you need original bytes, you can get it by `[os.fsencode(arg) for arg in sys.argv]`.
::::
:::::

:::::: {#auditing}
::::: function
audit(event, \*args)

::: index
single: auditing
:::

Raise an auditing event and trigger any active auditing hooks. *event* is a string identifying the event, and *args* may contain optional arguments with more information about the event. The number and types of arguments for a given event are considered a public and stable API and should not be modified between releases.

For example, one auditing event is named `os.chdir`. This event has one argument called *path* that will contain the requested new working directory.

`sys.audit`{.interpreted-text role="func"} will call the existing auditing hooks, passing the event name and arguments, and will re-raise the first exception from any hook. In general, if an exception is raised, it should not be handled and the process should be terminated as quickly as possible. This allows hook implementations to decide how to respond to particular events: they can merely log the event or abort the operation by raising an exception.

Hooks are added using the `sys.addaudithook`{.interpreted-text role="func"} or `PySys_AddAuditHook`{.interpreted-text role="c:func"} functions.

The native equivalent of this function is `PySys_Audit`{.interpreted-text role="c:func"}. Using the native function is preferred when possible.

See the `audit events table <audit-events>`{.interpreted-text role="ref"} for all events raised by CPython.

::: versionadded
3.8
:::
:::::
::::::

:::: data
base_exec_prefix

Equivalent to `exec_prefix`{.interpreted-text role="data"}, but referring to the base Python installation.

When running under `sys-path-init-virtual-environments`{.interpreted-text role="ref"}, `exec_prefix`{.interpreted-text role="data"} gets overwritten to the virtual environment prefix. `base_exec_prefix`{.interpreted-text role="data"}, conversely, does not change, and always points to the base Python installation. Refer to `sys-path-init-virtual-environments`{.interpreted-text role="ref"} for more information.

::: versionadded
3.3
:::
::::

:::: data
base_prefix

Equivalent to `prefix`{.interpreted-text role="data"}, but referring to the base Python installation.

When running under `virtual environment <venv-def>`{.interpreted-text role="ref"}, `prefix`{.interpreted-text role="data"} gets overwritten to the virtual environment prefix. `base_prefix`{.interpreted-text role="data"}, conversely, does not change, and always points to the base Python installation. Refer to `sys-path-init-virtual-environments`{.interpreted-text role="ref"} for more information.

::: versionadded
3.3
:::
::::

::: data
byteorder

An indicator of the native byte order. This will have the value `'big'` on big-endian (most-significant byte first) platforms, and `'little'` on little-endian (least-significant byte first) platforms.
:::

::: data
builtin_module_names

A tuple of strings containing the names of all modules that are compiled into this Python interpreter. (This information is not available in any other way \-\-- `modules.keys()` only lists the imported modules.)

See also the `sys.stdlib_module_names`{.interpreted-text role="data"} list.
:::

::: function
call_tracing(func, args)

Call `func(*args)`, while tracing is enabled. The tracing state is saved, and restored afterwards. This is intended to be called from a debugger from a checkpoint, to recursively debug or profile some other code.

Tracing is suspended while calling a tracing function set by `settrace`{.interpreted-text role="func"} or `setprofile`{.interpreted-text role="func"} to avoid infinite recursion. `!call_tracing`{.interpreted-text role="func"} enables explicit recursion of the tracing function.
:::

::: data
copyright

A string containing the copyright pertaining to the Python interpreter.
:::

:::: function
[clear_type_cache]{#clear_type_cache}()

Clear the internal type cache. The type cache is used to speed up attribute and method lookups. Use the function *only* to drop unnecessary references during reference leak debugging.

This function should be used for internal and specialized purposes only.

::: deprecated
3.13 Use the more general `_clear_internal_caches`{.interpreted-text role="func"} function instead.
:::
::::

:::: function
[clear_internal_caches]{#clear_internal_caches}()

Clear all internal performance-related caches. Use this function *only* to release unnecessary references and memory blocks when hunting for leaks.

::: versionadded
3.13
:::
::::

:::: function
[current_frames]{#current_frames}()

Return a dictionary mapping each thread\'s identifier to the topmost stack frame currently active in that thread at the time the function is called. Note that functions in the `traceback`{.interpreted-text role="mod"} module can build the call stack given such a frame.

This is most useful for debugging deadlock: this function does not require the deadlocked threads\' cooperation, and such threads\' call stacks are frozen for as long as they remain deadlocked. The frame returned for a non-deadlocked thread may bear no relationship to that thread\'s current activity by the time calling code examines the frame.

This function should be used for internal and specialized purposes only.

::: audit-event
sys.\_current_frames \"\" sys.\_current_frames
:::
::::

::::: function
[current_exceptions]{#current_exceptions}()

Return a dictionary mapping each thread\'s identifier to the topmost exception currently active in that thread at the time the function is called. If a thread is not currently handling an exception, it is not included in the result dictionary.

This is most useful for statistical profiling.

This function should be used for internal and specialized purposes only.

::: audit-event
sys.\_current_exceptions \"\" sys.\_current_exceptions
:::

::: versionchanged
3.12 Each value in the dictionary is now a single exception instance, rather than a 3-tuple as returned from `sys.exc_info()`.
:::
:::::

:::: function
breakpointhook()

This hook function is called by built-in `breakpoint`{.interpreted-text role="func"}. By default, it drops you into the `pdb`{.interpreted-text role="mod"} debugger, but it can be set to any other function so that you can choose which debugger gets used.

The signature of this function is dependent on what it calls. For example, the default binding (e.g. `pdb.set_trace()`) expects no arguments, but you might bind it to a function that expects additional arguments (positional and/or keyword). The built-in `breakpoint()` function passes its `*args` and `**kws` straight through. Whatever `breakpointhooks()` returns is returned from `breakpoint()`.

The default implementation first consults the environment variable `PYTHONBREAKPOINT`{.interpreted-text role="envvar"}. If that is set to `"0"` then this function returns immediately; i.e. it is a no-op. If the environment variable is not set, or is set to the empty string, `pdb.set_trace()` is called. Otherwise this variable should name a function to run, using Python\'s dotted-import nomenclature, e.g. `package.subpackage.module.function`. In this case, `package.subpackage.module` would be imported and the resulting module must have a callable named `function()`. This is run, passing in `*args` and `**kws`, and whatever `function()` returns, `sys.breakpointhook()` returns to the built-in `breakpoint`{.interpreted-text role="func"} function.

Note that if anything goes wrong while importing the callable named by `PYTHONBREAKPOINT`{.interpreted-text role="envvar"}, a `RuntimeWarning`{.interpreted-text role="exc"} is reported and the breakpoint is ignored.

Also note that if `sys.breakpointhook()` is overridden programmatically, `PYTHONBREAKPOINT`{.interpreted-text role="envvar"} is *not* consulted.

::: versionadded
3.7
:::
::::

::::: function
[debugmallocstats]{#debugmallocstats}()

Print low-level information to stderr about the state of CPython\'s memory allocator.

If Python is `built in debug mode <debug-build>`{.interpreted-text role="ref"} (`configure
--with-pydebug option <--with-pydebug>`{.interpreted-text role="option"}), it also performs some expensive internal consistency checks.

::: versionadded
3.3
:::

::: impl-detail
This function is specific to CPython. The exact output format is not defined here, and may change.
:::
:::::

:::: data
dllhandle

Integer specifying the handle of the Python DLL.

::: availability
Windows.
:::
::::

:::: function
displayhook(value)

If *value* is not `None`, this function prints `repr(value)` to `sys.stdout`, and saves *value* in `builtins._`. If `repr(value)` is not encodable to `sys.stdout.encoding` with `sys.stdout.errors` error handler (which is probably `'strict'`), encode it to `sys.stdout.encoding` with `'backslashreplace'` error handler.

`sys.displayhook` is called on the result of evaluating an `expression`{.interpreted-text role="term"} entered in an interactive Python session. The display of these values can be customized by assigning another one-argument function to `sys.displayhook`.

Pseudo-code:

    def displayhook(value):
        if value is None:
            return
        # Set '_' to None to avoid recursion
        builtins._ = None
        text = repr(value)
        try:
            sys.stdout.write(text)
        except UnicodeEncodeError:
            bytes = text.encode(sys.stdout.encoding, 'backslashreplace')
            if hasattr(sys.stdout, 'buffer'):
                sys.stdout.buffer.write(bytes)
            else:
                text = bytes.decode(sys.stdout.encoding, 'strict')
                sys.stdout.write(text)
        sys.stdout.write("\n")
        builtins._ = value

::: versionchanged
3.2 Use `'backslashreplace'` error handler on `UnicodeEncodeError`{.interpreted-text role="exc"}.
:::
::::

::: data
dont_write_bytecode

If this is true, Python won\'t try to write `.pyc` files on the import of source modules. This value is initially set to `True` or `False` depending on the `-B`{.interpreted-text role="option"} command line option and the `PYTHONDONTWRITEBYTECODE`{.interpreted-text role="envvar"} environment variable, but you can set it yourself to control bytecode file generation.
:::

::::::::: data
[emscripten_info]{#emscripten_info}

A `named tuple`{.interpreted-text role="term"} holding information about the environment on the *wasm32-emscripten* platform. The named tuple is provisional and may change in the future.

::: attribute
[emscripten_info.emscripten_version]{#emscripten_info.emscripten_version}

Emscripten version as tuple of ints (major, minor, micro), e.g. `(3, 1, 8)`.
:::

::: attribute
[emscripten_info.runtime]{#emscripten_info.runtime}

Runtime string, e.g. browser user agent, `'Node.js v14.18.2'`, or `'UNKNOWN'`.
:::

::: attribute
[emscripten_info.pthreads]{#emscripten_info.pthreads}

`True` if Python is compiled with Emscripten pthreads support.
:::

::: attribute
[emscripten_info.shared_memory]{#emscripten_info.shared_memory}

`True` if Python is compiled with shared memory support.
:::

::: availability
Emscripten.
:::

::: versionadded
3.11
:::
:::::::::

:::: data
pycache_prefix

If this is set (not `None`), Python will write bytecode-cache `.pyc` files to (and read them from) a parallel directory tree rooted at this directory, rather than from `__pycache__` directories in the source code tree. Any `__pycache__` directories in the source code tree will be ignored and new `.pyc` files written within the pycache prefix. Thus if you use `compileall`{.interpreted-text role="mod"} as a pre-build step, you must ensure you run it with the same pycache prefix (if any) that you will use at runtime.

A relative path is interpreted relative to the current working directory.

This value is initially set based on the value of the `-X`{.interpreted-text role="option"} `pycache_prefix=PATH` command-line option or the `PYTHONPYCACHEPREFIX`{.interpreted-text role="envvar"} environment variable (command-line takes precedence). If neither are set, it is `None`.

::: versionadded
3.8
:::
::::

::::: function
excepthook(type, value, traceback)

This function prints out a given traceback and exception to `sys.stderr`.

When an exception other than `SystemExit`{.interpreted-text role="exc"} is raised and uncaught, the interpreter calls `sys.excepthook` with three arguments, the exception class, exception instance, and a traceback object. In an interactive session this happens just before control is returned to the prompt; in a Python program this happens just before the program exits. The handling of such top-level exceptions can be customized by assigning another three-argument function to `sys.excepthook`.

::: audit-event
sys.excepthook hook,type,value,traceback sys.excepthook

Raise an auditing event `sys.excepthook` with arguments `hook`, `type`, `value`, `traceback` when an uncaught exception occurs. If no hook has been set, `hook` may be `None`. If any hook raises an exception derived from `RuntimeError`{.interpreted-text role="class"} the call to the hook will be suppressed. Otherwise, the audit hook exception will be reported as unraisable and `sys.excepthook` will be called.
:::

::: seealso
The `sys.unraisablehook`{.interpreted-text role="func"} function handles unraisable exceptions and the `threading.excepthook`{.interpreted-text role="func"} function handles exception raised by `threading.Thread.run`{.interpreted-text role="func"}.
:::
:::::

::::: data
\_\_breakpointhook\_\_ \_\_displayhook\_\_ \_\_excepthook\_\_ \_\_unraisablehook\_\_

These objects contain the original values of `breakpointhook`, `displayhook`, `excepthook`, and `unraisablehook` at the start of the program. They are saved so that `breakpointhook`, `displayhook` and `excepthook`, `unraisablehook` can be restored in case they happen to get replaced with broken or alternative objects.

::: versionadded
3.7 \_\_breakpointhook\_\_
:::

::: versionadded
3.8 \_\_unraisablehook\_\_
:::
:::::

:::: function
exception()

This function, when called while an exception handler is executing (such as an `except` or `except*` clause), returns the exception instance that was caught by this handler. When exception handlers are nested within one another, only the exception handled by the innermost handler is accessible.

If no exception handler is executing, this function returns `None`.

::: versionadded
3.11
:::
::::

::::: function
exc_info()

This function returns the old-style representation of the handled exception. If an exception `e` is currently handled (so `exception`{.interpreted-text role="func"} would return `e`), `exc_info`{.interpreted-text role="func"} returns the tuple `(type(e), e, e.__traceback__)`. That is, a tuple containing the type of the exception (a subclass of `BaseException`{.interpreted-text role="exc"}), the exception itself, and a `traceback
object <traceback-objects>`{.interpreted-text role="ref"} which typically encapsulates the call stack at the point where the exception last occurred.

::: index
pair: object; traceback
:::

If no exception is being handled anywhere on the stack, this function return a tuple containing three `None` values.

::: versionchanged
3.11 The `type` and `traceback` fields are now derived from the `value` (the exception instance), so when an exception is modified while it is being handled, the changes are reflected in the results of subsequent calls to `exc_info`{.interpreted-text role="func"}.
:::
:::::

:::::: data
exec_prefix

A string giving the site-specific directory prefix where the platform-dependent Python files are installed; by default, this is also `'/usr/local'`. This can be set at build time with the `--exec-prefix` argument to the `configure`{.interpreted-text role="program"} script. Specifically, all configuration files (e.g. the `pyconfig.h`{.interpreted-text role="file"} header file) are installed in the directory `{exec_prefix}/lib/python{X.Y}/config`{.interpreted-text role="file"}, and shared library modules are installed in `{exec_prefix}/lib/python{X.Y}/lib-dynload`{.interpreted-text role="file"}, where *X.Y* is the version number of Python, for example `3.2`.

:::: note
::: title
Note
:::

If a `virtual environment <venv-def>`{.interpreted-text role="ref"} is in effect, this `exec_prefix`{.interpreted-text role="data"} will point to the virtual environment. The value for the Python installation will still be available, via `base_exec_prefix`{.interpreted-text role="data"}. Refer to `sys-path-init-virtual-environments`{.interpreted-text role="ref"} for more information.
::::

::: versionchanged
3.14

When running under a `virtual environment <venv-def>`{.interpreted-text role="ref"}, `prefix`{.interpreted-text role="data"} and `exec_prefix`{.interpreted-text role="data"} are now set to the virtual environment prefix by the `path initialization <sys-path-init>`{.interpreted-text role="ref"}, instead of `site`{.interpreted-text role="mod"}. This means that `prefix`{.interpreted-text role="data"} and `exec_prefix`{.interpreted-text role="data"} always point to the virtual environment, even when `site`{.interpreted-text role="mod"} is disabled (`-S`{.interpreted-text role="option"}).
:::
::::::

::: data
executable

A string giving the absolute path of the executable binary for the Python interpreter, on systems where this makes sense. If Python is unable to retrieve the real path to its executable, `sys.executable`{.interpreted-text role="data"} will be an empty string or `None`.
:::

:::: function
exit(\[arg\])

Raise a `SystemExit`{.interpreted-text role="exc"} exception, signaling an intention to exit the interpreter.

The optional argument *arg* can be an integer giving the exit status (defaulting to zero), or another type of object. If it is an integer, zero is considered \"successful termination\" and any nonzero value is considered \"abnormal termination\" by shells and the like. Most systems require it to be in the range 0\--127, and produce undefined results otherwise. Some systems have a convention for assigning specific meanings to specific exit codes, but these are generally underdeveloped; Unix programs generally use 2 for command line syntax errors and 1 for all other kinds of errors. If another type of object is passed, `None` is equivalent to passing zero, and any other object is printed to `stderr`{.interpreted-text role="data"} and results in an exit code of 1. In particular, `sys.exit("some error message")` is a quick way to exit a program when an error occurs.

Since `exit`{.interpreted-text role="func"} ultimately \"only\" raises an exception, it will only exit the process when called from the main thread, and the exception is not intercepted. Cleanup actions specified by `finally`{.interpreted-text role="keyword"} clauses of `try`{.interpreted-text role="keyword"} statements are honored, and it is possible to intercept the exit attempt at an outer level.

::: versionchanged
3.6 If an error occurs in the cleanup after the Python interpreter has caught `SystemExit`{.interpreted-text role="exc"} (such as an error flushing buffered data in the standard streams), the exit status is changed to 120.
:::
::::

:::::::::::::: data
flags

The `named tuple`{.interpreted-text role="term"} *flags* exposes the status of command line flags. Flags should only be accessed only by name and not by index. The attributes are read only.

+------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                | `-d`{.interpreted-text role="option"}                                                                                                                            |
| flags.debug                  |                                                                                                                                                                  |
| :::                          |                                                                                                                                                                  |
+------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                | `-i`{.interpreted-text role="option"}                                                                                                                            |
| flags.inspect                |                                                                                                                                                                  |
| :::                          |                                                                                                                                                                  |
+------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                | `-i`{.interpreted-text role="option"}                                                                                                                            |
| flags.interactive            |                                                                                                                                                                  |
| :::                          |                                                                                                                                                                  |
+------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                | `-I`{.interpreted-text role="option"}                                                                                                                            |
| flags.isolated               |                                                                                                                                                                  |
| :::                          |                                                                                                                                                                  |
+------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                | `-O`{.interpreted-text role="option"} or `-OO`{.interpreted-text role="option"}                                                                                  |
| flags.optimize               |                                                                                                                                                                  |
| :::                          |                                                                                                                                                                  |
+------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                | `-B`{.interpreted-text role="option"}                                                                                                                            |
| flags.dont_write_bytecode    |                                                                                                                                                                  |
| :::                          |                                                                                                                                                                  |
+------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                | `-s`{.interpreted-text role="option"}                                                                                                                            |
| flags.no_user_site           |                                                                                                                                                                  |
| :::                          |                                                                                                                                                                  |
+------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                | `-S`{.interpreted-text role="option"}                                                                                                                            |
| flags.no_site                |                                                                                                                                                                  |
| :::                          |                                                                                                                                                                  |
+------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                | `-E`{.interpreted-text role="option"}                                                                                                                            |
| flags.ignore_environment     |                                                                                                                                                                  |
| :::                          |                                                                                                                                                                  |
+------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                | `-v`{.interpreted-text role="option"}                                                                                                                            |
| flags.verbose                |                                                                                                                                                                  |
| :::                          |                                                                                                                                                                  |
+------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                | `-b`{.interpreted-text role="option"}                                                                                                                            |
| flags.bytes_warning          |                                                                                                                                                                  |
| :::                          |                                                                                                                                                                  |
+------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                | `-q`{.interpreted-text role="option"}                                                                                                                            |
| flags.quiet                  |                                                                                                                                                                  |
| :::                          |                                                                                                                                                                  |
+------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                | `-R`{.interpreted-text role="option"}                                                                                                                            |
| flags.hash_randomization     |                                                                                                                                                                  |
| :::                          |                                                                                                                                                                  |
+------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                | `-X dev <-X>`{.interpreted-text role="option"} (`Python Development Mode <devmode>`{.interpreted-text role="ref"})                                               |
| flags.dev_mode               |                                                                                                                                                                  |
| :::                          |                                                                                                                                                                  |
+------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                | `-X utf8 <-X>`{.interpreted-text role="option"}                                                                                                                  |
| flags.utf8_mode              |                                                                                                                                                                  |
| :::                          |                                                                                                                                                                  |
+------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                | `-P`{.interpreted-text role="option"}                                                                                                                            |
| flags.safe_path              |                                                                                                                                                                  |
| :::                          |                                                                                                                                                                  |
+------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                | `-X int_max_str_digits <-X>`{.interpreted-text role="option"} (`integer string conversion length limitation <int_max_str_digits>`{.interpreted-text role="ref"}) |
| flags.int_max_str_digits     |                                                                                                                                                                  |
| :::                          |                                                                                                                                                                  |
+------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                | `-X warn_default_encoding <-X>`{.interpreted-text role="option"}                                                                                                 |
| flags.warn_default_encoding  |                                                                                                                                                                  |
| :::                          |                                                                                                                                                                  |
+------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                | `-X gil <-X>`{.interpreted-text role="option"} and `PYTHON_GIL`{.interpreted-text role="envvar"}                                                                 |
| flags.gil                    |                                                                                                                                                                  |
| :::                          |                                                                                                                                                                  |
+------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                | `-X thread_inherit_context <-X>`{.interpreted-text role="option"} and `PYTHON_THREAD_INHERIT_CONTEXT`{.interpreted-text role="envvar"}                           |
| flags.thread_inherit_context |                                                                                                                                                                  |
| :::                          |                                                                                                                                                                  |
+------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute                | `-X context_aware_warnings <-X>`{.interpreted-text role="option"} and `PYTHON_CONTEXT_AWARE_WARNINGS`{.interpreted-text role="envvar"}                           |
| flags.context_aware_warnings |                                                                                                                                                                  |
| :::                          |                                                                                                                                                                  |
+------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+

::: versionchanged
3.2 Added `quiet` attribute for the new `-q`{.interpreted-text role="option"} flag.
:::

::: versionadded
3.2.3 The `hash_randomization` attribute.
:::

::: versionchanged
3.3 Removed obsolete `division_warning` attribute.
:::

::: versionchanged
3.4 Added `isolated` attribute for `-I`{.interpreted-text role="option"} `isolated` flag.
:::

::: versionchanged
3.7 Added the `dev_mode` attribute for the new `Python Development
Mode <devmode>`{.interpreted-text role="ref"} and the `utf8_mode` attribute for the new `-X`{.interpreted-text role="option"} `utf8` flag.
:::

::: versionchanged
3.10 Added `warn_default_encoding` attribute for `-X`{.interpreted-text role="option"} `warn_default_encoding` flag.
:::

::: versionchanged
3.11 Added the `safe_path` attribute for `-P`{.interpreted-text role="option"} option.
:::

::: versionchanged
3.11 Added the `int_max_str_digits` attribute.
:::

::: versionchanged
3.13 Added the `gil` attribute.
:::

::: versionchanged
3.14 Added the `thread_inherit_context` attribute.
:::

::: versionchanged
3.14 Added the `context_aware_warnings` attribute.
:::
::::::::::::::

::: data
float_info

A `named tuple`{.interpreted-text role="term"} holding information about the float type. It contains low level information about the precision and internal representation. The values correspond to the various floating-point constants defined in the standard header file `float.h`{.interpreted-text role="file"} for the \'C\' programming language; see section 5.2.4.2.2 of the 1999 ISO/IEC C standard [\[C99\]](#C99){.citation}, \'Characteristics of floating types\', for details.

+-----------------------+-----------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| attribute             | float.h macro                                       | explanation                                                                                                                                                                                       |
+=======================+=====================================================+===================================================================================================================================================================================================+
| ::: attribute         | `!DBL_EPSILON`{.interpreted-text role="c:macro"}    | difference between 1.0 and the least value greater than 1.0 that is representable as a float.                                                                                                     |
| float_info.epsilon    |                                                     |                                                                                                                                                                                                   |
| :::                   |                                                     | See also `math.ulp`{.interpreted-text role="func"}.                                                                                                                                               |
+-----------------------+-----------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute         | `!DBL_DIG`{.interpreted-text role="c:macro"}        | The maximum number of decimal digits that can be faithfully represented in a float; see below.                                                                                                    |
| float_info.dig        |                                                     |                                                                                                                                                                                                   |
| :::                   |                                                     |                                                                                                                                                                                                   |
+-----------------------+-----------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute         | `!DBL_MANT_DIG`{.interpreted-text role="c:macro"}   | Float precision: the number of base-`radix` digits in the significand of a float.                                                                                                                 |
| float_info.mant_dig   |                                                     |                                                                                                                                                                                                   |
| :::                   |                                                     |                                                                                                                                                                                                   |
+-----------------------+-----------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute         | `!DBL_MAX`{.interpreted-text role="c:macro"}        | The maximum representable positive finite float.                                                                                                                                                  |
| float_info.max        |                                                     |                                                                                                                                                                                                   |
| :::                   |                                                     |                                                                                                                                                                                                   |
+-----------------------+-----------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute         | `!DBL_MAX_EXP`{.interpreted-text role="c:macro"}    | The maximum integer *e* such that `radix**(e-1)` is a representable finite float.                                                                                                                 |
| float_info.max_exp    |                                                     |                                                                                                                                                                                                   |
| :::                   |                                                     |                                                                                                                                                                                                   |
+-----------------------+-----------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute         | `!DBL_MAX_10_EXP`{.interpreted-text role="c:macro"} | The maximum integer *e* such that `10**e` is in the range of representable finite floats.                                                                                                         |
| float_info.max_10_exp |                                                     |                                                                                                                                                                                                   |
| :::                   |                                                     |                                                                                                                                                                                                   |
+-----------------------+-----------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute         | `!DBL_MIN`{.interpreted-text role="c:macro"}        | The minimum representable positive *normalized* float.                                                                                                                                            |
| float_info.min        |                                                     |                                                                                                                                                                                                   |
| :::                   |                                                     | Use `math.ulp(0.0) <math.ulp>`{.interpreted-text role="func"} to get the smallest positive *denormalized* representable float.                                                                    |
+-----------------------+-----------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute         | `!DBL_MIN_EXP`{.interpreted-text role="c:macro"}    | The minimum integer *e* such that `radix**(e-1)` is a normalized float.                                                                                                                           |
| float_info.min_exp    |                                                     |                                                                                                                                                                                                   |
| :::                   |                                                     |                                                                                                                                                                                                   |
+-----------------------+-----------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute         | `!DBL_MIN_10_EXP`{.interpreted-text role="c:macro"} | The minimum integer *e* such that `10**e` is a normalized float.                                                                                                                                  |
| float_info.min_10_exp |                                                     |                                                                                                                                                                                                   |
| :::                   |                                                     |                                                                                                                                                                                                   |
+-----------------------+-----------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute         | `!FLT_RADIX`{.interpreted-text role="c:macro"}      | The radix of exponent representation.                                                                                                                                                             |
| float_info.radix      |                                                     |                                                                                                                                                                                                   |
| :::                   |                                                     |                                                                                                                                                                                                   |
+-----------------------+-----------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ::: attribute         | `!FLT_ROUNDS`{.interpreted-text role="c:macro"}     | An integer representing the rounding mode for floating-point arithmetic. This reflects the value of the system `!FLT_ROUNDS`{.interpreted-text role="c:macro"} macro at interpreter startup time: |
| float_info.rounds     |                                                     |                                                                                                                                                                                                   |
| :::                   |                                                     | - `-1`: indeterminable                                                                                                                                                                            |
|                       |                                                     | - `0`: toward zero                                                                                                                                                                                |
|                       |                                                     | - `1`: to nearest                                                                                                                                                                                 |
|                       |                                                     | - `2`: toward positive infinity                                                                                                                                                                   |
|                       |                                                     | - `3`: toward negative infinity                                                                                                                                                                   |
|                       |                                                     |                                                                                                                                                                                                   |
|                       |                                                     | All other values for `!FLT_ROUNDS`{.interpreted-text role="c:macro"} characterize implementation-defined rounding behavior.                                                                       |
+-----------------------+-----------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

: Attributes of the `!float_info`{.interpreted-text role="data"} `named tuple`{.interpreted-text role="term"}

The attribute `sys.float_info.dig`{.interpreted-text role="attr"} needs further explanation. If `s` is any string representing a decimal number with at most `!sys.float_info.dig`{.interpreted-text role="attr"} significant digits, then converting `s` to a float and back again will recover a string representing the same decimal value:

    >>> import sys
    >>> sys.float_info.dig
    15
    >>> s = '3.14159265358979'    # decimal string with 15 significant digits
    >>> format(float(s), '.15g')  # convert to float and back -> same value
    '3.14159265358979'

But for strings with more than `sys.float_info.dig`{.interpreted-text role="attr"} significant digits, this isn\'t always true:

    >>> s = '9876543211234567'    # 16 significant digits is too many!
    >>> format(float(s), '.16g')  # conversion changes value
    '9876543211234568'
:::

:::: data
float_repr_style

A string indicating how the `repr`{.interpreted-text role="func"} function behaves for floats. If the string has value `'short'` then for a finite float `x`, `repr(x)` aims to produce a short string with the property that `float(repr(x)) == x`. This is the usual behaviour in Python 3.1 and later. Otherwise, `float_repr_style` has value `'legacy'` and `repr(x)` behaves in the same way as it did in versions of Python prior to 3.1.

::: versionadded
3.1
:::
::::

:::: function
getallocatedblocks()

Return the number of memory blocks currently allocated by the interpreter, regardless of their size. This function is mainly useful for tracking and debugging memory leaks. Because of the interpreter\'s internal caches, the result can vary from call to call; you may have to call `_clear_internal_caches`{.interpreted-text role="func"} and `gc.collect`{.interpreted-text role="func"} to get more predictable results.

If a Python build or implementation cannot reasonably compute this information, `getallocatedblocks`{.interpreted-text role="func"} is allowed to return 0 instead.

::: versionadded
3.4
:::
::::

:::: function
getunicodeinternedsize()

Return the number of unicode objects that have been interned.

::: versionadded
3.12
:::
::::

::::: function
getandroidapilevel()

Return the build-time API level of Android as an integer. This represents the minimum version of Android this build of Python can run on. For runtime version information, see `platform.android_ver`{.interpreted-text role="func"}.

::: availability
Android.
:::

::: versionadded
3.7
:::
:::::

::: function
getdefaultencoding()

Return `'utf-8'`. This is the name of the default string encoding, used in methods like `str.encode`{.interpreted-text role="meth"}.
:::

:::: function
getdlopenflags()

Return the current value of the flags that are used for `dlopen`{.interpreted-text role="c:func"} calls. Symbolic names for the flag values can be found in the `os`{.interpreted-text role="mod"} module (`RTLD_{xxx}`{.interpreted-text role="samp"} constants, e.g. `os.RTLD_LAZY`{.interpreted-text role="const"}).

::: availability
Unix.
:::
::::

:::::: function
getfilesystemencoding()

Get the `filesystem encoding <filesystem encoding and error handler>`{.interpreted-text role="term"}: the encoding used with the `filesystem error handler <filesystem
encoding and error handler>`{.interpreted-text role="term"} to convert between Unicode filenames and bytes filenames. The filesystem error handler is returned from `getfilesystemencodeerrors`{.interpreted-text role="func"}.

For best compatibility, str should be used for filenames in all cases, although representing filenames as bytes is also supported. Functions accepting or returning filenames should support either str or bytes and internally convert to the system\'s preferred representation.

`os.fsencode`{.interpreted-text role="func"} and `os.fsdecode`{.interpreted-text role="func"} should be used to ensure that the correct encoding and errors mode are used.

The `filesystem encoding and error handler`{.interpreted-text role="term"} are configured at Python startup by the `PyConfig_Read`{.interpreted-text role="c:func"} function: see `~PyConfig.filesystem_encoding`{.interpreted-text role="c:member"} and `~PyConfig.filesystem_errors`{.interpreted-text role="c:member"} members of `PyConfig`{.interpreted-text role="c:type"}.

::: versionchanged
3.2 `getfilesystemencoding`{.interpreted-text role="func"} result cannot be `None` anymore.
:::

::: versionchanged
3.6 Windows is no longer guaranteed to return `'mbcs'`. See `529`{.interpreted-text role="pep"} and `_enablelegacywindowsfsencoding`{.interpreted-text role="func"} for more information.
:::

::: versionchanged
3.7 Return `'utf-8'` if the `Python UTF-8 Mode <utf8-mode>`{.interpreted-text role="ref"} is enabled.
:::
::::::

:::: function
getfilesystemencodeerrors()

Get the `filesystem error handler <filesystem encoding and error
handler>`{.interpreted-text role="term"}: the error handler used with the `filesystem encoding
<filesystem encoding and error handler>`{.interpreted-text role="term"} to convert between Unicode filenames and bytes filenames. The filesystem encoding is returned from `getfilesystemencoding`{.interpreted-text role="func"}.

`os.fsencode`{.interpreted-text role="func"} and `os.fsdecode`{.interpreted-text role="func"} should be used to ensure that the correct encoding and errors mode are used.

The `filesystem encoding and error handler`{.interpreted-text role="term"} are configured at Python startup by the `PyConfig_Read`{.interpreted-text role="c:func"} function: see `~PyConfig.filesystem_encoding`{.interpreted-text role="c:member"} and `~PyConfig.filesystem_errors`{.interpreted-text role="c:member"} members of `PyConfig`{.interpreted-text role="c:type"}.

::: versionadded
3.6
:::
::::

:::: function
get_int_max_str_digits()

Returns the current value for the `integer string conversion length
limitation <int_max_str_digits>`{.interpreted-text role="ref"}. See also `set_int_max_str_digits`{.interpreted-text role="func"}.

::: versionadded
3.11
:::
::::

:::: function
get_lazy_imports()

Returns the current lazy imports mode as a string.

- `"normal"`: Only imports explicitly marked with the `lazy` keyword are lazy
- `"all"`: All top-level imports are potentially lazy
- `"none"`: All lazy imports are suppressed (even explicitly marked ones)

See also `set_lazy_imports`{.interpreted-text role="func"} and `810`{.interpreted-text role="pep"}.

::: versionadded
next
:::
::::

:::: function
get_lazy_imports_filter()

Returns the current lazy imports filter function, or `None` if no filter is set.

The filter function is called for every potentially lazy import to determine whether it should actually be lazy. See `set_lazy_imports_filter`{.interpreted-text role="func"} for details on the filter function signature.

::: versionadded
next
:::
::::

::::: function
getrefcount(object)

Return the reference count of the *object*. The count returned is generally one higher than you might expect, because it includes the (temporary) reference as an argument to `getrefcount`{.interpreted-text role="func"}.

Note that the returned value may not actually reflect how many references to the object are actually held. For example, some objects are `immortal`{.interpreted-text role="term"} and have a very high refcount that does not reflect the actual number of references. Consequently, do not rely on the returned value to be accurate, other than a value of 0 or 1.

::: impl-detail
`Immortal <immortal>`{.interpreted-text role="term"} objects with a large reference count can be identified via `_is_immortal`{.interpreted-text role="func"}.
:::

::: versionchanged
3.12 Immortal objects have very large refcounts that do not match the actual number of references to the object.
:::
:::::

::: function
getrecursionlimit()

Return the current value of the recursion limit, the maximum depth of the Python interpreter stack. This limit prevents infinite recursion from causing an overflow of the C stack and crashing Python. It can be set by `setrecursionlimit`{.interpreted-text role="func"}.
:::

::: function
getsizeof(object\[, default\])

Return the size of an object in bytes. The object can be any type of object. All built-in objects will return correct results, but this does not have to hold true for third-party extensions as it is implementation specific.

Only the memory consumption directly attributed to the object is accounted for, not the memory consumption of objects it refers to.

If given, *default* will be returned if the object does not provide means to retrieve the size. Otherwise a `TypeError`{.interpreted-text role="exc"} will be raised.

`getsizeof`{.interpreted-text role="func"} calls the object\'s `__sizeof__` method and adds an additional garbage collector overhead if the object is managed by the garbage collector.

See [recursive sizeof recipe](https://code.activestate.com/recipes/577504-compute-memory-footprint-of-an-object-and-its-cont/) for an example of using `getsizeof`{.interpreted-text role="func"} recursively to find the size of containers and all their contents.
:::

:::: function
getswitchinterval()

Return the interpreter\'s \"thread switch interval\" in seconds; see `setswitchinterval`{.interpreted-text role="func"}.

::: versionadded
3.2
:::
::::

::::: function
[getframe]{#getframe}(\[depth\])

Return a frame object from the call stack. If optional integer *depth* is given, return the frame object that many calls below the top of the stack. If that is deeper than the call stack, `ValueError`{.interpreted-text role="exc"} is raised. The default for *depth* is zero, returning the frame at the top of the call stack.

::: audit-event
sys.\_getframe frame sys.\_getframe
:::

::: impl-detail
This function should be used for internal and specialized purposes only. It is not guaranteed to exist in all implementations of Python.
:::
:::::

:::::: function
[getframemodulename]{#getframemodulename}(\[depth\])

Return the name of a module from the call stack. If optional integer *depth* is given, return the module that many calls below the top of the stack. If that is deeper than the call stack, or if the module is unidentifiable, `None` is returned. The default for *depth* is zero, returning the module at the top of the call stack.

::: audit-event
sys.\_getframemodulename depth sys.\_getframemodulename
:::

::: impl-detail
This function should be used for internal and specialized purposes only. It is not guaranteed to exist in all implementations of Python.
:::

::: versionadded
3.12
:::
::::::

::::: function
getobjects(limit\[, type\])

This function only exists if CPython was built using the specialized configure option `--with-trace-refs`{.interpreted-text role="option"}. It is intended only for debugging garbage-collection issues.

Return a list of up to *limit* dynamically allocated Python objects. If *type* is given, only objects of that exact type (not subtypes) are included.

Objects from the list are not safe to use. Specifically, the result will include objects from all interpreters that share their object allocator state (that is, ones created with `PyInterpreterConfig.use_main_obmalloc`{.interpreted-text role="c:member"} set to 1 or using `Py_NewInterpreter`{.interpreted-text role="c:func"}, and the `main interpreter <sub-interpreter-support>`{.interpreted-text role="ref"}). Mixing objects from different interpreters may lead to crashes or other unexpected behavior.

::: impl-detail
This function should be used for specialized purposes only. It is not guaranteed to exist in all implementations of Python.
:::

::: versionchanged
3.14

The result may include objects from other interpreters.
:::
:::::

:::: function
getprofile()

::: index
single: profile function single: profiler
:::

Get the profiler function as set by `setprofile`{.interpreted-text role="func"}.
::::

::::: function
gettrace()

::: index
single: trace function single: debugger
:::

Get the trace function as set by `settrace`{.interpreted-text role="func"}.

::: impl-detail
The `gettrace`{.interpreted-text role="func"} function is intended only for implementing debuggers, profilers, coverage tools and the like. Its behavior is part of the implementation platform, rather than part of the language definition, and thus may not be available in all Python implementations.
:::
:::::

:::::::: function
getwindowsversion()

Return a named tuple describing the Windows version currently running. The named elements are *major*, *minor*, *build*, *platform*, *service_pack*, *service_pack_minor*, *service_pack_major*, *suite_mask*, *product_type* and *platform_version*. *service_pack* contains a string, *platform_version* a 3-tuple and all other values are integers. The components can also be accessed by name, so `sys.getwindowsversion()[0]` is equivalent to `sys.getwindowsversion().major`. For compatibility with prior versions, only the first 5 elements are retrievable by indexing.

*platform* will be `2` (VER_PLATFORM_WIN32_NT).

*product_type* may be one of the following values:

  ---------------------------------------------------------------------------------------------
  Constant                               Meaning
  -------------------------------------- ------------------------------------------------------
  `1` (VER_NT_WORKSTATION)               The system is a workstation.

  `2` (VER_NT_DOMAIN_CONTROLLER)         The system is a domain controller.

  `3` (VER_NT_SERVER)                    The system is a server, but not a domain controller.
  ---------------------------------------------------------------------------------------------

This function wraps the Win32 `!GetVersionEx`{.interpreted-text role="c:func"} function; see the Microsoft documentation on `!OSVERSIONINFOEX`{.interpreted-text role="c:func"} for more information about these fields.

*platform_version* returns the major version, minor version and build number of the current operating system, rather than the version that is being emulated for the process. It is intended for use in logging rather than for feature detection.

:::: note
::: title
Note
:::

*platform_version* derives the version from kernel32.dll which can be of a different version than the OS version. Please use `platform`{.interpreted-text role="mod"} module for achieving accurate OS version.
::::

::: availability
Windows.
:::

::: versionchanged
3.2 Changed to a named tuple and added *service_pack_minor*, *service_pack_major*, *suite_mask*, and *product_type*.
:::

::: versionchanged
3.6 Added *platform_version*
:::
::::::::

:::::: function
get_asyncgen_hooks()

Returns an *asyncgen_hooks* object, which is similar to a `~collections.namedtuple`{.interpreted-text role="class"} of the form `(firstiter, finalizer)`, where *firstiter* and *finalizer* are expected to be either `None` or functions which take an `asynchronous generator iterator`{.interpreted-text role="term"} as an argument, and are used to schedule finalization of an asynchronous generator by an event loop.

::: versionadded
3.6 See `525`{.interpreted-text role="pep"} for more details.
:::

:::: note
::: title
Note
:::

This function has been added on a provisional basis (see `411`{.interpreted-text role="pep"} for details.)
::::
::::::

:::::: function
get_coroutine_origin_tracking_depth()

Get the current coroutine origin tracking depth, as set by `set_coroutine_origin_tracking_depth`{.interpreted-text role="func"}.

::: versionadded
3.7
:::

:::: note
::: title
Note
:::

This function has been added on a provisional basis (see `411`{.interpreted-text role="pep"} for details.) Use it only for debugging purposes.
::::
::::::

:::::::::::::: data
hash_info

A `named tuple`{.interpreted-text role="term"} giving parameters of the numeric hash implementation. For more details about hashing of numeric types, see `numeric-hash`{.interpreted-text role="ref"}.

::: attribute
hash_info.width

The width in bits used for hash values
:::

::: attribute
hash_info.modulus

The prime modulus P used for numeric hash scheme
:::

::: attribute
hash_info.inf

The hash value returned for a positive infinity
:::

::: attribute
hash_info.nan

(This attribute is no longer used)
:::

::: attribute
hash_info.imag

The multiplier used for the imaginary part of a complex number
:::

::: attribute
hash_info.algorithm

The name of the algorithm for hashing of str, bytes, and memoryview
:::

::: attribute
hash_info.hash_bits

The internal output size of the hash algorithm
:::

::: attribute
hash_info.seed_bits

The size of the seed key of the hash algorithm
:::

::: attribute
hash_info.cutoff

Cutoff for small string DJBX33A optimization in range `[1, cutoff)`.
:::

::: versionadded
3.2
:::

::: versionchanged
3.4 Added *algorithm*, *hash_bits*, *seed_bits*, and *cutoff*.
:::
::::::::::::::

::: data
hexversion

The version number encoded as a single integer. This is guaranteed to increase with each version, including proper support for non-production releases. For example, to test that the Python interpreter is at least version 1.5.2, use:

    if sys.hexversion >= 0x010502F0:
        # use some advanced feature
        ...
    else:
        # use an alternative implementation or warn the user
        ...

This is called `hexversion` since it only really looks meaningful when viewed as the result of passing it to the built-in `hex`{.interpreted-text role="func"} function. The `named tuple`{.interpreted-text role="term"} `sys.version_info`{.interpreted-text role="data"} may be used for a more human-friendly encoding of the same information.

More details of `hexversion` can be found at `apiabiversion`{.interpreted-text role="ref"}.
:::

:::::::: data
implementation

An object containing information about the implementation of the currently running Python interpreter. The following attributes are required to exist in all Python implementations.

*name* is the implementation\'s identifier, e.g. `'cpython'`. The actual string is defined by the Python implementation, but it is guaranteed to be lower case.

*version* is a named tuple, in the same format as `sys.version_info`{.interpreted-text role="data"}. It represents the version of the Python *implementation*. This has a distinct meaning from the specific version of the Python *language* to which the currently running interpreter conforms, which `sys.version_info` represents. For example, for PyPy 1.8 `sys.implementation.version` might be `sys.version_info(1, 8, 0, 'final', 0)`, whereas `sys.version_info` would be `sys.version_info(2, 7, 2, 'final', 0)`. For CPython they are the same value, since it is the reference implementation.

*hexversion* is the implementation version in hexadecimal format, like `sys.hexversion`{.interpreted-text role="data"}.

*cache_tag* is the tag used by the import machinery in the filenames of cached modules. By convention, it would be a composite of the implementation\'s name and version, like `'cpython-33'`. However, a Python implementation may use some other value if appropriate. If `cache_tag` is set to `None`, it indicates that module caching should be disabled.

*supports_isolated_interpreters* is a boolean value, whether this implementation supports multiple isolated interpreters. It is `True` for CPython on most platforms. Platforms with this support implement the low-level `!_interpreters`{.interpreted-text role="mod"} module.

::: seealso
`684`{.interpreted-text role="pep"}, `734`{.interpreted-text role="pep"}, and `concurrent.interpreters`{.interpreted-text role="mod"}.
:::

`sys.implementation`{.interpreted-text role="data"} may contain additional attributes specific to the Python implementation. These non-standard attributes must start with an underscore, and are not described here. Regardless of its contents, `sys.implementation`{.interpreted-text role="data"} will not change during a run of the interpreter, nor between implementation versions. (It may change between Python language versions, however.) See `421`{.interpreted-text role="pep"} for more information.

::: versionadded
3.3
:::

::: versionchanged
3.14 Added `supports_isolated_interpreters` field.
:::

:::: note
::: title
Note
:::

The addition of new required attributes must go through the normal PEP process. See `421`{.interpreted-text role="pep"} for more information.
::::
::::::::

::::::::: data
int_info

A `named tuple`{.interpreted-text role="term"} that holds information about Python\'s internal representation of integers. The attributes are read only.

::: attribute
int_info.bits_per_digit

The number of bits held in each digit. Python integers are stored internally in base `2**int_info.bits_per_digit`.
:::

::: attribute
int_info.sizeof_digit

The size in bytes of the C type used to represent a digit.
:::

::: attribute
int_info.default_max_str_digits

The default value for `sys.get_int_max_str_digits`{.interpreted-text role="func"} when it is not otherwise explicitly configured.
:::

::: attribute
int_info.str_digits_check_threshold

The minimum non-zero value for `sys.set_int_max_str_digits`{.interpreted-text role="func"}, `PYTHONINTMAXSTRDIGITS`{.interpreted-text role="envvar"}, or `-X int_max_str_digits <-X>`{.interpreted-text role="option"}.
:::

::: versionadded
3.1
:::

::: versionchanged
3.11

Added `~int_info.default_max_str_digits`{.interpreted-text role="attr"} and `~int_info.str_digits_check_threshold`{.interpreted-text role="attr"}.
:::
:::::::::

::::: data
\_\_interactivehook\_\_

When this attribute exists, its value is automatically called (with no arguments) when the interpreter is launched in `interactive mode
<tut-interactive>`{.interpreted-text role="ref"}. This is done after the `PYTHONSTARTUP`{.interpreted-text role="envvar"} file is read, so that you can set this hook there. The `site`{.interpreted-text role="mod"} module `sets this <rlcompleter-config>`{.interpreted-text role="ref"}.

::: audit-event
cpython.run_interactivehook hook sys.\_\_interactivehook\_\_

Raises an `auditing event <auditing>`{.interpreted-text role="ref"} `cpython.run_interactivehook` with the hook object as the argument when the hook is called on startup.
:::

::: versionadded
3.4
:::
:::::

::: function
intern(string)

Enter *string* in the table of \"interned\" strings and return the interned string \-- which is *string* itself or a copy. Interning strings is useful to gain a little performance on dictionary lookup \-- if the keys in a dictionary are interned, and the lookup key is interned, the key comparisons (after hashing) can be done by a pointer compare instead of a string compare. Normally, the names used in Python programs are automatically interned, and the dictionaries used to hold module, class or instance attributes have interned keys.

Interned strings are not `immortal`{.interpreted-text role="term"}; you must keep a reference to the return value of `intern`{.interpreted-text role="func"} around to benefit from it.
:::

::::: function
[is_gil_enabled]{#is_gil_enabled}()

Return `True`{.interpreted-text role="const"} if the `GIL`{.interpreted-text role="term"} is enabled and `False`{.interpreted-text role="const"} if it is disabled.

::: versionadded
3.13
:::

::: impl-detail
It is not guaranteed to exist in all implementations of Python.
:::
:::::

:::: function
is_finalizing()

Return `True`{.interpreted-text role="const"} if the main Python interpreter is `shutting down <interpreter shutdown>`{.interpreted-text role="term"}. Return `False`{.interpreted-text role="const"} otherwise.

See also the `PythonFinalizationError`{.interpreted-text role="exc"} exception.

::: versionadded
3.5
:::
::::

:::::::::::: data
[jit]{#jit}

Utilities for observing just-in-time compilation.

::: impl-detail
JIT compilation is an *experimental implementation detail* of CPython. `sys._jit` is not guaranteed to exist or behave the same way in all Python implementations, versions, or build configurations.
:::

::: versionadded
3.14
:::

::: function
[jit.is_available]{#jit.is_available}()

Return `True` if the current Python executable supports JIT compilation, and `False` otherwise. This can be controlled by building CPython with the `--experimental-jit` option on Windows, and the `--enable-experimental-jit`{.interpreted-text role="option"} option on all other platforms.
:::

::: function
[jit.is_enabled]{#jit.is_enabled}()

Return `True` if JIT compilation is enabled for the current Python process (implies `sys._jit.is_available`{.interpreted-text role="func"}), and `False` otherwise. If JIT compilation is available, this can be controlled by setting the `PYTHON_JIT`{.interpreted-text role="envvar"} environment variable to `0` (disabled) or `1` (enabled) at interpreter startup.
:::

::::::: function
[jit.is_active]{#jit.is_active}()

Return `True` if the topmost Python frame is currently executing JIT code (implies `sys._jit.is_enabled`{.interpreted-text role="func"}), and `False` otherwise.

:::: note
::: title
Note
:::

This function is intended for testing and debugging the JIT itself. It should be avoided for any other purpose.
::::

:::: note
::: title
Note
:::

Due to the nature of tracing JIT compilers, repeated calls to this function may give surprising results. For example, branching on its return value will likely lead to unexpected behavior (if doing so causes JIT code to be entered or exited):

``` pycon
>>> for warmup in range(BIG_NUMBER):
...     # This line is "hot", and is eventually JIT-compiled:
...     if sys._jit.is_active():
...         # This line is "cold", and is run in the interpreter:
...         assert sys._jit.is_active()
...
Traceback (most recent call last):
  File "<stdin>", line 5, in <module>
    assert sys._jit.is_active()
           ~~~~~~~~~~~~~~~~~~^^
AssertionError
```
::::
:::::::
::::::::::::

:::: data
last_exc

This variable is not always defined; it is set to the exception instance when an exception is not handled and the interpreter prints an error message and a stack traceback. Its intended use is to allow an interactive user to import a debugger module and engage in post-mortem debugging without having to re-execute the command that caused the error. (Typical use is `import pdb; pdb.pm()` to enter the post-mortem debugger; see `pdb`{.interpreted-text role="mod"} module for more information.)

::: versionadded
3.12
:::
::::

::::::: function
[is_immortal]{#is_immortal}(op)

Return `True`{.interpreted-text role="const"} if the given object is `immortal`{.interpreted-text role="term"}, `False`{.interpreted-text role="const"} otherwise.

:::: note
::: title
Note
:::

Objects that are immortal (and thus return `True` upon being passed to this function) are not guaranteed to be immortal in future versions, and vice versa for mortal objects.
::::

::: versionadded
3.14
:::

::: impl-detail
This function should be used for specialized purposes only. It is not guaranteed to exist in all implementations of Python.
:::
:::::::

::::: function
[is_interned]{#is_interned}(string)

Return `True`{.interpreted-text role="const"} if the given string is \"interned\", `False`{.interpreted-text role="const"} otherwise.

::: versionadded
3.13
:::

::: impl-detail
It is not guaranteed to exist in all implementations of Python.
:::
:::::

::: data
last_type last_value last_traceback

These three variables are deprecated; use `sys.last_exc`{.interpreted-text role="data"} instead. They hold the legacy representation of `sys.last_exc`, as returned from `exc_info`{.interpreted-text role="func"} above.
:::

::: data
maxsize

An integer giving the maximum value a variable of type `Py_ssize_t`{.interpreted-text role="c:type"} can take. It\'s usually `2**31 - 1` on a 32-bit platform and `2**63 - 1` on a 64-bit platform.
:::

:::: data
maxunicode

An integer giving the value of the largest Unicode code point, i.e. `1114111` (`0x10FFFF` in hexadecimal).

::: versionchanged
3.3 Before `393`{.interpreted-text role="pep"}, `sys.maxunicode` used to be either `0xFFFF` or `0x10FFFF`, depending on the configuration option that specified whether Unicode characters were stored as UCS-2 or UCS-4.
:::
::::

:::::: data
meta_path

A list of `meta path finder`{.interpreted-text role="term"} objects that have their `~importlib.abc.MetaPathFinder.find_spec`{.interpreted-text role="meth"} methods called to see if one of the objects can find the module to be imported. By default, it holds entries that implement Python\'s default import semantics. The `~importlib.abc.MetaPathFinder.find_spec`{.interpreted-text role="meth"} method is called with at least the absolute name of the module being imported. If the module to be imported is contained in a package, then the parent package\'s `~module.__path__`{.interpreted-text role="attr"} attribute is passed in as a second argument. The method returns a `module spec`{.interpreted-text role="term"}, or `None` if the module cannot be found.

::: seealso

`importlib.abc.MetaPathFinder`{.interpreted-text role="class"}

:   The abstract base class defining the interface of finder objects on `meta_path`{.interpreted-text role="data"}.

`importlib.machinery.ModuleSpec`{.interpreted-text role="class"}

:   The concrete class which `~importlib.abc.MetaPathFinder.find_spec`{.interpreted-text role="meth"} should return instances of.
:::

::: versionchanged
3.4

`Module specs <module spec>`{.interpreted-text role="term"} were introduced in Python 3.4, by `451`{.interpreted-text role="pep"}.
:::

::: versionchanged
3.12

Removed the fallback that looked for a `!find_module`{.interpreted-text role="meth"} method if a `meta_path`{.interpreted-text role="data"} entry didn\'t have a `~importlib.abc.MetaPathFinder.find_spec`{.interpreted-text role="meth"} method.
:::
::::::

::: data
modules

This is a dictionary that maps module names to modules which have already been loaded. This can be manipulated to force reloading of modules and other tricks. However, replacing the dictionary will not necessarily work as expected and deleting essential items from the dictionary may cause Python to fail. If you want to iterate over this global dictionary always use `sys.modules.copy()` or `tuple(sys.modules)` to avoid exceptions as its size may change during iteration as a side effect of code or activity in other threads.
:::

:::: data
orig_argv

The list of the original command line arguments passed to the Python executable.

The elements of `sys.orig_argv`{.interpreted-text role="data"} are the arguments to the Python interpreter, while the elements of `sys.argv`{.interpreted-text role="data"} are the arguments to the user\'s program. Arguments consumed by the interpreter itself will be present in `sys.orig_argv`{.interpreted-text role="data"} and missing from `sys.argv`{.interpreted-text role="data"}.

::: versionadded
3.10
:::
::::

::::: data
path

::: index
triple: module; search; path
:::

A list of strings that specifies the search path for modules. Initialized from the environment variable `PYTHONPATH`{.interpreted-text role="envvar"}, plus an installation-dependent default.

By default, as initialized upon program startup, a potentially unsafe path is prepended to `sys.path`{.interpreted-text role="data"} (*before* the entries inserted as a result of `PYTHONPATH`{.interpreted-text role="envvar"}):

- `python -m module` command line: prepend the current working directory.
- `python script.py` command line: prepend the script\'s directory. If it\'s a symbolic link, resolve symbolic links.
- `python -c code` and `python` (REPL) command lines: prepend an empty string, which means the current working directory.

To not prepend this potentially unsafe path, use the `-P`{.interpreted-text role="option"} command line option or the `PYTHONSAFEPATH`{.interpreted-text role="envvar"} environment variable.

A program is free to modify this list for its own purposes. Only strings should be added to `sys.path`{.interpreted-text role="data"}; all other data types are ignored during import.

::: seealso
\* Module `site`{.interpreted-text role="mod"} This describes how to use .pth files to extend `sys.path`{.interpreted-text role="data"}.
:::
:::::

::: data
path_hooks

A list of callables that take a path argument to try to create a `finder`{.interpreted-text role="term"} for the path. If a finder can be created, it is to be returned by the callable, else raise `ImportError`{.interpreted-text role="exc"}.

Originally specified in `302`{.interpreted-text role="pep"}.
:::

::: data
path_importer_cache

A dictionary acting as a cache for `finder`{.interpreted-text role="term"} objects. The keys are paths that have been passed to `sys.path_hooks`{.interpreted-text role="data"} and the values are the finders that are found. If a path is a valid file system path but no finder is found on `sys.path_hooks`{.interpreted-text role="data"} then `None` is stored.

Originally specified in `302`{.interpreted-text role="pep"}.
:::

:::::::: data
platform

A string containing a platform identifier. Known values are:

  System           `platform` value
  ---------------- ------------------
  AIX              `'aix'`
  Android          `'android'`
  Emscripten       `'emscripten'`
  FreeBSD          `'freebsd'`
  iOS              `'ios'`
  Linux            `'linux'`
  macOS            `'darwin'`
  Windows          `'win32'`
  Windows/Cygwin   `'cygwin'`
  WASI             `'wasi'`

On Unix systems not listed in the table, the value is the lowercased OS name as returned by `uname -s`, with the first part of the version as returned by `uname -r` appended, e.g. `'sunos5'`, *at the time when Python was built*. Unless you want to test for a specific system version, it is therefore recommended to use the following idiom:

    if sys.platform.startswith('sunos'):
        # SunOS-specific code here...

::: versionchanged
3.3 On Linux, `sys.platform`{.interpreted-text role="data"} doesn\'t contain the major version anymore. It is always `'linux'`, instead of `'linux2'` or `'linux3'`.
:::

::: versionchanged
3.8 On AIX, `sys.platform`{.interpreted-text role="data"} doesn\'t contain the major version anymore. It is always `'aix'`, instead of `'aix5'` or `'aix7'`.
:::

::: versionchanged
3.13 On Android, `sys.platform`{.interpreted-text role="data"} now returns `'android'` rather than `'linux'`.
:::

::: versionchanged
3.14 On FreeBSD, `sys.platform`{.interpreted-text role="data"} doesn\'t contain the major version anymore. It is always `'freebsd'`, instead of `'freebsd13'` or `'freebsd14'`.
:::

::: seealso
`os.name`{.interpreted-text role="data"} has a coarser granularity. `os.uname`{.interpreted-text role="func"} gives system-dependent version information.

The `platform`{.interpreted-text role="mod"} module provides detailed checks for the system\'s identity.
:::
::::::::

:::: data
platlibdir

Name of the platform-specific library directory. It is used to build the path of standard library and the paths of installed extension modules.

It is equal to `"lib"` on most platforms. On Fedora and SuSE, it is equal to `"lib64"` on 64-bit platforms which gives the following `sys.path` paths (where `X.Y` is the Python `major.minor` version):

- `/usr/lib64/pythonX.Y/`: Standard library (like `os.py` of the `os`{.interpreted-text role="mod"} module)
- `/usr/lib64/pythonX.Y/lib-dynload/`: C extension modules of the standard library (like the `errno`{.interpreted-text role="mod"} module, the exact filename is platform specific)
- `/usr/lib/pythonX.Y/site-packages/` (always use `lib`, not `sys.platlibdir`{.interpreted-text role="data"}): Third-party modules
- `/usr/lib64/pythonX.Y/site-packages/`: C extension modules of third-party packages

::: versionadded
3.9
:::
::::

:::::: data
prefix

A string giving the site-specific directory prefix where the platform independent Python files are installed; on Unix, the default is `/usr/local`{.interpreted-text role="file"}. This can be set at build time with the `--prefix`{.interpreted-text role="option"} argument to the `configure`{.interpreted-text role="program"} script. See `installation_paths`{.interpreted-text role="ref"} for derived paths.

:::: note
::: title
Note
:::

If a `virtual environment <venv-def>`{.interpreted-text role="ref"} is in effect, this `prefix`{.interpreted-text role="data"} will point to the virtual environment. The value for the Python installation will still be available, via `base_prefix`{.interpreted-text role="data"}. Refer to `sys-path-init-virtual-environments`{.interpreted-text role="ref"} for more information.
::::

::: versionchanged
3.14

When running under a `virtual environment <venv-def>`{.interpreted-text role="ref"}, `prefix`{.interpreted-text role="data"} and `exec_prefix`{.interpreted-text role="data"} are now set to the virtual environment prefix by the `path initialization <sys-path-init>`{.interpreted-text role="ref"}, instead of `site`{.interpreted-text role="mod"}. This means that `prefix`{.interpreted-text role="data"} and `exec_prefix`{.interpreted-text role="data"} always point to the virtual environment, even when `site`{.interpreted-text role="mod"} is disabled (`-S`{.interpreted-text role="option"}).
:::
::::::

:::: data
ps1 ps2

::: index
single: interpreter prompts single: prompts, interpreter single: \>\>\>; interpreter prompt single: \...; interpreter prompt
:::

Strings specifying the primary and secondary prompt of the interpreter. These are only defined if the interpreter is in interactive mode. Their initial values in this case are `'>>> '` and `'... '`. If a non-string object is assigned to either variable, its `str`{.interpreted-text role="func"} is re-evaluated each time the interpreter prepares to read a new interactive command; this can be used to implement a dynamic prompt.
::::

:::: function
setdlopenflags(n)

Set the flags used by the interpreter for `dlopen`{.interpreted-text role="c:func"} calls, such as when the interpreter loads extension modules. Among other things, this will enable a lazy resolving of symbols when importing a module, if called as `sys.setdlopenflags(0)`. To share symbols across extension modules, call as `sys.setdlopenflags(os.RTLD_GLOBAL)`. Symbolic names for the flag values can be found in the `os`{.interpreted-text role="mod"} module (`RTLD_{xxx}`{.interpreted-text role="samp"} constants, e.g. `os.RTLD_LAZY`{.interpreted-text role="const"}).

::: availability
Unix.
:::
::::

:::: function
set_int_max_str_digits(maxdigits)

Set the `integer string conversion length limitation
<int_max_str_digits>`{.interpreted-text role="ref"} used by this interpreter. See also `get_int_max_str_digits`{.interpreted-text role="func"}.

::: versionadded
3.11
:::
::::

:::: function
set_lazy_imports(mode)

Sets the global lazy imports mode. The *mode* parameter must be one of the following strings:

- `"normal"`: Only imports explicitly marked with the `lazy` keyword are lazy
- `"all"`: All top-level imports become potentially lazy
- `"none"`: All lazy imports are suppressed (even explicitly marked ones)

This function is intended for advanced users who need to control lazy imports across their entire application. Library developers should generally not use this function as it affects the runtime execution of applications.

In addition to the mode, lazy imports can be controlled via the filter provided by `set_lazy_imports_filter`{.interpreted-text role="func"}.

See also `get_lazy_imports`{.interpreted-text role="func"} and `810`{.interpreted-text role="pep"}.

::: versionadded
next
:::
::::

:::: function
set_lazy_imports_filter(filter)

Sets the lazy imports filter callback. The *filter* parameter must be a callable or `None` to clear the filter.

The filter function is called for every potentially lazy import to determine whether it should actually be lazy. It must have the following signature:

    def filter(importing_module: str, imported_module: str,
               fromlist: tuple[str, ...] | None) -> bool

Where:

- *importing_module* is the name of the module doing the import
- *imported_module* is the name of the module being imported
- *fromlist* is the tuple of names being imported (for `from ... import` statements), or `None` for regular imports

The filter should return `True` to allow the import to be lazy, or `False` to force an eager import.

This is an advanced feature intended for specialized users who need fine-grained control over lazy import behavior.

See also `get_lazy_imports_filter`{.interpreted-text role="func"} and `810`{.interpreted-text role="pep"}.

::: versionadded
next
:::
::::

::::::: function
setprofile(profilefunc)

::: index
single: profile function single: profiler
:::

Set the system\'s profile function, which allows you to implement a Python source code profiler in Python. See chapter `profile`{.interpreted-text role="ref"} for more information on the Python profiler. The system\'s profile function is called similarly to the system\'s trace function (see `settrace`{.interpreted-text role="func"}), but it is called with different events, for example it isn\'t called for each executed line of code (only on call and return, but the return event is reported even when an exception has been set). The function is thread-specific, but there is no way for the profiler to know about context switches between threads, so it does not make sense to use this in the presence of multiple threads. Also, its return value is not used, so it can simply return `None`. Error in the profile function will cause itself unset.

:::: note
::: title
Note
:::

The same tracing mechanism is used for `!setprofile`{.interpreted-text role="func"} as `settrace`{.interpreted-text role="func"}. To trace calls with `!setprofile`{.interpreted-text role="func"} inside a tracing function (e.g. in a debugger breakpoint), see `call_tracing`{.interpreted-text role="func"}.
::::

Profile functions should have three arguments: *frame*, *event*, and *arg*. *frame* is the current stack frame. *event* is a string: `'call'`, `'return'`, `'c_call'`, `'c_return'`, or `'c_exception'`. *arg* depends on the event type.

The events have the following meaning:

`'call'`

:   A function is called (or some other code block entered). The profile function is called; *arg* is `None`.

`'return'`

:   A function (or other code block) is about to return. The profile function is called; *arg* is the value that will be returned, or `None` if the event is caused by an exception being raised.

`'c_call'`

:   A C function is about to be called. This may be an extension function or a built-in. *arg* is the C function object.

`'c_return'`

:   A C function has returned. *arg* is the C function object.

`'c_exception'`

:   A C function has raised an exception. *arg* is the C function object.

::: audit-event
sys.setprofile \"\" sys.setprofile
:::
:::::::

:::: function
setrecursionlimit(limit)

Set the maximum depth of the Python interpreter stack to *limit*. This limit prevents infinite recursion from causing an overflow of the C stack and crashing Python.

The highest possible limit is platform-dependent. A user may need to set the limit higher when they have a program that requires deep recursion and a platform that supports a higher limit. This should be done with care, because a too-high limit can lead to a crash.

If the new limit is too low at the current recursion depth, a `RecursionError`{.interpreted-text role="exc"} exception is raised.

::: versionchanged
3.5.1 A `RecursionError`{.interpreted-text role="exc"} exception is now raised if the new limit is too low at the current recursion depth.
:::
::::

:::: function
setswitchinterval(interval)

Set the interpreter\'s thread switch interval (in seconds). This floating-point value determines the ideal duration of the \"timeslices\" allocated to concurrently running Python threads. Please note that the actual value can be higher, especially if long-running internal functions or methods are used. Also, which thread becomes scheduled at the end of the interval is the operating system\'s decision. The interpreter doesn\'t have its own scheduler.

::: versionadded
3.2
:::
::::

::::::::: function
settrace(tracefunc)

::: index
single: trace function single: debugger
:::

Set the system\'s trace function, which allows you to implement a Python source code debugger in Python. The function is thread-specific; for a debugger to support multiple threads, it must register a trace function using `settrace`{.interpreted-text role="func"} for each thread being debugged or use `threading.settrace`{.interpreted-text role="func"}.

Trace functions should have three arguments: *frame*, *event*, and *arg*. *frame* is the `current stack frame <frame-objects>`{.interpreted-text role="ref"}. *event* is a string: `'call'`, `'line'`, `'return'`, `'exception'` or `'opcode'`. *arg* depends on the event type.

The trace function is invoked (with *event* set to `'call'`) whenever a new local scope is entered; it should return a reference to a local trace function to be used for the new scope, or `None` if the scope shouldn\'t be traced.

The local trace function should return a reference to itself, or to another function which would then be used as the local trace function for the scope.

If there is any error occurred in the trace function, it will be unset, just like `settrace(None)` is called.

:::: note
::: title
Note
:::

Tracing is disabled while calling the trace function (e.g. a function set by `!settrace`{.interpreted-text role="func"}). For recursive tracing see `call_tracing`{.interpreted-text role="func"}.
::::

The events have the following meaning:

`'call'`

:   A function is called (or some other code block entered). The global trace function is called; *arg* is `None`; the return value specifies the local trace function.

`'line'`

:   The interpreter is about to execute a new line of code or re-execute the condition of a loop. The local trace function is called; *arg* is `None`; the return value specifies the new local trace function. See `Objects/lnotab_notes.txt`{.interpreted-text role="file"} for a detailed explanation of how this works. Per-line events may be disabled for a frame by setting `~frame.f_trace_lines`{.interpreted-text role="attr"} to `False`{.interpreted-text role="const"} on that `frame <frame-objects>`{.interpreted-text role="ref"}.

`'return'`

:   A function (or other code block) is about to return. The local trace function is called; *arg* is the value that will be returned, or `None` if the event is caused by an exception being raised. The trace function\'s return value is ignored.

`'exception'`

:   An exception has occurred. The local trace function is called; *arg* is a tuple `(exception, value, traceback)`; the return value specifies the new local trace function.

`'opcode'`

:   The interpreter is about to execute a new opcode (see `dis`{.interpreted-text role="mod"} for opcode details). The local trace function is called; *arg* is `None`; the return value specifies the new local trace function. Per-opcode events are not emitted by default: they must be explicitly requested by setting `~frame.f_trace_opcodes`{.interpreted-text role="attr"} to `True`{.interpreted-text role="const"} on the `frame <frame-objects>`{.interpreted-text role="ref"}.

Note that as an exception is propagated down the chain of callers, an `'exception'` event is generated at each level.

For more fine-grained usage, it\'s possible to set a trace function by assigning `frame.f_trace = tracefunc` explicitly, rather than relying on it being set indirectly via the return value from an already installed trace function. This is also required for activating the trace function on the current frame, which `settrace`{.interpreted-text role="func"} doesn\'t do. Note that in order for this to work, a global tracing function must have been installed with `settrace`{.interpreted-text role="func"} in order to enable the runtime tracing machinery, but it doesn\'t need to be the same tracing function (e.g. it could be a low overhead tracing function that simply returns `None` to disable itself immediately on each frame).

For more information on code and frame objects, refer to `types`{.interpreted-text role="ref"}.

::: audit-event
sys.settrace \"\" sys.settrace
:::

::: impl-detail
The `settrace`{.interpreted-text role="func"} function is intended only for implementing debuggers, profilers, coverage tools and the like. Its behavior is part of the implementation platform, rather than part of the language definition, and thus may not be available in all Python implementations.
:::

::: versionchanged
3.7

`'opcode'` event type added; `~frame.f_trace_lines`{.interpreted-text role="attr"} and `~frame.f_trace_opcodes`{.interpreted-text role="attr"} attributes added to frames
:::
:::::::::

:::::::: function
set_asyncgen_hooks(\[firstiter\] \[, finalizer\])

Accepts two optional keyword arguments which are callables that accept an `asynchronous generator iterator`{.interpreted-text role="term"} as an argument. The *firstiter* callable will be called when an asynchronous generator is iterated for the first time. The *finalizer* will be called when an asynchronous generator is about to be garbage collected.

::: audit-event
sys.set_asyncgen_hooks_firstiter \"\" sys.set_asyncgen_hooks
:::

::: audit-event
sys.set_asyncgen_hooks_finalizer \"\" sys.set_asyncgen_hooks
:::

Two auditing events are raised because the underlying API consists of two calls, each of which must raise its own event.

::: versionadded
3.6 See `525`{.interpreted-text role="pep"} for more details, and for a reference example of a *finalizer* method see the implementation of `asyncio.Loop.shutdown_asyncgens` in `Lib/asyncio/base_events.py`{.interpreted-text role="source"}
:::

:::: note
::: title
Note
:::

This function has been added on a provisional basis (see `411`{.interpreted-text role="pep"} for details.)
::::
::::::::

:::::: function
set_coroutine_origin_tracking_depth(depth)

Allows enabling or disabling coroutine origin tracking. When enabled, the `cr_origin` attribute on coroutine objects will contain a tuple of (filename, line number, function name) tuples describing the traceback where the coroutine object was created, with the most recent call first. When disabled, `cr_origin` will be `None`.

To enable, pass a *depth* value greater than zero; this sets the number of frames whose information will be captured. To disable, set *depth* to zero.

This setting is thread-specific.

::: versionadded
3.7
:::

:::: note
::: title
Note
:::

This function has been added on a provisional basis (see `411`{.interpreted-text role="pep"} for details.) Use it only for debugging purposes.
::::
::::::

:::::: function
activate_stack_trampoline(backend, /)

Activate the stack profiler trampoline *backend*. The only supported backend is `"perf"`.

Stack trampolines cannot be activated if the JIT is active.

::: availability
Linux.
:::

::: versionadded
3.12
:::

::: seealso
- `perf_profiling`{.interpreted-text role="ref"}
- <https://perf.wiki.kernel.org>
:::
::::::

::::: function
deactivate_stack_trampoline()

Deactivate the current stack profiler trampoline backend.

If no stack profiler is activated, this function has no effect.

::: availability
Linux.
:::

::: versionadded
3.12
:::
:::::

::::: function
is_stack_trampoline_active()

Return `True` if a stack profiler trampoline is active.

::: availability
Linux.
:::

::: versionadded
3.12
:::
:::::

::::::: function
remote_exec(pid, script)

Executes *script*, a file containing Python code in the remote process with the given *pid*.

This function returns immediately, and the code will be executed by the target process\'s main thread at the next available opportunity, similarly to how signals are handled. There is no interface to determine when the code has been executed. The caller is responsible for making sure that the file still exists whenever the remote process tries to read it and that it hasn\'t been overwritten.

The remote process must be running a CPython interpreter of the same major and minor version as the local process. If either the local or remote interpreter is pre-release (alpha, beta, or release candidate) then the local and remote interpreters must be the same exact version.

See `remote-debugging`{.interpreted-text role="ref"} for more information about the remote debugging mechanism.

::: audit-event
sys.remote_exec pid script_path

When the code is executed in the remote process, an `auditing event <auditing>`{.interpreted-text role="ref"} `sys.remote_exec` is raised with the *pid* and the path to the script file. This event is raised in the process that called `sys.remote_exec`{.interpreted-text role="func"}.
:::

::: audit-event
cpython.remote_debugger_script script_path

When the script is executed in the remote process, an `auditing event <auditing>`{.interpreted-text role="ref"} `cpython.remote_debugger_script` is raised with the path in the remote process. This event is raised in the remote process, not the one that called `sys.remote_exec`{.interpreted-text role="func"}.
:::

::: availability
Unix, Windows.
:::

::: versionadded
3.14 See `768`{.interpreted-text role="pep"} for more details.
:::
:::::::

:::::::: function
[enablelegacywindowsfsencoding]{#enablelegacywindowsfsencoding}()

Changes the `filesystem encoding and error handler`{.interpreted-text role="term"} to \'mbcs\' and \'replace\' respectively, for consistency with versions of Python prior to 3.6.

This is equivalent to defining the `PYTHONLEGACYWINDOWSFSENCODING`{.interpreted-text role="envvar"} environment variable before launching Python.

See also `sys.getfilesystemencoding`{.interpreted-text role="func"} and `sys.getfilesystemencodeerrors`{.interpreted-text role="func"}.

::: availability
Windows.
:::

:::: note
::: title
Note
:::

Changing the filesystem encoding after Python startup is risky because the old fsencoding or paths encoded by the old fsencoding may be cached somewhere. Use `PYTHONLEGACYWINDOWSFSENCODING`{.interpreted-text role="envvar"} instead.
::::

::: versionadded
3.6 See `529`{.interpreted-text role="pep"} for more details.
:::

::: deprecated-removed
3.13 3.16 Use `PYTHONLEGACYWINDOWSFSENCODING`{.interpreted-text role="envvar"} instead.
:::
::::::::

:::::: data
stdin stdout stderr

`File objects <file object>`{.interpreted-text role="term"} used by the interpreter for standard input, output and errors:

- `stdin` is used for all interactive input (including calls to `input`{.interpreted-text role="func"});
- `stdout` is used for the output of `print`{.interpreted-text role="func"} and `expression`{.interpreted-text role="term"} statements and for the prompts of `input`{.interpreted-text role="func"};
- The interpreter\'s own prompts and its error messages go to `stderr`.

These streams are regular `text files <text file>`{.interpreted-text role="term"} like those returned by the `open`{.interpreted-text role="func"} function. Their parameters are chosen as follows:

- The encoding and error handling are is initialized from `PyConfig.stdio_encoding`{.interpreted-text role="c:member"} and `PyConfig.stdio_errors`{.interpreted-text role="c:member"}.

  On Windows, UTF-8 is used for the console device. Non-character devices such as disk files and pipes use the system locale encoding (i.e. the ANSI codepage). Non-console character devices such as NUL (i.e. where `isatty()` returns `True`) use the value of the console input and output codepages at startup, respectively for stdin and stdout/stderr. This defaults to the system `locale encoding`{.interpreted-text role="term"} if the process is not initially attached to a console.

  The special behaviour of the console can be overridden by setting the environment variable PYTHONLEGACYWINDOWSSTDIO before starting Python. In that case, the console codepages are used as for any other character device.

  Under all platforms, you can override the character encoding by setting the `PYTHONIOENCODING`{.interpreted-text role="envvar"} environment variable before starting Python or by using the new `-X`{.interpreted-text role="option"} `utf8` command line option and `PYTHONUTF8`{.interpreted-text role="envvar"} environment variable. However, for the Windows console, this only applies when `PYTHONLEGACYWINDOWSSTDIO`{.interpreted-text role="envvar"} is also set.

- When interactive, the `stdout` stream is line-buffered. Otherwise, it is block-buffered like regular text files. The `stderr` stream is line-buffered in both cases. You can make both streams unbuffered by passing the `-u`{.interpreted-text role="option"} command-line option or setting the `PYTHONUNBUFFERED`{.interpreted-text role="envvar"} environment variable.

::: versionchanged
3.9 Non-interactive `stderr` is now line-buffered instead of fully buffered.
:::

:::: note
::: title
Note
:::

To write or read binary data from/to the standard streams, use the underlying binary `~io.TextIOBase.buffer`{.interpreted-text role="data"} object. For example, to write bytes to `stdout`{.interpreted-text role="data"}, use `sys.stdout.buffer.write(b'abc')`.

However, if you are writing a library (and do not control in which context its code will be executed), be aware that the standard streams may be replaced with file-like objects like `io.StringIO`{.interpreted-text role="class"} which do not support the `!buffer`{.interpreted-text role="attr"} attribute.
::::
::::::

::::: data
\_\_stdin\_\_ \_\_stdout\_\_ \_\_stderr\_\_

These objects contain the original values of `stdin`, `stderr` and `stdout` at the start of the program. They are used during finalization, and could be useful to print to the actual standard stream no matter if the `sys.std*` object has been redirected.

It can also be used to restore the actual files to known working file objects in case they have been overwritten with a broken object. However, the preferred way to do this is to explicitly save the previous stream before replacing it, and restore the saved object.

:::: note
::: title
Note
:::

Under some conditions `stdin`, `stdout` and `stderr` as well as the original values `__stdin__`, `__stdout__` and `__stderr__` can be `None`. It is usually the case for Windows GUI apps that aren\'t connected to a console and Python apps started with `pythonw`{.interpreted-text role="program"}.
::::
:::::

:::: data
stdlib_module_names

A frozenset of strings containing the names of standard library modules.

It is the same on all platforms. Modules which are not available on some platforms and modules disabled at Python build are also listed. All module kinds are listed: pure Python, built-in, frozen and extension modules. Test modules are excluded.

For packages, only the main package is listed: sub-packages and sub-modules are not listed. For example, the `email` package is listed, but the `email.mime` sub-package and the `email.message` sub-module are not listed.

See also the `sys.builtin_module_names`{.interpreted-text role="data"} list.

::: versionadded
3.10
:::
::::

::::::: data
thread_info

A `named tuple`{.interpreted-text role="term"} holding information about the thread implementation.

::: attribute
thread_info.name

The name of the thread implementation:

- `"nt"`: Windows threads
- `"pthread"`: POSIX threads
- `"pthread-stubs"`: stub POSIX threads (on WebAssembly platforms without threading support)
- `"solaris"`: Solaris threads
:::

::: attribute
thread_info.lock

The name of the lock implementation:

- `"semaphore"`: a lock uses a semaphore
- `"mutex+cond"`: a lock uses a mutex and a condition variable
- `None` if this information is unknown
:::

::: attribute
thread_info.version

The name and version of the thread library. It is a string, or `None` if this information is unknown.
:::

::: versionadded
3.3
:::
:::::::

::: data
tracebacklimit

When this variable is set to an integer value, it determines the maximum number of levels of traceback information printed when an unhandled exception occurs. The default is `1000`. When set to `0` or less, all traceback information is suppressed and only the exception type and value are printed.
:::

::::::::: function
unraisablehook(unraisable, /)

Handle an unraisable exception.

Called when an exception has occurred but there is no way for Python to handle it. For example, when a destructor raises an exception or during garbage collection (`gc.collect`{.interpreted-text role="func"}).

The *unraisable* argument has the following attributes:

- `!exc_type`{.interpreted-text role="attr"}: Exception type.
- `!exc_value`{.interpreted-text role="attr"}: Exception value, can be `None`.
- `!exc_traceback`{.interpreted-text role="attr"}: Exception traceback, can be `None`.
- `!err_msg`{.interpreted-text role="attr"}: Error message, can be `None`.
- `!object`{.interpreted-text role="attr"}: Object causing the exception, can be `None`.

The default hook formats `!err_msg`{.interpreted-text role="attr"} and `!object`{.interpreted-text role="attr"} as: `f'{err_msg}: {object!r}'`; use \"Exception ignored in\" error message if `!err_msg`{.interpreted-text role="attr"} is `None`. Similar to the `traceback`{.interpreted-text role="mod"} module, this adds color to exceptions by default. This can be disabled using `environment variables <using-on-controlling-color>`{.interpreted-text role="ref"}.

`sys.unraisablehook`{.interpreted-text role="func"} can be overridden to control how unraisable exceptions are handled.

::: versionchanged
3.15 Exceptions are now printed with colorful text.
:::

::: seealso
`excepthook`{.interpreted-text role="func"} which handles uncaught exceptions.
:::

:::: warning
::: title
Warning
:::

Storing `!exc_value`{.interpreted-text role="attr"} using a custom hook can create a reference cycle. It should be cleared explicitly to break the reference cycle when the exception is no longer needed.

Storing `!object`{.interpreted-text role="attr"} using a custom hook can resurrect it if it is set to an object which is being finalized. Avoid storing `!object`{.interpreted-text role="attr"} after the custom hook completes to avoid resurrecting objects.
::::

::: audit-event
sys.unraisablehook hook,unraisable sys.unraisablehook

Raise an auditing event `sys.unraisablehook` with arguments *hook*, *unraisable* when an exception that cannot be handled occurs. The *unraisable* object is the same as what will be passed to the hook. If no hook has been set, *hook* may be `None`.
:::

::: versionadded
3.8
:::
:::::::::

::: data
version

A string containing the version number of the Python interpreter plus additional information on the build number and compiler used. This string is displayed when the interactive interpreter is started. Do not extract version information out of it, rather, use `version_info`{.interpreted-text role="data"} and the functions provided by the `platform`{.interpreted-text role="mod"} module.
:::

::: data
api_version

The C API version, equivalent to the C macro `PYTHON_API_VERSION`{.interpreted-text role="c:macro"}. Defined for backwards compatibility.

Currently, this constant is not updated in new Python versions, and is not useful for versioning. This may change in the future.
:::

:::: data
version_info

A tuple containing the five components of the version number: *major*, *minor*, *micro*, *releaselevel*, and *serial*. All values except *releaselevel* are integers; the release level is `'alpha'`, `'beta'`, `'candidate'`, or `'final'`. The `version_info` value corresponding to the Python version 2.0 is `(2, 0, 0, 'final', 0)`. The components can also be accessed by name, so `sys.version_info[0]` is equivalent to `sys.version_info.major` and so on.

::: versionchanged
3.1 Added named component attributes.
:::
::::

::: data
warnoptions

This is an implementation detail of the warnings framework; do not modify this value. Refer to the `warnings`{.interpreted-text role="mod"} module for more information on the warnings framework.
:::

:::: data
winver

The version number used to form registry keys on Windows platforms. This is stored as string resource 1000 in the Python DLL. The value is normally the major and minor versions of the running Python interpreter. It is provided in the `!sys`{.interpreted-text role="mod"} module for informational purposes; modifying this value has no effect on the registry keys used by Python.

::: availability
Windows.
:::
::::

::: {.data noindex=""}
monitoring

Namespace containing functions and constants for register callbacks and controlling monitoring events. See `sys.monitoring`{.interpreted-text role="mod"} for details.
:::

::::: data
[xoptions]{#xoptions}

A dictionary of the various implementation-specific flags passed through the `-X`{.interpreted-text role="option"} command-line option. Option names are either mapped to their values, if given explicitly, or to `True`{.interpreted-text role="const"}. Example:

``` shell-session
$ ./python -Xa=b -Xc
Python 3.2a3+ (py3k, Oct 16 2010, 20:14:50)
[GCC 4.4.3] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import sys
>>> sys._xoptions
{'a': 'b', 'c': True}
```

::: impl-detail
This is a CPython-specific way of accessing options passed through `-X`{.interpreted-text role="option"}. Other implementations may export them through other means, or not at all.
:::

::: versionadded
3.2
:::
:::::

**Citations**

::: {#citations}

[C99]{#C99 .citation-label}

:   ISO/IEC 9899:1999. \"Programming languages \-- C.\" A public draft of this standard is available at [https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1256.pdf\\](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1256.pdf\) .
:::
