# Exception Handling {#exceptionhandling}

The functions described in this chapter will let you handle and raise Python exceptions. It is important to understand some of the basics of Python exception handling. It works somewhat like the POSIX `errno`{.interpreted-text role="c:data"} variable: there is a global indicator (per thread) of the last error that occurred. Most C API functions don\'t clear this on success, but will set it to indicate the cause of the error on failure. Most C API functions also return an error indicator, usually `NULL` if they are supposed to return a pointer, or `-1` if they return an integer (exception: the `PyArg_*` functions return `1` for success and `0` for failure).

Concretely, the error indicator consists of three object pointers: the exception\'s type, the exception\'s value, and the traceback object. Any of those pointers can be `NULL` if non-set (although some combinations are forbidden, for example you can\'t have a non-`NULL` traceback if the exception type is `NULL`).

When a function must fail because some function it called failed, it generally doesn\'t set the error indicator; the function it called already set it. It is responsible for either handling the error and clearing the exception or returning after cleaning up any resources it holds (such as object references or memory allocations); it should *not* continue normally if it is not prepared to handle the error. If returning due to an error, it is important to indicate to the caller that an error has been set. If the error is not handled or carefully propagated, additional calls into the Python/C API may not behave as intended and may fail in mysterious ways.

:::: note
::: title
Note
:::

The error indicator is **not** the result of `sys.exc_info`{.interpreted-text role="func"}. The former corresponds to an exception that is not yet caught (and is therefore still propagating), while the latter returns an exception after it is caught (and has therefore stopped propagating).
::::

## Printing and clearing

> Clear the error indicator. If the error indicator is not set, there is no effect.

> Print a standard traceback to `sys.stderr` and clear the error indicator. **Unless** the error is a `SystemExit`, in that case no traceback is printed and the Python process will exit with the error code specified by the `SystemExit` instance.
>
> Call this function **only** when the error indicator is set. Otherwise it will cause a fatal error!
>
> If *set_sys_last_vars* is nonzero, the variable `sys.last_exc`{.interpreted-text role="data"} is set to the printed exception. For backwards compatibility, the deprecated variables `sys.last_type`{.interpreted-text role="data"}, `sys.last_value`{.interpreted-text role="data"} and `sys.last_traceback`{.interpreted-text role="data"} are also set to the type, value and traceback of this exception, respectively.
>
> ::: versionchanged
> 3.12 The setting of `sys.last_exc`{.interpreted-text role="data"} was added.
> :::

> Alias for `PyErr_PrintEx(1)`.

> Call `sys.unraisablehook`{.interpreted-text role="func"} using the current exception and *obj* argument.
>
> This utility function prints a warning message to `sys.stderr` when an exception has been set but it is impossible for the interpreter to actually raise the exception. It is used, for example, when an exception occurs in an `~object.__del__`{.interpreted-text role="meth"} method.
>
> The function is called with a single argument *obj* that identifies the context in which the unraisable exception occurred. If possible, the repr of *obj* will be printed in the warning message. If *obj* is `NULL`, only the traceback is printed.
>
> An exception must be set when calling this function.
>
> ::: versionchanged
> 3.4 Print a traceback. Print only traceback if *obj* is `NULL`.
> :::
>
> ::: versionchanged
> 3.8 Use `sys.unraisablehook`{.interpreted-text role="func"}.
> :::

> Similar to `PyErr_WriteUnraisable`{.interpreted-text role="c:func"}, but the *format* and subsequent parameters help format the warning message; they have the same meaning and values as in `PyUnicode_FromFormat`{.interpreted-text role="c:func"}. `PyErr_WriteUnraisable(obj)` is roughly equivalent to `PyErr_FormatUnraisable("Exception ignored in: %R", obj)`. If *format* is `NULL`, only the traceback is printed.
>
> ::: versionadded
> 3.13
> :::

> Print the standard traceback display of `exc` to `sys.stderr`, including chained exceptions and notes.
>
> ::: versionadded
> 3.12
> :::

## Raising exceptions

These functions help you set the current thread\'s error indicator. For convenience, some of these functions will always return a `NULL` pointer for use in a `return` statement.

> This is the most common way to set the error indicator. The first argument specifies the exception type; it is normally one of the standard exceptions, e.g. `PyExc_RuntimeError`{.interpreted-text role="c:data"}. You need not create a new `strong reference`{.interpreted-text role="term"} to it (e.g. with `Py_INCREF`{.interpreted-text role="c:func"}). The second argument is an error message; it is decoded from `'utf-8'`.

> This function is similar to `PyErr_SetString`{.interpreted-text role="c:func"} but lets you specify an arbitrary Python object for the \"value\" of the exception.

> This function sets the error indicator and returns `NULL`. *exception* should be a Python exception class. The *format* and subsequent parameters help format the error message; they have the same meaning and values as in `PyUnicode_FromFormat`{.interpreted-text role="c:func"}. *format* is an ASCII-encoded string.

> Same as `PyErr_Format`{.interpreted-text role="c:func"}, but taking a `va_list`{.interpreted-text role="c:type"} argument rather than a variable number of arguments.
>
> ::: versionadded
> 3.5
> :::

