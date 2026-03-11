# String conversion and formatting {#string-conversion}

Functions for number conversion and formatted string output.

> Output not more than *size* bytes to *str* according to the format string *format* and the extra arguments. See the Unix man page `snprintf(3)`{.interpreted-text role="manpage"}.

> Output not more than *size* bytes to *str* according to the format string *format* and the variable argument list *va*. Unix man page `vsnprintf(3)`{.interpreted-text role="manpage"}.

`PyOS_snprintf`{.interpreted-text role="c:func"} and `PyOS_vsnprintf`{.interpreted-text role="c:func"} wrap the Standard C library functions `snprintf`{.interpreted-text role="c:func"} and `vsnprintf`{.interpreted-text role="c:func"}. Their purpose is to guarantee consistent behavior in corner cases, which the Standard C functions do not.

The wrappers ensure that `str[size-1]` is always `'\0'` upon return. They never write more than *size* bytes (including the trailing `'\0'`) into str. Both functions require that `str != NULL`, `size > 0`, `format != NULL` and `size < INT_MAX`. Note that this means there is no equivalent to the C99 `n = snprintf(NULL, 0, ...)` which would determine the necessary buffer size.

The return value (*rv*) for these functions should be interpreted as follows:

- When `0 <= rv < size`, the output conversion was successful and *rv* characters were written to *str* (excluding the trailing `'\0'` byte at `str[rv]`).
- When `rv >= size`, the output conversion was truncated and a buffer with `rv + 1` bytes would have been needed to succeed. `str[size-1]` is `'\0'` in this case.
- When `rv < 0`, the output conversion failed and `str[size-1]` is `'\0'` in this case too, but the rest of *str* is undefined. The exact cause of the error depends on the underlying platform.

The following functions provide locale-independent string to number conversions.

> Convert the initial part of the string in `str` to an `unsigned
> long`{.interpreted-text role="c:expr"} value according to the given `base`, which must be between `2` and `36` inclusive, or be the special value `0`.
>
> Leading white space and case of characters are ignored. If `base` is zero it looks for a leading `0b`, `0o` or `0x` to tell which base. If these are absent it defaults to `10`. Base must be 0 or between 2 and 36 (inclusive). If `ptr` is non-`NULL` it will contain a pointer to the end of the scan.
>
> If the converted value falls out of range of corresponding return type, range error occurs (`errno`{.interpreted-text role="c:data"} is set to `!ERANGE`{.interpreted-text role="c:macro"}) and `!ULONG_MAX`{.interpreted-text role="c:macro"} is returned. If no conversion can be performed, `0` is returned.
>
> See also the Unix man page `strtoul(3)`{.interpreted-text role="manpage"}.
>
> ::: versionadded
> 3.2
> :::

> Convert the initial part of the string in `str` to an `long`{.interpreted-text role="c:expr"} value according to the given `base`, which must be between `2` and `36` inclusive, or be the special value `0`.
>
> Same as `PyOS_strtoul`{.interpreted-text role="c:func"}, but return a `long`{.interpreted-text role="c:expr"} value instead and `LONG_MAX`{.interpreted-text role="c:macro"} on overflows.
>
> See also the Unix man page `strtol(3)`{.interpreted-text role="manpage"}.
>
> ::: versionadded
> 3.2
> :::

> Convert a string `s` to a `double`{.interpreted-text role="c:expr"}, raising a Python exception on failure. The set of accepted strings corresponds to the set of strings accepted by Python\'s `float`{.interpreted-text role="func"} constructor, except that `s` must not have leading or trailing whitespace. The conversion is independent of the current locale.
>
> If `endptr` is `NULL`, convert the whole string. Raise `ValueError`{.interpreted-text role="exc"} and return `-1.0` if the string is not a valid representation of a floating-point number.
>
> If endptr is not `NULL`, convert as much of the string as possible and set `*endptr` to point to the first unconverted character. If no initial segment of the string is the valid representation of a floating-point number, set `*endptr` to point to the beginning of the string, raise ValueError, and return `-1.0`.
>
> If `s` represents a value that is too large to store in a float (for example, `"1e500"` is such a string on many platforms) then if `overflow_exception` is `NULL` return `!INFINITY`{.interpreted-text role="c:macro"} (with an appropriate sign) and don\'t set any exception. Otherwise, `overflow_exception` must point to a Python exception object; raise that exception and return `-1.0`. In both cases, set `*endptr` to point to the first character after the converted value.
>
> If any other error occurs during the conversion (for example an out-of-memory error), set the appropriate Python exception and return `-1.0`.
>
> ::: versionadded
> 3.1
> :::

> Convert a `double`{.interpreted-text role="c:expr"} *val* to a string using supplied *format_code*, *precision*, and *flags*.
>
> *format_code* must be one of `'e'`, `'E'`, `'f'`, `'F'`, `'g'`, `'G'` or `'r'`. For `'r'`, the supplied *precision* must be 0 and is ignored. The `'r'` format code specifies the standard `repr`{.interpreted-text role="func"} format.
>
> *flags* can be zero or more of the following values or-ed together:
>
> > Always precede the returned string with a sign character, even if *val* is non-negative.
>
> > Ensure that the returned string will not look like an integer.
>
> > Apply \"alternate\" formatting rules. See the documentation for the `PyOS_snprintf`{.interpreted-text role="c:func"} `'#'` specifier for details.
>
> > Negative zero is converted to positive zero.
> >
> > ::: versionadded
> > 3.11
> > :::
>
> If *ptype* is non-`NULL`, then the value it points to will be set to one of the following constants depending on the type of *val*:
>
>   *\*ptype*   type of *val*
>   ----------- -----------------
>               finite number
>               infinite number
>               not a number
>
> The return value is a pointer to *buffer* with the converted string or `NULL` if the conversion failed. The caller is responsible for freeing the returned string by calling `PyMem_Free`{.interpreted-text role="c:func"}.
>
> ::: versionadded
> 3.1
> :::

# Character classification and conversion

The following macros provide locale-independent (unlike the C standard library `ctype.h`) character classification and conversion. The argument must be a signed or unsigned `char`{.interpreted-text role="c:expr"}.

> Return true if the character *c* is an alphanumeric character.

> Return true if the character *c* is an alphabetic character (`a-z` and `A-Z`).

> Return true if the character *c* is a decimal digit (`0-9`).

> Return true if the character *c* is a lowercase ASCII letter (`a-z`).

> Return true if the character *c* is an uppercase ASCII letter (`A-Z`).

> Return true if the character *c* is a whitespace character (space, tab, carriage return, newline, vertical tab, or form feed).

> Return true if the character *c* is a hexadecimal digit (`0-9`, `a-f`, and `A-F`).

> Return the lowercase equivalent of the character *c*.

> Return the uppercase equivalent of the character *c*.
