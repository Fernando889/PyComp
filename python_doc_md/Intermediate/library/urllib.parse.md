# `!urllib.parse`{.interpreted-text role="mod"} \-\-- Parse URLs into components

::: {.module synopsis="Parse URLs into or assemble them from components."}
urllib.parse
:::

**Source code:** `Lib/urllib/parse.py`{.interpreted-text role="source"}

::: index
single: WWW single: World Wide Web single: URL pair: URL; parsing pair: relative; URL
:::

------------------------------------------------------------------------

This module defines a standard interface to break Uniform Resource Locator (URL) strings up in components (addressing scheme, network location, path etc.), to combine the components back into a URL string, and to convert a \"relative URL\" to an absolute URL given a \"base URL.\"

The module has been designed to match the internet RFC on Relative Uniform Resource Locators. It supports the following URL schemes: `file`, `ftp`, `gopher`, `hdl`, `http`, `https`, `imap`, `itms-services`, `mailto`, `mms`, `news`, `nntp`, `prospero`, `rsync`, `rtsp`, `rtsps`, `rtspu`, `sftp`, `shttp`, `sip`, `sips`, `snews`, `svn`, `svn+ssh`, `telnet`, `wais`, `ws`, `wss`.

::: impl-detail
The inclusion of the `itms-services` URL scheme can prevent an app from passing Apple\'s App Store review process for the macOS and iOS App Stores. Handling for the `itms-services` scheme is always removed on iOS; on macOS, it *may* be removed if CPython has been built with the `--with-app-store-compliance`{.interpreted-text role="option"} option.
:::

The `!urllib.parse`{.interpreted-text role="mod"} module defines functions that fall into two broad categories: URL parsing and URL quoting. These are covered in detail in the following sections.

This module\'s functions use the deprecated term `netloc` (or `net_loc`), which was introduced in `1808`{.interpreted-text role="rfc"}. However, this term has been obsoleted by `3986`{.interpreted-text role="rfc"}, which introduced the term `authority` as its replacement. The use of `netloc` is continued for backward compatibility.

## URL Parsing

The URL parsing functions focus on splitting a URL string into its components, or on combining URL components into a URL string.

::::::::::::::: function
urlsplit(urlstring, scheme=None, allow_fragments=True, \*, missing_as_none=False)

Parse a URL into five components, returning a 5-item `named tuple`{.interpreted-text role="term"} `SplitResult`{.interpreted-text role="class"} or `SplitResultBytes`{.interpreted-text role="class"}. This corresponds to the general structure of a URL: `scheme://netloc/path?query#fragment`. Each tuple item is a string, possibly empty, or `None` if *missing_as_none* is true. Not defined component are represented an empty string (by default) or `None` if *missing_as_none* is true. The components are not broken up into smaller parts (for example, the network location is a single string), and % escapes are not expanded. The delimiters as shown above are not part of the result, except for a leading slash in the *path* component, which is retained if present. For example:

