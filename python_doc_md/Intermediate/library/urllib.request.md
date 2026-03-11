# `!urllib.request`{.interpreted-text role="mod"} \-\-- Extensible library for opening URLs

::: {.module synopsis="Extensible library for opening URLs."}
urllib.request
:::

**Source code:** `Lib/urllib/request.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

The `!urllib.request`{.interpreted-text role="mod"} module defines functions and classes which help in opening URLs (mostly HTTP) in a complex world \-\-- basic and digest authentication, redirections, cookies and more.

::: seealso
The [Requests package](https://requests.readthedocs.io/en/master/) is recommended for a higher-level HTTP client interface.
:::

:::: warning
::: title
Warning
:::

On macOS it is unsafe to use this module in programs using `os.fork`{.interpreted-text role="func"} because the `getproxies`{.interpreted-text role="func"} implementation for macOS uses a higher-level system API. Set the environment variable `no_proxy` to `*` to avoid this problem (e.g. `os.environ["no_proxy"] = "*"`).
::::

::: availability
not WASI.

This module does not work or is not available on WebAssembly. See `wasm-availability`{.interpreted-text role="ref"} for more information.
:::

The `!urllib.request`{.interpreted-text role="mod"} module defines the following functions:

::::::::: function
urlopen(url, data=None\[, timeout\], \*, context=None)

Open *url*, which can be either a string containing a valid, properly encoded URL, or a `Request`{.interpreted-text role="class"} object.

*data* must be an object specifying additional data to be sent to the server, or `None` if no such data is needed. See `Request`{.interpreted-text role="class"} for details.

urllib.request module uses HTTP/1.1 and includes `Connection:close` header in its HTTP requests.

The optional *timeout* parameter specifies a timeout in seconds for blocking operations like the connection attempt (if not specified, the global default timeout setting will be used). This actually only works for HTTP, HTTPS and FTP connections.

If *context* is specified, it must be a `ssl.SSLContext`{.interpreted-text role="class"} instance describing the various SSL options. See `~http.client.HTTPSConnection`{.interpreted-text role="class"} for more details.

This function always returns an object which can work as a `context manager`{.interpreted-text role="term"} and has the properties *url*, *headers*, and *status*. See `urllib.response.addinfourl`{.interpreted-text role="class"} for more detail on these properties.

For HTTP and HTTPS URLs, this function returns a `http.client.HTTPResponse`{.interpreted-text role="class"} object slightly modified. In addition to the three new methods above, the msg attribute contains the same information as the `~http.client.HTTPResponse.reason`{.interpreted-text role="attr"} attribute \-\-- the reason phrase returned by server \-\-- instead of the response headers as it is specified in the documentation for `~http.client.HTTPResponse`{.interpreted-text role="class"}.

For FTP, file, and data URLs, this function returns a `urllib.response.addinfourl`{.interpreted-text role="class"} object.

Raises `~urllib.error.URLError`{.interpreted-text role="exc"} on protocol errors.

Note that `None` may be returned if no handler handles the request (though the default installed global `OpenerDirector`{.interpreted-text role="class"} uses `UnknownHandler`{.interpreted-text role="class"} to ensure this never happens).

In addition, if proxy settings are detected (for example, when a `*_proxy` environment variable like `!http_proxy`{.interpreted-text role="envvar"} is set), `ProxyHandler`{.interpreted-text role="class"} is default installed and makes sure the requests are handled through the proxy.

The legacy `urllib.urlopen` function from Python 2.6 and earlier has been discontinued; `urllib.request.urlopen`{.interpreted-text role="func"} corresponds to the old `urllib2.urlopen`. Proxy handling, which was done by passing a dictionary parameter to `urllib.urlopen`, can be obtained by using `ProxyHandler`{.interpreted-text role="class"} objects.

::: audit-event
urllib.Request fullurl,data,headers,method urllib.request.urlopen

The default opener raises an `auditing event <auditing>`{.interpreted-text role="ref"} `urllib.Request` with arguments `fullurl`, `data`, `headers`, `method` taken from the request object.
:::

::: versionchanged
3.2 *cafile* and *capath* were added.

HTTPS virtual hosts are now supported if possible (that is, if `ssl.HAS_SNI`{.interpreted-text role="const"} is true).

*data* can be an iterable object.
:::

::: versionchanged
3.3 *cadefault* was added.
:::

::: versionchanged
3.4.3 *context* was added.
:::

::: versionchanged
3.10 HTTPS connection now send an ALPN extension with protocol indicator `http/1.1` when no *context* is given. Custom *context* should set ALPN protocols with `~ssl.SSLContext.set_alpn_protocols`{.interpreted-text role="meth"}.
:::

::: versionchanged
3.13 Remove *cafile*, *capath* and *cadefault* parameters: use the *context* parameter instead.
:::
:::::::::

::: function
install_opener(opener)

Install an `OpenerDirector`{.interpreted-text role="class"} instance as the default global opener. Installing an opener is only necessary if you want urlopen to use that opener; otherwise, simply call `OpenerDirector.open`{.interpreted-text role="meth"} instead of `~urllib.request.urlopen`{.interpreted-text role="func"}. The code does not check for a real `OpenerDirector`{.interpreted-text role="class"}, and any class with the appropriate interface will work.
:::

::: function
build_opener(\[handler, \...\])

Return an `OpenerDirector`{.interpreted-text role="class"} instance, which chains the handlers in the order given. *handler*s can be either instances of `BaseHandler`{.interpreted-text role="class"}, or subclasses of `BaseHandler`{.interpreted-text role="class"} (in which case it must be possible to call the constructor without any parameters). Instances of the following classes will be in front of the *handler*s, unless the *handler*s contain them, instances of them or subclasses of them: `ProxyHandler`{.interpreted-text role="class"} (if proxy settings are detected), `UnknownHandler`{.interpreted-text role="class"}, `HTTPHandler`{.interpreted-text role="class"}, `HTTPDefaultErrorHandler`{.interpreted-text role="class"}, `HTTPRedirectHandler`{.interpreted-text role="class"}, `FTPHandler`{.interpreted-text role="class"}, `FileHandler`{.interpreted-text role="class"}, `HTTPErrorProcessor`{.interpreted-text role="class"}.

If the Python installation has SSL support (i.e., if the `ssl`{.interpreted-text role="mod"} module can be imported), `HTTPSHandler`{.interpreted-text role="class"} will also be added.

A `BaseHandler`{.interpreted-text role="class"} subclass may also change its `handler_order`{.interpreted-text role="attr"} attribute to modify its position in the handlers list.
:::

:::::: function
pathname2url(path, \*, add_scheme=False)

Convert the given local path to a `file:` URL. This function uses `~urllib.parse.quote`{.interpreted-text role="func"} function to encode the path.

If *add_scheme* is false (the default), the return value omits the `file:` scheme prefix. Set *add_scheme* to true to return a complete URL.

This example shows the function being used on Windows:

    >>> from urllib.request import pathname2url
    >>> path = 'C:\\Program Files'
    >>> pathname2url(path, add_scheme=True)
    'file:///C:/Program%20Files'

::: versionchanged
3.14 Windows drive letters are no longer converted to uppercase, and `:` characters not following a drive letter no longer cause an `OSError`{.interpreted-text role="exc"} exception to be raised on Windows.
:::

::: versionchanged
3.14 Paths beginning with a slash are converted to URLs with authority sections. For example, the path `/etc/hosts` is converted to the URL `///etc/hosts`.
:::

