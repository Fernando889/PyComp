# Parsing arguments and building values {#arg-parsing}

These functions are useful when creating your own extension functions and methods. Additional information and examples are available in `extending-index`{.interpreted-text role="ref"}.

The first three of these functions described, `PyArg_ParseTuple`{.interpreted-text role="c:func"}, `PyArg_ParseTupleAndKeywords`{.interpreted-text role="c:func"}, and `PyArg_Parse`{.interpreted-text role="c:func"}, all use *format strings* which are used to tell the function about the expected arguments. The format strings use the same syntax for each of these functions.

## Parsing arguments

A format string consists of zero or more \"format units.\" A format unit describes one Python object; it is usually a single character or a parenthesized sequence of format units. With a few exceptions, a format unit that is not a parenthesized sequence normally corresponds to a single address argument to these functions. In the following description, the quoted form is the format unit; the entry in (round) parentheses is the Python object type that matches the format unit; and the entry in \[square\] brackets is the type of the C variable(s) whose address should be passed.

### Strings and buffers {#arg-parsing-string-and-buffers}

:::: note
::: title
Note
:::

On Python 3.12 and older, the macro `!PY_SSIZE_T_CLEAN`{.interpreted-text role="c:macro"} must be defined before including `Python.h`{.interpreted-text role="file"} to use all `#` variants of formats (`s#`, `y#`, etc.) explained below. This is not necessary on Python 3.13 and later.
::::

These formats allow accessing an object as a contiguous chunk of memory. You don\'t have to provide raw storage for the returned unicode or bytes area.

Unless otherwise stated, buffers are not NUL-terminated.

There are three ways strings and buffers can be converted to C:

- Formats such as `y*` and `s*` fill a `Py_buffer`{.interpreted-text role="c:type"} structure. This locks the underlying buffer so that the caller can subsequently use the buffer even inside a `Py_BEGIN_ALLOW_THREADS`{.interpreted-text role="c:type"} block without the risk of mutable data being resized or destroyed. As a result, **you have to call** `PyBuffer_Release`{.interpreted-text role="c:func"} after you have finished processing the data (or in any early abort case).

- The `es`, `es#`, `et` and `et#` formats allocate the result buffer. **You have to call** `PyMem_Free`{.interpreted-text role="c:func"} after you have finished processing the data (or in any early abort case).

