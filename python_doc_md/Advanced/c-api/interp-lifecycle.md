# Interpreter initialization and finalization {#initialization}

See `Python Initialization Configuration <init-config>`{.interpreted-text role="ref"} for details on how to configure the interpreter prior to initialization.

## Before Python initialization {#pre-init-safe}

In an application embedding Python, the `Py_Initialize`{.interpreted-text role="c:func"} function must be called before using any other Python/C API functions; with the exception of a few functions and the `global configuration variables
<global-conf-vars>`{.interpreted-text role="ref"}.

The following functions can be safely called before Python is initialized:

- Functions that initialize the interpreter:
  - `Py_Initialize`{.interpreted-text role="c:func"}
  - `Py_InitializeEx`{.interpreted-text role="c:func"}
  - `Py_InitializeFromConfig`{.interpreted-text role="c:func"}
  - `Py_BytesMain`{.interpreted-text role="c:func"}
  - `Py_Main`{.interpreted-text role="c:func"}
  - the runtime pre-initialization functions covered in `init-config`{.interpreted-text role="ref"}
- Configuration functions:
  - `PyImport_AppendInittab`{.interpreted-text role="c:func"}
  - `PyImport_ExtendInittab`{.interpreted-text role="c:func"}
  - `!PyInitFrozenExtensions`{.interpreted-text role="c:func"}
  - `PyMem_SetAllocator`{.interpreted-text role="c:func"}
  - `PyMem_SetupDebugHooks`{.interpreted-text role="c:func"}
  - `PyObject_SetArenaAllocator`{.interpreted-text role="c:func"}
  - `Py_SetProgramName`{.interpreted-text role="c:func"}
  - `Py_SetPythonHome`{.interpreted-text role="c:func"}
  - the configuration functions covered in `init-config`{.interpreted-text role="ref"}
- Informative functions:
  - `Py_IsInitialized`{.interpreted-text role="c:func"}
  - `PyMem_GetAllocator`{.interpreted-text role="c:func"}
  - `PyObject_GetArenaAllocator`{.interpreted-text role="c:func"}
  - `Py_GetBuildInfo`{.interpreted-text role="c:func"}
  - `Py_GetCompiler`{.interpreted-text role="c:func"}
  - `Py_GetCopyright`{.interpreted-text role="c:func"}
  - `Py_GetPlatform`{.interpreted-text role="c:func"}
  - `Py_GetVersion`{.interpreted-text role="c:func"}
  - `Py_IsInitialized`{.interpreted-text role="c:func"}
- Utilities:
  - `Py_DecodeLocale`{.interpreted-text role="c:func"}
  - the status reporting and utility functions covered in `init-config`{.interpreted-text role="ref"}
- Memory allocators:
  - `PyMem_RawMalloc`{.interpreted-text role="c:func"}
  - `PyMem_RawRealloc`{.interpreted-text role="c:func"}
  - `PyMem_RawCalloc`{.interpreted-text role="c:func"}
  - `PyMem_RawFree`{.interpreted-text role="c:func"}
- Synchronization:
  - `PyMutex_Lock`{.interpreted-text role="c:func"}
  - `PyMutex_Unlock`{.interpreted-text role="c:func"}

:::: note
::: title
Note
:::

Despite their apparent similarity to some of the functions listed above, the following functions **should not be called** before the interpreter has been initialized: `Py_EncodeLocale`{.interpreted-text role="c:func"}, `PyEval_InitThreads`{.interpreted-text role="c:func"}, and `Py_RunMain`{.interpreted-text role="c:func"}.
::::

## Global configuration variables {#global-conf-vars}

Python has variables for the global configuration to control different features and options. By default, these flags are controlled by `command line
options <using-on-interface-options>`{.interpreted-text role="ref"}.

When a flag is set by an option, the value of the flag is the number of times that the option was set. For example, `-b` sets `Py_BytesWarningFlag`{.interpreted-text role="c:data"} to 1 and `-bb` sets `Py_BytesWarningFlag`{.interpreted-text role="c:data"} to 2.

