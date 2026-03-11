# `!base64`{.interpreted-text role="mod"} \-\-- Base16, Base32, Base64, Base85 Data Encodings

::: {.module synopsis="RFC 4648: Base16, Base32, Base64 Data Encodings;
Base85 and Ascii85"}
base64
:::

**Source code:** `Lib/base64.py`{.interpreted-text role="source"}

::: index
pair: base64; encoding single: MIME; base64 encoding
:::

------------------------------------------------------------------------

This module provides functions for encoding binary data to printable ASCII characters and decoding such encodings back to binary data. This includes the `encodings specified in <base64-rfc-4648>`{.interpreted-text role="ref"} `4648`{.interpreted-text role="rfc"} (Base64, Base32 and Base16) and the non-standard `Base85 encodings <base64-base-85>`{.interpreted-text role="ref"}.

There are two interfaces provided by this module. The modern interface supports encoding `bytes-like objects <bytes-like object>`{.interpreted-text role="term"} to ASCII `bytes`{.interpreted-text role="class"}, and decoding `bytes-like objects <bytes-like object>`{.interpreted-text role="term"} or strings containing ASCII to `bytes`{.interpreted-text role="class"}. Both base-64 alphabets defined in `4648`{.interpreted-text role="rfc"} (normal, and URL- and filesystem-safe) are supported.

The `legacy interface <base64-legacy>`{.interpreted-text role="ref"} does not support decoding from strings, but it does provide functions for encoding and decoding to and from `file objects
<file object>`{.interpreted-text role="term"}. It only supports the Base64 standard alphabet, and it adds newlines every 76 characters as per `2045`{.interpreted-text role="rfc"}. Note that if you are looking for `2045`{.interpreted-text role="rfc"} support you probably want to be looking at the `email`{.interpreted-text role="mod"} package instead.

::: versionchanged
3.3 ASCII-only Unicode strings are now accepted by the decoding functions of the modern interface.
:::

::: versionchanged
3.4 Any `bytes-like objects <bytes-like object>`{.interpreted-text role="term"} are now accepted by all encoding and decoding functions in this module. Ascii85/Base85 support added.
:::

## RFC 4648 Encodings {#base64-rfc-4648}

The `4648`{.interpreted-text role="rfc"} encodings are suitable for encoding binary data so that it can be safely sent by email, used as parts of URLs, or included as part of an HTTP POST request.

:::: function
b64encode(s, altchars=None, \*, wrapcol=0)

Encode the `bytes-like object`{.interpreted-text role="term"} *s* using Base64 and return the encoded `bytes`{.interpreted-text role="class"}.

Optional *altchars* must be a `bytes-like object`{.interpreted-text role="term"} of length 2 which specifies an alternative alphabet for the `+` and `/` characters. This allows an application to e.g. generate URL or filesystem safe Base64 strings. The default is `None`, for which the standard Base64 alphabet is used.

If *wrapcol* is non-zero, insert a newline (`b'\n'`) character after at most every *wrapcol* characters. If *wrapcol* is zero (default), do not insert any newlines.

May assert or raise a `ValueError`{.interpreted-text role="exc"} if the length of *altchars* is not 2. Raises a `TypeError`{.interpreted-text role="exc"} if *altchars* is not a `bytes-like object`{.interpreted-text role="term"}.

::: versionchanged
3.15 Added the *wrapcol* parameter.
:::
::::

::::: function
b64decode(s, altchars=None, validate=False) b64decode(s, altchars=None, validate=True, \*, ignorechars)

Decode the Base64 encoded `bytes-like object`{.interpreted-text role="term"} or ASCII string *s* and return the decoded `bytes`{.interpreted-text role="class"}.

Optional *altchars* must be a `bytes-like object`{.interpreted-text role="term"} or ASCII string of length 2 which specifies the alternative alphabet used instead of the `+` and `/` characters.

A `binascii.Error`{.interpreted-text role="exc"} exception is raised if *s* is incorrectly padded.

If *ignorechars* is specified, it should be a `bytes-like object`{.interpreted-text role="term"} containing characters to ignore from the input when *validate* is true. If *ignorechars* contains the pad character `'='`, the pad characters presented before the end of the encoded data and the excess pad characters will be ignored. The default value of *validate* is `True` if *ignorechars* is specified, `False` otherwise.

If *validate* is false, characters that are neither in the normal base-64 alphabet nor (if *ignorechars* is not specified) the alternative alphabet are discarded prior to the padding check, but the `+` and `/` characters keep their meaning if they are not in *altchars* (they will be discarded in future Python versions).

If *validate* is true, these non-alphabet characters in the input result in a `binascii.Error`{.interpreted-text role="exc"}.

For more information about the strict base64 check, see `binascii.a2b_base64`{.interpreted-text role="func"}

::: versionchanged
3.15 Added the *ignorechars* parameter.
:::

::: deprecated
3.15 Accepting the `+` and `/` characters with an alternative alphabet is now deprecated.
:::
:::::

::: function
standard_b64encode(s)

Encode `bytes-like object`{.interpreted-text role="term"} *s* using the standard Base64 alphabet and return the encoded `bytes`{.interpreted-text role="class"}.
:::

::: function
standard_b64decode(s)

Decode `bytes-like object`{.interpreted-text role="term"} or ASCII string *s* using the standard Base64 alphabet and return the decoded `bytes`{.interpreted-text role="class"}.
:::

::: function
urlsafe_b64encode(s)

Encode `bytes-like object`{.interpreted-text role="term"} *s* using the URL- and filesystem-safe alphabet, which substitutes `-` instead of `+` and `_` instead of `/` in the standard Base64 alphabet, and return the encoded `bytes`{.interpreted-text role="class"}. The result can still contain `=`.
:::

:::: function
urlsafe_b64decode(s)

Decode `bytes-like object`{.interpreted-text role="term"} or ASCII string *s* using the URL- and filesystem-safe alphabet, which substitutes `-` instead of `+` and `_` instead of `/` in the standard Base64 alphabet, and return the decoded `bytes`{.interpreted-text role="class"}.

::: deprecated
3.15 Accepting the `+` and `/` characters is now deprecated.
:::
::::

::: function
b32encode(s)

Encode the `bytes-like object`{.interpreted-text role="term"} *s* using Base32 and return the encoded `bytes`{.interpreted-text role="class"}.
:::

::: function
b32decode(s, casefold=False, map01=None)

Decode the Base32 encoded `bytes-like object`{.interpreted-text role="term"} or ASCII string *s* and return the decoded `bytes`{.interpreted-text role="class"}.

Optional *casefold* is a flag specifying whether a lowercase alphabet is acceptable as input. For security purposes, the default is `False`.

`4648`{.interpreted-text role="rfc"} allows for optional mapping of the digit 0 (zero) to the letter O (oh), and for optional mapping of the digit 1 (one) to either the letter I (eye) or letter L (el). The optional argument *map01* when not `None`, specifies which letter the digit 1 should be mapped to (when *map01* is not `None`, the digit 0 is always mapped to the letter O). For security purposes the default is `None`, so that 0 and 1 are not allowed in the input.

A `binascii.Error`{.interpreted-text role="exc"} is raised if *s* is incorrectly padded or if there are non-alphabet characters present in the input.
:::

:::: function
b32hexencode(s)

Similar to `b32encode`{.interpreted-text role="func"} but uses the Extended Hex Alphabet, as defined in `4648`{.interpreted-text role="rfc"}.

::: versionadded
3.10
:::
::::

:::: function
b32hexdecode(s, casefold=False)

Similar to `b32decode`{.interpreted-text role="func"} but uses the Extended Hex Alphabet, as defined in `4648`{.interpreted-text role="rfc"}.

This version does not allow the digit 0 (zero) to the letter O (oh) and digit 1 (one) to either the letter I (eye) or letter L (el) mappings, all these characters are included in the Extended Hex Alphabet and are not interchangeable.

::: versionadded
3.10
:::
::::

::: function
b16encode(s)

Encode the `bytes-like object`{.interpreted-text role="term"} *s* using Base16 and return the encoded `bytes`{.interpreted-text role="class"}.
:::

::: function
b16decode(s, casefold=False)

Decode the Base16 encoded `bytes-like object`{.interpreted-text role="term"} or ASCII string *s* and return the decoded `bytes`{.interpreted-text role="class"}.

Optional *casefold* is a flag specifying whether a lowercase alphabet is acceptable as input. For security purposes, the default is `False`.

A `binascii.Error`{.interpreted-text role="exc"} is raised if *s* is incorrectly padded or if there are non-alphabet characters present in the input.
:::

## Base85 Encodings {#base64-base-85}

Base85 encoding is not formally specified but rather a de facto standard, thus different systems perform the encoding differently.

The `a85encode`{.interpreted-text role="func"} and `b85encode`{.interpreted-text role="func"} functions in this module are two implementations of the de facto standard. You should call the function with the Base85 implementation used by the software you intend to work with.

The two functions present in this module differ in how they handle the following:

- Whether to include enclosing `<~` and `~>` markers
- Whether to include newline characters
- The set of ASCII characters used for encoding
- Handling of null bytes

Refer to the documentation of the individual functions for more information.

:::: function
a85encode(b, \*, foldspaces=False, wrapcol=0, pad=False, adobe=False)

Encode the `bytes-like object`{.interpreted-text role="term"} *b* using Ascii85 and return the encoded `bytes`{.interpreted-text role="class"}.

*foldspaces* is an optional flag that uses the special short sequence \'y\' instead of 4 consecutive spaces (ASCII 0x20) as supported by \'btoa\'. This feature is not supported by the \"standard\" Ascii85 encoding.

If *wrapcol* is non-zero, insert a newline (`b'\n'`) character after at most every *wrapcol* characters. If *wrapcol* is zero (default), do not insert any newlines.

If *pad* is true, the input is padded with `b'\0'` so its length is a multiple of 4 bytes before encoding. Note that the `btoa` implementation always pads.

*adobe* controls whether the encoded byte sequence is framed with `<~` and `~>`, which is used by the Adobe implementation.

::: versionadded
3.4
:::
::::

:::: function
a85decode(b, \*, foldspaces=False, adobe=False, ignorechars=b\' tnrv\')

Decode the Ascii85 encoded `bytes-like object`{.interpreted-text role="term"} or ASCII string *b* and return the decoded `bytes`{.interpreted-text role="class"}.

*foldspaces* is a flag that specifies whether the \'y\' short sequence should be accepted as shorthand for 4 consecutive spaces (ASCII 0x20). This feature is not supported by the \"standard\" Ascii85 encoding.

*adobe* controls whether the input sequence is in Adobe Ascii85 format (i.e. is framed with \<\~ and \~\>).

*ignorechars* should be a `bytes-like object`{.interpreted-text role="term"} containing characters to ignore from the input. This should only contain whitespace characters, and by default contains all whitespace characters in ASCII.

::: versionadded
3.4
:::
::::

:::: function
b85encode(b, pad=False)

Encode the `bytes-like object`{.interpreted-text role="term"} *b* using base85 (as used in e.g. git-style binary diffs) and return the encoded `bytes`{.interpreted-text role="class"}.

If *pad* is true, the input is padded with `b'\0'` so its length is a multiple of 4 bytes before encoding.

::: versionadded
3.4
:::
::::

:::: function
b85decode(b)

Decode the base85-encoded `bytes-like object`{.interpreted-text role="term"} or ASCII string *b* and return the decoded `bytes`{.interpreted-text role="class"}. Padding is implicitly removed, if necessary.

::: versionadded
3.4
:::
::::

::::: function
z85encode(s, pad=False)

Encode the `bytes-like object`{.interpreted-text role="term"} *s* using Z85 (as used in ZeroMQ) and return the encoded `bytes`{.interpreted-text role="class"}. See [Z85 specification](https://rfc.zeromq.org/spec/32/) for more information.

If *pad* is true, the input is padded with `b'\0'` so its length is a multiple of 4 bytes before encoding.

::: versionadded
3.13
:::

::: versionchanged
3.15 The *pad* parameter was added.
:::
:::::

:::: function
z85decode(s)

Decode the Z85-encoded `bytes-like object`{.interpreted-text role="term"} or ASCII string *s* and return the decoded `bytes`{.interpreted-text role="class"}. See [Z85 specification](https://rfc.zeromq.org/spec/32/) for more information.

::: versionadded
3.13
:::
::::

## Legacy Interface {#base64-legacy}

::: function
decode(input, output)

Decode the contents of the binary *input* file and write the resulting binary data to the *output* file. *input* and *output* must be `file objects
<file object>`{.interpreted-text role="term"}. *input* will be read until `input.readline()` returns an empty bytes object.
:::

:::: function
decodebytes(s)

Decode the `bytes-like object`{.interpreted-text role="term"} *s*, which must contain one or more lines of base64 encoded data, and return the decoded `bytes`{.interpreted-text role="class"}.

::: versionadded
3.1
:::
::::

::: function
encode(input, output)

Encode the contents of the binary *input* file and write the resulting base64 encoded data to the *output* file. *input* and *output* must be `file
objects <file object>`{.interpreted-text role="term"}. *input* will be read until `input.read()` returns an empty bytes object. `encode`{.interpreted-text role="func"} inserts a newline character (`b'\n'`) after every 76 bytes of the output, as well as ensuring that the output always ends with a newline, as per `2045`{.interpreted-text role="rfc"} (MIME).
:::

:::: function
encodebytes(s)

Encode the `bytes-like object`{.interpreted-text role="term"} *s*, which can contain arbitrary binary data, and return `bytes`{.interpreted-text role="class"} containing the base64-encoded data, with newlines (`b'\n'`) inserted after every 76 bytes of output, and ensuring that there is a trailing newline, as per `2045`{.interpreted-text role="rfc"} (MIME).

::: versionadded
3.1
:::
::::

An example usage of the module:

> \>\>\> import base64 \>\>\> encoded = base64.b64encode(b\'data to be encoded\') \>\>\> encoded b\'ZGF0YSB0byBiZSBlbmNvZGVk\' \>\>\> data = base64.b64decode(encoded) \>\>\> data b\'data to be encoded\'

## Security Considerations {#base64-security}

A new security considerations section was added to `4648`{.interpreted-text role="rfc"} (section 12); it\'s recommended to review the security section for any code deployed to production.

::: seealso

Module `binascii`{.interpreted-text role="mod"}

:   Support module containing ASCII-to-binary and binary-to-ASCII conversions.

`1521`{.interpreted-text role="rfc"} - MIME (Multipurpose Internet Mail Extensions) Part One: Mechanisms for Specifying and Describing the Format of Internet Message Bodies

:   Section 5.2, \"Base64 Content-Transfer-Encoding,\" provides the definition of the base64 encoding.
:::
