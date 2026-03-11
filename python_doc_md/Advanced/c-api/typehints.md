# Objects for Type Hinting {#typehintobjects}

Various built-in types for type hinting are provided. Currently, two types exist \-- `GenericAlias <types-genericalias>`{.interpreted-text role="ref"} and `Union <types-union>`{.interpreted-text role="ref"}. Only `GenericAlias` is exposed to C.

> Create a `GenericAlias <types-genericalias>`{.interpreted-text role="ref"} object. Equivalent to calling the Python class `types.GenericAlias`{.interpreted-text role="class"}. The *origin* and *args* arguments set the `GenericAlias`\'s `__origin__` and `__args__` attributes respectively. *origin* should be a `PyTypeObject*`{.interpreted-text role="c:expr"}, and *args* can be a `PyTupleObject*`{.interpreted-text role="c:expr"} or any `PyObject*`. If *args* passed is not a tuple, a 1-tuple is automatically constructed and `__args__` is set to `(args,)`. Minimal checking is done for the arguments, so the function will succeed even if *origin* is not a type. The `GenericAlias`\'s `__parameters__` attribute is constructed lazily from `__args__`. On failure, an exception is raised and `NULL` is returned.
>
> Here\'s an example of how to make an extension type generic:
>
> ``` c
> ...
> static PyMethodDef my_obj_methods[] = {
>     // Other methods.
>     ...
>     {"__class_getitem__", Py_GenericAlias, METH_O|METH_CLASS, "See PEP 585"}
>     ...
> }
> ```
>
> ::: seealso
> The data model method `~object.__class_getitem__`{.interpreted-text role="meth"}.
> :::
>
> ::: versionadded
> 3.9
> :::

> The C type of the object returned by `Py_GenericAlias`{.interpreted-text role="c:func"}. Equivalent to `types.GenericAlias`{.interpreted-text role="class"} in Python.
>
> ::: versionadded
> 3.9
> :::
