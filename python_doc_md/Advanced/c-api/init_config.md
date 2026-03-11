# Python Initialization Configuration {#init-config}

## PyInitConfig C API {#pyinitconfig_api}

::: versionadded
3.14
:::

Python can be initialized with `Py_InitializeFromInitConfig`{.interpreted-text role="c:func"}.

The `Py_RunMain`{.interpreted-text role="c:func"} function can be used to write a customized Python program.

See also `Initialization, Finalization, and Threads <initialization>`{.interpreted-text role="ref"}.

::: seealso
`741`{.interpreted-text role="pep"} \"Python Configuration C API\".
:::

### Example

Example of customized Python always running with the `Python Development
Mode <devmode>`{.interpreted-text role="ref"} enabled; return `-1` on error:

``` c
int init_python(void)
{
    PyInitConfig *config = PyInitConfig_Create();
    if (config == NULL) {
        printf("PYTHON INIT ERROR: memory allocation failed\n");
        return -1;
    }

    // Enable the Python Development Mode
    if (PyInitConfig_SetInt(config, "dev_mode", 1) < 0) {
        goto error;
    }

    // Initialize Python with the configuration
    if (Py_InitializeFromInitConfig(config) < 0) {
        goto error;
    }
    PyInitConfig_Free(config);
    return 0;

error:
    {
        // Display the error message.
        //
        // This uncommon braces style is used, because you cannot make
        // goto targets point to variable declarations.
        const char *err_msg;
        (void)PyInitConfig_GetError(config, &err_msg);
        printf("PYTHON INIT ERROR: %s\n", err_msg);
        PyInitConfig_Free(config);
        return -1;
    }
}
```

### Create Config

> Opaque structure to configure the Python initialization.

> Create a new initialization configuration using `Isolated Configuration
> <init-isolated-conf>`{.interpreted-text role="ref"} default values.
>
> It must be freed by `PyInitConfig_Free`{.interpreted-text role="c:func"}.
>
> Return `NULL` on memory allocation failure.

> Free memory of the initialization configuration *config*.
>
> If *config* is `NULL`, no operation is performed.

### Error Handling

> Get the *config* error message.
>
> - Set *\*err_msg* and return `1` if an error is set.
> - Set *\*err_msg* to `NULL` and return `0` otherwise.
>
> An error message is a UTF-8 encoded string.
>
> If *config* has an exit code, format the exit code as an error message.
>
> The error message remains valid until another `PyInitConfig` function is called with *config*. The caller doesn\'t have to free the error message.

> Get the *config* exit code.
>
> - Set *\*exitcode* and return `1` if *config* has an exit code set.
> - Return `0` if *config* has no exit code set.
>
> Only the `Py_InitializeFromInitConfig()` function can set an exit code if the `parse_argv` option is non-zero.
>
> An exit code can be set when parsing the command line failed (exit code `2`) or when a command line option asks to display the command line help (exit code `0`).

### Get Options

The configuration option *name* parameter must be a non-NULL null-terminated UTF-8 encoded string. See `Configuration Options <pyinitconfig-opts>`{.interpreted-text role="ref"}.

> Test if the configuration has an option called *name*.
>
> Return `1` if the option exists, or return `0` otherwise.

> Get an integer configuration option.
>
> - Set *\*value*, and return `0` on success.
> - Set an error in *config* and return `-1` on error.

> Get a string configuration option as a null-terminated UTF-8 encoded string.
>
> - Set *\*value*, and return `0` on success.
> - Set an error in *config* and return `-1` on error.
>
> *\*value* can be set to `NULL` if the option is an optional string and the option is unset.
>
> On success, the string must be released with `free(value)` if it\'s not `NULL`.

> Get a string list configuration option as an array of null-terminated UTF-8 encoded strings.
>
> - Set *\*length* and *\*value*, and return `0` on success.
> - Set an error in *config* and return `-1` on error.
>
> On success, the string list must be released with `PyInitConfig_FreeStrList(length, items)`.

> Free memory of a string list created by `PyInitConfig_GetStrList()`.

### Set Options

The configuration option *name* parameter must be a non-NULL null-terminated UTF-8 encoded string. See `Configuration Options <pyinitconfig-opts>`{.interpreted-text role="ref"}.

Some configuration options have side effects on other options. This logic is only implemented when `Py_InitializeFromInitConfig()` is called, not by the \"Set\" functions below. For example, setting `dev_mode` to `1` does not set `faulthandler` to `1`.

> Set an integer configuration option.
>
> - Return `0` on success.
> - Set an error in *config* and return `-1` on error.

> Set a string configuration option from a null-terminated UTF-8 encoded string. The string is copied.
>
> - Return `0` on success.
> - Set an error in *config* and return `-1` on error.

> Set a string list configuration option from an array of null-terminated UTF-8 encoded strings. The string list is copied.
>
> - Return `0` on success.
> - Set an error in *config* and return `-1` on error.

### Module

> Add a built-in extension module to the table of built-in modules.
>
> The new module can be imported by the name *name*, and uses the function *initfunc* as the initialization function called on the first attempted import.
>
> - Return `0` on success.
> - Set an error in *config* and return `-1` on error.
>
> If Python is initialized multiple times, `PyInitConfig_AddModule()` must be called at each Python initialization.
>
> Similar to the `PyImport_AppendInittab`{.interpreted-text role="c:func"} function.

### Initialize Python

> Initialize Python from the initialization configuration.
>
> - Return `0` on success.
> - Set an error in *config* and return `-1` on error.
> - Set an exit code in *config* and return `-1` if Python wants to exit.
>
> See `PyInitConfig_GetExitcode()` for the exit code case.

