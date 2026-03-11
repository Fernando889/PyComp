# Profiling and tracing {#profiling}

The Python interpreter provides some low-level support for attaching profiling and execution tracing facilities. These are used for profiling, debugging, and coverage analysis tools.

This C interface allows the profiling or tracing code to avoid the overhead of calling through Python-level callable objects, making a direct C function call instead. The essential attributes of the facility have not changed; the interface allows trace functions to be installed per-thread, and the basic events reported to the trace function are the same as had been reported to the Python-level trace functions in previous versions.

> The type of the trace function registered using `PyEval_SetProfile`{.interpreted-text role="c:func"} and `PyEval_SetTrace`{.interpreted-text role="c:func"}. The first parameter is the object passed to the registration function as *obj*, *frame* is the frame object to which the event pertains, *what* is one of the constants `PyTrace_CALL`{.interpreted-text role="c:data"}, `PyTrace_EXCEPTION`{.interpreted-text role="c:data"}, `PyTrace_LINE`{.interpreted-text role="c:data"}, `PyTrace_RETURN`{.interpreted-text role="c:data"}, `PyTrace_C_CALL`{.interpreted-text role="c:data"}, `PyTrace_C_EXCEPTION`{.interpreted-text role="c:data"}, `PyTrace_C_RETURN`{.interpreted-text role="c:data"}, or `PyTrace_OPCODE`{.interpreted-text role="c:data"}, and *arg* depends on the value of *what*:
>
>   ----------------------------------------------------------------------------------------------------------------------------------------------
>   Value of *what*                                          Meaning of *arg*
>   -------------------------------------------------------- -------------------------------------------------------------------------------------
>   `PyTrace_CALL`{.interpreted-text role="c:data"}          Always `Py_None`{.interpreted-text role="c:data"}.
>
>   `PyTrace_EXCEPTION`{.interpreted-text role="c:data"}     Exception information as returned by `sys.exc_info`{.interpreted-text role="func"}.
>
>   `PyTrace_LINE`{.interpreted-text role="c:data"}          Always `Py_None`{.interpreted-text role="c:data"}.
>
>   `PyTrace_RETURN`{.interpreted-text role="c:data"}        Value being returned to the caller, or `NULL` if caused by an exception.
>
>   `PyTrace_C_CALL`{.interpreted-text role="c:data"}        Function object being called.
>
>   `PyTrace_C_EXCEPTION`{.interpreted-text role="c:data"}   Function object being called.
>
>   `PyTrace_C_RETURN`{.interpreted-text role="c:data"}      Function object being called.
>
>   `PyTrace_OPCODE`{.interpreted-text role="c:data"}        Always `Py_None`{.interpreted-text role="c:data"}.
>   ----------------------------------------------------------------------------------------------------------------------------------------------

> The value of the *what* parameter to a `Py_tracefunc`{.interpreted-text role="c:type"} function when a new call to a function or method is being reported, or a new entry into a generator. Note that the creation of the iterator for a generator function is not reported as there is no control transfer to the Python bytecode in the corresponding frame.

> The value of the *what* parameter to a `Py_tracefunc`{.interpreted-text role="c:type"} function when an exception has been raised. The callback function is called with this value for *what* when after any bytecode is processed after which the exception becomes set within the frame being executed. The effect of this is that as exception propagation causes the Python stack to unwind, the callback is called upon return to each frame as the exception propagates. Only trace functions receive these events; they are not needed by the profiler.

> The value passed as the *what* parameter to a `Py_tracefunc`{.interpreted-text role="c:type"} function (but not a profiling function) when a line-number event is being reported. It may be disabled for a frame by setting `~frame.f_trace_lines`{.interpreted-text role="attr"} to *0* on that frame.

> The value for the *what* parameter to `Py_tracefunc`{.interpreted-text role="c:type"} functions when a call is about to return.

> The value for the *what* parameter to `Py_tracefunc`{.interpreted-text role="c:type"} functions when a C function is about to be called.

> The value for the *what* parameter to `Py_tracefunc`{.interpreted-text role="c:type"} functions when a C function has raised an exception.

> The value for the *what* parameter to `Py_tracefunc`{.interpreted-text role="c:type"} functions when a C function has returned.

> The value for the *what* parameter to `Py_tracefunc`{.interpreted-text role="c:type"} functions (but not profiling functions) when a new opcode is about to be executed. This event is not emitted by default: it must be explicitly requested by setting `~frame.f_trace_opcodes`{.interpreted-text role="attr"} to *1* on the frame.

