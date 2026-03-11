# Command line and environment {#using-on-general}

The CPython interpreter scans the command line and the environment for various settings.

::: impl-detail
Other implementations\' command line schemes may differ. See `implementations`{.interpreted-text role="ref"} for further resources.
:::

## Command line {#using-on-cmdline}

When invoking Python, you may specify any of these options:

``` sh
python [-bBdEhiIOPqRsSuvVWx?] [-c command | -m module-name | script | - ] [args]
```

The most common use case is, of course, a simple invocation of a script:

``` sh
python myscript.py
```

### Interface options {#using-on-interface-options}

The interpreter interface resembles that of the UNIX shell, but provides some additional methods of invocation:

- When called with standard input connected to a tty device, it prompts for commands and executes them until an EOF (an end-of-file character, you can produce that with `Ctrl-D`{.interpreted-text role="kbd"} on UNIX or `Ctrl-Z, Enter`{.interpreted-text role="kbd"} on Windows) is read. For more on interactive mode, see `tut-interac`{.interpreted-text role="ref"}.
- When called with a file name argument or with a file as standard input, it reads and executes a script from that file.
- When called with a directory name argument, it reads and executes an appropriately named script from that directory.
- When called with `-c command`, it executes the Python statement(s) given as *command*. Here *command* may contain multiple statements separated by newlines. Leading whitespace is significant in Python statements!
- When called with `-m module-name`, the given module is located on the Python module path and executed as a script.

In non-interactive mode, the entire input is parsed before it is executed.

An interface option terminates the list of options consumed by the interpreter, all consecutive arguments will end up in `sys.argv`{.interpreted-text role="data"} \-- note that the first element, subscript zero (`sys.argv[0]`), is a string reflecting the program\'s source.

::::: option

`-c <command>`

:   

Execute the Python code in *command*. *command* can be one or more statements separated by newlines, with significant leading whitespace as in normal module code.

If this option is given, the first element of `sys.argv`{.interpreted-text role="data"} will be `"-c"` and the current directory will be added to the start of `sys.path`{.interpreted-text role="data"} (allowing modules in that directory to be imported as top level modules).

::: audit-event
cpython.run_command command cmdoption-c
:::

::: versionchanged
3.14 *command* is automatically dedented before execution.
:::
:::::

::::::::: option

`-m <module-name>`

:   

Search `sys.path`{.interpreted-text role="data"} for the named module and execute its contents as the `__main__`{.interpreted-text role="mod"} module.

Since the argument is a *module* name, you must not give a file extension (`.py`). The module name should be a valid absolute Python module name, but the implementation may not always enforce this (e.g. it may allow you to use a name that includes a hyphen).

Package names (including namespace packages) are also permitted. When a package name is supplied instead of a normal module, the interpreter will execute `<pkg>.__main__` as the main module. This behaviour is deliberately similar to the handling of directories and zipfiles that are passed to the interpreter as the script argument.

:::: note
::: title
Note
:::

This option cannot be used with built-in modules and extension modules written in C, since they do not have Python module files. However, it can still be used for precompiled modules, even if the original source file is not available.
::::

If this option is given, the first element of `sys.argv`{.interpreted-text role="data"} will be the full path to the module file (while the module file is being located, the first element will be set to `"-m"`). As with the `-c`{.interpreted-text role="option"} option, the current directory will be added to the start of `sys.path`{.interpreted-text role="data"}.

`-I`{.interpreted-text role="option"} option can be used to run the script in isolated mode where `sys.path`{.interpreted-text role="data"} contains neither the current directory nor the user\'s site-packages directory. All `PYTHON*` environment variables are ignored, too.

Many standard library modules contain code that is invoked on their execution as a script. An example is the `timeit`{.interpreted-text role="mod"} module:

``` sh
python -m timeit -s "setup here" "benchmarked code here"
python -m timeit -h # for details
```

::: audit-event
cpython.run_module module-name cmdoption-m
:::

::: seealso
`runpy.run_module`{.interpreted-text role="func"} Equivalent functionality directly available to Python code

`338`{.interpreted-text role="pep"} \-- Executing modules as scripts
:::

::: versionchanged
3.1 Supply the package name to run a `__main__` submodule.
:::

::: versionchanged
3.4 namespace packages are also supported
:::
:::::::::

