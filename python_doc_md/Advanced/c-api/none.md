# The `None` Object {#noneobject}

::: index
pair: object; None
:::

Note that the `PyTypeObject`{.interpreted-text role="c:type"} for `None` is not directly exposed in the Python/C API. Since `None` is a singleton, testing for object identity (using `==` in C) is sufficient. There is no `!PyNone_Check`{.interpreted-text role="c:func"} function for the same reason.

> The Python `None` object, denoting lack of value. This object has no methods and is `immortal`{.interpreted-text role="term"}.
>
> ::: versionchanged
> 3.12 `Py_None`{.interpreted-text role="c:data"} is `immortal`{.interpreted-text role="term"}.
> :::

> Return `Py_None`{.interpreted-text role="c:data"} from a function.
