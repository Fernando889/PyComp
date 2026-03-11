# `!array`{.interpreted-text role="mod"} \-\-- Efficient arrays of numeric values

::: {.module synopsis="Space efficient arrays of uniformly typed numeric values."}
array
:::

::: index
single: arrays
:::

------------------------------------------------------------------------

This module defines an object type which can compactly represent an array of basic values: characters, integers, floating-point numbers. Arrays are mutable `sequence`{.interpreted-text role="term"} types and behave very much like lists, except that the type of objects stored in them is constrained. The type is specified at object creation time by using a `type code`{.interpreted-text role="dfn"}, which is a single character. The following type codes are defined:

  ------------------------------------------------------------------------------------
  Type code   C Type               Python Type         Minimum size in bytes   Notes
  ----------- -------------------- ------------------- ----------------------- -------
  `'b'`       signed char          int                 1                       

  `'B'`       unsigned char        int                 1                       

  `'u'`       wchar_t              Unicode character   2                       \(1\)

  `'w'`       Py_UCS4              Unicode character   4                       \(2\)

  `'h'`       signed short         int                 2                       

  `'H'`       unsigned short       int                 2                       

  `'i'`       signed int           int                 2                       

  `'I'`       unsigned int         int                 2                       

  `'l'`       signed long          int                 4                       

  `'L'`       unsigned long        int                 4                       

  `'q'`       signed long long     int                 8                       

  `'Q'`       unsigned long long   int                 8                       

  `'f'`       float                float               4                       

  `'d'`       double               float               8                       
  ------------------------------------------------------------------------------------

Notes:

\(1\)

:   It can be 16 bits or 32 bits depending on the platform.

    ::: versionchanged
    3.9 `array('u')` now uses `wchar_t`{.interpreted-text role="c:type"} as C type instead of deprecated `Py_UNICODE`. This change doesn\'t affect its behavior because `Py_UNICODE` is alias of `wchar_t`{.interpreted-text role="c:type"} since Python 3.3.
    :::

    ::: deprecated-removed
    3.3 3.16 Please migrate to `'w'` typecode.
    :::

\(2\)

:   ::: versionadded
    3.13
    :::

The actual representation of values is determined by the machine architecture (strictly speaking, by the C implementation). The actual size can be accessed through the `array.itemsize`{.interpreted-text role="attr"} attribute.

The module defines the following item:

::: data
typecodes

A string with all available type codes.
:::

The module defines the following type:

::::::::::::::::::::::::::::::: {.array(typecode[, .initializer])}
A new array whose items are restricted by *typecode*, and initialized from the optional *initializer* value, which must be a `bytes`{.interpreted-text role="class"} or `bytearray`{.interpreted-text role="class"} object, a Unicode string, or iterable over elements of the appropriate type.

If given a `bytes`{.interpreted-text role="class"} or `bytearray`{.interpreted-text role="class"} object, the initializer is passed to the new array\'s `frombytes`{.interpreted-text role="meth"} method; if given a Unicode string, the initializer is passed to the `fromunicode`{.interpreted-text role="meth"} method; otherwise, the initializer\'s iterator is passed to the `extend`{.interpreted-text role="meth"} method to add initial items to the array.

Array objects support the ordinary `mutable <typesseq-mutable>`{.interpreted-text role="ref"} `sequence`{.interpreted-text role="term"} operations of indexing, slicing, concatenation, and multiplication. When using slice assignment, the assigned value must be an array object with the same type code; in all other cases, `TypeError`{.interpreted-text role="exc"} is raised. Array objects also implement the buffer interface, and may be used wherever `bytes-like objects <bytes-like object>`{.interpreted-text role="term"} are supported.

::: audit-event
array.\_\_new\_\_ typecode,initializer array.array
:::

::: attribute
typecode

The typecode character used to create the array.
:::

::: attribute
itemsize

The length in bytes of one array item in the internal representation.
:::

::: method
append(x)

Append a new item with value *x* to the end of the array.
:::

::::: method
buffer_info()

Return a tuple `(address, length)` giving the current memory address and the length in elements of the buffer used to hold array\'s contents. The size of the memory buffer in bytes can be computed as `array.buffer_info()[1] * array.itemsize`. This is occasionally useful when working with low-level (and inherently unsafe) I/O interfaces that require memory addresses, such as certain `!ioctl`{.interpreted-text role="c:func"} operations. The returned numbers are valid as long as the array exists and no length-changing operations are applied to it.

:::: note
::: title
Note
:::

