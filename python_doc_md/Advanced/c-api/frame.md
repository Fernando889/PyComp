# Frame Objects

> The C structure of the objects used to describe frame objects.
>
> There are no public members in this structure.
>
> ::: versionchanged
> 3.11 The members of this structure were removed from the public C API. Refer to the `What's New entry <pyframeobject-3.11-hiding>`{.interpreted-text role="ref"} for details.
> :::

The `PyEval_GetFrame`{.interpreted-text role="c:func"} and `PyThreadState_GetFrame`{.interpreted-text role="c:func"} functions can be used to get a frame object.

See also `Reflection <reflection>`{.interpreted-text role="ref"}.

> The type of frame objects. It is the same object as `types.FrameType`{.interpreted-text role="py:class"} in the Python layer.
>
> ::: versionchanged
> 3.11
>
> Previously, this type was only available after including `<frameobject.h>`.
> :::

> Create a new frame object. This function returns a `strong reference`{.interpreted-text role="term"} to the new frame object on success, and returns `NULL` with an exception set on failure.

> Return non-zero if *obj* is a frame object.
>
> ::: versionchanged
> 3.11
>
> Previously, this function was only available after including `<frameobject.h>`.
> :::

> Get the *frame* next outer frame.
>
> Return a `strong reference`{.interpreted-text role="term"}, or `NULL` if *frame* has no outer frame.
>
> ::: versionadded
> 3.9
> :::

> Get the *frame*\'s `~frame.f_builtins`{.interpreted-text role="attr"} attribute.
>
> Return a `strong reference`{.interpreted-text role="term"}. The result cannot be `NULL`.
>
> ::: versionadded
> 3.11
> :::

> Get the *frame* code.
>
> Return a `strong reference`{.interpreted-text role="term"}.
>
> The result (frame code) cannot be `NULL`.
>
> ::: versionadded
> 3.9
> :::

> Get the generator, coroutine, or async generator that owns this frame, or `NULL` if this frame is not owned by a generator. Does not raise an exception, even if the return value is `NULL`.
>
> Return a `strong reference`{.interpreted-text role="term"}, or `NULL`.
>
> ::: versionadded
> 3.11
> :::

> Get the *frame*\'s `~frame.f_globals`{.interpreted-text role="attr"} attribute.
>
> Return a `strong reference`{.interpreted-text role="term"}. The result cannot be `NULL`.
>
> ::: versionadded
> 3.11
> :::

> Get the *frame*\'s `~frame.f_lasti`{.interpreted-text role="attr"} attribute.
>
> Returns -1 if `frame.f_lasti` is `None`.
>
> ::: versionadded
> 3.11
> :::

> Get the variable *name* of *frame*.
>
> - Return a `strong reference`{.interpreted-text role="term"} to the variable value on success.
> - Raise `NameError`{.interpreted-text role="exc"} and return `NULL` if the variable does not exist.
> - Raise an exception and return `NULL` on error.
>
> *name* type must be a `str`{.interpreted-text role="class"}.
>
> ::: versionadded
> 3.12
> :::

> Similar to `PyFrame_GetVar`{.interpreted-text role="c:func"}, but the variable name is a C string encoded in UTF-8.
>
> ::: versionadded
> 3.12
> :::

> Get the *frame*\'s `~frame.f_locals`{.interpreted-text role="attr"} attribute. If the frame refers to an `optimized scope`{.interpreted-text role="term"}, this returns a write-through proxy object that allows modifying the locals. In all other cases (classes, modules, `exec`{.interpreted-text role="func"}, `eval`{.interpreted-text role="func"}) it returns the mapping representing the frame locals directly (as described for `locals`{.interpreted-text role="func"}).
>
> Return a `strong reference`{.interpreted-text role="term"}.
>
> ::: versionadded
> 3.11
> :::
>
> ::: versionchanged
> 3.13 As part of `667`{.interpreted-text role="pep"}, return an instance of `PyFrameLocalsProxy_Type`{.interpreted-text role="c:var"}.
> :::

> Return the line number that *frame* is currently executing.

## Frame Locals Proxies

::: versionadded
3.13
:::

The `~frame.f_locals`{.interpreted-text role="attr"} attribute on a `frame object <frame-objects>`{.interpreted-text role="ref"} is an instance of a \"frame-locals proxy\". The proxy object exposes a write-through view of the underlying locals dictionary for the frame. This ensures that the variables exposed by `f_locals` are always up to date with the live local variables in the frame itself.

See `667`{.interpreted-text role="pep"} for more information.

> The type of frame `locals`{.interpreted-text role="func"} proxy objects.

> Return non-zero if *obj* is a frame `locals`{.interpreted-text role="func"} proxy.

## Legacy Local Variable APIs

These APIs are `soft deprecated`{.interpreted-text role="term"}. As of Python 3.13, they do nothing. They exist solely for backwards compatibility.

> This function is `soft deprecated`{.interpreted-text role="term"} and does nothing.
>
> Prior to Python 3.13, this function would copy the `~frame.f_locals`{.interpreted-text role="attr"} attribute of *f* to the internal \"fast\" array of local variables, allowing changes in frame objects to be visible to the interpreter. If *clear* was true, this function would process variables that were unset in the locals dictionary.
>
> ::: versionchanged
> 3.13 This function now does nothing.
> :::

> This function is `soft deprecated`{.interpreted-text role="term"} and does nothing.
>
> Prior to Python 3.13, this function would copy the internal \"fast\" array of local variables (which is used by the interpreter) to the `~frame.f_locals`{.interpreted-text role="attr"} attribute of *f*, allowing changes in local variables to be visible to frame objects.
>
> ::: versionchanged
> 3.13 This function now does nothing.
> :::

> This function is `soft deprecated`{.interpreted-text role="term"} and does nothing.
>
> Prior to Python 3.13, this function was similar to `PyFrame_FastToLocals`{.interpreted-text role="c:func"}, but would return `0` on success, and `-1` with an exception set on failure.
>
> ::: versionchanged
> 3.13 This function now does nothing.
> :::

::: seealso
`667`{.interpreted-text role="pep"}
:::

## Internal Frames

Unless using `523`{.interpreted-text role="pep"}, you will not need this.

> The interpreter\'s internal frame representation.
>
> ::: versionadded
> 3.11
> :::

> Return a `strong reference`{.interpreted-text role="term"} to the code object for the frame.
>
> ::: versionadded
> 3.12
> :::

> Return the byte offset into the last executed instruction.
>
> ::: versionadded
> 3.12
> :::

> Return the currently executing line number, or -1 if there is no line number.
>
> ::: versionadded
> 3.12
> :::