## Configuration Options {#pyinitconfig-opts}

  Option                           PyConfig/PyPreConfig member                                                                                Type               Visibility
  -------------------------------- ---------------------------------------------------------------------------------------------------------- ------------------ ------------
  `"allocator"`                    `allocator <PyPreConfig.allocator>`{.interpreted-text role="c:member"}                                     `int`              Read-only
  `"argv"`                         `argv <PyConfig.argv>`{.interpreted-text role="c:member"}                                                  `list[str]`        Public
  `"base_exec_prefix"`             `base_exec_prefix <PyConfig.base_exec_prefix>`{.interpreted-text role="c:member"}                          `str`              Public
  `"base_executable"`              `base_executable <PyConfig.base_executable>`{.interpreted-text role="c:member"}                            `str`              Public
  `"base_prefix"`                  `base_prefix <PyConfig.base_prefix>`{.interpreted-text role="c:member"}                                    `str`              Public
  `"buffered_stdio"`               `buffered_stdio <PyConfig.buffered_stdio>`{.interpreted-text role="c:member"}                              `bool`             Read-only
  `"bytes_warning"`                `bytes_warning <PyConfig.bytes_warning>`{.interpreted-text role="c:member"}                                `int`              Public
  `"check_hash_pycs_mode"`         `check_hash_pycs_mode <PyConfig.check_hash_pycs_mode>`{.interpreted-text role="c:member"}                  `str`              Read-only
  `"code_debug_ranges"`            `code_debug_ranges <PyConfig.code_debug_ranges>`{.interpreted-text role="c:member"}                        `bool`             Read-only
  `"coerce_c_locale"`              `coerce_c_locale <PyPreConfig.coerce_c_locale>`{.interpreted-text role="c:member"}                         `bool`             Read-only
  `"coerce_c_locale_warn"`         `coerce_c_locale_warn <PyPreConfig.coerce_c_locale_warn>`{.interpreted-text role="c:member"}               `bool`             Read-only
  `"configure_c_stdio"`            `configure_c_stdio <PyConfig.configure_c_stdio>`{.interpreted-text role="c:member"}                        `bool`             Read-only
  `"configure_locale"`             `configure_locale <PyPreConfig.configure_locale>`{.interpreted-text role="c:member"}                       `bool`             Read-only
  `"cpu_count"`                    `cpu_count <PyConfig.cpu_count>`{.interpreted-text role="c:member"}                                        `int`              Public
  `"dev_mode"`                     `dev_mode <PyConfig.dev_mode>`{.interpreted-text role="c:member"}                                          `bool`             Read-only
  `"dump_refs"`                    `dump_refs <PyConfig.dump_refs>`{.interpreted-text role="c:member"}                                        `bool`             Read-only
  `"dump_refs_file"`               `dump_refs_file <PyConfig.dump_refs_file>`{.interpreted-text role="c:member"}                              `str`              Read-only
  `"exec_prefix"`                  `exec_prefix <PyConfig.exec_prefix>`{.interpreted-text role="c:member"}                                    `str`              Public
  `"executable"`                   `executable <PyConfig.executable>`{.interpreted-text role="c:member"}                                      `str`              Public
  `"faulthandler"`                 `faulthandler <PyConfig.faulthandler>`{.interpreted-text role="c:member"}                                  `bool`             Read-only
  `"filesystem_encoding"`          `filesystem_encoding <PyConfig.filesystem_encoding>`{.interpreted-text role="c:member"}                    `str`              Read-only
  `"filesystem_errors"`            `filesystem_errors <PyConfig.filesystem_errors>`{.interpreted-text role="c:member"}                        `str`              Read-only
  `"hash_seed"`                    `hash_seed <PyConfig.hash_seed>`{.interpreted-text role="c:member"}                                        `int`              Read-only
  `"home"`                         `home <PyConfig.home>`{.interpreted-text role="c:member"}                                                  `str`              Read-only
  `"import_time"`                  `import_time <PyConfig.import_time>`{.interpreted-text role="c:member"}                                    `int`              Read-only
  `"inspect"`                      `inspect <PyConfig.inspect>`{.interpreted-text role="c:member"}                                            `bool`             Public
  `"install_signal_handlers"`      `install_signal_handlers <PyConfig.install_signal_handlers>`{.interpreted-text role="c:member"}            `bool`             Read-only
  `"int_max_str_digits"`           `int_max_str_digits <PyConfig.int_max_str_digits>`{.interpreted-text role="c:member"}                      `int`              Public
  `"interactive"`                  `interactive <PyConfig.interactive>`{.interpreted-text role="c:member"}                                    `bool`             Public
  `"isolated"`                     `isolated <PyConfig.isolated>`{.interpreted-text role="c:member"}                                          `bool`             Read-only
  `"legacy_windows_fs_encoding"`   `legacy_windows_fs_encoding <PyPreConfig.legacy_windows_fs_encoding>`{.interpreted-text role="c:member"}   `bool`             Read-only
  `"legacy_windows_stdio"`         `legacy_windows_stdio <PyConfig.legacy_windows_stdio>`{.interpreted-text role="c:member"}                  `bool`             Read-only
  `"malloc_stats"`                 `malloc_stats <PyConfig.malloc_stats>`{.interpreted-text role="c:member"}                                  `bool`             Read-only
  `"module_search_paths"`          `module_search_paths <PyConfig.module_search_paths>`{.interpreted-text role="c:member"}                    `list[str]`        Public
  `"optimization_level"`           `optimization_level <PyConfig.optimization_level>`{.interpreted-text role="c:member"}                      `int`              Public
  `"orig_argv"`                    `orig_argv <PyConfig.orig_argv>`{.interpreted-text role="c:member"}                                        `list[str]`        Read-only
  `"parse_argv"`                   `parse_argv <PyConfig.parse_argv>`{.interpreted-text role="c:member"}                                      `bool`             Read-only
  `"parser_debug"`                 `parser_debug <PyConfig.parser_debug>`{.interpreted-text role="c:member"}                                  `bool`             Public
  `"pathconfig_warnings"`          `pathconfig_warnings <PyConfig.pathconfig_warnings>`{.interpreted-text role="c:member"}                    `bool`             Read-only
  `"perf_profiling"`               `perf_profiling <PyConfig.perf_profiling>`{.interpreted-text role="c:member"}                              `bool`             Read-only
  `"platlibdir"`                   `platlibdir <PyConfig.platlibdir>`{.interpreted-text role="c:member"}                                      `str`              Public
  `"prefix"`                       `prefix <PyConfig.prefix>`{.interpreted-text role="c:member"}                                              `str`              Public
  `"program_name"`                 `program_name <PyConfig.program_name>`{.interpreted-text role="c:member"}                                  `str`              Read-only
  `"pycache_prefix"`               `pycache_prefix <PyConfig.pycache_prefix>`{.interpreted-text role="c:member"}                              `str`              Public
  `"quiet"`                        `quiet <PyConfig.quiet>`{.interpreted-text role="c:member"}                                                `bool`             Public
  `"run_command"`                  `run_command <PyConfig.run_command>`{.interpreted-text role="c:member"}                                    `str`              Read-only
  `"run_filename"`                 `run_filename <PyConfig.run_filename>`{.interpreted-text role="c:member"}                                  `str`              Read-only
  `"run_module"`                   `run_module <PyConfig.run_module>`{.interpreted-text role="c:member"}                                      `str`              Read-only
  `"run_presite"`                  `run_presite <PyConfig.run_presite>`{.interpreted-text role="c:member"}                                    `str`              Read-only
  `"safe_path"`                    `safe_path <PyConfig.safe_path>`{.interpreted-text role="c:member"}                                        `bool`             Read-only
  `"show_ref_count"`               `show_ref_count <PyConfig.show_ref_count>`{.interpreted-text role="c:member"}                              `bool`             Read-only
  `"site_import"`                  `site_import <PyConfig.site_import>`{.interpreted-text role="c:member"}                                    `bool`             Read-only
  `"skip_source_first_line"`       `skip_source_first_line <PyConfig.skip_source_first_line>`{.interpreted-text role="c:member"}              `bool`             Read-only
  `"stdio_encoding"`               `stdio_encoding <PyConfig.stdio_encoding>`{.interpreted-text role="c:member"}                              `str`              Read-only
  `"stdio_errors"`                 `stdio_errors <PyConfig.stdio_errors>`{.interpreted-text role="c:member"}                                  `str`              Read-only
  `"stdlib_dir"`                   `stdlib_dir <PyConfig.stdlib_dir>`{.interpreted-text role="c:member"}                                      `str`              Public
  `"tracemalloc"`                  `tracemalloc <PyConfig.tracemalloc>`{.interpreted-text role="c:member"}                                    `int`              Read-only
  `"use_environment"`              `use_environment <PyConfig.use_environment>`{.interpreted-text role="c:member"}                            `bool`             Public
  `"use_frozen_modules"`           `use_frozen_modules <PyConfig.use_frozen_modules>`{.interpreted-text role="c:member"}                      `bool`             Read-only
  `"use_hash_seed"`                `use_hash_seed <PyConfig.use_hash_seed>`{.interpreted-text role="c:member"}                                `bool`             Read-only
  `"use_system_logger"`            `use_system_logger <PyConfig.use_system_logger>`{.interpreted-text role="c:member"}                        `bool`             Read-only
  `"user_site_directory"`          `user_site_directory <PyConfig.user_site_directory>`{.interpreted-text role="c:member"}                    `bool`             Read-only
  `"utf8_mode"`                    `utf8_mode <PyPreConfig.utf8_mode>`{.interpreted-text role="c:member"}                                     `bool`             Read-only
  `"verbose"`                      `verbose <PyConfig.verbose>`{.interpreted-text role="c:member"}                                            `int`              Public
  `"warn_default_encoding"`        `warn_default_encoding <PyConfig.warn_default_encoding>`{.interpreted-text role="c:member"}                `bool`             Read-only
  `"warnoptions"`                  `warnoptions <PyConfig.warnoptions>`{.interpreted-text role="c:member"}                                    `list[str]`        Public
  `"write_bytecode"`               `write_bytecode <PyConfig.write_bytecode>`{.interpreted-text role="c:member"}                              `bool`             Public
  `"xoptions"`                     `xoptions <PyConfig.xoptions>`{.interpreted-text role="c:member"}                                          `dict[str, str]`   Public
  `"_pystats"`                     `_pystats <PyConfig._pystats>`{.interpreted-text role="c:member"}                                          `bool`             Read-only

Visibility:

- Public: Can be retrieved by `PyConfig_Get`{.interpreted-text role="c:func"} and set by `PyConfig_Set`{.interpreted-text role="c:func"}.
- Read-only: Can be retrieved by `PyConfig_Get`{.interpreted-text role="c:func"}, but cannot be set by `PyConfig_Set`{.interpreted-text role="c:func"}.

## Runtime Python configuration API

At runtime, it\'s possible to get and set configuration options using `PyConfig_Get`{.interpreted-text role="c:func"} and `PyConfig_Set`{.interpreted-text role="c:func"} functions.

The configuration option *name* parameter must be a non-NULL null-terminated UTF-8 encoded string. See `Configuration Options <pyinitconfig-opts>`{.interpreted-text role="ref"}.

Some options are read from the `sys`{.interpreted-text role="mod"} attributes. For example, the option `"argv"` is read from `sys.argv`{.interpreted-text role="data"}.

> Get the current runtime value of a configuration option as a Python object.
>
> - Return a new reference on success.
> - Set an exception and return `NULL` on error.
>
> The object type depends on the configuration option. It can be:
>
> - `bool`
> - `int`
> - `str`
> - `list[str]`
> - `dict[str, str]`
>
> The caller must have an `attached thread state`{.interpreted-text role="term"}. The function cannot be called before Python initialization nor after Python finalization.
>
> ::: versionadded
> 3.14
> :::

> Similar to `PyConfig_Get`{.interpreted-text role="c:func"}, but get the value as a C int.
>
> - Return `0` on success.
> - Set an exception and return `-1` on error.
>
> ::: versionadded
> 3.14
> :::

> Get all configuration option names as a `frozenset`.
>
> - Return a new reference on success.
> - Set an exception and return `NULL` on error.
>
> The caller must have an `attached thread state`{.interpreted-text role="term"}. The function cannot be called before Python initialization nor after Python finalization.
>
> ::: versionadded
> 3.14
> :::

> Set the current runtime value of a configuration option.
>
> - Raise a `ValueError`{.interpreted-text role="exc"} if there is no option *name*.
> - Raise a `ValueError`{.interpreted-text role="exc"} if *value* is an invalid value.
> - Raise a `ValueError`{.interpreted-text role="exc"} if the option is read-only (cannot be set).
> - Raise a `TypeError`{.interpreted-text role="exc"} if *value* has not the proper type.
>
> The caller must have an `attached thread state`{.interpreted-text role="term"}. The function cannot be called before Python initialization nor after Python finalization.
>
> ::: audit-event
> cpython.PyConfig_Set name,value c.PyConfig_Set
> :::
>
> ::: versionadded
> 3.14
> :::

## PyConfig C API {#pyconfig_api}

::: versionadded
3.8
:::

Python can be initialized with `Py_InitializeFromConfig`{.interpreted-text role="c:func"} and the `PyConfig`{.interpreted-text role="c:type"} structure. It can be preinitialized with `Py_PreInitialize`{.interpreted-text role="c:func"} and the `PyPreConfig`{.interpreted-text role="c:type"} structure.

There are two kinds of configuration:

- The `Python Configuration <init-python-config>`{.interpreted-text role="ref"} can be used to build a customized Python which behaves as the regular Python. For example, environment variables and command line arguments are used to configure Python.
- The `Isolated Configuration <init-isolated-conf>`{.interpreted-text role="ref"} can be used to embed Python into an application. It isolates Python from the system. For example, environment variables are ignored, the LC_CTYPE locale is left unchanged and no signal handler is registered.

The `Py_RunMain`{.interpreted-text role="c:func"} function can be used to write a customized Python program.

See also `Initialization, Finalization, and Threads <initialization>`{.interpreted-text role="ref"}.

::: seealso
`587`{.interpreted-text role="pep"} \"Python Initialization Configuration\".
:::

### Example

Example of customized Python always running in isolated mode:

``` c
int main(int argc, char **argv)
{
    PyStatus status;

    PyConfig config;
    PyConfig_InitPythonConfig(&config);
    config.isolated = 1;

    /* Decode command line arguments.
       Implicitly preinitialize Python (in isolated mode). */
    status = PyConfig_SetBytesArgv(&config, argc, argv);
    if (PyStatus_Exception(status)) {
        goto exception;
    }

    status = Py_InitializeFromConfig(&config);
    if (PyStatus_Exception(status)) {
        goto exception;
    }
    PyConfig_Clear(&config);

    return Py_RunMain();

exception:
    PyConfig_Clear(&config);
    if (PyStatus_IsExit(status)) {
        return status.exitcode;
    }
    /* Display the error message and exit the process with
       non-zero exit code */
    Py_ExitStatusException(status);
}
```

### PyWideStringList

> List of `wchar_t*` strings.
>
> If *length* is non-zero, *items* must be non-`NULL` and all strings must be non-`NULL`.
>
> Methods:
>
> > Append *item* to *list*.
> >
> > Python must be preinitialized to call this function.
>
> > Insert *item* into *list* at *index*.
> >
> > If *index* is greater than or equal to *list* length, append *item* to *list*.
> >
> > *index* must be greater than or equal to `0`.
> >
> > Python must be preinitialized to call this function.
>
> Structure fields:
>
> > List length.
>
> > List items.

### PyStatus

> Structure to store an initialization function status: success, error or exit.
>
> For an error, it can store the C function name which created the error.
>
> Structure fields:
>
> > Exit code. Argument passed to `exit()`.
>
> > Error message.
>
> > Name of the function which created an error, can be `NULL`.
>
> Functions to create a status:
>
> > Success.
>
> > Initialization error with a message.
> >
> > *err_msg* must not be `NULL`.
>
> > Memory allocation failure (out of memory).
>
> > Exit Python with the specified exit code.
>
> Functions to handle a status:
>
> > Is the status an error or an exit? If true, the exception must be handled; by calling `Py_ExitStatusException`{.interpreted-text role="c:func"} for example.
>
> > Is the result an error?
>
> > Is the result an exit?
>
> > Call `exit(exitcode)` if *status* is an exit. Print the error message and exit with a non-zero exit code if *status* is an error. Must only be called if `PyStatus_Exception(status)` is non-zero.

:::: note
::: title
Note
:::

Internally, Python uses macros which set `PyStatus.func`, whereas functions to create a status set `func` to `NULL`.
::::

Example:

``` c
PyStatus alloc(void **ptr, size_t size)
{
    *ptr = PyMem_RawMalloc(size);
    if (*ptr == NULL) {
        return PyStatus_NoMemory();
    }
    return PyStatus_Ok();
}

int main(int argc, char **argv)
{
    void *ptr;
    PyStatus status = alloc(&ptr, 16);
    if (PyStatus_Exception(status)) {
        Py_ExitStatusException(status);
    }
    PyMem_Free(ptr);
    return 0;
}
```

### PyPreConfig

> Structure used to preinitialize Python.
>
> Function to initialize a preconfiguration:
>
> > Initialize the preconfiguration with `Python Configuration
> > <init-python-config>`{.interpreted-text role="ref"}.
>
> > Initialize the preconfiguration with `Isolated Configuration
> > <init-isolated-conf>`{.interpreted-text role="ref"}.
>
> Structure fields:
>
> > Name of the Python memory allocators:
> >
> > - `PYMEM_ALLOCATOR_NOT_SET` (`0`): don\'t change memory allocators (use defaults).
> > - `PYMEM_ALLOCATOR_DEFAULT` (`1`): `default memory allocators
> >   <default-memory-allocators>`{.interpreted-text role="ref"}.
> > - `PYMEM_ALLOCATOR_DEBUG` (`2`): `default memory allocators
> >   <default-memory-allocators>`{.interpreted-text role="ref"} with `debug hooks
> >   <pymem-debug-hooks>`{.interpreted-text role="ref"}.
> > - `PYMEM_ALLOCATOR_MALLOC` (`3`): use `malloc()` of the C library.
> > - `PYMEM_ALLOCATOR_MALLOC_DEBUG` (`4`): force usage of `malloc()` with `debug hooks <pymem-debug-hooks>`{.interpreted-text role="ref"}.
> > - `PYMEM_ALLOCATOR_PYMALLOC` (`5`): `Python pymalloc memory
> >   allocator <pymalloc>`{.interpreted-text role="ref"}.
> > - `PYMEM_ALLOCATOR_PYMALLOC_DEBUG` (`6`): `Python pymalloc
> >   memory allocator <pymalloc>`{.interpreted-text role="ref"} with `debug hooks
> >   <pymem-debug-hooks>`{.interpreted-text role="ref"}.
> > - `PYMEM_ALLOCATOR_MIMALLOC` (`6`): use `mimalloc`, a fast malloc replacement.
> > - `PYMEM_ALLOCATOR_MIMALLOC_DEBUG` (`7`): use `mimalloc`, a fast malloc replacement with `debug hooks <pymem-debug-hooks>`{.interpreted-text role="ref"}.
> >
> > `PYMEM_ALLOCATOR_PYMALLOC` and `PYMEM_ALLOCATOR_PYMALLOC_DEBUG` are not supported if Python is `configured using --without-pymalloc
> > <--without-pymalloc>`{.interpreted-text role="option"}.
> >
> > `PYMEM_ALLOCATOR_MIMALLOC` and `PYMEM_ALLOCATOR_MIMALLOC_DEBUG` are not supported if Python is `configured using --without-mimalloc
> > <--without-mimalloc>`{.interpreted-text role="option"} or if the underlying atomic support isn\'t available.
> >
> > See `Memory Management <memory>`{.interpreted-text role="ref"}.
> >
> > Default: `PYMEM_ALLOCATOR_NOT_SET`.
>
> > Set the LC_CTYPE locale to the user preferred locale.
> >
> > If equals to `0`, set `~PyPreConfig.coerce_c_locale`{.interpreted-text role="c:member"} and `~PyPreConfig.coerce_c_locale_warn`{.interpreted-text role="c:member"} members to `0`.
> >
> > See the `locale encoding`{.interpreted-text role="term"}.
> >
> > Default: `1` in Python config, `0` in isolated config.
>
> > If equals to `2`, coerce the C locale.
> >
> > If equals to `1`, read the LC_CTYPE locale to decide if it should be coerced.
> >
> > See the `locale encoding`{.interpreted-text role="term"}.
> >
> > Default: `-1` in Python config, `0` in isolated config.
>
> > If non-zero, emit a warning if the C locale is coerced.
> >
> > Default: `-1` in Python config, `0` in isolated config.
>
> > `Python Development Mode <devmode>`{.interpreted-text role="ref"}: see `PyConfig.dev_mode`{.interpreted-text role="c:member"}.
> >
> > Default: `-1` in Python mode, `0` in isolated mode.
>
> > Isolated mode: see `PyConfig.isolated`{.interpreted-text role="c:member"}.
> >
> > Default: `0` in Python mode, `1` in isolated mode.
>
> > If non-zero:
> >
> > - Set `PyPreConfig.utf8_mode`{.interpreted-text role="c:member"} to `0`,
> > - Set `PyConfig.filesystem_encoding`{.interpreted-text role="c:member"} to `"mbcs"`,
> > - Set `PyConfig.filesystem_errors`{.interpreted-text role="c:member"} to `"replace"`.
> >
> > Initialized from the `PYTHONLEGACYWINDOWSFSENCODING`{.interpreted-text role="envvar"} environment variable value.
> >
> > Only available on Windows. `#ifdef MS_WINDOWS` macro can be used for Windows specific code.
> >
> > Default: `0`.
>
> > If non-zero, `Py_PreInitializeFromArgs`{.interpreted-text role="c:func"} and `Py_PreInitializeFromBytesArgs`{.interpreted-text role="c:func"} parse their `argv` argument the same way the regular Python parses command line arguments: see `Command Line Arguments <using-on-cmdline>`{.interpreted-text role="ref"}.
> >
> > Default: `1` in Python config, `0` in isolated config.
>
> > Use `environment variables <using-on-envvars>`{.interpreted-text role="ref"}? See `PyConfig.use_environment`{.interpreted-text role="c:member"}.
> >
> > Default: `1` in Python config and `0` in isolated config.
>
> > If non-zero, enable the `Python UTF-8 Mode <utf8-mode>`{.interpreted-text role="ref"}.
> >
> > Set to `0` or `1` by the `-X utf8 <-X>`{.interpreted-text role="option"} command line option and the `PYTHONUTF8`{.interpreted-text role="envvar"} environment variable.
> >
> > Default: `1`.

### Preinitialize Python with PyPreConfig {#c-preinit}

The preinitialization of Python:

- Set the Python memory allocators (`PyPreConfig.allocator`{.interpreted-text role="c:member"})
- Configure the LC_CTYPE locale (`locale encoding`{.interpreted-text role="term"})
- Set the `Python UTF-8 Mode <utf8-mode>`{.interpreted-text role="ref"} (`PyPreConfig.utf8_mode`{.interpreted-text role="c:member"})

The current preconfiguration (`PyPreConfig` type) is stored in `_PyRuntime.preconfig`.

Functions to preinitialize Python:

> Preinitialize Python from *preconfig* preconfiguration.
>
> *preconfig* must not be `NULL`.

> Preinitialize Python from *preconfig* preconfiguration.
>
> Parse *argv* command line arguments (bytes strings) if `~PyPreConfig.parse_argv`{.interpreted-text role="c:member"} of *preconfig* is non-zero.
>
> *preconfig* must not be `NULL`.

> Preinitialize Python from *preconfig* preconfiguration.
>
> Parse *argv* command line arguments (wide strings) if `~PyPreConfig.parse_argv`{.interpreted-text role="c:member"} of *preconfig* is non-zero.
>
> *preconfig* must not be `NULL`.

The caller is responsible to handle exceptions (error or exit) using `PyStatus_Exception`{.interpreted-text role="c:func"} and `Py_ExitStatusException`{.interpreted-text role="c:func"}.

