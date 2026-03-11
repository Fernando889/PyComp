# `!email.generator`{.interpreted-text role="mod"}: Generating MIME documents

::: {.module synopsis="Generate flat text email messages from a message structure."}
email.generator
:::

**Source code:** `Lib/email/generator.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

One of the most common tasks is to generate the flat (serialized) version of the email message represented by a message object structure. You will need to do this if you want to send your message via `smtplib.SMTP.sendmail`{.interpreted-text role="meth"}, or print the message on the console. Taking a message object structure and producing a serialized representation is the job of the generator classes.

As with the `email.parser`{.interpreted-text role="mod"} module, you aren\'t limited to the functionality of the bundled generator; you could write one from scratch yourself. However the bundled generator knows how to generate most email in a standards-compliant way, should handle MIME and non-MIME email messages just fine, and is designed so that the bytes-oriented parsing and generation operations are inverses, assuming the same non-transforming `~email.policy`{.interpreted-text role="mod"} is used for both. That is, parsing the serialized byte stream via the `~email.parser.BytesParser`{.interpreted-text role="class"} class and then regenerating the serialized byte stream using `BytesGenerator`{.interpreted-text role="class"} should produce output identical to the input[^1]. (On the other hand, using the generator on an `~email.message.EmailMessage`{.interpreted-text role="class"} constructed by program may result in changes to the `~email.message.EmailMessage`{.interpreted-text role="class"} object as defaults are filled in.)

The `Generator`{.interpreted-text role="class"} class can be used to flatten a message into a text (as opposed to binary) serialized representation, but since Unicode cannot represent binary data directly, the message is of necessity transformed into something that contains only ASCII characters, using the standard email RFC Content Transfer Encoding techniques for encoding email messages for transport over channels that are not \"8 bit clean\".

To accommodate reproducible processing of SMIME-signed messages `Generator`{.interpreted-text role="class"} disables header folding for message parts of type `multipart/signed` and all subparts.

::::::::: {.BytesGenerator(outfp, .mangle_from_=None, .maxheaderlen=None, .*, .\\ .policy=None)}
Return a `BytesGenerator`{.interpreted-text role="class"} object that will write any message provided to the `flatten`{.interpreted-text role="meth"} method, or any surrogateescape encoded text provided to the `write`{.interpreted-text role="meth"} method, to the `file-like object`{.interpreted-text role="term"} *outfp*. *outfp* must support a `write` method that accepts binary data.

If optional *mangle_from\_* is `True`, put a `>` character in front of any line in the body that starts with the exact string `"From "`, that is `From` followed by a space at the beginning of a line. *mangle_from\_* defaults to the value of the `~email.policy.Policy.mangle_from_`{.interpreted-text role="attr"} setting of the *policy* (which is `True` for the `~email.policy.compat32`{.interpreted-text role="data"} policy and `False` for all others). *mangle_from\_* is intended for use when messages are stored in Unix mbox format (see `mailbox`{.interpreted-text role="mod"} and [WHY THE CONTENT-LENGTH FORMAT IS BAD](https://www.jwz.org/doc/content-length.html)).

If *maxheaderlen* is not `None`, refold any header lines that are longer than *maxheaderlen*, or if `0`, do not rewrap any headers. If *manheaderlen* is `None` (the default), wrap headers and other message lines according to the *policy* settings.

If *policy* is specified, use that policy to control message generation. If *policy* is `None` (the default), use the policy associated with the `~email.message.Message`{.interpreted-text role="class"} or `~email.message.EmailMessage`{.interpreted-text role="class"} object passed to `flatten` to control the message generation. See `email.policy`{.interpreted-text role="mod"} for details on what *policy* controls.

::: versionadded
3.2
:::

::: versionchanged
3.3 Added the *policy* keyword.
:::

::: versionchanged
3.6 The default behavior of the *mangle_from\_* and *maxheaderlen* parameters is to follow the policy.
:::

::: method
flatten(msg, unixfrom=False, linesep=None)

Print the textual representation of the message object structure rooted at *msg* to the output file specified when the `BytesGenerator`{.interpreted-text role="class"} instance was created.

If the `~email.policy`{.interpreted-text role="mod"} option `~email.policy.Policy.cte_type`{.interpreted-text role="attr"} is `8bit` (the default), copy any headers in the original parsed message that have not been modified to the output with any bytes with the high bit set reproduced as in the original, and preserve the non-ASCII `Content-Transfer-Encoding`{.interpreted-text role="mailheader"} of any body parts that have them. If `cte_type` is `7bit`, convert the bytes with the high bit set as needed using an ASCII-compatible `Content-Transfer-Encoding`{.interpreted-text role="mailheader"}. That is, transform parts with non-ASCII `Content-Transfer-Encoding`{.interpreted-text role="mailheader"} (`Content-Transfer-Encoding: 8bit`{.interpreted-text role="mailheader"}) to an ASCII compatible `Content-Transfer-Encoding`{.interpreted-text role="mailheader"}, and encode RFC-invalid non-ASCII bytes in headers using the MIME `unknown-8bit` character set, thus rendering them RFC-compliant.

If *unixfrom* is `True`, print the envelope header delimiter used by the Unix mailbox format (see `mailbox`{.interpreted-text role="mod"}) before the first of the `5322`{.interpreted-text role="rfc"} headers of the root message object. If the root object has no envelope header, craft a standard one. The default is `False`. Note that for subparts, no envelope header is ever printed.

If *linesep* is not `None`, use it as the separator character between all the lines of the flattened message. If *linesep* is `None` (the default), use the value specified in the *policy*.
:::

::: method
clone(fp)

Return an independent clone of this `BytesGenerator`{.interpreted-text role="class"} instance with the exact same option settings, and *fp* as the new *outfp*.
:::

::: method
write(s)

Encode *s* using the `ASCII` codec and the `surrogateescape` error handler, and pass it to the *write* method of the *outfp* passed to the `BytesGenerator`{.interpreted-text role="class"}\'s constructor.
:::
:::::::::

As a convenience, `~email.message.EmailMessage`{.interpreted-text role="class"} provides the methods `~email.message.EmailMessage.as_bytes`{.interpreted-text role="meth"} and `bytes(aMessage)` (a.k.a. `~email.message.EmailMessage.__bytes__`{.interpreted-text role="meth"}), which simplify the generation of a serialized binary representation of a message object. For more detail, see `email.message`{.interpreted-text role="mod"}.

Because strings cannot represent binary data, the `Generator`{.interpreted-text role="class"} class must convert any binary data in any message it flattens to an ASCII compatible format, by converting them to an ASCII compatible `Content-Transfer_Encoding`{.interpreted-text role="mailheader"}. Using the terminology of the email RFCs, you can think of this as `Generator`{.interpreted-text role="class"} serializing to an I/O stream that is not \"8 bit clean\". In other words, most applications will want to be using `BytesGenerator`{.interpreted-text role="class"}, and not `Generator`{.interpreted-text role="class"}.

::::::::: {.Generator(outfp, .mangle_from_=None, .maxheaderlen=None, .*, .\\ .policy=None)}
Return a `Generator`{.interpreted-text role="class"} object that will write any message provided to the `flatten`{.interpreted-text role="meth"} method, or any text provided to the `write`{.interpreted-text role="meth"} method, to the `file-like object`{.interpreted-text role="term"} *outfp*. *outfp* must support a `write` method that accepts string data.

If optional *mangle_from\_* is `True`, put a `>` character in front of any line in the body that starts with the exact string `"From "`, that is `From` followed by a space at the beginning of a line. *mangle_from\_* defaults to the value of the `~email.policy.Policy.mangle_from_`{.interpreted-text role="attr"} setting of the *policy* (which is `True` for the `~email.policy.compat32`{.interpreted-text role="data"} policy and `False` for all others). *mangle_from\_* is intended for use when messages are stored in Unix mbox format (see `mailbox`{.interpreted-text role="mod"} and [WHY THE CONTENT-LENGTH FORMAT IS BAD](https://www.jwz.org/doc/content-length.html)).

If *maxheaderlen* is not `None`, refold any header lines that are longer than *maxheaderlen*, or if `0`, do not rewrap any headers. If *manheaderlen* is `None` (the default), wrap headers and other message lines according to the *policy* settings.

If *policy* is specified, use that policy to control message generation. If *policy* is `None` (the default), use the policy associated with the `~email.message.Message`{.interpreted-text role="class"} or `~email.message.EmailMessage`{.interpreted-text role="class"} object passed to `flatten` to control the message generation. See `email.policy`{.interpreted-text role="mod"} for details on what *policy* controls.

::: versionchanged
3.3 Added the *policy* keyword.
:::

::: versionchanged
3.6 The default behavior of the *mangle_from\_* and *maxheaderlen* parameters is to follow the policy.
:::

:::: method
flatten(msg, unixfrom=False, linesep=None)

Print the textual representation of the message object structure rooted at *msg* to the output file specified when the `Generator`{.interpreted-text role="class"} instance was created.

If the `~email.policy`{.interpreted-text role="mod"} option `~email.policy.Policy.cte_type`{.interpreted-text role="attr"} is `8bit`, generate the message as if the option were set to `7bit`. (This is required because strings cannot represent non-ASCII bytes.) Convert any bytes with the high bit set as needed using an ASCII-compatible `Content-Transfer-Encoding`{.interpreted-text role="mailheader"}. That is, transform parts with non-ASCII `Content-Transfer-Encoding`{.interpreted-text role="mailheader"} (`Content-Transfer-Encoding: 8bit`{.interpreted-text role="mailheader"}) to an ASCII compatible `Content-Transfer-Encoding`{.interpreted-text role="mailheader"}, and encode RFC-invalid non-ASCII bytes in headers using the MIME `unknown-8bit` character set, thus rendering them RFC-compliant.

If *unixfrom* is `True`, print the envelope header delimiter used by the Unix mailbox format (see `mailbox`{.interpreted-text role="mod"}) before the first of the `5322`{.interpreted-text role="rfc"} headers of the root message object. If the root object has no envelope header, craft a standard one. The default is `False`. Note that for subparts, no envelope header is ever printed.

If *linesep* is not `None`, use it as the separator character between all the lines of the flattened message. If *linesep* is `None` (the default), use the value specified in the *policy*.

::: versionchanged
3.2 Added support for re-encoding `8bit` message bodies, and the *linesep* argument.
:::
::::

::: method
clone(fp)

Return an independent clone of this `Generator`{.interpreted-text role="class"} instance with the exact same options, and *fp* as the new *outfp*.
:::

::: method
write(s)

Write *s* to the *write* method of the *outfp* passed to the `Generator`{.interpreted-text role="class"}\'s constructor. This provides just enough file-like API for `Generator`{.interpreted-text role="class"} instances to be used in the `print`{.interpreted-text role="func"} function.
:::
:::::::::

As a convenience, `~email.message.EmailMessage`{.interpreted-text role="class"} provides the methods `~email.message.EmailMessage.as_string`{.interpreted-text role="meth"} and `str(aMessage)` (a.k.a. `~email.message.EmailMessage.__str__`{.interpreted-text role="meth"}), which simplify the generation of a formatted string representation of a message object. For more detail, see `email.message`{.interpreted-text role="mod"}.

The `!email.generator`{.interpreted-text role="mod"} module also provides a derived class, `DecodedGenerator`{.interpreted-text role="class"}, which is like the `Generator`{.interpreted-text role="class"} base class, except that non-`text`{.interpreted-text role="mimetype"} parts are not serialized, but are instead represented in the output stream by a string derived from a template filled in with information about the part.

::: {.DecodedGenerator(outfp, .mangle_from_=None, .maxheaderlen=None, .\\ .fmt=None, .*, .policy=None)}
Act like `Generator`{.interpreted-text role="class"}, except that for any subpart of the message passed to `Generator.flatten`{.interpreted-text role="meth"}, if the subpart is of main type `text`{.interpreted-text role="mimetype"}, print the decoded payload of the subpart, and if the main type is not `text`{.interpreted-text role="mimetype"}, instead of printing it fill in the string *fmt* using information from the part and print the resulting filled-in string.

To fill in *fmt*, execute `fmt % part_info`, where `part_info` is a dictionary composed of the following keys and values:

- `type` \-- Full MIME type of the non-`text`{.interpreted-text role="mimetype"} part
- `maintype` \-- Main MIME type of the non-`text`{.interpreted-text role="mimetype"} part
- `subtype` \-- Sub-MIME type of the non-`text`{.interpreted-text role="mimetype"} part
- `filename` \-- Filename of the non-`text`{.interpreted-text role="mimetype"} part
- `description` \-- Description associated with the non-`text`{.interpreted-text role="mimetype"} part
- `encoding` \-- Content transfer encoding of the non-`text`{.interpreted-text role="mimetype"} part

If *fmt* is `None`, use the following default *fmt*:

> \"\[Non-text (%(type)s) part of message omitted, filename %(filename)s\]\"

Optional *\_mangle_from\_* and *maxheaderlen* are as with the `Generator`{.interpreted-text role="class"} base class.
:::

**Footnotes**

[^1]: This statement assumes that you use the appropriate setting for `unixfrom`, and that there are no `email.policy`{.interpreted-text role="mod"} settings calling for automatic adjustments (for example, `~email.policy.EmailPolicy.refold_source`{.interpreted-text role="attr"} must be `none`, which is *not* the default). It is also not 100% true, since if the message does not conform to the RFC standards occasionally information about the exact original text is lost during parsing error recovery. It is a goal to fix these latter edge cases when possible.
