# `!http.cookies`{.interpreted-text role="mod"} \-\-- HTTP state management

::: {.module synopsis="Support for HTTP state management (cookies)."}
http.cookies
:::

**Source code:** `Lib/http/cookies.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

The `!http.cookies`{.interpreted-text role="mod"} module defines classes for abstracting the concept of cookies, an HTTP state management mechanism. It supports both simple string-only cookies, and provides an abstraction for having any serializable data-type as cookie value.

The module formerly strictly applied the parsing rules described in the `2109`{.interpreted-text role="rfc"} and `2068`{.interpreted-text role="rfc"} specifications. It has since been discovered that MSIE 3.0x didn\'t follow the character rules outlined in those specs; many current-day browsers and servers have also relaxed parsing rules when it comes to cookie handling. As a result, this module now uses parsing rules that are a bit less strict than they once were.

The character set, `string.ascii_letters`{.interpreted-text role="data"}, `string.digits`{.interpreted-text role="data"} and `` !#$%&'*+-.^_`|~: `` denote the set of valid characters allowed by this module in a cookie name (as `~Morsel.key`{.interpreted-text role="attr"}).

::: versionchanged
3.3 Allowed \'`:`\' as a valid cookie name character.
:::

::: versionchanged
3.15 Allowed \'`"`\' as a valid cookie value character.
:::

:::: note
::: title
Note
:::

On encountering an invalid cookie, `CookieError`{.interpreted-text role="exc"} is raised, so if your cookie data comes from a browser you should always prepare for invalid data and catch `CookieError`{.interpreted-text role="exc"} on parsing.
::::

::: exception
CookieError

Exception failing because of `2109`{.interpreted-text role="rfc"} invalidity: incorrect attributes, incorrect `Set-Cookie`{.interpreted-text role="mailheader"} header, etc.
:::

::: BaseCookie([input])
This class is a dictionary-like object whose keys are strings and whose values are `Morsel`{.interpreted-text role="class"} instances. Note that upon setting a key to a value, the value is first converted to a `Morsel`{.interpreted-text role="class"} containing the key and the value.

If *input* is given, it is passed to the `load`{.interpreted-text role="meth"} method.
:::

::: SimpleCookie([input])
This class derives from `BaseCookie`{.interpreted-text role="class"} and overrides `~BaseCookie.value_decode`{.interpreted-text role="meth"} and `~BaseCookie.value_encode`{.interpreted-text role="meth"}. `!SimpleCookie`{.interpreted-text role="class"} supports strings as cookie values. When setting the value, `!SimpleCookie`{.interpreted-text role="class"} calls the builtin `str`{.interpreted-text role="func"} to convert the value to a string. Values received from HTTP are kept as strings.
:::

::: seealso

Module `http.cookiejar`{.interpreted-text role="mod"}

:   HTTP cookie handling for web *clients*. The `http.cookiejar`{.interpreted-text role="mod"} and `!http.cookies`{.interpreted-text role="mod"} modules do not depend on each other.

`2109`{.interpreted-text role="rfc"} - HTTP State Management Mechanism

:   This is the state management specification implemented by this module.
:::

## Cookie Objects

::: method
BaseCookie.value_decode(val)

Return a tuple `(real_value, coded_value)` from a string representation. `real_value` can be any type. This method does no decoding in `BaseCookie`{.interpreted-text role="class"} \-\-- it exists so it can be overridden.
:::

::: method
BaseCookie.value_encode(val)

Return a tuple `(real_value, coded_value)`. *val* can be any type, but `coded_value` will always be converted to a string. This method does no encoding in `BaseCookie`{.interpreted-text role="class"} \-\-- it exists so it can be overridden.

In general, it should be the case that `value_encode`{.interpreted-text role="meth"} and `value_decode`{.interpreted-text role="meth"} are inverses on the range of *value_decode*.
:::

