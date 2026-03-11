# `!smtplib`{.interpreted-text role="mod"} \-\-- SMTP protocol client

::: {.module synopsis="SMTP protocol client (requires sockets)."}
smtplib
:::

**Source code:** `Lib/smtplib.py`{.interpreted-text role="source"}

::: index
pair: SMTP; protocol single: Simple Mail Transfer Protocol
:::

------------------------------------------------------------------------

The `!smtplib`{.interpreted-text role="mod"} module defines an SMTP client session object that can be used to send mail to any internet machine with an SMTP or ESMTP listener daemon. For details of SMTP and ESMTP operation, consult `821`{.interpreted-text role="rfc"} (Simple Mail Transfer Protocol) and `1869`{.interpreted-text role="rfc"} (SMTP Service Extensions).

::: availability
not WASI.

This module does not work or is not available on WebAssembly. See `wasm-availability`{.interpreted-text role="ref"} for more information.
:::

::::::::: {.SMTP(host='', .port=0, .local_hostname=None[, .timeout], .source_address=None)}
An `SMTP`{.interpreted-text role="class"} instance encapsulates an SMTP connection. It has methods that support a full repertoire of SMTP and ESMTP operations.

If the host parameter is set to a truthy value, `SMTP.connect`{.interpreted-text role="meth"} is called with host and port automatically when the object is created; otherwise, `!connect`{.interpreted-text role="meth"} must be called manually.

If specified, *local_hostname* is used as the FQDN of the local host in the HELO/EHLO command. Otherwise, the local hostname is found using `socket.getfqdn`{.interpreted-text role="func"}. If the `connect`{.interpreted-text role="meth"} call returns anything other than a success code, an `SMTPConnectError`{.interpreted-text role="exc"} is raised. The optional *timeout* parameter specifies a timeout in seconds for blocking operations like the connection attempt (if not specified, the global default timeout setting will be used). If the timeout expires, `TimeoutError`{.interpreted-text role="exc"} is raised. The optional *source_address* parameter allows binding to some specific source address in a machine with multiple network interfaces, and/or to some specific source TCP port. It takes a 2-tuple `(host, port)`, for the socket to bind to as its source address before connecting. If omitted (or if *host* or *port* are `''` and/or `0` respectively) the OS default behavior will be used.

For normal use, you should only require the initialization/connect, `sendmail`{.interpreted-text role="meth"}, and `SMTP.quit`{.interpreted-text role="meth"} methods. An example is included below.

The `SMTP`{.interpreted-text role="class"} class supports the `with`{.interpreted-text role="keyword"} statement. When used like this, the SMTP `QUIT` command is issued automatically when the `!with`{.interpreted-text role="keyword"} statement exits. E.g.:

    >>> from smtplib import SMTP
    >>> with SMTP("domain.org") as smtp:
    ...     smtp.noop()
    ...
    (250, b'Ok')
    >>>

::: audit-event
smtplib.send self,data smtplib.SMTP

All commands will raise an `auditing event <auditing>`{.interpreted-text role="ref"} `smtplib.SMTP.send` with arguments `self` and `data`, where `data` is the bytes about to be sent to the remote host.
:::

::: attribute
SMTP.default_port

The default port used for SMTP connections (25).
:::

::: versionchanged
3.3 Support for the `with`{.interpreted-text role="keyword"} statement was added.
:::

::: versionchanged
3.3 *source_address* argument was added.
:::

::: versionadded
3.5 The SMTPUTF8 extension (`6531`{.interpreted-text role="rfc"}) is now supported.
:::

::: versionchanged
3.9 If the *timeout* parameter is set to be zero, it will raise a `ValueError`{.interpreted-text role="class"} to prevent the creation of a non-blocking socket.
:::
:::::::::

::::::::: {.SMTP_SSL(host='', .port=0, .local_hostname=None, .* .[, .timeout], .\\ .context=None, .source_address=None)}
An `SMTP_SSL`{.interpreted-text role="class"} instance behaves exactly the same as instances of `SMTP`{.interpreted-text role="class"}. `SMTP_SSL`{.interpreted-text role="class"} should be used for situations where SSL is required from the beginning of the connection and using `SMTP.starttls`{.interpreted-text role="meth"} is not appropriate.

