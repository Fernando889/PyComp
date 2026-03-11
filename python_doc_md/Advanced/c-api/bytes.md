# Bytes Objects {#bytesobjects}

These functions raise `TypeError`{.interpreted-text role="exc"} when expecting a bytes parameter and called with a non-bytes parameter.

::: index
pair: object; bytes
:::

> This subtype of `PyObject`{.interpreted-text role="c:type"} represents a Python bytes object.

> This instance of `PyTypeObject`{.interpreted-text role="c:type"} represents the Python bytes type; it is the same object as `bytes`{.interpreted-text role="class"} in the Python layer.

> Return true if the object *o* is a bytes object or an instance of a subtype of the bytes type. This function always succeeds.

> Return true if the object *o* is a bytes object, but not an instance of a subtype of the bytes type. This function always succeeds.

> Return a new bytes object with a copy of the string *v* as value on success, and `NULL` on failure. The parameter *v* must not be `NULL`; it will not be checked.

> Return a new bytes object with a copy of the string *v* as value and length *len* on success, and `NULL` on failure. If *v* is `NULL`, the contents of the bytes object are uninitialized.
>
> ::: deprecated
> 3.15 `PyBytes_FromStringAndSize(NULL, len)` is `soft deprecated`{.interpreted-text role="term"}, use the `PyBytesWriter`{.interpreted-text role="c:type"} API instead.
> :::