::: versionchanged
3.14 The *add_scheme* parameter was added.
:::
::::::

::::::: function
url2pathname(url, \*, require_scheme=False, resolve_host=False)

Convert the given `file:` URL to a local path. This function uses `~urllib.parse.unquote`{.interpreted-text role="func"} to decode the URL.

If *require_scheme* is false (the default), the given value should omit a `file:` scheme prefix. If *require_scheme* is set to true, the given value should include the prefix; a `~urllib.error.URLError`{.interpreted-text role="exc"} is raised if it doesn\'t.

The URL authority is discarded if it is empty, `localhost`, or the local hostname. Otherwise, if *resolve_host* is set to true, the authority is resolved using `socket.gethostbyname`{.interpreted-text role="func"} and discarded if it matches a local IP address (as per `RFC 8089 §3 <8089#section-3>`{.interpreted-text role="rfc"}). If the authority is still unhandled, then on Windows a UNC path is returned, and on other platforms a `~urllib.error.URLError`{.interpreted-text role="exc"} is raised.

This example shows the function being used on Windows:

    >>> from urllib.request import url2pathname
    >>> url = 'file:///C:/Program%20Files'
    >>> url2pathname(url, require_scheme=True)
    'C:\\Program Files'

::: versionchanged
3.14 Windows drive letters are no longer converted to uppercase, and `:` characters not following a drive letter no longer cause an `OSError`{.interpreted-text role="exc"} exception to be raised on Windows.
:::

::: versionchanged
3.14 The URL authority is discarded if it matches the local hostname. Otherwise, if the authority isn\'t empty or `localhost`, then on Windows a UNC path is returned (as before), and on other platforms a `~urllib.error.URLError`{.interpreted-text role="exc"} is raised.
:::

::: versionchanged
3.14 The URL query and fragment components are discarded if present.
:::

::: versionchanged
3.14 The *require_scheme* and *resolve_host* parameters were added.
:::
:::::::

::::: function
getproxies()

This helper function returns a dictionary of scheme to proxy server URL mappings. It scans the environment for variables named `<scheme>_proxy`, in a case insensitive approach, for all operating systems first, and when it cannot find it, looks for proxy information from System Configuration for macOS and Windows Systems Registry for Windows. If both lowercase and uppercase environment variables exist (and disagree), lowercase is preferred.

:::: note
::: title
Note
:::

If the environment variable `REQUEST_METHOD` is set, which usually indicates your script is running in a CGI environment, the environment variable `HTTP_PROXY` (uppercase `_PROXY`) will be ignored. This is because that variable can be injected by a client using the \"Proxy:\" HTTP header. If you need to use an HTTP proxy in a CGI environment, either use `ProxyHandler` explicitly, or make sure the variable name is in lowercase (or at least the `_proxy` suffix).
::::
:::::

The following classes are provided:

:::::::: {.Request(url, .data=None, .headers={}, .origin_req_host=None, .unverifiable=False, .method=None)}
This class is an abstraction of a URL request.

*url* should be a string containing a valid, properly encoded URL.

*data* must be an object specifying additional data to send to the server, or `None` if no such data is needed. Currently HTTP requests are the only ones that use *data*. The supported object types include bytes, file-like objects, and iterables of bytes-like objects. If no `Content-Length` nor `Transfer-Encoding` header field has been provided, `HTTPHandler`{.interpreted-text role="class"} will set these headers according to the type of *data*. `Content-Length` will be used to send bytes objects, while `Transfer-Encoding: chunked` as specified in `7230`{.interpreted-text role="rfc"}, Section 3.3.1 will be used to send files and other iterables.

For an HTTP POST request method, *data* should be a buffer in the standard `application/x-www-form-urlencoded`{.interpreted-text role="mimetype"} format. The `urllib.parse.urlencode`{.interpreted-text role="func"} function takes a mapping or sequence of 2-tuples and returns an ASCII string in this format. It should be encoded to bytes before being used as the *data* parameter.

*headers* should be a dictionary, and will be treated as if `add_header`{.interpreted-text role="meth"} was called with each key and value as arguments. This is often used to \"spoof\" the `User-Agent` header value, which is used by a browser to identify itself \-- some HTTP servers only allow requests coming from common browsers as opposed to scripts. For example, Mozilla Firefox may identify itself as `"Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"`, while `urllib`{.interpreted-text role="mod"}\'s default user agent string is `"Python-urllib/2.6"` (on Python 2.6). All header keys are sent in camel case.

An appropriate `Content-Type` header should be included if the *data* argument is present. If this header has not been provided and *data* is not `None`, `Content-Type: application/x-www-form-urlencoded` will be added as a default.

The next two arguments are only of interest for correct handling of third-party HTTP cookies:

*origin_req_host* should be the request-host of the origin transaction, as defined by `2965`{.interpreted-text role="rfc"}. It defaults to `http.cookiejar.request_host(self)`. This is the host name or IP address of the original request that was initiated by the user. For example, if the request is for an image in an HTML document, this should be the request-host of the request for the page containing the image.

*unverifiable* should indicate whether the request is unverifiable, as defined by `2965`{.interpreted-text role="rfc"}. It defaults to `False`. An unverifiable request is one whose URL the user did not have the option to approve. For example, if the request is for an image in an HTML document, and the user had no option to approve the automatic fetching of the image, this should be true.

*method* should be a string that indicates the HTTP request method that will be used (e.g. `'HEAD'`). If provided, its value is stored in the `~Request.method`{.interpreted-text role="attr"} attribute and is used by `get_method`{.interpreted-text role="meth"}. The default is `'GET'` if *data* is `None` or `'POST'` otherwise. Subclasses may indicate a different default method by setting the `~Request.method`{.interpreted-text role="attr"} attribute in the class itself.

:::: note
::: title
Note
:::

The request will not work as expected if the data object is unable to deliver its content more than once (e.g. a file or an iterable that can produce the content only once) and the request is retried for HTTP redirects or authentication. The *data* is sent to the HTTP server right away after the headers. There is no support for a 100-continue expectation in the library.
::::

::: versionchanged
3.3 `Request.method`{.interpreted-text role="attr"} argument is added to the Request class.
:::

::: versionchanged
3.4 Default `Request.method`{.interpreted-text role="attr"} may be indicated at the class level.
:::

::: versionchanged
3.6 Do not raise an error if the `Content-Length` has not been provided and *data* is neither `None` nor a bytes object. Fall back to use chunked transfer encoding instead.
:::
::::::::

::: OpenerDirector()
The `OpenerDirector`{.interpreted-text role="class"} class opens URLs via `BaseHandler`{.interpreted-text role="class"}s chained together. It manages the chaining of handlers, and recovery from errors.
:::

::: BaseHandler()
This is the base class for all registered handlers \-\-- and handles only the simple mechanics of registration.
:::

::: HTTPDefaultErrorHandler()
A class which defines a default handler for HTTP error responses; all responses are turned into `~urllib.error.HTTPError`{.interpreted-text role="exc"} exceptions.
:::

