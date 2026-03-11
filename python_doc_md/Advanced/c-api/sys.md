# Operating System Utilities {#os}

> Return the file system representation for *path*. If the object is a `str`{.interpreted-text role="class"} or `bytes`{.interpreted-text role="class"} object, then a new `strong reference`{.interpreted-text role="term"} is returned. If the object implements the `os.PathLike`{.interpreted-text role="class"} interface, then `~os.PathLike.__fspath__`{.interpreted-text role="meth"} is returned as long as it is a `str`{.interpreted-text role="class"} or `bytes`{.interpreted-text role="class"} object. Otherwise `TypeError`{.interpreted-text role="exc"} is raised and `NULL` is returned.
>
> ::: versionadded
> 3.6
> :::

> Return true (nonzero) if the standard I/O file *fp* with name *filename* is deemed interactive. This is the case for files for which `isatty(fileno(fp))` is true. If the `PyConfig.interactive`{.interpreted-text role="c:member"} is non-zero, this function also returns true if the *filename* pointer is `NULL` or if the name is equal to one of the strings `'<stdin>'` or `'???'`.
>
> This function must not be called before Python is initialized.

> Function to prepare some internal state before a process fork. This should be called before calling `fork`{.interpreted-text role="c:func"} or any similar function that clones the current process. Only available on systems where `fork`{.interpreted-text role="c:func"} is defined.
>
> :::: warning
> ::: title
> Warning
> :::
>
> The C `fork`{.interpreted-text role="c:func"} call should only be made from the `"main" thread <fork-and-threads>`{.interpreted-text role="ref"} (of the `"main" interpreter <sub-interpreter-support>`{.interpreted-text role="ref"}). The same is true for `PyOS_BeforeFork()`.
> ::::
>
> ::: versionadded
> 3.7
> :::

> Function to update some internal state after a process fork. This should be called from the parent process after calling `fork`{.interpreted-text role="c:func"} or any similar function that clones the current process, regardless of whether process cloning was successful. Only available on systems where `fork`{.interpreted-text role="c:func"} is defined.
>
> :::: warning
> ::: title
> Warning
> :::
>
> The C `fork`{.interpreted-text role="c:func"} call should only be made from the `"main" thread <fork-and-threads>`{.interpreted-text role="ref"} (of the `"main" interpreter <sub-interpreter-support>`{.interpreted-text role="ref"}). The same is true for `PyOS_AfterFork_Parent()`.
> ::::
>
> ::: versionadded
> 3.7
> :::

> Function to update internal interpreter state after a process fork. This must be called from the child process after calling `fork`{.interpreted-text role="c:func"}, or any similar function that clones the current process, if there is any chance the process will call back into the Python interpreter. Only available on systems where `fork`{.interpreted-text role="c:func"} is defined.
>
> :::: warning
> ::: title
> Warning
> :::
>
> The C `fork`{.interpreted-text role="c:func"} call should only be made from the `"main" thread <fork-and-threads>`{.interpreted-text role="ref"} (of the `"main" interpreter <sub-interpreter-support>`{.interpreted-text role="ref"}). The same is true for `PyOS_AfterFork_Child()`.
> ::::
>
> ::: versionadded
> 3.7
> :::
>
> ::: seealso
> `os.register_at_fork`{.interpreted-text role="func"} allows registering custom Python functions to be called by `PyOS_BeforeFork()`{.interpreted-text role="c:func"}, `PyOS_AfterFork_Parent`{.interpreted-text role="c:func"} and `PyOS_AfterFork_Child`{.interpreted-text role="c:func"}.
> :::

> Function to update some internal state after a process fork; this should be called in the new process if the Python interpreter will continue to be used. If a new executable is loaded into the new process, this function does not need to be called.
>
> ::: deprecated
> 3.7 This function is superseded by `PyOS_AfterFork_Child()`{.interpreted-text role="c:func"}.
> :::

