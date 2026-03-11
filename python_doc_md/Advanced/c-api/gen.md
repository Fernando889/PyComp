# Generator Objects {#gen-objects}

Generator objects are what Python uses to implement generator iterators. They are normally created by iterating over a function that yields values, rather than explicitly calling `PyGen_New`{.interpreted-text role="c:func"} or `PyGen_NewWithQualName`{.interpreted-text role="c:func"}.

> The C structure used for generator objects.

> The type object corresponding to generator objects.

> Return true if *ob* is a generator object; *ob* must not be `NULL`. This function always succeeds.

> Return true if *ob*\'s type is `PyGen_Type`{.interpreted-text role="c:type"}; *ob* must not be `NULL`. This function always succeeds.

> Create and return a new generator object based on the *frame* object. A reference to *frame* is stolen by this function. The argument must not be `NULL`.

> Create and return a new generator object based on the *frame* object, with `__name__` and `__qualname__` set to *name* and *qualname*. A reference to *frame* is stolen by this function. The *frame* argument must not be `NULL`.

> Return a new `strong reference`{.interpreted-text role="term"} to the code object wrapped by *gen*. This function always succeeds.

## Asynchronous Generator Objects

::: seealso
`525`{.interpreted-text role="pep"}
:::

> The type object corresponding to asynchronous generator objects. This is available as `types.AsyncGeneratorType`{.interpreted-text role="class"} in the Python layer.
>
> ::: versionadded
> 3.6
> :::

> Create a new asynchronous generator wrapping *frame*, with `__name__` and `__qualname__` set to *name* and *qualname*. *frame* is stolen by this function and must not be `NULL`.
>
> On success, this function returns a `strong reference`{.interpreted-text role="term"} to the new asynchronous generator. On failure, this function returns `NULL` with an exception set.
>
> ::: versionadded
> 3.6
> :::

> Return true if *op* is an asynchronous generator object, false otherwise. This function always succeeds.
>
> ::: versionadded
> 3.6
> :::

## Deprecated API

> This is a `soft deprecated`{.interpreted-text role="term"} API that was included in Python\'s C API by mistake.
>
> It is solely here for completeness; do not use this API.