::: HTTPRedirectHandler()
A class to handle redirections.
:::

::: HTTPCookieProcessor(cookiejar=None)
A class to handle HTTP Cookies.
:::

::::: ProxyHandler(proxies=None)
Cause requests to go through a proxy. If *proxies* is given, it must be a dictionary mapping protocol names to URLs of proxies. The default is to read the list of proxies from the environment variables `<protocol>_proxy`. If no proxy environment variables are set, then in a Windows environment proxy settings are obtained from the registry\'s Internet Settings section, and in a macOS environment proxy information is retrieved from the System Configuration Framework.

To disable autodetected proxy pass an empty dictionary.

The `no_proxy`{.interpreted-text role="envvar"} environment variable can be used to specify hosts which shouldn\'t be reached via proxy; if set, it should be a comma-separated list of hostname suffixes, optionally with `:port` appended, for example `cern.ch,ncsa.uiuc.edu,some.host:8080`.

:::: note
::: title
Note
:::

`HTTP_PROXY` will be ignored if a variable `REQUEST_METHOD` is set; see the documentation on `~urllib.request.getproxies`{.interpreted-text role="func"}.
::::
:::::

::: HTTPPasswordMgr()
Keep a database of `(realm, uri) -> (user, password)` mappings.
:::

::: HTTPPasswordMgrWithDefaultRealm()
Keep a database of `(realm, uri) -> (user, password)` mappings. A realm of `None` is considered a catch-all realm, which is searched if no other realm fits.
:::

:::: HTTPPasswordMgrWithPriorAuth()
A variant of `HTTPPasswordMgrWithDefaultRealm`{.interpreted-text role="class"} that also has a database of `uri -> is_authenticated` mappings. Can be used by a BasicAuth handler to determine when to send authentication credentials immediately instead of waiting for a `401` response first.

::: versionadded
3.5
:::
::::

:::: AbstractBasicAuthHandler(password_mgr=None)
This is a mixin class that helps with HTTP authentication, both to the remote host and to a proxy. *password_mgr*, if given, should be something that is compatible with `HTTPPasswordMgr`{.interpreted-text role="class"}; refer to section `http-password-mgr`{.interpreted-text role="ref"} for information on the interface that must be supported. If *passwd_mgr* also provides `is_authenticated` and `update_authenticated` methods (see `http-password-mgr-with-prior-auth`{.interpreted-text role="ref"}), then the handler will use the `is_authenticated` result for a given URI to determine whether or not to send authentication credentials with the request. If `is_authenticated` returns `True` for the URI, credentials are sent. If `is_authenticated` is `False`, credentials are not sent, and then if a `401` response is received the request is re-sent with the authentication credentials. If authentication succeeds, `update_authenticated` is called to set `is_authenticated` `True` for the URI, so that subsequent requests to the URI or any of its super-URIs will automatically include the authentication credentials.

::: versionadded
3.5 Added `is_authenticated` support.
:::
::::

::: HTTPBasicAuthHandler(password_mgr=None)
Handle authentication with the remote host. *password_mgr*, if given, should be something that is compatible with `HTTPPasswordMgr`{.interpreted-text role="class"}; refer to section `http-password-mgr`{.interpreted-text role="ref"} for information on the interface that must be supported. HTTPBasicAuthHandler will raise a `ValueError`{.interpreted-text role="exc"} when presented with a wrong Authentication scheme.
:::

::: ProxyBasicAuthHandler(password_mgr=None)
Handle authentication with the proxy. *password_mgr*, if given, should be something that is compatible with `HTTPPasswordMgr`{.interpreted-text role="class"}; refer to section `http-password-mgr`{.interpreted-text role="ref"} for information on the interface that must be supported.
:::

:::: AbstractDigestAuthHandler(password_mgr=None)
This is a mixin class that helps with HTTP authentication, both to the remote host and to a proxy. *password_mgr*, if given, should be something that is compatible with `HTTPPasswordMgr`{.interpreted-text role="class"}; refer to section `http-password-mgr`{.interpreted-text role="ref"} for information on the interface that must be supported.

::: versionchanged
3.14 Added support for HTTP digest authentication algorithm `SHA-256`.
:::
::::

:::: HTTPDigestAuthHandler(password_mgr=None)
Handle authentication with the remote host. *password_mgr*, if given, should be something that is compatible with `HTTPPasswordMgr`{.interpreted-text role="class"}; refer to section `http-password-mgr`{.interpreted-text role="ref"} for information on the interface that must be supported. When both Digest Authentication Handler and Basic Authentication Handler are both added, Digest Authentication is always tried first. If the Digest Authentication returns a 40x response again, it is sent to Basic Authentication handler to Handle. This Handler method will raise a `ValueError`{.interpreted-text role="exc"} when presented with an authentication scheme other than Digest or Basic.

::: versionchanged
3.3 Raise `ValueError`{.interpreted-text role="exc"} on unsupported Authentication Scheme.
:::
::::

::: ProxyDigestAuthHandler(password_mgr=None)
Handle authentication with the proxy. *password_mgr*, if given, should be something that is compatible with `HTTPPasswordMgr`{.interpreted-text role="class"}; refer to section `http-password-mgr`{.interpreted-text role="ref"} for information on the interface that must be supported.
:::

::: HTTPHandler()
A class to handle opening of HTTP URLs.
:::

:::: {.HTTPSHandler(debuglevel=0, .context=None, .check_hostname=None)}
A class to handle opening of HTTPS URLs. *context* and *check_hostname* have the same meaning as in `http.client.HTTPSConnection`{.interpreted-text role="class"}.

::: versionchanged
3.2 *context* and *check_hostname* were added.
:::
::::

::: FileHandler()
Open local files.
:::

:::: DataHandler()
Open data URLs.

::: versionadded
3.4
:::
::::

::: FTPHandler()
Open FTP URLs.
:::

::: CacheFTPHandler()
Open FTP URLs, keeping a cache of open FTP connections to minimize delays.
:::

::: UnknownHandler()
A catch-all class to handle unknown URLs.
:::

::: HTTPErrorProcessor()
Process HTTP error responses.
:::

## Request Objects

The following methods describe `Request`{.interpreted-text role="class"}\'s public interface, and so all may be overridden in subclasses. It also defines several public attributes that can be used by clients to inspect the parsed request.

:::: attribute
Request.full_url

The original URL passed to the constructor.

::: versionchanged
3.4
:::

Request.full_url is a property with setter, getter and a deleter. Getting `~Request.full_url`{.interpreted-text role="attr"} returns the original request URL with the fragment, if it was present.
::::

::: attribute
Request.type

The URI scheme.
:::

::: attribute
Request.host

The URI authority, typically a host, but may also contain a port separated by a colon.
:::

::: attribute
Request.origin_req_host

The original host for the request, without port.
:::

::: attribute
Request.selector

The URI path. If the `Request`{.interpreted-text role="class"} uses a proxy, then selector will be the full URL that is passed to the proxy.
:::

:::: attribute
Request.data

The entity body for the request, or `None` if not specified.

::: versionchanged
3.4 Changing value of `Request.data`{.interpreted-text role="attr"} now deletes \"Content-Length\" header if it was previously set or calculated.
:::
::::

