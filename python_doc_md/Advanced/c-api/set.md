# Set Objects {#setobjects}

::: index
pair: object; set pair: object; frozenset
:::

This section details the public API for `set`{.interpreted-text role="class"} and `frozenset`{.interpreted-text role="class"} objects. Any functionality not listed below is best accessed using either the abstract object protocol (including `PyObject_CallMethod`{.interpreted-text role="c:func"}, `PyObject_RichCompareBool`{.interpreted-text role="c:func"}, `PyObject_Hash`{.interpreted-text role="c:func"}, `PyObject_Repr`{.interpreted-text role="c:func"}, `PyObject_IsTrue`{.interpreted-text role="c:func"}, `PyObject_Print`{.interpreted-text role="c:func"}, and `PyObject_GetIter`{.interpreted-text role="c:func"}) or the abstract number protocol (including `PyNumber_And`{.interpreted-text role="c:func"}, `PyNumber_Subtract`{.interpreted-text role="c:func"}, `PyNumber_Or`{.interpreted-text role="c:func"}, `PyNumber_Xor`{.interpreted-text role="c:func"}, `PyNumber_InPlaceAnd`{.interpreted-text role="c:func"}, `PyNumber_InPlaceSubtract`{.interpreted-text role="c:func"}, `PyNumber_InPlaceOr`{.interpreted-text role="c:func"}, and `PyNumber_InPlaceXor`{.interpreted-text role="c:func"}).

> This subtype of `PyObject`{.interpreted-text role="c:type"} is used to hold the internal data for both `set`{.interpreted-text role="class"} and `frozenset`{.interpreted-text role="class"} objects. It is like a `PyDictObject`{.interpreted-text role="c:type"} in that it is a fixed size for small sets (much like tuple storage) and will point to a separate, variable sized block of memory for medium and large sized sets (much like list storage). None of the fields of this structure should be considered public and all are subject to change. All access should be done through the documented API rather than by manipulating the values in the structure.

> This is an instance of `PyTypeObject`{.interpreted-text role="c:type"} representing the Python `set`{.interpreted-text role="class"} type.

> This is an instance of `PyTypeObject`{.interpreted-text role="c:type"} representing the Python `frozenset`{.interpreted-text role="class"} type.

The following type check macros work on pointers to any Python object. Likewise, the constructor functions work with any iterable Python object.

> Return true if *p* is a `set`{.interpreted-text role="class"} object or an instance of a subtype. This function always succeeds.

> Return true if *p* is a `frozenset`{.interpreted-text role="class"} object or an instance of a subtype. This function always succeeds.

> Return true if *p* is a `set`{.interpreted-text role="class"} object, a `frozenset`{.interpreted-text role="class"} object, or an instance of a subtype. This function always succeeds.

> Return true if *p* is a `set`{.interpreted-text role="class"} object but not an instance of a subtype. This function always succeeds.
>
> ::: versionadded
> 3.10
> :::

> Return true if *p* is a `set`{.interpreted-text role="class"} object or a `frozenset`{.interpreted-text role="class"} object but not an instance of a subtype. This function always succeeds.

> Return true if *p* is a `frozenset`{.interpreted-text role="class"} object but not an instance of a subtype. This function always succeeds.

> Return a new `set`{.interpreted-text role="class"} containing objects returned by the *iterable*. The *iterable* may be `NULL` to create a new empty set. Return the new set on success or `NULL` on failure. Raise `TypeError`{.interpreted-text role="exc"} if *iterable* is not actually iterable. The constructor is also useful for copying a set (`c=set(s)`).

> Return a new `frozenset`{.interpreted-text role="class"} containing objects returned by the *iterable*. The *iterable* may be `NULL` to create a new empty frozenset. Return the new set on success or `NULL` on failure. Raise `TypeError`{.interpreted-text role="exc"} if *iterable* is not actually iterable.

The following functions and macros are available for instances of `set`{.interpreted-text role="class"} or `frozenset`{.interpreted-text role="class"} or instances of their subtypes.

> ::: index
> pair: built-in function; len
> :::
>
> Return the length of a `set`{.interpreted-text role="class"} or `frozenset`{.interpreted-text role="class"} object. Equivalent to `len(anyset)`. Raises a `SystemError`{.interpreted-text role="exc"} if *anyset* is not a `set`{.interpreted-text role="class"}, `frozenset`{.interpreted-text role="class"}, or an instance of a subtype.

> Macro form of `PySet_Size`{.interpreted-text role="c:func"} without error checking.

> Return `1` if found, `0` if not found, and `-1` if an error is encountered. Unlike the Python `~object.__contains__`{.interpreted-text role="meth"} method, this function does not automatically convert unhashable sets into temporary frozensets. Raise a `TypeError`{.interpreted-text role="exc"} if the *key* is unhashable. Raise `SystemError`{.interpreted-text role="exc"} if *anyset* is not a `set`{.interpreted-text role="class"}, `frozenset`{.interpreted-text role="class"}, or an instance of a subtype.

> Add *key* to a `set`{.interpreted-text role="class"} instance. Also works with `frozenset`{.interpreted-text role="class"} instances (like `PyTuple_SetItem`{.interpreted-text role="c:func"} it can be used to fill in the values of brand new frozensets before they are exposed to other code). Return `0` on success or `-1` on failure. Raise a `TypeError`{.interpreted-text role="exc"} if the *key* is unhashable. Raise a `MemoryError`{.interpreted-text role="exc"} if there is no room to grow. Raise a `SystemError`{.interpreted-text role="exc"} if *set* is not an instance of `set`{.interpreted-text role="class"} or its subtype.

The following functions are available for instances of `set`{.interpreted-text role="class"} or its subtypes but not for instances of `frozenset`{.interpreted-text role="class"} or its subtypes.

> Return `1` if found and removed, `0` if not found (no action taken), and `-1` if an error is encountered. Does not raise `KeyError`{.interpreted-text role="exc"} for missing keys. Raise a `TypeError`{.interpreted-text role="exc"} if the *key* is unhashable. Unlike the Python `~set.discard`{.interpreted-text role="meth"} method, this function does not automatically convert unhashable sets into temporary frozensets. Raise `SystemError`{.interpreted-text role="exc"} if *set* is not an instance of `set`{.interpreted-text role="class"} or its subtype.

> Return a new reference to an arbitrary object in the *set*, and removes the object from the *set*. Return `NULL` on failure. Raise `KeyError`{.interpreted-text role="exc"} if the set is empty. Raise a `SystemError`{.interpreted-text role="exc"} if *set* is not an instance of `set`{.interpreted-text role="class"} or its subtype.

> Empty an existing set of all elements. Return `0` on success. Return `-1` and raise `SystemError`{.interpreted-text role="exc"} if *set* is not an instance of `set`{.interpreted-text role="class"} or its subtype.

## Deprecated API

> A `soft deprecated`{.interpreted-text role="term"} constant representing the size of an internal preallocated table inside `PySetObject`{.interpreted-text role="c:type"} instances.
>
> This is documented solely for completeness, as there are no guarantees that a given version of CPython uses preallocated tables with a fixed size. In code that does not deal with unstable set internals, `!PySet_MINSIZE`{.interpreted-text role="c:macro"} can be replaced with a small constant like `8`.
>
> If looking for the size of a set, use `PySet_Size`{.interpreted-text role="c:func"} instead.
