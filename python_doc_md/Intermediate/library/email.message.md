# `!email.message`{.interpreted-text role="mod"}: Representing an email message

::: {.module synopsis="The base class representing email messages."}
email.message
:::

**Source code:** `Lib/email/message.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

::: versionadded
3.6[^1]
:::

The central class in the `email`{.interpreted-text role="mod"} package is the `EmailMessage`{.interpreted-text role="class"} class, imported from the `!email.message`{.interpreted-text role="mod"} module. It is the base class for the `email`{.interpreted-text role="mod"} object model. `EmailMessage`{.interpreted-text role="class"} provides the core functionality for setting and querying header fields, for accessing message bodies, and for creating or modifying structured messages.

An email message consists of *headers* and a *payload* (which is also referred to as the *content*). Headers are `5322`{.interpreted-text role="rfc"} or `6532`{.interpreted-text role="rfc"} style field names and values, where the field name and value are separated by a colon. The colon is not part of either the field name or the field value. The payload may be a simple text message, or a binary object, or a structured sequence of sub-messages each with their own set of headers and their own payload. The latter type of payload is indicated by the message having a MIME type such as `multipart/\*`{.interpreted-text role="mimetype"} or `message/rfc822`{.interpreted-text role="mimetype"}.

The conceptual model provided by an `EmailMessage`{.interpreted-text role="class"} object is that of an ordered dictionary of headers coupled with a *payload* that represents the `5322`{.interpreted-text role="rfc"} body of the message, which might be a list of sub-`EmailMessage` objects. In addition to the normal dictionary methods for accessing the header names and values, there are methods for accessing specialized information from the headers (for example the MIME content type), for operating on the payload, for generating a serialized version of the message, and for recursively walking over the object tree.

The `EmailMessage`{.interpreted-text role="class"} dictionary-like interface is indexed by the header names, which must be ASCII values. The values of the dictionary are strings with some extra methods. Headers are stored and returned in case-preserving form, but field names are matched case-insensitively. The keys are ordered, but unlike a real dict, there can be duplicates. Additional methods are provided for working with headers that have duplicate keys.

The *payload* is either a string or bytes object, in the case of simple message objects, or a list of `EmailMessage`{.interpreted-text role="class"} objects, for MIME container documents such as `multipart/\*`{.interpreted-text role="mimetype"} and `message/rfc822`{.interpreted-text role="mimetype"} message objects.

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: EmailMessage(policy=default)
If *policy* is specified use the rules it specifies to update and serialize the representation of the message. If *policy* is not set, use the `~email.policy.default`{.interpreted-text role="class"} policy, which follows the rules of the email RFCs except for line endings (instead of the RFC mandated `\r\n`, it uses the Python standard `\n` line endings). For more information see the `~email.policy`{.interpreted-text role="mod"} documentation.[^2]

:::: method
as_string(unixfrom=False, maxheaderlen=None, policy=None)

Return the entire message flattened as a string. When optional *unixfrom* is true, the envelope header is included in the returned string. *unixfrom* defaults to `False`. For backward compatibility with the base `~email.message.Message`{.interpreted-text role="class"} class *maxheaderlen* is accepted, but defaults to `None`, which means that by default the line length is controlled by the `~email.policy.Policy.max_line_length`{.interpreted-text role="attr"} of the policy. The *policy* argument may be used to override the default policy obtained from the message instance. This can be used to control some of the formatting produced by the method, since the specified *policy* will be passed to the `~email.generator.Generator`{.interpreted-text role="class"}.

Flattening the message may trigger changes to the `EmailMessage`{.interpreted-text role="class"} if defaults need to be filled in to complete the transformation to a string (for example, MIME boundaries may be generated or modified).

Note that this method is provided as a convenience and may not be the most useful way to serialize messages in your application, especially if you are dealing with multiple messages. See `email.generator.Generator`{.interpreted-text role="class"} for a more flexible API for serializing messages. Note also that this method is restricted to producing messages serialized as \"7 bit clean\" when `~email.policy.EmailPolicy.utf8`{.interpreted-text role="attr"} is `False`, which is the default.

::: versionchanged
3.6 the default behavior when *maxheaderlen* is not specified was changed from defaulting to 0 to defaulting to the value of *max_line_length* from the policy.
:::
::::

:::: method
\_\_str\_\_()

Equivalent to `as_string(policy=self.policy.clone(utf8=True))`. Allows `str(msg)` to produce a string containing the serialized message in a readable format.

::: versionchanged
3.4 the method was changed to use `utf8=True`, thus producing an `6531`{.interpreted-text role="rfc"}-like message representation, instead of being a direct alias for `as_string`{.interpreted-text role="meth"}.
:::
::::

::: method
as_bytes(unixfrom=False, policy=None)

Return the entire message flattened as a bytes object. When optional *unixfrom* is true, the envelope header is included in the returned string. *unixfrom* defaults to `False`. The *policy* argument may be used to override the default policy obtained from the message instance. This can be used to control some of the formatting produced by the method, since the specified *policy* will be passed to the `~email.generator.BytesGenerator`{.interpreted-text role="class"}.

Flattening the message may trigger changes to the `EmailMessage`{.interpreted-text role="class"} if defaults need to be filled in to complete the transformation to a string (for example, MIME boundaries may be generated or modified).

Note that this method is provided as a convenience and may not be the most useful way to serialize messages in your application, especially if you are dealing with multiple messages. See `email.generator.BytesGenerator`{.interpreted-text role="class"} for a more flexible API for serializing messages.
:::

::: method
\_\_bytes\_\_()

Equivalent to `.as_bytes`{.interpreted-text role="meth"}. Allows `bytes(msg)` to produce a bytes object containing the serialized message.
:::

::: method
is_multipart()

Return `True` if the message\'s payload is a list of sub-`EmailMessage`{.interpreted-text role="class"} objects, otherwise return `False`. When `is_multipart`{.interpreted-text role="meth"} returns `False`, the payload should be a string object (which might be a CTE encoded binary payload). Note that `is_multipart`{.interpreted-text role="meth"} returning `True` does not necessarily mean that \"msg.get_content_maintype() == \'multipart\'\" will return the `True`. For example, `is_multipart` will return `True` when the `EmailMessage`{.interpreted-text role="class"} is of type `message/rfc822`.
:::

::: method
set_unixfrom(unixfrom)

Set the message\'s envelope header to *unixfrom*, which should be a string. (See `~mailbox.mboxMessage`{.interpreted-text role="class"} for a brief description of this header.)
:::

::: method
get_unixfrom()

Return the message\'s envelope header. Defaults to `None` if the envelope header was never set.
:::

The following methods implement the mapping-like interface for accessing the message\'s headers. Note that there are some semantic differences between these methods and a normal mapping (i.e. dictionary) interface. For example, in a dictionary there are no duplicate keys, but here there may be duplicate message headers. Also, in dictionaries there is no guaranteed order to the keys returned by `keys`{.interpreted-text role="meth"}, but in an `EmailMessage`{.interpreted-text role="class"} object, headers are always returned in the order they appeared in the original message, or in which they were added to the message later. Any header deleted and then re-added is always appended to the end of the header list.

These semantic differences are intentional and are biased toward convenience in the most common use cases.

Note that in all cases, any envelope header present in the message is not included in the mapping interface.

::: method
\_\_len\_\_()

Return the total number of headers, including duplicates.
:::

::: method
\_\_contains\_\_(name)

Return `True` if the message object has a field named *name*. Matching is done without regard to case and *name* does not include the trailing colon. Used for the `in` operator. For example:

    if 'message-id' in myMessage:
       print('Message-ID:', myMessage['message-id'])
:::

::: method
\_\_getitem\_\_(name)

Return the value of the named header field. *name* does not include the colon field separator. If the header is missing, `None` is returned; a `KeyError`{.interpreted-text role="exc"} is never raised.

Note that if the named field appears more than once in the message\'s headers, exactly which of those field values will be returned is undefined. Use the `get_all`{.interpreted-text role="meth"} method to get the values of all the extant headers named *name*.

Using the standard (non-`compat32`) policies, the returned value is an instance of a subclass of `email.headerregistry.BaseHeader`{.interpreted-text role="class"}.
:::

::: method
\_\_setitem\_\_(name, val)

Add a header to the message with field name *name* and value *val*. The field is appended to the end of the message\'s existing headers.

Note that this does *not* overwrite or delete any existing header with the same name. If you want to ensure that the new header is the only one present in the message with field name *name*, delete the field first, e.g.:

    del msg['subject']
    msg['subject'] = 'Python roolz!'

If the `policy <email.policy>`{.interpreted-text role="mod"} defines certain headers to be unique (as the standard policies do), this method may raise a `ValueError`{.interpreted-text role="exc"} when an attempt is made to assign a value to such a header when one already exists. This behavior is intentional for consistency\'s sake, but do not depend on it as we may choose to make such assignments do an automatic deletion of the existing header in the future.
:::

::: method
\_\_delitem\_\_(name)

Delete all occurrences of the field with name *name* from the message\'s headers. No exception is raised if the named field isn\'t present in the headers.
:::

::: method
keys()

Return a list of all the message\'s header field names.
:::

::: method
values()

Return a list of all the message\'s field values.
:::

::: method
items()

Return a list of 2-tuples containing all the message\'s field headers and values.
:::

::: method
get(name, failobj=None)

Return the value of the named header field. This is identical to `~object.__getitem__`{.interpreted-text role="meth"} except that optional *failobj* is returned if the named header is missing (*failobj* defaults to `None`).
:::

Here are some additional useful header related methods:

::: method
get_all(name, failobj=None)

Return a list of all the values for the field named *name*. If there are no such named headers in the message, *failobj* is returned (defaults to `None`).
:::

::: method
add_header([name]{#name}, [value]{#value}, \*\*\_params)

Extended header setting. This method is similar to `__setitem__`{.interpreted-text role="meth"} except that additional header parameters can be provided as keyword arguments. *\_name* is the header field to add and *\_value* is the *primary* value for the header.

For each item in the keyword argument dictionary *\_params*, the key is taken as the parameter name, with underscores converted to dashes (since dashes are illegal in Python identifiers). Normally, the parameter will be added as `key="value"` unless the value is `None`, in which case only the key will be added.

If the value contains non-ASCII characters, the charset and language may be explicitly controlled by specifying the value as a three tuple in the format `(CHARSET, LANGUAGE, VALUE)`, where `CHARSET` is a string naming the charset to be used to encode the value, `LANGUAGE` can usually be set to `None` or the empty string (see `2231`{.interpreted-text role="rfc"} for other possibilities), and `VALUE` is the string value containing non-ASCII code points. If a three tuple is not passed and the value contains non-ASCII characters, it is automatically encoded in `2231`{.interpreted-text role="rfc"} format using a `CHARSET` of `utf-8` and a `LANGUAGE` of `None`.

Here is an example:

    msg.add_header('Content-Disposition', 'attachment', filename='bud.gif')

This will add a header that looks like :

    Content-Disposition: attachment; filename="bud.gif"

An example of the extended interface with non-ASCII characters:

    msg.add_header('Content-Disposition', 'attachment',
                   filename=('iso-8859-1', '', 'Fußballer.ppt'))
:::

::: method
replace_header([name]{#name}, [value]{#value})

Replace a header. Replace the first header found in the message that matches *\_name*, retaining header order and field name case of the original header. If no matching header is found, raise a `KeyError`{.interpreted-text role="exc"}.
:::

::: method
get_content_type()

Return the message\'s content type, coerced to lower case of the form `maintype/subtype`{.interpreted-text role="mimetype"}. If there is no `Content-Type`{.interpreted-text role="mailheader"} header in the message return the value returned by `get_default_type`{.interpreted-text role="meth"}. If the `Content-Type`{.interpreted-text role="mailheader"} header is invalid, return `text/plain`.

(According to `2045`{.interpreted-text role="rfc"}, messages always have a default type, `get_content_type`{.interpreted-text role="meth"} will always return a value. `2045`{.interpreted-text role="rfc"} defines a message\'s default type to be `text/plain`{.interpreted-text role="mimetype"} unless it appears inside a `multipart/digest`{.interpreted-text role="mimetype"} container, in which case it would be `message/rfc822`{.interpreted-text role="mimetype"}. If the `Content-Type`{.interpreted-text role="mailheader"} header has an invalid type specification, `2045`{.interpreted-text role="rfc"} mandates that the default type be `text/plain`{.interpreted-text role="mimetype"}.)
:::

::: method
get_content_maintype()

Return the message\'s main content type. This is the `maintype`{.interpreted-text role="mimetype"} part of the string returned by `get_content_type`{.interpreted-text role="meth"}.
:::

::: method
get_content_subtype()

Return the message\'s sub-content type. This is the `subtype`{.interpreted-text role="mimetype"} part of the string returned by `get_content_type`{.interpreted-text role="meth"}.
:::

::: method
get_default_type()

Return the default content type. Most messages have a default content type of `text/plain`{.interpreted-text role="mimetype"}, except for messages that are subparts of `multipart/digest`{.interpreted-text role="mimetype"} containers. Such subparts have a default content type of `message/rfc822`{.interpreted-text role="mimetype"}.
:::

::: method
set_default_type(ctype)

Set the default content type. *ctype* should either be `text/plain`{.interpreted-text role="mimetype"} or `message/rfc822`{.interpreted-text role="mimetype"}, although this is not enforced. The default content type is not stored in the `Content-Type`{.interpreted-text role="mailheader"} header, so it only affects the return value of the `get_content_type` methods when no `Content-Type`{.interpreted-text role="mailheader"} header is present in the message.
:::

:::: method
set_param(param, value, header=\'Content-Type\', requote=True, charset=None, language=\'\', replace=False)

Set a parameter in the `Content-Type`{.interpreted-text role="mailheader"} header. If the parameter already exists in the header, replace its value with *value*. When *header* is `Content-Type` (the default) and the header does not yet exist in the message, add it, set its value to `text/plain`{.interpreted-text role="mimetype"}, and append the new parameter value. Optional *header* specifies an alternative header to `Content-Type`{.interpreted-text role="mailheader"}.

If the value contains non-ASCII characters, the charset and language may be explicitly specified using the optional *charset* and *language* parameters. Optional *language* specifies the `2231`{.interpreted-text role="rfc"} language, defaulting to the empty string. Both *charset* and *language* should be strings. The default is to use the `utf8` *charset* and `None` for the *language*.

If *replace* is `False` (the default) the header is moved to the end of the list of headers. If *replace* is `True`, the header will be updated in place.

Use of the *requote* parameter with `EmailMessage`{.interpreted-text role="class"} objects is deprecated.

Note that existing parameter values of headers may be accessed through the `~email.headerregistry.ParameterizedMIMEHeader.params`{.interpreted-text role="attr"} attribute of the header value (for example, `msg['Content-Type'].params['charset']`).

::: versionchanged
3.4 `replace` keyword was added.
:::
::::

::: method
del_param(param, header=\'content-type\', requote=True)

Remove the given parameter completely from the `Content-Type`{.interpreted-text role="mailheader"} header. The header will be re-written in place without the parameter or its value. Optional *header* specifies an alternative to `Content-Type`{.interpreted-text role="mailheader"}.

Use of the *requote* parameter with `EmailMessage`{.interpreted-text role="class"} objects is deprecated.
:::

::: method
get_filename(failobj=None)

Return the value of the `filename` parameter of the `Content-Disposition`{.interpreted-text role="mailheader"} header of the message. If the header does not have a `filename` parameter, this method falls back to looking for the `name` parameter on the `Content-Type`{.interpreted-text role="mailheader"} header. If neither is found, or the header is missing, then *failobj* is returned. The returned string will always be unquoted as per `email.utils.unquote`{.interpreted-text role="func"}.
:::

::: method
get_boundary(failobj=None)

Return the value of the `boundary` parameter of the `Content-Type`{.interpreted-text role="mailheader"} header of the message, or *failobj* if either the header is missing, or has no `boundary` parameter. The returned string will always be unquoted as per `email.utils.unquote`{.interpreted-text role="func"}.
:::

::: method
set_boundary(boundary)

Set the `boundary` parameter of the `Content-Type`{.interpreted-text role="mailheader"} header to *boundary*. `set_boundary`{.interpreted-text role="meth"} will always quote *boundary* if necessary. A `~email.errors.HeaderParseError`{.interpreted-text role="exc"} is raised if the message object has no `Content-Type`{.interpreted-text role="mailheader"} header.

Note that using this method is subtly different from deleting the old `Content-Type`{.interpreted-text role="mailheader"} header and adding a new one with the new boundary via `add_header`{.interpreted-text role="meth"}, because `set_boundary`{.interpreted-text role="meth"} preserves the order of the `Content-Type`{.interpreted-text role="mailheader"} header in the list of headers.
:::

::: method
get_content_charset(failobj=None)

Return the `charset` parameter of the `Content-Type`{.interpreted-text role="mailheader"} header, coerced to lower case. If there is no `Content-Type`{.interpreted-text role="mailheader"} header, or if that header has no `charset` parameter, *failobj* is returned.
:::

::: method
get_charsets(failobj=None)

Return a list containing the character set names in the message. If the message is a `multipart`{.interpreted-text role="mimetype"}, then the list will contain one element for each subpart in the payload, otherwise, it will be a list of length 1.

Each item in the list will be a string which is the value of the `charset` parameter in the `Content-Type`{.interpreted-text role="mailheader"} header for the represented subpart. If the subpart has no `Content-Type`{.interpreted-text role="mailheader"} header, no `charset` parameter, or is not of the `text`{.interpreted-text role="mimetype"} main MIME type, then that item in the returned list will be *failobj*.
:::

:::: method
is_attachment

Return `True` if there is a `Content-Disposition`{.interpreted-text role="mailheader"} header and its (case insensitive) value is `attachment`, `False` otherwise.

::: versionchanged
3.4.2 is_attachment is now a method instead of a property, for consistency with `~email.message.Message.is_multipart`{.interpreted-text role="meth"}.
:::
::::

:::: method
get_content_disposition()

Return the lowercased value (without parameters) of the message\'s `Content-Disposition`{.interpreted-text role="mailheader"} header if it has one, or `None`. The possible values for this method are *inline*, *attachment* or `None` if the message follows `2183`{.interpreted-text role="rfc"}.

::: versionadded
3.5
:::
::::

The following methods relate to interrogating and manipulating the content (payload) of the message.

:::::: method
walk()

The `walk`{.interpreted-text role="meth"} method is an all-purpose generator which can be used to iterate over all the parts and subparts of a message object tree, in depth-first traversal order. You will typically use `walk`{.interpreted-text role="meth"} as the iterator in a `for` loop; each iteration returns the next subpart.

Here\'s an example that prints the MIME type of every part of a multipart message structure:

::: testsetup
from email import message_from_binary_file with open(\'../Lib/test/test_email/data/msg_16.txt\', \'rb\') as f: msg = message_from_binary_file(f)
:::

::: doctest
\>\>\> for part in msg.walk(): \... print(part.get_content_type()) multipart/report text/plain message/delivery-status text/plain text/plain message/rfc822 text/plain
:::

`walk` iterates over the subparts of any part where `is_multipart`{.interpreted-text role="meth"} returns `True`, even though `msg.get_content_maintype() == 'multipart'` may return `False`. We can see this in our example by making use of the `_structure` debug helper function:

::: doctest
\>\>\> from email.iterators import [structure]{#structure} \>\>\> for part in msg.walk(): \... print(part.get_content_maintype() == \'multipart\', \... part.is_multipart()) True True False False False True False False False False False True False False \>\>\> [structure]{#structure}(msg) multipart/report text/plain message/delivery-status text/plain text/plain message/rfc822 text/plain
:::

Here the `message` parts are not `multiparts`, but they do contain subparts. `is_multipart()` returns `True` and `walk` descends into the subparts.
::::::

::: method
get_body(preferencelist=(\'related\', \'html\', \'plain\'))

Return the MIME part that is the best candidate to be the \"body\" of the message.

*preferencelist* must be a sequence of strings from the set `related`, `html`, and `plain`, and indicates the order of preference for the content type of the part returned.

Start looking for candidate matches with the object on which the `get_body` method is called.

If `related` is not included in *preferencelist*, consider the root part (or subpart of the root part) of any related encountered as a candidate if the (sub-)part matches a preference.

When encountering a `multipart/related`, check the `start` parameter and if a part with a matching `Content-ID`{.interpreted-text role="mailheader"} is found, consider only it when looking for candidate matches. Otherwise consider only the first (default root) part of the `multipart/related`.

If a part has a `Content-Disposition`{.interpreted-text role="mailheader"} header, only consider the part a candidate match if the value of the header is `inline`.

If none of the candidates matches any of the preferences in *preferencelist*, return `None`.

Notes: (1) For most applications the only *preferencelist* combinations that really make sense are `('plain',)`, `('html', 'plain')`, and the default `('related', 'html', 'plain')`. (2) Because matching starts with the object on which `get_body` is called, calling `get_body` on a `multipart/related` will return the object itself unless *preferencelist* has a non-default value. (3) Messages (or message parts) that do not specify a `Content-Type`{.interpreted-text role="mailheader"} or whose `Content-Type`{.interpreted-text role="mailheader"} header is invalid will be treated as if they are of type `text/plain`, which may occasionally cause `get_body` to return unexpected results.
:::

::: method
iter_attachments()

Return an iterator over all of the immediate sub-parts of the message that are not candidate \"body\" parts. That is, skip the first occurrence of each of `text/plain`, `text/html`, `multipart/related`, or `multipart/alternative` (unless they are explicitly marked as attachments via `Content-Disposition: attachment`{.interpreted-text role="mailheader"}), and return all remaining parts. When applied directly to a `multipart/related`, return an iterator over the all the related parts except the root part (ie: the part pointed to by the `start` parameter, or the first part if there is no `start` parameter or the `start` parameter doesn\'t match the `Content-ID`{.interpreted-text role="mailheader"} of any of the parts). When applied directly to a `multipart/alternative` or a non-`multipart`, return an empty iterator.
:::

::: method
iter_parts()

Return an iterator over all of the immediate sub-parts of the message, which will be empty for a non-`multipart`. (See also `~email.message.EmailMessage.walk`{.interpreted-text role="meth"}.)
:::

::: method
get_content(*args, content_manager=None,*\*kw)

Call the `~email.contentmanager.ContentManager.get_content`{.interpreted-text role="meth"} method of the *content_manager*, passing self as the message object, and passing along any other arguments or keywords as additional arguments. If *content_manager* is not specified, use the `content_manager` specified by the current `~email.policy`{.interpreted-text role="mod"}.
:::

::: method
set_content(*args, content_manager=None,*\*kw)

Call the `~email.contentmanager.ContentManager.set_content`{.interpreted-text role="meth"} method of the *content_manager*, passing self as the message object, and passing along any other arguments or keywords as additional arguments. If *content_manager* is not specified, use the `content_manager` specified by the current `~email.policy`{.interpreted-text role="mod"}.
:::

::: method
make_related(boundary=None)

Convert a non-`multipart` message into a `multipart/related` message, moving any existing `Content-`{.interpreted-text role="mailheader"} headers and payload into a (new) first part of the `multipart`. If *boundary* is specified, use it as the boundary string in the multipart, otherwise leave the boundary to be automatically created when it is needed (for example, when the message is serialized).
:::

::: method
make_alternative(boundary=None)

Convert a non-`multipart` or a `multipart/related` into a `multipart/alternative`, moving any existing `Content-`{.interpreted-text role="mailheader"} headers and payload into a (new) first part of the `multipart`. If *boundary* is specified, use it as the boundary string in the multipart, otherwise leave the boundary to be automatically created when it is needed (for example, when the message is serialized).
:::

::: method
make_mixed(boundary=None)

Convert a non-`multipart`, a `multipart/related`, or a `multipart-alternative` into a `multipart/mixed`, moving any existing `Content-`{.interpreted-text role="mailheader"} headers and payload into a (new) first part of the `multipart`. If *boundary* is specified, use it as the boundary string in the multipart, otherwise leave the boundary to be automatically created when it is needed (for example, when the message is serialized).
:::

::: method
add_related(*args, content_manager=None,*\*kw)

If the message is a `multipart/related`, create a new message object, pass all of the arguments to its `set_content`{.interpreted-text role="meth"} method, and `~email.message.Message.attach`{.interpreted-text role="meth"} it to the `multipart`. If the message is a non-`multipart`, call `make_related`{.interpreted-text role="meth"} and then proceed as above. If the message is any other type of `multipart`, raise a `TypeError`{.interpreted-text role="exc"}. If *content_manager* is not specified, use the `content_manager` specified by the current `~email.policy`{.interpreted-text role="mod"}. If the added part has no `Content-Disposition`{.interpreted-text role="mailheader"} header, add one with the value `inline`.
:::

::: method
add_alternative(*args, content_manager=None,*\*kw)

If the message is a `multipart/alternative`, create a new message object, pass all of the arguments to its `set_content`{.interpreted-text role="meth"} method, and `~email.message.Message.attach`{.interpreted-text role="meth"} it to the `multipart`. If the message is a non-`multipart` or `multipart/related`, call `make_alternative`{.interpreted-text role="meth"} and then proceed as above. If the message is any other type of `multipart`, raise a `TypeError`{.interpreted-text role="exc"}. If *content_manager* is not specified, use the `content_manager` specified by the current `~email.policy`{.interpreted-text role="mod"}.
:::

::: method
add_attachment(*args, content_manager=None,*\*kw)

If the message is a `multipart/mixed`, create a new message object, pass all of the arguments to its `set_content`{.interpreted-text role="meth"} method, and `~email.message.Message.attach`{.interpreted-text role="meth"} it to the `multipart`. If the message is a non-`multipart`, `multipart/related`, or `multipart/alternative`, call `make_mixed`{.interpreted-text role="meth"} and then proceed as above. If *content_manager* is not specified, use the `content_manager` specified by the current `~email.policy`{.interpreted-text role="mod"}. If the added part has no `Content-Disposition`{.interpreted-text role="mailheader"} header, add one with the value `attachment`. This method can be used both for explicit attachments (`Content-Disposition: attachment`{.interpreted-text role="mailheader"}) and `inline` attachments (`Content-Disposition: inline`{.interpreted-text role="mailheader"}), by passing appropriate options to the `content_manager`.
:::

::: method
clear()

Remove the payload and all of the headers.
:::

::: method
clear_content()

Remove the payload and all of the `!Content-`{.interpreted-text role="mailheader"} headers, leaving all other headers intact and in their original order.
:::

`EmailMessage`{.interpreted-text role="class"} objects have the following instance attributes:

::: attribute
preamble

The format of a MIME document allows for some text between the blank line following the headers, and the first multipart boundary string. Normally, this text is never visible in a MIME-aware mail reader because it falls outside the standard MIME armor. However, when viewing the raw text of the message, or when viewing the message in a non-MIME aware reader, this text can become visible.

The *preamble* attribute contains this leading extra-armor text for MIME documents. When the `~email.parser.Parser`{.interpreted-text role="class"} discovers some text after the headers but before the first boundary string, it assigns this text to the message\'s *preamble* attribute. When the `~email.generator.Generator`{.interpreted-text role="class"} is writing out the plain text representation of a MIME message, and it finds the message has a *preamble* attribute, it will write this text in the area between the headers and the first boundary. See `email.parser`{.interpreted-text role="mod"} and `email.generator`{.interpreted-text role="mod"} for details.

Note that if the message object has no preamble, the *preamble* attribute will be `None`.
:::

::: attribute
epilogue

The *epilogue* attribute acts the same way as the *preamble* attribute, except that it contains text that appears between the last boundary and the end of the message. As with the `~EmailMessage.preamble`{.interpreted-text role="attr"}, if there is no epilog text this attribute will be `None`.
:::

::: attribute
defects

The *defects* attribute contains a list of all the problems found when parsing this message. See `email.errors`{.interpreted-text role="mod"} for a detailed description of the possible parsing defects.
:::
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: MIMEPart(policy=default)
This class represents a subpart of a MIME message. It is identical to `EmailMessage`{.interpreted-text role="class"}, except that no `MIME-Version`{.interpreted-text role="mailheader"} headers are added when `~EmailMessage.set_content`{.interpreted-text role="meth"} is called, since sub-parts do not need their own `MIME-Version`{.interpreted-text role="mailheader"} headers.
:::

**Footnotes**

[^1]: Originally added in 3.4 as a `provisional module <provisional
    package>`{.interpreted-text role="term"}. Docs for legacy message class moved to `compat32_message`{.interpreted-text role="ref"}.

[^2]: The `EmailMessage`{.interpreted-text role="class"} class requires a policy that provides a `content_manager` attribute for content management methods like `set_content()` and `get_content()` to work. The legacy `~email.policy.compat32`{.interpreted-text role="const"} policy does not support these methods and should not be used with `EmailMessage`{.interpreted-text role="class"}.
