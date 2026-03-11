# Tuple Objects {#tupleobjects}

::: index
pair: object; tuple
:::

> This subtype of `PyObject`{.interpreted-text role="c:type"} represents a Python tuple object.

> This instance of `PyTypeObject`{.interpreted-text role="c:type"} represents the Python tuple type; it is the same object as `tuple`{.interpreted-text role="class"} in the Python layer.

> Return true if *p* is a tuple object or an instance of a subtype of the tuple type. This function always succeeds.

> Return true if *p* is a tuple object, but not an instance of a subtype of the tuple type. This function always succeeds.

> Return a new tuple object of size *len*, or `NULL` with an exception set on failure.

> Create a tuple of *size* items and copy references from *array* to the new tuple.
>
> *array* can be NULL if *size* is `0`.
>
> On success, return a new reference. On error, set an exception and return `NULL`.
>
> ::: versionadded
> 3.15
> :::

> Return a new tuple object of size *n*, or `NULL` with an exception set on failure. The tuple values are initialized to the subsequent *n* C arguments pointing to Python objects. `PyTuple_Pack(2, a, b)` is equivalent to `Py_BuildValue("(OO)", a, b)`.

> Take a pointer to a tuple object, and return the size of that tuple. On error, return `-1` with an exception set.

> Like `PyTuple_Size`{.interpreted-text role="c:func"}, but without error checking.

> Return the object at position *pos* in the tuple pointed to by *p*. If *pos* is negative or out of bounds, return `NULL` and set an `IndexError`{.interpreted-text role="exc"} exception.
>
> The returned reference is borrowed from the tuple *p* (that is: it is only valid as long as you hold a reference to *p*). To get a `strong reference`{.interpreted-text role="term"}, use `Py_NewRef(PyTuple_GetItem(...)) <Py_NewRef>`{.interpreted-text role="c:func"} or `PySequence_GetItem`{.interpreted-text role="c:func"}.

> Like `PyTuple_GetItem`{.interpreted-text role="c:func"}, but does no checking of its arguments.

> Return the slice of the tuple pointed to by *p* between *low* and *high*, or `NULL` with an exception set on failure.
>
> This is the equivalent of the Python expression `p[low:high]`. Indexing from the end of the tuple is not supported.

> Insert a reference to object *o* at position *pos* of the tuple pointed to by *p*. Return `0` on success. If *pos* is out of bounds, return `-1` and set an `IndexError`{.interpreted-text role="exc"} exception.
>
> :::: note
> ::: title
> Note
> :::
>
> This function \"steals\" a reference to *o* and discards a reference to an item already in the tuple at the affected position.
> ::::

> Like `PyTuple_SetItem`{.interpreted-text role="c:func"}, but does no error checking, and should *only* be used to fill in brand new tuples.
>
> Bounds checking is performed as an assertion if Python is built in `debug mode <debug-build>`{.interpreted-text role="ref"} or `with assertions <--with-assertions>`{.interpreted-text role="option"}.
>
> :::: note
> ::: title
> Note
> :::
>
> This function \"steals\" a reference to *o*, and, unlike `PyTuple_SetItem`{.interpreted-text role="c:func"}, does *not* discard a reference to any item that is being replaced; any reference in the tuple at position *pos* will be leaked.
> ::::
>
> :::: warning
> ::: title
> Warning
> :::
>
> This macro should *only* be used on tuples that are newly created. Using this macro on a tuple that is already in use (or in other words, has a refcount \> 1) could lead to undefined behavior.
> ::::

> Can be used to resize a tuple. *newsize* will be the new length of the tuple. Because tuples are *supposed* to be immutable, this should only be used if there is only one reference to the object. Do *not* use this if the tuple may already be known to some other part of the code. The tuple will always grow or shrink at the end. Think of this as destroying the old tuple and creating a new one, only more efficiently. Returns `0` on success. Client code should never assume that the resulting value of `*p` will be the same as before calling this function. If the object referenced by `*p` is replaced, the original `*p` is destroyed. On failure, returns `-1` and sets `*p` to `NULL`, and raises `MemoryError`{.interpreted-text role="exc"} or `SystemError`{.interpreted-text role="exc"}.

# Struct Sequence Objects

A struct sequence object is a `named tuple`{.interpreted-text role="term"}, that is, a sequence whose items can also be accessed through attributes. It is similar to `collections.namedtuple`{.interpreted-text role="func"}, but provides a slightly different interface.

To create a struct sequence, you first have to create a specific struct sequence type.

> Create a new struct sequence type from the data in *desc*, described below. Instances of the resulting type can be created with `PyStructSequence_New`{.interpreted-text role="c:func"}.
>
> Return `NULL` with an exception set on failure.

> Initializes a struct sequence type *type* from *desc* in place.

> Like `PyStructSequence_InitType`{.interpreted-text role="c:func"}, but returns `0` on success and `-1` with an exception set on failure.
>
> ::: versionadded
> 3.4
> :::

> Contains the meta information of a struct sequence type to create.
>
> > Fully qualified name of the type; null-terminated UTF-8 encoded. The name must contain the module name.
>
> > Pointer to docstring for the type or `NULL` to omit.
>
> > Pointer to `NULL`-terminated array with field names of the new type.
>
> > Number of fields visible to the Python side (if used as tuple).

> Describes a field of a struct sequence. As a struct sequence is modeled as a tuple, all fields are typed as `PyObject*`{.interpreted-text role="c:expr"}. The index in the `~PyStructSequence_Desc.fields`{.interpreted-text role="c:member"} array of the `PyStructSequence_Desc`{.interpreted-text role="c:type"} determines which field of the struct sequence is described.
>
> > Name for the field or `NULL` to end the list of named fields, set to `PyStructSequence_UnnamedField`{.interpreted-text role="c:data"} to leave unnamed.
>
> > Field docstring or `NULL` to omit.

> Special value for a field name to leave it unnamed.
>
> ::: versionchanged
> 3.9 The type was changed from `char *`.
> :::

> Creates an instance of *type*, which must have been created with `PyStructSequence_NewType`{.interpreted-text role="c:func"}.
>
> Return `NULL` with an exception set on failure.

> Return the object at position *pos* in the struct sequence pointed to by *p*.
>
> Bounds checking is performed as an assertion if Python is built in `debug mode <debug-build>`{.interpreted-text role="ref"} or `with assertions <--with-assertions>`{.interpreted-text role="option"}.

> Alias to `PyStructSequence_GetItem`{.interpreted-text role="c:func"}.
>
> ::: versionchanged
> 3.13 Now implemented as an alias to `PyStructSequence_GetItem`{.interpreted-text role="c:func"}.
> :::

> Sets the field at index *pos* of the struct sequence *p* to value *o*. Like `PyTuple_SET_ITEM`{.interpreted-text role="c:func"}, this should only be used to fill in brand new instances.
>
> Bounds checking is performed as an assertion if Python is built in `debug mode <debug-build>`{.interpreted-text role="ref"} or `with assertions <--with-assertions>`{.interpreted-text role="option"}.
>
> :::: note
> ::: title
> Note
> :::
>
> This function \"steals\" a reference to *o*.
> ::::

> Alias to `PyStructSequence_SetItem`{.interpreted-text role="c:func"}.
>
> ::: versionchanged
> 3.13 Now implemented as an alias to `PyStructSequence_SetItem`{.interpreted-text role="c:func"}.
> :::
