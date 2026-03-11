# Integer Objects {#longobjects}

::: index
pair: object; long integer pair: object; integer
:::

All integers are implemented as \"long\" integer objects of arbitrary size.

On error, most `PyLong_As*` APIs return `(return type)-1` which cannot be distinguished from a number. Use `PyErr_Occurred`{.interpreted-text role="c:func"} to disambiguate.

> This subtype of `PyObject`{.interpreted-text role="c:type"} represents a Python integer object.

> This instance of `PyTypeObject`{.interpreted-text role="c:type"} represents the Python integer type. This is the same object as `int`{.interpreted-text role="class"} in the Python layer.

> Return true if its argument is a `PyLongObject`{.interpreted-text role="c:type"} or a subtype of `PyLongObject`{.interpreted-text role="c:type"}. This function always succeeds.

> Return true if its argument is a `PyLongObject`{.interpreted-text role="c:type"}, but not a subtype of `PyLongObject`{.interpreted-text role="c:type"}. This function always succeeds.

> Return a new `PyLongObject`{.interpreted-text role="c:type"} object from *v*, or `NULL` on failure.
>
> ::: impl-detail
> CPython keeps an array of integer objects for all integers between `-5` and `1024`. When you create an int in that range you actually just get back a reference to the existing object.
> :::

> Return a new `PyLongObject`{.interpreted-text role="c:type"} object from a C `unsigned long`{.interpreted-text role="c:expr"}, or `NULL` on failure.

> Return a new `PyLongObject`{.interpreted-text role="c:type"} object from a C `Py_ssize_t`{.interpreted-text role="c:type"}, or `NULL` on failure.

> Return a new `PyLongObject`{.interpreted-text role="c:type"} object from a C `size_t`{.interpreted-text role="c:type"}, or `NULL` on failure.

> Return a new `PyLongObject`{.interpreted-text role="c:type"} object from a C `long long`{.interpreted-text role="c:expr"}, or `NULL` on failure.

> Return a new `PyLongObject`{.interpreted-text role="c:type"} object from a C `unsigned long long`{.interpreted-text role="c:expr"}, or `NULL` on failure.

> Return a new `PyLongObject`{.interpreted-text role="c:type"} object from the integer part of *v*, or `NULL` on failure.

> Return a new `PyLongObject`{.interpreted-text role="c:type"} based on the string value in *str*, which is interpreted according to the radix in *base*, or `NULL` on failure. If *pend* is non-`NULL`, *\*pend* will point to the end of *str* on success or to the first character that could not be processed on error. If *base* is `0`, *str* is interpreted using the `integers`{.interpreted-text role="ref"} definition; in this case, leading zeros in a non-zero decimal number raises a `ValueError`{.interpreted-text role="exc"}. If *base* is not `0`, it must be between `2` and `36`, inclusive. Leading and trailing whitespace and single underscores after a base specifier and between digits are ignored. If there are no digits or *str* is not NULL-terminated following the digits and trailing whitespace, `ValueError`{.interpreted-text role="exc"} will be raised.
>
> ::: seealso
> `PyLong_AsNativeBytes()`{.interpreted-text role="c:func"} and `PyLong_FromNativeBytes()`{.interpreted-text role="c:func"} functions can be used to convert a `PyLongObject`{.interpreted-text role="c:type"} to/from an array of bytes in base `256`.
> :::

> Convert a sequence of Unicode digits in the string *u* to a Python integer value.
>
> ::: versionadded
> 3.3
> :::

> Create a Python integer from the pointer *p*. The pointer value can be retrieved from the resulting value using `PyLong_AsVoidPtr`{.interpreted-text role="c:func"}.

> Create a Python integer from the value contained in the first *n_bytes* of *buffer*, interpreted as a two\'s-complement signed number.
>
> *flags* are as for `PyLong_AsNativeBytes`{.interpreted-text role="c:func"}. Passing `-1` will select the native endian that CPython was compiled with and assume that the most-significant bit is a sign bit. Passing `Py_ASNATIVEBYTES_UNSIGNED_BUFFER` will produce the same result as calling `PyLong_FromUnsignedNativeBytes`{.interpreted-text role="c:func"}. Other flags are ignored.
>
> ::: versionadded
> 3.13
> :::