> This is a shorthand for `PyErr_SetObject(type, Py_None)`.

> This is a shorthand for `PyErr_SetString(PyExc_TypeError, message)`, where *message* indicates that a built-in operation was invoked with an illegal argument. It is mostly for internal use.

> This is a shorthand for `PyErr_SetNone(PyExc_MemoryError)`; it returns `NULL` so an object allocation function can write `return PyErr_NoMemory();` when it runs out of memory.

> ::: index
> single: strerror (C function)
> :::
>
> This is a convenience function to raise an exception when a C library function has returned an error and set the C variable `errno`{.interpreted-text role="c:data"}. It constructs a tuple object whose first item is the integer `errno`{.interpreted-text role="c:data"} value and whose second item is the corresponding error message (gotten from `!strerror`{.interpreted-text role="c:func"}), and then calls `PyErr_SetObject(type, object)`. On Unix, when the `errno`{.interpreted-text role="c:data"} value is `!EINTR`{.interpreted-text role="c:macro"}, indicating an interrupted system call, this calls `PyErr_CheckSignals`{.interpreted-text role="c:func"}, and if that set the error indicator, leaves it set to that. The function always returns `NULL`, so a wrapper function around a system call can write `return PyErr_SetFromErrno(type);` when the system call returns an error.

> Similar to `PyErr_SetFromErrno`{.interpreted-text role="c:func"}, with the additional behavior that if *filenameObject* is not `NULL`, it is passed to the constructor of *type* as a third parameter. In the case of `OSError`{.interpreted-text role="exc"} exception, this is used to define the `!filename`{.interpreted-text role="attr"} attribute of the exception instance.

> Similar to `PyErr_SetFromErrnoWithFilenameObject`{.interpreted-text role="c:func"}, but takes a second filename object, for raising errors when a function that takes two filenames fails.
>
> ::: versionadded
> 3.4
> :::

> Similar to `PyErr_SetFromErrnoWithFilenameObject`{.interpreted-text role="c:func"}, but the filename is given as a C string. *filename* is decoded from the `filesystem
> encoding and error handler`{.interpreted-text role="term"}.

> This is a convenience function to raise `OSError`{.interpreted-text role="exc"}. If called with *ierr* of `0`, the error code returned by a call to `!GetLastError`{.interpreted-text role="c:func"} is used instead. It calls the Win32 function `!FormatMessage`{.interpreted-text role="c:func"} to retrieve the Windows description of error code given by *ierr* or `!GetLastError`{.interpreted-text role="c:func"}, then it constructs a `OSError`{.interpreted-text role="exc"} object with the `~OSError.winerror`{.interpreted-text role="attr"} attribute set to the error code, the `~OSError.strerror`{.interpreted-text role="attr"} attribute set to the corresponding error message (gotten from `!FormatMessage`{.interpreted-text role="c:func"}), and then calls `PyErr_SetObject(PyExc_OSError, object)`. This function always returns `NULL`.
>
> ::: availability
> Windows.
> :::

> Similar to `PyErr_SetFromWindowsErr`{.interpreted-text role="c:func"}, with an additional parameter specifying the exception type to be raised.
>
> ::: availability
> Windows.
> :::

> Similar to `PyErr_SetFromWindowsErr`{.interpreted-text role="c:func"}, with the additional behavior that if *filename* is not `NULL`, it is decoded from the filesystem encoding (`os.fsdecode`{.interpreted-text role="func"}) and passed to the constructor of `OSError`{.interpreted-text role="exc"} as a third parameter to be used to define the `!filename`{.interpreted-text role="attr"} attribute of the exception instance.
>
> ::: availability
> Windows.
> :::

> Similar to `PyErr_SetExcFromWindowsErr`{.interpreted-text role="c:func"}, with the additional behavior that if *filename* is not `NULL`, it is passed to the constructor of `OSError`{.interpreted-text role="exc"} as a third parameter to be used to define the `!filename`{.interpreted-text role="attr"} attribute of the exception instance.
>
> ::: availability
> Windows.
> :::

> Similar to `PyErr_SetExcFromWindowsErrWithFilenameObject`{.interpreted-text role="c:func"}, but accepts a second filename object.
>
> ::: availability
> Windows.
> :::
>
> ::: versionadded
> 3.4
> :::

> Similar to `PyErr_SetFromWindowsErrWithFilename`{.interpreted-text role="c:func"}, with an additional parameter specifying the exception type to be raised.
>
> ::: availability
> Windows.
> :::

> This is a convenience function to raise `ImportError`{.interpreted-text role="exc"}. *msg* will be set as the exception\'s message string. *name* and *path*, both of which can be `NULL`, will be set as the `ImportError`{.interpreted-text role="exc"}\'s respective `name` and `path` attributes.
>
> ::: versionadded
> 3.3
> :::

> Much like `PyErr_SetImportError`{.interpreted-text role="c:func"} but this function allows for specifying a subclass of `ImportError`{.interpreted-text role="exc"} to raise.
>
> ::: versionadded
> 3.6
> :::

> Set file, line, and offset information for the current exception. If the current exception is not a `SyntaxError`{.interpreted-text role="exc"}, then it sets additional attributes, which make the exception printing subsystem think the exception is a `SyntaxError`{.interpreted-text role="exc"}.
>
> ::: versionadded
> 3.4
> :::