> This API is kept for backward compatibility: setting `PyConfig.bytes_warning`{.interpreted-text role="c:member"} should be used instead, see `Python
> Initialization Configuration <init-config>`{.interpreted-text role="ref"}.
>
> Issue a warning when comparing `bytes`{.interpreted-text role="class"} or `bytearray`{.interpreted-text role="class"} with `str`{.interpreted-text role="class"} or `bytes`{.interpreted-text role="class"} with `int`{.interpreted-text role="class"}. Issue an error if greater or equal to `2`.
>
> Set by the `-b`{.interpreted-text role="option"} option.
>
> ::: deprecated-removed
> 3.12 3.15
> :::

> This API is kept for backward compatibility: setting `PyConfig.parser_debug`{.interpreted-text role="c:member"} should be used instead, see `Python
> Initialization Configuration <init-config>`{.interpreted-text role="ref"}.
>
> Turn on parser debugging output (for expert only, depending on compilation options).
>
> Set by the `-d`{.interpreted-text role="option"} option and the `PYTHONDEBUG`{.interpreted-text role="envvar"} environment variable.
>
> ::: deprecated-removed
> 3.12 3.15
> :::

> This API is kept for backward compatibility: setting `PyConfig.write_bytecode`{.interpreted-text role="c:member"} should be used instead, see `Python
> Initialization Configuration <init-config>`{.interpreted-text role="ref"}.
>
> If set to non-zero, Python won\'t try to write `.pyc` files on the import of source modules.
>
> Set by the `-B`{.interpreted-text role="option"} option and the `PYTHONDONTWRITEBYTECODE`{.interpreted-text role="envvar"} environment variable.
>
> ::: deprecated-removed
> 3.12 3.15
> :::

> This API is kept for backward compatibility: setting `PyConfig.pathconfig_warnings`{.interpreted-text role="c:member"} should be used instead, see `Python Initialization Configuration <init-config>`{.interpreted-text role="ref"}.
>
> Private flag used by `_freeze_module` and `frozenmain` programs.
>
> ::: deprecated-removed
> 3.12 3.15
> :::

> This API is kept for backward compatibility: setting `PyConfig.hash_seed`{.interpreted-text role="c:member"} and `PyConfig.use_hash_seed`{.interpreted-text role="c:member"} should be used instead, see `Python Initialization Configuration
> <init-config>`{.interpreted-text role="ref"}.
>
> Set to `1` if the `PYTHONHASHSEED`{.interpreted-text role="envvar"} environment variable is set to a non-empty string.
>
> If the flag is non-zero, read the `PYTHONHASHSEED`{.interpreted-text role="envvar"} environment variable to initialize the secret hash seed.
>
> ::: deprecated-removed
> 3.12 3.15
> :::

> This API is kept for backward compatibility: setting `PyConfig.use_environment`{.interpreted-text role="c:member"} should be used instead, see `Python Initialization Configuration <init-config>`{.interpreted-text role="ref"}.
>
> Ignore all `!PYTHON*`{.interpreted-text role="envvar"} environment variables, e.g. `PYTHONPATH`{.interpreted-text role="envvar"} and `PYTHONHOME`{.interpreted-text role="envvar"}, that might be set.
>
> Set by the `-E`{.interpreted-text role="option"} and `-I`{.interpreted-text role="option"} options.
>
> ::: deprecated-removed
> 3.12 3.15
> :::

> This API is kept for backward compatibility: setting `PyConfig.inspect`{.interpreted-text role="c:member"} should be used instead, see `Python Initialization Configuration <init-config>`{.interpreted-text role="ref"}.
>
> When a script is passed as first argument or the `-c`{.interpreted-text role="option"} option is used, enter interactive mode after executing the script or the command, even when `sys.stdin`{.interpreted-text role="data"} does not appear to be a terminal.
>
> Set by the `-i`{.interpreted-text role="option"} option and the `PYTHONINSPECT`{.interpreted-text role="envvar"} environment variable.
>
> ::: deprecated-removed
> 3.12 3.15
> :::