> Create a Python integer from the value contained in the first *n_bytes* of *buffer*, interpreted as an unsigned number.
>
> *flags* are as for `PyLong_AsNativeBytes`{.interpreted-text role="c:func"}. Passing `-1` will select the native endian that CPython was compiled with and assume that the most-significant bit is not a sign bit. Flags other than endian are ignored.
>
> ::: versionadded
> 3.13
> :::

> Macro for creating a Python integer from a process identifier.
>
> This can be defined as an alias to `PyLong_FromLong`{.interpreted-text role="c:func"} or `PyLong_FromLongLong`{.interpreted-text role="c:func"}, depending on the size of the system\'s PID type.
>
> ::: versionadded
> 3.2
> :::

> ::: index
> single: LONG_MAX (C macro) single: OverflowError (built-in exception)
> :::
>
> Return a C `long`{.interpreted-text role="c:expr"} representation of *obj*. If *obj* is not an instance of `PyLongObject`{.interpreted-text role="c:type"}, first call its `~object.__index__`{.interpreted-text role="meth"} method (if present) to convert it to a `PyLongObject`{.interpreted-text role="c:type"}.
>
> Raise `OverflowError`{.interpreted-text role="exc"} if the value of *obj* is out of range for a `long`{.interpreted-text role="c:expr"}.
>
> Returns `-1` on error. Use `PyErr_Occurred`{.interpreted-text role="c:func"} to disambiguate.
>
> ::: versionchanged
> 3.8 Use `~object.__index__`{.interpreted-text role="meth"} if available.
> :::
>
> ::: versionchanged
> 3.10 This function will no longer use `~object.__int__`{.interpreted-text role="meth"}.
> :::
>
> > A `soft deprecated`{.interpreted-text role="term"} alias. Exactly equivalent to the preferred `PyLong_AsLong`. In particular, it can fail with `OverflowError`{.interpreted-text role="exc"} or another exception.
> >
> > ::: deprecated
> > 3.14 The function is soft deprecated.
> > :::

> Similar to `PyLong_AsLong`{.interpreted-text role="c:func"}, but store the result in a C `int`{.interpreted-text role="c:expr"} instead of a C `long`{.interpreted-text role="c:expr"}.
>
> ::: versionadded
> 3.13
> :::

> Return a C `long`{.interpreted-text role="c:expr"} representation of *obj*. If *obj* is not an instance of `PyLongObject`{.interpreted-text role="c:type"}, first call its `~object.__index__`{.interpreted-text role="meth"} method (if present) to convert it to a `PyLongObject`{.interpreted-text role="c:type"}.
>
> If the value of *obj* is greater than `LONG_MAX`{.interpreted-text role="c:macro"} or less than `LONG_MIN`{.interpreted-text role="c:macro"}, set *\*overflow* to `1` or `-1`, respectively, and return `-1`; otherwise, set *\*overflow* to `0`. If any other exception occurs set *\*overflow* to `0` and return `-1` as usual.
>
> Returns `-1` on error. Use `PyErr_Occurred`{.interpreted-text role="c:func"} to disambiguate.
>
> ::: versionchanged
> 3.8 Use `~object.__index__`{.interpreted-text role="meth"} if available.
> :::
>
> ::: versionchanged
> 3.10 This function will no longer use `~object.__int__`{.interpreted-text role="meth"}.
> :::

> ::: index
> single: OverflowError (built-in exception)
> :::
>
> Return a C `long long`{.interpreted-text role="c:expr"} representation of *obj*. If *obj* is not an instance of `PyLongObject`{.interpreted-text role="c:type"}, first call its `~object.__index__`{.interpreted-text role="meth"} method (if present) to convert it to a `PyLongObject`{.interpreted-text role="c:type"}.
>
> Raise `OverflowError`{.interpreted-text role="exc"} if the value of *obj* is out of range for a `long long`{.interpreted-text role="c:expr"}.
>
> Returns `-1` on error. Use `PyErr_Occurred`{.interpreted-text role="c:func"} to disambiguate.
>
> ::: versionchanged
> 3.8 Use `~object.__index__`{.interpreted-text role="meth"} if available.
> :::
>
> ::: versionchanged
> 3.10 This function will no longer use `~object.__int__`{.interpreted-text role="meth"}.
> :::