> Similar to `PyErr_SyntaxLocationObject`{.interpreted-text role="c:func"}, but also sets the *end_lineno* and *end_col_offset* information for the current exception.
>
> ::: versionadded
> 3.10
> :::

> Like `PyErr_SyntaxLocationObject`{.interpreted-text role="c:func"}, but *filename* is a byte string decoded from the `filesystem encoding and error handler`{.interpreted-text role="term"}.
>
> ::: versionadded
> 3.2
> :::

> Like `PyErr_SyntaxLocationEx`{.interpreted-text role="c:func"}, but the *col_offset* parameter is omitted.

> This is a shorthand for `PyErr_SetString(PyExc_SystemError, message)`, where *message* indicates that an internal operation (e.g. a Python/C API function) was invoked with an illegal argument. It is mostly for internal use.

> Get the source line in *filename* at line *lineno*. *filename* should be a Python `str`{.interpreted-text role="class"} object.
>
> On success, this function returns a Python string object with the found line. On failure, this function returns `NULL` without an exception set.

> Similar to `PyErr_ProgramTextObject`{.interpreted-text role="c:func"}, but *filename* is a `const char *`{.interpreted-text role="c:expr"}, which is decoded with the `filesystem encoding and error handler`{.interpreted-text role="term"}, instead of a Python object reference.

## Issuing warnings

Use these functions to issue warnings from C code. They mirror similar functions exported by the Python `warnings`{.interpreted-text role="mod"} module. They normally print a warning message to *sys.stderr*; however, it is also possible that the user has specified that warnings are to be turned into errors, and in that case they will raise an exception. It is also possible that the functions raise an exception because of a problem with the warning machinery. The return value is `0` if no exception is raised, or `-1` if an exception is raised. (It is not possible to determine whether a warning message is actually printed, nor what the reason is for the exception; this is intentional.) If an exception is raised, the caller should do its normal exception handling (for example, `Py_DECREF`{.interpreted-text role="c:func"} owned references and return an error value).

> Issue a warning message. The *category* argument is a warning category (see below) or `NULL`; the *message* argument is a UTF-8 encoded string. *stack_level* is a positive number giving a number of stack frames; the warning will be issued from the currently executing line of code in that stack frame. A *stack_level* of 1 is the function calling `PyErr_WarnEx`{.interpreted-text role="c:func"}, 2 is the function above that, and so forth.
>
> Warning categories must be subclasses of `PyExc_Warning`{.interpreted-text role="c:data"}; `PyExc_Warning`{.interpreted-text role="c:data"} is a subclass of `PyExc_Exception`{.interpreted-text role="c:data"}; the default warning category is `PyExc_RuntimeWarning`{.interpreted-text role="c:data"}. The standard Python warning categories are available as global variables whose names are enumerated at `standardwarningcategories`{.interpreted-text role="ref"}.
>
> For information about warning control, see the documentation for the `warnings`{.interpreted-text role="mod"} module and the `-W`{.interpreted-text role="option"} option in the command line documentation. There is no C API for warning control.

> Issue a warning message with explicit control over all warning attributes. This is a straightforward wrapper around the Python function `warnings.warn_explicit`{.interpreted-text role="func"}; see there for more information. The *module* and *registry* arguments may be set to `NULL` to get the default effect described there.
>
> ::: versionadded
> 3.4
> :::

> Similar to `PyErr_WarnExplicitObject`{.interpreted-text role="c:func"} except that *message* and *module* are UTF-8 encoded strings, and *filename* is decoded from the `filesystem encoding and error handler`{.interpreted-text role="term"}.

> Function similar to `PyErr_WarnEx`{.interpreted-text role="c:func"}, but use `PyUnicode_FromFormat`{.interpreted-text role="c:func"} to format the warning message. *format* is an ASCII-encoded string.
>
> ::: versionadded
> 3.2
> :::

> Similar to `PyErr_WarnExplicit`{.interpreted-text role="c:func"}, but uses `PyUnicode_FromFormat`{.interpreted-text role="c:func"} to format the warning message. *format* is an ASCII-encoded string.
>
> ::: versionadded
> 3.2
> :::

> Function similar to `PyErr_WarnFormat`{.interpreted-text role="c:func"}, but *category* is `ResourceWarning`{.interpreted-text role="exc"} and it passes *source* to `!warnings.WarningMessage`{.interpreted-text role="class"}.
>
> ::: versionadded
> 3.6
> :::

## Querying the error indicator

> Test whether the error indicator is set. If set, return the exception *type* (the first argument to the last call to one of the `PyErr_Set*` functions or to `PyErr_Restore`{.interpreted-text role="c:func"}). If not set, return `NULL`. You do not own a reference to the return value, so you do not need to `Py_DECREF`{.interpreted-text role="c:func"} it.
>
> The caller must have an `attached thread state`{.interpreted-text role="term"}.
>
> :::: note
> ::: title
> Note
> :::
>
> Do not compare the return value to a specific exception; use `PyErr_ExceptionMatches`{.interpreted-text role="c:func"} instead, shown below. (The comparison could easily fail since the exception may be an instance instead of a class, in the case of a class exception, or it may be a subclass of the expected exception.)
> ::::