For `Python Configuration <init-python-config>`{.interpreted-text role="ref"} (`PyPreConfig_InitPythonConfig`{.interpreted-text role="c:func"}), if Python is initialized with command line arguments, the command line arguments must also be passed to preinitialize Python, since they have an effect on the pre-configuration like encodings. For example, the `-X utf8 <-X>`{.interpreted-text role="option"} command line option enables the `Python UTF-8 Mode <utf8-mode>`{.interpreted-text role="ref"}.

`PyMem_SetAllocator()` can be called after `Py_PreInitialize`{.interpreted-text role="c:func"} and before `Py_InitializeFromConfig`{.interpreted-text role="c:func"} to install a custom memory allocator. It can be called before `Py_PreInitialize`{.interpreted-text role="c:func"} if `PyPreConfig.allocator`{.interpreted-text role="c:member"} is set to `PYMEM_ALLOCATOR_NOT_SET`.

Python memory allocation functions like `PyMem_RawMalloc`{.interpreted-text role="c:func"} must not be used before the Python preinitialization, whereas calling directly `malloc()` and `free()` is always safe. `Py_DecodeLocale`{.interpreted-text role="c:func"} must not be called before the Python preinitialization.

Example using the preinitialization to enable the `Python UTF-8 Mode <utf8-mode>`{.interpreted-text role="ref"}:

``` c
PyStatus status;
PyPreConfig preconfig;
PyPreConfig_InitPythonConfig(&preconfig);

preconfig.utf8_mode = 1;

status = Py_PreInitialize(&preconfig);
if (PyStatus_Exception(status)) {
    Py_ExitStatusException(status);
}

/* at this point, Python speaks UTF-8 */

Py_Initialize();
/* ... use Python API here ... */
Py_Finalize();
```

### PyConfig

