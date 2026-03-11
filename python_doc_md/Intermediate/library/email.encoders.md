# `!email.encoders`{.interpreted-text role="mod"}: Encoders

::: {.module synopsis="Encoders for email message payloads."}
email.encoders
:::

**Source code:** `Lib/email/encoders.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

This module is part of the legacy (`Compat32`) email API. In the new API the functionality is provided by the *cte* parameter of the `~email.message.EmailMessage.set_content`{.interpreted-text role="meth"} method.

This module is deprecated in Python 3. The functions provided here should not be called explicitly since the `~email.mime.text.MIMEText`{.interpreted-text role="class"} class sets the content type and CTE header using the *\_subtype* and *\_charset* values passed during the instantiation of that class.

The remaining text in this section is the original documentation of the module.

When creating `~email.message.Message`{.interpreted-text role="class"} objects from scratch, you often need to encode the payloads for transport through compliant mail servers. This is especially true for `image/\*`{.interpreted-text role="mimetype"} and `text/\*`{.interpreted-text role="mimetype"} type messages containing binary data.

The `email`{.interpreted-text role="mod"} package provides some convenient encoders in its `!encoders`{.interpreted-text role="mod"} module. These encoders are actually used by the `~email.mime.audio.MIMEAudio`{.interpreted-text role="class"} and `~email.mime.image.MIMEImage`{.interpreted-text role="class"} class constructors to provide default encodings. All encoder functions take exactly one argument, the message object to encode. They usually extract the payload, encode it, and reset the payload to this newly encoded value. They should also set the `Content-Transfer-Encoding`{.interpreted-text role="mailheader"} header as appropriate.

Note that these functions are not meaningful for a multipart message. They must be applied to individual subparts instead, and will raise a `TypeError`{.interpreted-text role="exc"} if passed a message whose type is multipart.

Here are the encoding functions provided:

::: function
encode_quopri(msg)

Encodes the payload into quoted-printable form and sets the `Content-Transfer-Encoding`{.interpreted-text role="mailheader"} header to `quoted-printable`[^1]. This is a good encoding to use when most of your payload is normal printable data, but contains a few unprintable characters.
:::

::: function
encode_base64(msg)

Encodes the payload into base64 form and sets the `Content-Transfer-Encoding`{.interpreted-text role="mailheader"} header to `base64`. This is a good encoding to use when most of your payload is unprintable data since it is a more compact form than quoted-printable. The drawback of base64 encoding is that it renders the text non-human readable.
:::

::: function
encode_7or8bit(msg)

This doesn\'t actually modify the message\'s payload, but it does set the `Content-Transfer-Encoding`{.interpreted-text role="mailheader"} header to either `7bit` or `8bit` as appropriate, based on the payload data.
:::

::: function
encode_noop(msg)

This does nothing; it doesn\'t even set the `Content-Transfer-Encoding`{.interpreted-text role="mailheader"} header.
:::

**Footnotes**

[^1]: Note that encoding with `encode_quopri`{.interpreted-text role="meth"} also encodes all tabs and space characters in the data.
