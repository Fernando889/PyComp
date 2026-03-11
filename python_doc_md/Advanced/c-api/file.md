# File Objects {#fileobjects}

::: index
pair: object; file
:::

These APIs are a minimal emulation of the Python 2 C API for built-in file objects, which used to rely on the buffered I/O (`FILE*`{.interpreted-text role="c:expr"}) support from the C standard library. In Python 3, files and streams use the new `io`{.interpreted-text role="mod"} module, which defines several layers over the low-level unbuffered I/O of the operating system. The functions described below are convenience C wrappers over these new APIs, and meant mostly for internal error reporting in the interpreter; third-party code is advised to access the `io`{.interpreted-text role="mod"} APIs instead.

> Create a Python file object from the file descriptor of an already opened file *fd*. The arguments *name*, *encoding*, *errors* and *newline* can be `NULL` to use the defaults; *buffering* can be *-1* to use the default. *name* is ignored and kept for backward compatibility. Return `NULL` on failure. For a more comprehensive description of the arguments, please refer to the `io.open`{.interpreted-text role="func"} function documentation.
>
> :::: warning
> ::: title
> Warning
> :::
>
> Since Python streams have their own buffering layer, mixing them with OS-level file descriptors can produce various issues (such as unexpected ordering of data).
> ::::
>
> ::: versionchanged
> 3.2 Ignore *name* attribute.
> :::

> Return the file descriptor associated with *p* as an `int`{.interpreted-text role="c:expr"}. If the object is an integer, its value is returned. If not, the object\'s `~io.IOBase.fileno`{.interpreted-text role="meth"} method is called if it exists; the method must return an integer, which is returned as the file descriptor value. Sets an exception and returns `-1` on failure.

> ::: index
> single: EOFError (built-in exception)
> :::
>
> Equivalent to `p.readline([n])`, this function reads one line from the object *p*. *p* may be a file object or any object with a `~io.IOBase.readline`{.interpreted-text role="meth"} method. If *n* is `0`, exactly one line is read, regardless of the length of the line. If *n* is greater than `0`, no more than *n* bytes will be read from the file; a partial line can be returned. In both cases, an empty string is returned if the end of the file is reached immediately. If *n* is less than `0`, however, one line is read regardless of length, but `EOFError`{.interpreted-text role="exc"} is raised if the end of the file is reached immediately.

> Overrides the normal behavior of `io.open_code`{.interpreted-text role="func"} to pass its parameter through the provided handler.
>
> The *handler* is a function of type:
>
> > Equivalent of `PyObject *(\*)(PyObject *path,
> > void *userData)`{.interpreted-text role="c:expr"}, where *path* is guaranteed to be `PyUnicodeObject`{.interpreted-text role="c:type"}.
>
> The *userData* pointer is passed into the hook function. Since hook functions may be called from different runtimes, this pointer should not refer directly to Python state.
>
> As this hook is intentionally used during import, avoid importing new modules during its execution unless they are known to be frozen or available in `sys.modules`.
>
> Once a hook has been set, it cannot be removed or replaced, and later calls to `PyFile_SetOpenCodeHook`{.interpreted-text role="c:func"} will fail. On failure, the function returns -1 and sets an exception if the interpreter has been initialized.
>
> This function is safe to call before `Py_Initialize`{.interpreted-text role="c:func"}.
>
> ::: audit-event
> setopencodehook \"\" c.PyFile_SetOpenCodeHook
> :::
>
> ::: versionadded
> 3.8
> :::

> Open *path* with the mode `'rb'`. *path* must be a Python `str`{.interpreted-text role="class"} object. The behavior of this function may be overridden by `PyFile_SetOpenCodeHook`{.interpreted-text role="c:func"} to allow for some preprocessing of the text.
>
> This is analogous to `io.open_code`{.interpreted-text role="func"} in Python.
>
> On success, this function returns a `strong reference`{.interpreted-text role="term"} to a Python file object. On failure, this function returns `NULL` with an exception set.
>
> ::: versionadded
> 3.8
> :::

> Similar to `PyFile_OpenCodeObject`{.interpreted-text role="c:func"}, but *path* is a UTF-8 encoded `const char*`{.interpreted-text role="c:expr"}.
>
> ::: versionadded
> 3.8
> :::

> ::: index
> single: Py_PRINT_RAW (C macro)
> :::
>
> Write object *obj* to file object *p*. The only supported flag for *flags* is `Py_PRINT_RAW`{.interpreted-text role="c:macro"}; if given, the `str`{.interpreted-text role="func"} of the object is written instead of the `repr`{.interpreted-text role="func"}. Return `0` on success or `-1` on failure; the appropriate exception will be set.

> Write string *s* to file object *p*. Return `0` on success or `-1` on failure; the appropriate exception will be set.

## Deprecated API

These are `soft deprecated`{.interpreted-text role="term"} APIs that were included in Python\'s C API by mistake. They are documented solely for completeness; use other `PyFile*` APIs instead.

> Use `PyFile_FromFd`{.interpreted-text role="c:func"} with defaults (`fd, NULL, "w", -1, NULL, NULL, NULL, 0`) instead.

> Type of file-like objects used internally at Python startup when `io`{.interpreted-text role="py:mod"} is not yet available. Use Python `open`{.interpreted-text role="py:func"} or `PyFile_FromFd`{.interpreted-text role="c:func"} to create file objects instead.