::: attribute
Request.unverifiable

boolean, indicates whether the request is unverifiable as defined by `2965`{.interpreted-text role="rfc"}.
:::

::::: attribute
Request.method

The HTTP request method to use. By default its value is `None`{.interpreted-text role="const"}, which means that `~Request.get_method`{.interpreted-text role="meth"} will do its normal computation of the method to be used. Its value can be set (thus overriding the default computation in `~Request.get_method`{.interpreted-text role="meth"}) either by providing a default value by setting it at the class level in a `Request`{.interpreted-text role="class"} subclass, or by passing a value in to the `Request`{.interpreted-text role="class"} constructor via the *method* argument.

::: versionadded
3.3
:::

::: versionchanged
3.4 A default value can now be set in subclasses; previously it could only be set via the constructor argument.
:::
:::::

:::: method
Request.get_method()

Return a string indicating the HTTP request method. If `Request.method`{.interpreted-text role="attr"} is not `None`, return its value, otherwise return `'GET'` if `Request.data`{.interpreted-text role="attr"} is `None`, or `'POST'` if it\'s not. This is only meaningful for HTTP requests.

::: versionchanged
3.3 get_method now looks at the value of `Request.method`{.interpreted-text role="attr"}.
:::
::::

::: method
Request.add_header(key, val)

Add another header to the request. Headers are currently ignored by all handlers except HTTP handlers, where they are added to the list of headers sent to the server. Note that there cannot be more than one header with the same name, and later calls will overwrite previous calls in case the *key* collides. Currently, this is no loss of HTTP functionality, since all headers which have meaning when used more than once have a (header-specific) way of gaining the same functionality using only one header. Note that headers added using this method are also added to redirected requests.
:::

::: method
Request.add_unredirected_header(key, header)

Add a header that will not be added to a redirected request.
:::

::: method
Request.has_header(header)

Return whether the instance has the named header (checks both regular and unredirected).
:::

:::: method
Request.remove_header(header)

Remove named header from the request instance (both from regular and unredirected headers).

::: versionadded
3.4
:::
::::

:::: method
Request.get_full_url()

Return the URL given in the constructor.

::: versionchanged
3.4
:::

Returns `Request.full_url`{.interpreted-text role="attr"}
::::

::: method
Request.set_proxy(host, type)

Prepare the request by connecting to a proxy server. The *host* and *type* will replace those of the instance, and the instance\'s selector will be the original URL given in the constructor.
:::

::: method
Request.get_header(header_name, default=None)

Return the value of the given header. If the header is not present, return the default value.
:::

::: method
Request.header_items()

Return a list of tuples (header_name, header_value) of the Request headers.
:::

::: versionchanged
3.4 The request methods add_data, has_data, get_data, get_type, get_host, get_selector, get_origin_req_host and is_unverifiable that were deprecated since 3.3 have been removed.
:::

## OpenerDirector Objects {#opener-director-objects}

`OpenerDirector`{.interpreted-text role="class"} instances have the following methods:

::: method
OpenerDirector.add_handler(handler)

*handler* should be an instance of `BaseHandler`{.interpreted-text role="class"}. The following methods are searched, and added to the possible chains (note that HTTP errors are a special case). Note that, in the following, *protocol* should be replaced with the actual protocol to handle, for example `http_response`{.interpreted-text role="meth"} would be the HTTP protocol response handler. Also *type* should be replaced with the actual HTTP code, for example `http_error_404`{.interpreted-text role="meth"} would handle HTTP 404 errors.

- `!<protocol>_open`{.interpreted-text role="meth"} \-\-- signal that the handler knows how to open *protocol* URLs.

  See [`BaseHandler.<protocol>_open`{.interpreted-text role="meth"}](..%20method::%20BaseHandler.%3Cprotocol%3E_open(req):noindex:) for more information.

- `!http_error_\<type\>`{.interpreted-text role="meth"} \-\-- signal that the handler knows how to handle HTTP errors with HTTP error code *type*.

  See [`BaseHandler.http_error_\<nnn\>`{.interpreted-text role="meth"}](..%20method::%20BaseHandler.http_error_%3Cnnn%3E(req,%20fp,%20code,%20msg,%20hdrs)) for more information.

- `!<protocol>_error`{.interpreted-text role="meth"} \-\-- signal that the handler knows how to handle errors from (non-`http`) *protocol*.

- `!<protocol>_request`{.interpreted-text role="meth"} \-\-- signal that the handler knows how to pre-process *protocol* requests.

  See [`BaseHandler.<protocol>_request`{.interpreted-text role="meth"}](..%20method::%20BaseHandler.%3Cprotocol%3E_request(req):noindex:) for more information.

- `!<protocol>_response`{.interpreted-text role="meth"} \-\-- signal that the handler knows how to post-process *protocol* responses.

  See [`BaseHandler.<protocol>_response`{.interpreted-text role="meth"}](..%20method::%20BaseHandler.%3Cprotocol%3E_response(req,%20response):noindex:) for more information.
:::

::: method
OpenerDirector.open(url, data=None\[, timeout\])

Open the given *url* (which can be a request object or a string), optionally passing the given *data*. Arguments, return values and exceptions raised are the same as those of `urlopen`{.interpreted-text role="func"} (which simply calls the `open`{.interpreted-text role="meth"} method on the currently installed global `OpenerDirector`{.interpreted-text role="class"}). The optional *timeout* parameter specifies a timeout in seconds for blocking operations like the connection attempt (if not specified, the global default timeout setting will be used). The timeout feature actually works only for HTTP, HTTPS and FTP connections.
:::

::: method
OpenerDirector.error(proto, \*args)

Handle an error of the given protocol. This will call the registered error handlers for the given protocol with the given arguments (which are protocol specific). The HTTP protocol is a special case which uses the HTTP response code to determine the specific error handler; refer to the `!http_error_\<type\>`{.interpreted-text role="meth"} methods of the handler classes.

Return values and exceptions raised are the same as those of `urlopen`{.interpreted-text role="func"}.
:::

OpenerDirector objects open URLs in three stages:

The order in which these methods are called within each stage is determined by sorting the handler instances.

1.  Every handler with a method named like `!<protocol>_request`{.interpreted-text role="meth"} has that method called to pre-process the request.

2.  Handlers with a method named like `!<protocol>_open`{.interpreted-text role="meth"} are called to handle the request. This stage ends when a handler either returns a non-`None`{.interpreted-text role="const"} value (ie. a response), or raises an exception (usually `~urllib.error.URLError`{.interpreted-text role="exc"}). Exceptions are allowed to propagate.

    In fact, the above algorithm is first tried for methods named `~BaseHandler.default_open`{.interpreted-text role="meth"}. If all such methods return `None`{.interpreted-text role="const"}, the algorithm is repeated for methods named like `!<protocol>_open`{.interpreted-text role="meth"}. If all such methods return `None`{.interpreted-text role="const"}, the algorithm is repeated for methods named `~BaseHandler.unknown_open`{.interpreted-text role="meth"}.

    Note that the implementation of these methods may involve calls of the parent `OpenerDirector`{.interpreted-text role="class"} instance\'s `~OpenerDirector.open`{.interpreted-text role="meth"} and `~OpenerDirector.error`{.interpreted-text role="meth"} methods.