When using array objects from code written in C or C++ (the only way to effectively make use of this information), it makes more sense to use the buffer interface supported by array objects. This method is maintained for backward compatibility and should be avoided in new code. The buffer interface is documented in `bufferobjects`{.interpreted-text role="ref"}.
::::
:::::

::: method
byteswap()

\"Byteswap\" all items of the array. This is only supported for values which are 1, 2, 4, or 8 bytes in size; for other types of values, `RuntimeError`{.interpreted-text role="exc"} is raised. It is useful when reading data from a file written on a machine with a different byte order.
:::

::: method
count(x)

Return the number of occurrences of *x* in the array.
:::

::: method
extend(iterable)

Append items from *iterable* to the end of the array. If *iterable* is another array, it must have *exactly* the same type code; if not, `TypeError`{.interpreted-text role="exc"} will be raised. If *iterable* is not an array, it must be iterable and its elements must be the right type to be appended to the array.
:::

:::: method
frombytes(buffer)

Appends items from the `bytes-like object`{.interpreted-text role="term"}, interpreting its content as an array of machine values (as if it had been read from a file using the `fromfile`{.interpreted-text role="meth"} method).

::: versionadded
3.2 `!fromstring`{.interpreted-text role="meth"} is renamed to `frombytes`{.interpreted-text role="meth"} for clarity.
:::
::::

::: method
fromfile(f, n)

Read *n* items (as machine values) from the `file object`{.interpreted-text role="term"} *f* and append them to the end of the array. If less than *n* items are available, `EOFError`{.interpreted-text role="exc"} is raised, but the items that were available are still inserted into the array.
:::

::: method
fromlist(list)

Append items from the list. This is equivalent to `for x in list: a.append(x)` except that if there is a type error, the array is unchanged.
:::

::: method
fromunicode(s)

Extends this array with data from the given Unicode string. The array must have type code `'u'` or `'w'`; otherwise a `ValueError`{.interpreted-text role="exc"} is raised. Use `array.frombytes(unicodestring.encode(enc))` to append Unicode data to an array of some other type.
:::

:::: method
index(x\[, start\[, stop\]\])

Return the smallest *i* such that *i* is the index of the first occurrence of *x* in the array. The optional arguments *start* and *stop* can be specified to search for *x* within a subsection of the array. Raise `ValueError`{.interpreted-text role="exc"} if *x* is not found.

::: versionchanged
3.10 Added optional *start* and *stop* parameters.
:::
::::

::: method
insert(i, x)

Insert a new item with value *x* in the array before position *i*. Negative values are treated as being relative to the end of the array.
:::

::: method
pop(\[i\])

Removes the item with the index *i* from the array and returns it. The optional argument defaults to `-1`, so that by default the last item is removed and returned.
:::

::: method
remove(x)

Remove the first occurrence of *x* from the array.
:::

:::: method
clear()

Remove all elements from the array.

::: versionadded
3.13
:::
::::

::: method
reverse()

Reverse the order of the items in the array.
:::

:::: method
tobytes()

Convert the array to an array of machine values and return the bytes representation (the same sequence of bytes that would be written to a file by the `tofile`{.interpreted-text role="meth"} method.)

::: versionadded
3.2 `!tostring`{.interpreted-text role="meth"} is renamed to `tobytes`{.interpreted-text role="meth"} for clarity.
:::
::::

::: method
tofile(f)

Write all items (as machine values) to the `file object`{.interpreted-text role="term"} *f*.
:::

::: method
tolist()

Convert the array to an ordinary list with the same items.
:::

::: method
tounicode()

Convert the array to a Unicode string. The array must have a type `'u'` or `'w'`; otherwise a `ValueError`{.interpreted-text role="exc"} is raised. Use `array.tobytes().decode(enc)` to obtain a Unicode string from an array of some other type.
:::
:::::::::::::::::::::::::::::::

The string representation of array objects has the form `array(typecode, initializer)`. The *initializer* is omitted if the array is empty, otherwise it is a Unicode string if the *typecode* is `'u'` or `'w'`, otherwise it is a list of numbers. The string representation is guaranteed to be able to be converted back to an array with the same type and value using `eval`{.interpreted-text role="func"}, so long as the `~array.array`{.interpreted-text role="class"} class has been imported using `from array import array`. Variables `inf` and `nan` must also be defined if it contains corresponding floating-point values. Examples:

    array('l')
    array('w', 'hello \u2641')
    array('l', [1, 2, 3, 4, 5])
    array('d', [1.0, 2.0, 3.14, -inf, nan])

::: seealso

Module `struct`{.interpreted-text role="mod"}

:   Packing and unpacking of heterogeneous binary data.

[NumPy](https://numpy.org/)

:   The NumPy package defines another array type.
:::