> This API is kept for backward compatibility: setting `PyConfig.interactive`{.interpreted-text role="c:member"} should be used instead, see `Python Initialization Configuration <init-config>`{.interpreted-text role="ref"}.
>
> Set by the `-i`{.interpreted-text role="option"} option.
>
> ::: deprecated-removed
> 3.12 3.15
> :::

> This API is kept for backward compatibility: setting `PyConfig.isolated`{.interpreted-text role="c:member"} should be used instead, see `Python Initialization Configuration <init-config>`{.interpreted-text role="ref"}.
>
> Run Python in isolated mode. In isolated mode `sys.path`{.interpreted-text role="data"} contains neither the script\'s directory nor the user\'s site-packages directory.
>
> Set by the `-I`{.interpreted-text role="option"} option.
>
> ::: versionadded
> 3.4
> :::
>
> ::: deprecated-removed
> 3.12 3.15
> :::

> This API is kept for backward compatibility: setting `PyPreConfig.legacy_windows_fs_encoding`{.interpreted-text role="c:member"} should be used instead, see `Python Initialization Configuration <init-config>`{.interpreted-text role="ref"}.
>
> If the flag is non-zero, use the `mbcs` encoding with `replace` error handler, instead of the UTF-8 encoding with `surrogatepass` error handler, for the `filesystem encoding and error handler`{.interpreted-text role="term"}.
>
> Set to `1` if the `PYTHONLEGACYWINDOWSFSENCODING`{.interpreted-text role="envvar"} environment variable is set to a non-empty string.
>
> See `529`{.interpreted-text role="pep"} for more details.
>
> ::: availability
> Windows.
> :::
>
> ::: deprecated-removed
> 3.12 3.15
> :::

> This API is kept for backward compatibility: setting `PyConfig.legacy_windows_stdio`{.interpreted-text role="c:member"} should be used instead, see `Python Initialization Configuration <init-config>`{.interpreted-text role="ref"}.
>
> If the flag is non-zero, use `io.FileIO`{.interpreted-text role="class"} instead of `!io._WindowsConsoleIO`{.interpreted-text role="class"} for `sys`{.interpreted-text role="mod"} standard streams.
>
> Set to `1` if the `PYTHONLEGACYWINDOWSSTDIO`{.interpreted-text role="envvar"} environment variable is set to a non-empty string.
>
> See `528`{.interpreted-text role="pep"} for more details.
>
> ::: availability
> Windows.
> :::
>
> ::: deprecated-removed
> 3.12 3.15
> :::

> This API is kept for backward compatibility: setting `PyConfig.site_import`{.interpreted-text role="c:member"} should be used instead, see `Python Initialization Configuration <init-config>`{.interpreted-text role="ref"}.
>
> Disable the import of the module `site`{.interpreted-text role="mod"} and the site-dependent manipulations of `sys.path`{.interpreted-text role="data"} that it entails. Also disable these manipulations if `site`{.interpreted-text role="mod"} is explicitly imported later (call `site.main`{.interpreted-text role="func"} if you want them to be triggered).
>
> Set by the `-S`{.interpreted-text role="option"} option.
>
> ::: deprecated-removed
> 3.12 3.15
> :::

> This API is kept for backward compatibility: setting `PyConfig.user_site_directory`{.interpreted-text role="c:member"} should be used instead, see `Python Initialization Configuration <init-config>`{.interpreted-text role="ref"}.
>
> Don\'t add the `user site-packages directory <site.USER_SITE>`{.interpreted-text role="data"} to `sys.path`{.interpreted-text role="data"}.
>
> Set by the `-s`{.interpreted-text role="option"} and `-I`{.interpreted-text role="option"} options, and the `PYTHONNOUSERSITE`{.interpreted-text role="envvar"} environment variable.
>
> ::: deprecated-removed
> 3.12 3.15
> :::

> This API is kept for backward compatibility: setting `PyConfig.optimization_level`{.interpreted-text role="c:member"} should be used instead, see `Python Initialization Configuration <init-config>`{.interpreted-text role="ref"}.
>
> Set by the `-O`{.interpreted-text role="option"} option and the `PYTHONOPTIMIZE`{.interpreted-text role="envvar"} environment variable.
>
> ::: deprecated-removed
> 3.12 3.15
> :::