> ::: index
> single: USE_STACKCHECK (C macro)
> :::
>
> Return true when the interpreter runs out of stack space. This is a reliable check, but is only available when `!USE_STACKCHECK`{.interpreted-text role="c:macro"} is defined (currently on certain versions of Windows using the Microsoft Visual C++ compiler). `!USE_STACKCHECK`{.interpreted-text role="c:macro"} will be defined automatically; you should never change the definition in your own code.

> Return the current signal handler for signal *i*. This is a thin wrapper around either `!sigaction`{.interpreted-text role="c:func"} or `!signal`{.interpreted-text role="c:func"}. Do not call those functions directly!

> Set the signal handler for signal *i* to be *h*; return the old signal handler. This is a thin wrapper around either `!sigaction`{.interpreted-text role="c:func"} or `!signal`{.interpreted-text role="c:func"}. Do not call those functions directly!

> Check if a `!SIGINT`{.interpreted-text role="c:macro"} signal has been received.
>
> Returns `1` if a `!SIGINT`{.interpreted-text role="c:macro"} has occurred and clears the signal flag, or `0` otherwise.
>
> In most cases, you should prefer `PyErr_CheckSignals`{.interpreted-text role="c:func"} over this function. `!PyErr_CheckSignals`{.interpreted-text role="c:func"} invokes the appropriate signal handlers for all pending signals, allowing Python code to handle the signal properly. This function only detects `!SIGINT`{.interpreted-text role="c:macro"} and does not invoke any Python signal handlers.
>
> This function is async-signal-safe and this function cannot fail. The caller must hold an `attached thread state`{.interpreted-text role="term"}.

> :::: warning
> ::: title
> Warning
> :::
>
> This function should not be called directly: use the `PyConfig`{.interpreted-text role="c:type"} API with the `PyConfig_SetBytesString`{.interpreted-text role="c:func"} function which ensures that `Python is preinitialized <c-preinit>`{.interpreted-text role="ref"}.
>
> This function must not be called before `Python is preinitialized
> <c-preinit>`{.interpreted-text role="ref"} and so that the LC_CTYPE locale is properly configured: see the `Py_PreInitialize`{.interpreted-text role="c:func"} function.
> ::::
>
> Decode a byte string from the `filesystem encoding and error handler`{.interpreted-text role="term"}. If the error handler is `surrogateescape error handler
> <surrogateescape>`{.interpreted-text role="ref"}, undecodable bytes are decoded as characters in range U+DC80..U+DCFF; and if a byte sequence can be decoded as a surrogate character, the bytes are escaped using the surrogateescape error handler instead of decoding them.
>
> Return a pointer to a newly allocated wide character string, use `PyMem_RawFree`{.interpreted-text role="c:func"} to free the memory. If size is not `NULL`, write the number of wide characters excluding the null character into `*size`
>
> Return `NULL` on decoding error or memory allocation error. If *size* is not `NULL`, `*size` is set to `(size_t)-1` on memory error or set to `(size_t)-2` on decoding error.
>
> The `filesystem encoding and error handler`{.interpreted-text role="term"} are selected by `PyConfig_Read`{.interpreted-text role="c:func"}: see `~PyConfig.filesystem_encoding`{.interpreted-text role="c:member"} and `~PyConfig.filesystem_errors`{.interpreted-text role="c:member"} members of `PyConfig`{.interpreted-text role="c:type"}.
>
> Decoding errors should never happen, unless there is a bug in the C library.
>
> Use the `Py_EncodeLocale`{.interpreted-text role="c:func"} function to encode the character string back to a byte string.
>
> ::: seealso
> The `PyUnicode_DecodeFSDefaultAndSize`{.interpreted-text role="c:func"} and `PyUnicode_DecodeLocaleAndSize`{.interpreted-text role="c:func"} functions.
> :::
>
> ::: versionadded
> 3.5
> :::
>
> ::: versionchanged
> 3.7 The function now uses the UTF-8 encoding in the `Python UTF-8 Mode
> <utf8-mode>`{.interpreted-text role="ref"}.
> :::
>
> ::: versionchanged
> 3.8 The function now uses the UTF-8 encoding on Windows if `PyPreConfig.legacy_windows_fs_encoding`{.interpreted-text role="c:member"} is zero;
> :::