::: method
BaseCookie.output(attrs=None, header=\'Set-Cookie:\', sep=\'rn\')

Return a string representation suitable to be sent as HTTP headers. *attrs* and *header* are sent to each `Morsel`{.interpreted-text role="class"}\'s `~Morsel.output`{.interpreted-text role="meth"} method. *sep* is used to join the headers together, and is by default the combination `'\r\n'` (CRLF).
:::

::: method
BaseCookie.js_output(attrs=None)

Return an embeddable JavaScript snippet, which, if run on a browser which supports JavaScript, will act the same as if the HTTP headers was sent.

The meaning for *attrs* is the same as in `output`{.interpreted-text role="meth"}.
:::

::: method
BaseCookie.load(rawdata)

If *rawdata* is a string, parse it as an `HTTP_COOKIE` and add the values found there as `Morsel`{.interpreted-text role="class"}s. If it is a dictionary, it is equivalent to:

    for k, v in rawdata.items():
        cookie[k] = v
:::

## Morsel Objects

::::::: Morsel
Abstract a key/value pair, which has some `2109`{.interpreted-text role="rfc"} attributes.

Morsels are dictionary-like objects, whose set of keys is constant \-\-- the valid `2109`{.interpreted-text role="rfc"} attributes, which are:

> ::: attribute
> expires path comment domain max-age secure version httponly samesite partitioned
> :::

The attribute `httponly`{.interpreted-text role="attr"} specifies that the cookie is only transferred in HTTP requests, and is not accessible through JavaScript. This is intended to mitigate some forms of cross-site scripting.

The attribute `samesite`{.interpreted-text role="attr"} controls when the browser sends the cookie with cross-site requests. This helps to mitigate CSRF attacks. Valid values are \"Strict\" (only sent with same-site requests), \"Lax\" (sent with same-site requests and top-level navigations), and \"None\" (sent with same-site and cross-site requests). When using \"None\", the \"secure\" attribute must also be set, as required by modern browsers.

The attribute `partitioned`{.interpreted-text role="attr"} indicates to user agents that these cross-site cookies *should* only be available in the same top-level context that the cookie was first set in. For this to be accepted by the user agent, you **must** also set `Secure`.

In addition, it is recommended to use the `__Host` prefix when setting partitioned cookies to make them bound to the hostname and not the registrable domain. Read [CHIPS (Cookies Having Independent Partitioned State)](https://github.com/privacycg/CHIPS/blob/main/README.md) for full details and examples.

The keys are case-insensitive and their default value is `''`.

::: versionchanged
3.5 `!__eq__`{.interpreted-text role="meth"} now takes `~Morsel.key`{.interpreted-text role="attr"} and `~Morsel.value`{.interpreted-text role="attr"} into account.
:::

::: versionchanged
3.7 Attributes `~Morsel.key`{.interpreted-text role="attr"}, `~Morsel.value`{.interpreted-text role="attr"} and `~Morsel.coded_value`{.interpreted-text role="attr"} are read-only. Use `~Morsel.set`{.interpreted-text role="meth"} for setting them.
:::

::: versionchanged
3.8 Added support for the `samesite`{.interpreted-text role="attr"} attribute.
:::

::: versionchanged
3.14 Added support for the `partitioned`{.interpreted-text role="attr"} attribute.
:::
:::::::

::: attribute
Morsel.value

The value of the cookie.
:::

::: attribute
Morsel.coded_value

The encoded value of the cookie \-\-- this is what should be sent.
:::

::: attribute
Morsel.key

The name of the cookie.
:::

::: method
Morsel.set(key, value, coded_value)

Set the *key*, *value* and *coded_value* attributes.
:::

::: method
Morsel.isReservedKey(K)

Whether *K* is a member of the set of keys of a `Morsel`{.interpreted-text role="class"}.
:::

::: method
Morsel.output(attrs=None, header=\'Set-Cookie:\')

Return a string representation of the Morsel, suitable to be sent as an HTTP header. By default, all the attributes are included, unless *attrs* is given, in which case it should be a list of attributes to use. *header* is by default `"Set-Cookie:"`.
:::

::: method
Morsel.js_output(attrs=None)

Return an embeddable JavaScript snippet, which, if run on a browser which supports JavaScript, will act the same as if the HTTP header was sent.

The meaning for *attrs* is the same as in `output`{.interpreted-text role="meth"}.
:::

::: method
Morsel.OutputString(attrs=None)

Return a string representing the Morsel, without any surrounding HTTP or JavaScript.

The meaning for *attrs* is the same as in `output`{.interpreted-text role="meth"}.
:::

:::: method
Morsel.update(values)

Update the values in the Morsel dictionary with the values in the dictionary *values*. Raise an error if any of the keys in the *values* dict is not a valid `2109`{.interpreted-text role="rfc"} attribute.

::: versionchanged
3.5 an error is raised for invalid keys.
:::
::::

:::: method
Morsel.copy(value)

Return a shallow copy of the Morsel object.

::: versionchanged
3.5 return a Morsel object instead of a dict.
:::
::::

::: method
Morsel.setdefault(key, value=None)

Raise an error if key is not a valid `2109`{.interpreted-text role="rfc"} attribute, otherwise behave the same as `dict.setdefault`{.interpreted-text role="meth"}.
:::

## Example {#cookie-example}

The following example demonstrates how to use the `!http.cookies`{.interpreted-text role="mod"} module.

::: {.doctest options="+NORMALIZE_WHITESPACE"}
\>\>\> from http import cookies \>\>\> C = cookies.SimpleCookie() \>\>\> C\[\"fig\"\] = \"newton\" \>\>\> C\[\"sugar\"\] = \"wafer\" \>\>\> print(C) \# generate HTTP headers Set-Cookie: fig=newton Set-Cookie: sugar=wafer \>\>\> print(C.output()) \# same thing Set-Cookie: fig=newton Set-Cookie: sugar=wafer \>\>\> C = cookies.SimpleCookie() \>\>\> C\[\"rocky\"\] = \"road\" \>\>\> C\[\"rocky\"\]\[\"path\"\] = \"/cookie\" \>\>\> print(C.output(header=\"Cookie:\")) Cookie: rocky=road; Path=/cookie \>\>\> print(C.output(attrs=\[\], header=\"Cookie:\")) Cookie: rocky=road \>\>\> C = cookies.SimpleCookie() \>\>\> C.load(\"chips=ahoy; vienna=finger\") \# load from a string (HTTP header) \>\>\> print(C) Set-Cookie: chips=ahoy Set-Cookie: vienna=finger \>\>\> C = cookies.SimpleCookie() \>\>\> C.load(\'keebler=\"E=everybody; L=\\\"Loves\\\"; fudge=;\";\') \>\>\> print(C) Set-Cookie: keebler=\"E=everybody; L=\"Loves\"; fudge=;\" \>\>\> C = cookies.SimpleCookie() \>\>\> C\[\"oreo\"\] = \"doublestuff\" \>\>\> C\[\"oreo\"\]\[\"path\"\] = \"/\" \>\>\> print(C) Set-Cookie: oreo=doublestuff; Path=/ \>\>\> C = cookies.SimpleCookie() \>\>\> C\[\"twix\"\] = \"none for you\" \>\>\> C\[\"twix\"\].value \'none for you\' \>\>\> C = cookies.SimpleCookie() \>\>\> C\[\"number\"\] = 7 \# equivalent to C\[\"number\"\] = str(7) \>\>\> C\[\"string\"\] = \"seven\" \>\>\> C\[\"number\"\].value \'7\' \>\>\> C\[\"string\"\].value \'seven\' \>\>\> print(C) Set-Cookie: number=7 Set-Cookie: string=seven \>\>\> import json \>\>\> C = cookies.SimpleCookie() \>\>\> C.load(f\'cookies=7; mixins=\"{json.dumps({\"chips\": \"dark chocolate\"})}\"; state=gooey\') \>\>\> print(C) Set-Cookie: cookies=7 Set-Cookie: mixins=\"{\"chips\": \"dark chocolate\"}\" Set-Cookie: state=gooey
:::