> Take a C `printf`{.interpreted-text role="c:func"}-style *format* string and a variable number of arguments, calculate the size of the resulting Python bytes object and return a bytes object with the values formatted into it. The variable arguments must be C types and must correspond exactly to the format characters in the *format* string. The following format characters are allowed:
>
> ::: tabularcolumns
> [\|l\|](##SUBST##|l|)l[\|L\|](##SUBST##|L|)
> :::
>
>   -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
>   Format Characters   Type                     Comment
>   ------------------- ------------------------ --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
>   `%%`                *n/a*                    The literal % character.
>
>   `%c`                int                      A single byte, represented as a C int.
>
>   `%d`                int                      Equivalent to `printf("%d")`.[^1]
>
>   `%u`                unsigned int             Equivalent to `printf("%u")`.[^2]
>
>   `%ld`               long                     Equivalent to `printf("%ld")`.[^3]
>
>   `%lu`               unsigned long            Equivalent to `printf("%lu")`.[^4]
>
>   `%zd`               :c:type:\`Py_ssize_t\`   Equivalent to `printf("%zd")`.[^5]
>
>   `%zu`               size_t                   Equivalent to `printf("%zu")`.[^6]
>
>   `%i`                int                      Equivalent to `printf("%i")`.[^7]
>
>   `%x`                int                      Equivalent to `printf("%x")`.[^8]
>
>   `%s`                const char\*             A null-terminated C character array.
>
>   `%p`                const void\*             The hex representation of a C pointer. Mostly equivalent to `printf("%p")` except that it is guaranteed to start with the literal `0x` regardless of what the platform\'s `printf` yields.
>   -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
>
> An unrecognized format character causes all the rest of the format string to be copied as-is to the result object, and any extra arguments discarded.

> Identical to `PyBytes_FromFormat`{.interpreted-text role="c:func"} except that it takes exactly two arguments.

> Return the bytes representation of object *o* that implements the buffer protocol.

> Return the length of the bytes in bytes object *o*.

> Similar to `PyBytes_Size`{.interpreted-text role="c:func"}, but without error checking.

> Return a pointer to the contents of *o*. The pointer refers to the internal buffer of *o*, which consists of `len(o) + 1` bytes. The last byte in the buffer is always null, regardless of whether there are any other null bytes. The data must not be modified in any way, unless the object was just created using `PyBytes_FromStringAndSize(NULL, size)`. It must not be deallocated. If *o* is not a bytes object at all, `PyBytes_AsString`{.interpreted-text role="c:func"} returns `NULL` and raises `TypeError`{.interpreted-text role="exc"}.

> Similar to `PyBytes_AsString`{.interpreted-text role="c:func"}, but without error checking.

> Return the null-terminated contents of the object *obj* through the output variables *buffer* and *length*. Returns `0` on success.
>
> If *length* is `NULL`, the bytes object may not contain embedded null bytes; if it does, the function returns `-1` and a `ValueError`{.interpreted-text role="exc"} is raised.
>
> The buffer refers to an internal buffer of *obj*, which includes an additional null byte at the end (not counted in *length*). The data must not be modified in any way, unless the object was just created using `PyBytes_FromStringAndSize(NULL, size)`. It must not be deallocated. If *obj* is not a bytes object at all, `PyBytes_AsStringAndSize`{.interpreted-text role="c:func"} returns `-1` and raises `TypeError`{.interpreted-text role="exc"}.
>
> ::: versionchanged
> 3.5 Previously, `TypeError`{.interpreted-text role="exc"} was raised when embedded null bytes were encountered in the bytes object.
> :::

> Create a new bytes object in *\*bytes* containing the contents of *newpart* appended to *bytes*; the caller will own the new reference. The reference to the old value of *bytes* will be stolen. If the new object cannot be created, the old reference to *bytes* will still be discarded and the value of *\*bytes* will be set to `NULL`; the appropriate exception will be set.

> Create a new bytes object in *\*bytes* containing the contents of *newpart* appended to *bytes*. This version releases the `strong reference`{.interpreted-text role="term"} to *newpart* (i.e. decrements its reference count).

> Similar to `sep.join(iterable)` in Python.
>
> *sep* must be Python `bytes`{.interpreted-text role="class"} object. (Note that `PyUnicode_Join`{.interpreted-text role="c:func"} accepts `NULL` separator and treats it as a space, whereas `PyBytes_Join`{.interpreted-text role="c:func"} doesn\'t accept `NULL` separator.)
>
> *iterable* must be an iterable object yielding objects that implement the `buffer protocol <bufferobjects>`{.interpreted-text role="ref"}.
>
> On success, return a new `bytes`{.interpreted-text role="class"} object. On error, set an exception and return `NULL`.
>
> ::: versionadded
> 3.14
> :::

> Resize a bytes object. *newsize* will be the new length of the bytes object. You can think of it as creating a new bytes object and destroying the old one, only more efficiently. Pass the address of an existing bytes object as an lvalue (it may be written into), and the new size desired. On success, *\*bytes* holds the resized bytes object and `0` is returned; the address in *\*bytes* may differ from its input value. If the reallocation fails, the original bytes object at *\*bytes* is deallocated, *\*bytes* is set to `NULL`, `MemoryError`{.interpreted-text role="exc"} is set, and `-1` is returned.
>
> ::: deprecated
> 3.15 The function is `soft deprecated`{.interpreted-text role="term"}, use the `PyBytesWriter`{.interpreted-text role="c:type"} API instead.
> :::

> Get the string representation of *bytes*. This function is currently used to implement `!bytes.__repr__`{.interpreted-text role="meth"} in Python.
>
> This function does not do type checking; it is undefined behavior to pass *bytes* as a non-bytes object or `NULL`.
>
> If *smartquotes* is true, the representation will use a double-quoted string instead of single-quoted string when single-quotes are present in *bytes*. For example, the byte string `'Python'` would be represented as `b"'Python'"` when *smartquotes* is true, or `b'\'Python\''` when it is false.
>
> On success, this function returns a `strong reference`{.interpreted-text role="term"} to a `str`{.interpreted-text role="class"} object containing the representation. On failure, this returns `NULL` with an exception set.

> Unescape a backslash-escaped string *s*. *s* must not be `NULL`. *len* must be the size of *s*.
>
> *errors* must be one of `"strict"`, `"replace"`, or `"ignore"`. If *errors* is `NULL`, then `"strict"` is used by default.
>
> On success, this function returns a `strong reference`{.interpreted-text role="term"} to a Python `bytes`{.interpreted-text role="class"} object containing the unescaped string. On failure, this function returns `NULL` with an exception set.
>
> ::: versionchanged
> 3.9 *unicode* and *recode_encoding* are now unused.
> :::

# PyBytesWriter

The `PyBytesWriter`{.interpreted-text role="c:type"} API can be used to create a Python `bytes`{.interpreted-text role="class"} object.

::: versionadded
3.15
:::

> A bytes writer instance.
>
> The API is **not thread safe**: a writer should only be used by a single thread at the same time.
>
> The instance must be destroyed by `PyBytesWriter_Finish`{.interpreted-text role="c:func"} on success, or `PyBytesWriter_Discard`{.interpreted-text role="c:func"} on error.

## Create, Finish, Discard

> Create a `PyBytesWriter`{.interpreted-text role="c:type"} to write *size* bytes.
>
> If *size* is greater than zero, allocate *size* bytes, and set the writer size to *size*. The caller is responsible to write *size* bytes using `PyBytesWriter_GetData`{.interpreted-text role="c:func"}. This function does not overallocate.
>
> On error, set an exception and return `NULL`.
>
> *size* must be positive or zero.

> Finish a `PyBytesWriter`{.interpreted-text role="c:type"} created by `PyBytesWriter_Create`{.interpreted-text role="c:func"}.
>
> On success, return a Python `bytes`{.interpreted-text role="class"} object. On error, set an exception and return `NULL`.
>
> The writer instance is invalid after the call in any case. No API can be called on the writer after `PyBytesWriter_Finish`{.interpreted-text role="c:func"}.

> Similar to `PyBytesWriter_Finish`{.interpreted-text role="c:func"}, but resize the writer to *size* bytes before creating the `bytes`{.interpreted-text role="class"} object.

> Similar to `PyBytesWriter_Finish`{.interpreted-text role="c:func"}, but resize the writer using *buf* pointer before creating the `bytes`{.interpreted-text role="class"} object.
>
> Set an exception and return `NULL` if *buf* pointer is outside the internal buffer bounds.
>
> Function pseudo-code:
>
> ``` c
> Py_ssize_t size = (char*)buf - (char*)PyBytesWriter_GetData(writer);
> return PyBytesWriter_FinishWithSize(writer, size);
> ```

> Discard a `PyBytesWriter`{.interpreted-text role="c:type"} created by `PyBytesWriter_Create`{.interpreted-text role="c:func"}.
>
> Do nothing if *writer* is `NULL`.
>
> The writer instance is invalid after the call. No API can be called on the writer after `PyBytesWriter_Discard`{.interpreted-text role="c:func"}.

## High-level API

> Grow the *writer* internal buffer by *size* bytes, write *size* bytes of *bytes* at the *writer* end, and add *size* to the *writer* size.
>
> If *size* is equal to `-1`, call `strlen(bytes)` to get the string length.
>
> On success, return `0`. On error, set an exception and return `-1`.

> Similar to `PyBytes_FromFormat`{.interpreted-text role="c:func"}, but write the output directly at the writer end. Grow the writer internal buffer on demand. Then add the written size to the writer size.
>
> On success, return `0`. On error, set an exception and return `-1`.

## Getters

> Get the writer size.

> Get the writer data: start of the internal buffer.
>
> The pointer is valid until `PyBytesWriter_Finish`{.interpreted-text role="c:func"} or `PyBytesWriter_Discard`{.interpreted-text role="c:func"} is called on *writer*.

## Low-level API

> Resize the writer to *size* bytes. It can be used to enlarge or to shrink the writer. This function typically overallocates to achieve amortized performance when resizing multiple times.
>
> Newly allocated bytes are left uninitialized.
>
> On success, return `0`. On error, set an exception and return `-1`.
>
> *size* must be positive or zero.

> Resize the writer by adding *grow* bytes to the current writer size. This function typically overallocates to achieve amortized performance when resizing multiple times.
>
> Newly allocated bytes are left uninitialized.
>
> On success, return `0`. On error, set an exception and return `-1`.
>
> *size* can be negative to shrink the writer.

> Similar to `PyBytesWriter_Grow`{.interpreted-text role="c:func"}, but update also the *buf* pointer.
>
> The *buf* pointer is moved if the internal buffer is moved in memory. The *buf* relative position within the internal buffer is left unchanged.
>
> On error, set an exception and return `NULL`.
>
> *buf* must not be `NULL`.
>
> Function pseudo-code:
>
> ``` c
> Py_ssize_t pos = (char*)buf - (char*)PyBytesWriter_GetData(writer);
> if (PyBytesWriter_Grow(writer, size) < 0) {
>     return NULL;
> }
> return (char*)PyBytesWriter_GetData(writer) + pos;
> ```

[^1]: For integer specifiers (d, u, ld, lu, zd, zu, i, x): the 0-conversion flag has effect even when a precision is given.

[^2]: For integer specifiers (d, u, ld, lu, zd, zu, i, x): the 0-conversion flag has effect even when a precision is given.

[^3]: For integer specifiers (d, u, ld, lu, zd, zu, i, x): the 0-conversion flag has effect even when a precision is given.

[^4]: For integer specifiers (d, u, ld, lu, zd, zu, i, x): the 0-conversion flag has effect even when a precision is given.

[^5]: For integer specifiers (d, u, ld, lu, zd, zu, i, x): the 0-conversion flag has effect even when a precision is given.

[^6]: For integer specifiers (d, u, ld, lu, zd, zu, i, x): the 0-conversion flag has effect even when a precision is given.

[^7]: For integer specifiers (d, u, ld, lu, zd, zu, i, x): the 0-conversion flag has effect even when a precision is given.

[^8]: For integer specifiers (d, u, ld, lu, zd, zu, i, x): the 0-conversion flag has effect even when a precision is given.