3.  Every handler with a method named like `!<protocol>_response`{.interpreted-text role="meth"} has that method called to post-process the response.

## BaseHandler Objects {#base-handler-objects}

`BaseHandler`{.interpreted-text role="class"} objects provide a couple of methods that are directly useful, and others that are meant to be used by derived classes. These are intended for direct use:

::: method
BaseHandler.add_parent(director)

Add a director as parent.
:::

::: method
BaseHandler.close()

Remove any parents.
:::

The following attribute and methods should only be used by classes derived from `BaseHandler`{.interpreted-text role="class"}.

:::: note
::: title
Note
:::

The convention has been adopted that subclasses defining `!<protocol>_request`{.interpreted-text role="meth"} or `!<protocol>_response`{.interpreted-text role="meth"} methods are named `!\*Processor`{.interpreted-text role="class"}; all others are named `!\*Handler`{.interpreted-text role="class"}.
::::

::: attribute
BaseHandler.parent

A valid `OpenerDirector`{.interpreted-text role="class"}, which can be used to open using a different protocol, or handle errors.
:::

::: method
BaseHandler.default_open(req)

This method is *not* defined in `BaseHandler`{.interpreted-text role="class"}, but subclasses should define it if they want to catch all URLs.

This method, if implemented, will be called by the parent `OpenerDirector`{.interpreted-text role="class"}. It should return a file-like object as described in the return value of the `~OpenerDirector.open`{.interpreted-text role="meth"} method of `OpenerDirector`{.interpreted-text role="class"}, or `None`. It should raise `~urllib.error.URLError`{.interpreted-text role="exc"}, unless a truly exceptional thing happens (for example, `MemoryError`{.interpreted-text role="exc"} should not be mapped to `~urllib.error.URLError`{.interpreted-text role="exc"}).

This method will be called before any protocol-specific open method.
:::

> This method is *not* defined in `BaseHandler`{.interpreted-text role="class"}, but subclasses should define it if they want to handle URLs with the given protocol.
>
> This method, if defined, will be called by the parent `OpenerDirector`{.interpreted-text role="class"}. Return values should be the same as for `~BaseHandler.default_open`{.interpreted-text role="meth"}.

::: method
BaseHandler.unknown_open(req)

This method is *not* defined in `BaseHandler`{.interpreted-text role="class"}, but subclasses should define it if they want to catch all URLs with no specific registered handler to open it.

This method, if implemented, will be called by the `parent`{.interpreted-text role="attr"} `OpenerDirector`{.interpreted-text role="class"}. Return values should be the same as for `default_open`{.interpreted-text role="meth"}.
:::

::: method
BaseHandler.http_error_default(req, fp, code, msg, hdrs)

This method is *not* defined in `BaseHandler`{.interpreted-text role="class"}, but subclasses should override it if they intend to provide a catch-all for otherwise unhandled HTTP errors. It will be called automatically by the `OpenerDirector`{.interpreted-text role="class"} getting the error, and should not normally be called in other circumstances.

`OpenerDirector`{.interpreted-text role="class"} will call this method with five positional arguments:

1.  a `Request`{.interpreted-text role="class"} object,
2.  a file-like object with the HTTP error body,
3.  the three-digit code of the error, as a string,
4.  the user-visible explanation of the code, as a string, and
5.  the headers of the error, as a mapping object.

Return values and exceptions raised should be the same as those of `urlopen`{.interpreted-text role="func"}.
:::

> *nnn* should be a three-digit HTTP error code. This method is also not defined in `BaseHandler`{.interpreted-text role="class"}, but will be called, if it exists, on an instance of a subclass, when an HTTP error with code *nnn* occurs.
>
> Subclasses should override this method to handle specific HTTP errors.
>
> Arguments, return values and exceptions raised should be the same as for `~BaseHandler.http_error_default`{.interpreted-text role="meth"}.

> This method is *not* defined in `BaseHandler`{.interpreted-text role="class"}, but subclasses should define it if they want to pre-process requests of the given protocol.
>
> This method, if defined, will be called by the parent `OpenerDirector`{.interpreted-text role="class"}. *req* will be a `Request`{.interpreted-text role="class"} object. The return value should be a `Request`{.interpreted-text role="class"} object.

> This method is *not* defined in `BaseHandler`{.interpreted-text role="class"}, but subclasses should define it if they want to post-process responses of the given protocol.
>
> This method, if defined, will be called by the parent `OpenerDirector`{.interpreted-text role="class"}. *req* will be a `Request`{.interpreted-text role="class"} object. *response* will be an object implementing the same interface as the return value of `urlopen`{.interpreted-text role="func"}. The return value should implement the same interface as the return value of `urlopen`{.interpreted-text role="func"}.

## HTTPRedirectHandler Objects {#http-redirect-handler}

:::: note
::: title
Note
:::

Some HTTP redirections require action from this module\'s client code. If this is the case, `~urllib.error.HTTPError`{.interpreted-text role="exc"} is raised. See `2616`{.interpreted-text role="rfc"} for details of the precise meanings of the various redirection codes.

An `~urllib.error.HTTPError`{.interpreted-text role="exc"} exception raised as a security consideration if the HTTPRedirectHandler is presented with a redirected URL which is not an HTTP, HTTPS or FTP URL.
::::

::::: method
HTTPRedirectHandler.redirect_request(req, fp, code, msg, hdrs, newurl)

Return a `Request`{.interpreted-text role="class"} or `None` in response to a redirect. This is called by the default implementations of the `!http_error_30\*`{.interpreted-text role="meth"} methods when a redirection is received from the server. If a redirection should take place, return a new `Request`{.interpreted-text role="class"} to allow `!http_error_30\*`{.interpreted-text role="meth"} to perform the redirect to *newurl*. Otherwise, raise `~urllib.error.HTTPError`{.interpreted-text role="exc"} if no other handler should try to handle this URL, or return `None` if you can\'t but another handler might.

:::: note
::: title
Note
:::

The default implementation of this method does not strictly follow `2616`{.interpreted-text role="rfc"}, which says that 301 and 302 responses to `POST` requests must not be automatically redirected without confirmation by the user. In reality, browsers do allow automatic redirection of these responses, changing the POST to a `GET`, and the default implementation reproduces this behavior.
::::
:::::

::: method
HTTPRedirectHandler.http_error_301(req, fp, code, msg, hdrs)

Redirect to the `Location:` or `URI:` URL. This method is called by the parent `OpenerDirector`{.interpreted-text role="class"} when getting an HTTP \'moved permanently\' response.
:::

::: method
HTTPRedirectHandler.http_error_302(req, fp, code, msg, hdrs)

The same as `http_error_301`{.interpreted-text role="meth"}, but called for the \'found\' response.
:::

::: method
HTTPRedirectHandler.http_error_303(req, fp, code, msg, hdrs)

The same as `http_error_301`{.interpreted-text role="meth"}, but called for the \'see other\' response.
:::

::: method
HTTPRedirectHandler.http_error_307(req, fp, code, msg, hdrs)

The same as `http_error_301`{.interpreted-text role="meth"}, but called for the \'temporary redirect\' response. It does not allow changing the request method from `POST` to `GET`.
:::

