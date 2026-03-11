# Boolean Objects {#boolobjects}

Booleans in Python are implemented as a subclass of integers. There are only two booleans, `Py_False`{.interpreted-text role="c:data"} and `Py_True`{.interpreted-text role="c:data"}. As such, the normal creation and deletion functions don\'t apply to booleans. The following macros are available, however.

> This instance of `PyTypeObject`{.interpreted-text role="c:type"} represents the Python boolean type; it is the same object as `bool`{.interpreted-text role="class"} in the Python layer.

> Return true if *o* is of type `PyBool_Type`{.interpreted-text role="c:data"}. This function always succeeds.

> The Python `False` object. This object has no methods and is `immortal`{.interpreted-text role="term"}.
>
> ::: versionchanged
> 3.12 `Py_False`{.interpreted-text role="c:data"} is `immortal`{.interpreted-text role="term"}.
> :::

> The Python `True` object. This object has no methods and is `immortal`{.interpreted-text role="term"}.
>
> ::: versionchanged
> 3.12 `Py_True`{.interpreted-text role="c:data"} is `immortal`{.interpreted-text role="term"}.
> :::

> Return `Py_False`{.interpreted-text role="c:data"} from a function.

> Return `Py_True`{.interpreted-text role="c:data"} from a function.

> Return `Py_True`{.interpreted-text role="c:data"} or `Py_False`{.interpreted-text role="c:data"}, depending on the truth value of *v*.
