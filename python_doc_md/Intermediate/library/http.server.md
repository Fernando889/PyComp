# `!http.server`{.interpreted-text role="mod"} \-\-- HTTP servers

::: {.module synopsis="HTTP server and request handlers."}
http.server
:::

**Source code:** `Lib/http/server.py`{.interpreted-text role="source"}

::: index
pair: WWW; server pair: HTTP; protocol single: URL single: httpd
:::

------------------------------------------------------------------------

This module defines classes for implementing HTTP servers.

:::: warning
::: title
Warning
:::

`!http.server`{.interpreted-text role="mod"} is not recommended for production. It only implements `basic security checks <http.server-security>`{.interpreted-text role="ref"}.
::::

::: availability
not WASI.

This module does not work or is not available on WebAssembly. See `wasm-availability`{.interpreted-text role="ref"} for more information.
:::

One class, `HTTPServer`{.interpreted-text role="class"}, is a `socketserver.TCPServer`{.interpreted-text role="class"} subclass. It creates and listens at the HTTP socket, dispatching the requests to a handler. Code to create and run the server looks like this:

    def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
        server_address = ('', 8000)
        httpd = server_class(server_address, handler_class)
        httpd.serve_forever()

::: {.HTTPServer(server_address, .RequestHandlerClass)}
This class builds on the `~socketserver.TCPServer`{.interpreted-text role="class"} class by storing the server address as instance variables named `server_name`{.interpreted-text role="attr"} and `server_port`{.interpreted-text role="attr"}. The server is accessible by the handler, typically through the handler\'s `server`{.interpreted-text role="attr"} instance variable.
:::

:::: {.ThreadingHTTPServer(server_address, .RequestHandlerClass)}
This class is identical to HTTPServer but uses threads to handle requests by using the `~socketserver.ThreadingMixIn`{.interpreted-text role="class"}. This is useful to handle web browsers pre-opening sockets, on which `HTTPServer`{.interpreted-text role="class"} would wait indefinitely.

::: versionadded
3.7
:::
::::

::::: {.HTTPSServer(server_address, .RequestHandlerClass,\\ .bind_and_activate=True, .*, .certfile, .keyfile=None,\\ .password=None, .alpn_protocols=None)}
Subclass of `HTTPServer`{.interpreted-text role="class"} with a wrapped socket using the `ssl`{.interpreted-text role="mod"} module. If the `ssl`{.interpreted-text role="mod"} module is not available, instantiating a `!HTTPSServer`{.interpreted-text role="class"} object fails with a `RuntimeError`{.interpreted-text role="exc"}.

The *certfile* argument is the path to the SSL certificate chain file, and the *keyfile* is the path to file containing the private key.

A *password* can be specified for files protected and wrapped with PKCS#8, but beware that this could possibly expose hardcoded passwords in clear.

::: seealso
See `ssl.SSLContext.load_cert_chain`{.interpreted-text role="meth"} for additional information on the accepted values for *certfile*, *keyfile* and *password*.
:::

When specified, the *alpn_protocols* argument must be a sequence of strings specifying the \"Application-Layer Protocol Negotiation\" (ALPN) protocols supported by the server. ALPN allows the server and the client to negotiate the application protocol during the TLS handshake.

By default, it is set to `["http/1.1"]`, meaning the server supports HTTP/1.1.

::: versionadded
3.14
:::
:::::

:::: {.ThreadingHTTPSServer(server_address, .RequestHandlerClass,\\ .bind_and_activate=True, .*, .certfile, .keyfile=None,\\ .password=None, .alpn_protocols=None)}
This class is identical to `HTTPSServer`{.interpreted-text role="class"} but uses threads to handle requests by inheriting from `~socketserver.ThreadingMixIn`{.interpreted-text role="class"}. This is analogous to `ThreadingHTTPServer`{.interpreted-text role="class"} only using `HTTPSServer`{.interpreted-text role="class"}.

::: versionadded
3.14
:::
::::