> Return a C `long long`{.interpreted-text role="c:expr"} representation of *obj*. If *obj* is not an instance of `PyLongObject`{.interpreted-text role="c:type"}, first call its `~object.__index__`{.interpreted-text role="meth"} method (if present) to convert it to a `PyLongObject`{.interpreted-text role="c:type"}.
>
> If the value of *obj* is greater than `LLONG_MAX`{.interpreted-text role="c:macro"} or less than `LLONG_MIN`{.interpreted-text role="c:macro"}, set *\*overflow* to `1` or `-1`, respectively, and return `-1`; otherwise, set *\*overflow* to `0`. If any other exception occurs set *\*overflow* to `0` and return `-1` as usual.
>
> Returns `-1` on error. Use `PyErr_Occurred`{.interpreted-text role="c:func"} to disambiguate.
>
> ::: versionadded
> 3.2
> :::
>
> ::: versionchanged
> 3.8 Use `~object.__index__`{.interpreted-text role="meth"} if available.
> :::
>
> ::: versionchanged
> 3.10 This function will no longer use `~object.__int__`{.interpreted-text role="meth"}.
> :::

> ::: index
> single: PY_SSIZE_T_MAX (C macro) single: OverflowError (built-in exception)
> :::
>
> Return a C `Py_ssize_t`{.interpreted-text role="c:type"} representation of *pylong*. *pylong* must be an instance of `PyLongObject`{.interpreted-text role="c:type"}.
>
> Raise `OverflowError`{.interpreted-text role="exc"} if the value of *pylong* is out of range for a `Py_ssize_t`{.interpreted-text role="c:type"}.
>
> Returns `-1` on error. Use `PyErr_Occurred`{.interpreted-text role="c:func"} to disambiguate.

> ::: index
> single: ULONG_MAX (C macro) single: OverflowError (built-in exception)
> :::
>
> Return a C `unsigned long`{.interpreted-text role="c:expr"} representation of *pylong*. *pylong* must be an instance of `PyLongObject`{.interpreted-text role="c:type"}.
>
> Raise `OverflowError`{.interpreted-text role="exc"} if the value of *pylong* is out of range for a `unsigned long`{.interpreted-text role="c:expr"}.
>
> Returns `(unsigned long)-1` on error. Use `PyErr_Occurred`{.interpreted-text role="c:func"} to disambiguate.

> ::: index
> single: SIZE_MAX (C macro) single: OverflowError (built-in exception)
> :::
>
> Return a C `size_t`{.interpreted-text role="c:type"} representation of *pylong*. *pylong* must be an instance of `PyLongObject`{.interpreted-text role="c:type"}.
>
> Raise `OverflowError`{.interpreted-text role="exc"} if the value of *pylong* is out of range for a `size_t`{.interpreted-text role="c:type"}.
>
> Returns `(size_t)-1` on error. Use `PyErr_Occurred`{.interpreted-text role="c:func"} to disambiguate.

> ::: index
> single: OverflowError (built-in exception)
> :::
>
> Return a C `unsigned long long`{.interpreted-text role="c:expr"} representation of *pylong*. *pylong* must be an instance of `PyLongObject`{.interpreted-text role="c:type"}.
>
> Raise `OverflowError`{.interpreted-text role="exc"} if the value of *pylong* is out of range for an `unsigned long long`{.interpreted-text role="c:expr"}.
>
> Returns `(unsigned long long)-1` on error. Use `PyErr_Occurred`{.interpreted-text role="c:func"} to disambiguate.
>
> ::: versionchanged
> 3.1 A negative *pylong* now raises `OverflowError`{.interpreted-text role="exc"}, not `TypeError`{.interpreted-text role="exc"}.
> :::

