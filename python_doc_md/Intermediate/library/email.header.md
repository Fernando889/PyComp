# `!email.header`{.interpreted-text role="mod"}: Internationalized headers

::: {.module synopsis="Representing non-ASCII headers"}
email.header
:::

**Source code:** `Lib/email/header.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

This module is part of the legacy (`Compat32`) email API. In the current API encoding and decoding of headers is handled transparently by the dictionary-like API of the `~email.message.EmailMessage`{.interpreted-text role="class"} class. In addition to uses in legacy code, this module can be useful in applications that need to completely control the character sets used when encoding headers.

The remaining text in this section is the original documentation of the module.

`2822`{.interpreted-text role="rfc"} is the base standard that describes the format of email messages. It derives from the older `822`{.interpreted-text role="rfc"} standard which came into widespread use at a time when most email was composed of ASCII characters only. `2822`{.interpreted-text role="rfc"} is a specification written assuming email contains only 7-bit ASCII characters.

Of course, as email has been deployed worldwide, it has become internationalized, such that language specific character sets can now be used in email messages. The base standard still requires email messages to be transferred using only 7-bit ASCII characters, so a slew of RFCs have been written describing how to encode email containing non-ASCII characters into `2822`{.interpreted-text role="rfc"}-compliant format. These RFCs include `2045`{.interpreted-text role="rfc"}, `2046`{.interpreted-text role="rfc"}, `2047`{.interpreted-text role="rfc"}, and `2231`{.interpreted-text role="rfc"}. The `email`{.interpreted-text role="mod"} package supports these standards in its `!email.header`{.interpreted-text role="mod"} and `email.charset`{.interpreted-text role="mod"} modules.

If you want to include non-ASCII characters in your email headers, say in the `Subject`{.interpreted-text role="mailheader"} or `To`{.interpreted-text role="mailheader"} fields, you should use the `Header`{.interpreted-text role="class"} class and assign the field in the `~email.message.Message`{.interpreted-text role="class"} object to an instance of `Header`{.interpreted-text role="class"} instead of using a string for the header value. Import the `Header`{.interpreted-text role="class"} class from the `!email.header`{.interpreted-text role="mod"} module. For example:

    >>> from email.message import Message
    >>> from email.header import Header
    >>> msg = Message()
    >>> h = Header('p\xf6stal', 'iso-8859-1')
    >>> msg['Subject'] = h
    >>> msg.as_string()
    'Subject: =?iso-8859-1?q?p=F6stal?=\n\n'

Notice here how we wanted the `Subject`{.interpreted-text role="mailheader"} field to contain a non-ASCII character? We did this by creating a `Header`{.interpreted-text role="class"} instance and passing in the character set that the byte string was encoded in. When the subsequent `~email.message.Message`{.interpreted-text role="class"} instance was flattened, the `Subject`{.interpreted-text role="mailheader"} field was properly `2047`{.interpreted-text role="rfc"} encoded. MIME-aware mail readers would show this header using the embedded ISO-8859-1 character.

Here is the `Header`{.interpreted-text role="class"} class description:

:::::::::: {.Header(s=None, .charset=None, .maxlinelen=None, .header_name=None, .continuation_ws=' .', .errors='strict')}
Create a MIME-compliant header that can contain strings in different character sets.

Optional *s* is the initial header value. If `None` (the default), the initial header value is not set. You can later append to the header with `append`{.interpreted-text role="meth"} method calls. *s* may be an instance of `bytes`{.interpreted-text role="class"} or `str`{.interpreted-text role="class"}, but see the `append`{.interpreted-text role="meth"} documentation for semantics.

Optional *charset* serves two purposes: it has the same meaning as the *charset* argument to the `append`{.interpreted-text role="meth"} method. It also sets the default character set for all subsequent `append`{.interpreted-text role="meth"} calls that omit the *charset* argument. If *charset* is not provided in the constructor (the default), the `us-ascii` character set is used both as *s*\'s initial charset and as the default for subsequent `append`{.interpreted-text role="meth"} calls.

The maximum line length can be specified explicitly via *maxlinelen*. For splitting the first line to a shorter value (to account for the field header which isn\'t included in *s*, e.g. `Subject`{.interpreted-text role="mailheader"}) pass in the name of the field in *header_name*. The default *maxlinelen* is 78, and the default value for *header_name* is `None`, meaning it is not taken into account for the first line of a long, split header.

Optional *continuation_ws* must be `2822`{.interpreted-text role="rfc"}-compliant folding whitespace, and is usually either a space or a hard tab character. This character will be prepended to continuation lines. *continuation_ws* defaults to a single space character.

Optional *errors* is passed straight through to the `append`{.interpreted-text role="meth"} method.

::: method
append(s, charset=None, errors=\'strict\')

Append the string *s* to the MIME header.

Optional *charset*, if given, should be a `~email.charset.Charset`{.interpreted-text role="class"} instance (see `email.charset`{.interpreted-text role="mod"}) or the name of a character set, which will be converted to a `~email.charset.Charset`{.interpreted-text role="class"} instance. A value of `None` (the default) means that the *charset* given in the constructor is used.

*s* may be an instance of `bytes`{.interpreted-text role="class"} or `str`{.interpreted-text role="class"}. If it is an instance of `bytes`{.interpreted-text role="class"}, then *charset* is the encoding of that byte string, and a `UnicodeError`{.interpreted-text role="exc"} will be raised if the string cannot be decoded with that character set.

If *s* is an instance of `str`{.interpreted-text role="class"}, then *charset* is a hint specifying the character set of the characters in the string.

In either case, when producing an `2822`{.interpreted-text role="rfc"}-compliant header using `2047`{.interpreted-text role="rfc"} rules, the string will be encoded using the output codec of the charset. If the string cannot be encoded using the output codec, a UnicodeError will be raised.

Optional *errors* is passed as the errors argument to the decode call if *s* is a byte string.
:::

:::: method
encode(splitchars=\';, t\', maxlinelen=None, linesep=\'n\')

Encode a message header into an RFC-compliant format, possibly wrapping long lines and encapsulating non-ASCII parts in base64 or quoted-printable encodings.

Optional *splitchars* is a string containing characters which should be given extra weight by the splitting algorithm during normal header wrapping. This is in very rough support of [RFC 2822](http://www.faqs.org/rfcs/rfc2822.html "RFC 2822")\'s \'higher level syntactic breaks\': split points preceded by a splitchar are preferred during line splitting, with the characters preferred in the order in which they appear in the string. Space and tab may be included in the string to indicate whether preference should be given to one over the other as a split point when other split chars do not appear in the line being split. Splitchars does not affect [RFC 2047](http://www.faqs.org/rfcs/rfc2047.html "RFC 2047") encoded lines.

*maxlinelen*, if given, overrides the instance\'s value for the maximum line length.

*linesep* specifies the characters used to separate the lines of the folded header. It defaults to the most useful value for Python application code (`\n`), but `\r\n` can be specified in order to produce headers with RFC-compliant line separators.

::: versionchanged
3.2 Added the *linesep* argument.
:::
::::

The `Header`{.interpreted-text role="class"} class also provides a number of methods to support standard operators and built-in functions.

:::: method
\_\_str\_\_()

Returns an approximation of the `Header`{.interpreted-text role="class"} as a string, using an unlimited line length. All pieces are converted to unicode using the specified encoding and joined together appropriately. Any pieces with a charset of `'unknown-8bit'` are decoded as ASCII using the `'replace'` error handler.

::: versionchanged
3.2 Added handling for the `'unknown-8bit'` charset.
:::
::::

::: method
\_\_eq\_\_(other)

This method allows you to compare two `Header`{.interpreted-text role="class"} instances for equality.
:::

::: method
\_\_ne\_\_(other)

This method allows you to compare two `Header`{.interpreted-text role="class"} instances for inequality.
:::
::::::::::

The `!email.header`{.interpreted-text role="mod"} module also provides the following convenient functions.

::::: function
decode_header(header)

Decode a message header value without converting the character set. The header value is in *header*.

For historical reasons, this function may return either:

1.  A list of pairs containing each of the decoded parts of the header, `(decoded_bytes, charset)`, where *decoded_bytes* is always an instance of `bytes`{.interpreted-text role="class"}, and *charset* is either:

    > - A lower case string containing the name of the character set specified.
    > - `None` for non-encoded parts of the header.

2.  A list of length 1 containing a pair `(string, None)`, where *string* is always an instance of `str`{.interpreted-text role="class"}.

An `email.errors.HeaderParseError`{.interpreted-text role="exc"} may be raised when certain decoding errors occur (e.g. a base64 decoding exception).

Here are examples:

> \>\>\> from email.header import decode_header \>\>\> decode_header(\'=?iso-8859-1?q?p=F6stal?=\') \[(b\'pxf6stal\', \'iso-8859-1\')\] \>\>\> decode_header(\'unencoded_string\') \[(\'unencoded_string\', None)\] \>\>\> decode_header(\'bar =?utf-8?B?ZsOzbw==?=\') \[(b\'bar \', None), (b\'fxc3xb3o\', \'utf-8\')\]

:::: note
::: title
Note
:::

This function exists for backwards compatibility only. For new code, we recommend using `email.headerregistry.HeaderRegistry`{.interpreted-text role="class"}.
::::
:::::

::::: function
make_header(decoded_seq, maxlinelen=None, header_name=None, continuation_ws=\' \')

Create a `Header`{.interpreted-text role="class"} instance from a sequence of pairs as returned by `decode_header`{.interpreted-text role="func"}.

`decode_header`{.interpreted-text role="func"} takes a header value string and returns a sequence of pairs of the format `(decoded_string, charset)` where *charset* is the name of the character set.

This function takes one of those sequence of pairs and returns a `Header`{.interpreted-text role="class"} instance. Optional *maxlinelen*, *header_name*, and *continuation_ws* are as in the `Header`{.interpreted-text role="class"} constructor.

:::: note
::: title
Note
:::

This function exists for backwards compatibility only, and is not recommended for use in new code.
::::
:::::