If the host parameter is set to a truthy value, `SMTP.connect`{.interpreted-text role="meth"} is called with host and port automatically when the object is created; otherwise, `!SMTP.connect`{.interpreted-text role="meth"} must be called manually.

The optional arguments *local_hostname*, *timeout* and *source_address* have the same meaning as they do in the `SMTP`{.interpreted-text role="class"} class. *context*, also optional, can contain a `~ssl.SSLContext`{.interpreted-text role="class"} and allows configuring various aspects of the secure connection. Please read `ssl-security`{.interpreted-text role="ref"} for best practices.

::: attribute
SMTP_SSL.default_port

The default port used for SMTP-over-SSL connections (465).
:::

::: versionchanged
3.3 *context* was added.
:::

::: versionchanged
3.3 The *source_address* argument was added.
:::

::: versionchanged
3.4 The class now supports hostname check with `ssl.SSLContext.check_hostname`{.interpreted-text role="attr"} and *Server Name Indication* (see `ssl.HAS_SNI`{.interpreted-text role="const"}).
:::

::: versionchanged
3.9 If the *timeout* parameter is set to be zero, it will raise a `ValueError`{.interpreted-text role="class"} to prevent the creation of a non-blocking socket
:::

::: versionchanged
3.12 The deprecated *keyfile* and *certfile* parameters have been removed.
:::
:::::::::

:::: {.LMTP(host='', .port=LMTP_PORT, .local_hostname=None, .\\ .source_address=None[, .timeout])}
The LMTP protocol, which is very similar to ESMTP, is heavily based on the standard SMTP client. It\'s common to use Unix sockets for LMTP, so our `~SMTP.connect`{.interpreted-text role="meth"} method must support that as well as a regular host:port server. The optional arguments *local_hostname* and *source_address* have the same meaning as they do in the `SMTP`{.interpreted-text role="class"} class. To specify a Unix socket, you must use an absolute path for *host*, starting with a \'/\'.

Authentication is supported, using the regular SMTP mechanism. When using a Unix socket, LMTP generally don\'t support or require any authentication, but your mileage might vary.

::: versionchanged
3.9 The optional *timeout* parameter was added.
:::
::::

A nice selection of exceptions is defined as well:

:::: exception
SMTPException

Subclass of `OSError`{.interpreted-text role="exc"} that is the base exception class for all the other exceptions provided by this module.

::: versionchanged
3.4 SMTPException became subclass of `OSError`{.interpreted-text role="exc"}
:::
::::

::: exception
SMTPServerDisconnected

This exception is raised when the server unexpectedly disconnects, or when an attempt is made to use the `SMTP`{.interpreted-text role="class"} instance before connecting it to a server.
:::

::::: exception
SMTPResponseException

Base class for all exceptions that include an SMTP error code. These exceptions are generated in some instances when the SMTP server returns an error code.

::: attribute
smtp_code

The error code.
:::

::: attribute
smtp_error

The error message.
:::
:::::

::: exception
SMTPSenderRefused

Sender address refused. In addition to the attributes set by on all `SMTPResponseException`{.interpreted-text role="exc"} exceptions, this sets \'sender\' to the string that the SMTP server refused.
:::

:::: exception
SMTPRecipientsRefused

All recipient addresses refused.

::: attribute
recipients

A dictionary of exactly the same sort as returned by `SMTP.sendmail`{.interpreted-text role="meth"} containing the errors for each recipient.
:::
::::

::: exception
SMTPDataError

The SMTP server refused to accept the message data.
:::

::: exception
SMTPConnectError

Error occurred during establishment of a connection with the server.
:::

::: exception
SMTPHeloError

The server refused our `HELO` message.
:::

:::: exception
SMTPNotSupportedError

The command or option attempted is not supported by the server.

::: versionadded
3.5
:::
::::

::: exception
SMTPAuthenticationError

SMTP authentication went wrong. Most probably the server didn\'t accept the username/password combination provided.
:::

::: seealso

`821`{.interpreted-text role="rfc"} - Simple Mail Transfer Protocol

:   Protocol definition for SMTP. This document covers the model, operating procedure, and protocol details for SMTP.

`1869`{.interpreted-text role="rfc"} - SMTP Service Extensions