> Return a C `unsigned long`{.interpreted-text role="c:expr"} representation of *obj*. If *obj* is not an instance of `PyLongObject`{.interpreted-text role="c:type"}, first call its `~object.__index__`{.interpreted-text role="meth"} method (if present) to convert it to a `PyLongObject`{.interpreted-text role="c:type"}.
>
> If the value of *obj* is out of range for an `unsigned long`{.interpreted-text role="c:expr"}, return the reduction of that value modulo `ULONG_MAX + 1`.
>
> Returns `(unsigned long)-1` on error. Use `PyErr_Occurred`{.interpreted-text role="c:func"} to disambiguate.
>
> ::: versionchanged
> 3.8 Use `~object.__index__`{.interpreted-text role="meth"} if available.
> :::
>
> ::: versionchanged
> 3.10 This function will no longer use `~object.__int__`{.interpreted-text role="meth"}.
> :::

> Return a C `unsigned long long`{.interpreted-text role="c:expr"} representation of *obj*. If *obj* is not an instance of `PyLongObject`{.interpreted-text role="c:type"}, first call its `~object.__index__`{.interpreted-text role="meth"} method (if present) to convert it to a `PyLongObject`{.interpreted-text role="c:type"}.
>
> If the value of *obj* is out of range for an `unsigned long long`{.interpreted-text role="c:expr"}, return the reduction of that value modulo `ULLONG_MAX + 1`.
>
> Returns `(unsigned long long)-1` on error. Use `PyErr_Occurred`{.interpreted-text role="c:func"} to disambiguate.
>
> ::: versionchanged
> 3.8 Use `~object.__index__`{.interpreted-text role="meth"} if available.
> :::
>
> ::: versionchanged
> 3.10 This function will no longer use `~object.__int__`{.interpreted-text role="meth"}.
> :::

> Return a C `double`{.interpreted-text role="c:expr"} representation of *pylong*. *pylong* must be an instance of `PyLongObject`{.interpreted-text role="c:type"}.
>
> Raise `OverflowError`{.interpreted-text role="exc"} if the value of *pylong* is out of range for a `double`{.interpreted-text role="c:expr"}.
>
> Returns `-1.0` on error. Use `PyErr_Occurred`{.interpreted-text role="c:func"} to disambiguate.

> Convert a Python integer *pylong* to a C `void`{.interpreted-text role="c:expr"} pointer. If *pylong* cannot be converted, an `OverflowError`{.interpreted-text role="exc"} will be raised. This is only assured to produce a usable `void`{.interpreted-text role="c:expr"} pointer for values created with `PyLong_FromVoidPtr`{.interpreted-text role="c:func"}.
>
> Returns `NULL` on error. Use `PyErr_Occurred`{.interpreted-text role="c:func"} to disambiguate.

