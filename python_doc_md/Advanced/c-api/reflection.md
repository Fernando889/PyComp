# Reflection

> ::: deprecated
> 3.13
>
> Use `PyEval_GetFrameBuiltins`{.interpreted-text role="c:func"} instead.
> :::
>
> Return a dictionary of the builtins in the current execution frame, or the interpreter of the thread state if no frame is currently executing.

> ::: deprecated
> 3.13
>
> Use either `PyEval_GetFrameLocals`{.interpreted-text role="c:func"} to obtain the same behaviour as calling `locals`{.interpreted-text role="func"} in Python code, or else call `PyFrame_GetLocals`{.interpreted-text role="c:func"} on the result of `PyEval_GetFrame`{.interpreted-text role="c:func"} to access the `~frame.f_locals`{.interpreted-text role="attr"} attribute of the currently executing frame.
> :::
>
> Return a mapping providing access to the local variables in the current execution frame, or `NULL` if no frame is currently executing.
>
> Refer to `locals`{.interpreted-text role="func"} for details of the mapping returned at different scopes.
>
> As this function returns a `borrowed reference`{.interpreted-text role="term"}, the dictionary returned for `optimized scopes <optimized scope>`{.interpreted-text role="term"} is cached on the frame object and will remain alive as long as the frame object does. Unlike `PyEval_GetFrameLocals`{.interpreted-text role="c:func"} and `locals`{.interpreted-text role="func"}, subsequent calls to this function in the same frame will update the contents of the cached dictionary to reflect changes in the state of the local variables rather than returning a new snapshot.
>
> ::: versionchanged
> 3.13 As part of `667`{.interpreted-text role="pep"}, `PyFrame_GetLocals`{.interpreted-text role="c:func"}, `locals`{.interpreted-text role="func"}, and `FrameType.f_locals <frame.f_locals>`{.interpreted-text role="attr"} no longer make use of the shared cache dictionary. Refer to the `What's New entry <whatsnew313-locals-semantics>`{.interpreted-text role="ref"} for additional details.
> :::

> ::: deprecated
> 3.13
>
> Use `PyEval_GetFrameGlobals`{.interpreted-text role="c:func"} instead.
> :::
>
> Return a dictionary of the global variables in the current execution frame, or `NULL` if no frame is currently executing.

> Return the `attached thread state`{.interpreted-text role="term"}\'s frame, which is `NULL` if no frame is currently executing.
>
> See also `PyThreadState_GetFrame`{.interpreted-text role="c:func"}.

> Return a dictionary of the builtins in the current execution frame, or the interpreter of the thread state if no frame is currently executing.
>
> ::: versionadded
> 3.13
> :::

> Return a dictionary of the local variables in the current execution frame, or `NULL` if no frame is currently executing. Equivalent to calling `locals`{.interpreted-text role="func"} in Python code.
>
> To access `~frame.f_locals`{.interpreted-text role="attr"} on the current frame without making an independent snapshot in `optimized scopes <optimized scope>`{.interpreted-text role="term"}, call `PyFrame_GetLocals`{.interpreted-text role="c:func"} on the result of `PyEval_GetFrame`{.interpreted-text role="c:func"}.
>
> ::: versionadded
> 3.13
> :::

> Return a dictionary of the global variables in the current execution frame, or `NULL` if no frame is currently executing. Equivalent to calling `globals`{.interpreted-text role="func"} in Python code.
>
> ::: versionadded
> 3.13
> :::

> Return the name of *func* if it is a function, class or instance object, else the name of *func*s type.

> Return a description string, depending on the type of *func*. Return values include \"()\" for functions and methods, \" constructor\", \" instance\", and \" object\". Concatenated with the result of `PyEval_GetFuncName`{.interpreted-text role="c:func"}, the result will be a description of *func*.
