# Byte Array Objects {#bytearrayobjects}

::: index
pair: object; bytearray
:::

> This subtype of `PyObject`{.interpreted-text role="c:type"} represents a Python bytearray object.

> This instance of `PyTypeObject`{.interpreted-text role="c:type"} represents the Python bytearray type; it is the same object as `bytearray`{.interpreted-text role="class"} in the Python layer.

## Type check macros

> Return true if the object *o* is a bytearray object or an instance of a subtype of the bytearray type. This function always succeeds.

> Return true if the object *o* is a bytearray object, but not an instance of a subtype of the bytearray type. This function always succeeds.

## Direct API functions

> Return a new bytearray object from any object, *o*, that implements the `buffer protocol <bufferobjects>`{.interpreted-text role="ref"}.
>
> On failure, return `NULL` with an exception set.

> Create a new bytearray object from *string* and its length, *len*.
>
> On failure, return `NULL` with an exception set.

> Concat bytearrays *a* and *b* and return a new bytearray with the result.
>
> On failure, return `NULL` with an exception set.

> Return the size of *bytearray* after checking for a `NULL` pointer.

> Return the contents of *bytearray* as a char array after checking for a `NULL` pointer. The returned array always has an extra null byte appended.

> Resize the internal buffer of *bytearray* to *len*. Failure is a `-1` return with an exception set.
>
> ::: versionchanged
> 3.14 A negative *len* will now result in an exception being set and -1 returned.
> :::

## Macros

These macros trade safety for speed and they don\'t check pointers.

> Similar to `PyByteArray_AsString`{.interpreted-text role="c:func"}, but without error checking.

> Similar to `PyByteArray_Size`{.interpreted-text role="c:func"}, but without error checking.