> Copy the Python integer value *pylong* to a native *buffer* of size *n_bytes*. The *flags* can be set to `-1` to behave similarly to a C cast, or to values documented below to control the behavior.
>
> Returns `-1` with an exception raised on error. This may happen if *pylong* cannot be interpreted as an integer, or if *pylong* was negative and the `Py_ASNATIVEBYTES_REJECT_NEGATIVE` flag was set.
>
> Otherwise, returns the number of bytes required to store the value. If this is equal to or less than *n_bytes*, the entire value was copied. All *n_bytes* of the buffer are written: remaining bytes filled by copies of the sign bit.
>
> If the returned value is greater than *n_bytes*, the value was truncated: as many of the lowest bits of the value as could fit are written, and the higher bits are ignored. This matches the typical behavior of a C-style downcast.
>
> :::: note
> ::: title
> Note
> :::
>
> Overflow is not considered an error. If the returned value is larger than *n_bytes*, most significant bits were discarded.
> ::::
>
> `0` will never be returned.
>
> Values are always copied as two\'s-complement.
>
> Usage example:
>
> ``` c
> int32_t value;
> Py_ssize_t bytes = PyLong_AsNativeBytes(pylong, &value, sizeof(value), -1);
> if (bytes < 0) {
>     // Failed. A Python exception was set with the reason.
>     return NULL;
> }
> else if (bytes <= (Py_ssize_t)sizeof(value)) {
>     // Success!
> }
> else {
>     // Overflow occurred, but 'value' contains the truncated
>     // lowest bits of pylong.
> }
> ```
>
> Passing zero to *n_bytes* will return the size of a buffer that would be large enough to hold the value. This may be larger than technically necessary, but not unreasonably so. If *n_bytes=0*, *buffer* may be `NULL`.
>
> :::: note
> ::: title
> Note
> :::
>
> Passing *n_bytes=0* to this function is not an accurate way to determine the bit length of the value.
> ::::
>
> To get at the entire Python value of an unknown size, the function can be called twice: first to determine the buffer size, then to fill it:
>
> ``` c
> // Ask how much space we need.
> Py_ssize_t expected = PyLong_AsNativeBytes(pylong, NULL, 0, -1);
> if (expected < 0) {
>     // Failed. A Python exception was set with the reason.
>     return NULL;
> }
> assert(expected != 0);  // Impossible per the API definition.
> uint8_t *bignum = malloc(expected);
> if (!bignum) {
>     PyErr_SetString(PyExc_MemoryError, "bignum malloc failed.");
>     return NULL;
> }
> // Safely get the entire value.
> Py_ssize_t bytes = PyLong_AsNativeBytes(pylong, bignum, expected, -1);
> if (bytes < 0) {  // Exception has been set.
>     free(bignum);
>     return NULL;
> }
> else if (bytes > expected) {  // This should not be possible.
>     PyErr_SetString(PyExc_RuntimeError,
>         "Unexpected bignum truncation after a size check.");
>     free(bignum);
>     return NULL;
> }
> // The expected success given the above pre-check.
> // ... use bignum ...
> free(bignum);
> ```
>
> *flags* is either `-1` (`Py_ASNATIVEBYTES_DEFAULTS`) to select defaults that behave most like a C cast, or a combination of the other flags in the table below. Note that `-1` cannot be combined with other flags.
>
> Currently, `-1` corresponds to `Py_ASNATIVEBYTES_NATIVE_ENDIAN | Py_ASNATIVEBYTES_UNSIGNED_BUFFER`.
>
>   Flag   Value
>   ------ -------
>          `-1`
>          `0`
>          `1`
>          `3`
>          `4`
>          `8`
>          `16`
>
> Specifying `Py_ASNATIVEBYTES_NATIVE_ENDIAN` will override any other endian flags. Passing `2` is reserved.
>
> By default, sufficient buffer will be requested to include a sign bit. For example, when converting 128 with *n_bytes=1*, the function will return 2 (or more) in order to store a zero sign bit.
>
> If `Py_ASNATIVEBYTES_UNSIGNED_BUFFER` is specified, a zero sign bit will be omitted from size calculations. This allows, for example, 128 to fit in a single-byte buffer. If the destination buffer is later treated as signed, a positive input value may become negative. Note that the flag does not affect handling of negative values: for those, space for a sign bit is always requested.
>
> Specifying `Py_ASNATIVEBYTES_REJECT_NEGATIVE` causes an exception to be set if *pylong* is negative. Without this flag, negative values will be copied provided there is enough space for at least one sign bit, regardless of whether `Py_ASNATIVEBYTES_UNSIGNED_BUFFER` was specified.
>
> If `Py_ASNATIVEBYTES_ALLOW_INDEX` is specified and a non-integer value is passed, its `~object.__index__`{.interpreted-text role="meth"} method will be called first. This may result in Python code executing and other threads being allowed to run, which could cause changes to other objects or values in use. When *flags* is `-1`, this option is not set, and non-integer values will raise `TypeError`{.interpreted-text role="exc"}.
>
> :::: note
> ::: title
> Note
> :::
>
> With the default *flags* (`-1`, or *UNSIGNED_BUFFER* without *REJECT_NEGATIVE*), multiple Python integers can map to a single value without overflow. For example, both `255` and `-1` fit a single-byte buffer and set all its bits. This matches typical C cast behavior.
> ::::
>
> ::: versionadded
> 3.13
> :::

> Macro for converting a Python integer into a process identifier.
>
> This can be defined as an alias to `PyLong_AsLong`{.interpreted-text role="c:func"}, `PyLong_FromLongLong`{.interpreted-text role="c:func"}, or `PyLong_AsInt`{.interpreted-text role="c:func"}, depending on the size of the system\'s PID type.
>
> ::: versionadded
> 3.2
> :::

> Get the sign of the integer object *obj*.
>
> On success, set *\*sign* to the integer sign (0, -1 or +1 for zero, negative or positive integer, respectively) and return 0.
>
> On failure, return -1 with an exception set. This function always succeeds if *obj* is a `PyLongObject`{.interpreted-text role="c:type"} or its subtype.
>
> ::: versionadded
> 3.14
> :::

