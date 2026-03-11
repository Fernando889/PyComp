# Floating-Point Objects {#floatobjects}

::: index
pair: object; floating-point
:::

> This subtype of `PyObject`{.interpreted-text role="c:type"} represents a Python floating-point object.

> This instance of `PyTypeObject`{.interpreted-text role="c:type"} represents the Python floating-point type. This is the same object as `float`{.interpreted-text role="class"} in the Python layer.

> Return true if its argument is a `PyFloatObject`{.interpreted-text role="c:type"} or a subtype of `PyFloatObject`{.interpreted-text role="c:type"}. This function always succeeds.

> Return true if its argument is a `PyFloatObject`{.interpreted-text role="c:type"}, but not a subtype of `PyFloatObject`{.interpreted-text role="c:type"}. This function always succeeds.

> Create a `PyFloatObject`{.interpreted-text role="c:type"} object based on the string value in *str*, or `NULL` on failure.

> Create a `PyFloatObject`{.interpreted-text role="c:type"} object from *v*, or `NULL` on failure.

> Return a C `double`{.interpreted-text role="c:expr"} representation of the contents of *pyfloat*. If *pyfloat* is not a Python floating-point object but has a `~object.__float__`{.interpreted-text role="meth"} method, this method will first be called to convert *pyfloat* into a float. If `!__float__`{.interpreted-text role="meth"} is not defined then it falls back to `~object.__index__`{.interpreted-text role="meth"}. This method returns `-1.0` upon failure, so one should call `PyErr_Occurred`{.interpreted-text role="c:func"} to check for errors.
>
> ::: versionchanged
> 3.8 Use `~object.__index__`{.interpreted-text role="meth"} if available.
> :::

> Return a C `double`{.interpreted-text role="c:expr"} representation of the contents of *pyfloat*, but without error checking.

> Return a structseq instance which contains information about the precision, minimum and maximum values of a float. It\'s a thin wrapper around the header file `float.h`{.interpreted-text role="file"}.

> Return the maximum representable finite float *DBL_MAX* as C `double`{.interpreted-text role="c:expr"}.

> Return the minimum normalized positive float *DBL_MIN* as C `double`{.interpreted-text role="c:expr"}.

> This macro expands to a constant expression of type `double`{.interpreted-text role="c:expr"}, that represents the positive infinity.
>
> It is equivalent to the `!INFINITY`{.interpreted-text role="c:macro"} macro from the C11 standard `<math.h>` header.
>
> ::: deprecated
> 3.15 The macro is `soft deprecated`{.interpreted-text role="term"}.
> :::

> This macro expands to a constant expression of type `double`{.interpreted-text role="c:expr"}, that represents a quiet not-a-number (qNaN) value.
>
> On most platforms, this is equivalent to the `!NAN`{.interpreted-text role="c:macro"} macro from the C11 standard `<math.h>` header.

> Equivalent to `!INFINITY`{.interpreted-text role="c:macro"}.
>
> ::: deprecated
> 3.14 The macro is `soft deprecated`{.interpreted-text role="term"}.
> :::

> The definition (accurate for a `double`{.interpreted-text role="c:expr"} type) of the `math.e`{.interpreted-text role="data"} constant.

> High precision (long double) definition of `~math.e`{.interpreted-text role="data"} constant.
>
> ::: deprecated-removed
> 3.15 3.20
> :::

> The definition (accurate for a `double`{.interpreted-text role="c:expr"} type) of the `math.pi`{.interpreted-text role="data"} constant.

> High precision (long double) definition of `~math.pi`{.interpreted-text role="data"} constant.
>
> ::: deprecated-removed
> 3.15 3.20
> :::

> The definition (accurate for a `double`{.interpreted-text role="c:expr"} type) of the `math.tau`{.interpreted-text role="data"} constant.
>
> ::: versionadded
> 3.6
> :::

> Return `math.nan`{.interpreted-text role="data"} from a function.
>
> On most platforms, this is equivalent to `return PyFloat_FromDouble(NAN)`.

> Return `math.inf`{.interpreted-text role="data"} or `-math.inf <math.inf>`{.interpreted-text role="data"} from a function, depending on the sign of *sign*.
>
> On most platforms, this is equivalent to the following:
>
> ``` c
> return PyFloat_FromDouble(copysign(INFINITY, sign));
> ```