The `HTTPServer`{.interpreted-text role="class"}, `ThreadingHTTPServer`{.interpreted-text role="class"}, `HTTPSServer`{.interpreted-text role="class"} and `ThreadingHTTPSServer`{.interpreted-text role="class"} must be given a *RequestHandlerClass* on instantiation, of which this module provides three different variants:

::::::::::::::::::::::::::::::::::::::::::::: {.BaseHTTPRequestHandler(request, .client_address, .server)}
This class is used to handle the HTTP requests that arrive at the server. By itself, it cannot respond to any actual HTTP requests; it must be subclassed to handle each request method (e.g. GET or POST). `BaseHTTPRequestHandler`{.interpreted-text role="class"} provides a number of class and instance variables, and methods for use by subclasses.

The handler will parse the request and the headers, then call a method specific to the request type. The method name is constructed from the request. For example, for the request method `SPAM`, the `!do_SPAM`{.interpreted-text role="meth"} method will be called with no arguments. All of the relevant information is stored in instance variables of the handler. Subclasses should not need to override or extend the `!__init__`{.interpreted-text role="meth"} method.

`BaseHTTPRequestHandler`{.interpreted-text role="class"} has the following instance variables:

::: attribute
client_address

Contains a tuple of the form `(host, port)` referring to the client\'s address.
:::

::: attribute
server

Contains the server instance.
:::

::: attribute
close_connection

Boolean that should be set before `handle_one_request`{.interpreted-text role="meth"} returns, indicating if another request may be expected, or if the connection should be shut down.
:::

::: attribute
requestline

Contains the string representation of the HTTP request line. The terminating CRLF is stripped. This attribute should be set by `handle_one_request`{.interpreted-text role="meth"}. If no valid request line was processed, it should be set to the empty string.
:::

::: attribute
command

Contains the command (request type). For example, `'GET'`.
:::

::: attribute
path

Contains the request path. If query component of the URL is present, then `path` includes the query. Using the terminology of `3986`{.interpreted-text role="rfc"}, `path` here includes `hier-part` and the `query`.
:::

::: attribute
request_version

Contains the version string from the request. For example, `'HTTP/1.0'`.
:::

::: attribute
headers

Holds an instance of the class specified by the `MessageClass`{.interpreted-text role="attr"} class variable. This instance parses and manages the headers in the HTTP request. The `~http.client.parse_headers`{.interpreted-text role="func"} function from `http.client`{.interpreted-text role="mod"} is used to parse the headers and it requires that the HTTP request provide a valid `5322`{.interpreted-text role="rfc"} style header.
:::

::: attribute
rfile

An `io.BufferedIOBase`{.interpreted-text role="class"} input stream, ready to read from the start of the optional input data.
:::

:::: attribute
wfile

Contains the output stream for writing a response back to the client. Proper adherence to the HTTP protocol must be used when writing to this stream in order to achieve successful interoperation with HTTP clients.

::: versionchanged
3.6 This is an `io.BufferedIOBase`{.interpreted-text role="class"} stream.
:::
::::

`BaseHTTPRequestHandler`{.interpreted-text role="class"} has the following attributes:

::: attribute
server_version

Specifies the server software version. You may want to override this. The format is multiple whitespace-separated strings, where each string is of the form name\[/version\]. For example, `'BaseHTTP/0.2'`.
:::

::: attribute
sys_version

Contains the Python system version, in a form usable by the `version_string`{.interpreted-text role="attr"} method and the `server_version`{.interpreted-text role="attr"} class variable. For example, `'Python/1.4'`.
:::

::: attribute
error_message_format

Specifies a format string that should be used by `send_error`{.interpreted-text role="meth"} method for building an error response to the client. The string is filled by default with variables from `responses`{.interpreted-text role="attr"} based on the status code that passed to `send_error`{.interpreted-text role="meth"}.
:::

::: attribute
error_content_type

Specifies the Content-Type HTTP header of error responses sent to the client. The default value is `'text/html'`.
:::

::: attribute
protocol_version