::: {.doctest options="+NORMALIZE_WHITESPACE"}
\>\>\> from urllib.parse import urlsplit \>\>\> urlsplit(\"scheme://netloc/path?query#fragment\") SplitResult(scheme=\'scheme\', netloc=\'netloc\', path=\'/path\', query=\'query\', fragment=\'fragment\') \>\>\> o = urlsplit(\"http://docs.python.org:80/3/library/urllib.parse.html?\" \... \"highlight=params#url-parsing\") \>\>\> o SplitResult(scheme=\'http\', netloc=\'docs.python.org:80\', path=\'/3/library/urllib.parse.html\', query=\'highlight=params\', fragment=\'url-parsing\') \>\>\> o.scheme \'http\' \>\>\> o.netloc \'docs.python.org:80\' \>\>\> o.hostname \'docs.python.org\' \>\>\> o.port 80 \>\>\> o.\_replace(fragment=\"\").geturl() \'http://docs.python.org:80/3/library/urllib.parse.html?highlight=params\' \>\>\> urlsplit(\"http://docs.python.org?\") SplitResult(scheme=\'http\', netloc=\'docs.python.org\', path=\'\', query=\'\', fragment=\'\') \>\>\> urlsplit(\"http://docs.python.org?\", missing_as_none=True) SplitResult(scheme=\'http\', netloc=\'docs.python.org\', path=\'\', query=\'\', fragment=None)
:::

Following the syntax specifications in `1808`{.interpreted-text role="rfc"}, `!urlsplit`{.interpreted-text role="func"} recognizes a netloc only if it is properly introduced by \'//\'. Otherwise the input is presumed to be a relative URL and thus to start with a path component.

::: {.doctest options="+NORMALIZE_WHITESPACE"}
\>\>\> from urllib.parse import urlsplit \>\>\> urlsplit(\'//www.cwi.nl:80/%7Eguido/Python.html\') SplitResult(scheme=\'\', netloc=\'www.cwi.nl:80\', path=\'/%7Eguido/Python.html\', query=\'\', fragment=\'\') \>\>\> urlsplit(\'www.cwi.nl/%7Eguido/Python.html\') SplitResult(scheme=\'\', netloc=\'\', path=\'www.cwi.nl/%7Eguido/Python.html\', query=\'\', fragment=\'\') \>\>\> urlsplit(\'help/Python.html\') SplitResult(scheme=\'\', netloc=\'\', path=\'help/Python.html\', query=\'\', fragment=\'\') \>\>\> urlsplit(\'help/Python.html\', missing_as_none=True) SplitResult(scheme=None, netloc=None, path=\'help/Python.html\', query=None, fragment=None)
:::

The *scheme* argument gives the default addressing scheme, to be used only if the URL does not specify one. It should be the same type (text or bytes) as *urlstring* or `None`, except that the `''` is always allowed, and is automatically converted to `b''` if appropriate.

If the *allow_fragments* argument is false, fragment identifiers are not recognized. Instead, they are parsed as part of the path or query component, and `fragment`{.interpreted-text role="attr"} is set to `None` or the empty string (depending on the value of *missing_as_none*) in the return value.

The return value is a `named tuple`{.interpreted-text role="term"}, which means that its items can be accessed by index or as named attributes, which are:

  ---------------------------------------------------------------------------------------------------------------------------------
  Attribute                                   Index   Value                                Value if not present
  ------------------------------------------- ------- ------------------------------------ ----------------------------------------
  `scheme`{.interpreted-text role="attr"}     0       URL scheme specifier                 *scheme* parameter or empty string[^1]

  `netloc`{.interpreted-text role="attr"}     1       Network location part                `None` or empty string[^2]

  `path`{.interpreted-text role="attr"}       2       Hierarchical path                    empty string

  `query`{.interpreted-text role="attr"}      3       Query component                      `None` or empty string[^3]

  `fragment`{.interpreted-text role="attr"}   4       Fragment identifier                  `None` or empty string[^4]

  `username`{.interpreted-text role="attr"}           User name                            `None`

  `password`{.interpreted-text role="attr"}           Password                             `None`

  `hostname`{.interpreted-text role="attr"}           Host name (lower case)               `None`

  `port`{.interpreted-text role="attr"}               Port number as integer, if present   `None`
  ---------------------------------------------------------------------------------------------------------------------------------

Reading the `port`{.interpreted-text role="attr"} attribute will raise a `ValueError`{.interpreted-text role="exc"} if an invalid port is specified in the URL. See section `urlparse-result-object`{.interpreted-text role="ref"} for more information on the result object.

Unmatched square brackets in the `netloc`{.interpreted-text role="attr"} attribute will raise a `ValueError`{.interpreted-text role="exc"}.

Characters in the `netloc`{.interpreted-text role="attr"} attribute that decompose under NFKC normalization (as used by the IDNA encoding) into any of `/`, `?`, `#`, `@`, or `:` will raise a `ValueError`{.interpreted-text role="exc"}. If the URL is decomposed before parsing, no error will be raised.

Following some of the [WHATWG spec](https://url.spec.whatwg.org/#concept-basic-url-parser) that updates `3986`{.interpreted-text role="rfc"}, leading C0 control and space characters are stripped from the URL. `\n`, `\r` and tab `\t` characters are removed from the URL at any position.

As is the case with all named tuples, the subclass has a few additional methods and attributes that are particularly useful. One such method is `_replace`{.interpreted-text role="meth"}. The `_replace`{.interpreted-text role="meth"} method will return a new `SplitResult`{.interpreted-text role="class"} object replacing specified fields with new values.

::: {.doctest options="+NORMALIZE_WHITESPACE"}
\>\>\> from urllib.parse import urlsplit \>\>\> u = urlsplit(\'//www.cwi.nl:80/%7Eguido/Python.html\') \>\>\> u SplitResult(scheme=\'\', netloc=\'www.cwi.nl:80\', path=\'/%7Eguido/Python.html\', query=\'\', fragment=\'\') \>\>\> u.\_replace(scheme=\'http\') SplitResult(scheme=\'http\', netloc=\'www.cwi.nl:80\', path=\'/%7Eguido/Python.html\', query=\'\', fragment=\'\')
:::

:::: warning
::: title
Warning
:::

`urlsplit`{.interpreted-text role="func"} does not perform validation. See `URL parsing
security <url-parsing-security>`{.interpreted-text role="ref"} for details.
::::

::: versionchanged
3.2 Added IPv6 URL parsing capabilities.
:::

::: versionchanged
3.3 The fragment is now parsed for all URL schemes (unless *allow_fragments* is false), in accordance with `3986`{.interpreted-text role="rfc"}. Previously, an allowlist of schemes that support fragments existed.
:::

::: versionchanged
3.6 Out-of-range port numbers now raise `ValueError`{.interpreted-text role="exc"}, instead of returning `None`.
:::

::: versionchanged
3.8 Characters that affect netloc parsing under NFKC normalization will now raise `ValueError`{.interpreted-text role="exc"}.
:::

::: versionchanged
3.10 ASCII newline and tab characters are stripped from the URL.
:::

::: versionchanged
3.12 Leading WHATWG C0 control and space characters are stripped from the URL.
:::

::: versionchanged
3.15 Added the *missing_as_none* parameter.
:::
:::::::::::::::

::::::: function
parse_qs(qs, keep_blank_values=False, strict_parsing=False, encoding=\'utf-8\', errors=\'replace\', max_num_fields=None, separator=\'&\')

Parse a query string given as a string argument (data of type `application/x-www-form-urlencoded`{.interpreted-text role="mimetype"}). Data are returned as a dictionary. The dictionary keys are the unique query variable names and the values are lists of values for each name.

The optional argument *keep_blank_values* is a flag indicating whether blank values in percent-encoded queries should be treated as blank strings. A true value indicates that blanks should be retained as blank strings. The default false value indicates that blank values are to be ignored and treated as if they were not included.

The optional argument *strict_parsing* is a flag indicating what to do with parsing errors. If false (the default), errors are silently ignored. If true, errors raise a `ValueError`{.interpreted-text role="exc"} exception.

The optional *encoding* and *errors* parameters specify how to decode percent-encoded sequences into Unicode characters, as accepted by the `bytes.decode`{.interpreted-text role="meth"} method.

The optional argument *max_num_fields* is the maximum number of fields to read. If set, then throws a `ValueError`{.interpreted-text role="exc"} if there are more than *max_num_fields* fields read.

The optional argument *separator* is the symbol to use for separating the query arguments. It defaults to `&`.

Use the `urllib.parse.urlencode`{.interpreted-text role="func"} function (with the `doseq` parameter set to `True`) to convert such dictionaries into query strings.

::: versionchanged
3.2 Add *encoding* and *errors* parameters.
:::

::: versionchanged
3.8 Added *max_num_fields* parameter.
:::

::: versionchanged
3.10 Added *separator* parameter with the default value of `&`. Python versions earlier than Python 3.10 allowed using both `;` and `&` as query parameter separator. This has been changed to allow only a single separator key, with `&` as the default separator.
:::

::: deprecated
3.14 Accepting objects with false values (like `0` and `[]`) except empty strings and byte-like objects and `None` is now deprecated.
:::
:::::::

:::::: function
parse_qsl(qs, keep_blank_values=False, strict_parsing=False, encoding=\'utf-8\', errors=\'replace\', max_num_fields=None, separator=\'&\')

Parse a query string given as a string argument (data of type `application/x-www-form-urlencoded`{.interpreted-text role="mimetype"}). Data are returned as a list of name, value pairs.

The optional argument *keep_blank_values* is a flag indicating whether blank values in percent-encoded queries should be treated as blank strings. A true value indicates that blanks should be retained as blank strings. The default false value indicates that blank values are to be ignored and treated as if they were not included.

The optional argument *strict_parsing* is a flag indicating what to do with parsing errors. If false (the default), errors are silently ignored. If true, errors raise a `ValueError`{.interpreted-text role="exc"} exception.

The optional *encoding* and *errors* parameters specify how to decode percent-encoded sequences into Unicode characters, as accepted by the `bytes.decode`{.interpreted-text role="meth"} method.

The optional argument *max_num_fields* is the maximum number of fields to read. If set, then throws a `ValueError`{.interpreted-text role="exc"} if there are more than *max_num_fields* fields read.

The optional argument *separator* is the symbol to use for separating the query arguments. It defaults to `&`.

Use the `urllib.parse.urlencode`{.interpreted-text role="func"} function to convert such lists of pairs into query strings.

::: versionchanged
3.2 Add *encoding* and *errors* parameters.
:::

::: versionchanged
3.8 Added *max_num_fields* parameter.
:::

::: versionchanged
3.10 Added *separator* parameter with the default value of `&`. Python versions earlier than Python 3.10 allowed using both `;` and `&` as query parameter separator. This has been changed to allow only a single separator key, with `&` as the default separator.
:::
::::::

:::: function
urlunsplit(parts) urlunsplit(parts, \*, keep_empty)

Construct a URL from a tuple as returned by `urlsplit`{.interpreted-text role="func"}. The *parts* argument can be any five-item iterable.

This may result in a slightly different, but equivalent URL, if the URL that was parsed originally had unnecessary delimiters (for example, a `?` with an empty query; the RFC states that these are equivalent).

If *keep_empty* is true, empty strings are kept in the result (for example, a `?` for an empty query), only `None` components are omitted. This allows rebuilding a URL that was parsed with option `missing_as_none=True`. By default, *keep_empty* is true if *parts* is the result of the `urlsplit`{.interpreted-text role="func"} call with `missing_as_none=True`.

::: versionchanged
3.15 Added the *keep_empty* parameter.
:::
::::

::: function
urlparse(urlstring, scheme=None, allow_fragments=True, \*, missing_as_none=False)

This is similar to `urlsplit`{.interpreted-text role="func"}, but additionally splits the *path* component on *path* and *params*. This function returns a 6-item `named tuple`{.interpreted-text role="term"} `ParseResult`{.interpreted-text role="class"} or `ParseResultBytes`{.interpreted-text role="class"}. Its items are the same as for the `!urlsplit`{.interpreted-text role="func"} result, except that *params* is inserted at index 3, between *path* and *query*.

This function is based on obsoleted `1738`{.interpreted-text role="rfc"} and `1808`{.interpreted-text role="rfc"}, which listed *params* as the main URL component. The more recent URL syntax allows parameters to be applied to each segment of the *path* portion of the URL (see `3986`{.interpreted-text role="rfc"}). `urlsplit`{.interpreted-text role="func"} should generally be used instead of `urlparse`{.interpreted-text role="func"}. A separate function is needed to separate the path segments and parameters.
:::

:::: function
urlunparse(parts) urlunparse(parts, \*, keep_empty)

Combine the elements of a tuple as returned by `urlparse`{.interpreted-text role="func"} into a complete URL as a string. The *parts* argument can be any six-item iterable.

This may result in a slightly different, but equivalent URL, if the URL that was parsed originally had unnecessary delimiters (for example, a `?` with an empty query; the RFC states that these are equivalent).

If *keep_empty* is true, empty strings are kept in the result (for example, a `?` for an empty query), only `None` components are omitted. This allows rebuilding a URL that was parsed with option `missing_as_none=True`. By default, *keep_empty* is true if *parts* is the result of the `urlparse`{.interpreted-text role="func"} call with `missing_as_none=True`.

::: versionchanged
3.15 Added the *keep_empty* parameter.
:::
::::

::::::::: function
urljoin(base, url, allow_fragments=True)

Construct a full (\"absolute\") URL by combining a \"base URL\" (*base*) with another URL (*url*). Informally, this uses components of the base URL, in particular the addressing scheme, the network location and (part of) the path, to provide missing components in the relative URL. For example:

> \>\>\> from urllib.parse import urljoin \>\>\> urljoin(\'http://www.cwi.nl/%7Eguido/Python.html\', \'FAQ.html\') \'http://www.cwi.nl/%7Eguido/FAQ.html\'

The *allow_fragments* argument has the same meaning and default as for `urlsplit`{.interpreted-text role="func"}.

::::: note
::: title
Note
:::

If *url* is an absolute URL (that is, it starts with `//` or `scheme://`), the *url*\'s hostname and/or scheme will be present in the result. For example:

::: doctest
\>\>\> urljoin(\'http://www.cwi.nl/%7Eguido/Python.html\', \... \'//www.python.org/%7Eguido\') \'http://www.python.org/%7Eguido\'
:::

If you do not want that behavior, preprocess the *url* with `urlsplit`{.interpreted-text role="func"} and `urlunsplit`{.interpreted-text role="func"}, removing possible *scheme* and *netloc* parts.
:::::

:::: warning
::: title
Warning
:::

Because an absolute URL may be passed as the `url` parameter, it is generally **not secure** to use `urljoin` with an attacker-controlled `url`. For example in, `urljoin("https://website.com/users/", username)`, if `username` can contain an absolute URL, the result of `urljoin` will be the absolute URL.
::::

::: versionchanged
3.5

Behavior updated to match the semantics defined in `3986`{.interpreted-text role="rfc"}.
:::
:::::::::

::::: function
urldefrag(url, \*, missing_as_none=False)

If *url* contains a fragment identifier, return a modified version of *url* with no fragment identifier, and the fragment identifier as a separate string. If there is no fragment identifier in *url*, return *url* unmodified and an empty string (by default) or `None` if *missing_as_none* is true.

The return value is a `named tuple`{.interpreted-text role="term"}, its items can be accessed by index or as named attributes:

  -------------------------------------------------------------------------------------------------------
  Attribute                                   Index   Value                  Value if not present
  ------------------------------------------- ------- ---------------------- ----------------------------
  `url`{.interpreted-text role="attr"}        0       URL with no fragment   empty string

  `fragment`{.interpreted-text role="attr"}   1       Fragment identifier    `None` or empty string[^5]
  -------------------------------------------------------------------------------------------------------

See section `urlparse-result-object`{.interpreted-text role="ref"} for more information on the result object.

::: versionchanged
3.2 Result is a structured object rather than a simple 2-tuple.
:::

::: versionchanged
3.15 Added the *missing_as_none* parameter.
:::
:::::

::: function
unwrap(url)

Extract the url from a wrapped URL (that is, a string formatted as `<URL:scheme://host/path>`, `<scheme://host/path>`, `URL:scheme://host/path` or `scheme://host/path`). If *url* is not a wrapped URL, it is returned without changes.
:::

## URL parsing security

The `urlsplit`{.interpreted-text role="func"} and `urlparse`{.interpreted-text role="func"} APIs do not perform **validation** of inputs. They may not raise errors on inputs that other applications consider invalid. They may also succeed on some inputs that might not be considered URLs elsewhere. Their purpose is for practical functionality rather than purity.

Instead of raising an exception on unusual input, they may instead return some component parts as empty strings or `None` (depending on the value of the *missing_as_none* argument). Or components may contain more than perhaps they should.

We recommend that users of these APIs where the values may be used anywhere with security implications code defensively. Do some verification within your code before trusting a returned component part. Does that `scheme` make sense? Is that a sensible `path`? Is there anything strange about that `hostname`? etc.

What constitutes a URL is not universally well defined. Different applications have different needs and desired constraints. For instance the living [WHATWG spec](https://url.spec.whatwg.org/#concept-basic-url-parser) describes what user facing web clients such as a web browser require. While `3986`{.interpreted-text role="rfc"} is more general. These functions incorporate some aspects of both, but cannot be claimed compliant with either. The APIs and existing user code with expectations on specific behaviors predate both standards leading us to be very cautious about making API behavior changes.

## Parsing ASCII Encoded Bytes

The URL parsing functions were originally designed to operate on character strings only. In practice, it is useful to be able to manipulate properly quoted and encoded URLs as sequences of ASCII bytes. Accordingly, the URL parsing functions in this module all operate on `bytes`{.interpreted-text role="class"} and `bytearray`{.interpreted-text role="class"} objects in addition to `str`{.interpreted-text role="class"} objects.

If `str`{.interpreted-text role="class"} data is passed in, the result will also contain only `str`{.interpreted-text role="class"} data. If `bytes`{.interpreted-text role="class"} or `bytearray`{.interpreted-text role="class"} data is passed in, the result will contain only `bytes`{.interpreted-text role="class"} data.

Attempting to mix `str`{.interpreted-text role="class"} data with `bytes`{.interpreted-text role="class"} or `bytearray`{.interpreted-text role="class"} in a single function call will result in a `TypeError`{.interpreted-text role="exc"} being raised, while attempting to pass in non-ASCII byte values will trigger `UnicodeDecodeError`{.interpreted-text role="exc"}.

To support easier conversion of result objects between `str`{.interpreted-text role="class"} and `bytes`{.interpreted-text role="class"}, all return values from URL parsing functions provide either an `encode`{.interpreted-text role="meth"} method (when the result contains `str`{.interpreted-text role="class"} data) or a `decode`{.interpreted-text role="meth"} method (when the result contains `bytes`{.interpreted-text role="class"} data). The signatures of these methods match those of the corresponding `str`{.interpreted-text role="class"} and `bytes`{.interpreted-text role="class"} methods (except that the default encoding is `'ascii'` rather than `'utf-8'`). Each produces a value of a corresponding type that contains either `bytes`{.interpreted-text role="class"} data (for `encode`{.interpreted-text role="meth"} methods) or `str`{.interpreted-text role="class"} data (for `decode`{.interpreted-text role="meth"} methods).

Applications that need to operate on potentially improperly quoted URLs that may contain non-ASCII data will need to do their own decoding from bytes to characters before invoking the URL parsing methods.

The behaviour described in this section applies only to the URL parsing functions. The URL quoting functions use their own rules when producing or consuming byte sequences as detailed in the documentation of the individual URL quoting functions.

::: versionchanged
3.2 URL parsing functions now accept ASCII encoded byte sequences
:::

## Structured Parse Results {#urlparse-result-object}

The result objects from the `urlsplit`{.interpreted-text role="func"}, `urlparse`{.interpreted-text role="func"} and `urldefrag`{.interpreted-text role="func"} functions are subclasses of the `tuple`{.interpreted-text role="class"} type. These subclasses add the attributes listed in the documentation for those functions, the encoding and decoding support described in the previous section, as well as an additional method:

::: method
urllib.parse.SplitResult.geturl()

Return the re-combined version of the original URL as a string. This may differ from the original URL in that the scheme may be normalized to lower case and empty components may be dropped. Specifically, empty parameters, queries, and fragment identifiers will be removed unless the URL was parsed with `missing_as_none=True`.

For `urldefrag`{.interpreted-text role="func"} results, only empty fragment identifiers will be removed. For `urlsplit`{.interpreted-text role="func"} and `urlparse`{.interpreted-text role="func"} results, all noted changes will be made to the URL returned by this method.

The result of this method remains unchanged if passed back through the original parsing function:

> \>\>\> from urllib.parse import urlsplit \>\>\> url = \'HTTP://www.Python.org/doc/#\' \>\>\> r1 = urlsplit(url) \>\>\> r1.geturl() \'http://www.Python.org/doc/\' \>\>\> r2 = urlsplit(r1.geturl()) \>\>\> r2.geturl() \'http://www.Python.org/doc/\' \>\>\> r3 = urlsplit(url, missing_as_none=True) \>\>\> r3.geturl() \'http://www.Python.org/doc/#\'
:::

The following classes provide the implementations of the structured parse results when operating on `str`{.interpreted-text role="class"} objects:

:::: {.DefragResult(url, .fragment)}
Concrete class for `urldefrag`{.interpreted-text role="func"} results containing `str`{.interpreted-text role="class"} data. The `encode`{.interpreted-text role="meth"} method returns a `DefragResultBytes`{.interpreted-text role="class"} instance.

::: versionadded
3.2
:::
::::

::: {.ParseResult(scheme, .netloc, .path, .params, .query, .fragment)}
Concrete class for `urlparse`{.interpreted-text role="func"} results containing `str`{.interpreted-text role="class"} data. The `encode`{.interpreted-text role="meth"} method returns a `ParseResultBytes`{.interpreted-text role="class"} instance.
:::

::: {.SplitResult(scheme, .netloc, .path, .query, .fragment)}
Concrete class for `urlsplit`{.interpreted-text role="func"} results containing `str`{.interpreted-text role="class"} data. The `encode`{.interpreted-text role="meth"} method returns a `SplitResultBytes`{.interpreted-text role="class"} instance.
:::

The following classes provide the implementations of the parse results when operating on `bytes`{.interpreted-text role="class"} or `bytearray`{.interpreted-text role="class"} objects:

:::: {.DefragResultBytes(url, .fragment)}
Concrete class for `urldefrag`{.interpreted-text role="func"} results containing `bytes`{.interpreted-text role="class"} data. The `decode`{.interpreted-text role="meth"} method returns a `DefragResult`{.interpreted-text role="class"} instance.

::: versionadded
3.2
:::
::::

:::: {.ParseResultBytes(scheme, .netloc, .path, .params, .query, .fragment)}
Concrete class for `urlparse`{.interpreted-text role="func"} results containing `bytes`{.interpreted-text role="class"} data. The `decode`{.interpreted-text role="meth"} method returns a `ParseResult`{.interpreted-text role="class"} instance.

::: versionadded
3.2
:::
::::

:::: {.SplitResultBytes(scheme, .netloc, .path, .query, .fragment)}
Concrete class for `urlsplit`{.interpreted-text role="func"} results containing `bytes`{.interpreted-text role="class"} data. The `decode`{.interpreted-text role="meth"} method returns a `SplitResult`{.interpreted-text role="class"} instance.

::: versionadded
3.2
:::
::::

## URL Quoting

The URL quoting functions focus on taking program data and making it safe for use as URL components by quoting special characters and appropriately encoding non-ASCII text. They also support reversing these operations to recreate the original data from the contents of a URL component if that task isn\'t already covered by the URL parsing functions above.

:::: function
quote(string, safe=\'/\', encoding=None, errors=None)

Replace special characters in *string* using the `%{xx}`{.interpreted-text role="samp"} escape. Letters, digits, and the characters `'_.-~'` are never quoted. By default, this function is intended for quoting the path section of a URL. The optional *safe* parameter specifies additional ASCII characters that should not be quoted \-\-- its default value is `'/'`.

*string* may be either a `str`{.interpreted-text role="class"} or a `bytes`{.interpreted-text role="class"} object.

::: versionchanged
3.7 Moved from `2396`{.interpreted-text role="rfc"} to `3986`{.interpreted-text role="rfc"} for quoting URL strings. \"\~\" is now included in the set of unreserved characters.
:::

The optional *encoding* and *errors* parameters specify how to deal with non-ASCII characters, as accepted by the `str.encode`{.interpreted-text role="meth"} method. *encoding* defaults to `'utf-8'`. *errors* defaults to `'strict'`, meaning unsupported characters raise a `UnicodeEncodeError`{.interpreted-text role="class"}. *encoding* and *errors* must not be supplied if *string* is a `bytes`{.interpreted-text role="class"}, or a `TypeError`{.interpreted-text role="class"} is raised.

Note that `quote(string, safe, encoding, errors)` is equivalent to `quote_from_bytes(string.encode(encoding, errors), safe)`.

Example: `quote('/El Niño/')` yields `'/El%20Ni%C3%B1o/'`.
::::

::: function
quote_plus(string, safe=\'\', encoding=None, errors=None)

Like `quote`{.interpreted-text role="func"}, but also replace spaces with plus signs, as required for quoting HTML form values when building up a query string to go into a URL. Plus signs in the original string are escaped unless they are included in *safe*. It also does not have *safe* default to `'/'`.

Example: `quote_plus('/El Niño/')` yields `'%2FEl+Ni%C3%B1o%2F'`.
:::

::: function
quote_from_bytes(bytes, safe=\'/\')

Like `quote`{.interpreted-text role="func"}, but accepts a `bytes`{.interpreted-text role="class"} object rather than a `str`{.interpreted-text role="class"}, and does not perform string-to-bytes encoding.

Example: `quote_from_bytes(b'a&\xef')` yields `'a%26%EF'`.
:::

:::: function
unquote(string, encoding=\'utf-8\', errors=\'replace\')

Replace `%{xx}`{.interpreted-text role="samp"} escapes with their single-character equivalent. The optional *encoding* and *errors* parameters specify how to decode percent-encoded sequences into Unicode characters, as accepted by the `bytes.decode`{.interpreted-text role="meth"} method.

*string* may be either a `str`{.interpreted-text role="class"} or a `bytes`{.interpreted-text role="class"} object.

*encoding* defaults to `'utf-8'`. *errors* defaults to `'replace'`, meaning invalid sequences are replaced by a placeholder character.

Example: `unquote('/El%20Ni%C3%B1o/')` yields `'/El Niño/'`.

::: versionchanged
3.9 *string* parameter supports bytes and str objects (previously only str).
:::
::::

::: function
unquote_plus(string, encoding=\'utf-8\', errors=\'replace\')

Like `unquote`{.interpreted-text role="func"}, but also replace plus signs with spaces, as required for unquoting HTML form values.

*string* must be a `str`{.interpreted-text role="class"}.

Example: `unquote_plus('/El+Ni%C3%B1o/')` yields `'/El Niño/'`.
:::

::: function
unquote_to_bytes(string)

Replace `%{xx}`{.interpreted-text role="samp"} escapes with their single-octet equivalent, and return a `bytes`{.interpreted-text role="class"} object.

*string* may be either a `str`{.interpreted-text role="class"} or a `bytes`{.interpreted-text role="class"} object.

If it is a `str`{.interpreted-text role="class"}, unescaped non-ASCII characters in *string* are encoded into UTF-8 bytes.

Example: `unquote_to_bytes('a%26%EF')` yields `b'a&\xef'`.
:::

:::::: function
urlencode(query, doseq=False, safe=\'\', encoding=None, errors=None, quote_via=quote_plus)

Convert a mapping object or a sequence of two-element tuples, which may contain `str`{.interpreted-text role="class"} or `bytes`{.interpreted-text role="class"} objects, to a percent-encoded ASCII text string. If the resultant string is to be used as a *data* for POST operation with the `~urllib.request.urlopen`{.interpreted-text role="func"} function, then it should be encoded to bytes, otherwise it would result in a `TypeError`{.interpreted-text role="exc"}.

The resulting string is a series of `key=value` pairs separated by `'&'` characters, where both *key* and *value* are quoted using the *quote_via* function. By default, `quote_plus`{.interpreted-text role="func"} is used to quote the values, which means spaces are quoted as a `'+'` character and \'/\' characters are encoded as `%2F`, which follows the standard for GET requests (`application/x-www-form-urlencoded`). An alternate function that can be passed as *quote_via* is `quote`{.interpreted-text role="func"}, which will encode spaces as `%20` and not encode \'/\' characters. For maximum control of what is quoted, use `quote` and specify a value for *safe*.

When a sequence of two-element tuples is used as the *query* argument, the first element of each tuple is a key and the second is a value. The value element in itself can be a sequence and in that case, if the optional parameter *doseq* evaluates to `True`, individual `key=value` pairs separated by `'&'` are generated for each element of the value sequence for the key. The order of parameters in the encoded string will match the order of parameter tuples in the sequence.

The *safe*, *encoding*, and *errors* parameters are passed down to *quote_via* (the *encoding* and *errors* parameters are only passed when a query element is a `str`{.interpreted-text role="class"}).

To reverse this encoding process, `parse_qs`{.interpreted-text role="func"} and `parse_qsl`{.interpreted-text role="func"} are provided in this module to parse query strings into Python data structures.

Refer to `urllib examples <urllib-examples>`{.interpreted-text role="ref"} to find out how the `urllib.parse.urlencode`{.interpreted-text role="func"} method can be used for generating the query string of a URL or data for a POST request.

::: versionchanged
3.2 *query* supports bytes and string objects.
:::

::: versionchanged
3.5 Added the *quote_via* parameter.
:::

::: deprecated
3.14 Accepting objects with false values (like `0` and `[]`) except empty strings and byte-like objects and `None` is now deprecated.
:::
::::::

::: seealso

[WHATWG](https://url.spec.whatwg.org/) - URL Living standard

:   Working Group for the URL Standard that defines URLs, domains, IP addresses, the application/x-www-form-urlencoded format, and their API.

`3986`{.interpreted-text role="rfc"} - Uniform Resource Identifiers

:   This is the current standard (STD66). Any changes to urllib.parse module should conform to this. Certain deviations could be observed, which are mostly for backward compatibility purposes and for certain de-facto parsing requirements as commonly observed in major browsers.

`2732`{.interpreted-text role="rfc"} - Format for Literal IPv6 Addresses in URL\'s.

:   This specifies the parsing requirements of IPv6 URLs.

`2396`{.interpreted-text role="rfc"} - Uniform Resource Identifiers (URI): Generic Syntax

:   Document describing the generic syntactic requirements for both Uniform Resource Names (URNs) and Uniform Resource Locators (URLs).

`2368`{.interpreted-text role="rfc"} - The mailto URL scheme.

:   Parsing requirements for mailto URL schemes.

`1808`{.interpreted-text role="rfc"} - Relative Uniform Resource Locators

:   This Request For Comments includes the rules for joining an absolute and a relative URL, including a fair number of \"Abnormal Examples\" which govern the treatment of border cases.

`1738`{.interpreted-text role="rfc"} - Uniform Resource Locators (URL)

:   This specifies the formal syntax and semantics of absolute URLs.
:::

[^1]: Depending on the value of the *missing_as_none* argument.

[^2]: Depending on the value of the *missing_as_none* argument.

[^3]: Depending on the value of the *missing_as_none* argument.

[^4]: Depending on the value of the *missing_as_none* argument.

[^5]: Depending on the value of the *missing_as_none* argument.
