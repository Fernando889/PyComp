# `!http.cookiejar`{.interpreted-text role="mod"} \-\-- Cookie handling for HTTP clients

::: {.module synopsis="Classes for automatic handling of HTTP cookies."}
http.cookiejar
:::

**Source code:** `Lib/http/cookiejar.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

The `!http.cookiejar`{.interpreted-text role="mod"} module defines classes for automatic handling of HTTP cookies. It is useful for accessing websites that require small pieces of data \-- `cookies`{.interpreted-text role="dfn"} \-- to be set on the client machine by an HTTP response from a web server, and then returned to the server in later HTTP requests.

Both the regular Netscape cookie protocol and the protocol defined by `2965`{.interpreted-text role="rfc"} are handled. RFC 2965 handling is switched off by default. `2109`{.interpreted-text role="rfc"} cookies are parsed as Netscape cookies and subsequently treated either as Netscape or RFC 2965 cookies according to the \'policy\' in effect. Note that the great majority of cookies on the internet are Netscape cookies. `!http.cookiejar`{.interpreted-text role="mod"} attempts to follow the de-facto Netscape cookie protocol (which differs substantially from that set out in the original Netscape specification), including taking note of the `max-age` and `port` cookie-attributes introduced with RFC 2965.

:::: note
::: title
Note
:::

The various named parameters found in `Set-Cookie`{.interpreted-text role="mailheader"} and `Set-Cookie2`{.interpreted-text role="mailheader"} headers (eg. `domain` and `expires`) are conventionally referred to as `attributes`{.interpreted-text role="dfn"}. To distinguish them from Python attributes, the documentation for this module uses the term `cookie-attribute`{.interpreted-text role="dfn"} instead.
::::

The module defines the following exception:

:::: exception
LoadError

Instances of `FileCookieJar`{.interpreted-text role="class"} raise this exception on failure to load cookies from a file. `LoadError`{.interpreted-text role="exc"} is a subclass of `OSError`{.interpreted-text role="exc"}.

::: versionchanged
3.3 `LoadError`{.interpreted-text role="exc"} used to be a subtype of `IOError`{.interpreted-text role="exc"}, which is now an alias of `OSError`{.interpreted-text role="exc"}.
:::
::::

The following classes are provided:

::: CookieJar(policy=None)
*policy* is an object implementing the `CookiePolicy`{.interpreted-text role="class"} interface.

The `CookieJar`{.interpreted-text role="class"} class stores HTTP cookies. It extracts cookies from HTTP requests, and returns them in HTTP responses. `CookieJar`{.interpreted-text role="class"} instances automatically expire contained cookies when necessary. Subclasses are also responsible for storing and retrieving cookies from a file or database.
:::

:::: {.FileCookieJar(filename=None, .delayload=None, .policy=None)}
*policy* is an object implementing the `CookiePolicy`{.interpreted-text role="class"} interface. For the other arguments, see the documentation for the corresponding attributes.

A `CookieJar`{.interpreted-text role="class"} which can load cookies from, and perhaps save cookies to, a file on disk. Cookies are **NOT** loaded from the named file until either the `load`{.interpreted-text role="meth"} or `revert`{.interpreted-text role="meth"} method is called. Subclasses of this class are documented in section `file-cookie-jar-classes`{.interpreted-text role="ref"}.

This should not be initialized directly -- use its subclasses below instead.

::: versionchanged
3.8

The filename parameter supports a `path-like object`{.interpreted-text role="term"}.
:::
::::

::: CookiePolicy()
This class is responsible for deciding whether each cookie should be accepted from / returned to the server.
:::

::: {.DefaultCookiePolicy( .blocked_domains=None, .allowed_domains=None, .netscape=True, .rfc2965=False, .rfc2109_as_netscape=None, .hide_cookie2=False, .strict_domain=False, .strict_rfc2965_unverifiable=True, .strict_ns_unverifiable=False, .strict_ns_domain=DefaultCookiePolicy.DomainLiberal, .strict_ns_set_initial_dollar=False, .strict_ns_set_path=False, .secure_protocols=(\"https\", .\"wss\") .)}
Constructor arguments should be passed as keyword arguments only. *blocked_domains* is a sequence of domain names that we never accept cookies from, nor return cookies to. *allowed_domains* if not `None`{.interpreted-text role="const"}, this is a sequence of the only domains for which we accept and return cookies. *secure_protocols* is a sequence of protocols for which secure cookies can be added to. By default *https* and *wss* (secure websocket) are considered secure protocols. For all other arguments, see the documentation for `CookiePolicy`{.interpreted-text role="class"} and `DefaultCookiePolicy`{.interpreted-text role="class"} objects.

`DefaultCookiePolicy`{.interpreted-text role="class"} implements the standard accept / reject rules for Netscape and `2965`{.interpreted-text role="rfc"} cookies. By default, `2109`{.interpreted-text role="rfc"} cookies (ie. cookies received in a `Set-Cookie`{.interpreted-text role="mailheader"} header with a version cookie-attribute of 1) are treated according to the RFC 2965 rules. However, if RFC 2965 handling is turned off or `rfc2109_as_netscape`{.interpreted-text role="attr"} is `True`, RFC 2109 cookies are \'downgraded\' by the `CookieJar`{.interpreted-text role="class"} instance to Netscape cookies, by setting the `version`{.interpreted-text role="attr"} attribute of the `Cookie`{.interpreted-text role="class"} instance to 0. `DefaultCookiePolicy`{.interpreted-text role="class"} also provides some parameters to allow some fine-tuning of policy.
:::

::: Cookie()
This class represents Netscape, `2109`{.interpreted-text role="rfc"} and `2965`{.interpreted-text role="rfc"} cookies. It is not expected that users of `!http.cookiejar`{.interpreted-text role="mod"} construct their own `Cookie`{.interpreted-text role="class"} instances. Instead, if necessary, call `make_cookies`{.interpreted-text role="meth"} on a `CookieJar`{.interpreted-text role="class"} instance.
:::

::: seealso

Module `urllib.request`{.interpreted-text role="mod"}

:   URL opening with automatic cookie handling.

Module `http.cookies`{.interpreted-text role="mod"}

:   HTTP cookie classes, principally useful for server-side code. The `!http.cookiejar`{.interpreted-text role="mod"} and `http.cookies`{.interpreted-text role="mod"} modules do not depend on each other.

<https://curl.se/rfc/cookie_spec.html>

:   The specification of the original Netscape cookie protocol. Though this is still the dominant protocol, the \'Netscape cookie protocol\' implemented by all the major browsers (and `!http.cookiejar`{.interpreted-text role="mod"}) only bears a passing resemblance to the one sketched out in `cookie_spec.html`.

`2109`{.interpreted-text role="rfc"} - HTTP State Management Mechanism

:   Obsoleted by `2965`{.interpreted-text role="rfc"}. Uses `Set-Cookie`{.interpreted-text role="mailheader"} with version=1.

`2965`{.interpreted-text role="rfc"} - HTTP State Management Mechanism

:   The Netscape protocol with the bugs fixed. Uses `Set-Cookie2`{.interpreted-text role="mailheader"} in place of `Set-Cookie`{.interpreted-text role="mailheader"}. Not widely used.

<https://kristol.org/cookie/errata.html>

:   Unfinished errata to `2965`{.interpreted-text role="rfc"}.

`2964`{.interpreted-text role="rfc"} - Use of HTTP State Management
:::

## CookieJar and FileCookieJar Objects {#cookie-jar-objects}

`CookieJar`{.interpreted-text role="class"} objects support the `iterator`{.interpreted-text role="term"} protocol for iterating over contained `Cookie`{.interpreted-text role="class"} objects.

`CookieJar`{.interpreted-text role="class"} has the following methods:

:::: method
CookieJar.add_cookie_header(request)

Add correct `Cookie`{.interpreted-text role="mailheader"} header to *request*.

If policy allows (ie. the `rfc2965`{.interpreted-text role="attr"} and `hide_cookie2`{.interpreted-text role="attr"} attributes of the `CookieJar`{.interpreted-text role="class"}\'s `CookiePolicy`{.interpreted-text role="class"} instance are true and false respectively), the `Cookie2`{.interpreted-text role="mailheader"} header is also added when appropriate.

The *request* object (usually a `urllib.request.Request`{.interpreted-text role="class"} instance) must support the methods `get_full_url`{.interpreted-text role="meth"}, `has_header`{.interpreted-text role="meth"}, `get_header`{.interpreted-text role="meth"}, `header_items`{.interpreted-text role="meth"}, `add_unredirected_header`{.interpreted-text role="meth"} and the attributes `host`{.interpreted-text role="attr"}, `!type`{.interpreted-text role="attr"}, `unverifiable`{.interpreted-text role="attr"} and `origin_req_host`{.interpreted-text role="attr"} as documented by `urllib.request`{.interpreted-text role="mod"}.

::: versionchanged
3.3

*request* object needs `origin_req_host`{.interpreted-text role="attr"} attribute. Dependency on a deprecated method `get_origin_req_host`{.interpreted-text role="meth"} has been removed.
:::
::::

:::: method
CookieJar.extract_cookies(response, request)

Extract cookies from HTTP *response* and store them in the `CookieJar`{.interpreted-text role="class"}, where allowed by policy.

The `CookieJar`{.interpreted-text role="class"} will look for allowable `Set-Cookie`{.interpreted-text role="mailheader"} and `Set-Cookie2`{.interpreted-text role="mailheader"} headers in the *response* argument, and store cookies as appropriate (subject to the `CookiePolicy.set_ok`{.interpreted-text role="meth"} method\'s approval).

The *response* object (usually the result of a call to `urllib.request.urlopen`{.interpreted-text role="meth"}, or similar) should support an `info`{.interpreted-text role="meth"} method, which returns an `email.message.Message`{.interpreted-text role="class"} instance.

The *request* object (usually a `urllib.request.Request`{.interpreted-text role="class"} instance) must support the method `get_full_url`{.interpreted-text role="meth"} and the attributes `host`{.interpreted-text role="attr"}, `unverifiable`{.interpreted-text role="attr"} and `origin_req_host`{.interpreted-text role="attr"}, as documented by `urllib.request`{.interpreted-text role="mod"}. The request is used to set default values for cookie-attributes as well as for checking that the cookie is allowed to be set.

::: versionchanged
3.3

*request* object needs `origin_req_host`{.interpreted-text role="attr"} attribute. Dependency on a deprecated method `get_origin_req_host`{.interpreted-text role="meth"} has been removed.
:::
::::

::: method
CookieJar.set_policy(policy)

Set the `CookiePolicy`{.interpreted-text role="class"} instance to be used.
:::

::: method
CookieJar.make_cookies(response, request)

Return sequence of `Cookie`{.interpreted-text role="class"} objects extracted from *response* object.

See the documentation for `extract_cookies`{.interpreted-text role="meth"} for the interfaces required of the *response* and *request* arguments.
:::

::: method
CookieJar.set_cookie_if_ok(cookie, request)

Set a `Cookie`{.interpreted-text role="class"} if policy says it\'s OK to do so.
:::

::: method
CookieJar.set_cookie(cookie)

Set a `Cookie`{.interpreted-text role="class"}, without checking with policy to see whether or not it should be set.
:::

::: method
CookieJar.clear(\[domain\[, path\[, name\]\]\])

Clear some cookies.

If invoked without arguments, clear all cookies. If given a single argument, only cookies belonging to that *domain* will be removed. If given two arguments, cookies belonging to the specified *domain* and URL *path* are removed. If given three arguments, then the cookie with the specified *domain*, *path* and *name* is removed.

Raises `KeyError`{.interpreted-text role="exc"} if no matching cookie exists.
:::

::: method
CookieJar.clear_session_cookies()

Discard all session cookies.

Discards all contained cookies that have a true `discard`{.interpreted-text role="attr"} attribute (usually because they had either no `max-age` or `expires` cookie-attribute, or an explicit `discard` cookie-attribute). For interactive browsers, the end of a session usually corresponds to closing the browser window.

Note that the `save`{.interpreted-text role="meth"} method won\'t save session cookies anyway, unless you ask otherwise by passing a true *ignore_discard* argument.
:::

`FileCookieJar`{.interpreted-text role="class"} implements the following additional methods:

::: method
FileCookieJar.save(filename=None, ignore_discard=False, ignore_expires=False)

Save cookies to a file.

This base class raises `NotImplementedError`{.interpreted-text role="exc"}. Subclasses may leave this method unimplemented.

*filename* is the name of file in which to save cookies. If *filename* is not specified, `self.filename`{.interpreted-text role="attr"} is used (whose default is the value passed to the constructor, if any); if `self.filename`{.interpreted-text role="attr"} is `None`{.interpreted-text role="const"}, `ValueError`{.interpreted-text role="exc"} is raised.

*ignore_discard*: save even cookies set to be discarded. *ignore_expires*: save even cookies that have expired

The file is overwritten if it already exists, thus wiping all the cookies it contains. Saved cookies can be restored later using the `load`{.interpreted-text role="meth"} or `revert`{.interpreted-text role="meth"} methods.
:::

:::: method
FileCookieJar.load(filename=None, ignore_discard=False, ignore_expires=False)

Load cookies from a file.

Old cookies are kept unless overwritten by newly loaded ones.

Arguments are as for `save`{.interpreted-text role="meth"}.

The named file must be in the format understood by the class, or `LoadError`{.interpreted-text role="exc"} will be raised. Also, `OSError`{.interpreted-text role="exc"} may be raised, for example if the file does not exist.

::: versionchanged
3.3 `IOError`{.interpreted-text role="exc"} used to be raised, it is now an alias of `OSError`{.interpreted-text role="exc"}.
:::
::::

::: method
FileCookieJar.revert(filename=None, ignore_discard=False, ignore_expires=False)

Clear all cookies and reload cookies from a saved file.

`revert`{.interpreted-text role="meth"} can raise the same exceptions as `load`{.interpreted-text role="meth"}. If there is a failure, the object\'s state will not be altered.
:::

`FileCookieJar`{.interpreted-text role="class"} instances have the following public attributes:

::: attribute
FileCookieJar.filename

Filename of default file in which to keep cookies. This attribute may be assigned to.
:::

::: attribute
FileCookieJar.delayload

If true, load cookies lazily from disk. This attribute should not be assigned to. This is only a hint, since this only affects performance, not behaviour (unless the cookies on disk are changing). A `CookieJar`{.interpreted-text role="class"} object may ignore it. None of the `FileCookieJar`{.interpreted-text role="class"} classes included in the standard library lazily loads cookies.
:::

## FileCookieJar subclasses and co-operation with web browsers {#file-cookie-jar-classes}

The following `CookieJar`{.interpreted-text role="class"} subclasses are provided for reading and writing.

::::::: {.MozillaCookieJar(filename=None, .delayload=None, .policy=None)}
A `FileCookieJar`{.interpreted-text role="class"} that can load from and save cookies to disk in the Mozilla `cookies.txt` file format (which is also used by curl and the Lynx and Netscape browsers).

:::: note
::: title
Note
:::

This loses information about `2965`{.interpreted-text role="rfc"} cookies, and also about newer or non-standard cookie-attributes such as `port`.
::::

:::: warning
::: title
Warning
:::

Back up your cookies before saving if you have cookies whose loss / corruption would be inconvenient (there are some subtleties which may lead to slight changes in the file over a load / save round-trip).
::::

Also note that cookies saved while Mozilla is running will get clobbered by Mozilla.
:::::::

:::: {.LWPCookieJar(filename=None, .delayload=None, .policy=None)}
A `FileCookieJar`{.interpreted-text role="class"} that can load from and save cookies to disk in format compatible with the libwww-perl library\'s `Set-Cookie3` file format. This is convenient if you want to store cookies in a human-readable file.

::: versionchanged
3.8

The filename parameter supports a `path-like object`{.interpreted-text role="term"}.
:::
::::

## CookiePolicy Objects {#cookie-policy-objects}

Objects implementing the `CookiePolicy`{.interpreted-text role="class"} interface have the following methods:

::: method
CookiePolicy.set_ok(cookie, request)

Return boolean value indicating whether cookie should be accepted from server.

*cookie* is a `Cookie`{.interpreted-text role="class"} instance. *request* is an object implementing the interface defined by the documentation for `CookieJar.extract_cookies`{.interpreted-text role="meth"}.
:::

::: method
CookiePolicy.return_ok(cookie, request)

Return boolean value indicating whether cookie should be returned to server.

*cookie* is a `Cookie`{.interpreted-text role="class"} instance. *request* is an object implementing the interface defined by the documentation for `CookieJar.add_cookie_header`{.interpreted-text role="meth"}.
:::

::: method
CookiePolicy.domain_return_ok(domain, request)

Return `False` if cookies should not be returned, given cookie domain.

This method is an optimization. It removes the need for checking every cookie with a particular domain (which might involve reading many files). Returning true from `domain_return_ok`{.interpreted-text role="meth"} and `path_return_ok`{.interpreted-text role="meth"} leaves all the work to `return_ok`{.interpreted-text role="meth"}.

If `domain_return_ok`{.interpreted-text role="meth"} returns true for the cookie domain, `path_return_ok`{.interpreted-text role="meth"} is called for the cookie path. Otherwise, `path_return_ok`{.interpreted-text role="meth"} and `return_ok`{.interpreted-text role="meth"} are never called for that cookie domain. If `path_return_ok`{.interpreted-text role="meth"} returns true, `return_ok`{.interpreted-text role="meth"} is called with the `Cookie`{.interpreted-text role="class"} object itself for a full check. Otherwise, `return_ok`{.interpreted-text role="meth"} is never called for that cookie path.

Note that `domain_return_ok`{.interpreted-text role="meth"} is called for every *cookie* domain, not just for the *request* domain. For example, the function might be called with both `".example.com"` and `"www.example.com"` if the request domain is `"www.example.com"`. The same goes for `path_return_ok`{.interpreted-text role="meth"}.

The *request* argument is as documented for `return_ok`{.interpreted-text role="meth"}.
:::

::: method
CookiePolicy.path_return_ok(path, request)

Return `False` if cookies should not be returned, given cookie path.

See the documentation for `domain_return_ok`{.interpreted-text role="meth"}.
:::

In addition to implementing the methods above, implementations of the `CookiePolicy`{.interpreted-text role="class"} interface must also supply the following attributes, indicating which protocols should be used, and how. All of these attributes may be assigned to.

::: attribute
CookiePolicy.netscape

Implement Netscape protocol.
:::

::: attribute
CookiePolicy.rfc2965

Implement `2965`{.interpreted-text role="rfc"} protocol.
:::

::: attribute
CookiePolicy.hide_cookie2

Don\'t add `Cookie2`{.interpreted-text role="mailheader"} header to requests (the presence of this header indicates to the server that we understand `2965`{.interpreted-text role="rfc"} cookies).
:::

The most useful way to define a `CookiePolicy`{.interpreted-text role="class"} class is by subclassing from `DefaultCookiePolicy`{.interpreted-text role="class"} and overriding some or all of the methods above. `CookiePolicy`{.interpreted-text role="class"} itself may be used as a \'null policy\' to allow setting and receiving any and all cookies (this is unlikely to be useful).

## DefaultCookiePolicy Objects {#default-cookie-policy-objects}

Implements the standard rules for accepting and returning cookies.

Both `2965`{.interpreted-text role="rfc"} and Netscape cookies are covered. RFC 2965 handling is switched off by default.

The easiest way to provide your own policy is to override this class and call its methods in your overridden implementations before adding your own additional checks:

    import http.cookiejar
    class MyCookiePolicy(http.cookiejar.DefaultCookiePolicy):
        def set_ok(self, cookie, request):
            if not http.cookiejar.DefaultCookiePolicy.set_ok(self, cookie, request):
                return False
            if i_dont_want_to_store_this_cookie(cookie):
                return False
            return True

In addition to the features required to implement the `CookiePolicy`{.interpreted-text role="class"} interface, this class allows you to block and allow domains from setting and receiving cookies. There are also some strictness switches that allow you to tighten up the rather loose Netscape protocol rules a little bit (at the cost of blocking some benign cookies).

A domain blocklist and allowlist is provided (both off by default). Only domains not in the blocklist and present in the allowlist (if the allowlist is active) participate in cookie setting and returning. Use the *blocked_domains* constructor argument, and `blocked_domains`{.interpreted-text role="meth"} and `set_blocked_domains`{.interpreted-text role="meth"} methods (and the corresponding argument and methods for *allowed_domains*). If you set an allowlist, you can turn it off again by setting it to `None`{.interpreted-text role="const"}.

Domains in block or allow lists that do not start with a dot must equal the cookie domain to be matched. For example, `"example.com"` matches a blocklist entry of `"example.com"`, but `"www.example.com"` does not. Domains that do start with a dot are matched by more specific domains too. For example, both `"www.example.com"` and `"www.coyote.example.com"` match `".example.com"` (but `"example.com"` itself does not). IP addresses are an exception, and must match exactly. For example, if blocked_domains contains `"192.168.1.2"` and `".168.1.2"`, 192.168.1.2 is blocked, but 193.168.1.2 is not.

`DefaultCookiePolicy`{.interpreted-text role="class"} implements the following additional methods:

::: method
DefaultCookiePolicy.blocked_domains()

Return the sequence of blocked domains (as a tuple).
:::

::: method
DefaultCookiePolicy.set_blocked_domains(blocked_domains)

Set the sequence of blocked domains.
:::

::: method
DefaultCookiePolicy.is_blocked(domain)

Return `True` if *domain* is on the blocklist for setting or receiving cookies.
:::

::: method
DefaultCookiePolicy.allowed_domains()

Return `None`{.interpreted-text role="const"}, or the sequence of allowed domains (as a tuple).
:::

::: method
DefaultCookiePolicy.set_allowed_domains(allowed_domains)

Set the sequence of allowed domains, or `None`{.interpreted-text role="const"}.
:::

::: method
DefaultCookiePolicy.is_not_allowed(domain)

Return `True` if *domain* is not on the allowlist for setting or receiving cookies.
:::

`DefaultCookiePolicy`{.interpreted-text role="class"} instances have the following attributes, which are all initialised from the constructor arguments of the same name, and which may all be assigned to.

::: attribute
DefaultCookiePolicy.rfc2109_as_netscape

If true, request that the `CookieJar`{.interpreted-text role="class"} instance downgrade `2109`{.interpreted-text role="rfc"} cookies (ie. cookies received in a `Set-Cookie`{.interpreted-text role="mailheader"} header with a version cookie-attribute of 1) to Netscape cookies by setting the version attribute of the `Cookie`{.interpreted-text role="class"} instance to 0. The default value is `None`{.interpreted-text role="const"}, in which case RFC 2109 cookies are downgraded if and only if `2965`{.interpreted-text role="rfc"} handling is turned off. Therefore, RFC 2109 cookies are downgraded by default.
:::

General strictness switches:

::: attribute
DefaultCookiePolicy.strict_domain

Don\'t allow sites to set two-component domains with country-code top-level domains like `.co.uk`, `.gov.uk`, `.co.nz`.etc. This is far from perfect and isn\'t guaranteed to work!
:::

`2965`{.interpreted-text role="rfc"} protocol strictness switches:

::: attribute
DefaultCookiePolicy.strict_rfc2965_unverifiable

Follow `2965`{.interpreted-text role="rfc"} rules on unverifiable transactions (usually, an unverifiable transaction is one resulting from a redirect or a request for an image hosted on another site). If this is false, cookies are *never* blocked on the basis of verifiability
:::

Netscape protocol strictness switches:

::: attribute
DefaultCookiePolicy.strict_ns_unverifiable

Apply `2965`{.interpreted-text role="rfc"} rules on unverifiable transactions even to Netscape cookies.
:::

::: attribute
DefaultCookiePolicy.strict_ns_domain

Flags indicating how strict to be with domain-matching rules for Netscape cookies. See below for acceptable values.
:::

::: attribute
DefaultCookiePolicy.strict_ns_set_initial_dollar

Ignore cookies in Set-Cookie: headers that have names starting with `'$'`.
:::

::: attribute
DefaultCookiePolicy.strict_ns_set_path

Don\'t allow setting cookies whose path doesn\'t path-match request URI.
:::

`~DefaultCookiePolicy.strict_ns_domain`{.interpreted-text role="attr"} is a collection of flags. Its value is constructed by or-ing together (for example, `DomainStrictNoDots|DomainStrictNonDomain` means both flags are set).

::: attribute
DefaultCookiePolicy.DomainStrictNoDots

When setting cookies, the \'host prefix\' must not contain a dot (eg. `www.foo.bar.com` can\'t set a cookie for `.bar.com`, because `www.foo` contains a dot).
:::

::: attribute
DefaultCookiePolicy.DomainStrictNonDomain

Cookies that did not explicitly specify a `domain` cookie-attribute can only be returned to a domain equal to the domain that set the cookie (eg. `spam.example.com` won\'t be returned cookies from `example.com` that had no `domain` cookie-attribute).
:::

::: attribute
DefaultCookiePolicy.DomainRFC2965Match

When setting cookies, require a full `2965`{.interpreted-text role="rfc"} domain-match.
:::

The following attributes are provided for convenience, and are the most useful combinations of the above flags:

::: attribute
DefaultCookiePolicy.DomainLiberal

Equivalent to 0 (ie. all of the above Netscape domain strictness flags switched off).
:::

::: attribute
DefaultCookiePolicy.DomainStrict

Equivalent to `DomainStrictNoDots|DomainStrictNonDomain`.
:::

## Cookie Objects

`Cookie`{.interpreted-text role="class"} instances have Python attributes roughly corresponding to the standard cookie-attributes specified in the various cookie standards. The correspondence is not one-to-one, because there are complicated rules for assigning default values, because the `max-age` and `expires` cookie-attributes contain equivalent information, and because `2109`{.interpreted-text role="rfc"} cookies may be \'downgraded\' by `!http.cookiejar`{.interpreted-text role="mod"} from version 1 to version 0 (Netscape) cookies.

Assignment to these attributes should not be necessary other than in rare circumstances in a `CookiePolicy`{.interpreted-text role="class"} method. The class does not enforce internal consistency, so you should know what you\'re doing if you do that.

::: attribute
Cookie.version

Integer or `None`{.interpreted-text role="const"}. Netscape cookies have `version`{.interpreted-text role="attr"} 0. `2965`{.interpreted-text role="rfc"} and `2109`{.interpreted-text role="rfc"} cookies have a `version` cookie-attribute of 1. However, note that `!http.cookiejar`{.interpreted-text role="mod"} may \'downgrade\' RFC 2109 cookies to Netscape cookies, in which case `version`{.interpreted-text role="attr"} is 0.
:::

::: attribute
Cookie.name

Cookie name (a string).
:::

::: attribute
Cookie.value

Cookie value (a string), or `None`{.interpreted-text role="const"}.
:::

::: attribute
Cookie.port

String representing a port or a set of ports (eg. \'80\', or \'80,8080\'), or `None`{.interpreted-text role="const"}.
:::

::: attribute
Cookie.domain

Cookie domain (a string).
:::

::: attribute
Cookie.path

Cookie path (a string, eg. `'/acme/rocket_launchers'`).
:::

::: attribute
Cookie.secure

`True` if cookie should only be returned over a secure connection.
:::

::: attribute
Cookie.expires

Integer expiry date in seconds since epoch, or `None`{.interpreted-text role="const"}. See also the `is_expired`{.interpreted-text role="meth"} method.
:::

::: attribute
Cookie.discard

`True` if this is a session cookie.
:::

::: attribute
Cookie.comment

String comment from the server explaining the function of this cookie, or `None`{.interpreted-text role="const"}.
:::

::: attribute
Cookie.comment_url

URL linking to a comment from the server explaining the function of this cookie, or `None`{.interpreted-text role="const"}.
:::

::: attribute
Cookie.rfc2109

`True` if this cookie was received as an `2109`{.interpreted-text role="rfc"} cookie (ie. the cookie arrived in a `Set-Cookie`{.interpreted-text role="mailheader"} header, and the value of the Version cookie-attribute in that header was 1). This attribute is provided because `!http.cookiejar`{.interpreted-text role="mod"} may \'downgrade\' RFC 2109 cookies to Netscape cookies, in which case `version`{.interpreted-text role="attr"} is 0.
:::

::: attribute
Cookie.port_specified

`True` if a port or set of ports was explicitly specified by the server (in the `Set-Cookie`{.interpreted-text role="mailheader"} / `Set-Cookie2`{.interpreted-text role="mailheader"} header).
:::

::: attribute
Cookie.domain_specified

`True` if a domain was explicitly specified by the server.
:::

::: attribute
Cookie.domain_initial_dot

`True` if the domain explicitly specified by the server began with a dot (`'.'`).
:::

Cookies may have additional non-standard cookie-attributes. These may be accessed using the following methods:

::: method
Cookie.has_nonstandard_attr(name)

Return `True` if cookie has the named cookie-attribute.
:::

::: method
Cookie.get_nonstandard_attr(name, default=None)

If cookie has the named cookie-attribute, return its value. Otherwise, return *default*.
:::

::: method
Cookie.set_nonstandard_attr(name, value)

Set the value of the named cookie-attribute.
:::

The `Cookie`{.interpreted-text role="class"} class also defines the following method:

::: method
Cookie.is_expired(now=None)

`True` if cookie has passed the time at which the server requested it should expire. If *now* is given (in seconds since the epoch), return whether the cookie has expired at the specified time.
:::

## Examples

The first example shows the most common usage of `!http.cookiejar`{.interpreted-text role="mod"}:

    import http.cookiejar, urllib.request
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    r = opener.open("http://example.com/")

This example illustrates how to open a URL using your Netscape, Mozilla, or Lynx cookies (assumes Unix/Netscape convention for location of the cookies file):

    import os, http.cookiejar, urllib.request
    cj = http.cookiejar.MozillaCookieJar()
    cj.load(os.path.join(os.path.expanduser("~"), ".netscape", "cookies.txt"))
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    r = opener.open("http://example.com/")

The next example illustrates the use of `DefaultCookiePolicy`{.interpreted-text role="class"}. Turn on `2965`{.interpreted-text role="rfc"} cookies, be more strict about domains when setting and returning Netscape cookies, and block some domains from setting cookies or having them returned:

    import urllib.request
    from http.cookiejar import CookieJar, DefaultCookiePolicy
    policy = DefaultCookiePolicy(
        rfc2965=True, strict_ns_domain=Policy.DomainStrict,
        blocked_domains=["ads.net", ".ads.net"])
    cj = CookieJar(policy)
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    r = opener.open("http://example.com/")