> This API is kept for backward compatibility: setting `PyConfig.quiet`{.interpreted-text role="c:member"} should be used instead, see `Python
> Initialization Configuration <init-config>`{.interpreted-text role="ref"}.
>
> Don\'t display the copyright and version messages even in interactive mode.
>
> Set by the `-q`{.interpreted-text role="option"} option.
>
> ::: versionadded
> 3.2
> :::
>
> ::: deprecated-removed
> 3.12 3.15
> :::

> This API is kept for backward compatibility: setting `PyConfig.buffered_stdio`{.interpreted-text role="c:member"} should be used instead, see `Python
> Initialization Configuration <init-config>`{.interpreted-text role="ref"}.
>
> Force the stdout and stderr streams to be unbuffered.
>
> Set by the `-u`{.interpreted-text role="option"} option and the `PYTHONUNBUFFERED`{.interpreted-text role="envvar"} environment variable.
>
> ::: deprecated-removed
> 3.12 3.15
> :::

> This API is kept for backward compatibility: setting `PyConfig.verbose`{.interpreted-text role="c:member"} should be used instead, see `Python
> Initialization Configuration <init-config>`{.interpreted-text role="ref"}.
>
> Print a message each time a module is initialized, showing the place (filename or built-in module) from which it is loaded. If greater or equal to `2`, print a message for each file that is checked for when searching for a module. Also provides information on module cleanup at exit.
>
> Set by the `-v`{.interpreted-text role="option"} option and the `PYTHONVERBOSE`{.interpreted-text role="envvar"} environment variable.
>
> ::: deprecated-removed
> 3.12 3.15
> :::

## Initializing and finalizing the interpreter

> ::: index
> single: PyEval_InitThreads() single: modules (in module sys) single: path (in module sys) pair: module; builtins pair: module; \_\_main\_\_ pair: module; sys triple: module; search; path single: Py_FinalizeEx (C function)
> :::
>
> Initialize the Python interpreter. In an application embedding Python, this should be called before using any other Python/C API functions; see `Before Python Initialization <pre-init-safe>`{.interpreted-text role="ref"} for the few exceptions.
>
> This initializes the table of loaded modules (`sys.modules`), and creates the fundamental modules `builtins`{.interpreted-text role="mod"}, `__main__`{.interpreted-text role="mod"} and `sys`{.interpreted-text role="mod"}. It also initializes the module search path (`sys.path`). It does not set `sys.argv`; use the `Python Initialization Configuration <init-config>`{.interpreted-text role="ref"} API for that. This is a no-op when called for a second time (without calling `Py_FinalizeEx`{.interpreted-text role="c:func"} first). There is no return value; it is a fatal error if the initialization fails.
>
> Use `Py_InitializeFromConfig`{.interpreted-text role="c:func"} to customize the `Python Initialization Configuration <init-config>`{.interpreted-text role="ref"}.
>
> :::: note
> ::: title
> Note
> :::
>
> On Windows, changes the console mode from `O_TEXT` to `O_BINARY`, which will also affect non-Python uses of the console using the C Runtime.
> ::::

> This function works like `Py_Initialize`{.interpreted-text role="c:func"} if *initsigs* is `1`. If *initsigs* is `0`, it skips initialization registration of signal handlers, which may be useful when CPython is embedded as part of a larger application.
>
> Use `Py_InitializeFromConfig`{.interpreted-text role="c:func"} to customize the `Python Initialization Configuration <init-config>`{.interpreted-text role="ref"}.

> Initialize Python from *config* configuration, as described in `init-from-config`{.interpreted-text role="ref"}.
>
> See the `init-config`{.interpreted-text role="ref"} section for details on pre-initializing the interpreter, populating the runtime configuration structure, and querying the returned status structure.

> Return true (nonzero) when the Python interpreter has been initialized, false (zero) if not. After `Py_FinalizeEx`{.interpreted-text role="c:func"} is called, this returns false until `Py_Initialize`{.interpreted-text role="c:func"} is called again.