Specifies the HTTP version to which the server is conformant. It is sent in responses to let the client know the server\'s communication capabilities for future requests. If set to `'HTTP/1.1'`, the server will permit HTTP persistent connections; however, your server *must* then include an accurate `Content-Length` header (using `send_header`{.interpreted-text role="meth"}) in all of its responses to clients. For backwards compatibility, the setting defaults to `'HTTP/1.0'`.
:::

::: attribute
MessageClass

Specifies an `email.message.Message`{.interpreted-text role="class"}-like class to parse HTTP headers. Typically, this is not overridden, and it defaults to `http.client.HTTPMessage`{.interpreted-text role="class"}.
:::

::: attribute
responses

This attribute contains a mapping of error code integers to two-element tuples containing a short and long message. For example, `{code: (shortmessage, longmessage)}`. The *shortmessage* is usually used as the *message* key in an error response, and *longmessage* as the *explain* key. It is used by `send_response_only`{.interpreted-text role="meth"} and `send_error`{.interpreted-text role="meth"} methods.
:::

A `BaseHTTPRequestHandler`{.interpreted-text role="class"} instance has the following methods:

::: method
handle()

Calls `handle_one_request`{.interpreted-text role="meth"} once (or, if persistent connections are enabled, multiple times) to handle incoming HTTP requests. You should never need to override it; instead, implement appropriate `!do_\*`{.interpreted-text role="meth"} methods.
:::

::: method
handle_one_request()

This method will parse and dispatch the request to the appropriate `!do_\*`{.interpreted-text role="meth"} method. You should never need to override it.
:::

:::: method
handle_expect_100()

When an HTTP/1.1 conformant server receives an `Expect: 100-continue` request header it responds back with a `100 Continue` followed by `200 OK` headers. This method can be overridden to raise an error if the server does not want the client to continue. For e.g. server can choose to send `417 Expectation Failed` as a response header and `return False`.

::: versionadded
3.2
:::
::::

:::: method
send_error(code, message=None, explain=None)

Sends and logs a complete error reply to the client. The numeric *code* specifies the HTTP error code, with *message* as an optional, short, human readable description of the error. The *explain* argument can be used to provide more detailed information about the error; it will be formatted using the `error_message_format`{.interpreted-text role="attr"} attribute and emitted, after a complete set of headers, as the response body. The `responses`{.interpreted-text role="attr"} attribute holds the default values for *message* and *explain* that will be used if no value is provided; for unknown codes the default value for both is the string `???`. The body will be empty if the method is HEAD or the response code is one of the following: `1{xx}`{.interpreted-text role="samp"}, `204 No Content`, `205 Reset Content`, `304 Not Modified`.

::: versionchanged
3.4 The error response includes a Content-Length header. Added the *explain* argument.
:::
::::

:::: method
send_response(code, message=None)

Adds a response header to the headers buffer and logs the accepted request. The HTTP response line is written to the internal buffer, followed by *Server* and *Date* headers. The values for these two headers are picked up from the `version_string`{.interpreted-text role="meth"} and `date_time_string`{.interpreted-text role="meth"} methods, respectively. If the server does not intend to send any other headers using the `send_header`{.interpreted-text role="meth"} method, then `send_response`{.interpreted-text role="meth"} should be followed by an `end_headers`{.interpreted-text role="meth"} call.

::: versionchanged
3.3 Headers are stored to an internal buffer and `end_headers`{.interpreted-text role="meth"} needs to be called explicitly.
:::
::::

:::: method
send_header(keyword, value)

Adds the HTTP header to an internal buffer which will be written to the output stream when either `end_headers`{.interpreted-text role="meth"} or `flush_headers`{.interpreted-text role="meth"} is invoked. *keyword* should specify the header keyword, with *value* specifying its value. Note that, after the send_header calls are done, `end_headers`{.interpreted-text role="meth"} MUST BE called in order to complete the operation.

::: versionchanged
3.2 Headers are stored in an internal buffer.
:::
::::

:::: method
send_response_only(code, message=None)

Sends the response header only, used for the purposes when `100 Continue` response is sent by the server to the client. The headers not buffered and sent directly the output stream.If the *message* is not specified, the HTTP message corresponding the response *code* is sent.