> Encode a wide character string to the `filesystem encoding and error
> handler`{.interpreted-text role="term"}. If the error handler is `surrogateescape error handler
> <surrogateescape>`{.interpreted-text role="ref"}, surrogate characters in the range U+DC80..U+DCFF are converted to bytes 0x80..0xFF.
>
> Return a pointer to a newly allocated byte string, use `PyMem_Free`{.interpreted-text role="c:func"} to free the memory. Return `NULL` on encoding error or memory allocation error.
>
> If error_pos is not `NULL`, `*error_pos` is set to `(size_t)-1` on success, or set to the index of the invalid character on encoding error.
>
> The `filesystem encoding and error handler`{.interpreted-text role="term"} are selected by `PyConfig_Read`{.interpreted-text role="c:func"}: see `~PyConfig.filesystem_encoding`{.interpreted-text role="c:member"} and `~PyConfig.filesystem_errors`{.interpreted-text role="c:member"} members of `PyConfig`{.interpreted-text role="c:type"}.
>
> Use the `Py_DecodeLocale`{.interpreted-text role="c:func"} function to decode the bytes string back to a wide character string.
>
> :::: warning
> ::: title
> Warning
> :::
>
> This function must not be called before `Python is preinitialized
> <c-preinit>`{.interpreted-text role="ref"} and so that the LC_CTYPE locale is properly configured: see the `Py_PreInitialize`{.interpreted-text role="c:func"} function.
> ::::
>
> ::: seealso
> The `PyUnicode_EncodeFSDefault`{.interpreted-text role="c:func"} and `PyUnicode_EncodeLocale`{.interpreted-text role="c:func"} functions.
> :::
>
> ::: versionadded
> 3.5
> :::
>
> ::: versionchanged
> 3.7 The function now uses the UTF-8 encoding in the `Python UTF-8 Mode
> <utf8-mode>`{.interpreted-text role="ref"}.
> :::
>
> ::: versionchanged
> 3.8 The function now uses the UTF-8 encoding on Windows if `PyPreConfig.legacy_windows_fs_encoding`{.interpreted-text role="c:member"} is zero.
> :::

> Similar to `!fopen`{.interpreted-text role="c:func"}, but *path* is a Python object and an exception is set on error.
>
> *path* must be a `str`{.interpreted-text role="class"} object, a `bytes`{.interpreted-text role="class"} object, or a `path-like object`{.interpreted-text role="term"}.
>
> On success, return the new file pointer. On error, set an exception and return `NULL`.
>
> The file must be closed by `Py_fclose`{.interpreted-text role="c:func"} rather than calling directly `!fclose`{.interpreted-text role="c:func"}.
>
> The file descriptor is created non-inheritable (`446`{.interpreted-text role="pep"}).
>
> The caller must have an `attached thread state`{.interpreted-text role="term"}.
>
> ::: versionadded
> 3.14
> :::

> Close a file that was opened by `Py_fopen`{.interpreted-text role="c:func"}.
>
> On success, return `0`. On error, return `EOF` and `errno` is set to indicate the error. In either case, any further access (including another call to `Py_fclose`{.interpreted-text role="c:func"}) to the stream results in undefined behavior.
>
> ::: versionadded
> 3.14
> :::

# System Functions {#systemfunctions}

These are utility functions that make functionality from the `sys`{.interpreted-text role="mod"} module accessible to C code. They all work with the current interpreter thread\'s `sys`{.interpreted-text role="mod"} module\'s dict, which is contained in the internal thread state structure.

> Get the attribute *name* of the `sys`{.interpreted-text role="mod"} module. Return a `strong reference`{.interpreted-text role="term"}. Raise `RuntimeError`{.interpreted-text role="exc"} and return `NULL` if it does not exist or if the `sys`{.interpreted-text role="mod"} module cannot be found.
>
> If the non-existing object should not be treated as a failure, you can use `PySys_GetOptionalAttr`{.interpreted-text role="c:func"} instead.
>
> ::: versionadded
> 3.15
> :::