- ::: {#c-arg-borrowed-buffer}
  Other formats take a `str`{.interpreted-text role="class"} or a read-only `bytes-like object`{.interpreted-text role="term"}, such as `bytes`{.interpreted-text role="class"}, and provide a `const char *` pointer to its buffer. In this case the buffer is \"borrowed\": it is managed by the corresponding Python object, and shares the lifetime of this object. You won\'t have to release any memory yourself.
  :::

  To ensure that the underlying buffer may be safely borrowed, the object\'s `PyBufferProcs.bf_releasebuffer`{.interpreted-text role="c:member"} field must be `NULL`. This disallows common mutable objects such as `bytearray`{.interpreted-text role="class"}, but also some read-only objects such as `memoryview`{.interpreted-text role="class"} of `bytes`{.interpreted-text role="class"}.

  Besides this `bf_releasebuffer` requirement, there is no check to verify whether the input object is immutable (e.g. whether it would honor a request for a writable buffer, or whether another thread can mutate the data).

`s` (`str`{.interpreted-text role="class"}) \[const char \*\]

:   Convert a Unicode object to a C pointer to a character string. A pointer to an existing string is stored in the character pointer variable whose address you pass. The C string is NUL-terminated. The Python string must not contain embedded null code points; if it does, a `ValueError`{.interpreted-text role="exc"} exception is raised. Unicode objects are converted to C strings using `'utf-8'` encoding. If this conversion fails, a `UnicodeError`{.interpreted-text role="exc"} is raised.

    :::: note
    ::: title
    Note
    :::

    This format does not accept `bytes-like objects
    <bytes-like object>`{.interpreted-text role="term"}. If you want to accept filesystem paths and convert them to C character strings, it is preferable to use the `O&` format with `PyUnicode_FSConverter`{.interpreted-text role="c:func"} as *converter*.
    ::::

    ::: versionchanged
    3.5 Previously, `TypeError`{.interpreted-text role="exc"} was raised when embedded null code points were encountered in the Python string.
    :::

`s*` (`str`{.interpreted-text role="class"} or `bytes-like object`{.interpreted-text role="term"}) \[Py_buffer\]

:   This format accepts Unicode objects as well as bytes-like objects. It fills a `Py_buffer`{.interpreted-text role="c:type"} structure provided by the caller. In this case the resulting C string may contain embedded NUL bytes. Unicode objects are converted to C strings using `'utf-8'` encoding.

`s#` (`str`{.interpreted-text role="class"}, read-only `bytes-like object`{.interpreted-text role="term"}) \[const char \*, `Py_ssize_t`{.interpreted-text role="c:type"}\]

:   Like `s*`, except that it provides a `borrowed buffer <c-arg-borrowed-buffer>`{.interpreted-text role="ref"}. The result is stored into two C variables, the first one a pointer to a C string, the second one its length. The string may contain embedded null bytes. Unicode objects are converted to C strings using `'utf-8'` encoding.

`z` (`str`{.interpreted-text role="class"} or `None`) \[const char \*\]

:   Like `s`, but the Python object may also be `None`, in which case the C pointer is set to `NULL`.

`z*` (`str`{.interpreted-text role="class"}, `bytes-like object`{.interpreted-text role="term"} or `None`) \[Py_buffer\]

:   Like `s*`, but the Python object may also be `None`, in which case the `buf` member of the `Py_buffer`{.interpreted-text role="c:type"} structure is set to `NULL`.

`z#` (`str`{.interpreted-text role="class"}, read-only `bytes-like object`{.interpreted-text role="term"} or `None`) \[const char \*, `Py_ssize_t`{.interpreted-text role="c:type"}\]

:   Like `s#`, but the Python object may also be `None`, in which case the C pointer is set to `NULL`.

`y` (read-only `bytes-like object`{.interpreted-text role="term"}) \[const char \*\]

:   This format converts a bytes-like object to a C pointer to a `borrowed <c-arg-borrowed-buffer>`{.interpreted-text role="ref"} character string; it does not accept Unicode objects. The bytes buffer must not contain embedded null bytes; if it does, a `ValueError`{.interpreted-text role="exc"} exception is raised.

    ::: versionchanged
    3.5 Previously, `TypeError`{.interpreted-text role="exc"} was raised when embedded null bytes were encountered in the bytes buffer.
    :::

`y*` (`bytes-like object`{.interpreted-text role="term"}) \[Py_buffer\]

:   This variant on `s*` doesn\'t accept Unicode objects, only bytes-like objects. **This is the recommended way to accept binary data.**

`y#` (read-only `bytes-like object`{.interpreted-text role="term"}) \[const char \*, `Py_ssize_t`{.interpreted-text role="c:type"}\]

:   This variant on `s#` doesn\'t accept Unicode objects, only bytes-like objects.

`S` (`bytes`{.interpreted-text role="class"}) \[PyBytesObject \*\]

:   Requires that the Python object is a `bytes`{.interpreted-text role="class"} object, without attempting any conversion. Raises `TypeError`{.interpreted-text role="exc"} if the object is not a bytes object. The C variable may also be declared as `PyObject*`{.interpreted-text role="c:expr"}.

`Y` (`bytearray`{.interpreted-text role="class"}) \[PyByteArrayObject \*\]

:   Requires that the Python object is a `bytearray`{.interpreted-text role="class"} object, without attempting any conversion. Raises `TypeError`{.interpreted-text role="exc"} if the object is not a `bytearray`{.interpreted-text role="class"} object. The C variable may also be declared as `PyObject*`{.interpreted-text role="c:expr"}.

`U` (`str`{.interpreted-text role="class"}) \[PyObject \*\]

:   Requires that the Python object is a Unicode object, without attempting any conversion. Raises `TypeError`{.interpreted-text role="exc"} if the object is not a Unicode object. The C variable may also be declared as `PyObject*`{.interpreted-text role="c:expr"}.

`w*` (read-write `bytes-like object`{.interpreted-text role="term"}) \[Py_buffer\]

:   This format accepts any object which implements the read-write buffer interface. It fills a `Py_buffer`{.interpreted-text role="c:type"} structure provided by the caller. The buffer may contain embedded null bytes. The caller has to call `PyBuffer_Release`{.interpreted-text role="c:func"} when it is done with the buffer.

`es` (`str`{.interpreted-text role="class"}) \[const char \*encoding, char \*\*buffer\]

:   This variant on `s` is used for encoding Unicode into a character buffer. It only works for encoded data without embedded NUL bytes.

    This format requires two arguments. The first is only used as input, and must be a `const char*`{.interpreted-text role="c:expr"} which points to the name of an encoding as a NUL-terminated string, or `NULL`, in which case `'utf-8'` encoding is used. An exception is raised if the named encoding is not known to Python. The second argument must be a `char**`{.interpreted-text role="c:expr"}; the value of the pointer it references will be set to a buffer with the contents of the argument text. The text will be encoded in the encoding specified by the first argument.

    `PyArg_ParseTuple`{.interpreted-text role="c:func"} will allocate a buffer of the needed size, copy the encoded data into this buffer and adjust *\*buffer* to reference the newly allocated storage. The caller is responsible for calling `PyMem_Free`{.interpreted-text role="c:func"} to free the allocated buffer after use.

`et` (`str`{.interpreted-text role="class"}, `bytes`{.interpreted-text role="class"} or `bytearray`{.interpreted-text role="class"}) \[const char \*encoding, char \*\*buffer\]

:   Same as `es` except that byte string objects are passed through without recoding them. Instead, the implementation assumes that the byte string object uses the encoding passed in as parameter.

`es#` (`str`{.interpreted-text role="class"}) \[const char \*encoding, char \*\*buffer, `Py_ssize_t`{.interpreted-text role="c:type"} \*buffer_length\]

:   This variant on `s#` is used for encoding Unicode into a character buffer. Unlike the `es` format, this variant allows input data which contains NUL characters.

    It requires three arguments. The first is only used as input, and must be a `const char*`{.interpreted-text role="c:expr"} which points to the name of an encoding as a NUL-terminated string, or `NULL`, in which case `'utf-8'` encoding is used. An exception is raised if the named encoding is not known to Python. The second argument must be a `char**`{.interpreted-text role="c:expr"}; the value of the pointer it references will be set to a buffer with the contents of the argument text. The text will be encoded in the encoding specified by the first argument. The third argument must be a pointer to an integer; the referenced integer will be set to the number of bytes in the output buffer.

    There are two modes of operation:

    If *\*buffer* points a `NULL` pointer, the function will allocate a buffer of the needed size, copy the encoded data into this buffer and set *\*buffer* to reference the newly allocated storage. The caller is responsible for calling `PyMem_Free`{.interpreted-text role="c:func"} to free the allocated buffer after usage.

    If *\*buffer* points to a non-`NULL` pointer (an already allocated buffer), `PyArg_ParseTuple`{.interpreted-text role="c:func"} will use this location as the buffer and interpret the initial value of *\*buffer_length* as the buffer size. It will then copy the encoded data into the buffer and NUL-terminate it. If the buffer is not large enough, a `ValueError`{.interpreted-text role="exc"} will be set.

    In both cases, *\*buffer_length* is set to the length of the encoded data without the trailing NUL byte.

`et#` (`str`{.interpreted-text role="class"}, `bytes`{.interpreted-text role="class"} or `bytearray`{.interpreted-text role="class"}) \[const char \*encoding, char \*\*buffer, `Py_ssize_t`{.interpreted-text role="c:type"} \*buffer_length\]

:   Same as `es#` except that byte string objects are passed through without recoding them. Instead, the implementation assumes that the byte string object uses the encoding passed in as parameter.

::: versionchanged
3.12 `u`, `u#`, `Z`, and `Z#` are removed because they used a legacy `Py_UNICODE*` representation.
:::

### Numbers

These formats allow representing Python numbers or single characters as C numbers. Formats that require `int`{.interpreted-text role="class"}, `float`{.interpreted-text role="class"} or `complex`{.interpreted-text role="class"} can also use the corresponding special methods `~object.__index__`{.interpreted-text role="meth"}, `~object.__float__`{.interpreted-text role="meth"} or `~object.__complex__`{.interpreted-text role="meth"} to convert the Python object to the required type.

For signed integer formats, `OverflowError`{.interpreted-text role="exc"} is raised if the value is out of range for the C type. For unsigned integer formats, the most significant bits are silently truncated when the receiving field is too small to receive the value, and `DeprecationWarning`{.interpreted-text role="exc"} is emitted when the value is larger than the maximal value for the C type or less than the minimal value for the corresponding signed integer type of the same size.

`b` (`int`{.interpreted-text role="class"}) \[unsigned char\]

:   Convert a nonnegative Python integer to an unsigned tiny integer, stored in a C `unsigned char`{.interpreted-text role="c:expr"}.

`B` (`int`{.interpreted-text role="class"}) \[unsigned char\]

:   Convert a Python integer to a tiny integer without overflow checking, stored in a C `unsigned char`{.interpreted-text role="c:expr"}. Convert a Python integer to a C `unsigned char`{.interpreted-text role="c:expr"}.

`h` (`int`{.interpreted-text role="class"}) \[short int\]

:   Convert a Python integer to a C `short int`{.interpreted-text role="c:expr"}.

`H` (`int`{.interpreted-text role="class"}) \[unsigned short int\]

:   Convert a Python integer to a C `unsigned short int`{.interpreted-text role="c:expr"}.

`i` (`int`{.interpreted-text role="class"}) \[int\]

:   Convert a Python integer to a plain C `int`{.interpreted-text role="c:expr"}.

`I` (`int`{.interpreted-text role="class"}) \[unsigned int\]

:   Convert a Python integer to a C `unsigned int`{.interpreted-text role="c:expr"}.

`l` (`int`{.interpreted-text role="class"}) \[long int\]

:   Convert a Python integer to a C `long int`{.interpreted-text role="c:expr"}.

`k` (`int`{.interpreted-text role="class"}) \[unsigned long\]

:   Convert a Python integer to a C `unsigned long`{.interpreted-text role="c:expr"}.

    ::: versionchanged
    3.14 Use `~object.__index__`{.interpreted-text role="meth"} if available.
    :::

`L` (`int`{.interpreted-text role="class"}) \[long long\]

:   Convert a Python integer to a C `long long`{.interpreted-text role="c:expr"}.

`K` (`int`{.interpreted-text role="class"}) \[unsigned long long\]

:   Convert a Python integer to a C `unsigned long long`{.interpreted-text role="c:expr"}.

    ::: versionchanged
    3.14 Use `~object.__index__`{.interpreted-text role="meth"} if available.
    :::

`n` (`int`{.interpreted-text role="class"}) \[`Py_ssize_t`{.interpreted-text role="c:type"}\]

:   Convert a Python integer to a C `Py_ssize_t`{.interpreted-text role="c:type"}.

`c` (`bytes`{.interpreted-text role="class"} or `bytearray`{.interpreted-text role="class"} of length 1) \[char\]

:   Convert a Python byte, represented as a `bytes`{.interpreted-text role="class"} or `bytearray`{.interpreted-text role="class"} object of length 1, to a C `char`{.interpreted-text role="c:expr"}.

    ::: versionchanged
    3.3 Allow `bytearray`{.interpreted-text role="class"} objects.
    :::

`C` (`str`{.interpreted-text role="class"} of length 1) \[int\]

:   Convert a Python character, represented as a `str`{.interpreted-text role="class"} object of length 1, to a C `int`{.interpreted-text role="c:expr"}.

`f` (`float`{.interpreted-text role="class"}) \[float\]

:   Convert a Python floating-point number to a C `float`{.interpreted-text role="c:expr"}.

`d` (`float`{.interpreted-text role="class"}) \[double\]

:   Convert a Python floating-point number to a C `double`{.interpreted-text role="c:expr"}.

`D` (`complex`{.interpreted-text role="class"}) \[Py_complex\]

:   Convert a Python complex number to a C `Py_complex`{.interpreted-text role="c:type"} structure.

::: deprecated
3.15

For unsigned integer formats `B`, `H`, `I`, `k` and `K`, `DeprecationWarning`{.interpreted-text role="exc"} is emitted when the value is larger than the maximal value for the C type or less than the minimal value for the corresponding signed integer type of the same size.
:::

### Other objects

`O` (object) \[PyObject \*\]

:   Store a Python object (without any conversion) in a C object pointer. The C program thus receives the actual object that was passed. A new `strong reference`{.interpreted-text role="term"} to the object is not created (i.e. its reference count is not increased). The pointer stored is not `NULL`.

`O!` (object) \[*typeobject*, PyObject \*\]

:   Store a Python object in a C object pointer. This is similar to `O`, but takes two C arguments: the first is the address of a Python type object, the second is the address of the C variable (of type `PyObject*`{.interpreted-text role="c:expr"}) into which the object pointer is stored. If the Python object does not have the required type, `TypeError`{.interpreted-text role="exc"} is raised.

::: {#o_ampersand}

`O&` (object) \[*converter*, *address*\]

:   Convert a Python object to a C variable through a *converter* function. This takes two arguments: the first is a function, the second is the address of a C variable (of arbitrary type), converted to `void *`{.interpreted-text role="c:expr"}. The *converter* function in turn is called as follows:

    ``` c
    status = converter(object, address);
    ```

    where *object* is the Python object to be converted and *address* is the `void*`{.interpreted-text role="c:expr"} argument that was passed to the `PyArg_Parse*` function. The returned *status* should be `1` for a successful conversion and `0` if the conversion has failed. When the conversion fails, the *converter* function should raise an exception and leave the content of *address* unmodified.

    If the *converter* returns `!Py_CLEANUP_SUPPORTED`{.interpreted-text role="c:macro"}, it may get called a second time if the argument parsing eventually fails, giving the converter a chance to release any memory that it had already allocated. In this second call, the *object* parameter will be `NULL`; *address* will have the same value as in the original call.

    Examples of converters: `PyUnicode_FSConverter`{.interpreted-text role="c:func"} and `PyUnicode_FSDecoder`{.interpreted-text role="c:func"}.

    ::: versionchanged
    3.1 `!Py_CLEANUP_SUPPORTED`{.interpreted-text role="c:macro"} was added.
    :::

`p` (`bool`{.interpreted-text role="class"}) \[int\]

:   Tests the value passed in for truth (a boolean **p**redicate) and converts the result to its equivalent C true/false integer value. Sets the int to `1` if the expression was true and `0` if it was false. This accepts any valid Python value. See `truth`{.interpreted-text role="ref"} for more information about how Python tests values for truth.

    ::: versionadded
    3.3
    :::

`(items)` (sequence) \[*matching-items*\]

:   The object must be a Python sequence (except `str`{.interpreted-text role="class"}, `bytes`{.interpreted-text role="class"} or `bytearray`{.interpreted-text role="class"}) whose length is the number of format units in *items*. The C arguments must correspond to the individual format units in *items*. Format units for sequences may be nested.

    If *items* contains format units which store a `borrowed buffer
    <c-arg-borrowed-buffer>`{.interpreted-text role="ref"} (`s`, `s#`, `z`, `z#`, `y`, or `y#`) or a `borrowed reference`{.interpreted-text role="term"} (`S`, `Y`, `U`, `O`, or `O!`), the object must be a Python tuple. The *converter* for the `O&` format unit in *items* must not store a borrowed buffer or a borrowed reference.

    ::: versionchanged
    3.14 `str`{.interpreted-text role="class"} and `bytearray`{.interpreted-text role="class"} objects no longer accepted as a sequence.
    :::

    ::: deprecated
    3.14 Non-tuple sequences are deprecated if *items* contains format units which store a borrowed buffer or a borrowed reference.
    :::
:::

A few other characters have a meaning in a format string. These may not occur inside nested parentheses. They are:

`|`

:   Indicates that the remaining arguments in the Python argument list are optional. The C variables corresponding to optional arguments should be initialized to their default value \-\-- when an optional argument is not specified, `PyArg_ParseTuple`{.interpreted-text role="c:func"} does not touch the contents of the corresponding C variable(s).

`$`

:   `PyArg_ParseTupleAndKeywords`{.interpreted-text role="c:func"} only: Indicates that the remaining arguments in the Python argument list are keyword-only. Currently, all keyword-only arguments must also be optional arguments, so `|` must always be specified before `$` in the format string.

    ::: versionadded
    3.3
    :::

`:`

:   The list of format units ends here; the string after the colon is used as the function name in error messages (the \"associated value\" of the exception that `PyArg_ParseTuple`{.interpreted-text role="c:func"} raises).

`;`

:   The list of format units ends here; the string after the semicolon is used as the error message *instead* of the default error message. `:` and `;` mutually exclude each other.

Note that any Python object references which are provided to the caller are *borrowed* references; do not release them (i.e. do not decrement their reference count)!

Additional arguments passed to these functions must be addresses of variables whose type is determined by the format string; these are used to store values from the input tuple. There are a few cases, as described in the list of format units above, where these parameters are used as input values; they should match what is specified for the corresponding format unit in that case.

For the conversion to succeed, the *arg* object must match the format and the format must be exhausted. On success, the `PyArg_Parse*` functions return true, otherwise they return false and raise an appropriate exception. When the `PyArg_Parse*` functions fail due to conversion failure in one of the format units, the variables at the addresses corresponding to that and the following format units are left untouched.

### API Functions

> Parse the parameters of a function that takes only positional parameters into local variables. Returns true on success; on failure, it returns false and raises the appropriate exception.

> Identical to `PyArg_ParseTuple`{.interpreted-text role="c:func"}, except that it accepts a va_list rather than a variable number of arguments.

> Parse the parameters of a function that takes both positional and keyword parameters into local variables. The *keywords* argument is a `NULL`-terminated array of keyword parameter names specified as null-terminated ASCII or UTF-8 encoded C strings. Empty names denote `positional-only parameters <positional-only_parameter>`{.interpreted-text role="ref"}. Returns true on success; on failure, it returns false and raises the appropriate exception.
>
> :::: note
> ::: title
> Note
> :::
>
> The *keywords* parameter declaration is `char * const *`{.interpreted-text role="c:expr"} in C and `const char * const *`{.interpreted-text role="c:expr"} in C++. This can be overridden with the `PY_CXX_CONST`{.interpreted-text role="c:macro"} macro.
> ::::
>
> ::: versionchanged
> 3.6 Added support for `positional-only parameters
> <positional-only_parameter>`{.interpreted-text role="ref"}.
> :::
>
> ::: versionchanged
> 3.13 The *keywords* parameter has now type `char * const *`{.interpreted-text role="c:expr"} in C and `const char * const *`{.interpreted-text role="c:expr"} in C++, instead of `char **`{.interpreted-text role="c:expr"}. Added support for non-ASCII keyword parameter names.
> :::

> Identical to `PyArg_ParseTupleAndKeywords`{.interpreted-text role="c:func"}, except that it accepts a va_list rather than a variable number of arguments.

> Ensure that the keys in the keywords argument dictionary are strings. This is only needed if `PyArg_ParseTupleAndKeywords`{.interpreted-text role="c:func"} is not used, since the latter already does this check.
>
> ::: versionadded
> 3.2
> :::

> Parse the parameter of a function that takes a single positional parameter into a local variable. Returns true on success; on failure, it returns false and raises the appropriate exception.
>
> Example:
>
> ``` c
> // Function using METH_O calling convention
> static PyObject*
> my_function(PyObject *module, PyObject *arg)
> {
>     int value;
>     if (!PyArg_Parse(arg, "i:my_function", &value)) {
>         return NULL;
>     }
>     // ... use value ...
> }
> ```

> A simpler form of parameter retrieval which does not use a format string to specify the types of the arguments. Functions which use this method to retrieve their parameters should be declared as `METH_VARARGS`{.interpreted-text role="c:macro"} in function or method tables. The tuple containing the actual parameters should be passed as *args*; it must actually be a tuple. The length of the tuple must be at least *min* and no more than *max*; *min* and *max* may be equal. Additional arguments must be passed to the function, each of which should be a pointer to a `PyObject*`{.interpreted-text role="c:expr"} variable; these will be filled in with the values from *args*; they will contain `borrowed references <borrowed reference>`{.interpreted-text role="term"}. The variables which correspond to optional parameters not given by *args* will not be filled in; these should be initialized by the caller. This function returns true on success and false if *args* is not a tuple or contains the wrong number of elements; an exception will be set if there was a failure.
>
> This is an example of the use of this function, taken from the sources for the `!_weakref`{.interpreted-text role="mod"} helper module for weak references:
>
> ``` c
> static PyObject *
> weakref_ref(PyObject *self, PyObject *args)
> {
>     PyObject *object;
>     PyObject *callback = NULL;
>     PyObject *result = NULL;
>
>     if (PyArg_UnpackTuple(args, "ref", 1, 2, &object, &callback)) {
>         result = PyWeakref_NewRef(object, callback);
>     }
>     return result;
> }
> ```
>
> The call to `PyArg_UnpackTuple`{.interpreted-text role="c:func"} in this example is entirely equivalent to this call to `PyArg_ParseTuple`{.interpreted-text role="c:func"}:
>
> ``` c
> PyArg_ParseTuple(args, "O|O:ref", &object, &callback)
> ```

> The value to be inserted, if any, before `char * const *`{.interpreted-text role="c:expr"} in the *keywords* parameter declaration of `PyArg_ParseTupleAndKeywords`{.interpreted-text role="c:func"} and `PyArg_VaParseTupleAndKeywords`{.interpreted-text role="c:func"}. Default empty for C and `const` for C++ (`const char * const *`{.interpreted-text role="c:expr"}). To override, define it to the desired value before including `Python.h`{.interpreted-text role="file"}.
>
> ::: versionadded
> 3.13
> :::

## Building values

> Create a new value based on a format string similar to those accepted by the `PyArg_Parse*` family of functions and a sequence of values. Returns the value or `NULL` in the case of an error; an exception will be raised if `NULL` is returned.
>
> `Py_BuildValue`{.interpreted-text role="c:func"} does not always build a tuple. It builds a tuple only if its format string contains two or more format units. If the format string is empty, it returns `None`; if it contains exactly one format unit, it returns whatever object is described by that format unit. To force it to return a tuple of size 0 or one, parenthesize the format string.
>
> When memory buffers are passed as parameters to supply data to build objects, as for the `s` and `s#` formats, the required data is copied. Buffers provided by the caller are never referenced by the objects created by `Py_BuildValue`{.interpreted-text role="c:func"}. In other words, if your code invokes `malloc`{.interpreted-text role="c:func"} and passes the allocated memory to `Py_BuildValue`{.interpreted-text role="c:func"}, your code is responsible for calling `free`{.interpreted-text role="c:func"} for that memory once `Py_BuildValue`{.interpreted-text role="c:func"} returns.
>
> In the following description, the quoted form is the format unit; the entry in (round) parentheses is the Python object type that the format unit will return; and the entry in \[square\] brackets is the type of the C value(s) to be passed.
>
> The characters space, tab, colon and comma are ignored in format strings (but not within format units such as `s#`). This can be used to make long format strings a tad more readable.
>
> `s` (`str`{.interpreted-text role="class"} or `None`) \[const char \*\]
>
> :   Convert a null-terminated C string to a Python `str`{.interpreted-text role="class"} object using `'utf-8'` encoding. If the C string pointer is `NULL`, `None` is used.
>
> `s#` (`str`{.interpreted-text role="class"} or `None`) \[const char \*, `Py_ssize_t`{.interpreted-text role="c:type"}\]
>
> :   Convert a C string and its length to a Python `str`{.interpreted-text role="class"} object using `'utf-8'` encoding. If the C string pointer is `NULL`, the length is ignored and `None` is returned.
>
> `y` (`bytes`{.interpreted-text role="class"}) \[const char \*\]
>
> :   This converts a C string to a Python `bytes`{.interpreted-text role="class"} object. If the C string pointer is `NULL`, `None` is returned.
>
> `y#` (`bytes`{.interpreted-text role="class"}) \[const char \*, `Py_ssize_t`{.interpreted-text role="c:type"}\]
>
> :   This converts a C string and its lengths to a Python object. If the C string pointer is `NULL`, `None` is returned.
>
> `z` (`str`{.interpreted-text role="class"} or `None`) \[const char \*\]
>
> :   Same as `s`.
>
> `z#` (`str`{.interpreted-text role="class"} or `None`) \[const char \*, `Py_ssize_t`{.interpreted-text role="c:type"}\]
>
> :   Same as `s#`.
>
> `u` (`str`{.interpreted-text role="class"}) \[const wchar_t \*\]
>
> :   Convert a null-terminated `wchar_t`{.interpreted-text role="c:type"} buffer of Unicode (UTF-16 or UCS-4) data to a Python Unicode object. If the Unicode buffer pointer is `NULL`, `None` is returned.
>
> `u#` (`str`{.interpreted-text role="class"}) \[const wchar_t \*, `Py_ssize_t`{.interpreted-text role="c:type"}\]
>
> :   Convert a Unicode (UTF-16 or UCS-4) data buffer and its length to a Python Unicode object. If the Unicode buffer pointer is `NULL`, the length is ignored and `None` is returned.
>
> `U` (`str`{.interpreted-text role="class"} or `None`) \[const char \*\]
>
> :   Same as `s`.
>
> `U#` (`str`{.interpreted-text role="class"} or `None`) \[const char \*, `Py_ssize_t`{.interpreted-text role="c:type"}\]
>
> :   Same as `s#`.
>
> `i` (`int`{.interpreted-text role="class"}) \[int\]
>
> :   Convert a plain C `int`{.interpreted-text role="c:expr"} to a Python integer object.
>
> `b` (`int`{.interpreted-text role="class"}) \[char\]
>
> :   Convert a plain C `char`{.interpreted-text role="c:expr"} to a Python integer object.
>
> `h` (`int`{.interpreted-text role="class"}) \[short int\]
>
> :   Convert a plain C `short int`{.interpreted-text role="c:expr"} to a Python integer object.
>
> `l` (`int`{.interpreted-text role="class"}) \[long int\]
>
> :   Convert a C `long int`{.interpreted-text role="c:expr"} to a Python integer object.
>
> `B` (`int`{.interpreted-text role="class"}) \[unsigned char\]
>
> :   Convert a C `unsigned char`{.interpreted-text role="c:expr"} to a Python integer object.
>
> `H` (`int`{.interpreted-text role="class"}) \[unsigned short int\]
>
> :   Convert a C `unsigned short int`{.interpreted-text role="c:expr"} to a Python integer object.
>
> `I` (`int`{.interpreted-text role="class"}) \[unsigned int\]
>
> :   Convert a C `unsigned int`{.interpreted-text role="c:expr"} to a Python integer object.
>
> `k` (`int`{.interpreted-text role="class"}) \[unsigned long\]
>
> :   Convert a C `unsigned long`{.interpreted-text role="c:expr"} to a Python integer object.
>
> `L` (`int`{.interpreted-text role="class"}) \[long long\]
>
> :   Convert a C `long long`{.interpreted-text role="c:expr"} to a Python integer object.
>
> ::: {#capi-py-buildvalue-format-K}
>
> `K` (`int`{.interpreted-text role="class"}) \[unsigned long long\]
>
> :   Convert a C `unsigned long long`{.interpreted-text role="c:expr"} to a Python integer object.
>
> `n` (`int`{.interpreted-text role="class"}) \[`Py_ssize_t`{.interpreted-text role="c:type"}\]
>
> :   Convert a C `Py_ssize_t`{.interpreted-text role="c:type"} to a Python integer.
>
> `p` (`bool`{.interpreted-text role="class"}) \[int\]
>
> :   Convert a C `int`{.interpreted-text role="c:expr"} to a Python `bool`{.interpreted-text role="class"} object.
>
>     Be aware that this format requires an `int` argument. Unlike most other contexts in C, variadic arguments are not coerced to a suitable type automatically. You can convert another type (for example, a pointer or a float) to a suitable `int` value using `(x) ? 1 : 0` or `!!x`.
>
>     ::: versionadded
>     3.14
>     :::
>
> `c` (`bytes`{.interpreted-text role="class"} of length 1) \[char\]
>
> :   Convert a C `int`{.interpreted-text role="c:expr"} representing a byte to a Python `bytes`{.interpreted-text role="class"} object of length 1.
>
> `C` (`str`{.interpreted-text role="class"} of length 1) \[int\]
>
> :   Convert a C `int`{.interpreted-text role="c:expr"} representing a character to Python `str`{.interpreted-text role="class"} object of length 1.
>
> `d` (`float`{.interpreted-text role="class"}) \[double\]
>
> :   Convert a C `double`{.interpreted-text role="c:expr"} to a Python floating-point number.
>
> `f` (`float`{.interpreted-text role="class"}) \[float\]
>
> :   Convert a C `float`{.interpreted-text role="c:expr"} to a Python floating-point number.
>
> `D` (`complex`{.interpreted-text role="class"}) \[Py_complex \*\]
>
> :   Convert a C `Py_complex`{.interpreted-text role="c:type"} structure to a Python complex number.
>
> `O` (object) \[PyObject \*\]
>
> :   Pass a Python object untouched but create a new `strong reference`{.interpreted-text role="term"} to it (i.e. its reference count is incremented by one). If the object passed in is a `NULL` pointer, it is assumed that this was caused because the call producing the argument found an error and set an exception. Therefore, `Py_BuildValue`{.interpreted-text role="c:func"} will return `NULL` but won\'t raise an exception. If no exception has been raised yet, `SystemError`{.interpreted-text role="exc"} is set.
>
> `S` (object) \[PyObject \*\]
>
> :   Same as `O`.
>
> `N` (object) \[PyObject \*\]
>
> :   Same as `O`, except it doesn\'t create a new `strong reference`{.interpreted-text role="term"}. Useful when the object is created by a call to an object constructor in the argument list.
>
> `O&` (object) \[*converter*, *anything*\]
>
> :   Convert *anything* to a Python object through a *converter* function. The function is called with *anything* (which should be compatible with `void*`{.interpreted-text role="c:expr"}) as its argument and should return a \"new\" Python object, or `NULL` if an error occurred.
>
> `(items)` (`tuple`{.interpreted-text role="class"}) \[*matching-items*\]
>
> :   Convert a sequence of C values to a Python tuple with the same number of items.
>
> `[items]` (`list`{.interpreted-text role="class"}) \[*matching-items*\]
>
> :   Convert a sequence of C values to a Python list with the same number of items.
>
> `{items}` (`dict`{.interpreted-text role="class"}) \[*matching-items*\]
>
> :   Convert a sequence of C values to a Python dictionary. Each pair of consecutive C values adds one item to the dictionary, serving as key and value, respectively.
> :::
>
> If there is an error in the format string, the `SystemError`{.interpreted-text role="exc"} exception is set and `NULL` returned.

> Identical to `Py_BuildValue`{.interpreted-text role="c:func"}, except that it accepts a va_list rather than a variable number of arguments.
