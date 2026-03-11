# Unicode Objects and Codecs {#unicodeobjects}

## Unicode Objects

Since the implementation of `393`{.interpreted-text role="pep"} in Python 3.3, Unicode objects internally use a variety of representations, in order to allow handling the complete range of Unicode characters while staying memory efficient. There are special cases for strings where all code points are below 128, 256, or 65536; otherwise, code points must be below 1114112 (which is the full Unicode range).

UTF-8 representation is created on demand and cached in the Unicode object.

:::: note
::: title
Note
:::

The `Py_UNICODE`{.interpreted-text role="c:type"} representation has been removed since Python 3.12 with deprecated APIs. See `623`{.interpreted-text role="pep"} for more information.
::::

### Unicode Type

These are the basic Unicode object types used for the Unicode implementation in Python:

> This instance of `PyTypeObject`{.interpreted-text role="c:type"} represents the Python Unicode type. It is exposed to Python code as `str`{.interpreted-text role="py:class"}.

> This instance of `PyTypeObject`{.interpreted-text role="c:type"} represents the Python Unicode iterator type. It is used to iterate over Unicode string objects.

The following APIs are C macros and static inlined functions for fast checks and access to internal read-only data of Unicode objects:

> Return true if the object *obj* is a Unicode object or an instance of a Unicode subtype. This function always succeeds.

> Return true if the object *obj* is a Unicode object, but not an instance of a subtype. This function always succeeds.

> Return the length of the Unicode string, in code points. *unicode* has to be a Unicode object in the \"canonical\" representation (not checked).
>
> ::: versionadded
> 3.3
> :::

> Return one of the PyUnicode kind constants (see above) that indicate how many bytes per character this Unicode object uses to store its data. *unicode* has to be a Unicode object in the \"canonical\" representation (not checked).
>
> ::: versionadded
> 3.3
> :::

> Return a void pointer to the raw Unicode buffer. *unicode* has to be a Unicode object in the \"canonical\" representation (not checked).
>
> ::: versionadded
> 3.3
> :::

> Read a character from a Unicode object *unicode*, which must be in the \"canonical\" representation. This is less efficient than `PyUnicode_READ`{.interpreted-text role="c:func"} if you do multiple consecutive reads.
>
> ::: versionadded
> 3.3
> :::

> Return the maximum code point that is suitable for creating another string based on *unicode*, which must be in the \"canonical\" representation. This is always an approximation but more efficient than iterating over the string.
>
> ::: versionadded
> 3.3
> :::

> Return `1` if the string is a valid identifier according to the language definition, section `identifiers`{.interpreted-text role="ref"}. Return `0` otherwise.
>
> ::: versionchanged
> 3.9 The function does not call `Py_FatalError`{.interpreted-text role="c:func"} anymore if the string is not ready.
> :::

> Return true if the string only contains ASCII characters. Equivalent to `str.isascii`{.interpreted-text role="py:meth"}.
>
> ::: versionadded
> 3.2
> :::

> If the hash of *str*, as returned by `PyObject_Hash`{.interpreted-text role="c:func"}, has been cached and is immediately available, return it. Otherwise, return `-1` *without* setting an exception.
>
> If *str* is not a string (that is, if `PyUnicode_Check(obj)` is false), the behavior is undefined.
>
> This function never fails with an exception.
>
> Note that there are no guarantees on when an object\'s hash is cached, and the (non-)existence of a cached hash does not imply that the string has any other properties.

### Unicode Character Properties

Unicode provides many different character properties. The most often needed ones are available through these macros which are mapped to C functions depending on the Python configuration.

> Return `1` or `0` depending on whether *ch* is a whitespace character.

> Return `1` or `0` depending on whether *ch* is a lowercase character.

> Return `1` or `0` depending on whether *ch* is an uppercase character.

> Return `1` or `0` depending on whether *ch* is a titlecase character.

> Return `1` or `0` depending on whether *ch* is a linebreak character.

> Return `1` or `0` depending on whether *ch* is a decimal character.

> Return `1` or `0` depending on whether *ch* is a digit character.

> Return `1` or `0` depending on whether *ch* is a numeric character.

> Return `1` or `0` depending on whether *ch* is an alphabetic character.

> Return `1` or `0` depending on whether *ch* is an alphanumeric character.

> Return `1` or `0` depending on whether *ch* is a printable character, in the sense of `str.isprintable`{.interpreted-text role="meth"}.

These APIs can be used for fast direct character conversions:

> Return the character *ch* converted to lower case.

> Return the character *ch* converted to upper case.

> Return the character *ch* converted to title case.

> Return the character *ch* converted to a decimal positive integer. Return `-1` if this is not possible. This function does not raise exceptions.

> Return the character *ch* converted to a single digit integer. Return `-1` if this is not possible. This function does not raise exceptions.

> Return the character *ch* converted to a double. Return `-1.0` if this is not possible. This function does not raise exceptions.

These APIs can be used to work with surrogates:

> Check if *ch* is a surrogate (`0xD800 <= ch <= 0xDFFF`).

> Check if *ch* is a high surrogate (`0xD800 <= ch <= 0xDBFF`).

> Check if *ch* is a low surrogate (`0xDC00 <= ch <= 0xDFFF`).

> Return the high UTF-16 surrogate (`0xD800` to `0xDBFF`) for a Unicode code point in the range `[0x10000; 0x10FFFF]`.

> Return the low UTF-16 surrogate (`0xDC00` to `0xDFFF`) for a Unicode code point in the range `[0x10000; 0x10FFFF]`.

> Join two surrogate code points and return a single `Py_UCS4`{.interpreted-text role="c:type"} value. *high* and *low* are respectively the leading and trailing surrogates in a surrogate pair. *high* must be in the range `[0xD800; 0xDBFF]` and *low* must be in the range `[0xDC00; 0xDFFF]`.

### Creating and accessing Unicode strings