> Equivalent to `PyErr_GivenExceptionMatches(PyErr_Occurred(), exc)`. This should only be called when an exception is actually set; a memory access violation will occur if no exception has been raised.

> Return true if the *given* exception matches the exception type in *exc*. If *exc* is a class object, this also returns true when *given* is an instance of a subclass. If *exc* is a tuple, all exception types in the tuple (and recursively in subtuples) are searched for a match.

> Return the exception currently being raised, clearing the error indicator at the same time. Return `NULL` if the error indicator is not set.
>
> This function is used by code that needs to catch exceptions, or code that needs to save and restore the error indicator temporarily.
>
> For example:
>
> ``` c
> {
>    PyObject *exc = PyErr_GetRaisedException();
>
>    /* ... code that might produce other errors ... */
>
>    PyErr_SetRaisedException(exc);
> }
> ```
>
> ::: seealso
> `PyErr_GetHandledException`{.interpreted-text role="c:func"}, to save the exception currently being handled.
> :::
>
> ::: versionadded
> 3.12
> :::

> Set *exc* as the exception currently being raised, clearing the existing exception if one is set.
>
> :::: warning
> ::: title
> Warning
> :::
>
> This call steals a reference to *exc*, which must be a valid exception.
> ::::
>
> ::: versionadded
> 3.12
> :::

> ::: deprecated
> 3.12
>
> Use `PyErr_GetRaisedException`{.interpreted-text role="c:func"} instead.
> :::
>
> Retrieve the error indicator into three variables whose addresses are passed. If the error indicator is not set, set all three variables to `NULL`. If it is set, it will be cleared and you own a reference to each object retrieved. The value and traceback object may be `NULL` even when the type object is not.
>
> :::: note
> ::: title
> Note
> :::
>
> This function is normally only used by legacy code that needs to catch exceptions or save and restore the error indicator temporarily.
>
> For example:
>
> ``` c
> {
>    PyObject *type, *value, *traceback;
>    PyErr_Fetch(&type, &value, &traceback);
>
>    /* ... code that might produce other errors ... */
>
>    PyErr_Restore(type, value, traceback);
> }
> ```
> ::::