> Check if the integer object *obj* is positive (`obj > 0`).
>
> If *obj* is an instance of `PyLongObject`{.interpreted-text role="c:type"} or its subtype, return `1` when it\'s positive and `0` otherwise. Else set an exception and return `-1`.
>
> ::: versionadded
> 3.14
> :::

> Check if the integer object *obj* is negative (`obj < 0`).
>
> If *obj* is an instance of `PyLongObject`{.interpreted-text role="c:type"} or its subtype, return `1` when it\'s negative and `0` otherwise. Else set an exception and return `-1`.
>
> ::: versionadded
> 3.14
> :::

> Check if the integer object *obj* is zero.
>
> If *obj* is an instance of `PyLongObject`{.interpreted-text role="c:type"} or its subtype, return `1` when it\'s zero and `0` otherwise. Else set an exception and return `-1`.
>
> ::: versionadded
> 3.14
> :::

> On success, return a read only `named tuple`{.interpreted-text role="term"}, that holds information about Python\'s internal representation of integers. See `sys.int_info`{.interpreted-text role="data"} for description of individual fields.
>
> On failure, return `NULL` with an exception set.
>
> ::: versionadded
> 3.1
> :::

> Return 1 if *op* is compact, 0 otherwise.
>
> This function makes it possible for performance-critical code to implement a "fast path" for small integers. For compact values use `PyUnstable_Long_CompactValue`{.interpreted-text role="c:func"}; for others fall back to a `PyLong_As* <PyLong_AsSize_t>`{.interpreted-text role="c:func"} function or `PyLong_AsNativeBytes`{.interpreted-text role="c:func"}.
>
> The speedup is expected to be negligible for most users.
>
> Exactly what values are considered compact is an implementation detail and is subject to change.
>
> ::: versionadded
> 3.12
> :::

> If *op* is compact, as determined by `PyUnstable_Long_IsCompact`{.interpreted-text role="c:func"}, return its value.
>
> Otherwise, the return value is undefined.
>
> ::: versionadded
> 3.12
> :::

## Export API

::: versionadded
3.14
:::

> Layout of an array of \"digits\" (\"limbs\" in the GMP terminology), used to represent absolute value for arbitrary precision integers.
>
> Use `PyLong_GetNativeLayout`{.interpreted-text role="c:func"} to get the native layout of Python `int`{.interpreted-text role="class"} objects, used internally for integers with \"big enough\" absolute value.
>
> See also `sys.int_info`{.interpreted-text role="data"} which exposes similar information in Python.
>
> > Bits per digit. For example, a 15 bit digit means that bits 0-14 contain meaningful information.
>
> > Digit size in bytes. For example, a 15 bit digit will require at least 2 bytes.
>
> > Digits order:
> >
> > - `1` for most significant digit first
> > - `-1` for least significant digit first
>
> > Digit endianness:
> >
> > - `1` for most significant byte first (big endian)
> > - `-1` for least significant byte first (little endian)

> Get the native layout of Python `int`{.interpreted-text role="class"} objects.
>
> See the `PyLongLayout`{.interpreted-text role="c:type"} structure.
>
> The function must not be called before Python initialization nor after Python finalization. The returned layout is valid until Python is finalized. The layout is the same for all Python sub-interpreters in a process, and so it can be cached.

> Export of a Python `int`{.interpreted-text role="class"} object.
>
> There are two cases:
>
> - If `digits`{.interpreted-text role="c:member"} is `NULL`, only use the `value`{.interpreted-text role="c:member"} member.
> - If `digits`{.interpreted-text role="c:member"} is not `NULL`, use `negative`{.interpreted-text role="c:member"}, `ndigits`{.interpreted-text role="c:member"} and `digits`{.interpreted-text role="c:member"} members.
>
> > The native integer value of the exported `int`{.interpreted-text role="class"} object. Only valid if `digits`{.interpreted-text role="c:member"} is `NULL`.
>
> > `1` if the number is negative, `0` otherwise. Only valid if `digits`{.interpreted-text role="c:member"} is not `NULL`.
>
> > Number of digits in `digits`{.interpreted-text role="c:member"} array. Only valid if `digits`{.interpreted-text role="c:member"} is not `NULL`.
>
> > Read-only array of unsigned digits. Can be `NULL`.