To create Unicode objects and access their basic sequence properties, use these APIs:

> Create a new Unicode object. *maxchar* should be the true maximum code point to be placed in the string. As an approximation, it can be rounded up to the nearest value in the sequence 127, 255, 65535, 1114111.
>
> On error, set an exception and return `NULL`.
>
> After creation, the string can be filled by `PyUnicode_WriteChar`{.interpreted-text role="c:func"}, `PyUnicode_CopyCharacters`{.interpreted-text role="c:func"}, `PyUnicode_Fill`{.interpreted-text role="c:func"}, `PyUnicode_WRITE`{.interpreted-text role="c:func"} or similar. Since strings are supposed to be immutable, take care to not "use" the result while it is being modified. In particular, before it\'s filled with its final contents, a string:
>
> - must not be hashed,
> - must not be `converted to UTF-8 <PyUnicode_AsUTF8AndSize>`{.interpreted-text role="c:func"}, or another non-\"canonical\" representation,
> - must not have its reference count changed,
> - must not be shared with code that might do one of the above.
>
> This list is not exhaustive. Avoiding these uses is your responsibility; Python does not always check these requirements.
>
> To avoid accidentally exposing a partially-written string object, prefer using the `PyUnicodeWriter`{.interpreted-text role="c:type"} API, or one of the `PyUnicode_From*` functions below.
>
> ::: versionadded
> 3.3
> :::

> Create a Unicode object from the char buffer *str*. The bytes will be interpreted as being UTF-8 encoded. The buffer is copied into the new object. The return value might be a shared object, i.e. modification of the data is not allowed.
>
> This function raises `SystemError`{.interpreted-text role="exc"} when:
>
> - *size* \< 0,
> - *str* is `NULL` and *size* \> 0
>
> ::: versionchanged
> 3.12 *str* == `NULL` with *size* \> 0 is not allowed anymore.
> :::

> Create a Unicode object from a UTF-8 encoded null-terminated char buffer *str*.