> Structure containing most parameters to configure Python.
>
> When done, the `PyConfig_Clear`{.interpreted-text role="c:func"} function must be used to release the configuration memory.
>
> Structure methods:
>
> > Initialize configuration with the `Python Configuration
> > <init-python-config>`{.interpreted-text role="ref"}.
>
> > Initialize configuration with the `Isolated Configuration
> > <init-isolated-conf>`{.interpreted-text role="ref"}.
>
> > Copy the wide character string *str* into `*config_str`.
> >
> > `Preinitialize Python <c-preinit>`{.interpreted-text role="ref"} if needed.
>
> > Decode *str* using `Py_DecodeLocale`{.interpreted-text role="c:func"} and set the result into `*config_str`.
> >
> > `Preinitialize Python <c-preinit>`{.interpreted-text role="ref"} if needed.
>
> > Set command line arguments (`~PyConfig.argv`{.interpreted-text role="c:member"} member of *config*) from the *argv* list of wide character strings.
> >
> > `Preinitialize Python <c-preinit>`{.interpreted-text role="ref"} if needed.
>
> > Set command line arguments (`~PyConfig.argv`{.interpreted-text role="c:member"} member of *config*) from the *argv* list of bytes strings. Decode bytes using `Py_DecodeLocale`{.interpreted-text role="c:func"}.
> >
> > `Preinitialize Python <c-preinit>`{.interpreted-text role="ref"} if needed.
>
> > Set the list of wide strings *list* to *length* and *items*.
> >
> > `Preinitialize Python <c-preinit>`{.interpreted-text role="ref"} if needed.
>
> > Read all Python configuration.
> >
> > Fields which are already initialized are left unchanged.
> >
> > Fields for `path configuration <init-path-config>`{.interpreted-text role="ref"} are no longer calculated or modified when calling this function, as of Python 3.11.
> >
> > The `PyConfig_Read`{.interpreted-text role="c:func"} function only parses `PyConfig.argv`{.interpreted-text role="c:member"} arguments once: `PyConfig.parse_argv`{.interpreted-text role="c:member"} is set to `2` after arguments are parsed. Since Python arguments are stripped from `PyConfig.argv`{.interpreted-text role="c:member"}, parsing arguments twice would parse the application options as Python options.
> >
> > `Preinitialize Python <c-preinit>`{.interpreted-text role="ref"} if needed.
> >
> > ::: versionchanged
> > 3.10 The `PyConfig.argv`{.interpreted-text role="c:member"} arguments are now only parsed once, `PyConfig.parse_argv`{.interpreted-text role="c:member"} is set to `2` after arguments are parsed, and arguments are only parsed if `PyConfig.parse_argv`{.interpreted-text role="c:member"} equals `1`.
> > :::
> >
> > ::: versionchanged
> > 3.11 `PyConfig_Read`{.interpreted-text role="c:func"} no longer calculates all paths, and so fields listed under `Python Path Configuration <init-path-config>`{.interpreted-text role="ref"} may no longer be updated until `Py_InitializeFromConfig`{.interpreted-text role="c:func"} is called.
> > :::
>
> > Release configuration memory.
>
> Most `PyConfig` methods `preinitialize Python <c-preinit>`{.interpreted-text role="ref"} if needed. In that case, the Python preinitialization configuration (`PyPreConfig`{.interpreted-text role="c:type"}) is based on the `PyConfig`{.interpreted-text role="c:type"}. If configuration fields which are in common with `PyPreConfig`{.interpreted-text role="c:type"} are tuned, they must be set before calling a `PyConfig`{.interpreted-text role="c:type"} method:
>
> - `PyConfig.dev_mode`{.interpreted-text role="c:member"}
> - `PyConfig.isolated`{.interpreted-text role="c:member"}
> - `PyConfig.parse_argv`{.interpreted-text role="c:member"}
> - `PyConfig.use_environment`{.interpreted-text role="c:member"}
>
> Moreover, if `PyConfig_SetArgv`{.interpreted-text role="c:func"} or `PyConfig_SetBytesArgv`{.interpreted-text role="c:func"} is used, this method must be called before other methods, since the preinitialization configuration depends on command line arguments (if `~PyConfig.parse_argv`{.interpreted-text role="c:member"} is non-zero).
>
> The caller of these methods is responsible to handle exceptions (error or exit) using `PyStatus_Exception()` and `Py_ExitStatusException()`.
>
> Structure fields:
>
> > ::: index
> > single: main() single: argv (in module sys)
> > :::
> >
> > Set `sys.argv`{.interpreted-text role="data"} command line arguments based on `~PyConfig.argv`{.interpreted-text role="c:member"}. These parameters are similar to those passed to the program\'s `main`{.interpreted-text role="c:func"} function with the difference that the first entry should refer to the script file to be executed rather than the executable hosting the Python interpreter. If there isn\'t a script that will be run, the first entry in `~PyConfig.argv`{.interpreted-text role="c:member"} can be an empty string.
> >
> > Set `~PyConfig.parse_argv`{.interpreted-text role="c:member"} to `1` to parse `~PyConfig.argv`{.interpreted-text role="c:member"} the same way the regular Python parses Python command line arguments and then to strip Python arguments from `~PyConfig.argv`{.interpreted-text role="c:member"}.
> >
> > If `~PyConfig.argv`{.interpreted-text role="c:member"} is empty, an empty string is added to ensure that `sys.argv`{.interpreted-text role="data"} always exists and is never empty.
> >
> > Default: `NULL`.
> >
> > See also the `~PyConfig.orig_argv`{.interpreted-text role="c:member"} member.
>
> > If equals to zero, `Py_RunMain()` prepends a potentially unsafe path to `sys.path`{.interpreted-text role="data"} at startup:
> >
> > - If `argv[0] <PyConfig.argv>`{.interpreted-text role="c:member"} is equal to `L"-m"` (`python -m module`), prepend the current working directory.
> > - If running a script (`python script.py`), prepend the script\'s directory. If it\'s a symbolic link, resolve symbolic links.
> > - Otherwise (`python -c code` and `python`), prepend an empty string, which means the current working directory.
> >
> > Set to `1` by the `-P`{.interpreted-text role="option"} command line option and the `PYTHONSAFEPATH`{.interpreted-text role="envvar"} environment variable.
> >
> > Default: `0` in Python config, `1` in isolated config.
> >
> > ::: versionadded
> > 3.11
> > :::
>
> > `sys.base_exec_prefix`{.interpreted-text role="data"}.
> >
> > Default: `NULL`.
> >
> > Part of the `Python Path Configuration <init-path-config>`{.interpreted-text role="ref"} output.
> >
> > See also `PyConfig.exec_prefix`{.interpreted-text role="c:member"}.
>
> > Python base executable: `sys._base_executable`{.interpreted-text role="data"}.
> >
> > Set by the `__PYVENV_LAUNCHER__`{.interpreted-text role="envvar"} environment variable.
> >
> > Set from `PyConfig.executable`{.interpreted-text role="c:member"} if `NULL`.
> >
> > Default: `NULL`.
> >
> > Part of the `Python Path Configuration <init-path-config>`{.interpreted-text role="ref"} output.
> >
> > See also `PyConfig.executable`{.interpreted-text role="c:member"}.
>
> > `sys.base_prefix`{.interpreted-text role="data"}.
> >
> > Default: `NULL`.
> >
> > Part of the `Python Path Configuration <init-path-config>`{.interpreted-text role="ref"} output.
> >
> > See also `PyConfig.prefix`{.interpreted-text role="c:member"}.
>
> > If equals to `0` and `~PyConfig.configure_c_stdio`{.interpreted-text role="c:member"} is non-zero, disable buffering on the C streams stdout and stderr.
> >
> > Set to `0` by the `-u`{.interpreted-text role="option"} command line option and the `PYTHONUNBUFFERED`{.interpreted-text role="envvar"} environment variable.
> >
> > stdin is always opened in buffered mode.
> >
> > Default: `1`.
>
> > If equals to `1`, issue a warning when comparing `bytes`{.interpreted-text role="class"} or `bytearray`{.interpreted-text role="class"} with `str`{.interpreted-text role="class"}, or comparing `bytes`{.interpreted-text role="class"} with `int`{.interpreted-text role="class"}.
> >
> > If equal or greater to `2`, raise a `BytesWarning`{.interpreted-text role="exc"} exception in these cases.
> >
> > Incremented by the `-b`{.interpreted-text role="option"} command line option.
> >
> > Default: `0`.
> >
> > ::: deprecated-removed
> > 3.15 3.17
> >
> > The `-b`{.interpreted-text role="option"} and `!-bb`{.interpreted-text role="option"} options will become no-op in 3.17. `~PyConfig.bytes_warning`{.interpreted-text role="c:member"} member will be removed in 3.17.
> > :::
>
> > If non-zero, emit a `EncodingWarning`{.interpreted-text role="exc"} warning when `io.TextIOWrapper`{.interpreted-text role="class"} uses its default encoding. See `io-encoding-warning`{.interpreted-text role="ref"} for details.
> >
> > Default: `0`.
> >
> > ::: versionadded
> > 3.10
> > :::
>
> > If equals to `0`, disables the inclusion of the end line and column mappings in code objects. Also disables traceback printing carets to specific error locations.
> >
> > Set to `0` by the `PYTHONNODEBUGRANGES`{.interpreted-text role="envvar"} environment variable and by the `-X no_debug_ranges <-X>`{.interpreted-text role="option"} command line option.
> >
> > Default: `1`.
> >
> > ::: versionadded
> > 3.11
> > :::
>
> > Control the validation behavior of hash-based `.pyc` files: value of the `--check-hash-based-pycs`{.interpreted-text role="option"} command line option.
> >
> > Valid values:
> >
> > - `L"always"`: Hash the source file for invalidation regardless of value of the \'check_source\' flag.
> > - `L"never"`: Assume that hash-based pycs always are valid.
> > - `L"default"`: The \'check_source\' flag in hash-based pycs determines invalidation.
> >
> > Default: `L"default"`.
> >
> > See also `552`{.interpreted-text role="pep"} \"Deterministic pycs\".
>
> > If non-zero, configure C standard streams:
> >
> > - On Windows, set the binary mode (`O_BINARY`) on stdin, stdout and stderr.
> > - If `~PyConfig.buffered_stdio`{.interpreted-text role="c:member"} equals zero, disable buffering of stdin, stdout and stderr streams.
> > - If `~PyConfig.interactive`{.interpreted-text role="c:member"} is non-zero, enable stream buffering on stdin and stdout (only stdout on Windows).
> >
> > Default: `1` in Python config, `0` in isolated config.
>
> > If non-zero, enable the `Python Development Mode <devmode>`{.interpreted-text role="ref"}.
> >
> > Set to `1` by the `-X dev <-X>`{.interpreted-text role="option"} option and the `PYTHONDEVMODE`{.interpreted-text role="envvar"} environment variable.
> >
> > Default: `-1` in Python mode, `0` in isolated mode.
>
> > Dump Python references?
> >
> > If non-zero, dump all objects which are still alive at exit.
> >
> > Set to `1` by the `PYTHONDUMPREFS`{.interpreted-text role="envvar"} environment variable.
> >
> > Needs a special build of Python with the `Py_TRACE_REFS` macro defined: see the `configure --with-trace-refs option <--with-trace-refs>`{.interpreted-text role="option"}.
> >
> > Default: `0`.
>
> > Filename where to dump Python references.
> >
> > Set by the `PYTHONDUMPREFSFILE`{.interpreted-text role="envvar"} environment variable.
> >
> > Default: `NULL`.
> >
> > ::: versionadded
> > 3.11
> > :::
>
> > The site-specific directory prefix where the platform-dependent Python files are installed: `sys.exec_prefix`{.interpreted-text role="data"}.
> >
> > Default: `NULL`.
> >
> > Part of the `Python Path Configuration <init-path-config>`{.interpreted-text role="ref"} output.
> >
> > See also `PyConfig.base_exec_prefix`{.interpreted-text role="c:member"}.
>
> > The absolute path of the executable binary for the Python interpreter: `sys.executable`{.interpreted-text role="data"}.
> >
> > Default: `NULL`.
> >
> > Part of the `Python Path Configuration <init-path-config>`{.interpreted-text role="ref"} output.
> >
> > See also `PyConfig.base_executable`{.interpreted-text role="c:member"}.
>
> > Enable faulthandler?
> >
> > If non-zero, call `faulthandler.enable`{.interpreted-text role="func"} at startup.
> >
> > Set to `1` by `-X faulthandler <-X>`{.interpreted-text role="option"} and the `PYTHONFAULTHANDLER`{.interpreted-text role="envvar"} environment variable.
> >
> > Default: `-1` in Python mode, `0` in isolated mode.
>
> > `Filesystem encoding <filesystem encoding and error handler>`{.interpreted-text role="term"}: `sys.getfilesystemencoding`{.interpreted-text role="func"}.
> >
> > On macOS, Android and VxWorks: use `"utf-8"` by default.
> >
> > On Windows: use `"utf-8"` by default, or `"mbcs"` if `~PyPreConfig.legacy_windows_fs_encoding`{.interpreted-text role="c:member"} of `PyPreConfig`{.interpreted-text role="c:type"} is non-zero.
> >
> > Default encoding on other platforms:
> >
> > - `"utf-8"` if `PyPreConfig.utf8_mode`{.interpreted-text role="c:member"} is non-zero.
> > - `"ascii"` if Python detects that `nl_langinfo(CODESET)` announces the ASCII encoding, whereas the `mbstowcs()` function decodes from a different encoding (usually Latin1).
> > - `"utf-8"` if `nl_langinfo(CODESET)` returns an empty string.
> > - Otherwise, use the `locale encoding`{.interpreted-text role="term"}: `nl_langinfo(CODESET)` result.
> >
> > At Python startup, the encoding name is normalized to the Python codec name. For example, `"ANSI_X3.4-1968"` is replaced with `"ascii"`.
> >
> > See also the `~PyConfig.filesystem_errors`{.interpreted-text role="c:member"} member.
>
> > `Filesystem error handler <filesystem encoding and error handler>`{.interpreted-text role="term"}: `sys.getfilesystemencodeerrors`{.interpreted-text role="func"}.
> >
> > On Windows: use `"surrogatepass"` by default, or `"replace"` if `~PyPreConfig.legacy_windows_fs_encoding`{.interpreted-text role="c:member"} of `PyPreConfig`{.interpreted-text role="c:type"} is non-zero.
> >
> > On other platforms: use `"surrogateescape"` by default.
> >
> > Supported error handlers:
> >
> > - `"strict"`
> > - `"surrogateescape"`
> > - `"surrogatepass"` (only supported with the UTF-8 encoding)
> >
> > See also the `~PyConfig.filesystem_encoding`{.interpreted-text role="c:member"} member.
>
> > If non-zero, use frozen modules.
> >
> > Set by the `PYTHON_FROZEN_MODULES`{.interpreted-text role="envvar"} environment variable.
> >
> > Default: `1` in a release build, or `0` in a `debug build
> > <debug-build>`{.interpreted-text role="ref"}.
>
> > Randomized hash function seed.
> >
> > If `~PyConfig.use_hash_seed`{.interpreted-text role="c:member"} is zero, a seed is chosen randomly at Python startup, and `~PyConfig.hash_seed`{.interpreted-text role="c:member"} is ignored.
> >
> > Set by the `PYTHONHASHSEED`{.interpreted-text role="envvar"} environment variable.
> >
> > Default *use_hash_seed* value: `-1` in Python mode, `0` in isolated mode.
>
> > Set the default Python \"home\" directory, that is, the location of the standard Python libraries (see `PYTHONHOME`{.interpreted-text role="envvar"}).
> >
> > Set by the `PYTHONHOME`{.interpreted-text role="envvar"} environment variable.
> >
> > Default: `NULL`.
> >
> > Part of the `Python Path Configuration <init-path-config>`{.interpreted-text role="ref"} input.
>
> > If `1`, profile import time. If `2`, include additional output that indicates when an imported module has already been loaded.
> >
> > Set by the `-X importtime <-X>`{.interpreted-text role="option"} option and the `PYTHONPROFILEIMPORTTIME`{.interpreted-text role="envvar"} environment variable.
> >
> > Default: `0`.
> >
> > ::: versionchanged
> > 3.14
> >
> > Added support for `import_time = 2`
> > :::
>
> > Enter interactive mode after executing a script or a command.
> >
> > If greater than `0`, enable inspect: when a script is passed as first argument or the -c option is used, enter interactive mode after executing the script or the command, even when `sys.stdin`{.interpreted-text role="data"} does not appear to be a terminal.
> >
> > Incremented by the `-i`{.interpreted-text role="option"} command line option. Set to `1` if the `PYTHONINSPECT`{.interpreted-text role="envvar"} environment variable is non-empty.
> >
> > Default: `0`.
>
> > Install Python signal handlers?
> >
> > Default: `1` in Python mode, `0` in isolated mode.
>
> > If greater than `0`, enable the interactive mode (REPL).
> >
> > Incremented by the `-i`{.interpreted-text role="option"} command line option.
> >
> > Default: `0`.
>
> > Configures the `integer string conversion length limitation
> > <int_max_str_digits>`{.interpreted-text role="ref"}. An initial value of `-1` means the value will be taken from the command line or environment or otherwise default to 4300 (`sys.int_info.default_max_str_digits`{.interpreted-text role="data"}). A value of `0` disables the limitation. Values greater than zero but less than 640 (`sys.int_info.str_digits_check_threshold`{.interpreted-text role="data"}) are unsupported and will produce an error.
> >
> > Configured by the `-X int_max_str_digits <-X>`{.interpreted-text role="option"} command line flag or the `PYTHONINTMAXSTRDIGITS`{.interpreted-text role="envvar"} environment variable.
> >
> > Default: `-1` in Python mode. 4300 (`sys.int_info.default_max_str_digits`{.interpreted-text role="data"}) in isolated mode.
> >
> > ::: versionadded
> > 3.12
> > :::
>
> > If the value of `~PyConfig.cpu_count`{.interpreted-text role="c:member"} is not `-1` then it will override the return values of `os.cpu_count`{.interpreted-text role="func"}, `os.process_cpu_count`{.interpreted-text role="func"}, and `multiprocessing.cpu_count`{.interpreted-text role="func"}.
> >
> > Configured by the `-X cpu_count={n|default}`{.interpreted-text role="samp"} command line flag or the `PYTHON_CPU_COUNT`{.interpreted-text role="envvar"} environment variable.
> >
> > Default: `-1`.
> >
> > ::: versionadded
> > 3.13
> > :::
>
> > If greater than `0`, enable isolated mode:
> >
> > - Set `~PyConfig.safe_path`{.interpreted-text role="c:member"} to `1`: don\'t prepend a potentially unsafe path to `sys.path`{.interpreted-text role="data"} at Python startup, such as the current directory, the script\'s directory or an empty string.
> > - Set `~PyConfig.use_environment`{.interpreted-text role="c:member"} to `0`: ignore `PYTHON` environment variables.
> > - Set `~PyConfig.user_site_directory`{.interpreted-text role="c:member"} to `0`: don\'t add the user site directory to `sys.path`{.interpreted-text role="data"}.
> > - Python REPL doesn\'t import `readline`{.interpreted-text role="mod"} nor enable default readline configuration on interactive prompts.
> >
> > Set to `1` by the `-I`{.interpreted-text role="option"} command line option.
> >
> > Default: `0` in Python mode, `1` in isolated mode.
> >
> > See also the `Isolated Configuration <init-isolated-conf>`{.interpreted-text role="ref"} and `PyPreConfig.isolated`{.interpreted-text role="c:member"}.
>
> > If non-zero, use `io.FileIO`{.interpreted-text role="class"} instead of `!io._WindowsConsoleIO`{.interpreted-text role="class"} for `sys.stdin`{.interpreted-text role="data"}, `sys.stdout`{.interpreted-text role="data"} and `sys.stderr`{.interpreted-text role="data"}.
> >
> > Set to `1` if the `PYTHONLEGACYWINDOWSSTDIO`{.interpreted-text role="envvar"} environment variable is set to a non-empty string.
> >
> > Only available on Windows. `#ifdef MS_WINDOWS` macro can be used for Windows specific code.
> >
> > Default: `0`.
> >
> > See also the `528`{.interpreted-text role="pep"} (Change Windows console encoding to UTF-8).
>
> > If non-zero, dump statistics on `Python pymalloc memory allocator
> > <pymalloc>`{.interpreted-text role="ref"} at exit.
> >
> > Set to `1` by the `PYTHONMALLOCSTATS`{.interpreted-text role="envvar"} environment variable.
> >
> > The option is ignored if Python is `configured using
> > the --without-pymalloc option <--without-pymalloc>`{.interpreted-text role="option"}.
> >
> > Default: `0`.
>
> > Platform library directory name: `sys.platlibdir`{.interpreted-text role="data"}.
> >
> > Set by the `PYTHONPLATLIBDIR`{.interpreted-text role="envvar"} environment variable.
> >
> > Default: value of the `PLATLIBDIR` macro which is set by the `configure --with-platlibdir option <--with-platlibdir>`{.interpreted-text role="option"} (default: `"lib"`, or `"DLLs"` on Windows).
> >
> > Part of the `Python Path Configuration <init-path-config>`{.interpreted-text role="ref"} input.
> >
> > ::: versionadded
> > 3.9
> > :::
> >
> > ::: versionchanged
> > 3.11 This macro is now used on Windows to locate the standard library extension modules, typically under `DLLs`. However, for compatibility, note that this value is ignored for any non-standard layouts, including in-tree builds and virtual environments.
> > :::
>
> > Module search paths (`sys.path`{.interpreted-text role="data"}) as a string separated by `DELIM` (`os.pathsep`{.interpreted-text role="data"}).
> >
> > Set by the `PYTHONPATH`{.interpreted-text role="envvar"} environment variable.
> >
> > Default: `NULL`.
> >
> > Part of the `Python Path Configuration <init-path-config>`{.interpreted-text role="ref"} input.
>
> > Module search paths: `sys.path`{.interpreted-text role="data"}.
> >
> > If `~PyConfig.module_search_paths_set`{.interpreted-text role="c:member"} is equal to `0`, `Py_InitializeFromConfig`{.interpreted-text role="c:func"} will replace `~PyConfig.module_search_paths`{.interpreted-text role="c:member"} and sets `~PyConfig.module_search_paths_set`{.interpreted-text role="c:member"} to `1`.
> >
> > Default: empty list (`module_search_paths`) and `0` (`module_search_paths_set`).
> >
> > Part of the `Python Path Configuration <init-path-config>`{.interpreted-text role="ref"} output.
>
> > Compilation optimization level:
> >
> > - `0`: Peephole optimizer, set `__debug__` to `True`.
> > - `1`: Level 0, remove assertions, set `__debug__` to `False`.
> > - `2`: Level 1, strip docstrings.
> >
> > Incremented by the `-O`{.interpreted-text role="option"} command line option. Set to the `PYTHONOPTIMIZE`{.interpreted-text role="envvar"} environment variable value.
> >
> > Default: `0`.
>
> > The list of the original command line arguments passed to the Python executable: `sys.orig_argv`{.interpreted-text role="data"}.
> >
> > If `~PyConfig.orig_argv`{.interpreted-text role="c:member"} list is empty and `~PyConfig.argv`{.interpreted-text role="c:member"} is not a list only containing an empty string, `PyConfig_Read`{.interpreted-text role="c:func"} copies `~PyConfig.argv`{.interpreted-text role="c:member"} into `~PyConfig.orig_argv`{.interpreted-text role="c:member"} before modifying `~PyConfig.argv`{.interpreted-text role="c:member"} (if `~PyConfig.parse_argv`{.interpreted-text role="c:member"} is non-zero).
> >
> > See also the `~PyConfig.argv`{.interpreted-text role="c:member"} member and the `Py_GetArgcArgv`{.interpreted-text role="c:func"} function.
> >
> > Default: empty list.
> >
> > ::: versionadded
> > 3.10
> > :::
>
> > Parse command line arguments?
> >
> > If equals to `1`, parse `~PyConfig.argv`{.interpreted-text role="c:member"} the same way the regular Python parses `command line arguments <using-on-cmdline>`{.interpreted-text role="ref"}, and strip Python arguments from `~PyConfig.argv`{.interpreted-text role="c:member"}.
> >
> > The `PyConfig_Read`{.interpreted-text role="c:func"} function only parses `PyConfig.argv`{.interpreted-text role="c:member"} arguments once: `PyConfig.parse_argv`{.interpreted-text role="c:member"} is set to `2` after arguments are parsed. Since Python arguments are stripped from `PyConfig.argv`{.interpreted-text role="c:member"}, parsing arguments twice would parse the application options as Python options.
> >
> > Default: `1` in Python mode, `0` in isolated mode.
> >
> > ::: versionchanged
> > 3.10 The `PyConfig.argv`{.interpreted-text role="c:member"} arguments are now only parsed if `PyConfig.parse_argv`{.interpreted-text role="c:member"} equals to `1`.
> > :::
>
> > Parser debug mode. If greater than `0`, turn on parser debugging output (for expert only, depending on compilation options).
> >
> > Incremented by the `-d`{.interpreted-text role="option"} command line option. Set to the `PYTHONDEBUG`{.interpreted-text role="envvar"} environment variable value.
> >
> > Needs a `debug build of Python <debug-build>`{.interpreted-text role="ref"} (the `Py_DEBUG` macro must be defined).
> >
> > Default: `0`.
>
> > If non-zero, calculation of path configuration is allowed to log warnings into `stderr`. If equals to `0`, suppress these warnings.
> >
> > Default: `1` in Python mode, `0` in isolated mode.
> >
> > Part of the `Python Path Configuration <init-path-config>`{.interpreted-text role="ref"} input.
> >
> > ::: versionchanged
> > 3.11 Now also applies on Windows.
> > :::
>
> > The site-specific directory prefix where the platform independent Python files are installed: `sys.prefix`{.interpreted-text role="data"}.
> >
> > Default: `NULL`.
> >
> > Part of the `Python Path Configuration <init-path-config>`{.interpreted-text role="ref"} output.
> >
> > See also `PyConfig.base_prefix`{.interpreted-text role="c:member"}.
>
> > Program name used to initialize `~PyConfig.executable`{.interpreted-text role="c:member"} and in early error messages during Python initialization.
> >
> > - On macOS, use `PYTHONEXECUTABLE`{.interpreted-text role="envvar"} environment variable if set.
> > - If the `WITH_NEXT_FRAMEWORK` macro is defined, use `__PYVENV_LAUNCHER__`{.interpreted-text role="envvar"} environment variable if set.
> > - Use `argv[0]` of `~PyConfig.argv`{.interpreted-text role="c:member"} if available and non-empty.
> > - Otherwise, use `L"python"` on Windows, or `L"python3"` on other platforms.
> >
> > Default: `NULL`.
> >
> > Part of the `Python Path Configuration <init-path-config>`{.interpreted-text role="ref"} input.
>
> > Directory where cached `.pyc` files are written: `sys.pycache_prefix`{.interpreted-text role="data"}.
> >
> > Set by the `-X pycache_prefix=PATH <-X>`{.interpreted-text role="option"} command line option and the `PYTHONPYCACHEPREFIX`{.interpreted-text role="envvar"} environment variable. The command-line option takes precedence.
> >
> > If `NULL`, `sys.pycache_prefix`{.interpreted-text role="data"} is set to `None`.
> >
> > Default: `NULL`.
>
> > Quiet mode. If greater than `0`, don\'t display the copyright and version at Python startup in interactive mode.
> >
> > Incremented by the `-q`{.interpreted-text role="option"} command line option.
> >
> > Default: `0`.
>
> > Value of the `-c`{.interpreted-text role="option"} command line option.
> >
> > Used by `Py_RunMain`{.interpreted-text role="c:func"}.
> >
> > Default: `NULL`.
>
> > Filename passed on the command line: trailing command line argument without `-c`{.interpreted-text role="option"} or `-m`{.interpreted-text role="option"}. It is used by the `Py_RunMain`{.interpreted-text role="c:func"} function.
> >
> > For example, it is set to `script.py` by the `python3 script.py arg` command line.
> >
> > See also the `PyConfig.skip_source_first_line`{.interpreted-text role="c:member"} option.
> >
> > Default: `NULL`.
>
> > Value of the `-m`{.interpreted-text role="option"} command line option.
> >
> > Used by `Py_RunMain`{.interpreted-text role="c:func"}.
> >
> > Default: `NULL`.
>
> > `package.module` path to module that should be imported before `site.py` is run.
> >
> > Set by the `-X presite=package.module <-X>`{.interpreted-text role="option"} command-line option and the `PYTHON_PRESITE`{.interpreted-text role="envvar"} environment variable. The command-line option takes precedence.
> >
> > Needs a `debug build of Python <debug-build>`{.interpreted-text role="ref"} (the `Py_DEBUG` macro must be defined).
> >
> > Default: `NULL`.
>
> > Show total reference count at exit (excluding `immortal`{.interpreted-text role="term"} objects)?
> >
> > Set to `1` by `-X showrefcount <-X>`{.interpreted-text role="option"} command line option.
> >
> > Needs a `debug build of Python <debug-build>`{.interpreted-text role="ref"} (the `Py_REF_DEBUG` macro must be defined).
> >
> > Default: `0`.
>
> > Import the `site`{.interpreted-text role="mod"} module at startup?
> >
> > If equal to zero, disable the import of the module site and the site-dependent manipulations of `sys.path`{.interpreted-text role="data"} that it entails.
> >
> > Also disable these manipulations if the `site`{.interpreted-text role="mod"} module is explicitly imported later (call `site.main`{.interpreted-text role="func"} if you want them to be triggered).
> >
> > Set to `0` by the `-S`{.interpreted-text role="option"} command line option.
> >
> > `sys.flags.no_site <sys.flags>`{.interpreted-text role="data"} is set to the inverted value of `~PyConfig.site_import`{.interpreted-text role="c:member"}.
> >
> > Default: `1`.
>
> > If non-zero, skip the first line of the `PyConfig.run_filename`{.interpreted-text role="c:member"} source.
> >
> > It allows the usage of non-Unix forms of `#!cmd`. This is intended for a DOS specific hack only.
> >
> > Set to `1` by the `-x`{.interpreted-text role="option"} command line option.
> >
> > Default: `0`.
>
> > Encoding and encoding errors of `sys.stdin`{.interpreted-text role="data"}, `sys.stdout`{.interpreted-text role="data"} and `sys.stderr`{.interpreted-text role="data"} (but `sys.stderr`{.interpreted-text role="data"} always uses `"backslashreplace"` error handler).
> >
> > Use the `PYTHONIOENCODING`{.interpreted-text role="envvar"} environment variable if it is non-empty.
> >
> > Default encoding:
> >
> > - `"UTF-8"` if `PyPreConfig.utf8_mode`{.interpreted-text role="c:member"} is non-zero.
> > - Otherwise, use the `locale encoding`{.interpreted-text role="term"}.
> >
> > Default error handler:
> >
> > - On Windows: use `"surrogateescape"`.
> > - `"surrogateescape"` if `PyPreConfig.utf8_mode`{.interpreted-text role="c:member"} is non-zero, or if the LC_CTYPE locale is \"C\" or \"POSIX\".
> > - `"strict"` otherwise.
> >
> > See also `PyConfig.legacy_windows_stdio`{.interpreted-text role="c:member"}.
>
> > Enable tracemalloc?
> >
> > If non-zero, call `tracemalloc.start`{.interpreted-text role="func"} at startup.
> >
> > Set by `-X tracemalloc=N <-X>`{.interpreted-text role="option"} command line option and by the `PYTHONTRACEMALLOC`{.interpreted-text role="envvar"} environment variable.
> >
> > Default: `-1` in Python mode, `0` in isolated mode.
>
> > Enable the Linux `perf` profiler support?
> >
> > If equals to `1`, enable support for the Linux `perf` profiler.
> >
> > If equals to `2`, enable support for the Linux `perf` profiler with DWARF JIT support.
> >
> > Set to `1` by `-X perf <-X>`{.interpreted-text role="option"} command-line option and the `PYTHONPERFSUPPORT`{.interpreted-text role="envvar"} environment variable.
> >
> > Set to `2` by the `-X perf_jit <-X>`{.interpreted-text role="option"} command-line option and the `PYTHON_PERF_JIT_SUPPORT`{.interpreted-text role="envvar"} environment variable.
> >
> > Default: `-1`.
> >
> > ::: seealso
> > See `perf_profiling`{.interpreted-text role="ref"} for more information.
> > :::
> >
> > ::: versionadded
> > 3.12
> > :::
>
> > Directory of the Python standard library.
> >
> > Default: `NULL`.
> >
> > ::: versionadded
> > 3.11
> > :::
>
> > Use `environment variables <using-on-envvars>`{.interpreted-text role="ref"}?
> >
> > If equals to zero, ignore the `environment variables
> > <using-on-envvars>`{.interpreted-text role="ref"}.
> >
> > Set to `0` by the `-E`{.interpreted-text role="option"} environment variable.
> >
> > Default: `1` in Python config and `0` in isolated config.
>
> > If non-zero, `stdout` and `stderr` will be redirected to the system log.
> >
> > Only available on macOS 10.12 and later, and on iOS.
> >
> > Default: `0` (don\'t use the system log) on macOS; `1` on iOS (use the system log).
> >
> > ::: versionadded
> > 3.14
> > :::
>
> > If non-zero, add the user site directory to `sys.path`{.interpreted-text role="data"}.
> >
> > Set to `0` by the `-s`{.interpreted-text role="option"} and `-I`{.interpreted-text role="option"} command line options.
> >
> > Set to `0` by the `PYTHONNOUSERSITE`{.interpreted-text role="envvar"} environment variable.
> >
> > Default: `1` in Python mode, `0` in isolated mode.
>
> > Verbose mode. If greater than `0`, print a message each time a module is imported, showing the place (filename or built-in module) from which it is loaded.
> >
> > If greater than or equal to `2`, print a message for each file that is checked for when searching for a module. Also provides information on module cleanup at exit.
> >
> > Incremented by the `-v`{.interpreted-text role="option"} command line option.
> >
> > Set by the `PYTHONVERBOSE`{.interpreted-text role="envvar"} environment variable value.
> >
> > Default: `0`.
>
> > Options of the `warnings`{.interpreted-text role="mod"} module to build warnings filters, lowest to highest priority: `sys.warnoptions`{.interpreted-text role="data"}.
> >
> > The `warnings`{.interpreted-text role="mod"} module adds `sys.warnoptions`{.interpreted-text role="data"} in the reverse order: the last `PyConfig.warnoptions`{.interpreted-text role="c:member"} item becomes the first item of `warnings.filters`{.interpreted-text role="data"} which is checked first (highest priority).
> >
> > The `-W`{.interpreted-text role="option"} command line options adds its value to `~PyConfig.warnoptions`{.interpreted-text role="c:member"}, it can be used multiple times.
> >
> > The `PYTHONWARNINGS`{.interpreted-text role="envvar"} environment variable can also be used to add warning options. Multiple options can be specified, separated by commas (`,`).
> >
> > Default: empty list.
>
> > If equal to `0`, Python won\'t try to write `.pyc` files on the import of source modules.
> >
> > Set to `0` by the `-B`{.interpreted-text role="option"} command line option and the `PYTHONDONTWRITEBYTECODE`{.interpreted-text role="envvar"} environment variable.
> >
> > `sys.dont_write_bytecode`{.interpreted-text role="data"} is initialized to the inverted value of `~PyConfig.write_bytecode`{.interpreted-text role="c:member"}.
> >
> > Default: `1`.
>
> > Values of the `-X`{.interpreted-text role="option"} command line options: `sys._xoptions`{.interpreted-text role="data"}.
> >
> > Default: empty list.
>
> > If non-zero, write performance statistics at Python exit.
> >
> > Need a special build with the `Py_STATS` macro: see `--enable-pystats`{.interpreted-text role="option"}.
> >
> > Default: `0`.

If `~PyConfig.parse_argv`{.interpreted-text role="c:member"} is non-zero, `~PyConfig.argv`{.interpreted-text role="c:member"} arguments are parsed the same way the regular Python parses `command line
arguments <using-on-cmdline>`{.interpreted-text role="ref"}, and Python arguments are stripped from `~PyConfig.argv`{.interpreted-text role="c:member"}.

The `~PyConfig.xoptions`{.interpreted-text role="c:member"} options are parsed to set other options: see the `-X`{.interpreted-text role="option"} command line option.

::: versionchanged
3.9

The `show_alloc_count` field has been removed.
:::

### Initialization with PyConfig {#init-from-config}

Initializing the interpreter from a populated configuration struct is handled by calling `Py_InitializeFromConfig`{.interpreted-text role="c:func"}.

The caller is responsible to handle exceptions (error or exit) using `PyStatus_Exception`{.interpreted-text role="c:func"} and `Py_ExitStatusException`{.interpreted-text role="c:func"}.

If `PyImport_FrozenModules`{.interpreted-text role="c:func"}, `PyImport_AppendInittab`{.interpreted-text role="c:func"} or `PyImport_ExtendInittab`{.interpreted-text role="c:func"} are used, they must be set or called after Python preinitialization and before the Python initialization. If Python is initialized multiple times, `PyImport_AppendInittab`{.interpreted-text role="c:func"} or `PyImport_ExtendInittab`{.interpreted-text role="c:func"} must be called before each Python initialization.

The current configuration (`PyConfig` type) is stored in `PyInterpreterState.config`.

Example setting the program name:

``` c
void init_python(void)
{
    PyStatus status;

    PyConfig config;
    PyConfig_InitPythonConfig(&config);

    /* Set the program name. Implicitly preinitialize Python. */
    status = PyConfig_SetString(&config, &config.program_name,
                                L"/path/to/my_program");
    if (PyStatus_Exception(status)) {
        goto exception;
    }

    status = Py_InitializeFromConfig(&config);
    if (PyStatus_Exception(status)) {
        goto exception;
    }
    PyConfig_Clear(&config);
    return;

exception:
    PyConfig_Clear(&config);
    Py_ExitStatusException(status);
}
```

More complete example modifying the default configuration, read the configuration, and then override some parameters. Note that since 3.11, many parameters are not calculated until initialization, and so values cannot be read from the configuration structure. Any values set before initialize is called will be left unchanged by initialization:

``` c
PyStatus init_python(const char *program_name)
{
    PyStatus status;

    PyConfig config;
    PyConfig_InitPythonConfig(&config);

    /* Set the program name before reading the configuration
       (decode byte string from the locale encoding).

       Implicitly preinitialize Python. */
    status = PyConfig_SetBytesString(&config, &config.program_name,
                                     program_name);
    if (PyStatus_Exception(status)) {
        goto done;
    }

    /* Read all configuration at once */
    status = PyConfig_Read(&config);
    if (PyStatus_Exception(status)) {
        goto done;
    }

    /* Specify sys.path explicitly */
    /* If you want to modify the default set of paths, finish
       initialization first and then use PySys_GetAttrString("path") */
    config.module_search_paths_set = 1;
    status = PyWideStringList_Append(&config.module_search_paths,
                                     L"/path/to/stdlib");
    if (PyStatus_Exception(status)) {
        goto done;
    }
    status = PyWideStringList_Append(&config.module_search_paths,
                                     L"/path/to/more/modules");
    if (PyStatus_Exception(status)) {
        goto done;
    }

    /* Override executable computed by PyConfig_Read() */
    status = PyConfig_SetString(&config, &config.executable,
                                L"/path/to/my_executable");
    if (PyStatus_Exception(status)) {
        goto done;
    }

    status = Py_InitializeFromConfig(&config);

done:
    PyConfig_Clear(&config);
    return status;
}
```

### Isolated Configuration {#init-isolated-conf}

`PyPreConfig_InitIsolatedConfig`{.interpreted-text role="c:func"} and `PyConfig_InitIsolatedConfig`{.interpreted-text role="c:func"} functions create a configuration to isolate Python from the system. For example, to embed Python into an application.

This configuration ignores global configuration variables, environment variables, command line arguments (`PyConfig.argv`{.interpreted-text role="c:member"} is not parsed) and user site directory. The C standard streams (ex: `stdout`) and the LC_CTYPE locale are left unchanged. Signal handlers are not installed.

Configuration files are still used with this configuration to determine paths that are unspecified. Ensure `PyConfig.home`{.interpreted-text role="c:member"} is specified to avoid computing the default path configuration.

### Python Configuration {#init-python-config}

`PyPreConfig_InitPythonConfig`{.interpreted-text role="c:func"} and `PyConfig_InitPythonConfig`{.interpreted-text role="c:func"} functions create a configuration to build a customized Python which behaves as the regular Python.

Environments variables and command line arguments are used to configure Python, whereas global configuration variables are ignored.

This function enables C locale coercion (`538`{.interpreted-text role="pep"}) and `Python UTF-8 Mode <utf8-mode>`{.interpreted-text role="ref"} (`540`{.interpreted-text role="pep"}) depending on the LC_CTYPE locale, `PYTHONUTF8`{.interpreted-text role="envvar"} and `PYTHONCOERCECLOCALE`{.interpreted-text role="envvar"} environment variables.

### Python Path Configuration {#init-path-config}

`PyConfig`{.interpreted-text role="c:type"} contains multiple fields for the path configuration:

- Path configuration inputs:
  - `PyConfig.home`{.interpreted-text role="c:member"}
  - `PyConfig.platlibdir`{.interpreted-text role="c:member"}
  - `PyConfig.pathconfig_warnings`{.interpreted-text role="c:member"}
  - `PyConfig.program_name`{.interpreted-text role="c:member"}
  - `PyConfig.pythonpath_env`{.interpreted-text role="c:member"}
  - current working directory: to get absolute paths
  - `PATH` environment variable to get the program full path (from `PyConfig.program_name`{.interpreted-text role="c:member"})
  - `__PYVENV_LAUNCHER__` environment variable
  - (Windows only) Application paths in the registry under \"SoftwarePythonPythonCoreX.YPythonPath\" of HKEY_CURRENT_USER and HKEY_LOCAL_MACHINE (where X.Y is the Python version).
- Path configuration output fields:
  - `PyConfig.base_exec_prefix`{.interpreted-text role="c:member"}
  - `PyConfig.base_executable`{.interpreted-text role="c:member"}
  - `PyConfig.base_prefix`{.interpreted-text role="c:member"}
  - `PyConfig.exec_prefix`{.interpreted-text role="c:member"}
  - `PyConfig.executable`{.interpreted-text role="c:member"}
  - `PyConfig.module_search_paths_set`{.interpreted-text role="c:member"}, `PyConfig.module_search_paths`{.interpreted-text role="c:member"}
  - `PyConfig.prefix`{.interpreted-text role="c:member"}

If at least one \"output field\" is not set, Python calculates the path configuration to fill unset fields. If `~PyConfig.module_search_paths_set`{.interpreted-text role="c:member"} is equal to `0`, `~PyConfig.module_search_paths`{.interpreted-text role="c:member"} is overridden and `~PyConfig.module_search_paths_set`{.interpreted-text role="c:member"} is set to `1`.

It is possible to completely ignore the function calculating the default path configuration by setting explicitly all path configuration output fields listed above. A string is considered as set even if it is non-empty. `module_search_paths` is considered as set if `module_search_paths_set` is set to `1`. In this case, `module_search_paths` will be used without modification.

Set `~PyConfig.pathconfig_warnings`{.interpreted-text role="c:member"} to `0` to suppress warnings when calculating the path configuration (Unix only, Windows does not log any warning).

If `~PyConfig.base_prefix`{.interpreted-text role="c:member"} or `~PyConfig.base_exec_prefix`{.interpreted-text role="c:member"} fields are not set, they inherit their value from `~PyConfig.prefix`{.interpreted-text role="c:member"} and `~PyConfig.exec_prefix`{.interpreted-text role="c:member"} respectively.

`Py_RunMain`{.interpreted-text role="c:func"} and `Py_Main`{.interpreted-text role="c:func"} modify `sys.path`{.interpreted-text role="data"}:

- If `~PyConfig.run_filename`{.interpreted-text role="c:member"} is set and is a directory which contains a `__main__.py` script, prepend `~PyConfig.run_filename`{.interpreted-text role="c:member"} to `sys.path`{.interpreted-text role="data"}.
- If `~PyConfig.isolated`{.interpreted-text role="c:member"} is zero:
  - If `~PyConfig.run_module`{.interpreted-text role="c:member"} is set, prepend the current directory to `sys.path`{.interpreted-text role="data"}. Do nothing if the current directory cannot be read.
  - If `~PyConfig.run_filename`{.interpreted-text role="c:member"} is set, prepend the directory of the filename to `sys.path`{.interpreted-text role="data"}.
  - Otherwise, prepend an empty string to `sys.path`{.interpreted-text role="data"}.

If `~PyConfig.site_import`{.interpreted-text role="c:member"} is non-zero, `sys.path`{.interpreted-text role="data"} can be modified by the `site`{.interpreted-text role="mod"} module. If `~PyConfig.user_site_directory`{.interpreted-text role="c:member"} is non-zero and the user\'s site-package directory exists, the `site`{.interpreted-text role="mod"} module appends the user\'s site-package directory to `sys.path`{.interpreted-text role="data"}.

The following configuration files are used by the path configuration:

- `pyvenv.cfg`
- `._pth` file (ex: `python._pth`)
- `pybuilddir.txt` (Unix only)

If a `._pth` file is present:

- Set `~PyConfig.isolated`{.interpreted-text role="c:member"} to `1`.
- Set `~PyConfig.use_environment`{.interpreted-text role="c:member"} to `0`.
- Set `~PyConfig.site_import`{.interpreted-text role="c:member"} to `0`.
- Set `~PyConfig.user_site_directory`{.interpreted-text role="c:member"} to `0` (since 3.15).
- Set `~PyConfig.safe_path`{.interpreted-text role="c:member"} to `1`.

If `~PyConfig.home`{.interpreted-text role="c:member"} is not set and a `pyvenv.cfg` file is present in the same directory as `~PyConfig.executable`{.interpreted-text role="c:member"}, or its parent, `~PyConfig.prefix`{.interpreted-text role="c:member"} and `~PyConfig.exec_prefix`{.interpreted-text role="c:member"} are set that location. When this happens, `~PyConfig.base_prefix`{.interpreted-text role="c:member"} and `~PyConfig.base_exec_prefix`{.interpreted-text role="c:member"} still keep their value, pointing to the base installation. See `sys-path-init-virtual-environments`{.interpreted-text role="ref"} for more information.

The `__PYVENV_LAUNCHER__` environment variable is used to set `PyConfig.base_executable`{.interpreted-text role="c:member"}.

::: versionchanged
3.14

`~PyConfig.prefix`{.interpreted-text role="c:member"}, and `~PyConfig.exec_prefix`{.interpreted-text role="c:member"}, are now set to the `pyvenv.cfg` directory. This was previously done by `site`{.interpreted-text role="mod"}, therefore affected by `-S`{.interpreted-text role="option"}.
:::

::: versionchanged
3.15

`~PyConfig.user_site_directory`{.interpreted-text role="c:member"} is now set to `0` when a `._pth` file is present.
:::

## Py_GetArgcArgv()

> Get the original command line arguments, before Python modified them.
>
> See also `PyConfig.orig_argv`{.interpreted-text role="c:member"} member.

## Delaying main module execution

In some embedding use cases, it may be desirable to separate interpreter initialization from the execution of the main module.

This separation can be achieved by setting `PyConfig.run_command` to the empty string during initialization (to prevent the interpreter from dropping into the interactive prompt), and then subsequently executing the desired main module code using `__main__.__dict__` as the global namespace.