:   Definition of the ESMTP extensions for SMTP. This describes a framework for extending SMTP with new commands, supporting dynamic discovery of the commands provided by the server, and defines a few additional commands.
:::

## SMTP Objects

An `SMTP`{.interpreted-text role="class"} instance has the following methods:

:::: method
SMTP.set_debuglevel(level)

Set the debug output level. A value of 1 or `True` for *level* results in debug messages for connection and for all messages sent to and received from the server. A value of 2 for *level* results in these messages being timestamped.

::: versionchanged
3.5 Added debuglevel 2.
:::
::::

::: method
SMTP.docmd(cmd, args=\'\')

Send a command *cmd* to the server. The optional argument *args* is simply concatenated to the command, separated by a space.

This returns a 2-tuple composed of a numeric response code and the actual response line (multiline responses are joined into one long line.)

In normal operation it should not be necessary to call this method explicitly. It is used to implement other methods and may be useful for testing private extensions.

If the connection to the server is lost while waiting for the reply, `SMTPServerDisconnected`{.interpreted-text role="exc"} will be raised.
:::

:::: method
SMTP.connect(host=\'localhost\', port=0)

Connect to a host on a given port. The defaults are to connect to the local host at the standard SMTP port (25). If the hostname ends with a colon (`':'`) followed by a number, that suffix will be stripped off and the number interpreted as the port number to use. This method is automatically invoked by the constructor if a host is specified during instantiation. Returns a 2-tuple of the response code and message sent by the server in its connection response.

If port is not changed from its default value of 0, the value of the `default_port`{.interpreted-text role="attr"} attribute is used.

::: audit-event
smtplib.connect self,host,port smtplib.SMTP.connect
:::
::::

::: method
SMTP.helo(name=\'\')

Identify yourself to the SMTP server using `HELO`. The hostname argument defaults to the fully qualified domain name of the local host. The message returned by the server is stored as the `helo_resp`{.interpreted-text role="attr"} attribute of the object.

In normal operation it should not be necessary to call this method explicitly. It will be implicitly called by the `sendmail`{.interpreted-text role="meth"} when necessary.
:::

::: method
SMTP.ehlo(name=\'\')

Identify yourself to an ESMTP server using `EHLO`. The hostname argument defaults to the fully qualified domain name of the local host. Examine the response for ESMTP option and store them for use by `has_extn`{.interpreted-text role="meth"}. Also sets several informational attributes: the message returned by the server is stored as the `ehlo_resp`{.interpreted-text role="attr"} attribute, `does_esmtp`{.interpreted-text role="attr"} is set to `True` or `False` depending on whether the server supports ESMTP, and `esmtp_features`{.interpreted-text role="attr"} will be a dictionary containing the names of the SMTP service extensions this server supports, and their parameters (if any).

Unless you wish to use `has_extn`{.interpreted-text role="meth"} before sending mail, it should not be necessary to call this method explicitly. It will be implicitly called by `sendmail`{.interpreted-text role="meth"} when necessary.
:::

::: method
SMTP.ehlo_or_helo_if_needed()

This method calls `ehlo`{.interpreted-text role="meth"} and/or `helo`{.interpreted-text role="meth"} if there has been no previous `EHLO` or `HELO` command this session. It tries ESMTP `EHLO` first.

`SMTPHeloError`{.interpreted-text role="exc"}

:   The server didn\'t reply properly to the `HELO` greeting.
:::

::: method
SMTP.has_extn(name)

Return `True`{.interpreted-text role="const"} if *name* is in the set of SMTP service extensions returned by the server, `False`{.interpreted-text role="const"} otherwise. Case is ignored.
:::

::::: method
SMTP.verify(address)

Check the validity of an address on this server using SMTP `VRFY`. Returns a tuple consisting of code 250 and a full `822`{.interpreted-text role="rfc"} address (including human name) if the user address is valid. Otherwise returns an SMTP error code of 400 or greater and an error string.

:::: note
::: title
Note
:::

Many sites disable SMTP `VRFY` in order to foil spammers.
::::
:::::

:::: method
SMTP.login(user, password, \*, initial_response_ok=True)

Log in on an SMTP server that requires authentication. The arguments are the username and the password to authenticate with. If there has been no previous `EHLO` or `HELO` command this session, this method tries ESMTP `EHLO` first. This method will return normally if the authentication was successful, or may raise the following exceptions:

`SMTPHeloError`{.interpreted-text role="exc"}

:   The server didn\'t reply properly to the `HELO` greeting.

`SMTPAuthenticationError`{.interpreted-text role="exc"}

:   The server didn\'t accept the username/password combination.

`SMTPNotSupportedError`{.interpreted-text role="exc"}

:   The `AUTH` command is not supported by the server.

`SMTPException`{.interpreted-text role="exc"}

:   No suitable authentication method was found.

Each of the authentication methods supported by `!smtplib`{.interpreted-text role="mod"} are tried in turn if they are advertised as supported by the server. See `auth`{.interpreted-text role="meth"} for a list of supported authentication methods. *initial_response_ok* is passed through to `auth`{.interpreted-text role="meth"}.

Optional keyword argument *initial_response_ok* specifies whether, for authentication methods that support it, an \"initial response\" as specified in `4954`{.interpreted-text role="rfc"} can be sent along with the `AUTH` command, rather than requiring a challenge/response.

::: versionchanged
3.5 `SMTPNotSupportedError`{.interpreted-text role="exc"} may be raised, and the *initial_response_ok* parameter was added.
:::
::::

:::: method
SMTP.auth(mechanism, authobject, \*, initial_response_ok=True)

Issue an `SMTP` `AUTH` command for the specified authentication *mechanism*, and handle the challenge response via *authobject*.

*mechanism* specifies which authentication mechanism is to be used as argument to the `AUTH` command; the valid values are those listed in the `auth` element of `esmtp_features`{.interpreted-text role="attr"}.

*authobject* must be a callable object taking an optional single argument:

    data = authobject(challenge=None)

If optional keyword argument *initial_response_ok* is true, `authobject()` will be called first with no argument. It can return the `4954`{.interpreted-text role="rfc"} \"initial response\" ASCII `str` which will be encoded and sent with the `AUTH` command as below. If the `authobject()` does not support an initial response (e.g. because it requires a challenge), it should return `None` when called with `challenge=None`. If *initial_response_ok* is false, then `authobject()` will not be called first with `None`.

If the initial response check returns `None`, or if *initial_response_ok* is false, `authobject()` will be called to process the server\'s challenge response; the *challenge* argument it is passed will be a `bytes`. It should return ASCII `str` *data* that will be base64 encoded and sent to the server.

The `SMTP` class provides `authobjects` for the `CRAM-MD5`, `PLAIN`, and `LOGIN` mechanisms; they are named `SMTP.auth_cram_md5`, `SMTP.auth_plain`, and `SMTP.auth_login` respectively. They all require that the `user` and `password` properties of the `SMTP` instance are set to appropriate values.

User code does not normally need to call `auth` directly, but can instead call the `login`{.interpreted-text role="meth"} method, which will try each of the above mechanisms in turn, in the order listed. `auth` is exposed to facilitate the implementation of authentication methods not (or not yet) supported directly by `!smtplib`{.interpreted-text role="mod"}.

::: versionadded
3.5
:::
::::

::::::: method
SMTP.starttls(\*, context=None)

Put the SMTP connection in TLS (Transport Layer Security) mode. All SMTP commands that follow will be encrypted. You should then call `ehlo`{.interpreted-text role="meth"} again.

If *keyfile* and *certfile* are provided, they are used to create an `ssl.SSLContext`{.interpreted-text role="class"}.

Optional *context* parameter is an `ssl.SSLContext`{.interpreted-text role="class"} object; This is an alternative to using a keyfile and a certfile and if specified both *keyfile* and *certfile* should be `None`.

If there has been no previous `EHLO` or `HELO` command this session, this method tries ESMTP `EHLO` first.

::: versionchanged
3.12 The deprecated *keyfile* and *certfile* parameters have been removed.
:::

`SMTPHeloError`{.interpreted-text role="exc"}

:   The server didn\'t reply properly to the `HELO` greeting.

`SMTPNotSupportedError`{.interpreted-text role="exc"}

:   The server does not support the STARTTLS extension.

`RuntimeError`{.interpreted-text role="exc"}

:   SSL/TLS support is not available to your Python interpreter.

::: versionchanged
3.3 *context* was added.
:::

::: versionchanged
3.4 The method now supports hostname check with `ssl.SSLContext.check_hostname`{.interpreted-text role="attr"} and *Server Name Indicator* (see `~ssl.HAS_SNI`{.interpreted-text role="const"}).
:::

::: versionchanged
3.5 The error raised for lack of STARTTLS support is now the `SMTPNotSupportedError`{.interpreted-text role="exc"} subclass instead of the base `SMTPException`{.interpreted-text role="exc"}.
:::
:::::::

::::::: method
SMTP.sendmail(from_addr, to_addrs, msg, mail_options=(), rcpt_options=())

Send mail. The required arguments are an `822`{.interpreted-text role="rfc"} from-address string, a list of `822`{.interpreted-text role="rfc"} to-address strings (a bare string will be treated as a list with 1 address), and a message string. The caller may pass a list of ESMTP options (such as `"8bitmime"`) to be used in `MAIL FROM` commands as *mail_options*. ESMTP options (such as `DSN` commands) that should be used with all `RCPT` commands can be passed as *rcpt_options*. Each option should be passed as a string containing the full text of the option, including any potential key (for instance, `"NOTIFY=SUCCESS,FAILURE"`). (If you need to use different ESMTP options to different recipients you have to use the low-level methods such as `!mail`{.interpreted-text role="meth"}, `!rcpt`{.interpreted-text role="meth"} and `!data`{.interpreted-text role="meth"} to send the message.)

:::: note
::: title
Note
:::

The *from_addr* and *to_addrs* parameters are used to construct the message envelope used by the transport agents. `sendmail` does not modify the message headers in any way.
::::

*msg* may be a string containing characters in the ASCII range, or a byte string. A string is encoded to bytes using the ascii codec, and lone `\r` and `\n` characters are converted to `\r\n` characters. A byte string is not modified.

If there has been no previous `EHLO` or `HELO` command this session, this method tries ESMTP `EHLO` first. If the server does ESMTP, message size and each of the specified options will be passed to it (if the option is in the feature set the server advertises). If `EHLO` fails, `HELO` will be tried and ESMTP options suppressed.

This method will return normally if the mail is accepted for at least one recipient. Otherwise it will raise an exception. That is, if this method does not raise an exception, then someone should get your mail. If this method does not raise an exception, it returns a dictionary, with one entry for each recipient that was refused. Each entry contains a tuple of the SMTP error code and the accompanying error message sent by the server.

If `SMTPUTF8` is included in *mail_options*, and the server supports it, *from_addr* and *to_addrs* may contain non-ASCII characters.

This method may raise the following exceptions:

`SMTPRecipientsRefused`{.interpreted-text role="exc"}

:   All recipients were refused. Nobody got the mail.

`SMTPHeloError`{.interpreted-text role="exc"}

:   The server didn\'t reply properly to the `HELO` greeting.

`SMTPSenderRefused`{.interpreted-text role="exc"}

:   The server didn\'t accept the *from_addr*.

`SMTPDataError`{.interpreted-text role="exc"}

:   The server replied with an unexpected error code (other than a refusal of a recipient).

`SMTPNotSupportedError`{.interpreted-text role="exc"}

:   `SMTPUTF8` was given in the *mail_options* but is not supported by the server.

Unless otherwise noted, the connection will be open even after an exception is raised.

::: versionchanged
3.2 *msg* may be a byte string.
:::

::: versionchanged
3.5 `SMTPUTF8` support added, and `SMTPNotSupportedError`{.interpreted-text role="exc"} may be raised if `SMTPUTF8` is specified but the server does not support it.
:::
:::::::

::::: method
SMTP.send_message(msg, from_addr=None, to_addrs=None, mail_options=(), rcpt_options=())

This is a convenience method for calling `sendmail`{.interpreted-text role="meth"} with the message represented by an `email.message.Message`{.interpreted-text role="class"} object. The arguments have the same meaning as for `sendmail`{.interpreted-text role="meth"}, except that *msg* is a `Message` object.

If *from_addr* is `None` or *to_addrs* is `None`, `send_message` fills those arguments with addresses extracted from the headers of *msg* as specified in `5322`{.interpreted-text role="rfc"}: *from_addr* is set to the `Sender`{.interpreted-text role="mailheader"} field if it is present, and otherwise to the `From`{.interpreted-text role="mailheader"} field. *to_addrs* combines the values (if any) of the `To`{.interpreted-text role="mailheader"}, `Cc`{.interpreted-text role="mailheader"}, and `Bcc`{.interpreted-text role="mailheader"} fields from *msg*. If exactly one set of `Resent-*`{.interpreted-text role="mailheader"} headers appear in the message, the regular headers are ignored and the `Resent-*`{.interpreted-text role="mailheader"} headers are used instead. If the message contains more than one set of `Resent-*`{.interpreted-text role="mailheader"} headers, a `ValueError`{.interpreted-text role="exc"} is raised, since there is no way to unambiguously detect the most recent set of `Resent-`{.interpreted-text role="mailheader"} headers.

`send_message` serializes *msg* using `~email.generator.BytesGenerator`{.interpreted-text role="class"} with `\r\n` as the *linesep*, and calls `sendmail`{.interpreted-text role="meth"} to transmit the resulting message. Regardless of the values of *from_addr* and *to_addrs*, `send_message` does not transmit any `Bcc`{.interpreted-text role="mailheader"} or `Resent-Bcc`{.interpreted-text role="mailheader"} headers that may appear in *msg*. If any of the addresses in *from_addr* and *to_addrs* contain non-ASCII characters and the server does not advertise `SMTPUTF8` support, an `SMTPNotSupportedError`{.interpreted-text role="exc"} is raised. Otherwise the `Message` is serialized with a clone of its `~email.policy`{.interpreted-text role="mod"} with the `~email.policy.EmailPolicy.utf8`{.interpreted-text role="attr"} attribute set to `True`, and `SMTPUTF8` and `BODY=8BITMIME` are added to *mail_options*.

::: versionadded
3.2
:::

::: versionadded
3.5 Support for internationalized addresses (`SMTPUTF8`).
:::
:::::

::: method
SMTP.quit()

Terminate the SMTP session and close the connection. Return the result of the SMTP `QUIT` command.
:::

Low-level methods corresponding to the standard SMTP/ESMTP commands `HELP`, `RSET`, `NOOP`, `MAIL`, `RCPT`, and `DATA` are also supported. Normally these do not need to be called directly, so they are not documented here. For details, consult the module code.

Additionally, an SMTP instance has the following attributes:

::: attribute
SMTP.helo_resp

The response to the `HELO` command, see `helo`{.interpreted-text role="meth"}.
:::

::: attribute
SMTP.ehlo_resp

The response to the `EHLO` command, see `ehlo`{.interpreted-text role="meth"}.
:::

::: attribute
SMTP.does_esmtp

A boolean value indicating whether the server supports ESMTP, see `ehlo`{.interpreted-text role="meth"}.
:::

::: attribute
SMTP.esmtp_features

A dictionary of the names of SMTP service extensions supported by the server, see `ehlo`{.interpreted-text role="meth"}.
:::

## SMTP Example

This example prompts the user for addresses needed in the message envelope (\'To\' and \'From\' addresses), and the message to be delivered. Note that the headers to be included with the message must be included in the message as entered; this example doesn\'t do any processing of the `822`{.interpreted-text role="rfc"} headers. In particular, the \'To\' and \'From\' addresses must be included in the message headers explicitly:

    import smtplib

    def prompt(title):
        return input(title).strip()

    from_addr = prompt("From: ")
    to_addrs  = prompt("To: ").split()
    print("Enter message, end with ^D (Unix) or ^Z (Windows):")

    # Add the From: and To: headers at the start!
    lines = [f"From: {from_addr}", f"To: {', '.join(to_addrs)}", ""]
    while True:
        try:
            line = input()
        except EOFError:
            break
        else:
            lines.append(line)

    msg = "\r\n".join(lines)
    print("Message length is", len(msg))

    server = smtplib.SMTP("localhost")
    server.set_debuglevel(1)
    server.sendmail(from_addr, to_addrs, msg)
    server.quit()

:::: note
::: title
Note
:::

In general, you will want to use the `email`{.interpreted-text role="mod"} package\'s features to construct an email message, which you can then send via `~smtplib.SMTP.send_message`{.interpreted-text role="meth"}; see `email-examples`{.interpreted-text role="ref"}.
::::