> Take a C `printf`{.interpreted-text role="c:func"}-style *format* string and a variable number of arguments, calculate the size of the resulting Python Unicode string and return a string with the values formatted into it. The variable arguments must be C types and must correspond exactly to the format characters in the *format* ASCII-encoded string.
>
> A conversion specifier contains two or more characters and has the following components, which must occur in this order:
>
> 1.  The `'%'` character, which marks the start of the specifier.
> 2.  Conversion flags (optional), which affect the result of some conversion types.
> 3.  Minimum field width (optional). If specified as an `'*'` (asterisk), the actual width is given in the next argument, which must be of type `int`{.interpreted-text role="c:expr"}, and the object to convert comes after the minimum field width and optional precision.
> 4.  Precision (optional), given as a `'.'` (dot) followed by the precision. If specified as `'*'` (an asterisk), the actual precision is given in the next argument, which must be of type `int`{.interpreted-text role="c:expr"}, and the value to convert comes after the precision.
> 5.  Length modifier (optional).
> 6.  Conversion type.
>
> The conversion flag characters are:
>
> ::: tabularcolumns
> [\|l\|](##SUBST##|l|)L\|
> :::
>
>   ------------------------------------------------------------------------------------------
>   Flag    Meaning
>   ------- ----------------------------------------------------------------------------------
>   `0`     The conversion will be zero padded for numeric values.
>
>   `-`     The converted value is left adjusted (overrides the `0` flag if both are given).
>   ------------------------------------------------------------------------------------------
>
> The length modifiers for following integer conversions (`d`, `i`, `o`, `u`, `x`, or `X`) specify the type of the argument (`int`{.interpreted-text role="c:expr"} by default):
>
> ::: tabularcolumns
> [\|l\|](##SUBST##|l|)L\|
> :::
>
>   ------------------------------------------------------------------------------------------------------------------
>   Modifier   Types
>   ---------- -------------------------------------------------------------------------------------------------------
>   `l`        `long`{.interpreted-text role="c:expr"} or `unsigned long`{.interpreted-text role="c:expr"}
>
>   `ll`       `long long`{.interpreted-text role="c:expr"} or `unsigned long long`{.interpreted-text role="c:expr"}
>
>   `j`        `intmax_t`{.interpreted-text role="c:type"} or `uintmax_t`{.interpreted-text role="c:type"}
>
>   `z`        `size_t`{.interpreted-text role="c:type"} or `ssize_t`{.interpreted-text role="c:type"}
>
>   `t`        `ptrdiff_t`{.interpreted-text role="c:type"}
>   ------------------------------------------------------------------------------------------------------------------
>
> The length modifier `l` for following conversions `s` or `V` specify that the type of the argument is `const wchar_t*`{.interpreted-text role="c:expr"}.
>
> The conversion specifiers are:
>
>   Conversion Specifier   Type                                                                                                                                                Comment
>   ---------------------- --------------------------------------------------------------------------------------------------------------------------------------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
>   `%`                    *n/a*                                                                                                                                               The literal `%` character.
>   `d`, `i`               Specified by the length modifier                                                                                                                    The decimal representation of a signed C integer.
>   `u`                    Specified by the length modifier                                                                                                                    The decimal representation of an unsigned C integer.
>   `o`                    Specified by the length modifier                                                                                                                    The octal representation of an unsigned C integer.
>   `x`                    Specified by the length modifier                                                                                                                    The hexadecimal representation of an unsigned C integer (lowercase).
>   `X`                    Specified by the length modifier                                                                                                                    The hexadecimal representation of an unsigned C integer (uppercase).
>   `c`                    `int`{.interpreted-text role="c:expr"}                                                                                                              A single character.
>   `s`                    `const char*`{.interpreted-text role="c:expr"} or `const wchar_t*`{.interpreted-text role="c:expr"}                                                 A null-terminated C character array.
>   `p`                    `const void*`{.interpreted-text role="c:expr"}                                                                                                      The hex representation of a C pointer. Mostly equivalent to `printf("%p")` except that it is guaranteed to start with the literal `0x` regardless of what the platform\'s `printf` yields.
>   `A`                    `PyObject*`{.interpreted-text role="c:expr"}                                                                                                        The result of calling `ascii`{.interpreted-text role="func"}.
>   `U`                    `PyObject*`{.interpreted-text role="c:expr"}                                                                                                        A Unicode object.
>   `V`                    `PyObject*`{.interpreted-text role="c:expr"}, `const char*`{.interpreted-text role="c:expr"} or `const wchar_t*`{.interpreted-text role="c:expr"}   A Unicode object (which may be `NULL`) and a null-terminated C character array as a second parameter (which will be used, if the first parameter is `NULL`).
>   `S`                    `PyObject*`{.interpreted-text role="c:expr"}                                                                                                        The result of calling `PyObject_Str`{.interpreted-text role="c:func"}.
>   `R`                    `PyObject*`{.interpreted-text role="c:expr"}                                                                                                        The result of calling `PyObject_Repr`{.interpreted-text role="c:func"}.
>   `T`                    `PyObject*`{.interpreted-text role="c:expr"}                                                                                                        Get the fully qualified name of an object type; call `PyType_GetFullyQualifiedName`{.interpreted-text role="c:func"}.
>   `#T`                   `PyObject*`{.interpreted-text role="c:expr"}                                                                                                        Similar to `T` format, but use a colon (`:`) as separator between the module name and the qualified name.
>   `N`                    `PyTypeObject*`{.interpreted-text role="c:expr"}                                                                                                    Get the fully qualified name of a type; call `PyType_GetFullyQualifiedName`{.interpreted-text role="c:func"}.
>   `#N`                   `PyTypeObject*`{.interpreted-text role="c:expr"}                                                                                                    Similar to `N` format, but use a colon (`:`) as separator between the module name and the qualified name.
>
> :::: note
> ::: title
> Note
> :::
>
> The width formatter unit is number of characters rather than bytes. The precision formatter unit is number of bytes or `wchar_t`{.interpreted-text role="c:type"} items (if the length modifier `l` is used) for `"%s"` and `"%V"` (if the `PyObject*` argument is `NULL`), and a number of characters for `"%A"`, `"%U"`, `"%S"`, `"%R"` and `"%V"` (if the `PyObject*` argument is not `NULL`).
> ::::
>
> :::: note
> ::: title
> Note
> :::
>
> Unlike to C `printf`{.interpreted-text role="c:func"} the `0` flag has effect even when a precision is given for integer conversions (`d`, `i`, `u`, `o`, `x`, or `X`).
> ::::
>
> ::: versionchanged
> 3.2 Support for `"%lld"` and `"%llu"` added.
> :::
>
> ::: versionchanged
> 3.3 Support for `"%li"`, `"%lli"` and `"%zi"` added.
> :::
>
> ::: versionchanged
> 3.4 Support width and precision formatter for `"%s"`, `"%A"`, `"%U"`, `"%V"`, `"%S"`, `"%R"` added.
> :::
>
> ::: versionchanged
> 3.12 Support for conversion specifiers `o` and `X`. Support for length modifiers `j` and `t`. Length modifiers are now applied to all integer conversions. Length modifier `l` is now applied to conversion specifiers `s` and `V`. Support for variable width and precision `*`. Support for flag `-`.
>
> An unrecognized format character now sets a `SystemError`{.interpreted-text role="exc"}. In previous versions it caused all the rest of the format string to be copied as-is to the result string, and any extra arguments discarded.
> :::
>
> ::: versionchanged
> 3.13 Support for `%T`, `%#T`, `%N` and `%#N` formats added.
> :::

> Identical to `PyUnicode_FromFormat`{.interpreted-text role="c:func"} except that it takes exactly two arguments.

> Copy an instance of a Unicode subtype to a new true Unicode object if necessary. If *obj* is already a true Unicode object (not a subtype), return a new `strong reference`{.interpreted-text role="term"} to the object.
>
> Objects other than Unicode or its subtypes will cause a `TypeError`{.interpreted-text role="exc"}.

> Create a Unicode Object from the given Unicode code point *ordinal*.
>
> The ordinal must be in `range(0x110000)`. A `ValueError`{.interpreted-text role="exc"} is raised in the case it is not.

> Append the string *right* to the end of *p_left*. *p_left* must point to a `strong reference`{.interpreted-text role="term"} to a Unicode object; `!PyUnicode_Append`{.interpreted-text role="c:func"} releases (\"steals\") this reference.
>
> On error, set *\*p_left* to `NULL` and set an exception.
>
> On success, set *\*p_left* to a new strong reference to the result.

> The function is similar to `PyUnicode_Append`{.interpreted-text role="c:func"}, with the only difference being that it decrements the reference count of *right* by one.

> Return a mapping suitable for decoding a custom single-byte encoding. Given a Unicode string *string* of up to 256 characters representing an encoding table, returns either a compact internal mapping object or a dictionary mapping character ordinals to byte values. Raises a `TypeError`{.interpreted-text role="exc"} and return `NULL` on invalid input.
>
> ::: versionadded
> 3.2
> :::

> Return the name of the default string encoding, `"utf-8"`. See `sys.getdefaultencoding`{.interpreted-text role="func"}.
>
> The returned string does not need to be freed, and is valid until interpreter shutdown.

> Return the length of the Unicode object, in code points.
>
> On error, set an exception and return `-1`.
>
> ::: versionadded
> 3.3
> :::

> Resize a Unicode object *\*unicode* to the new *length* in code points.
>
> Try to resize the string in place (which is usually faster than allocating a new string and copying characters), or create a new string.
>
> *\*unicode* is modified to point to the new (resized) object and `0` is returned on success. Otherwise, `-1` is returned and an exception is set, and *\*unicode* is left untouched.
>
> The function doesn\'t check string content, the result may not be a string in canonical representation.

> Read a character from a string. This function checks that *unicode* is a Unicode object and the index is not out of bounds, in contrast to `PyUnicode_READ_CHAR`{.interpreted-text role="c:func"}, which performs no error checking.
>
> Return character on success, `-1` on error with an exception set.
>
> ::: versionadded
> 3.3
> :::

> Copy the string *unicode* into a new UCS4 buffer that is allocated using `PyMem_Malloc`{.interpreted-text role="c:func"}. If this fails, `NULL` is returned with a `MemoryError`{.interpreted-text role="exc"} set. The returned buffer always has an extra null code point appended.
>
> ::: versionadded
> 3.3
> :::

### Locale Encoding

The current locale encoding can be used to decode text from the operating system.

> Similar to `PyUnicode_DecodeLocaleAndSize`{.interpreted-text role="c:func"}, but compute the string length using `!strlen`{.interpreted-text role="c:func"}.
>
> ::: versionadded
> 3.3
> :::

> Encode a Unicode object to UTF-8 on Android and VxWorks, or to the current locale encoding on other platforms. The supported error handlers are `"strict"` and `"surrogateescape"` (`383`{.interpreted-text role="pep"}). The encoder uses `"strict"` error handler if *errors* is `NULL`. Return a `bytes`{.interpreted-text role="class"} object. *unicode* cannot contain embedded null characters.
>
> Use `PyUnicode_EncodeFSDefault`{.interpreted-text role="c:func"} to encode a string to the `filesystem encoding and error handler`{.interpreted-text role="term"}.
>
> This function ignores the `Python UTF-8 Mode <utf8-mode>`{.interpreted-text role="ref"}.
>
> ::: seealso
> The `Py_EncodeLocale`{.interpreted-text role="c:func"} function.
> :::
>
> ::: versionadded
> 3.3
> :::
>
> ::: versionchanged
> 3.7 The function now also uses the current locale encoding for the `surrogateescape` error handler, except on Android. Previously, `Py_EncodeLocale`{.interpreted-text role="c:func"} was used for the `surrogateescape`, and the current locale encoding was used for `strict`.
> :::

### File System Encoding

Functions encoding to and decoding from the `filesystem encoding and
error handler`{.interpreted-text role="term"} (`383`{.interpreted-text role="pep"} and `529`{.interpreted-text role="pep"}).

To encode file names to `bytes`{.interpreted-text role="class"} during argument parsing, the `"O&"` converter should be used, passing `!PyUnicode_FSConverter`{.interpreted-text role="c:func"} as the conversion function:

> `PyArg_Parse\* converter <arg-parsing>`{.interpreted-text role="ref"}: encode `str`{.interpreted-text role="class"} objects \-- obtained directly or through the `os.PathLike`{.interpreted-text role="class"} interface \-- to `bytes`{.interpreted-text role="class"} using `PyUnicode_EncodeFSDefault`{.interpreted-text role="c:func"}; `bytes`{.interpreted-text role="class"} objects are output as-is. *result* must be an address of a C variable of type `PyObject*`{.interpreted-text role="c:expr"} (or `PyBytesObject*`{.interpreted-text role="c:expr"}). On success, set the variable to a new `strong reference`{.interpreted-text role="term"} to a `bytes object <bytesobjects>`{.interpreted-text role="ref"} which must be released when it is no longer used and return a non-zero value (`Py_CLEANUP_SUPPORTED`{.interpreted-text role="c:macro"}). Embedded null bytes are not allowed in the result. On failure, return `0` with an exception set.
>
> If *obj* is `NULL`, the function releases a strong reference stored in the variable referred by *result* and returns `1`.
>
> ::: versionadded
> 3.1
> :::
>
> ::: versionchanged
> 3.6 Accepts a `path-like object`{.interpreted-text role="term"}.
> :::

To decode file names to `str`{.interpreted-text role="class"} during argument parsing, the `"O&"` converter should be used, passing `!PyUnicode_FSDecoder`{.interpreted-text role="c:func"} as the conversion function:

> `PyArg_Parse\* converter <arg-parsing>`{.interpreted-text role="ref"}: decode `bytes`{.interpreted-text role="class"} objects \-- obtained either directly or indirectly through the `os.PathLike`{.interpreted-text role="class"} interface \-- to `str`{.interpreted-text role="class"} using `PyUnicode_DecodeFSDefaultAndSize`{.interpreted-text role="c:func"}; `str`{.interpreted-text role="class"} objects are output as-is. *result* must be an address of a C variable of type `PyObject*`{.interpreted-text role="c:expr"} (or `PyUnicodeObject*`{.interpreted-text role="c:expr"}). On success, set the variable to a new `strong reference`{.interpreted-text role="term"} to a `Unicode object <unicodeobjects>`{.interpreted-text role="ref"} which must be released when it is no longer used and return a non-zero value (`Py_CLEANUP_SUPPORTED`{.interpreted-text role="c:macro"}). Embedded null characters are not allowed in the result. On failure, return `0` with an exception set.
>
> If *obj* is `NULL`, release the strong reference to the object referred to by *result* and return `1`.
>
> ::: versionadded
> 3.2
> :::
>
> ::: versionchanged
> 3.6 Accepts a `path-like object`{.interpreted-text role="term"}.
> :::

> Decode a string from the `filesystem encoding and error handler`{.interpreted-text role="term"}.
>
> If you need to decode a string from the current locale encoding, use `PyUnicode_DecodeLocaleAndSize`{.interpreted-text role="c:func"}.
>
> ::: seealso
> The `Py_DecodeLocale`{.interpreted-text role="c:func"} function.
> :::
>
> ::: versionchanged
> 3.6 The `filesystem error handler <filesystem encoding and error
> handler>`{.interpreted-text role="term"} is now used.
> :::

> Decode a null-terminated string from the `filesystem encoding and
> error handler`{.interpreted-text role="term"}.
>
> If the string length is known, use `PyUnicode_DecodeFSDefaultAndSize`{.interpreted-text role="c:func"}.
>
> ::: versionchanged
> 3.6 The `filesystem error handler <filesystem encoding and error
> handler>`{.interpreted-text role="term"} is now used.
> :::

> Encode a Unicode object to the `filesystem encoding and error
> handler`{.interpreted-text role="term"}, and return `bytes`{.interpreted-text role="class"}. Note that the resulting `bytes`{.interpreted-text role="class"} object can contain null bytes.
>
> If you need to encode a string to the current locale encoding, use `PyUnicode_EncodeLocale`{.interpreted-text role="c:func"}.
>
> ::: seealso
> The `Py_EncodeLocale`{.interpreted-text role="c:func"} function.
> :::
>
> ::: versionadded
> 3.2
> :::
>
> ::: versionchanged
> 3.6 The `filesystem error handler <filesystem encoding and error
> handler>`{.interpreted-text role="term"} is now used.
> :::

### wchar_t Support

`wchar_t`{.interpreted-text role="c:type"} support for platforms which support it:

> Create a Unicode object from the `wchar_t`{.interpreted-text role="c:type"} buffer *wstr* of the given *size*. Passing `-1` as the *size* indicates that the function must itself compute the length, using `!wcslen`{.interpreted-text role="c:func"}. Return `NULL` on failure.

> Copy the Unicode object contents into the `wchar_t`{.interpreted-text role="c:type"} buffer *wstr*. At most *size* `wchar_t`{.interpreted-text role="c:type"} characters are copied (excluding a possibly trailing null termination character). Return the number of `wchar_t`{.interpreted-text role="c:type"} characters copied or `-1` in case of an error.
>
> When *wstr* is `NULL`, instead return the *size* that would be required to store all of *unicode* including a terminating null.
>
> Note that the resulting `wchar_t*`{.interpreted-text role="c:expr"} string may or may not be null-terminated. It is the responsibility of the caller to make sure that the `wchar_t*`{.interpreted-text role="c:expr"} string is null-terminated in case this is required by the application. Also, note that the `wchar_t*`{.interpreted-text role="c:expr"} string might contain null characters, which would cause the string to be truncated when used with most C functions.

> Convert the Unicode object to a wide character string. The output string always ends with a null character. If *size* is not `NULL`, write the number of wide characters (excluding the trailing null termination character) into *\*size*. Note that the resulting `wchar_t`{.interpreted-text role="c:type"} string might contain null characters, which would cause the string to be truncated when used with most C functions. If *size* is `NULL` and the `wchar_t*`{.interpreted-text role="c:expr"} string contains null characters a `ValueError`{.interpreted-text role="exc"} is raised.
>
> Returns a buffer allocated by `PyMem_New`{.interpreted-text role="c:macro"} (use `PyMem_Free`{.interpreted-text role="c:func"} to free it) on success. On error, returns `NULL` and *\*size* is undefined. Raises a `MemoryError`{.interpreted-text role="exc"} if memory allocation is failed.
>
> ::: versionadded
> 3.2
> :::
>
> ::: versionchanged
> 3.7 Raises a `ValueError`{.interpreted-text role="exc"} if *size* is `NULL` and the `wchar_t*`{.interpreted-text role="c:expr"} string contains null characters.
> :::

## Built-in Codecs {#builtincodecs}

Python provides a set of built-in codecs which are written in C for speed. All of these codecs are directly usable via the following functions.

Many of the following APIs take two arguments encoding and errors, and they have the same semantics as the ones of the built-in `str`{.interpreted-text role="func"} string object constructor.

Setting encoding to `NULL` causes the default encoding to be used which is UTF-8. The file system calls should use `PyUnicode_FSConverter`{.interpreted-text role="c:func"} for encoding file names. This uses the `filesystem encoding and error handler`{.interpreted-text role="term"} internally.

Error handling is set by errors which may also be set to `NULL` meaning to use the default handling defined for the codec. Default error handling for all built-in codecs is \"strict\" (`ValueError`{.interpreted-text role="exc"} is raised).

The codecs all use a similar interface. Only deviations from the following generic ones are documented for simplicity.

### Generic Codecs

The following macro is provided:

> The Unicode code point `U+FFFD` (replacement character).
>
> This Unicode character is used as the replacement character during decoding if the *errors* argument is set to \"replace\".

These are the generic codec APIs:

### UTF-8 Codecs

These are the UTF-8 codec APIs:

> Create a Unicode object by decoding *size* bytes of the UTF-8 encoded string *str*. Return `NULL` if an exception was raised by the codec.

> Encode a Unicode object using UTF-8 and return the result as Python bytes object. Error handling is \"strict\". Return `NULL` if an exception was raised by the codec.
>
> The function fails if the string contains surrogate code points (`U+D800` - `U+DFFF`).

> Return a pointer to the UTF-8 encoding of the Unicode object, and store the size of the encoded representation (in bytes) in *size*. The *size* argument can be `NULL`; in this case no size will be stored. The returned buffer always has an extra null byte appended (not included in *size*), regardless of whether there are any other null code points.
>
> On error, set an exception, set *size* to `-1` (if it\'s not NULL) and return `NULL`.
>
> The function fails if the string contains surrogate code points (`U+D800` - `U+DFFF`).
>
> This caches the UTF-8 representation of the string in the Unicode object, and subsequent calls will return a pointer to the same buffer. The caller is not responsible for deallocating the buffer. The buffer is deallocated and pointers to it become invalid when the Unicode object is garbage collected.
>
> ::: versionadded
> 3.3
> :::
>
> ::: versionchanged
> 3.7 The return type is now `const char *` rather of `char *`.
> :::
>
> ::: versionchanged
> 3.10 This function is a part of the `limited API <limited-c-api>`{.interpreted-text role="ref"}.
> :::

> As `PyUnicode_AsUTF8AndSize`{.interpreted-text role="c:func"}, but does not store the size.
>
> :::: warning
> ::: title
> Warning
> :::
>
> This function does not have any special behavior for [null characters](https://en.wikipedia.org/wiki/Null_character) embedded within *unicode*. As a result, strings containing null characters will remain in the returned string, which some C functions might interpret as the end of the string, leading to truncation. If truncation is an issue, it is recommended to use `PyUnicode_AsUTF8AndSize`{.interpreted-text role="c:func"} instead.
> ::::
>
> ::: versionadded
> 3.3
> :::
>
> ::: versionchanged
> 3.7 The return type is now `const char *` rather of `char *`.
> :::

### UTF-32 Codecs

These are the UTF-32 codec APIs:

> Return a Python byte string using the UTF-32 encoding in native byte order. The string always starts with a BOM mark. Error handling is \"strict\". Return `NULL` if an exception was raised by the codec.

### UTF-16 Codecs

These are the UTF-16 codec APIs:

> Return a Python byte string using the UTF-16 encoding in native byte order. The string always starts with a BOM mark. Error handling is \"strict\". Return `NULL` if an exception was raised by the codec.

### UTF-7 Codecs

These are the UTF-7 codec APIs:

> Create a Unicode object by decoding *size* bytes of the UTF-7 encoded string *str*. Return `NULL` if an exception was raised by the codec.

### Unicode-Escape Codecs

These are the \"Unicode Escape\" codec APIs:

> Encode a Unicode object using Unicode-Escape and return the result as a bytes object. Error handling is \"strict\". Return `NULL` if an exception was raised by the codec.

### Raw-Unicode-Escape Codecs

These are the \"Raw Unicode Escape\" codec APIs:

> Encode a Unicode object using Raw-Unicode-Escape and return the result as a bytes object. Error handling is \"strict\". Return `NULL` if an exception was raised by the codec.

### Latin-1 Codecs

These are the Latin-1 codec APIs: Latin-1 corresponds to the first 256 Unicode ordinals and only these are accepted by the codecs during encoding.

> Create a Unicode object by decoding *size* bytes of the Latin-1 encoded string *str*. Return `NULL` if an exception was raised by the codec.

> Encode a Unicode object using Latin-1 and return the result as Python bytes object. Error handling is \"strict\". Return `NULL` if an exception was raised by the codec.

### ASCII Codecs

These are the ASCII codec APIs. Only 7-bit ASCII data is accepted. All other codes generate errors.

> Create a Unicode object by decoding *size* bytes of the ASCII encoded string *str*. Return `NULL` if an exception was raised by the codec.

> Encode a Unicode object using ASCII and return the result as Python bytes object. Error handling is \"strict\". Return `NULL` if an exception was raised by the codec.

### Character Map Codecs

This codec is special in that it can be used to implement many different codecs (and this is in fact what was done to obtain most of the standard codecs included in the `!encodings`{.interpreted-text role="mod"} package). The codec uses mappings to encode and decode characters. The mapping objects provided must support the `~object.__getitem__`{.interpreted-text role="meth"} mapping interface; dictionaries and sequences work well.

These are the mapping codec APIs:

> Encode a Unicode object using the given *mapping* object and return the result as a bytes object. Error handling is \"strict\". Return `NULL` if an exception was raised by the codec.
>
> The *mapping* object must map Unicode ordinal integers to bytes objects, integers in the range from 0 to 255 or `None`. Unmapped character ordinals (ones which cause a `LookupError`{.interpreted-text role="exc"}) as well as mapped to `None` are treated as \"undefined mapping\" and cause an error.

The following codec API is special in that maps Unicode to Unicode.

> Translate a string by applying a character mapping table to it and return the resulting Unicode object. Return `NULL` if an exception was raised by the codec.
>
> The mapping table must map Unicode ordinal integers to Unicode ordinal integers or `None` (causing deletion of the character).
>
> Mapping tables need only provide the `~object.__getitem__`{.interpreted-text role="meth"} interface; dictionaries and sequences work well. Unmapped character ordinals (ones which cause a `LookupError`{.interpreted-text role="exc"}) are left untouched and are copied as-is.
>
> *errors* has the usual meaning for codecs. It may be `NULL` which indicates to use the default error handling.

### MBCS codecs for Windows

These are the MBCS codec APIs. They are currently only available on Windows and use the Win32 MBCS converters to implement the conversions. Note that MBCS (or DBCS) is a class of encodings, not just one. The target encoding is defined by the user settings on the machine running the codec.

> Create a Unicode object by decoding *size* bytes of the MBCS encoded string *str*. Return `NULL` if an exception was raised by the codec.

> Encode a Unicode object using MBCS and return the result as Python bytes object. Error handling is \"strict\". Return `NULL` if an exception was raised by the codec.

> Encode the Unicode object using the specified code page and return a Python bytes object. Return `NULL` if an exception was raised by the codec. Use `!CP_ACP`{.interpreted-text role="c:macro"} code page to get the MBCS encoder.
>
> ::: versionadded
> 3.3
> :::

## Methods and Slot Functions {#unicodemethodsandslots}

The following APIs are capable of handling Unicode objects and strings on input (we refer to them as strings in the descriptions) and return Unicode objects or integers as appropriate.

They all return `NULL` or `-1` if an exception occurs.

> Concat two strings giving a new Unicode string.

> Split a string giving a list of Unicode strings. If *sep* is `NULL`, splitting will be done at all whitespace substrings. Otherwise, splits occur at the given separator. At most *maxsplit* splits will be done. If negative, no limit is set. Separators are not included in the resulting list.
>
> On error, return `NULL` with an exception set.
>
> Equivalent to `str.split`{.interpreted-text role="py:meth"}.

> Similar to `PyUnicode_Split`{.interpreted-text role="c:func"}, but splitting will be done beginning at the end of the string.
>
> On error, return `NULL` with an exception set.
>
> Equivalent to `str.rsplit`{.interpreted-text role="py:meth"}.

> Split a Unicode string at line breaks, returning a list of Unicode strings. CRLF is considered to be one line break. If *keepends* is `0`, the Line break characters are not included in the resulting strings.

> Split a Unicode string at the first occurrence of *sep*, and return a 3-tuple containing the part before the separator, the separator itself, and the part after the separator. If the separator is not found, return a 3-tuple containing the string itself, followed by two empty strings.
>
> *sep* must not be empty.
>
> On error, return `NULL` with an exception set.
>
> Equivalent to `str.partition`{.interpreted-text role="py:meth"}.

> Similar to `PyUnicode_Partition`{.interpreted-text role="c:func"}, but split a Unicode string at the last occurrence of *sep*. If the separator is not found, return a 3-tuple containing two empty strings, followed by the string itself.
>
> *sep* must not be empty.
>
> On error, return `NULL` with an exception set.
>
> Equivalent to `str.rpartition`{.interpreted-text role="py:meth"}.

> Join a sequence of strings using the given *separator* and return the resulting Unicode string.

> Compare two strings and return `-1`, `0`, `1` for less than, equal, and greater than, respectively.
>
> This function returns `-1` upon failure, so one should call `PyErr_Occurred`{.interpreted-text role="c:func"} to check for errors.
>
> ::: seealso
> The `PyUnicode_Equal`{.interpreted-text role="c:func"} function.
> :::

> Test if two strings are equal:
>
> - Return `1` if *a* is equal to *b*.
> - Return `0` if *a* is not equal to *b*.
> - Set a `TypeError`{.interpreted-text role="exc"} exception and return `-1` if *a* or *b* is not a `str`{.interpreted-text role="class"} object.
>
> The function always succeeds if *a* and *b* are `str`{.interpreted-text role="class"} objects.
>
> The function works for `str`{.interpreted-text role="class"} subclasses, but does not honor custom `__eq__()` method.
>
> ::: seealso
> The `PyUnicode_Compare`{.interpreted-text role="c:func"} function.
> :::
>
> ::: versionadded
> 3.14
> :::

> Compare a Unicode object with a char buffer which is interpreted as being UTF-8 or ASCII encoded and return true (`1`) if they are equal, or false (`0`) otherwise. If the Unicode object contains surrogate code points (`U+D800` - `U+DFFF`) or the C string is not valid UTF-8, false (`0`) is returned.
>
> This function does not raise exceptions.
>
> ::: versionadded
> 3.13
> :::

> Similar to `PyUnicode_EqualToUTF8AndSize`{.interpreted-text role="c:func"}, but compute *string* length using `!strlen`{.interpreted-text role="c:func"}. If the Unicode object contains null characters, false (`0`) is returned.
>
> ::: versionadded
> 3.13
> :::

> Compare a Unicode object, *unicode*, with *string* and return `-1`, `0`, `1` for less than, equal, and greater than, respectively. It is best to pass only ASCII-encoded strings, but the function interprets the input string as ISO-8859-1 if it contains non-ASCII characters.
>
> This function does not raise exceptions.

> Rich compare two Unicode strings and return one of the following:
>
> - `NULL` in case an exception was raised
> - `Py_True`{.interpreted-text role="c:data"} or `Py_False`{.interpreted-text role="c:data"} for successful comparisons
> - `Py_NotImplemented`{.interpreted-text role="c:data"} in case the type combination is unknown
>
> Possible values for *op* are `Py_GT`{.interpreted-text role="c:macro"}, `Py_GE`{.interpreted-text role="c:macro"}, `Py_EQ`{.interpreted-text role="c:macro"}, `Py_NE`{.interpreted-text role="c:macro"}, `Py_LT`{.interpreted-text role="c:macro"}, and `Py_LE`{.interpreted-text role="c:macro"}.

> Return a new string object from *format* and *args*; this is analogous to `format % args`.

> Check whether *substr* is contained in *unicode* and return true or false accordingly.
>
> *substr* has to coerce to a one element Unicode string. `-1` is returned if there was an error.

> Intern the argument `*p_unicode`{.interpreted-text role="c:expr"} in place. The argument must be the address of a pointer variable pointing to a Python Unicode string object. If there is an existing interned string that is the same as `*p_unicode`{.interpreted-text role="c:expr"}, it sets `*p_unicode`{.interpreted-text role="c:expr"} to it (releasing the reference to the old string object and creating a new `strong reference`{.interpreted-text role="term"} to the interned string object), otherwise it leaves `*p_unicode`{.interpreted-text role="c:expr"} alone and interns it.
>
> (Clarification: even though there is a lot of talk about references, think of this function as reference-neutral. You must own the object you pass in; after the call you no longer own the passed-in reference, but you newly own the result.)
>
> This function never raises an exception. On error, it leaves its argument unchanged without interning it.
>
> Instances of subclasses of `str`{.interpreted-text role="py:class"} may not be interned, that is, `PyUnicode_CheckExact(*p_unicode)`{.interpreted-text role="c:expr"} must be true. If it is not, then \-- as with any other error \-- the argument is left unchanged.
>
> Note that interned strings are not "immortal". You must keep a reference to the result to benefit from interning.

> A combination of `PyUnicode_FromString`{.interpreted-text role="c:func"} and `PyUnicode_InternInPlace`{.interpreted-text role="c:func"}, meant for statically allocated strings.
>
> Return a new (\"owned\") reference to either a new Unicode string object that has been interned, or an earlier interned string object with the same value.
>
> Python may keep a reference to the result, or make it `immortal`{.interpreted-text role="term"}, preventing it from being garbage-collected promptly. For interning an unbounded number of different strings, such as ones coming from user input, prefer calling `PyUnicode_FromString`{.interpreted-text role="c:func"} and `PyUnicode_InternInPlace`{.interpreted-text role="c:func"} directly.

> Return a non-zero value if *str* is interned, zero if not. The *str* argument must be a string; this is not checked. This function always succeeds.
>
> ::: impl-detail
> A non-zero return value may carry additional information about *how* the string is interned. The meaning of such non-zero values, as well as each specific string\'s intern-related details, may change between CPython versions.
> :::

## PyUnicodeWriter

The `PyUnicodeWriter`{.interpreted-text role="c:type"} API can be used to create a Python `str`{.interpreted-text role="class"} object.

::: versionadded
3.14
:::

> A Unicode writer instance.
>
> The instance must be destroyed by `PyUnicodeWriter_Finish`{.interpreted-text role="c:func"} on success, or `PyUnicodeWriter_Discard`{.interpreted-text role="c:func"} on error.

> Create a Unicode writer instance.
>
> *length* must be greater than or equal to `0`.
>
> If *length* is greater than `0`, preallocate an internal buffer of *length* characters.
>
> Set an exception and return `NULL` on error.

> Return the final Python `str`{.interpreted-text role="class"} object and destroy the writer instance.
>
> Set an exception and return `NULL` on error.
>
> The writer instance is invalid after this call.

> Discard the internal Unicode buffer and destroy the writer instance.
>
> If *writer* is `NULL`, no operation is performed.
>
> The writer instance is invalid after this call.

> Write the single Unicode character *ch* into *writer*.
>
> On success, return `0`. On error, set an exception, leave the writer unchanged, and return `-1`.

> Decode the string *str* from UTF-8 in strict mode and write the output into *writer*.
>
> *size* is the string length in bytes. If *size* is equal to `-1`, call `strlen(str)` to get the string length.
>
> On success, return `0`. On error, set an exception, leave the writer unchanged, and return `-1`.
>
> See also `PyUnicodeWriter_DecodeUTF8Stateful`{.interpreted-text role="c:func"}.

> Write the ASCII string *str* into *writer*.
>
> *size* is the string length in bytes. If *size* is equal to `-1`, call `strlen(str)` to get the string length.
>
> *str* must only contain ASCII characters. The behavior is undefined if *str* contains non-ASCII characters.
>
> On success, return `0`. On error, set an exception, leave the writer unchanged, and return `-1`.
>
> ::: versionadded
> 3.14
> :::

> Write the wide string *str* into *writer*.
>
> *size* is a number of wide characters. If *size* is equal to `-1`, call `wcslen(str)` to get the string length.
>
> On success, return `0`. On error, set an exception, leave the writer unchanged, and return `-1`.

> Writer the UCS4 string *str* into *writer*.
>
> *size* is a number of UCS4 characters.
>
> On success, return `0`. On error, set an exception, leave the writer unchanged, and return `-1`.

> Call `PyObject_Str`{.interpreted-text role="c:func"} on *obj* and write the output into *writer*.
>
> On success, return `0`. On error, set an exception, leave the writer unchanged, and return `-1`.

> Call `PyObject_Repr`{.interpreted-text role="c:func"} on *obj* and write the output into *writer*.
>
> On success, return `0`. On error, set an exception, leave the writer unchanged, and return `-1`.

> Write the substring `str[start:end]` into *writer*.
>
> *str* must be Python `str`{.interpreted-text role="class"} object. *start* must be greater than or equal to 0, and less than or equal to *end*. *end* must be less than or equal to *str* length.
>
> On success, return `0`. On error, set an exception, leave the writer unchanged, and return `-1`.

> Similar to `PyUnicode_FromFormat`{.interpreted-text role="c:func"}, but write the output directly into *writer*.
>
> On success, return `0`. On error, set an exception, leave the writer unchanged, and return `-1`.

> Decode the string *str* from UTF-8 with *errors* error handler and write the output into *writer*.
>
> *size* is the string length in bytes. If *size* is equal to `-1`, call `strlen(str)` to get the string length.
>
> *errors* is an `error handler <error-handlers>`{.interpreted-text role="ref"} name, such as `"replace"`. If *errors* is `NULL`, use the strict error handler.
>
> If *consumed* is not `NULL`, set *\*consumed* to the number of decoded bytes on success. If *consumed* is `NULL`, treat trailing incomplete UTF-8 byte sequences as an error.
>
> On success, return `0`. On error, set an exception, leave the writer unchanged, and return `-1`.
>
> See also `PyUnicodeWriter_WriteUTF8`{.interpreted-text role="c:func"}.

## Deprecated API

The following API is deprecated.

> This is a typedef of `wchar_t`{.interpreted-text role="c:type"}, which is a 16-bit type or 32-bit type depending on the platform. Please use `wchar_t`{.interpreted-text role="c:type"} directly instead.
>
> ::: versionchanged
> 3.3 In previous versions, this was a 16-bit type or a 32-bit type depending on whether you selected a \"narrow\" or \"wide\" Unicode version of Python at build time.
> :::
>
> ::: deprecated-removed
> 3.13 3.15
> :::

> Do nothing and return `0`. This API is kept only for backward compatibility, but there are no plans to remove it.
>
> ::: versionadded
> 3.3
> :::
>
> ::: deprecated
> 3.10 This API does nothing since Python 3.12. Previously, this needed to be called for each string created using the old API (`!PyUnicode_FromUnicode`{.interpreted-text role="c:func"} or similar).
> :::

> Do nothing and return `1`. This API is kept only for backward compatibility, but there are no plans to remove it.
>
> ::: versionadded
> 3.3
> :::
>
> ::: deprecated
> 3.14 This API does nothing since Python 3.12. Previously, this could be called to check if `PyUnicode_READY`{.interpreted-text role="c:func"} is necessary.
> :::
