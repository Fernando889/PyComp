# `!email.parser`{.interpreted-text role="mod"}: Parsing email messages

::: {.module synopsis="Parse flat text email messages to produce a message object structure."}
email.parser
:::

**Source code:** `Lib/email/parser.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

Message object structures can be created in one of two ways: they can be created from whole cloth by creating an `~email.message.EmailMessage`{.interpreted-text role="class"} object, adding headers using the dictionary interface, and adding payload(s) using `~email.message.EmailMessage.set_content`{.interpreted-text role="meth"} and related methods, or they can be created by parsing a serialized representation of the email message.

The `email`{.interpreted-text role="mod"} package provides a standard parser that understands most email document structures, including MIME documents. You can pass the parser a bytes, string or file object, and the parser will return to you the root `~email.message.EmailMessage`{.interpreted-text role="class"} instance of the object structure. For simple, non-MIME messages the payload of this root object will likely be a string containing the text of the message. For MIME messages, the root object will return `True` from its `~email.message.EmailMessage.is_multipart`{.interpreted-text role="meth"} method, and the subparts can be accessed via the payload manipulation methods, such as `~email.message.EmailMessage.get_body`{.interpreted-text role="meth"}, `~email.message.EmailMessage.iter_parts`{.interpreted-text role="meth"}, and `~email.message.EmailMessage.walk`{.interpreted-text role="meth"}.

There are actually two parser interfaces available for use, the `Parser`{.interpreted-text role="class"} API and the incremental `FeedParser`{.interpreted-text role="class"} API. The `Parser`{.interpreted-text role="class"} API is most useful if you have the entire text of the message in memory, or if the entire message lives in a file on the file system. `FeedParser`{.interpreted-text role="class"} is more appropriate when you are reading the message from a stream which might block waiting for more input (such as reading an email message from a socket). The `FeedParser`{.interpreted-text role="class"} can consume and parse the message incrementally, and only returns the root object when you close the parser.

Note that the parser can be extended in limited ways, and of course you can implement your own parser completely from scratch. All of the logic that connects the `email`{.interpreted-text role="mod"} package\'s bundled parser and the `~email.message.EmailMessage`{.interpreted-text role="class"} class is embodied in the `~email.policy.Policy`{.interpreted-text role="class"} class, so a custom parser can create message object trees any way it finds necessary by implementing custom versions of the appropriate `!Policy`{.interpreted-text role="class"} methods.

## FeedParser API

The `BytesFeedParser`{.interpreted-text role="class"}, imported from the `email.feedparser`{.interpreted-text role="mod"} module, provides an API that is conducive to incremental parsing of email messages, such as would be necessary when reading the text of an email message from a source that can block (such as a socket). The `BytesFeedParser`{.interpreted-text role="class"} can of course be used to parse an email message fully contained in a `bytes-like
object`{.interpreted-text role="term"}, string, or file, but the `BytesParser`{.interpreted-text role="class"} API may be more convenient for such use cases. The semantics and results of the two parser APIs are identical.

The `BytesFeedParser`{.interpreted-text role="class"}\'s API is simple; you create an instance, feed it a bunch of bytes until there\'s no more to feed it, then close the parser to retrieve the root message object. The `BytesFeedParser`{.interpreted-text role="class"} is extremely accurate when parsing standards-compliant messages, and it does a very good job of parsing non-compliant messages, providing information about how a message was deemed broken. It will populate a message object\'s `~email.message.EmailMessage.defects`{.interpreted-text role="attr"} attribute with a list of any problems it found in a message. See the `email.errors`{.interpreted-text role="mod"} module for the list of defects that it can find.

Here is the API for the `BytesFeedParser`{.interpreted-text role="class"}:

:::::::: {.BytesFeedParser(_factory=None, .*, .policy=policy.compat32)}
Create a `BytesFeedParser`{.interpreted-text role="class"} instance. Optional *\_factory* is a no-argument callable; if not specified use the `~email.policy.Policy.message_factory`{.interpreted-text role="attr"} from the *policy*. Call *\_factory* whenever a new message object is needed.

If *policy* is specified use the rules it specifies to update the representation of the message. If *policy* is not set, use the `compat32 <email.policy.Compat32>`{.interpreted-text role="class"} policy, which maintains backward compatibility with the Python 3.2 version of the email package and provides `~email.message.Message`{.interpreted-text role="class"} as the default factory. All other policies provide `~email.message.EmailMessage`{.interpreted-text role="class"} as the default *\_factory*. For more information on what else *policy* controls, see the `~email.policy`{.interpreted-text role="mod"} documentation.

Note: **The policy keyword should always be specified**; The default will change to `email.policy.default`{.interpreted-text role="data"} in a future version of Python.

::: versionadded
3.2
:::

::: versionchanged
3.3 Added the *policy* keyword.
:::

::: versionchanged
3.6 *\_factory* defaults to the policy `message_factory`.
:::

::: method
feed(data)

Feed the parser some more data. *data* should be a `bytes-like
object`{.interpreted-text role="term"} containing one or more lines. The lines can be partial and the parser will stitch such partial lines together properly. The lines can have any of the three common line endings: carriage return, newline, or carriage return and newline (they can even be mixed).
:::

::: method
close()

Complete the parsing of all previously fed data and return the root message object. It is undefined what happens if `~feed`{.interpreted-text role="meth"} is called after this method has been called.
:::
::::::::

:::: {.FeedParser(_factory=None, .*, .policy=policy.compat32)}
Works like `BytesFeedParser`{.interpreted-text role="class"} except that the input to the `~BytesFeedParser.feed`{.interpreted-text role="meth"} method must be a string. This is of limited utility, since the only way for such a message to be valid is for it to contain only ASCII text or, if `~email.policy.EmailPolicy.utf8`{.interpreted-text role="attr"} is `True`, no binary attachments.

::: versionchanged
3.3 Added the *policy* keyword.
:::
::::

## Parser API

The `BytesParser`{.interpreted-text role="class"} class, imported from the `!email.parser`{.interpreted-text role="mod"} module, provides an API that can be used to parse a message when the complete contents of the message are available in a `bytes-like object`{.interpreted-text role="term"} or file. The `!email.parser`{.interpreted-text role="mod"} module also provides `Parser`{.interpreted-text role="class"} for parsing strings, and header-only parsers, `BytesHeaderParser`{.interpreted-text role="class"} and `HeaderParser`{.interpreted-text role="class"}, which can be used if you\'re only interested in the headers of the message. `BytesHeaderParser`{.interpreted-text role="class"} and `HeaderParser`{.interpreted-text role="class"} can be much faster in these situations, since they do not attempt to parse the message body, instead setting the payload to the raw body.

:::::::: {.BytesParser(_class=None, .*, .policy=policy.compat32)}
Create a `BytesParser`{.interpreted-text role="class"} instance. The *\_class* and *policy* arguments have the same meaning and semantics as the *\_factory* and *policy* arguments of `BytesFeedParser`{.interpreted-text role="class"}.

Note: **The policy keyword should always be specified**; The default will change to `email.policy.default`{.interpreted-text role="data"} in a future version of Python.

::: versionchanged
3.3 Removed the *strict* argument that was deprecated in 2.4. Added the *policy* keyword.
:::

::: versionchanged
3.6 *\_class* defaults to the policy `message_factory`.
:::

::: method
parse(fp, headersonly=False)

Read all the data from the binary file-like object *fp*, parse the resulting bytes, and return the message object. *fp* must support both the `~io.IOBase.readline`{.interpreted-text role="meth"} and the `~io.IOBase.read`{.interpreted-text role="meth"} methods.

The bytes contained in *fp* must be formatted as a block of `5322`{.interpreted-text role="rfc"} (or, if `~email.policy.EmailPolicy.utf8`{.interpreted-text role="attr"} is `True`, `6532`{.interpreted-text role="rfc"}) style headers and header continuation lines, optionally preceded by an envelope header. The header block is terminated either by the end of the data or by a blank line. Following the header block is the body of the message (which may contain MIME-encoded subparts, including subparts with a `Content-Transfer-Encoding`{.interpreted-text role="mailheader"} of `8bit`).

Optional *headersonly* is a flag specifying whether to stop parsing after reading the headers or not. The default is `False`, meaning it parses the entire contents of the file.
:::

::: method
parsebytes(bytes, headersonly=False)

Similar to the `parse`{.interpreted-text role="meth"} method, except it takes a `bytes-like
object`{.interpreted-text role="term"} instead of a file-like object. Calling this method on a `bytes-like object`{.interpreted-text role="term"} is equivalent to wrapping *bytes* in a `~io.BytesIO`{.interpreted-text role="class"} instance first and calling `parse`{.interpreted-text role="meth"}.

Optional *headersonly* is as with the `parse`{.interpreted-text role="meth"} method.
:::

::: versionadded
3.2
:::
::::::::

:::: {.BytesHeaderParser(_class=None, .*, .policy=policy.compat32)}
Exactly like `BytesParser`{.interpreted-text role="class"}, except that *headersonly* defaults to `True`.

::: versionadded
3.3
:::
::::

::::::: {.Parser(_class=None, .*, .policy=policy.compat32)}
This class is parallel to `BytesParser`{.interpreted-text role="class"}, but handles string input.

::: versionchanged
3.3 Removed the *strict* argument. Added the *policy* keyword.
:::

::: versionchanged
3.6 *\_class* defaults to the policy `message_factory`.
:::

::: method
parse(fp, headersonly=False)

Read all the data from the text-mode file-like object *fp*, parse the resulting text, and return the root message object. *fp* must support both the `~io.TextIOBase.readline`{.interpreted-text role="meth"} and the `~io.TextIOBase.read`{.interpreted-text role="meth"} methods on file-like objects.

Other than the text mode requirement, this method operates like `BytesParser.parse`{.interpreted-text role="meth"}.
:::

::: method
parsestr(text, headersonly=False)

Similar to the `parse`{.interpreted-text role="meth"} method, except it takes a string object instead of a file-like object. Calling this method on a string is equivalent to wrapping *text* in a `~io.StringIO`{.interpreted-text role="class"} instance first and calling `parse`{.interpreted-text role="meth"}.

Optional *headersonly* is as with the `parse`{.interpreted-text role="meth"} method.
:::
:::::::

::: {.HeaderParser(_class=None, .*, .policy=policy.compat32)}
Exactly like `Parser`{.interpreted-text role="class"}, except that *headersonly* defaults to `True`.
:::

Since creating a message object structure from a string or a file object is such a common task, four functions are provided as a convenience. They are available in the top-level `email`{.interpreted-text role="mod"} package namespace.

::: currentmodule
email
:::

::::: function
message_from_bytes(s, [class]{#class}=None, \*, policy=policy.compat32)

Return a message object structure from a `bytes-like object`{.interpreted-text role="term"}. This is equivalent to `BytesParser().parsebytes(s)`. Optional *\_class* and *policy* are interpreted as with the `~email.parser.BytesParser`{.interpreted-text role="class"} class constructor.

::: versionadded
3.2
:::

::: versionchanged
3.3 Removed the *strict* argument. Added the *policy* keyword.
:::
:::::

::::: function
message_from_binary_file(fp, [class]{#class}=None, \*, policy=policy.compat32)

Return a message object structure tree from an open binary `file
object`{.interpreted-text role="term"}. This is equivalent to `BytesParser().parse(fp)`. *\_class* and *policy* are interpreted as with the `~email.parser.BytesParser`{.interpreted-text role="class"} class constructor.

::: versionadded
3.2
:::

::: versionchanged
3.3 Removed the *strict* argument. Added the *policy* keyword.
:::
:::::

:::: function
message_from_string(s, [class]{#class}=None, \*, policy=policy.compat32)

Return a message object structure from a string. This is equivalent to `Parser().parsestr(s)`. *\_class* and *policy* are interpreted as with the `~email.parser.Parser`{.interpreted-text role="class"} class constructor.

::: versionchanged
3.3 Removed the *strict* argument. Added the *policy* keyword.
:::
::::

::::: function
message_from_file(fp, [class]{#class}=None, \*, policy=policy.compat32)

Return a message object structure tree from an open `file object`{.interpreted-text role="term"}. This is equivalent to `Parser().parse(fp)`. *\_class* and *policy* are interpreted as with the `~email.parser.Parser`{.interpreted-text role="class"} class constructor.

::: versionchanged
3.3 Removed the *strict* argument. Added the *policy* keyword.
:::

::: versionchanged
3.6 *\_class* defaults to the policy `message_factory`.
:::
:::::

Here\'s an example of how you might use `message_from_bytes`{.interpreted-text role="func"} at an interactive Python prompt:

    >>> import email
    >>> msg = email.message_from_bytes(myBytes)  # doctest: +SKIP

## Additional notes

Here are some notes on the parsing semantics:

- Most non-`multipart`{.interpreted-text role="mimetype"} type messages are parsed as a single message object with a string payload. These objects will return `False` for `~email.message.EmailMessage.is_multipart`{.interpreted-text role="meth"}, and `~email.message.EmailMessage.iter_parts`{.interpreted-text role="meth"} will yield an empty list.
- All `multipart`{.interpreted-text role="mimetype"} type messages will be parsed as a container message object with a list of sub-message objects for their payload. The outer container message will return `True` for `~email.message.EmailMessage.is_multipart`{.interpreted-text role="meth"}, and `~email.message.EmailMessage.iter_parts`{.interpreted-text role="meth"} will yield a list of subparts.
- Most messages with a content type of `message/\*`{.interpreted-text role="mimetype"} (such as `message/delivery-status`{.interpreted-text role="mimetype"} and `message/rfc822`{.interpreted-text role="mimetype"}) will also be parsed as container object containing a list payload of length 1. Their `~email.message.EmailMessage.is_multipart`{.interpreted-text role="meth"} method will return `True`. The single element yielded by `~email.message.EmailMessage.iter_parts`{.interpreted-text role="meth"} will be a sub-message object.
- Some non-standards-compliant messages may not be internally consistent about their `multipart`{.interpreted-text role="mimetype"}-edness. Such messages may have a `Content-Type`{.interpreted-text role="mailheader"} header of type `multipart`{.interpreted-text role="mimetype"}, but their `~email.message.EmailMessage.is_multipart`{.interpreted-text role="meth"} method may return `False`. If such messages were parsed with the `~email.parser.FeedParser`{.interpreted-text role="class"}, they will have an instance of the `~email.errors.MultipartInvariantViolationDefect`{.interpreted-text role="class"} class in their *defects* attribute list. See `email.errors`{.interpreted-text role="mod"} for details.