> Return true (non-zero) if the main Python interpreter is `shutting down <interpreter shutdown>`{.interpreted-text role="term"}. Return false (zero) otherwise.
>
> ::: versionadded
> 3.13
> :::

> Undo all initializations made by `Py_Initialize`{.interpreted-text role="c:func"} and subsequent use of Python/C API functions, and destroy all sub-interpreters (see `Py_NewInterpreter`{.interpreted-text role="c:func"} below) that were created and not yet destroyed since the last call to `Py_Initialize`{.interpreted-text role="c:func"}. This is a no-op when called for a second time (without calling `Py_Initialize`{.interpreted-text role="c:func"} again first).
>
> Since this is the reverse of `Py_Initialize`{.interpreted-text role="c:func"}, it should be called in the same thread with the same interpreter active. That means the main thread and the main interpreter. This should never be called while `Py_RunMain`{.interpreted-text role="c:func"} is running.
>
> Normally the return value is `0`. If there were errors during finalization (flushing buffered data), `-1` is returned.
>
> Note that Python will do a best effort at freeing all memory allocated by the Python interpreter. Therefore, any C-Extension should make sure to correctly clean up all of the previously allocated PyObjects before using them in subsequent calls to `Py_Initialize`{.interpreted-text role="c:func"}. Otherwise it could introduce vulnerabilities and incorrect behavior.
>
> This function is provided for a number of reasons. An embedding application might want to restart Python without having to restart the application itself. An application that has loaded the Python interpreter from a dynamically loadable library (or DLL) might want to free all memory allocated by Python before unloading the DLL. During a hunt for memory leaks in an application a developer might want to free all memory allocated by Python before exiting from the application.
>
> **Bugs and caveats:** The destruction of modules and objects in modules is done in random order; this may cause destructors (`~object.__del__`{.interpreted-text role="meth"} methods) to fail when they depend on other objects (even functions) or modules. Dynamically loaded extension modules loaded by Python are not unloaded. Small amounts of memory allocated by the Python interpreter may not be freed (if you find a leak, please report it). Memory tied up in circular references between objects is not freed. Interned strings will all be deallocated regardless of their reference count. Some memory allocated by extension modules may not be freed. Some extensions may not work properly if their initialization routine is called more than once; this can happen if an application calls `Py_Initialize`{.interpreted-text role="c:func"} and `Py_FinalizeEx`{.interpreted-text role="c:func"} more than once. `Py_FinalizeEx`{.interpreted-text role="c:func"} must not be called recursively from within itself. Therefore, it must not be called by any code that may be run as part of the interpreter shutdown process, such as `atexit`{.interpreted-text role="py:mod"} handlers, object finalizers, or any code that may be run while flushing the stdout and stderr files.
>
> ::: audit-event
> cpython.\_PySys_ClearAuditHooks \"\" c.Py_FinalizeEx
> :::
>
> ::: versionadded
> 3.6
> :::

> This is a backwards-compatible version of `Py_FinalizeEx`{.interpreted-text role="c:func"} that disregards the return value.

> Similar to `Py_Main`{.interpreted-text role="c:func"} but *argv* is an array of bytes strings, allowing the calling application to delegate the text decoding step to the CPython runtime.
>
> ::: versionadded
> 3.8
> :::

