# Python support for free threading {#freethreading-python-howto}

Starting with the 3.13 release, CPython has support for a build of Python called `free threading`{.interpreted-text role="term"} where the `global interpreter lock`{.interpreted-text role="term"} (GIL) is disabled. Free-threaded execution allows for full utilization of the available processing power by running threads in parallel on available CPU cores. While not all software will benefit from this automatically, programs designed with threading in mind will run faster on multi-core hardware.

Some third-party packages, in particular ones with an `extension module`{.interpreted-text role="term"}, may not be ready for use in a free-threaded build, and will re-enable the `GIL`{.interpreted-text role="term"}.

This document describes the implications of free threading for Python code. See `freethreading-extensions-howto`{.interpreted-text role="ref"} for information on how to write C extensions that support the free-threaded build.

::: seealso
`703`{.interpreted-text role="pep"} -- Making the Global Interpreter Lock Optional in CPython for an overall description of free-threaded Python.
:::

## Installation

Starting with Python 3.13, the official macOS and Windows installers optionally support installing free-threaded Python binaries. The installers are available at <https://www.python.org/downloads/>.

For information on other platforms, see the [Installing a Free-Threaded Python](https://py-free-threading.github.io/installing-cpython/), a community-maintained installation guide for installing free-threaded Python.

When building CPython from source, the `--disable-gil`{.interpreted-text role="option"} configure option should be used to build a free-threaded Python interpreter.

## Identifying free-threaded Python

To check if the current interpreter supports free-threading, `python -VV <-V>`{.interpreted-text role="option"} and `sys.version`{.interpreted-text role="data"} contain \"free-threading build\". The new `sys._is_gil_enabled`{.interpreted-text role="func"} function can be used to check whether the GIL is actually disabled in the running process.

The `sysconfig.get_config_var("Py_GIL_DISABLED")` configuration variable can be used to determine whether the build supports free threading. If the variable is set to `1`, then the build supports free threading. This is the recommended mechanism for decisions related to the build configuration.

## The global interpreter lock in free-threaded Python

Free-threaded builds of CPython support optionally running with the GIL enabled at runtime using the environment variable `PYTHON_GIL`{.interpreted-text role="envvar"} or the command-line option `-X gil`{.interpreted-text role="option"}.

The GIL may also automatically be enabled when importing a C-API extension module that is not explicitly marked as supporting free threading. A warning will be printed in this case.

In addition to individual package documentation, the following websites track the status of popular packages support for free threading:

- <https://py-free-threading.github.io/tracking/>
- <https://hugovk.github.io/free-threaded-wheels/>

## Thread safety

The free-threaded build of CPython aims to provide similar thread-safety behavior at the Python level to the default GIL-enabled build. Built-in types like `dict`{.interpreted-text role="class"}, `list`{.interpreted-text role="class"}, and `set`{.interpreted-text role="class"} use internal locks to protect against concurrent modifications in ways that behave similarly to the GIL. However, Python has not historically guaranteed specific behavior for concurrent modifications to these built-in types, so this should be treated as a description of the current implementation, not a guarantee of current or future behavior.

:::: note
::: title
Note
:::

It\'s recommended to use the `threading.Lock`{.interpreted-text role="class"} or other synchronization primitives instead of relying on the internal locks of built-in types, when possible.
::::

## Known limitations

This section describes known limitations of the free-threaded CPython build.

### Immortalization

In the free-threaded build, some objects are `immortal`{.interpreted-text role="term"}. Immortal objects are not deallocated and have reference counts that are never modified. This is done to avoid reference count contention that would prevent efficient multi-threaded scaling.

As of the 3.14 release, immortalization is limited to:

- Code constants: numeric literals, string literals, and tuple literals composed of other constants.
- Strings interned by `sys.intern`{.interpreted-text role="func"}.

### Frame objects

It is not safe to access `frame.f_locals`{.interpreted-text role="attr"} from a `frame <frame-objects>`{.interpreted-text role="ref"} object if that frame is currently executing in another thread, and doing so may crash the interpreter.

### Iterators

It is generally not thread-safe to access the same iterator object from multiple threads concurrently, and threads may see duplicate or missing elements.

### Single-threaded performance

The free-threaded build has additional overhead when executing Python code compared to the default GIL-enabled build. The amount of overhead depends on the workload and hardware. On the pyperformance benchmark suite, the average overhead ranges from about 1% on macOS aarch64 to 8% on x86-64 Linux systems.

## Behavioral changes

This section describes CPython behavioural changes with the free-threaded build.

### Context variables

In the free-threaded build, the flag `~sys.flags.thread_inherit_context`{.interpreted-text role="data"} is set to true by default which causes threads created with `threading.Thread`{.interpreted-text role="class"} to start with a copy of the `~contextvars.Context()`{.interpreted-text role="class"} of the caller of `~threading.Thread.start`{.interpreted-text role="meth"}. In the default GIL-enabled build, the flag defaults to false so threads start with an empty `~contextvars.Context()`{.interpreted-text role="class"}.

### Warning filters

In the free-threaded build, the flag `~sys.flags.context_aware_warnings`{.interpreted-text role="data"} is set to true by default. In the default GIL-enabled build, the flag defaults to false. If the flag is true then the `warnings.catch_warnings`{.interpreted-text role="class"} context manager uses a context variable for warning filters. If the flag is false then `~warnings.catch_warnings`{.interpreted-text role="class"} modifies the global filters list, which is not thread-safe. See the `warnings`{.interpreted-text role="mod"} module for more details.