> ::: deprecated
> 3.12
>
> Use `PyErr_SetRaisedException`{.interpreted-text role="c:func"} instead.
> :::
>
> Set the error indicator from the three objects, *type*, *value*, and *traceback*, clearing the existing exception if one is set. If the objects are `NULL`, the error indicator is cleared. Do not pass a `NULL` type and non-`NULL` value or traceback. The exception type should be a class. Do not pass an invalid exception type or value. (Violating these rules will cause subtle problems later.) This call takes away a reference to each object: you must own a reference to each object before the call and after the call you no longer own these references. (If you don\'t understand this, don\'t use this function. I warned you.)
>
> :::: note
> ::: title
> Note
> :::
>
> This function is normally only used by legacy code that needs to save and restore the error indicator temporarily. Use `PyErr_Fetch`{.interpreted-text role="c:func"} to save the current error indicator.
> ::::

> ::: deprecated
> 3.12
>
> Use `PyErr_GetRaisedException`{.interpreted-text role="c:func"} instead, to avoid any possible de-normalization.
> :::
>
> Under certain circumstances, the values returned by `PyErr_Fetch`{.interpreted-text role="c:func"} below can be \"unnormalized\", meaning that `*exc` is a class object but `*val` is not an instance of the same class. This function can be used to instantiate the class in that case. If the values are already normalized, nothing happens. The delayed normalization is implemented to improve performance.
>
> :::: note
> ::: title
> Note
> :::
>
> This function *does not* implicitly set the `~BaseException.__traceback__`{.interpreted-text role="attr"} attribute on the exception value. If setting the traceback appropriately is desired, the following additional snippet is needed:
>
> ``` c
> if (tb != NULL) {
>   PyException_SetTraceback(val, tb);
> }
> ```
> ::::

> Retrieve the active exception instance, as would be returned by `sys.exception`{.interpreted-text role="func"}. This refers to an exception that was *already caught*, not to an exception that was freshly raised. Returns a new reference to the exception or `NULL`. Does not modify the interpreter\'s exception state.
>
> :::: note
> ::: title
> Note
> :::
>
> This function is not normally used by code that wants to handle exceptions. Rather, it can be used when code needs to save and restore the exception state temporarily. Use `PyErr_SetHandledException`{.interpreted-text role="c:func"} to restore or clear the exception state.
> ::::
>
> ::: versionadded
> 3.11
> :::

> Set the active exception, as known from `sys.exception()`. This refers to an exception that was *already caught*, not to an exception that was freshly raised. To clear the exception state, pass `NULL`.
>
> :::: note
> ::: title
> Note
> :::
>
> This function is not normally used by code that wants to handle exceptions. Rather, it can be used when code needs to save and restore the exception state temporarily. Use `PyErr_GetHandledException`{.interpreted-text role="c:func"} to get the exception state.
> ::::
>
> ::: versionadded
> 3.11
> :::

> Retrieve the old-style representation of the exception info, as known from `sys.exc_info`{.interpreted-text role="func"}. This refers to an exception that was *already caught*, not to an exception that was freshly raised. Returns new references for the three objects, any of which may be `NULL`. Does not modify the exception info state. This function is kept for backwards compatibility. Prefer using `PyErr_GetHandledException`{.interpreted-text role="c:func"}.
>
> :::: note
> ::: title
> Note
> :::
>
> This function is not normally used by code that wants to handle exceptions. Rather, it can be used when code needs to save and restore the exception state temporarily. Use `PyErr_SetExcInfo`{.interpreted-text role="c:func"} to restore or clear the exception state.
> ::::
>
> ::: versionadded
> 3.3
> :::

> Set the exception info, as known from `sys.exc_info()`. This refers to an exception that was *already caught*, not to an exception that was freshly raised. This function steals the references of the arguments. To clear the exception state, pass `NULL` for all three arguments. This function is kept for backwards compatibility. Prefer using `PyErr_SetHandledException`{.interpreted-text role="c:func"}.
>
> :::: note
> ::: title
> Note
> :::
>
> This function is not normally used by code that wants to handle exceptions. Rather, it can be used when code needs to save and restore the exception state temporarily. Use `PyErr_GetExcInfo`{.interpreted-text role="c:func"} to read the exception state.
> ::::
>
> ::: versionadded
> 3.3
> :::
>
> ::: versionchanged
> 3.11 The `type` and `traceback` arguments are no longer used and can be NULL. The interpreter now derives them from the exception instance (the `value` argument). The function still steals references of all three arguments.
> :::

## Signal Handling

> ::: index
> pair: module; signal single: SIGINT (C macro) single: KeyboardInterrupt (built-in exception)
> :::
>
> Handle external interruptions, such as signals or activating a debugger, whose processing has been delayed until it is safe to run Python code and/or raise exceptions.
>
> For example, pressing `Ctrl-C`{.interpreted-text role="kbd"} causes a terminal to send the `signal.SIGINT`{.interpreted-text role="py:data"} signal. This function executes the corresponding Python signal handler, which, by default, raises the `KeyboardInterrupt`{.interpreted-text role="exc"} exception.
>
> `!PyErr_CheckSignals`{.interpreted-text role="c:func"} should be called by long-running C code frequently enough so that the response appears immediate to humans.
>
> Handlers invoked by this function currently include:
>
> - Signal handlers, including Python functions registered using the `signal`{.interpreted-text role="mod"} module.
>
>   Signal handlers are only run in the main thread of the main interpreter.
>
>   (This is where the function got the name: originally, signals were the only way to interrupt the interpreter.)
>
> - Running the garbage collector, if necessary.
>
> - Executing a pending `remote debugger <remote-debugging>`{.interpreted-text role="ref"} script.
>
> If any handler raises an exception, immediately return `-1` with that exception set. Any remaining interruptions are left to be processed on the next `PyErr_CheckSignals()`{.interpreted-text role="c:func"} invocation, if appropriate.
>
> If all handlers finish successfully, or there are no handlers to run, return `0`.
>
> ::: versionchanged
> 3.12 This function may now invoke the garbage collector.
> :::
>
> ::: versionchanged
> 3.14 This function may now execute a remote debugger script, if remote debugging is enabled.
> :::

> ::: index
> pair: module; signal single: SIGINT (C macro) single: KeyboardInterrupt (built-in exception)
> :::
>
> Simulate the effect of a `!SIGINT`{.interpreted-text role="c:macro"} signal arriving. This is equivalent to `PyErr_SetInterruptEx(SIGINT)`.
>
> :::: note
> ::: title
> Note
> :::
>
> This function is async-signal-safe. It can be called without an `attached thread state`{.interpreted-text role="term"} and from a C signal handler.
> ::::

> ::: index
> pair: module; signal single: KeyboardInterrupt (built-in exception)
> :::
>
> Simulate the effect of a signal arriving. The next time `PyErr_CheckSignals`{.interpreted-text role="c:func"} is called, the Python signal handler for the given signal number will be called.
>
> This function can be called by C code that sets up its own signal handling and wants Python signal handlers to be invoked as expected when an interruption is requested (for example when the user presses Ctrl-C to interrupt an operation).
>
> If the given signal isn\'t handled by Python (it was set to `signal.SIG_DFL`{.interpreted-text role="py:const"} or `signal.SIG_IGN`{.interpreted-text role="py:const"}), it will be ignored.
>
> If *signum* is outside of the allowed range of signal numbers, `-1` is returned. Otherwise, `0` is returned. The error indicator is never changed by this function.
>
> :::: note
> ::: title
> Note
> :::
>
> This function is async-signal-safe. It can be called without an `attached thread state`{.interpreted-text role="term"} and from a C signal handler.
> ::::
>
> ::: versionadded
> 3.10
> :::

> This utility function specifies a file descriptor to which the signal number is written as a single byte whenever a signal is received. *fd* must be non-blocking. It returns the previous such file descriptor.
>
> The value `-1` disables the feature; this is the initial state. This is equivalent to `signal.set_wakeup_fd`{.interpreted-text role="func"} in Python, but without any error checking. *fd* should be a valid file descriptor. The function should only be called from the main thread.
>
> ::: versionchanged
> 3.5 On Windows, the function now also supports socket handles.
> :::

## Exception Classes

> This utility function creates and returns a new exception class. The *name* argument must be the name of the new exception, a C string of the form `module.classname`. The *base* and *dict* arguments are normally `NULL`. This creates a class object derived from `Exception`{.interpreted-text role="exc"} (accessible in C as `PyExc_Exception`{.interpreted-text role="c:data"}).
>
> The `~type.__module__`{.interpreted-text role="attr"} attribute of the new class is set to the first part (up to the last dot) of the *name* argument, and the class name is set to the last part (after the last dot). The *base* argument can be used to specify alternate base classes; it can either be only one class or a tuple of classes. The *dict* argument can be used to specify a dictionary of class variables and methods.

> Same as `PyErr_NewException`{.interpreted-text role="c:func"}, except that the new exception class can easily be given a docstring: If *doc* is non-`NULL`, it will be used as the docstring for the exception class.
>
> ::: versionadded
> 3.2
> :::

> Return non-zero if *ob* is an exception class, zero otherwise. This function always succeeds.

> Return `~PyTypeObject.tp_name`{.interpreted-text role="c:member"} of the exception class *ob*.

> This is a `soft deprecated`{.interpreted-text role="term"} macro including the base fields for an exception object.
>
> This was included in Python\'s C API by mistake and is not designed for use in extensions. For creating custom exception objects, use `PyErr_NewException`{.interpreted-text role="c:func"} or otherwise create a class inheriting from `PyExc_BaseException`{.interpreted-text role="c:data"}.

## Exception Objects

> Return true if *op* is an instance of `BaseException`{.interpreted-text role="class"}, false otherwise. This function always succeeds.

> Equivalent to `Py_TYPE(op) <Py_TYPE>`{.interpreted-text role="c:func"}.

> Return the traceback associated with the exception as a new reference, as accessible from Python through the `~BaseException.__traceback__`{.interpreted-text role="attr"} attribute. If there is no traceback associated, this returns `NULL`.

> Set the traceback associated with the exception to *tb*. Use `Py_None` to clear it.

> Return the context (another exception instance during whose handling *ex* was raised) associated with the exception as a new reference, as accessible from Python through the `~BaseException.__context__`{.interpreted-text role="attr"} attribute. If there is no context associated, this returns `NULL`.

> Set the context associated with the exception to *ctx*. Use `NULL` to clear it. There is no type check to make sure that *ctx* is an exception instance. This steals a reference to *ctx*.

> Return the cause (either an exception instance, or `None`, set by `raise ... from ...`) associated with the exception as a new reference, as accessible from Python through the `~BaseException.__cause__`{.interpreted-text role="attr"} attribute.

> Set the cause associated with the exception to *cause*. Use `NULL` to clear it. There is no type check to make sure that *cause* is either an exception instance or `None`. This steals a reference to *cause*.
>
> The `~BaseException.__suppress_context__`{.interpreted-text role="attr"} attribute is implicitly set to `True` by this function.

> Return `~BaseException.args`{.interpreted-text role="attr"} of exception *ex*.

> Set `~BaseException.args`{.interpreted-text role="attr"} of exception *ex* to *args*.

> Implement part of the interpreter\'s implementation of `!except*`{.interpreted-text role="keyword"}. *orig* is the original exception that was caught, and *excs* is the list of the exceptions that need to be raised. This list contains the unhandled part of *orig*, if any, as well as the exceptions that were raised from the `!except*`{.interpreted-text role="keyword"} clauses (so they have a different traceback from *orig*) and those that were reraised (and have the same traceback as *orig*). Return the `ExceptionGroup`{.interpreted-text role="exc"} that needs to be reraised in the end, or `None` if there is nothing to reraise.
>
> ::: versionadded
> 3.12
> :::

## Unicode Exception Objects {#unicodeexceptions}

The following functions are used to create and modify Unicode exceptions from C.

> Create a `UnicodeDecodeError`{.interpreted-text role="class"} object with the attributes *encoding*, *object*, *length*, *start*, *end* and *reason*. *encoding* and *reason* are UTF-8 encoded strings.

## Recursion Control {#recursion}

These two functions provide a way to perform safe recursive calls at the C level, both in the core and in extension modules. They are needed if the recursive code does not necessarily invoke Python code (which tracks its recursion depth automatically). They are also not needed for *tp_call* implementations because the `call protocol <call>`{.interpreted-text role="ref"} takes care of recursion handling.

> Marks a point where a recursive C-level call is about to be performed.
>
> The function then checks if the stack limit is reached. If this is the case, a `RecursionError`{.interpreted-text role="exc"} is set and a nonzero value is returned. Otherwise, zero is returned.
>
> *where* should be a UTF-8 encoded string such as `" in instance check"` to be concatenated to the `RecursionError`{.interpreted-text role="exc"} message caused by the recursion depth limit.
>
> ::: seealso
> The `PyUnstable_ThreadState_SetStackProtection`{.interpreted-text role="c:func"} function.
> :::
>
> ::: versionchanged
> 3.9 This function is now also available in the `limited API <limited-c-api>`{.interpreted-text role="ref"}.
> :::

> Ends a `Py_EnterRecursiveCall`{.interpreted-text role="c:func"}. Must be called once for each *successful* invocation of `Py_EnterRecursiveCall`{.interpreted-text role="c:func"}.
>
> ::: versionchanged
> 3.9 This function is now also available in the `limited API <limited-c-api>`{.interpreted-text role="ref"}.
> :::

Properly implementing `~PyTypeObject.tp_repr`{.interpreted-text role="c:member"} for container types requires special recursion handling. In addition to protecting the stack, `~PyTypeObject.tp_repr`{.interpreted-text role="c:member"} also needs to track objects to prevent cycles. The following two functions facilitate this functionality. Effectively, these are the C equivalent to `reprlib.recursive_repr`{.interpreted-text role="func"}.

> Called at the beginning of the `~PyTypeObject.tp_repr`{.interpreted-text role="c:member"} implementation to detect cycles.
>
> If the object has already been processed, the function returns a positive integer. In that case the `~PyTypeObject.tp_repr`{.interpreted-text role="c:member"} implementation should return a string object indicating a cycle. As examples, `dict`{.interpreted-text role="class"} objects return `{...}` and `list`{.interpreted-text role="class"} objects return `[...]`.
>
> The function will return a negative integer if the recursion limit is reached. In that case the `~PyTypeObject.tp_repr`{.interpreted-text role="c:member"} implementation should typically return `NULL`.
>
> Otherwise, the function returns zero and the `~PyTypeObject.tp_repr`{.interpreted-text role="c:member"} implementation can continue normally.

> Ends a `Py_ReprEnter`{.interpreted-text role="c:func"}. Must be called once for each invocation of `Py_ReprEnter`{.interpreted-text role="c:func"} that returns zero.

> Get the recursion limit for the current interpreter. It can be set with `Py_SetRecursionLimit`{.interpreted-text role="c:func"}. The recursion limit prevents the Python interpreter stack from growing infinitely.
>
> This function cannot fail, and the caller must hold an `attached thread state`{.interpreted-text role="term"}.
>
> ::: seealso
> `sys.getrecursionlimit`{.interpreted-text role="py:func"}
> :::

> Set the recursion limit for the current interpreter.
>
> This function cannot fail, and the caller must hold an `attached thread state`{.interpreted-text role="term"}.
>
> ::: seealso
> `sys.setrecursionlimit`{.interpreted-text role="py:func"}
> :::

## Exception and warning types {#standardexceptions}

All standard Python exceptions and warning categories are available as global variables whose names are `PyExc_` followed by the Python exception name. These have the type `PyObject*`{.interpreted-text role="c:expr"}; they are all class objects.

For completeness, here are all the variables:

### Exception types

  C name   Python name
  -------- ---------------------------------------------------------
           `BaseException`{.interpreted-text role="exc"}
           `BaseExceptionGroup`{.interpreted-text role="exc"}
           `Exception`{.interpreted-text role="exc"}
           `ArithmeticError`{.interpreted-text role="exc"}
           `AssertionError`{.interpreted-text role="exc"}
           `AttributeError`{.interpreted-text role="exc"}
           `BlockingIOError`{.interpreted-text role="exc"}
           `BrokenPipeError`{.interpreted-text role="exc"}
           `BufferError`{.interpreted-text role="exc"}
           `ChildProcessError`{.interpreted-text role="exc"}
           `ConnectionAbortedError`{.interpreted-text role="exc"}
           `ConnectionError`{.interpreted-text role="exc"}
           `ConnectionRefusedError`{.interpreted-text role="exc"}
           `ConnectionResetError`{.interpreted-text role="exc"}
           `EOFError`{.interpreted-text role="exc"}
           `FileExistsError`{.interpreted-text role="exc"}
           `FileNotFoundError`{.interpreted-text role="exc"}
           `FloatingPointError`{.interpreted-text role="exc"}
           `GeneratorExit`{.interpreted-text role="exc"}
           `ImportCycleError`{.interpreted-text role="exc"}
           `ImportError`{.interpreted-text role="exc"}
           `IndentationError`{.interpreted-text role="exc"}
           `IndexError`{.interpreted-text role="exc"}
           `InterruptedError`{.interpreted-text role="exc"}
           `IsADirectoryError`{.interpreted-text role="exc"}
           `KeyError`{.interpreted-text role="exc"}
           `KeyboardInterrupt`{.interpreted-text role="exc"}
           `LookupError`{.interpreted-text role="exc"}
           `MemoryError`{.interpreted-text role="exc"}
           `ModuleNotFoundError`{.interpreted-text role="exc"}
           `NameError`{.interpreted-text role="exc"}
           `NotADirectoryError`{.interpreted-text role="exc"}
           `NotImplementedError`{.interpreted-text role="exc"}
           `OSError`{.interpreted-text role="exc"}
           `OverflowError`{.interpreted-text role="exc"}
           `PermissionError`{.interpreted-text role="exc"}
           `ProcessLookupError`{.interpreted-text role="exc"}
           `PythonFinalizationError`{.interpreted-text role="exc"}
           `RecursionError`{.interpreted-text role="exc"}
           `ReferenceError`{.interpreted-text role="exc"}
           `RuntimeError`{.interpreted-text role="exc"}
           `StopAsyncIteration`{.interpreted-text role="exc"}
           `StopIteration`{.interpreted-text role="exc"}
           `SyntaxError`{.interpreted-text role="exc"}
           `SystemError`{.interpreted-text role="exc"}
           `SystemExit`{.interpreted-text role="exc"}
           `TabError`{.interpreted-text role="exc"}
           `TimeoutError`{.interpreted-text role="exc"}
           `TypeError`{.interpreted-text role="exc"}
           `UnboundLocalError`{.interpreted-text role="exc"}
           `UnicodeDecodeError`{.interpreted-text role="exc"}
           `UnicodeEncodeError`{.interpreted-text role="exc"}
           `UnicodeError`{.interpreted-text role="exc"}
           `UnicodeTranslateError`{.interpreted-text role="exc"}
           `ValueError`{.interpreted-text role="exc"}
           `ZeroDivisionError`{.interpreted-text role="exc"}

::: versionadded
3.3 `PyExc_BlockingIOError`{.interpreted-text role="c:data"}, `PyExc_BrokenPipeError`{.interpreted-text role="c:data"}, `PyExc_ChildProcessError`{.interpreted-text role="c:data"}, `PyExc_ConnectionError`{.interpreted-text role="c:data"}, `PyExc_ConnectionAbortedError`{.interpreted-text role="c:data"}, `PyExc_ConnectionRefusedError`{.interpreted-text role="c:data"}, `PyExc_ConnectionResetError`{.interpreted-text role="c:data"}, `PyExc_FileExistsError`{.interpreted-text role="c:data"}, `PyExc_FileNotFoundError`{.interpreted-text role="c:data"}, `PyExc_InterruptedError`{.interpreted-text role="c:data"}, `PyExc_IsADirectoryError`{.interpreted-text role="c:data"}, `PyExc_NotADirectoryError`{.interpreted-text role="c:data"}, `PyExc_PermissionError`{.interpreted-text role="c:data"}, `PyExc_ProcessLookupError`{.interpreted-text role="c:data"} and `PyExc_TimeoutError`{.interpreted-text role="c:data"} were introduced following `3151`{.interpreted-text role="pep"}.
:::

::: versionadded
3.5 `PyExc_StopAsyncIteration`{.interpreted-text role="c:data"} and `PyExc_RecursionError`{.interpreted-text role="c:data"}.
:::

::: versionadded
3.6 `PyExc_ModuleNotFoundError`{.interpreted-text role="c:data"}.
:::

::: versionadded
3.11 `PyExc_BaseExceptionGroup`{.interpreted-text role="c:data"}.
:::

### OSError aliases

The following are a compatibility aliases to `PyExc_OSError`{.interpreted-text role="c:data"}.

::: versionchanged
3.3 These aliases used to be separate exception types.
:::

  C name   Python name                               Notes
  -------- ----------------------------------------- ----------------------------
           `OSError`{.interpreted-text role="exc"}   
           `OSError`{.interpreted-text role="exc"}   
           `OSError`{.interpreted-text role="exc"}   [\[win\]](#win){.citation}

Notes:

### Warning types {#standardwarningcategories}

  C name   Python name
  -------- -----------------------------------------------------------
           `Warning`{.interpreted-text role="exc"}
           `BytesWarning`{.interpreted-text role="exc"}
           `DeprecationWarning`{.interpreted-text role="exc"}
           `EncodingWarning`{.interpreted-text role="exc"}
           `FutureWarning`{.interpreted-text role="exc"}
           `ImportWarning`{.interpreted-text role="exc"}
           `PendingDeprecationWarning`{.interpreted-text role="exc"}
           `ResourceWarning`{.interpreted-text role="exc"}
           `RuntimeWarning`{.interpreted-text role="exc"}
           `SyntaxWarning`{.interpreted-text role="exc"}
           `UnicodeWarning`{.interpreted-text role="exc"}
           `UserWarning`{.interpreted-text role="exc"}

::: versionadded
3.2 `PyExc_ResourceWarning`{.interpreted-text role="c:data"}.
:::

::: versionadded
3.10 `PyExc_EncodingWarning`{.interpreted-text role="c:data"}.
:::

## Tracebacks

> Type object for traceback objects. This is available as `types.TracebackType`{.interpreted-text role="class"} in the Python layer.

> Return true if *op* is a traceback object, false otherwise. This function does not account for subtypes.

> Replace the `~BaseException.__traceback__`{.interpreted-text role="attr"} attribute on the current exception with a new traceback prepending *f* to the existing chain.
>
> Calling this function without an exception set is undefined behavior.
>
> This function returns `0` on success, and returns `-1` with an exception set on failure.

> Write the traceback *tb* into the file *f*.
>
> This function returns `0` on success, and returns `-1` with an exception set on failure.

::: {#citations}

[win]{#win .citation-label}

:   `!PyExc_WindowsError`{.interpreted-text role="c:var"} is only defined on Windows; protect code that uses this by testing that the preprocessor macro `MS_WINDOWS` is defined.
:::