> This is the same as `PySys_GetAttr`{.interpreted-text role="c:func"}, but *name* is specified as a `const char*`{.interpreted-text role="c:expr"} UTF-8 encoded bytes string, rather than a `PyObject*`{.interpreted-text role="c:expr"}.
>
> If the non-existing object should not be treated as a failure, you can use `PySys_GetOptionalAttrString`{.interpreted-text role="c:func"} instead.
>
> ::: versionadded
> 3.15
> :::

> Variant of `PySys_GetAttr`{.interpreted-text role="c:func"} which doesn\'t raise exception if the object does not exist.
>
> - Set *\*result* to a new `strong reference`{.interpreted-text role="term"} to the object and return `1` if the object exists.
> - Set *\*result* to `NULL` and return `0` without setting an exception if the object does not exist.
> - Set an exception, set *\*result* to `NULL`, and return `-1`, if an error occurred.
>
> ::: versionadded
> 3.15
> :::

> This is the same as `PySys_GetOptionalAttr`{.interpreted-text role="c:func"}, but *name* is specified as a `const char*`{.interpreted-text role="c:expr"} UTF-8 encoded bytes string, rather than a `PyObject*`{.interpreted-text role="c:expr"}.
>
> ::: versionadded
> 3.15
> :::

> Similar to `PySys_GetAttrString`{.interpreted-text role="c:func"}, but return a `borrowed
> reference`{.interpreted-text role="term"} and return `NULL` *without* setting exception on failure.
>
> Preserves exception that was set before the call.

> Set *name* in the `sys`{.interpreted-text role="mod"} module to *v* unless *v* is `NULL`, in which case *name* is deleted from the sys module. Returns `0` on success, `-1` on error.

> Write the output string described by *format* to `sys.stdout`{.interpreted-text role="data"}. No exceptions are raised, even if truncation occurs (see below).
>
> *format* should limit the total size of the formatted output string to 1000 bytes or less \-- after 1000 bytes, the output string is truncated. In particular, this means that no unrestricted \"%s\" formats should occur; these should be limited using \"%.\<N\>s\" where \<N\> is a decimal number calculated so that \<N\> plus the maximum size of other formatted text does not exceed 1000 bytes. Also watch out for \"%f\", which can print hundreds of digits for very large numbers.
>
> If a problem occurs, or `sys.stdout`{.interpreted-text role="data"} is unset, the formatted message is written to the real (C level) *stdout*.

> As `PySys_WriteStdout`{.interpreted-text role="c:func"}, but write to `sys.stderr`{.interpreted-text role="data"} or *stderr* instead.

> Function similar to PySys_WriteStdout() but format the message using `PyUnicode_FromFormatV`{.interpreted-text role="c:func"} and don\'t truncate the message to an arbitrary length.
>
> ::: versionadded
> 3.2
> :::

> As `PySys_FormatStdout`{.interpreted-text role="c:func"}, but write to `sys.stderr`{.interpreted-text role="data"} or *stderr* instead.
>
> ::: versionadded
> 3.2
> :::

> Return the current dictionary of `-X`{.interpreted-text role="option"} options, similarly to `sys._xoptions`{.interpreted-text role="data"}. On error, `NULL` is returned and an exception is set.
>
> ::: versionadded
> 3.2
> :::

> Raise an auditing event with any active hooks. Return zero for success and non-zero with an exception set on failure.
>
> The *event* string argument must not be *NULL*.
>
> If any hooks have been added, *format* and other arguments will be used to construct a tuple to pass. Apart from `N`, the same format characters as used in `Py_BuildValue`{.interpreted-text role="c:func"} are available. If the built value is not a tuple, it will be added into a single-element tuple.
>
> The `N` format option must not be used. It consumes a reference, but since there is no way to know whether arguments to this function will be consumed, using it may cause reference leaks.
>
> Note that `#` format characters should always be treated as `Py_ssize_t`{.interpreted-text role="c:type"}, regardless of whether `PY_SSIZE_T_CLEAN` was defined.
>
> `sys.audit`{.interpreted-text role="func"} performs the same function from Python code.
>
> See also `PySys_AuditTuple`{.interpreted-text role="c:func"}.
>
> ::: versionadded
> 3.8
> :::
>
> ::: versionchanged
> 3.8.2
>
> Require `Py_ssize_t`{.interpreted-text role="c:type"} for `#` format characters. Previously, an unavoidable deprecation warning was raised.
> :::

