# Mapping Protocol {#mapping}

See also `PyObject_GetItem`{.interpreted-text role="c:func"}, `PyObject_SetItem`{.interpreted-text role="c:func"} and `PyObject_DelItem`{.interpreted-text role="c:func"}.

> Return `1` if the object provides the mapping protocol or supports slicing, and `0` otherwise. Note that it returns `1` for Python classes with a `~object.__getitem__`{.interpreted-text role="meth"} method, since in general it is impossible to determine what type of keys the class supports. This function always succeeds.

> This is the same as `PyObject_GetItem`{.interpreted-text role="c:func"}, but *key* is specified as a `const char*`{.interpreted-text role="c:expr"} UTF-8 encoded bytes string, rather than a `PyObject*`{.interpreted-text role="c:expr"}.

> Variant of `PyObject_GetItem`{.interpreted-text role="c:func"} which doesn\'t raise `KeyError`{.interpreted-text role="exc"} if the key is not found.
>
> If the key is found, return `1` and set *\*result* to a new `strong reference`{.interpreted-text role="term"} to the corresponding value. If the key is not found, return `0` and set *\*result* to `NULL`; the `KeyError`{.interpreted-text role="exc"} is silenced. If an error other than `KeyError`{.interpreted-text role="exc"} is raised, return `-1` and set *\*result* to `NULL`.
>
> ::: versionadded
> 3.13
> :::

> This is the same as `PyMapping_GetOptionalItem`{.interpreted-text role="c:func"}, but *key* is specified as a `const char*`{.interpreted-text role="c:expr"} UTF-8 encoded bytes string, rather than a `PyObject*`{.interpreted-text role="c:expr"}.
>
> ::: versionadded
> 3.13
> :::

> This is the same as `PyObject_SetItem`{.interpreted-text role="c:func"}, but *key* is specified as a `const char*`{.interpreted-text role="c:expr"} UTF-8 encoded bytes string, rather than a `PyObject*`{.interpreted-text role="c:expr"}.

> This is an alias of `PyObject_DelItem`{.interpreted-text role="c:func"}.

> This is the same as `PyObject_DelItem`{.interpreted-text role="c:func"}, but *key* is specified as a `const char*`{.interpreted-text role="c:expr"} UTF-8 encoded bytes string, rather than a `PyObject*`{.interpreted-text role="c:expr"}.

> Return `1` if the mapping object has the key *key* and `0` otherwise. This is equivalent to the Python expression `key in o`. On failure, return `-1`.
>
> ::: versionadded
> 3.13
> :::

> This is the same as `PyMapping_HasKeyWithError`{.interpreted-text role="c:func"}, but *key* is specified as a `const char*`{.interpreted-text role="c:expr"} UTF-8 encoded bytes string, rather than a `PyObject*`{.interpreted-text role="c:expr"}.
>
> ::: versionadded
> 3.13
> :::

> Return `1` if the mapping object has the key *key* and `0` otherwise. This is equivalent to the Python expression `key in o`. This function always succeeds.
>
> :::: note
> ::: title
> Note
> :::
>
> Exceptions which occur when this calls the `~object.__getitem__`{.interpreted-text role="meth"} method are silently ignored. For proper error handling, use `PyMapping_HasKeyWithError`{.interpreted-text role="c:func"}, `PyMapping_GetOptionalItem`{.interpreted-text role="c:func"} or `PyObject_GetItem()`{.interpreted-text role="c:func"} instead.
> ::::

> This is the same as `PyMapping_HasKey`{.interpreted-text role="c:func"}, but *key* is specified as a `const char*`{.interpreted-text role="c:expr"} UTF-8 encoded bytes string, rather than a `PyObject*`{.interpreted-text role="c:expr"}.
>
> :::: note
> ::: title
> Note
> :::
>
> Exceptions that occur when this calls the `~object.__getitem__`{.interpreted-text role="meth"} method or while creating the temporary `str`{.interpreted-text role="class"} object are silently ignored. For proper error handling, use `PyMapping_HasKeyStringWithError`{.interpreted-text role="c:func"}, `PyMapping_GetOptionalItemString`{.interpreted-text role="c:func"} or `PyMapping_GetItemString`{.interpreted-text role="c:func"} instead.
> ::::

> On success, return a list of the keys in object *o*. On failure, return `NULL`.
>
> ::: versionchanged
> 3.7 Previously, the function returned a list or a tuple.
> :::

> On success, return a list of the values in object *o*. On failure, return `NULL`.
>
> ::: versionchanged
> 3.7 Previously, the function returned a list or a tuple.
> :::

> On success, return a list of the items in object *o*, where each item is a tuple containing a key-value pair. On failure, return `NULL`.
>
> ::: versionchanged
> 3.7 Previously, the function returned a list or a tuple.
> :::