> The main program for the standard interpreter, encapsulating a full initialization/finalization cycle, as well as additional behaviour to implement reading configurations settings from the environment and command line, and then executing `__main__` in accordance with `using-on-cmdline`{.interpreted-text role="ref"}.
>
> This is made available for programs which wish to support the full CPython command line interface, rather than just embedding a Python runtime in a larger application.
>
> The *argc* and *argv* parameters are similar to those which are passed to a C program\'s `main`{.interpreted-text role="c:func"} function, except that the *argv* entries are first converted to `wchar_t` using `Py_DecodeLocale`{.interpreted-text role="c:func"}. It is also important to note that the argument list entries may be modified to point to strings other than those passed in (however, the contents of the strings pointed to by the argument list are not modified).
>
> The return value is `2` if the argument list does not represent a valid Python command line, and otherwise the same as `Py_RunMain`{.interpreted-text role="c:func"}.
>
> In terms of the CPython runtime configuration APIs documented in the `runtime configuration <init-config>`{.interpreted-text role="ref"} section (and without accounting for error handling), `Py_Main` is approximately equivalent to:
>
> ``` c
> PyConfig config;
> PyConfig_InitPythonConfig(&config);
> PyConfig_SetArgv(&config, argc, argv);
> Py_InitializeFromConfig(&config);
> PyConfig_Clear(&config);
>
> Py_RunMain();
> ```
>
> In normal usage, an embedding application will call this function *instead* of calling `Py_Initialize`{.interpreted-text role="c:func"}, `Py_InitializeEx`{.interpreted-text role="c:func"} or `Py_InitializeFromConfig`{.interpreted-text role="c:func"} directly, and all settings will be applied as described elsewhere in this documentation. If this function is instead called *after* a preceding runtime initialization API call, then exactly which environmental and command line configuration settings will be updated is version dependent (as it depends on which settings correctly support being modified after they have already been set once when the runtime was first initialized).

> Executes the main module in a fully configured CPython runtime.
>
> Executes the command (`PyConfig.run_command`{.interpreted-text role="c:member"}), the script (`PyConfig.run_filename`{.interpreted-text role="c:member"}) or the module (`PyConfig.run_module`{.interpreted-text role="c:member"}) specified on the command line or in the configuration. If none of these values are set, runs the interactive Python prompt (REPL) using the `__main__` module\'s global namespace.
>
> If `PyConfig.inspect`{.interpreted-text role="c:member"} is not set (the default), the return value will be `0` if the interpreter exits normally (that is, without raising an exception), the exit status of an unhandled `SystemExit`{.interpreted-text role="exc"}, or `1` for any other unhandled exception.
>
> If `PyConfig.inspect`{.interpreted-text role="c:member"} is set (such as when the `-i`{.interpreted-text role="option"} option is used), rather than returning when the interpreter exits, execution will instead resume in an interactive Python prompt (REPL) using the `__main__` module\'s global namespace. If the interpreter exited with an exception, it is immediately raised in the REPL session. The function return value is then determined by the way the *REPL session* terminates: `0`, `1`, or the status of a `SystemExit`{.interpreted-text role="exc"}, as specified above.
>
> This function always finalizes the Python interpreter before it returns.
>
> See `Python Configuration <init-python-config>`{.interpreted-text role="ref"} for an example of a customized Python that always runs in isolated mode using `Py_RunMain`{.interpreted-text role="c:func"}.

> Register an `atexit`{.interpreted-text role="mod"} callback for the target interpreter *interp*. This is similar to `Py_AtExit`{.interpreted-text role="c:func"}, but takes an explicit interpreter and data pointer for the callback.
>
> There must be an `attached thread state`{.interpreted-text role="term"} for *interp*.
>
> ::: versionadded
> 3.13
> :::

## Cautions regarding runtime finalization

In the late stage of `interpreter shutdown`{.interpreted-text role="term"}, after attempting to wait for non-daemon threads to exit (though this can be interrupted by `KeyboardInterrupt`{.interpreted-text role="class"}) and running the `atexit`{.interpreted-text role="mod"} functions, the runtime is marked as *finalizing*: `Py_IsFinalizing`{.interpreted-text role="c:func"} and `sys.is_finalizing`{.interpreted-text role="func"} return true. At this point, only the *finalization thread* that initiated finalization (typically the main thread) is allowed to acquire the `GIL`{.interpreted-text role="term"}.

If any thread, other than the finalization thread, attempts to attach a `thread state`{.interpreted-text role="term"} during finalization, either explicitly or implicitly, the thread enters **a permanently blocked state** where it remains until the program exits. In most cases this is harmless, but this can result in deadlock if a later stage of finalization attempts to acquire a lock owned by the blocked thread, or otherwise waits on the blocked thread.