> Set the profiler function to *func*. The *obj* parameter is passed to the function as its first parameter, and may be any Python object, or `NULL`. If the profile function needs to maintain state, using a different value for *obj* for each thread provides a convenient and thread-safe place to store it. The profile function is called for all monitored events except `PyTrace_LINE`{.interpreted-text role="c:data"} `PyTrace_OPCODE`{.interpreted-text role="c:data"} and `PyTrace_EXCEPTION`{.interpreted-text role="c:data"}.
>
> See also the `sys.setprofile`{.interpreted-text role="func"} function.
>
> The caller must have an `attached thread state`{.interpreted-text role="term"}.

> Like `PyEval_SetProfile`{.interpreted-text role="c:func"} but sets the profile function in all running threads belonging to the current interpreter instead of the setting it only on the current thread.
>
> The caller must have an `attached thread state`{.interpreted-text role="term"}.
>
> As `PyEval_SetProfile`{.interpreted-text role="c:func"}, this function ignores any exceptions raised while setting the profile functions in all threads.

::: versionadded
3.12
:::

> Set the tracing function to *func*. This is similar to `PyEval_SetProfile`{.interpreted-text role="c:func"}, except the tracing function does receive line-number events and per-opcode events, but does not receive any event related to C function objects being called. Any trace function registered using `PyEval_SetTrace`{.interpreted-text role="c:func"} will not receive `PyTrace_C_CALL`{.interpreted-text role="c:data"}, `PyTrace_C_EXCEPTION`{.interpreted-text role="c:data"} or `PyTrace_C_RETURN`{.interpreted-text role="c:data"} as a value for the *what* parameter.
>
> See also the `sys.settrace`{.interpreted-text role="func"} function.
>
> The caller must have an `attached thread state`{.interpreted-text role="term"}.

> Like `PyEval_SetTrace`{.interpreted-text role="c:func"} but sets the tracing function in all running threads belonging to the current interpreter instead of the setting it only on the current thread.
>
> The caller must have an `attached thread state`{.interpreted-text role="term"}.
>
> As `PyEval_SetTrace`{.interpreted-text role="c:func"}, this function ignores any exceptions raised while setting the trace functions in all threads.

::: versionadded
3.12
:::

# Reference tracing

::: versionadded
3.13
:::

> The type of the trace function registered using `PyRefTracer_SetTracer`{.interpreted-text role="c:func"}. The first parameter is a Python object that has been just created (when **event** is set to `PyRefTracer_CREATE`{.interpreted-text role="c:data"}) or about to be destroyed (when **event** is set to `PyRefTracer_DESTROY`{.interpreted-text role="c:data"}). The **data** argument is the opaque pointer that was provided when `PyRefTracer_SetTracer`{.interpreted-text role="c:func"} was called.
>
> If a new tracing function is registered replacing the current one, a call to the trace function will be made with the object set to **NULL** and **event** set to `PyRefTracer_TRACKER_REMOVED`{.interpreted-text role="c:data"}. This will happen just before the new function is registered.

::: versionadded
3.13
:::

> The value for the *event* parameter to `PyRefTracer`{.interpreted-text role="c:type"} functions when a Python object has been created.

> The value for the *event* parameter to `PyRefTracer`{.interpreted-text role="c:type"} functions when a Python object has been destroyed.

> The value for the *event* parameter to `PyRefTracer`{.interpreted-text role="c:type"} functions when the current tracer is about to be replaced by a new one.
>
> ::: versionadded
> 3.14
> :::

> Register a reference tracer function. The function will be called when a new Python object has been created or when an object is going to be destroyed. If **data** is provided it must be an opaque pointer that will be provided when the tracer function is called. Return `0` on success. Set an exception and return `-1` on error.
>
> Note that tracer functions **must not** create Python objects inside or otherwise the call will be re-entrant. The tracer also **must not** clear any existing exception or set an exception. A `thread state`{.interpreted-text role="term"} will be active every time the tracer function is called.
>
> There must be an `attached thread state`{.interpreted-text role="term"} when calling this function.
>
> If another tracer function was already registered, the old function will be called with **event** set to `PyRefTracer_TRACKER_REMOVED`{.interpreted-text role="c:data"} just before the new function is registered.

::: versionadded
3.13
:::

> Get the registered reference tracer function and the value of the opaque data pointer that was registered when `PyRefTracer_SetTracer`{.interpreted-text role="c:func"} was called. If no tracer was registered this function will return NULL and will set the **data** pointer to NULL.
>
> There must be an `attached thread state`{.interpreted-text role="term"} when calling this function.

::: versionadded
3.13
:::