> Export a Python `int`{.interpreted-text role="class"} object.
>
> *export_long* must point to a `PyLongExport`{.interpreted-text role="c:type"} structure allocated by the caller. It must not be `NULL`.
>
> On success, fill in *\*export_long* and return `0`. On error, set an exception and return `-1`.
>
> `PyLong_FreeExport`{.interpreted-text role="c:func"} must be called when the export is no longer needed.
>
> > ::: impl-detail
> > This function always succeeds if *obj* is a Python `int`{.interpreted-text role="class"} object or a subclass.
> > :::

> Release the export *export_long* created by `PyLong_Export`{.interpreted-text role="c:func"}.
>
> ::: impl-detail
> Calling `PyLong_FreeExport`{.interpreted-text role="c:func"} is optional if *export_long-\>digits* is `NULL`.
> :::

## PyLongWriter API

The `PyLongWriter`{.interpreted-text role="c:type"} API can be used to import an integer.

::: versionadded
3.14
:::

> A Python `int`{.interpreted-text role="class"} writer instance.
>
> The instance must be destroyed by `PyLongWriter_Finish`{.interpreted-text role="c:func"} or `PyLongWriter_Discard`{.interpreted-text role="c:func"}.

> Create a `PyLongWriter`{.interpreted-text role="c:type"}.
>
> On success, allocate *\*digits* and return a writer. On error, set an exception and return `NULL`.
>
> *negative* is `1` if the number is negative, or `0` otherwise.
>
> *ndigits* is the number of digits in the *digits* array. It must be greater than 0.
>
> *digits* must not be NULL.
>
> After a successful call to this function, the caller should fill in the array of digits *digits* and then call `PyLongWriter_Finish`{.interpreted-text role="c:func"} to get a Python `int`{.interpreted-text role="class"}. The layout of *digits* is described by `PyLong_GetNativeLayout`{.interpreted-text role="c:func"}.
>
> Digits must be in the range \[`0`; `(1 << bits_per_digit) - 1`\] (where the `~PyLongLayout.bits_per_digit`{.interpreted-text role="c:type"} is the number of bits per digit). Any unused most significant digits must be set to `0`.
>
> Alternately, call `PyLongWriter_Discard`{.interpreted-text role="c:func"} to destroy the writer instance without creating an `~int`{.interpreted-text role="class"} object.

> Finish a `PyLongWriter`{.interpreted-text role="c:type"} created by `PyLongWriter_Create`{.interpreted-text role="c:func"}.
>
> On success, return a Python `int`{.interpreted-text role="class"} object. On error, set an exception and return `NULL`.
>
> The function takes care of normalizing the digits and converts the object to a compact integer if needed.
>
> The writer instance and the *digits* array are invalid after the call.

> Discard a `PyLongWriter`{.interpreted-text role="c:type"} created by `PyLongWriter_Create`{.interpreted-text role="c:func"}.
>
> If *writer* is `NULL`, no operation is performed.
>
> The writer instance and the *digits* array are invalid after the call.

## Deprecated API

These macros are `soft deprecated`{.interpreted-text role="term"}. They describe parameters of the internal representation of `PyLongObject`{.interpreted-text role="c:type"} instances.

Use `PyLong_GetNativeLayout`{.interpreted-text role="c:func"} instead, along with `PyLong_Export`{.interpreted-text role="c:func"} to read integer data or `PyLongWriter`{.interpreted-text role="c:type"} to write it. These currently use the same layout, but are designed to continue working correctly even if CPython\'s internal integer representation changes.

> This is equivalent to `~PyLongLayout.bits_per_digit`{.interpreted-text role="c:member"} in the output of `PyLong_GetNativeLayout`{.interpreted-text role="c:func"}.

> This is currently equivalent to `1 << PyLong_SHIFT`{.interpreted-text role="c:expr"}.

> This is currently equivalent to `(1 << PyLong_SHIFT) - 1`{.interpreted-text role="c:expr"}