Gross? Yes. This prevents random crashes and/or unexpectedly skipped C++ finalizations further up the call stack when such threads were forcibly exited here in CPython 3.13 and earlier. The CPython runtime `thread state`{.interpreted-text role="term"} C APIs have never had any error reporting or handling expectations at `thread state`{.interpreted-text role="term"} attachment time that would\'ve allowed for graceful exit from this situation. Changing that would require new stable C APIs and rewriting the majority of C code in the CPython ecosystem to use those with error handling.

## Process-wide parameters

> ::: index
> single: Py_Initialize() single: main()
> :::
>
> This API is kept for backward compatibility: setting `PyConfig.program_name`{.interpreted-text role="c:member"} should be used instead, see `Python
> Initialization Configuration <init-config>`{.interpreted-text role="ref"}.
>
> This function should be called before `Py_Initialize`{.interpreted-text role="c:func"} is called for the first time, if it is called at all. It tells the interpreter the value of the `argv[0]` argument to the `main`{.interpreted-text role="c:func"} function of the program (converted to wide characters). This is used by some other functions below to find the Python run-time libraries relative to the interpreter executable. The default value is `'python'`. The argument should point to a zero-terminated wide character string in static storage whose contents will not change for the duration of the program\'s execution. No code in the Python interpreter will change the contents of this storage.
>
> Use `Py_DecodeLocale`{.interpreted-text role="c:func"} to decode a bytes string to get a `wchar_t*`{.interpreted-text role="c:expr"} string.
>
> ::: deprecated-removed
> 3.11 3.15
> :::

> Return the version of this Python interpreter. This is a string that looks something like :
>
> ``` c
> "3.0a5+ (py3k:63103M, May 12 2008, 00:53:55) \n[GCC 4.2.3]"
> ```
>
> ::: index
> single: version (in module sys)
> :::
>
> The first word (up to the first space character) is the current Python version; the first characters are the major and minor version separated by a period. The returned string points into static storage; the caller should not modify its value. The value is available to Python code as `sys.version`{.interpreted-text role="data"}.
>
> See also the `Py_Version`{.interpreted-text role="c:var"} constant.

> ::: index
> single: platform (in module sys)
> :::
>
> Return the platform identifier for the current platform. On Unix, this is formed from the \"official\" name of the operating system, converted to lower case, followed by the major revision number; e.g., for Solaris 2.x, which is also known as SunOS 5.x, the value is `'sunos5'`. On macOS, it is `'darwin'`. On Windows, it is `'win'`. The returned string points into static storage; the caller should not modify its value. The value is available to Python code as `sys.platform`.

> Return the official copyright string for the current Python version, for example
>
> `'Copyright 1991-1995 Stichting Mathematisch Centrum, Amsterdam'`
>
> ::: index
> single: copyright (in module sys)
> :::
>
> The returned string points into static storage; the caller should not modify its value. The value is available to Python code as `sys.copyright`.

> Return an indication of the compiler used to build the current Python version, in square brackets, for example:
>
> ``` c
> "[GCC 2.7.2.2]"
> ```
>
> ::: index
> single: version (in module sys)
> :::
>
> The returned string points into static storage; the caller should not modify its value. The value is available to Python code as part of the variable `sys.version`.

> Return information about the sequence number and build date and time of the current Python interpreter instance, for example :
>
> ``` c
> "#67, Aug  1 1997, 22:34:28"
> ```
>
> ::: index
> single: version (in module sys)
> :::
>
> The returned string points into static storage; the caller should not modify its value. The value is available to Python code as part of the variable `sys.version`.