:::: method
HTTPRedirectHandler.http_error_308(req, fp, code, msg, hdrs)

The same as `http_error_301`{.interpreted-text role="meth"}, but called for the \'permanent redirect\' response. It does not allow changing the request method from `POST` to `GET`.

::: versionadded
3.11
:::
::::

## HTTPCookieProcessor Objects {#http-cookie-processor}

`HTTPCookieProcessor`{.interpreted-text role="class"} instances have one attribute:

::: attribute
HTTPCookieProcessor.cookiejar

The `http.cookiejar.CookieJar`{.interpreted-text role="class"} in which cookies are stored.
:::

## ProxyHandler Objects {#proxy-handler}

::: {.method noindex=""}
ProxyHandler.\<protocol\>\_open(request)

The `ProxyHandler`{.interpreted-text role="class"} will have a method `!<protocol>_open`{.interpreted-text role="meth"} for every *protocol* which has a proxy in the *proxies* dictionary given in the constructor. The method will modify requests to go through the proxy, by calling `request.set_proxy()`, and call the next handler in the chain to actually execute the protocol.
:::

## HTTPPasswordMgr Objects {#http-password-mgr}

These methods are available on `HTTPPasswordMgr`{.interpreted-text role="class"} and `HTTPPasswordMgrWithDefaultRealm`{.interpreted-text role="class"} objects.

::: method
HTTPPasswordMgr.add_password(realm, uri, user, passwd)

*uri* can be either a single URI, or a sequence of URIs. *realm*, *user* and *passwd* must be strings. This causes `(user, passwd)` to be used as authentication tokens when authentication for *realm* and a super-URI of any of the given URIs is given.
:::

::: method
HTTPPasswordMgr.find_user_password(realm, authuri)

Get user/password for given realm and URI, if any. This method will return `(None, None)` if there is no matching user/password.

For `HTTPPasswordMgrWithDefaultRealm`{.interpreted-text role="class"} objects, the realm `None` will be searched if the given *realm* has no matching user/password.
:::

## HTTPPasswordMgrWithPriorAuth Objects {#http-password-mgr-with-prior-auth}

This password manager extends `HTTPPasswordMgrWithDefaultRealm`{.interpreted-text role="class"} to support tracking URIs for which authentication credentials should always be sent.

::: method
HTTPPasswordMgrWithPriorAuth.add_password(realm, uri, user, passwd, is_authenticated=False)

*realm*, *uri*, *user*, *passwd* are as for `HTTPPasswordMgr.add_password`{.interpreted-text role="meth"}. *is_authenticated* sets the initial value of the `is_authenticated` flag for the given URI or list of URIs. If *is_authenticated* is specified as `True`, *realm* is ignored.
:::

::: method
HTTPPasswordMgrWithPriorAuth.find_user_password(realm, authuri)

Same as for `HTTPPasswordMgrWithDefaultRealm`{.interpreted-text role="class"} objects
:::

::: method
HTTPPasswordMgrWithPriorAuth.update_authenticated(self, uri, is_authenticated=False)

Update the `is_authenticated` flag for the given *uri* or list of URIs.
:::

::: method
HTTPPasswordMgrWithPriorAuth.is_authenticated(self, authuri)

Returns the current state of the `is_authenticated` flag for the given URI.
:::

## AbstractBasicAuthHandler Objects {#abstract-basic-auth-handler}

::: method
AbstractBasicAuthHandler.http_error_auth_reqed(authreq, host, req, headers)

Handle an authentication request by getting a user/password pair, and re-trying the request. *authreq* should be the name of the header where the information about the realm is included in the request, *host* specifies the URL and path to authenticate for, *req* should be the (failed) `Request`{.interpreted-text role="class"} object, and *headers* should be the error headers.

*host* is either an authority (e.g. `"python.org"`) or a URL containing an authority component (e.g. `"http://python.org/"`). In either case, the authority must not contain a userinfo component (so, `"python.org"` and `"python.org:80"` are fine, `"joe:password@python.org"` is not).
:::

## HTTPBasicAuthHandler Objects {#http-basic-auth-handler}

::: method
HTTPBasicAuthHandler.http_error_401(req, fp, code, msg, hdrs)

Retry the request with authentication information, if available.
:::

## ProxyBasicAuthHandler Objects {#proxy-basic-auth-handler}

::: method
ProxyBasicAuthHandler.http_error_407(req, fp, code, msg, hdrs)

Retry the request with authentication information, if available.
:::

## AbstractDigestAuthHandler Objects {#abstract-digest-auth-handler}

::: method
AbstractDigestAuthHandler.http_error_auth_reqed(authreq, host, req, headers)

*authreq* should be the name of the header where the information about the realm is included in the request, *host* should be the host to authenticate to, *req* should be the (failed) `Request`{.interpreted-text role="class"} object, and *headers* should be the error headers.
:::

## HTTPDigestAuthHandler Objects {#http-digest-auth-handler}

::: method
HTTPDigestAuthHandler.http_error_401(req, fp, code, msg, hdrs)

Retry the request with authentication information, if available.
:::

## ProxyDigestAuthHandler Objects {#proxy-digest-auth-handler}

::: method
ProxyDigestAuthHandler.http_error_407(req, fp, code, msg, hdrs)

Retry the request with authentication information, if available.
:::

## HTTPHandler Objects {#http-handler-objects}

::: method
HTTPHandler.http_open(req)

Send an HTTP request, which can be either GET or POST, depending on `req.data`.
:::

## HTTPSHandler Objects {#https-handler-objects}

::: method
HTTPSHandler.https_open(req)

Send an HTTPS request, which can be either GET or POST, depending on `req.data`.
:::

## FileHandler Objects {#file-handler-objects}

:::: method
FileHandler.file_open(req)

Open the file locally, if there is no host name, or the host name is `'localhost'`.

::: versionchanged
3.2 This method is applicable only for local hostnames. When a remote hostname is given, a `~urllib.error.URLError`{.interpreted-text role="exc"} is raised.
:::
::::

## DataHandler Objects {#data-handler-objects}

::: method
DataHandler.data_open(req)

Read a data URL. This kind of URL contains the content encoded in the URL itself. The data URL syntax is specified in `2397`{.interpreted-text role="rfc"}. This implementation ignores white spaces in base64 encoded data URLs so the URL may be wrapped in whatever source file it comes from. But even though some browsers don\'t mind about a missing padding at the end of a base64 encoded data URL, this implementation will raise a `ValueError`{.interpreted-text role="exc"} in that case.
:::

## FTPHandler Objects {#ftp-handler-objects}

::: method
FTPHandler.ftp_open(req)

Open the FTP file indicated by *req*. The login is always done with empty username and password.
:::

## CacheFTPHandler Objects {#cacheftp-handler-objects}

`CacheFTPHandler`{.interpreted-text role="class"} objects are `FTPHandler`{.interpreted-text role="class"} objects with the following additional methods:

::: method
CacheFTPHandler.setTimeout(t)

Set timeout of connections to *t* seconds.
:::

::: method
CacheFTPHandler.setMaxConns(m)

Set maximum number of cached connections to *m*.
:::

## UnknownHandler Objects {#unknown-handler-objects}