> Similar to `PySys_Audit`{.interpreted-text role="c:func"}, but pass arguments as a Python object. *args* must be a `tuple`{.interpreted-text role="class"}. To pass no arguments, *args* can be *NULL*.
>
> ::: versionadded
> 3.13
> :::

> Append the callable *hook* to the list of active auditing hooks. Return zero on success and non-zero on failure. If the runtime has been initialized, also set an error on failure. Hooks added through this API are called for all interpreters created by the runtime.
>
> The *userData* pointer is passed into the hook function. Since hook functions may be called from different runtimes, this pointer should not refer directly to Python state.
>
> This function is safe to call before `Py_Initialize`{.interpreted-text role="c:func"}. When called after runtime initialization, existing audit hooks are notified and may silently abort the operation by raising an error subclassed from `Exception`{.interpreted-text role="class"} (other errors will not be silenced).
>
> The hook function is always called with an `attached thread state`{.interpreted-text role="term"} by the Python interpreter that raised the event.
>
> See `578`{.interpreted-text role="pep"} for a detailed description of auditing. Functions in the runtime and standard library that raise events are listed in the `audit events table <audit-events>`{.interpreted-text role="ref"}. Details are in each function\'s documentation.
>
> ::: audit-event
> sys.addaudithook \"\" c.PySys_AddAuditHook
>
> If the interpreter is initialized, this function raises an auditing event `sys.addaudithook` with no arguments. If any existing hooks raise an exception derived from `Exception`{.interpreted-text role="class"}, the new hook will not be added and the exception is cleared. As a result, callers cannot assume that their hook has been added unless they control all existing hooks.
> :::
>
> > The type of the hook function. *event* is the C string event argument passed to `PySys_Audit`{.interpreted-text role="c:func"} or `PySys_AuditTuple`{.interpreted-text role="c:func"}. *args* is guaranteed to be a `PyTupleObject`{.interpreted-text role="c:type"}. *userData* is the argument passed to PySys_AddAuditHook().
>
> ::: versionadded
> 3.8
> :::

# Process Control {#processcontrol}

> ::: index
> single: abort (C function)
> :::
>
> Print a fatal error message and kill the process. No cleanup is performed. This function should only be invoked when a condition is detected that would make it dangerous to continue using the Python interpreter; e.g., when the object administration appears to be corrupted. On Unix, the standard C library function `!abort`{.interpreted-text role="c:func"} is called which will attempt to produce a `core`{.interpreted-text role="file"} file.
>
> The `Py_FatalError()` function is replaced with a macro which logs automatically the name of the current function, unless the `Py_LIMITED_API` macro is defined.
>
> ::: versionchanged
> 3.9 Log the function name automatically.
> :::

> ::: index
> single: Py_FinalizeEx (C function) single: exit (C function)
> :::
>
> Exit the current process. This calls `Py_FinalizeEx`{.interpreted-text role="c:func"} and then calls the standard C library function `exit(status)`. If `Py_FinalizeEx`{.interpreted-text role="c:func"} indicates an error, the exit status is set to 120.
>
> ::: versionchanged
> 3.6 Errors from finalization no longer ignored.
> :::

> ::: index
> single: Py_FinalizeEx (C function) single: cleanup functions
> :::
>
> Register a cleanup function to be called by `Py_FinalizeEx`{.interpreted-text role="c:func"}. The cleanup function will be called with no arguments and should return no value. At most 32 cleanup functions can be registered. When the registration is successful, `Py_AtExit`{.interpreted-text role="c:func"} returns `0`; on failure, it returns `-1`. The cleanup function registered last is called first. Each cleanup function will be called at most once. Since Python\'s internal finalization will have completed before the cleanup function, no Python APIs should be called by *func*.
>
> ::: seealso
> `PyUnstable_AtExit`{.interpreted-text role="c:func"} for passing a `void *data` argument.
> :::