::::: {#cmdarg-dash}
:::: describe
- 

Read commands from standard input (`sys.stdin`{.interpreted-text role="data"}). If standard input is a terminal, `-i`{.interpreted-text role="option"} is implied.

If this option is given, the first element of `sys.argv`{.interpreted-text role="data"} will be `"-"` and the current directory will be added to the start of `sys.path`{.interpreted-text role="data"}.

::: audit-event
cpython.run_stdin \"\" \"\"
:::
::::
:::::

:::::: {#cmdarg-script}
::::: describe
\<script\>

Execute the Python code contained in *script*, which must be a filesystem path (absolute or relative) referring to either a Python file, a directory containing a `__main__.py` file, or a zipfile containing a `__main__.py` file.

If this option is given, the first element of `sys.argv`{.interpreted-text role="data"} will be the script name as given on the command line.

If the script name refers directly to a Python file, the directory containing that file is added to the start of `sys.path`{.interpreted-text role="data"}, and the file is executed as the `__main__`{.interpreted-text role="mod"} module.

If the script name refers to a directory or zipfile, the script name is added to the start of `sys.path`{.interpreted-text role="data"} and the `__main__.py` file in that location is executed as the `__main__`{.interpreted-text role="mod"} module.

`-I`{.interpreted-text role="option"} option can be used to run the script in isolated mode where `sys.path`{.interpreted-text role="data"} contains neither the script\'s directory nor the user\'s site-packages directory. All `PYTHON*` environment variables are ignored, too.

::: audit-event
cpython.run_file filename
:::

::: seealso
`runpy.run_path`{.interpreted-text role="func"} Equivalent functionality directly available to Python code
:::
:::::
::::::

If no interface option is given, `-i`{.interpreted-text role="option"} is implied, `sys.argv[0]` is an empty string (`""`) and the current directory will be added to the start of `sys.path`{.interpreted-text role="data"}. Also, tab-completion and history editing is automatically enabled, if available on your platform (see `rlcompleter-config`{.interpreted-text role="ref"}).

::: seealso
`tut-invoking`{.interpreted-text role="ref"}
:::

::: versionchanged
3.4 Automatic enabling of tab-completion and history editing.
:::

### Generic options {#using-on-generic-options}

::: option
-? -h \--help

Print a short description of all command line options and corresponding environment variables and exit.
:::

:::: option

`--help-env`

:   

Print a short description of Python-specific environment variables and exit.

::: versionadded
3.11
:::
::::

:::: option

`--help-xoptions`

:   

Print a description of implementation-specific `-X`{.interpreted-text role="option"} options and exit.

::: versionadded
3.11
:::
::::

:::: option

`--help-all`

:   

Print complete usage information and exit.

::: versionadded
3.11
:::
::::

:::: option

`-V`

:   

`--version`

:   

Print the Python version number and exit. Example output could be:

``` none
Python 3.8.0b2+
```

When given twice, print more information about the build, like:

``` none
Python 3.8.0b2+ (3.8:0c076caaa8, Apr 20 2019, 21:55:00)
[GCC 6.2.0 20161005]
```

::: versionadded
3.6 The `-VV` option.
:::
::::

### Miscellaneous options {#using-on-misc-options}

::::: option

`-b`

:   

Issue a warning when converting `bytes`{.interpreted-text role="class"} or `bytearray`{.interpreted-text role="class"} to `str`{.interpreted-text role="class"} without specifying encoding or comparing `!bytes`{.interpreted-text role="class"} or `!bytearray`{.interpreted-text role="class"} with `!str`{.interpreted-text role="class"} or `!bytes`{.interpreted-text role="class"} with `int`{.interpreted-text role="class"}. Issue an error when the option is given twice (`!-bb`{.interpreted-text role="option"}).

::: versionchanged
3.5 Affects also comparisons of `bytes`{.interpreted-text role="class"} with `int`{.interpreted-text role="class"}.
:::

::: deprecated
3.15

Deprecate `-b`{.interpreted-text role="option"} and `!-bb`{.interpreted-text role="option"} command line options and schedule them to become no-op in Python 3.17. These were primarily helpers for the Python 2 -\> 3 transition. Starting with Python 3.17, no `BytesWarning`{.interpreted-text role="exc"} will be raised for these cases; use a type checker instead.
:::
:::::

::: option

`-B`

:   

If given, Python won\'t try to write `.pyc` files on the import of source modules. See also `PYTHONDONTWRITEBYTECODE`{.interpreted-text role="envvar"}.
:::

::: option
\--check-hash-based-pycs default[\|always\|](##SUBST##|always|)never

Control the validation behavior of hash-based `.pyc` files. See `pyc-invalidation`{.interpreted-text role="ref"}. When set to `default`, checked and unchecked hash-based bytecode cache files are validated according to their default semantics. When set to `always`, all hash-based `.pyc` files, whether checked or unchecked, are validated against their corresponding source file. When set to `never`, hash-based `.pyc` files are not validated against their corresponding source files.

The semantics of timestamp-based `.pyc` files are unaffected by this option.
:::

::: option

`-d`

:   

Turn on parser debugging output (for expert only). See also the `PYTHONDEBUG`{.interpreted-text role="envvar"} environment variable.

This option requires a `debug build of Python <debug-build>`{.interpreted-text role="ref"}, otherwise it\'s ignored.
:::

::: option

`-E`

:   

Ignore all `PYTHON*` environment variables, e.g. `PYTHONPATH`{.interpreted-text role="envvar"} and `PYTHONHOME`{.interpreted-text role="envvar"}, that might be set.

See also the `-P`{.interpreted-text role="option"} and `-I`{.interpreted-text role="option"} (isolated) options.
:::

::: option

`-i`

:   

Enter interactive mode after execution.

Using the `-i`{.interpreted-text role="option"} option will enter interactive mode in any of the following circumstances:

- When a script is passed as first argument
- When the `-c`{.interpreted-text role="option"} option is used
- When the `-m`{.interpreted-text role="option"} option is used

Interactive mode will start even when `sys.stdin`{.interpreted-text role="data"} does not appear to be a terminal. The `PYTHONSTARTUP`{.interpreted-text role="envvar"} file is not read.

This can be useful to inspect global variables or a stack trace when a script raises an exception. See also `PYTHONINSPECT`{.interpreted-text role="envvar"}.
:::

:::: option

`-I`

:   

Run Python in isolated mode. This also implies `-E`{.interpreted-text role="option"}, `-P`{.interpreted-text role="option"} and `-s`{.interpreted-text role="option"} options.

In isolated mode `sys.path`{.interpreted-text role="data"} contains neither the script\'s directory nor the user\'s site-packages directory. All `PYTHON*` environment variables are ignored, too. Further restrictions may be imposed to prevent the user from injecting malicious code.

::: versionadded
3.4
:::
::::

:::: option

`-O`

:   

Remove assert statements and any code conditional on the value of `__debug__`{.interpreted-text role="const"}. Augment the filename for compiled (`bytecode`{.interpreted-text role="term"}) files by adding `.opt-1` before the `.pyc` extension (see `488`{.interpreted-text role="pep"}). See also `PYTHONOPTIMIZE`{.interpreted-text role="envvar"}.

::: versionchanged
3.5 Modify `.pyc` filenames according to `488`{.interpreted-text role="pep"}.
:::
::::

:::: option

`-OO`

:   

Do `-O`{.interpreted-text role="option"} and also discard docstrings. Augment the filename for compiled (`bytecode`{.interpreted-text role="term"}) files by adding `.opt-2` before the `.pyc` extension (see `488`{.interpreted-text role="pep"}).

::: versionchanged
3.5 Modify `.pyc` filenames according to `488`{.interpreted-text role="pep"}.
:::
::::

:::: option

`-P`

:   

Don\'t prepend a potentially unsafe path to `sys.path`{.interpreted-text role="data"}:

- `python -m module` command line: Don\'t prepend the current working directory.
- `python script.py` command line: Don\'t prepend the script\'s directory. If it\'s a symbolic link, resolve symbolic links.
- `python -c code` and `python` (REPL) command lines: Don\'t prepend an empty string, which means the current working directory.

See also the `PYTHONSAFEPATH`{.interpreted-text role="envvar"} environment variable, and `-E`{.interpreted-text role="option"} and `-I`{.interpreted-text role="option"} (isolated) options.

::: versionadded
3.11
:::
::::

:::: option

`-q`

:   

Don\'t display the copyright and version messages even in interactive mode.

::: versionadded
3.2
:::
::::

::::: option

`-R`

:   

Turn on hash randomization. This option only has an effect if the `PYTHONHASHSEED`{.interpreted-text role="envvar"} environment variable is set to anything other than `random`, since hash randomization is enabled by default.

On previous versions of Python, this option turns on hash randomization, so that the `~object.__hash__`{.interpreted-text role="meth"} values of str and bytes objects are \"salted\" with an unpredictable random value. Although they remain constant within an individual Python process, they are not predictable between repeated invocations of Python.

Hash randomization is intended to provide protection against a denial-of-service caused by carefully chosen inputs that exploit the worst case performance of a dict construction, *O*(*n*^2^) complexity. See <http://ocert.org/advisories/ocert-2011-003.html> for details.

`PYTHONHASHSEED`{.interpreted-text role="envvar"} allows you to set a fixed value for the hash seed secret.

::: versionadded
3.2.3
:::

::: versionchanged
3.7 The option is no longer ignored.
:::
:::::

:::: option

`-s`

:   

Don\'t add the `user site-packages directory <site.USER_SITE>`{.interpreted-text role="data"} to `sys.path`{.interpreted-text role="data"}.

See also `PYTHONNOUSERSITE`{.interpreted-text role="envvar"}.

::: seealso
`370`{.interpreted-text role="pep"} \-- Per user site-packages directory
:::
::::

::: option

`-S`

:   

Disable the import of the module `site`{.interpreted-text role="mod"} and the site-dependent manipulations of `sys.path`{.interpreted-text role="data"} that it entails. Also disable these manipulations if `site`{.interpreted-text role="mod"} is explicitly imported later (call `site.main`{.interpreted-text role="func"} if you want them to be triggered).
:::

:::: option

`-u`

:   

Force the stdout and stderr streams to be unbuffered. This option has no effect on the stdin stream.

See also `PYTHONUNBUFFERED`{.interpreted-text role="envvar"}.

::: versionchanged
3.7 The text layer of the stdout and stderr streams now is unbuffered.
:::
::::

:::: option

`-v`

:   

Print a message each time a module is initialized, showing the place (filename or built-in module) from which it is loaded. When given twice (`!-vv`{.interpreted-text role="option"}), print a message for each file that is checked for when searching for a module. Also provides information on module cleanup at exit.

::: versionchanged
3.10 The `site`{.interpreted-text role="mod"} module reports the site-specific paths and `.pth`{.interpreted-text role="file"} files being processed.
:::

See also `PYTHONVERBOSE`{.interpreted-text role="envvar"}.
::::

> Warning control. Python\'s warning machinery by default prints warning messages to `sys.stderr`{.interpreted-text role="data"}.
>
> The simplest settings apply a particular action unconditionally to all warnings emitted by a process (even those that are otherwise ignored by default):
>
> ``` sh
> -Wdefault  # Warn once per call location
> -Werror    # Convert to exceptions
> -Walways   # Warn every time
> -Wall      # Same as -Walways
> -Wmodule   # Warn once per calling module
> -Wonce     # Warn once per Python process
> -Wignore   # Never warn
> ```
>
> The action names can be abbreviated as desired and the interpreter will resolve them to the appropriate action name. For example, `-Wi` is the same as `-Wignore`.
>
> The full form of argument is:
>
> ``` sh
> action:message:category:module:lineno
> ```
>
> Empty fields match all values; trailing empty fields may be omitted. For example `-W ignore::DeprecationWarning` ignores all DeprecationWarning warnings.
>
> The *action* field is as explained above but only applies to warnings that match the remaining fields.
>
> The *message* field must match the start of the warning message; this match is case-insensitive. If it starts and ends with a forward slash (`/`), it specifies a regular expression, otherwise it specifies a literal string.
>
> The *category* field matches the warning category (ex: `DeprecationWarning`). This must be a class name; the match test whether the actual warning category of the message is a subclass of the specified warning category.
>
> The *module* field matches the (fully qualified) module name; this match is case-sensitive. If it starts and ends with a forward slash (`/`), it specifies a regular expression that the start of the fully qualified module name must match, otherwise it specifies a literal string that the fully qualified module name must be equal to.
>
> The *lineno* field matches the line number, where zero matches all line numbers and is thus equivalent to an omitted line number.
>
> Multiple `-W`{.interpreted-text role="option"} options can be given; when a warning matches more than one option, the action for the last matching option is performed. Invalid `-W`{.interpreted-text role="option"} options are ignored (though, a warning message is printed about invalid options when the first warning is issued).
>
> Warnings can also be controlled using the `PYTHONWARNINGS`{.interpreted-text role="envvar"} environment variable and from within a Python program using the `warnings`{.interpreted-text role="mod"} module. For example, the `warnings.filterwarnings`{.interpreted-text role="func"} function can be used to use a regular expression on the warning message.
>
> See `warning-filter`{.interpreted-text role="ref"} and `describing-warning-filters`{.interpreted-text role="ref"} for more details.
>
> ::: versionchanged
> 3.15 Added regular expression support for *message* and *module*.
> :::

::: option

`-x`

:   

Skip the first line of the source, allowing use of non-Unix forms of `#!cmd`. This is intended for a DOS specific hack only.
:::

:::::: option

`-X`

:   

Reserved for various implementation-specific options. CPython currently defines the following possible values:

- `-X faulthandler` to enable `faulthandler`{.interpreted-text role="mod"}. See also `PYTHONFAULTHANDLER`{.interpreted-text role="envvar"}.

  ::: versionadded
  3.3
  :::

- `-X showrefcount` to output the total reference count and number of used memory blocks when the program finishes or after each statement in the interactive interpreter. This only works on `debug builds
  <debug-build>`{.interpreted-text role="ref"}.

  ::: versionadded
  3.4
  :::

- `-X tracemalloc` to start tracing Python memory allocations using the `tracemalloc`{.interpreted-text role="mod"} module. By default, only the most recent frame is stored in a traceback of a trace. Use `-X tracemalloc=NFRAME` to start tracing with a traceback limit of *NFRAME* frames. See `tracemalloc.start`{.interpreted-text role="func"} and `PYTHONTRACEMALLOC`{.interpreted-text role="envvar"} for more information.

  ::: versionadded
  3.4
  :::

- `-X int_max_str_digits` configures the `integer string conversion
  length limitation <int_max_str_digits>`{.interpreted-text role="ref"}. See also `PYTHONINTMAXSTRDIGITS`{.interpreted-text role="envvar"}.

  ::: versionadded
  3.11
  :::

- `-X importtime` to show how long each import takes. It shows module name, cumulative time (including nested imports) and self time (excluding nested imports). Note that its output may be broken in multi-threaded application. Typical usage is `python -X importtime -c 'import asyncio'`.

  `-X importtime=2` enables additional output that indicates when an imported module has already been loaded. In such cases, the string `cached` will be printed in both time columns.

  See also `PYTHONPROFILEIMPORTTIME`{.interpreted-text role="envvar"}.

  ::: versionadded
  3.7
  :::

  ::: versionchanged
  3.14

  Added `-X importtime=2` to also trace imports of loaded modules, and reserved values other than `1` and `2` for future use.
  :::

- `-X dev`: enable `Python Development Mode <devmode>`{.interpreted-text role="ref"}, introducing additional runtime checks that are too expensive to be enabled by default. See also `PYTHONDEVMODE`{.interpreted-text role="envvar"}.

  ::: versionadded
  3.7
  :::

- `-X utf8` enables the `Python UTF-8 Mode <utf8-mode>`{.interpreted-text role="ref"}. `-X utf8=0` explicitly disables `Python UTF-8 Mode <utf8-mode>`{.interpreted-text role="ref"} (even when it would otherwise activate automatically). See also `PYTHONUTF8`{.interpreted-text role="envvar"}.

  ::: versionadded
  3.7
  :::

- `-X pycache_prefix=PATH` enables writing `.pyc` files to a parallel tree rooted at the given directory instead of to the code tree. See also `PYTHONPYCACHEPREFIX`{.interpreted-text role="envvar"}.

  ::: versionadded
  3.8
  :::

- `-X warn_default_encoding` issues a `EncodingWarning`{.interpreted-text role="class"} when the locale-specific default encoding is used for opening files. See also `PYTHONWARNDEFAULTENCODING`{.interpreted-text role="envvar"}.

  ::: versionadded
  3.10
  :::

- `-X no_debug_ranges` disables the inclusion of the tables mapping extra location information (end line, start column offset and end column offset) to every instruction in code objects. This is useful when smaller code objects and pyc files are desired as well as suppressing the extra visual location indicators when the interpreter displays tracebacks. See also `PYTHONNODEBUGRANGES`{.interpreted-text role="envvar"}.

  ::: versionadded
  3.11
  :::

- `-X frozen_modules` determines whether or not frozen modules are ignored by the import machinery. A value of `on` means they get imported and `off` means they are ignored. The default is `on` if this is an installed Python (the normal case). If it\'s under development (running from the source tree) then the default is `off`. Note that the `!importlib_bootstrap`{.interpreted-text role="mod"} and `!importlib_bootstrap_external`{.interpreted-text role="mod"} frozen modules are always used, even if this flag is set to `off`. See also `PYTHON_FROZEN_MODULES`{.interpreted-text role="envvar"}.

  ::: versionadded
  3.11
  :::

- `-X perf` enables support for the Linux `perf` profiler. When this option is provided, the `perf` profiler will be able to report Python calls. This option is only available on some platforms and will do nothing if is not supported on the current system. The default value is \"off\". See also `PYTHONPERFSUPPORT`{.interpreted-text role="envvar"} and `perf_profiling`{.interpreted-text role="ref"}.

  ::: versionadded
  3.12
  :::

- `-X perf_jit` enables support for the Linux `perf` profiler with DWARF support. When this option is provided, the `perf` profiler will be able to report Python calls using DWARF information. This option is only available on some platforms and will do nothing if is not supported on the current system. The default value is \"off\". See also `PYTHON_PERF_JIT_SUPPORT`{.interpreted-text role="envvar"} and `perf_profiling`{.interpreted-text role="ref"}.

  ::: versionadded
  3.13
  :::

- `-X disable_remote_debug` disables the remote debugging support as described in `768`{.interpreted-text role="pep"}. This includes both the functionality to schedule code for execution in another process and the functionality to receive code for execution in the current process.

  This option is only available on some platforms and will do nothing if is not supported on the current system. See also `PYTHON_DISABLE_REMOTE_DEBUG`{.interpreted-text role="envvar"} and `768`{.interpreted-text role="pep"}.

  ::: versionadded
  3.14
  :::

- `-X cpu_count={n}`{.interpreted-text role="samp"} overrides `os.cpu_count`{.interpreted-text role="func"}, `os.process_cpu_count`{.interpreted-text role="func"}, and `multiprocessing.cpu_count`{.interpreted-text role="func"}. *n* must be greater than or equal to 1. This option may be useful for users who need to limit CPU resources of a container system. See also `PYTHON_CPU_COUNT`{.interpreted-text role="envvar"}. If *n* is `default`, nothing is overridden.

  ::: versionadded
  3.13
  :::

- `-X presite={package.module}`{.interpreted-text role="samp"} specifies a module that should be imported before the `site`{.interpreted-text role="mod"} module is executed and before the `__main__`{.interpreted-text role="mod"} module exists. Therefore, the imported module isn\'t `__main__`{.interpreted-text role="mod"}. This can be used to execute code early during Python initialization. Python needs to be `built in debug mode <debug-build>`{.interpreted-text role="ref"} for this option to exist. See also `PYTHON_PRESITE`{.interpreted-text role="envvar"}.

  ::: versionadded
  3.13
  :::

- `-X gil={0,1}`{.interpreted-text role="samp"} forces the GIL to be disabled or enabled, respectively. Setting to `0` is only available in builds configured with `--disable-gil`{.interpreted-text role="option"}. See also `PYTHON_GIL`{.interpreted-text role="envvar"} and `whatsnew313-free-threaded-cpython`{.interpreted-text role="ref"}.

  ::: versionadded
  3.13
  :::

- `-X thread_inherit_context={0,1}`{.interpreted-text role="samp"} causes `~threading.Thread`{.interpreted-text role="class"} to, by default, use a copy of context of the caller of `Thread.start()` when starting. Otherwise, threads will start with an empty context. If unset, the value of this option defaults to `1` on free-threaded builds and to `0` otherwise. See also `PYTHON_THREAD_INHERIT_CONTEXT`{.interpreted-text role="envvar"}.

  ::: versionadded
  3.14
  :::

- `-X context_aware_warnings={0,1}`{.interpreted-text role="samp"} causes the `warnings.catch_warnings`{.interpreted-text role="class"} context manager to use a `~contextvars.ContextVar`{.interpreted-text role="class"} to store warnings filter state. If unset, the value of this option defaults to `1` on free-threaded builds and to `0` otherwise. See also `PYTHON_CONTEXT_AWARE_WARNINGS`{.interpreted-text role="envvar"}.

  ::: versionadded
  3.14
  :::

- `-X tlbc={0,1}`{.interpreted-text role="samp"} enables (1, the default) or disables (0) thread-local bytecode in builds configured with `--disable-gil`{.interpreted-text role="option"}. When disabled, this also disables the specializing interpreter. See also `PYTHON_TLBC`{.interpreted-text role="envvar"}.

  ::: versionadded
  3.14
  :::

- `-X lazy_imports={all,none,normal}`{.interpreted-text role="samp"} controls lazy import behavior. `all` makes all imports lazy by default, `none` disables lazy imports entirely (even explicit `lazy` statements become eager), and `normal` (the default) respects the `lazy` keyword in source code. See also `PYTHON_LAZY_IMPORTS`{.interpreted-text role="envvar"}.

  ::: versionadded
  next
  :::

It also allows passing arbitrary values and retrieving them through the `sys._xoptions`{.interpreted-text role="data"} dictionary.

::: versionadded
3.2
:::

::: versionchanged
3.9 Removed the `-X showalloccount` option.
:::

::: versionchanged
3.10 Removed the `-X oldparser` option.
:::
::::::

::: versionremoved
3.14

`!-J`{.interpreted-text role="option"} is no longer reserved for use by [Jython](https://www.jython.org/), and now has no special meaning.
:::

### Controlling color {#using-on-controlling-color}

The Python interpreter is configured by default to use colors to highlight output in certain situations such as when displaying tracebacks. This behavior can be controlled by setting different environment variables.

Setting the environment variable `TERM` to `dumb` will disable color.

If the [[\|FORCE_COLOR\|](##SUBST##|FORCE_COLOR|)]() environment variable is set, then color will be enabled regardless of the value of TERM. This is useful on CI systems which aren't terminals but can still display ANSI escape sequences.

If the [[\|NO_COLOR\|](##SUBST##|NO_COLOR|)]() environment variable is set, Python will disable all color in the output. This takes precedence over `FORCE_COLOR`.

All these environment variables are used also by other tools to control color output. To control the color output only in the Python interpreter, the `PYTHON_COLORS`{.interpreted-text role="envvar"} environment variable can be used. This variable takes precedence over `NO_COLOR`, which in turn takes precedence over `FORCE_COLOR`.

## Environment variables {#using-on-envvars}

These environment variables influence Python\'s behavior, they are processed before the command-line switches other than -E or -I. It is customary that command-line switches override environmental variables where there is a conflict.

::: envvar
PYTHONHOME

Change the location of the standard Python libraries. By default, the libraries are searched in `{prefix}/lib/python{version}`{.interpreted-text role="file"} and `{exec_prefix}/lib/python{version}`{.interpreted-text role="file"}, where `{prefix}`{.interpreted-text role="file"} and `{exec_prefix}`{.interpreted-text role="file"} are installation-dependent directories, both defaulting to `/usr/local`{.interpreted-text role="file"}.

When `PYTHONHOME`{.interpreted-text role="envvar"} is set to a single directory, its value replaces both `{prefix}`{.interpreted-text role="file"} and `{exec_prefix}`{.interpreted-text role="file"}. To specify different values for these, set `PYTHONHOME`{.interpreted-text role="envvar"} to `{prefix}:{exec_prefix}`{.interpreted-text role="file"}.
:::

::: envvar
PYTHONPATH

Augment the default search path for module files. The format is the same as the shell\'s `PATH`{.interpreted-text role="envvar"}: one or more directory pathnames separated by `os.pathsep`{.interpreted-text role="data"} (e.g. colons on Unix or semicolons on Windows). Non-existent directories are silently ignored.

In addition to normal directories, individual `PYTHONPATH`{.interpreted-text role="envvar"} entries may refer to zipfiles containing pure Python modules (in either source or compiled form). Extension modules cannot be imported from zipfiles.

The default search path is installation dependent, but generally begins with `{prefix}/lib/python{version}`{.interpreted-text role="file"} (see `PYTHONHOME`{.interpreted-text role="envvar"} above). It is *always* appended to `PYTHONPATH`{.interpreted-text role="envvar"}.

An additional directory will be inserted in the search path in front of `PYTHONPATH`{.interpreted-text role="envvar"} as described above under `using-on-interface-options`{.interpreted-text role="ref"}. The search path can be manipulated from within a Python program as the variable `sys.path`{.interpreted-text role="data"}.
:::

:::: envvar
PYTHONSAFEPATH

If this is set to a non-empty string, don\'t prepend a potentially unsafe path to `sys.path`{.interpreted-text role="data"}: see the `-P`{.interpreted-text role="option"} option for details.

::: versionadded
3.11
:::
::::

:::: envvar
PYTHONPLATLIBDIR

If this is set to a non-empty string, it overrides the `sys.platlibdir`{.interpreted-text role="data"} value.

::: versionadded
3.9
:::
::::

:::: envvar
PYTHONSTARTUP

If this is the name of a readable file, the Python commands in that file are executed before the first prompt is displayed in interactive mode. The file is executed in the same namespace where interactive commands are executed so that objects defined or imported in it can be used without qualification in the interactive session. You can also change the prompts `sys.ps1`{.interpreted-text role="data"} and `sys.ps2`{.interpreted-text role="data"} and the hook `sys.__interactivehook__`{.interpreted-text role="data"} in this file.

::: audit-event
cpython.run_startup filename envvar-PYTHONSTARTUP

Raises an `auditing event <auditing>`{.interpreted-text role="ref"} `cpython.run_startup` with the filename as the argument when called on startup.
:::
::::

::: envvar
PYTHONOPTIMIZE

If this is set to a non-empty string it is equivalent to specifying the `-O`{.interpreted-text role="option"} option. If set to an integer, it is equivalent to specifying `-O`{.interpreted-text role="option"} multiple times.
:::

:::: envvar
PYTHONBREAKPOINT

If this is set, it names a callable using dotted-path notation. The module containing the callable will be imported and then the callable will be run by the default implementation of `sys.breakpointhook`{.interpreted-text role="func"} which itself is called by built-in `breakpoint`{.interpreted-text role="func"}. If not set, or set to the empty string, it is equivalent to the value \"pdb.set_trace\". Setting this to the string \"0\" causes the default implementation of `sys.breakpointhook`{.interpreted-text role="func"} to do nothing but return immediately.

::: versionadded
3.7
:::
::::

::: envvar
PYTHONDEBUG

If this is set to a non-empty string it is equivalent to specifying the `-d`{.interpreted-text role="option"} option. If set to an integer, it is equivalent to specifying `-d`{.interpreted-text role="option"} multiple times.

This environment variable requires a `debug build of Python
<debug-build>`{.interpreted-text role="ref"}, otherwise it\'s ignored.
:::

:::::: envvar
PYTHONINSPECT

If this is set to a non-empty string it is equivalent to specifying the `-i`{.interpreted-text role="option"} option.

This variable can also be modified by Python code using `os.environ`{.interpreted-text role="data"} to force inspect mode on program termination.

::: audit-event
cpython.run_stdin \"\" \"\"
:::

::: versionchanged
3.12.5 (also 3.11.10, 3.10.15, 3.9.20, and 3.8.20) Emits audit events.
:::

::: versionchanged
3.13 Uses PyREPL if possible, in which case `PYTHONSTARTUP`{.interpreted-text role="envvar"} is also executed. Emits audit events.
:::
::::::

::: envvar
PYTHONUNBUFFERED

If this is set to a non-empty string it is equivalent to specifying the `-u`{.interpreted-text role="option"} option.
:::

::: envvar
PYTHONVERBOSE

If this is set to a non-empty string it is equivalent to specifying the `-v`{.interpreted-text role="option"} option. If set to an integer, it is equivalent to specifying `-v`{.interpreted-text role="option"} multiple times.
:::

::: envvar
PYTHONCASEOK

If this is set, Python ignores case in `import`{.interpreted-text role="keyword"} statements. This only works on Windows and macOS.
:::

::: envvar
PYTHONDONTWRITEBYTECODE

If this is set to a non-empty string, Python won\'t try to write `.pyc` files on the import of source modules. This is equivalent to specifying the `-B`{.interpreted-text role="option"} option.
:::

:::: envvar
PYTHONPYCACHEPREFIX

If this is set, Python will write `.pyc` files in a mirror directory tree at this path, instead of in `__pycache__` directories within the source tree. This is equivalent to specifying the `-X`{.interpreted-text role="option"} `pycache_prefix=PATH` option.

::: versionadded
3.8
:::
::::

:::: envvar
PYTHONHASHSEED

If this variable is not set or set to `random`, a random value is used to seed the hashes of str and bytes objects.

If `PYTHONHASHSEED`{.interpreted-text role="envvar"} is set to an integer value, it is used as a fixed seed for generating the hash() of the types covered by the hash randomization.

Its purpose is to allow repeatable hashing, such as for selftests for the interpreter itself, or to allow a cluster of python processes to share hash values.

The integer must be a decimal number in the range \[0,4294967295\]. Specifying the value 0 will disable hash randomization.

::: versionadded
3.2.3
:::
::::

:::: envvar
PYTHONINTMAXSTRDIGITS

If this variable is set to an integer, it is used to configure the interpreter\'s global `integer string conversion length limitation
<int_max_str_digits>`{.interpreted-text role="ref"}.

::: versionadded
3.11
:::
::::

::::: envvar
PYTHONIOENCODING

If this is set before running the interpreter, it overrides the encoding used for stdin/stdout/stderr, in the syntax `encodingname:errorhandler`. Both the `encodingname` and the `:errorhandler` parts are optional and have the same meaning as in `str.encode`{.interpreted-text role="func"}.

For stderr, the `:errorhandler` part is ignored; the handler will always be `'backslashreplace'`.

::: versionchanged
3.4 The `encodingname` part is now optional.
:::

::: versionchanged
3.6 On Windows, the encoding specified by this variable is ignored for interactive console buffers unless `PYTHONLEGACYWINDOWSSTDIO`{.interpreted-text role="envvar"} is also specified. Files and pipes redirected through the standard streams are not affected.
:::
:::::

:::: envvar
PYTHONNOUSERSITE

If this is set, Python won\'t add the `user site-packages directory
<site.USER_SITE>`{.interpreted-text role="data"} to `sys.path`{.interpreted-text role="data"}.

::: seealso
`370`{.interpreted-text role="pep"} \-- Per user site-packages directory
:::
::::

:::: envvar
PYTHONUSERBASE

Defines the `user base directory <site.USER_BASE>`{.interpreted-text role="data"}, which is used to compute the path of the `user site-packages directory <site.USER_SITE>`{.interpreted-text role="data"} and `installation paths <sysconfig-user-scheme>`{.interpreted-text role="ref"} for `python -m pip install --user`.

::: seealso
`370`{.interpreted-text role="pep"} \-- Per user site-packages directory
:::
::::

::: envvar
PYTHONEXECUTABLE

If this environment variable is set, `sys.argv[0]` will be set to its value instead of the value got through the C runtime. Only works on macOS.
:::

:::: envvar
PYTHONWARNINGS

This is equivalent to the `-W`{.interpreted-text role="option"} option. If set to a comma separated string, it is equivalent to specifying `-W`{.interpreted-text role="option"} multiple times, with filters later in the list taking precedence over those earlier in the list.

The simplest settings apply a particular action unconditionally to all warnings emitted by a process (even those that are otherwise ignored by default):

``` sh
PYTHONWARNINGS=default  # Warn once per call location
PYTHONWARNINGS=error    # Convert to exceptions
PYTHONWARNINGS=always   # Warn every time
PYTHONWARNINGS=all      # Same as PYTHONWARNINGS=always
PYTHONWARNINGS=module   # Warn once per calling module
PYTHONWARNINGS=once     # Warn once per Python process
PYTHONWARNINGS=ignore   # Never warn
```

See `warning-filter`{.interpreted-text role="ref"} and `describing-warning-filters`{.interpreted-text role="ref"} for more details.

::: versionchanged
3.15 Added regular expression support for *message* and *module*.
:::
::::

:::: envvar
PYTHONFAULTHANDLER

If this environment variable is set to a non-empty string, `faulthandler.enable`{.interpreted-text role="func"} is called at startup: install a handler for `~signal.SIGSEGV`{.interpreted-text role="const"}, `~signal.SIGFPE`{.interpreted-text role="const"}, `~signal.SIGABRT`{.interpreted-text role="const"}, `~signal.SIGBUS`{.interpreted-text role="const"} and `~signal.SIGILL`{.interpreted-text role="const"} signals to dump the Python traceback. This is equivalent to `-X`{.interpreted-text role="option"} `faulthandler` option.

::: versionadded
3.3
:::
::::

:::: envvar
PYTHONTRACEMALLOC

If this environment variable is set to a non-empty string, start tracing Python memory allocations using the `tracemalloc`{.interpreted-text role="mod"} module. The value of the variable is the maximum number of frames stored in a traceback of a trace. For example, `PYTHONTRACEMALLOC=1` stores only the most recent frame. See the `tracemalloc.start`{.interpreted-text role="func"} function for more information. This is equivalent to setting the `-X`{.interpreted-text role="option"} `tracemalloc` option.

::: versionadded
3.4
:::
::::

::::: envvar
PYTHONPROFILEIMPORTTIME

If this environment variable is set to `1`, Python will show how long each import takes. If set to `2`, Python will include output for imported modules that have already been loaded. This is equivalent to setting the `-X`{.interpreted-text role="option"} `importtime` option.

::: versionadded
3.7
:::

::: versionchanged
3.14

Added `PYTHONPROFILEIMPORTTIME=2` to also trace imports of loaded modules.
:::
:::::

:::: envvar
PYTHONASYNCIODEBUG

If this environment variable is set to a non-empty string, enable the `debug mode <asyncio-debug-mode>`{.interpreted-text role="ref"} of the `asyncio`{.interpreted-text role="mod"} module.

::: versionadded
3.4
:::
::::

::::: envvar
PYTHONMALLOC

Set the Python memory allocators and/or install debug hooks.

Set the family of memory allocators used by Python:

- `default`: use the `default memory allocators
  <default-memory-allocators>`{.interpreted-text role="ref"}.
- `malloc`: use the `malloc`{.interpreted-text role="c:func"} function of the C library for all domains (`PYMEM_DOMAIN_RAW`{.interpreted-text role="c:macro"}, `PYMEM_DOMAIN_MEM`{.interpreted-text role="c:macro"}, `PYMEM_DOMAIN_OBJ`{.interpreted-text role="c:macro"}).
- `pymalloc`: use the `pymalloc allocator <pymalloc>`{.interpreted-text role="ref"} for `PYMEM_DOMAIN_MEM`{.interpreted-text role="c:macro"} and `PYMEM_DOMAIN_OBJ`{.interpreted-text role="c:macro"} domains and use the `malloc`{.interpreted-text role="c:func"} function for the `PYMEM_DOMAIN_RAW`{.interpreted-text role="c:macro"} domain.
- `mimalloc`: use the `mimalloc allocator <mimalloc>`{.interpreted-text role="ref"} for `PYMEM_DOMAIN_MEM`{.interpreted-text role="c:macro"} and `PYMEM_DOMAIN_OBJ`{.interpreted-text role="c:macro"} domains and use the `malloc`{.interpreted-text role="c:func"} function for the `PYMEM_DOMAIN_RAW`{.interpreted-text role="c:macro"} domain.

Install `debug hooks <pymem-debug-hooks>`{.interpreted-text role="ref"}:

- `debug`: install debug hooks on top of the `default memory
  allocators <default-memory-allocators>`{.interpreted-text role="ref"}.
- `malloc_debug`: same as `malloc` but also install debug hooks.
- `pymalloc_debug`: same as `pymalloc` but also install debug hooks.
- `mimalloc_debug`: same as `mimalloc` but also install debug hooks.

::: versionadded
3.6
:::

::: versionchanged
3.7 Added the `"default"` allocator.
:::
:::::

:::: envvar
PYTHONMALLOCSTATS

If set to a non-empty string, Python will print statistics of the `pymalloc memory allocator <pymalloc>`{.interpreted-text role="ref"} every time a new pymalloc object arena is created, and on shutdown.

This variable is ignored if the `PYTHONMALLOC`{.interpreted-text role="envvar"} environment variable is used to force the `malloc`{.interpreted-text role="c:func"} allocator of the C library, or if Python is configured without `pymalloc` support.

::: versionchanged
3.6 This variable can now also be used on Python compiled in release mode. It now has no effect if set to an empty string.
:::
::::

:::::: envvar
PYTHON_PYMALLOC_HUGEPAGES

If set to a non-zero integer, enable huge page support for `pymalloc <pymalloc>`{.interpreted-text role="ref"} arenas. Set to `0` or unset to disable. Python must be compiled with `--with-pymalloc-hugepages`{.interpreted-text role="option"} for this variable to have any effect.

When enabled, arena allocation uses `MAP_HUGETLB` (Linux) or `MEM_LARGE_PAGES` (Windows) with automatic fallback to regular pages if huge pages are not available.

:::: warning
::: title
Warning
:::

On Linux, if the huge-page pool is exhausted, page faults --- including copy-on-write faults triggered by `os.fork`{.interpreted-text role="func"} --- deliver `SIGBUS` and kill the process. Only enable this in environments where the huge-page pool is properly sized and fork-safety is not a concern.
::::

::: versionadded
3.15
:::
::::::

::::: envvar
PYTHONLEGACYWINDOWSFSENCODING

If set to a non-empty string, the default `filesystem encoding and
error handler`{.interpreted-text role="term"} mode will revert to their pre-3.6 values of \'mbcs\' and \'replace\', respectively. Otherwise, the new defaults \'utf-8\' and \'surrogatepass\' are used.

This may also be enabled at runtime with `sys._enablelegacywindowsfsencoding`{.interpreted-text role="func"}.

::: availability
Windows.
:::

::: versionadded
3.6 See `529`{.interpreted-text role="pep"} for more details.
:::
:::::

::::: envvar
PYTHONLEGACYWINDOWSSTDIO

If set to a non-empty string, does not use the new console reader and writer. This means that Unicode characters will be encoded according to the active console code page, rather than using utf-8.

This variable is ignored if the standard streams are redirected (to files or pipes) rather than referring to console buffers.

::: availability
Windows.
:::

::: versionadded
3.6
:::
:::::

::::: envvar
PYTHONCOERCECLOCALE

If set to the value `0`, causes the main Python command line application to skip coercing the legacy ASCII-based C and POSIX locales to a more capable UTF-8 based alternative.

If this variable is *not* set (or is set to a value other than `0`), the `LC_ALL` locale override environment variable is also not set, and the current locale reported for the `LC_CTYPE` category is either the default `C` locale, or else the explicitly ASCII-based `POSIX` locale, then the Python CLI will attempt to configure the following locales for the `LC_CTYPE` category in the order listed before loading the interpreter runtime:

- `C.UTF-8`
- `C.utf8`
- `UTF-8`

If setting one of these locale categories succeeds, then the `LC_CTYPE` environment variable will also be set accordingly in the current process environment before the Python runtime is initialized. This ensures that in addition to being seen by both the interpreter itself and other locale-aware components running in the same process (such as the GNU `readline` library), the updated setting is also seen in subprocesses (regardless of whether or not those processes are running a Python interpreter), as well as in operations that query the environment rather than the current C locale (such as Python\'s own `locale.getdefaultlocale`{.interpreted-text role="func"}).

Configuring one of these locales (either explicitly or via the above implicit locale coercion) automatically enables the `surrogateescape` `error handler <error-handlers>`{.interpreted-text role="ref"} for `sys.stdin`{.interpreted-text role="data"} and `sys.stdout`{.interpreted-text role="data"} (`sys.stderr`{.interpreted-text role="data"} continues to use `backslashreplace` as it does in any other locale). This stream handling behavior can be overridden using `PYTHONIOENCODING`{.interpreted-text role="envvar"} as usual.

For debugging purposes, setting `PYTHONCOERCECLOCALE=warn` will cause Python to emit warning messages on `stderr` if either the locale coercion activates, or else if a locale that *would* have triggered coercion is still active when the Python runtime is initialized.

Also note that even when locale coercion is disabled, or when it fails to find a suitable target locale, `PYTHONUTF8`{.interpreted-text role="envvar"} will still activate by default in legacy ASCII-based locales. Both features must be disabled in order to force the interpreter to use `ASCII` instead of `UTF-8` for system interfaces.

::: availability
Unix.
:::

::: versionadded
3.7 See `538`{.interpreted-text role="pep"} for more details.
:::
:::::

:::: envvar
PYTHONDEVMODE

If this environment variable is set to a non-empty string, enable `Python Development Mode <devmode>`{.interpreted-text role="ref"}, introducing additional runtime checks that are too expensive to be enabled by default. This is equivalent to setting the `-X`{.interpreted-text role="option"} `dev` option.

::: versionadded
3.7
:::
::::

:::: envvar
PYTHONUTF8

If set to `1`, enable the `Python UTF-8 Mode <utf8-mode>`{.interpreted-text role="ref"}.

If set to `0`, disable the `Python UTF-8 Mode <utf8-mode>`{.interpreted-text role="ref"}.

Setting any other non-empty string causes an error during interpreter initialisation.

::: versionadded
3.7
:::
::::

:::: envvar
PYTHONWARNDEFAULTENCODING

If this environment variable is set to a non-empty string, issue a `EncodingWarning`{.interpreted-text role="class"} when the locale-specific default encoding is used.

See `io-encoding-warning`{.interpreted-text role="ref"} for details.

::: versionadded
3.10
:::
::::

:::: envvar
PYTHONNODEBUGRANGES

If this variable is set, it disables the inclusion of the tables mapping extra location information (end line, start column offset and end column offset) to every instruction in code objects. This is useful when smaller code objects and pyc files are desired as well as suppressing the extra visual location indicators when the interpreter displays tracebacks.

::: versionadded
3.11
:::
::::

:::: envvar
PYTHONPERFSUPPORT

If this variable is set to a nonzero value, it enables support for the Linux `perf` profiler so Python calls can be detected by it.

If set to `0`, disable Linux `perf` profiler support.

See also the `-X perf <-X>`{.interpreted-text role="option"} command-line option and `perf_profiling`{.interpreted-text role="ref"}.

::: versionadded
3.12
:::
::::

:::: envvar
PYTHON_PERF_JIT_SUPPORT

If this variable is set to a nonzero value, it enables support for the Linux `perf` profiler so Python calls can be detected by it using DWARF information.

If set to `0`, disable Linux `perf` profiler support.

See also the `-X perf_jit <-X>`{.interpreted-text role="option"} command-line option and `perf_profiling`{.interpreted-text role="ref"}.

::: versionadded
3.13
:::
::::

:::: envvar
PYTHON_DISABLE_REMOTE_DEBUG

If this variable is set to a non-empty string, it disables the remote debugging feature described in `768`{.interpreted-text role="pep"}. This includes both the functionality to schedule code for execution in another process and the functionality to receive code for execution in the current process.

See also the `-X disable_remote_debug`{.interpreted-text role="option"} command-line option.

::: versionadded
3.14
:::
::::

:::: envvar
PYTHON_CPU_COUNT

If this variable is set to a positive integer, it overrides the return values of `os.cpu_count`{.interpreted-text role="func"} and `os.process_cpu_count`{.interpreted-text role="func"}.

See also the `-X cpu_count <-X>`{.interpreted-text role="option"} command-line option.

::: versionadded
3.13
:::
::::

:::: envvar
PYTHON_FROZEN_MODULES

If this variable is set to `on` or `off`, it determines whether or not frozen modules are ignored by the import machinery. A value of `on` means they get imported and `off` means they are ignored. The default is `on` for non-debug builds (the normal case) and `off` for debug builds. Note that the `!importlib_bootstrap`{.interpreted-text role="mod"} and `!importlib_bootstrap_external`{.interpreted-text role="mod"} frozen modules are always used, even if this flag is set to `off`.

See also the `-X frozen_modules <-X>`{.interpreted-text role="option"} command-line option.

::: versionadded
3.13
:::
::::

:::: envvar
PYTHON_COLORS

If this variable is set to `1`, the interpreter will colorize various kinds of output. Setting it to `0` deactivates this behavior. See also `using-on-controlling-color`{.interpreted-text role="ref"}.

::: versionadded
3.13
:::
::::

:::: envvar
PYTHON_BASIC_REPL

If this variable is set to any value, the interpreter will not attempt to load the Python-based `REPL`{.interpreted-text role="term"} that requires `readline`{.interpreted-text role="mod"}, and will instead use the traditional parser-based `REPL`{.interpreted-text role="term"}.

::: versionadded
3.13
:::
::::

:::: envvar
PYTHON_HISTORY

This environment variable can be used to set the location of a `.python_history` file (by default, it is `.python_history` in the user\'s home directory).

::: versionadded
3.13
:::
::::

:::: envvar
PYTHON_GIL

If this variable is set to `1`, the global interpreter lock (GIL) will be forced on. Setting it to `0` forces the GIL off (needs Python configured with the `--disable-gil`{.interpreted-text role="option"} build option).

See also the `-X gil <-X>`{.interpreted-text role="option"} command-line option, which takes precedence over this variable, and `whatsnew313-free-threaded-cpython`{.interpreted-text role="ref"}.

::: versionadded
3.13
:::
::::

:::: envvar
PYTHON_THREAD_INHERIT_CONTEXT

If this variable is set to `1` then `~threading.Thread`{.interpreted-text role="class"} will, by default, use a copy of context of the caller of `Thread.start()` when starting. Otherwise, new threads will start with an empty context. If unset, this variable defaults to `1` on free-threaded builds and to `0` otherwise. See also `-X thread_inherit_context<-X>`{.interpreted-text role="option"}.

::: versionadded
3.14
:::
::::

:::: envvar
PYTHON_CONTEXT_AWARE_WARNINGS

If set to `1` then the `warnings.catch_warnings`{.interpreted-text role="class"} context manager will use a `~contextvars.ContextVar`{.interpreted-text role="class"} to store warnings filter state. If unset, this variable defaults to `1` on free-threaded builds and to `0` otherwise. See `-X
context_aware_warnings<-X>`{.interpreted-text role="option"}.

::: versionadded
3.14
:::
::::

:::: envvar
PYTHON_JIT

On builds where experimental just-in-time compilation is available, this variable can force the JIT to be disabled (`0`) or enabled (`1`) at interpreter startup.

::: versionadded
3.13
:::
::::

:::: envvar
PYTHON_TLBC

If set to `1` enables thread-local bytecode. If set to `0` thread-local bytecode and the specializing interpreter are disabled. Only applies to builds configured with `--disable-gil`{.interpreted-text role="option"}.

See also the `-X tlbc <-X>`{.interpreted-text role="option"} command-line option.

::: versionadded
3.14
:::
::::

:::: envvar
PYTHON_LAZY_IMPORTS

Controls lazy import behavior. Accepts three values: `all` makes all imports lazy by default, `none` disables lazy imports entirely (even explicit `lazy` statements become eager), and `normal` (the default) respects the `lazy` keyword in source code.

See also the `-X lazy_imports <-X>`{.interpreted-text role="option"} command-line option.

::: versionadded
next
:::
::::

### Debug-mode variables

::: envvar
PYTHONDUMPREFS

If set, Python will dump objects and reference counts still alive after shutting down the interpreter.

Needs Python configured with the `--with-trace-refs`{.interpreted-text role="option"} build option.
:::

:::: envvar
PYTHONDUMPREFSFILE

If set, Python will dump objects and reference counts still alive after shutting down the interpreter into a file under the path given as the value to this environment variable.

Needs Python configured with the `--with-trace-refs`{.interpreted-text role="option"} build option.

::: versionadded
3.11
:::
::::

:::: envvar
PYTHON_PRESITE

If this variable is set to a module, that module will be imported early in the interpreter lifecycle, before the `site`{.interpreted-text role="mod"} module is executed, and before the `__main__`{.interpreted-text role="mod"} module is created. Therefore, the imported module is not treated as `__main__`{.interpreted-text role="mod"}.

This can be used to execute code early during Python initialization.

To import a submodule, use `package.module` as the value, like in an import statement.

See also the `-X presite <-X>`{.interpreted-text role="option"} command-line option, which takes precedence over this variable.

Needs Python configured with the `--with-pydebug`{.interpreted-text role="option"} build option.

::: versionadded
3.13
:::
::::