> ::: index
> single: main() single: Py_FatalError() single: argv (in module sys)
> :::
>
> This API is kept for backward compatibility: setting `PyConfig.argv`{.interpreted-text role="c:member"}, `PyConfig.parse_argv`{.interpreted-text role="c:member"} and `PyConfig.safe_path`{.interpreted-text role="c:member"} should be used instead, see `Python
> Initialization Configuration <init-config>`{.interpreted-text role="ref"}.
>
> Set `sys.argv`{.interpreted-text role="data"} based on *argc* and *argv*. These parameters are similar to those passed to the program\'s `main`{.interpreted-text role="c:func"} function with the difference that the first entry should refer to the script file to be executed rather than the executable hosting the Python interpreter. If there isn\'t a script that will be run, the first entry in *argv* can be an empty string. If this function fails to initialize `sys.argv`{.interpreted-text role="data"}, a fatal condition is signalled using `Py_FatalError`{.interpreted-text role="c:func"}.
>
> If *updatepath* is zero, this is all the function does. If *updatepath* is non-zero, the function also modifies `sys.path`{.interpreted-text role="data"} according to the following algorithm:
>
> - If the name of an existing script is passed in `argv[0]`, the absolute path of the directory where the script is located is prepended to `sys.path`{.interpreted-text role="data"}.
> - Otherwise (that is, if *argc* is `0` or `argv[0]` doesn\'t point to an existing file name), an empty string is prepended to `sys.path`{.interpreted-text role="data"}, which is the same as prepending the current working directory (`"."`).
>
> Use `Py_DecodeLocale`{.interpreted-text role="c:func"} to decode a bytes string to get a `wchar_t*`{.interpreted-text role="c:expr"} string.
>
> See also `PyConfig.orig_argv`{.interpreted-text role="c:member"} and `PyConfig.argv`{.interpreted-text role="c:member"} members of the `Python Initialization Configuration <init-config>`{.interpreted-text role="ref"}.
>
> :::: note
> ::: title
> Note
> :::
>
> It is recommended that applications embedding the Python interpreter for purposes other than executing a single script pass `0` as *updatepath*, and update `sys.path`{.interpreted-text role="data"} themselves if desired. See `2008-5983`{.interpreted-text role="cve"}.
>
> On versions before 3.1.3, you can achieve the same effect by manually popping the first `sys.path`{.interpreted-text role="data"} element after having called `PySys_SetArgv`{.interpreted-text role="c:func"}, for example using:
>
> ``` c
> PyRun_SimpleString("import sys; sys.path.pop(0)\n");
> ```
> ::::
>
> ::: versionadded
> 3.1.3
> :::
>
> ::: deprecated-removed
> 3.11 3.15
> :::

> This API is kept for backward compatibility: setting `PyConfig.argv`{.interpreted-text role="c:member"} and `PyConfig.parse_argv`{.interpreted-text role="c:member"} should be used instead, see `Python Initialization Configuration <init-config>`{.interpreted-text role="ref"}.
>
> This function works like `PySys_SetArgvEx`{.interpreted-text role="c:func"} with *updatepath* set to `1` unless the `python`{.interpreted-text role="program"} interpreter was started with the `-I`{.interpreted-text role="option"}.
>
> Use `Py_DecodeLocale`{.interpreted-text role="c:func"} to decode a bytes string to get a `wchar_t*`{.interpreted-text role="c:expr"} string.
>
> See also `PyConfig.orig_argv`{.interpreted-text role="c:member"} and `PyConfig.argv`{.interpreted-text role="c:member"} members of the `Python Initialization Configuration <init-config>`{.interpreted-text role="ref"}.
>
> ::: versionchanged
> 3.4 The *updatepath* value depends on `-I`{.interpreted-text role="option"}.
> :::
>
> ::: deprecated-removed
> 3.11 3.15
> :::

> This API is kept for backward compatibility: setting `PyConfig.home`{.interpreted-text role="c:member"} should be used instead, see `Python
> Initialization Configuration <init-config>`{.interpreted-text role="ref"}.
>
> Set the default \"home\" directory, that is, the location of the standard Python libraries. See `PYTHONHOME`{.interpreted-text role="envvar"} for the meaning of the argument string.
>
> The argument should point to a zero-terminated character string in static storage whose contents will not change for the duration of the program\'s execution. No code in the Python interpreter will change the contents of this storage.
>
> Use `Py_DecodeLocale`{.interpreted-text role="c:func"} to decode a bytes string to get a `wchar_t*`{.interpreted-text role="c:expr"} string.
>
> ::: deprecated-removed
> 3.11 3.15
> :::