> Return `1` if the given floating-point number *X* is finite, that is, it is normal, subnormal or zero, but not infinite or NaN. Return `0` otherwise.
>
> ::: deprecated
> 3.14 The macro is `soft deprecated`{.interpreted-text role="term"}. Use `!isfinite`{.interpreted-text role="c:macro"} instead.
> :::

> Return `1` if the given floating-point number *X* is positive or negative infinity. Return `0` otherwise.
>
> ::: deprecated
> 3.14 The macro is `soft deprecated`{.interpreted-text role="term"}. Use `!isinf`{.interpreted-text role="c:macro"} instead.
> :::

> Return `1` if the given floating-point number *X* is a not-a-number (NaN) value. Return `0` otherwise.
>
> ::: deprecated
> 3.14 The macro is `soft deprecated`{.interpreted-text role="term"}. Use `!isnan`{.interpreted-text role="c:macro"} instead.
> :::

## Pack and Unpack functions

The pack and unpack functions provide an efficient platform-independent way to store floating-point values as byte strings. The Pack routines produce a bytes string from a C `double`{.interpreted-text role="c:expr"}, and the Unpack routines produce a C `double`{.interpreted-text role="c:expr"} from such a bytes string. The suffix (2, 4 or 8) specifies the number of bytes in the bytes string.

On platforms that appear to use IEEE 754 formats these functions work by copying bits. On other platforms, the 2-byte format is identical to the IEEE 754 binary16 half-precision format, the 4-byte format (32-bit) is identical to the IEEE 754 binary32 single precision format, and the 8-byte format to the IEEE 754 binary64 double precision format, although the packing of INFs and NaNs (if such things exist on the platform) isn\'t handled correctly, and attempting to unpack a bytes string containing an IEEE INF or NaN will raise an exception.

Note that NaNs type may not be preserved on IEEE platforms (signaling NaN become quiet NaN), for example on x86 systems in 32-bit mode.

On non-IEEE platforms with more precision, or larger dynamic range, than IEEE 754 supports, not all values can be packed; on non-IEEE platforms with less precision, or smaller dynamic range, not all values can be unpacked. What happens in such cases is partly accidental (alas).

::: versionadded
3.11
:::

### Pack functions

The pack routines write 2, 4 or 8 bytes, starting at *p*. *le* is an `int`{.interpreted-text role="c:expr"} argument, non-zero if you want the bytes string in little-endian format (exponent last, at `p+1`, `p+3`, or `p+6` `p+7`), zero if you want big-endian format (exponent first, at *p*). The `PY_BIG_ENDIAN`{.interpreted-text role="c:macro"} constant can be used to use the native endian: it is equal to `1` on big endian processor, or `0` on little endian processor.

Return value: `0` if all is OK, `-1` if error (and an exception is set, most likely `OverflowError`{.interpreted-text role="exc"}).

There are two problems on non-IEEE platforms:

- What this does is undefined if *x* is a NaN or infinity.
- `-0.0` and `+0.0` produce the same bytes string.

> Pack a C double as the IEEE 754 binary16 half-precision format.

> Pack a C double as the IEEE 754 binary32 single precision format.

> Pack a C double as the IEEE 754 binary64 double precision format.

### Unpack functions

The unpack routines read 2, 4 or 8 bytes, starting at *p*. *le* is an `int`{.interpreted-text role="c:expr"} argument, non-zero if the bytes string is in little-endian format (exponent last, at `p+1`, `p+3` or `p+6` and `p+7`), zero if big-endian (exponent first, at *p*). The `PY_BIG_ENDIAN`{.interpreted-text role="c:macro"} constant can be used to use the native endian: it is equal to `1` on big endian processor, or `0` on little endian processor.

Return value: The unpacked double. On error, this is `-1.0` and `PyErr_Occurred`{.interpreted-text role="c:func"} is true (and an exception is set, most likely `OverflowError`{.interpreted-text role="exc"}).

Note that on a non-IEEE platform this will refuse to unpack a bytes string that represents a NaN or infinity.

> Unpack the IEEE 754 binary16 half-precision format as a C double.

> Unpack the IEEE 754 binary32 single precision format as a C double.

> Unpack the IEEE 754 binary64 double precision format as a C double.
