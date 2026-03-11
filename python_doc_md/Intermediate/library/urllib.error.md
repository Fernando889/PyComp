# `!urllib.error`{.interpreted-text role="mod"} \-\-- Exception classes raised by urllib.request

::: {.module synopsis="Exception classes raised by urllib.request."}
urllib.error
:::

**Source code:** `Lib/urllib/error.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

The `!urllib.error`{.interpreted-text role="mod"} module defines the exception classes for exceptions raised by `urllib.request`{.interpreted-text role="mod"}. The base exception class is `URLError`{.interpreted-text role="exc"}.

The following exceptions are raised by `!urllib.error`{.interpreted-text role="mod"} as appropriate:

::::: exception
URLError

The handlers raise this exception (or derived exceptions) when they run into a problem. It is a subclass of `OSError`{.interpreted-text role="exc"}.

::: attribute
reason

The reason for this error. It can be a message string or another exception instance.
:::

::: versionchanged
3.3 `URLError`{.interpreted-text role="exc"} used to be a subtype of `IOError`{.interpreted-text role="exc"}, which is now an alias of `OSError`{.interpreted-text role="exc"}.
:::
:::::

::::::::: exception
HTTPError(url, code, msg, hdrs, fp)

Though being an exception (a subclass of `URLError`{.interpreted-text role="exc"}), an `HTTPError`{.interpreted-text role="exc"} can also function as a non-exceptional file-like return value (the same thing that `~urllib.request.urlopen`{.interpreted-text role="func"} returns). This is useful when handling exotic HTTP errors, such as requests for authentication.

::: attribute
url

Contains the request URL. An alias for *filename* attribute.
:::

::: attribute
code

An HTTP status code as defined in `2616`{.interpreted-text role="rfc"}. This numeric value corresponds to a value found in the dictionary of codes as found in `http.server.BaseHTTPRequestHandler.responses`{.interpreted-text role="attr"}.
:::

::: attribute
reason

This is usually a string explaining the reason for this error. An alias for *msg* attribute.
:::

:::: attribute
headers

The HTTP response headers for the HTTP request that caused the `HTTPError`{.interpreted-text role="exc"}. An alias for *hdrs* attribute.

::: versionadded
3.4
:::
::::

::: attribute
fp

A file-like object where the HTTP error body can be read from.
:::
:::::::::

:::: exception
ContentTooShortError(msg, content)

This exception is raised when the `~urllib.request.urlretrieve`{.interpreted-text role="func"} function detects that the amount of the downloaded data is less than the expected amount (given by the *Content-Length* header).

::: attribute
content

The downloaded (and supposedly truncated) data.
:::
::::