::: versionadded
3.2
:::
::::

:::: method
end_headers()

Adds a blank line (indicating the end of the HTTP headers in the response) to the headers buffer and calls `flush_headers`{.interpreted-text role="meth"}.

::: versionchanged
3.2 The buffered headers are written to the output stream.
:::
::::

:::: method
flush_headers()

Finally send the headers to the output stream and flush the internal headers buffer.

::: versionadded
3.3
:::
::::

::: method
log_request(code=\'-\', size=\'-\')

Logs an accepted (successful) request. *code* should specify the numeric HTTP code associated with the response. If a size of the response is available, then it should be passed as the *size* parameter.
:::

::: method
log_error(\...)

Logs an error when a request cannot be fulfilled. By default, it passes the message to `log_message`{.interpreted-text role="meth"}, so it takes the same arguments (*format* and additional values).
:::

::: method
log_message(format, \...)

Logs an arbitrary message to `sys.stderr`. This is typically overridden to create custom error logging mechanisms. The *format* argument is a standard printf-style format string, where the additional arguments to `log_message`{.interpreted-text role="meth"} are applied as inputs to the formatting. The client ip address and current date and time are prefixed to every message logged.
:::

::: method
version_string()

Returns the server software\'s version string. This is a combination of the `server_version`{.interpreted-text role="attr"} and `sys_version`{.interpreted-text role="attr"} attributes.
:::

::: method
date_time_string(timestamp=None)

Returns the date and time given by *timestamp* (which must be `None` or in the format returned by `time.time`{.interpreted-text role="func"}), formatted for a message header. If *timestamp* is omitted, it uses the current date and time.

The result looks like `'Sun, 06 Nov 1994 08:49:37 GMT'`.
:::

::: method
log_date_time_string()

Returns the current date and time, formatted for logging.
:::

:::: method
address_string()

Returns the client address.

::: versionchanged
3.3 Previously, a name lookup was performed. To avoid name resolution delays, it now always returns the IP address.
:::
::::
:::::::::::::::::::::::::::::::::::::::::::::

::::::::::: {.SimpleHTTPRequestHandler(request, .client_address, .server, .directory=None)}
This class serves files from the directory *directory* and below, or the current directory if *directory* is not provided, directly mapping the directory structure to HTTP requests.

::: versionchanged
3.7 Added the *directory* parameter.
:::

::: versionchanged
3.9 The *directory* parameter accepts a `path-like object`{.interpreted-text role="term"}.
:::

A lot of the work, such as parsing the request, is done by the base class `BaseHTTPRequestHandler`{.interpreted-text role="class"}. This class implements the `do_GET`{.interpreted-text role="func"} and `do_HEAD`{.interpreted-text role="func"} functions.

The following are defined as class-level attributes of `SimpleHTTPRequestHandler`{.interpreted-text role="class"}:

::: attribute
server_version

This will be `"SimpleHTTP/" + __version__`, where `__version__` is defined at the module level.
:::

:::: attribute
extensions_map

A dictionary mapping suffixes into MIME types, contains custom overrides for the default system mappings. The mapping is used case-insensitively, and so should contain only lower-cased keys.

::: versionchanged
3.9 This dictionary is no longer filled with the default system mappings, but only contains overrides.
:::
::::

The `SimpleHTTPRequestHandler`{.interpreted-text role="class"} class defines the following methods:

::: method
do_HEAD()

This method serves the `'HEAD'` request type: it sends the headers it would send for the equivalent `GET` request. See the `do_GET`{.interpreted-text role="meth"} method for a more complete explanation of the possible headers.
:::

:::: method
do_GET()

The request is mapped to a local file by interpreting the request as a path relative to the current working directory.

If the request was mapped to a directory, the directory is checked for a file named `index.html` or `index.htm` (in that order). If found, the file\'s contents are returned; otherwise a directory listing is generated by calling the `list_directory`{.interpreted-text role="meth"} method. This method uses `os.listdir`{.interpreted-text role="func"} to scan the directory, and returns a `404` error response if the `~os.listdir`{.interpreted-text role="func"} fails.

If the request was mapped to a file, it is opened. Any `OSError`{.interpreted-text role="exc"} exception in opening the requested file is mapped to a `404`, `'File not found'` error. If there was an `'If-Modified-Since'` header in the request, and the file was not modified after this time, a `304`, `'Not Modified'` response is sent. Otherwise, the content type is guessed by calling the `guess_type`{.interpreted-text role="meth"} method, which in turn uses the *extensions_map* variable, and the file contents are returned.

A `'Content-type:'` header with the guessed content type is output, followed by a `'Content-Length:'` header with the file\'s size and a `'Last-Modified:'` header with the file\'s modification time.

Then follows a blank line signifying the end of the headers, and then the contents of the file are output.

For example usage, see the implementation of the `test` function in `Lib/http/server.py`{.interpreted-text role="source"}.

::: versionchanged
3.7 Support of the `'If-Modified-Since'` header.
:::
::::
:::::::::::

The `SimpleHTTPRequestHandler`{.interpreted-text role="class"} class can be used in the following manner in order to create a very basic webserver serving files relative to the current directory:

    import http.server
    import socketserver

    PORT = 8000

    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()

`SimpleHTTPRequestHandler`{.interpreted-text role="class"} can also be subclassed to enhance behavior, such as using different index file names by overriding the class attribute `index_pages`{.interpreted-text role="attr"}.

## Command-line interface {#http-server-cli}

`!http.server`{.interpreted-text role="mod"} can also be invoked directly using the `-m`{.interpreted-text role="option"} switch of the interpreter. The following example illustrates how to serve files relative to the current directory:

    python -m http.server [OPTIONS] [port]

The following options are accepted:

::: program
http.server
:::

::: option
port

The server listens to port 8000 by default. The default can be overridden by passing the desired port number as an argument:

    python -m http.server 9000
:::

::::: option

`-b, --bind <address>`

:   

Specifies a specific address to which it should bind. Both IPv4 and IPv6 addresses are supported. By default, the server binds itself to all interfaces. For example, the following command causes the server to bind to localhost only:

    python -m http.server --bind 127.0.0.1

::: versionadded
3.4
:::

::: versionchanged
3.8 Support IPv6 in the `--bind` option.
:::
:::::

:::: option

`-d, --directory <dir>`

:   

Specifies a directory to which it should serve the files. By default, the server uses the current directory. For example, the following command uses a specific directory:

    python -m http.server --directory /tmp/

::: versionadded
3.7
:::
::::

:::: option

`-p, --protocol <version>`

:   

Specifies the HTTP version to which the server is conformant. By default, the server is conformant to HTTP/1.0. For example, the following command runs an HTTP/1.1 conformant server:

    python -m http.server --protocol HTTP/1.1

::: versionadded
3.11
:::
::::

:::: option

`--tls-cert`

:   

Specifies a TLS certificate chain for HTTPS connections:

    python -m http.server --tls-cert fullchain.pem

::: versionadded
3.14
:::
::::

:::: option

`--tls-key`

:   

Specifies a private key file for HTTPS connections.

This option requires `--tls-cert` to be specified.

::: versionadded
3.14
:::
::::

:::: option

`--tls-password-file`

:   

Specifies the password file for password-protected private keys:

    python -m http.server \
           --tls-cert cert.pem \
           --tls-key key.pem \
           --tls-password-file password.txt

This option requires [\--tls-cert]{.title-ref}\` to be specified.

::: versionadded
3.14
:::
::::

## Security considerations {#http.server-security}

::: index
pair: http.server; security
:::

`SimpleHTTPRequestHandler`{.interpreted-text role="class"} will follow symbolic links when handling requests, this makes it possible for files outside of the specified directory to be served.

Earlier versions of Python did not scrub control characters from the log messages emitted to stderr from `python -m http.server` or the default `BaseHTTPRequestHandler`{.interpreted-text role="class"} `.log_message` implementation. This could allow remote clients connecting to your server to send nefarious control codes to your terminal.

::: versionchanged
3.12 Control characters are scrubbed in stderr logs.
:::