::: method
UnknownHandler.unknown_open()

Raise a `~urllib.error.URLError`{.interpreted-text role="exc"} exception.
:::

## HTTPErrorProcessor Objects {#http-error-processor-objects}

::: method
HTTPErrorProcessor.http_response(request, response)

Process HTTP error responses.

For 200 error codes, the response object is returned immediately.

For non-200 error codes, this simply passes the job on to the `!http_error_\<type\>`{.interpreted-text role="meth"} handler methods, via `OpenerDirector.error`{.interpreted-text role="meth"}. Eventually, `HTTPDefaultErrorHandler`{.interpreted-text role="class"} will raise an `~urllib.error.HTTPError`{.interpreted-text role="exc"} if no other handler handles the error.
:::

::: method
HTTPErrorProcessor.https_response(request, response)

Process HTTPS error responses.

The behavior is same as `http_response`{.interpreted-text role="meth"}.
:::

## Examples {#urllib-request-examples}

In addition to the examples below, more examples are given in `urllib-howto`{.interpreted-text role="ref"}.

This example gets the python.org main page and displays the first 300 bytes of it:

    >>> import urllib.request
    >>> with urllib.request.urlopen('http://www.python.org/') as f:
    ...     print(f.read(300))
    ...
    b'<!doctype html>\n<!--[if lt IE 7]>   <html class="no-js ie6 lt-ie7 lt-ie8 lt-ie9">   <![endif]-->\n<!--[if IE 7]>      <html class="no-js ie7 lt-ie8 lt-ie9">          <![endif]-->\n<!--[if IE 8]>      <html class="no-js ie8 lt-ie9">

Note that urlopen returns a bytes object. This is because there is no way for urlopen to automatically determine the encoding of the byte stream it receives from the HTTP server. In general, a program will decode the returned bytes object to string once it determines or guesses the appropriate encoding.

The following HTML spec document, <https://html.spec.whatwg.org/#charset>, lists the various ways in which an HTML or an XML document could have specified its encoding information.

For additional information, see the W3C document: <https://www.w3.org/International/questions/qa-html-encoding-declarations>.

As the python.org website uses *utf-8* encoding as specified in its meta tag, we will use the same for decoding the bytes object:

    >>> with urllib.request.urlopen('http://www.python.org/') as f:
    ...     print(f.read(100).decode('utf-8'))
    ...
    <!doctype html>
    <!--[if lt IE 7]>   <html class="no-js ie6 lt-ie7 lt-ie8 lt-ie9">   <![endif]-->
    <!-

It is also possible to achieve the same result without using the `context manager`{.interpreted-text role="term"} approach:

    >>> import urllib.request
    >>> f = urllib.request.urlopen('http://www.python.org/')
    >>> try:
    ...     print(f.read(100).decode('utf-8'))
    ... finally:
    ...     f.close()
    ...
    <!doctype html>
    <!--[if lt IE 7]>   <html class="no-js ie6 lt-ie7 lt-ie8 lt-ie9">   <![endif]-->
    <!--

In the following example, we are sending a data-stream to the stdin of a CGI and reading the data it returns to us. Note that this example will only work when the Python installation supports SSL. :

    >>> import urllib.request
    >>> req = urllib.request.Request(url='https://localhost/cgi-bin/test.cgi',
    ...                       data=b'This data is passed to stdin of the CGI')
    >>> with urllib.request.urlopen(req) as f:
    ...     print(f.read().decode('utf-8'))
    ...
    Got Data: "This data is passed to stdin of the CGI"

The code for the sample CGI used in the above example is:

    #!/usr/bin/env python
    import sys
    data = sys.stdin.read()
    print('Content-type: text/plain\n\nGot Data: "%s"' % data)

Here is an example of doing a `PUT` request using `Request`{.interpreted-text role="class"}:

    import urllib.request
    DATA = b'some data'
    req = urllib.request.Request(url='http://localhost:8080', data=DATA, method='PUT')
    with urllib.request.urlopen(req) as f:
        pass
    print(f.status)
    print(f.reason)

Use of Basic HTTP Authentication:

    import urllib.request
    # Create an OpenerDirector with support for Basic HTTP Authentication...
    auth_handler = urllib.request.HTTPBasicAuthHandler()
    auth_handler.add_password(realm='PDQ Application',
                              uri='https://mahler:8092/site-updates.py',
                              user='klem',
                              passwd='kadidd!ehopper')
    opener = urllib.request.build_opener(auth_handler)
    # ...and install it globally so it can be used with urlopen.
    urllib.request.install_opener(opener)
    with urllib.request.urlopen('http://www.example.com/login.html') as f:
        print(f.read().decode('utf-8'))

`build_opener`{.interpreted-text role="func"} provides many handlers by default, including a `ProxyHandler`{.interpreted-text role="class"}. By default, `ProxyHandler`{.interpreted-text role="class"} uses the environment variables named `<scheme>_proxy`, where `<scheme>` is the URL scheme involved. For example, the `!http_proxy`{.interpreted-text role="envvar"} environment variable is read to obtain the HTTP proxy\'s URL.

This example replaces the default `ProxyHandler`{.interpreted-text role="class"} with one that uses programmatically supplied proxy URLs, and adds proxy authorization support with `ProxyBasicAuthHandler`{.interpreted-text role="class"}. :

    proxy_handler = urllib.request.ProxyHandler({'http': 'http://www.example.com:3128/'})
    proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
    proxy_auth_handler.add_password('realm', 'host', 'username', 'password')

    opener = urllib.request.build_opener(proxy_handler, proxy_auth_handler)
    # This time, rather than install the OpenerDirector, we use it directly:
    with opener.open('http://www.example.com/login.html') as f:
       print(f.read().decode('utf-8'))

Adding HTTP headers:

Use the *headers* argument to the `Request`{.interpreted-text role="class"} constructor, or:

    import urllib.request
    req = urllib.request.Request('http://www.example.com/')
    req.add_header('Referer', 'http://www.python.org/')
    # Customize the default User-Agent header value:
    req.add_header('User-Agent', 'urllib-example/0.1 (Contact: . . .)')
    with urllib.request.urlopen(req) as f:
        print(f.read().decode('utf-8'))

`OpenerDirector`{.interpreted-text role="class"} automatically adds a `User-Agent`{.interpreted-text role="mailheader"} header to every `Request`{.interpreted-text role="class"}. To change this:

    import urllib.request
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    with opener.open('http://www.example.com/') as f:
       print(f.read().decode('utf-8'))

Also, remember that a few standard headers (`Content-Length`{.interpreted-text role="mailheader"}, `Content-Type`{.interpreted-text role="mailheader"} and `Host`{.interpreted-text role="mailheader"}) are added when the `Request`{.interpreted-text role="class"} is passed to `urlopen`{.interpreted-text role="func"} (or `OpenerDirector.open`{.interpreted-text role="meth"}).

