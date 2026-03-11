# `!email.errors`{.interpreted-text role="mod"}: Exception and Defect classes

::: {.module synopsis="The exception classes used by the email package."}
email.errors
:::

**Source code:** `Lib/email/errors.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

The following exception classes are defined in the `!email.errors`{.interpreted-text role="mod"} module:

::: exception
MessageError()

This is the base class for all exceptions that the `email`{.interpreted-text role="mod"} package can raise. It is derived from the standard `Exception`{.interpreted-text role="exc"} class and defines no additional methods.
:::

::: exception
MessageParseError()

This is the base class for exceptions raised by the `~email.parser.Parser`{.interpreted-text role="class"} class. It is derived from `MessageError`{.interpreted-text role="exc"}. This class is also used internally by the parser used by `~email.headerregistry`{.interpreted-text role="mod"}.
:::

::: exception
HeaderParseError()

Raised under some error conditions when parsing the `5322`{.interpreted-text role="rfc"} headers of a message, this class is derived from `MessageParseError`{.interpreted-text role="exc"}. The `~email.message.EmailMessage.set_boundary`{.interpreted-text role="meth"} method will raise this error if the content type is unknown when the method is called. `~email.header.Header`{.interpreted-text role="class"} may raise this error for certain base64 decoding errors, and when an attempt is made to create a header that appears to contain an embedded header (that is, there is what is supposed to be a continuation line that has no leading whitespace and looks like a header).
:::

::: exception
BoundaryError()

Deprecated and no longer used.
:::

::: exception
MultipartConversionError()

Raised if the `~email.message.Message.attach`{.interpreted-text role="meth"} method is called on an instance of a class derived from `~email.mime.nonmultipart.MIMENonMultipart`{.interpreted-text role="class"} (e.g. `~email.mime.image.MIMEImage`{.interpreted-text role="class"}). `MultipartConversionError`{.interpreted-text role="exc"} multiply inherits from `MessageError`{.interpreted-text role="exc"} and the built-in `TypeError`{.interpreted-text role="exc"}.
:::

::: exception
HeaderWriteError()

Raised when an error occurs when the `~email.generator`{.interpreted-text role="mod"} outputs headers.
:::

::: exception
MessageDefect()

This is the base class for all defects found when parsing email messages. It is derived from `ValueError`{.interpreted-text role="exc"}.
:::

::: exception
HeaderDefect()

This is the base class for all defects found when parsing email headers. It is derived from `MessageDefect`{.interpreted-text role="exc"}.
:::

Here is the list of the defects that the `~email.parser.FeedParser`{.interpreted-text role="class"} can find while parsing messages. Note that the defects are added to the message where the problem was found, so for example, if a message nested inside a `multipart/alternative`{.interpreted-text role="mimetype"} had a malformed header, that nested message object would have a defect, but the containing messages would not.

All defect classes are subclassed from `email.errors.MessageDefect`{.interpreted-text role="class"}.

::: exception
NoBoundaryInMultipartDefect

A message claimed to be a multipart, but had no `boundary`{.interpreted-text role="mimetype"} parameter.
:::

::: exception
StartBoundaryNotFoundDefect

The start boundary claimed in the `Content-Type`{.interpreted-text role="mailheader"} header was never found.
:::

:::: exception
CloseBoundaryNotFoundDefect

A start boundary was found, but no corresponding close boundary was ever found.

::: versionadded
3.3
:::
::::

::: exception
FirstHeaderLineIsContinuationDefect

The message had a continuation line as its first header line.
:::

::: exception
MisplacedEnvelopeHeaderDefect

A \"Unix From\" header was found in the middle of a header block.
:::

:::: exception
MissingHeaderBodySeparatorDefect

A line was found while parsing headers that had no leading white space but contained no \':\'. Parsing continues assuming that the line represents the first line of the body.

::: versionadded
3.3
:::
::::

:::: exception
MalformedHeaderDefect

A header was found that was missing a colon, or was otherwise malformed.

::: deprecated
3.3 This defect has not been used for several Python versions.
:::
::::

::: exception
MultipartInvariantViolationDefect

A message claimed to be a `multipart`{.interpreted-text role="mimetype"}, but no subparts were found. Note that when a message has this defect, its `~email.message.Message.is_multipart`{.interpreted-text role="meth"} method may return `False` even though its content type claims to be `multipart`{.interpreted-text role="mimetype"}.
:::

::: exception
InvalidBase64PaddingDefect

When decoding a block of base64 encoded bytes, the padding was not correct. Enough padding is added to perform the decode, but the resulting decoded bytes may be invalid.
:::

::: exception
InvalidBase64CharactersDefect

When decoding a block of base64 encoded bytes, characters outside the base64 alphabet were encountered. The characters are ignored, but the resulting decoded bytes may be invalid.
:::

::: exception
InvalidBase64LengthDefect

When decoding a block of base64 encoded bytes, the number of non-padding base64 characters was invalid (1 more than a multiple of 4). The encoded block was kept as-is.
:::

::: exception
InvalidDateDefect

When decoding an invalid or unparsable date field. The original value is kept as-is.
:::