::: {#urllib-examples}
Here is an example session that uses the `GET` method to retrieve a URL containing parameters:

    >>> import urllib.request
    >>> import urllib.parse
    >>> params = urllib.parse.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
    >>> url = "http://www.musi-cal.com/cgi-bin/query?%s" % params
    >>> with urllib.request.urlopen(url) as f:
    ...     print(f.read().decode('utf-8'))
    ...
:::

The following example uses the `POST` method instead. Note that params output from urlencode is encoded to bytes before it is sent to urlopen as data:

    >>> import urllib.request
    >>> import urllib.parse
    >>> data = urllib.parse.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
    >>> data = data.encode('ascii')
    >>> with urllib.request.urlopen("http://requestb.in/xrbl82xr", data) as f:
    ...     print(f.read().decode('utf-8'))
    ...

The following example uses an explicitly specified HTTP proxy, overriding environment settings:

    >>> import urllib.request
    >>> proxies = {'http': 'http://proxy.example.com:8080/'}
    >>> opener = urllib.request.build_opener(urllib.request.ProxyHandler(proxies))
    >>> with opener.open("http://www.python.org") as f:
    ...     f.read().decode('utf-8')
    ...

The following example uses no proxies at all, overriding environment settings:

    >>> import urllib.request
    >>> opener = urllib.request.build_opener(urllib.request.ProxyHandler({}}))
    >>> with opener.open("http://www.python.org/") as f:
    ...     f.read().decode('utf-8')
    ...

## Legacy interface

The following functions and classes are ported from the Python 2 module `urllib` (as opposed to `urllib2`). They might become deprecated at some point in the future.

::: function
urlretrieve(url, filename=None, reporthook=None, data=None)

Copy a network object denoted by a URL to a local file. If the URL points to a local file, the object will not be copied unless filename is supplied. Return a tuple `(filename, headers)` where *filename* is the local file name under which the object can be found, and *headers* is whatever the `!info`{.interpreted-text role="meth"} method of the object returned by `urlopen`{.interpreted-text role="func"} returned (for a remote object). Exceptions are the same as for `urlopen`{.interpreted-text role="func"}.

The second argument, if present, specifies the file location to copy to (if absent, the location will be a tempfile with a generated name). The third argument, if present, is a callable that will be called once on establishment of the network connection and once after each block read thereafter. The callable will be passed three arguments; a count of blocks transferred so far, a block size in bytes, and the total size of the file. The third argument may be `-1` on older FTP servers which do not return a file size in response to a retrieval request.

The following example illustrates the most common usage scenario:

    >>> import urllib.request
    >>> local_filename, headers = urllib.request.urlretrieve('http://python.org/')
    >>> html = open(local_filename)
    >>> html.close()

If the *url* uses the `http:`{.interpreted-text role="file"} scheme identifier, the optional *data* argument may be given to specify a `POST` request (normally the request type is `GET`). The *data* argument must be a bytes object in standard `application/x-www-form-urlencoded`{.interpreted-text role="mimetype"} format; see the `urllib.parse.urlencode`{.interpreted-text role="func"} function.

`urlretrieve`{.interpreted-text role="func"} will raise `~urllib.error.ContentTooShortError`{.interpreted-text role="exc"} when it detects that the amount of data available was less than the expected amount (which is the size reported by a *Content-Length* header). This can occur, for example, when the download is interrupted.

The *Content-Length* is treated as a lower bound: if there\'s more data to read, urlretrieve reads more data, but if less data is available, it raises the exception.

You can still retrieve the downloaded data in this case, it is stored in the `!content`{.interpreted-text role="attr"} attribute of the exception instance.

If no *Content-Length* header was supplied, urlretrieve can not check the size of the data it has downloaded, and just returns it. In this case you just have to assume that the download was successful.
:::

::: function
urlcleanup()

Cleans up temporary files that may have been left behind by previous calls to `urlretrieve`{.interpreted-text role="func"}.
:::

## `!urllib.request`{.interpreted-text role="mod"} Restrictions

::: index
pair: HTTP; protocol pair: FTP; protocol
:::

- Currently, only the following protocols are supported: HTTP (versions 0.9 and 1.0), FTP, local files, and data URLs.

  ::: versionchanged
  3.4 Added support for data URLs.
  :::

- The caching feature of `urlretrieve`{.interpreted-text role="func"} has been disabled until someone finds the time to hack proper processing of Expiration time headers.

- There should be a function to query whether a particular URL is in the cache.

- For backward compatibility, if a URL appears to point to a local file but the file can\'t be opened, the URL is re-interpreted using the FTP protocol. This can sometimes cause confusing error messages.

- The `urlopen`{.interpreted-text role="func"} and `urlretrieve`{.interpreted-text role="func"} functions can cause arbitrarily long delays while waiting for a network connection to be set up. This means that it is difficult to build an interactive web client using these functions without using threads.

  ::: index
  single: HTML pair: HTTP; protocol
  :::

- The data returned by `urlopen`{.interpreted-text role="func"} or `urlretrieve`{.interpreted-text role="func"} is the raw data returned by the server. This may be binary data (such as an image), plain text or (for example) HTML. The HTTP protocol provides type information in the reply header, which can be inspected by looking at the `Content-Type`{.interpreted-text role="mailheader"} header. If the returned data is HTML, you can use the module `html.parser`{.interpreted-text role="mod"} to parse it.

  ::: index
  single: FTP
  :::

- The code handling the FTP protocol cannot differentiate between a file and a directory. This can lead to unexpected behavior when attempting to read a URL that points to a file that is not accessible. If the URL ends in a `/`, it is assumed to refer to a directory and will be handled accordingly. But if an attempt to read a file leads to a 550 error (meaning the URL cannot be found or is not accessible, often for permission reasons), then the path is treated as a directory in order to handle the case when a directory is specified by a URL but the trailing `/` has been left off. This can cause misleading results when you try to fetch a file whose read permissions make it inaccessible; the FTP code will try to read it, fail with a 550 error, and then perform a directory listing for the unreadable file. If fine-grained control is needed, consider using the `ftplib`{.interpreted-text role="mod"} module.

# `!urllib.response`{.interpreted-text role="mod"} \-\-- Response classes used by urllib

::: {.module synopsis="Response classes used by urllib."}
urllib.response
:::

The `!urllib.response`{.interpreted-text role="mod"} module defines functions and classes which define a minimal file-like interface, including `read()` and `readline()`. Functions defined by this module are used internally by the `!urllib.request`{.interpreted-text role="mod"} module. The typical response object is a `urllib.response.addinfourl`{.interpreted-text role="class"} instance:

::::::::::::::: addinfourl
::: attribute
url

URL of the resource retrieved, commonly used to determine if a redirect was followed.
:::

::: attribute
headers

Returns the headers of the response in the form of an `~email.message.EmailMessage`{.interpreted-text role="class"} instance.
:::

:::: attribute
status

::: versionadded
3.9
:::

Status code returned by server.
::::

:::: method
geturl()

::: deprecated
3.9 Deprecated in favor of `~addinfourl.url`{.interpreted-text role="attr"}.
:::
::::

:::: method
info()

::: deprecated
3.9 Deprecated in favor of `~addinfourl.headers`{.interpreted-text role="attr"}.
:::
::::

:::: attribute
code

::: deprecated
3.9 Deprecated in favor of `~addinfourl.status`{.interpreted-text role="attr"}.
:::
::::

:::: method
getcode()

::: deprecated
3.9 Deprecated in favor of `~addinfourl.status`{.interpreted-text role="attr"}.
:::
::::
:::::::::::::::
