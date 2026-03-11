# `!urllib.robotparser`{.interpreted-text role="mod"} \-\-- Parser for robots.txt

::: {.module synopsis="Load a robots.txt file and answer questions about
fetchability of other URLs."}
urllib.robotparser
:::

**Source code:** `Lib/urllib/robotparser.py`{.interpreted-text role="source"}

::: index
single: WWW single: World Wide Web single: URL single: robots.txt
:::

------------------------------------------------------------------------

This module provides a single class, `RobotFileParser`{.interpreted-text role="class"}, which answers questions about whether or not a particular user agent can fetch a URL on the website that published the `robots.txt`{.interpreted-text role="file"} file. For more details on the structure of `robots.txt`{.interpreted-text role="file"} files, see <http://www.robotstxt.org/orig.html>.

::::::::::::::: RobotFileParser(url='')
This class provides methods to read, parse and answer questions about the `robots.txt`{.interpreted-text role="file"} file at *url*.

::: method
set_url(url)

Sets the URL referring to a `robots.txt`{.interpreted-text role="file"} file.
:::

::: method
read()

Reads the `robots.txt`{.interpreted-text role="file"} URL and feeds it to the parser.
:::

::: method
parse(lines)

Parses the lines argument.
:::

::: method
can_fetch(useragent, url)

Returns `True` if the *useragent* is allowed to fetch the *url* according to the rules contained in the parsed `robots.txt`{.interpreted-text role="file"} file.
:::

::: method
mtime()

Returns the time the `robots.txt` file was last fetched. This is useful for long-running web spiders that need to check for new `robots.txt` files periodically.
:::

::: method
modified()

Sets the time the `robots.txt` file was last fetched to the current time.
:::

:::: method
crawl_delay(useragent)

Returns the value of the `Crawl-delay` parameter from `robots.txt` for the *useragent* in question. If there is no such parameter or it doesn\'t apply to the *useragent* specified or the `robots.txt` entry for this parameter has invalid syntax, return `None`.

::: versionadded
3.6
:::
::::

:::: method
request_rate(useragent)

Returns the contents of the `Request-rate` parameter from `robots.txt` as a `named tuple`{.interpreted-text role="term"} `RequestRate(requests, seconds)`. If there is no such parameter or it doesn\'t apply to the *useragent* specified or the `robots.txt` entry for this parameter has invalid syntax, return `None`.

::: versionadded
3.6
:::
::::

:::: method
site_maps()

Returns the contents of the `Sitemap` parameter from `robots.txt` in the form of a `list`{.interpreted-text role="func"}. If there is no such parameter or the `robots.txt` entry for this parameter has invalid syntax, return `None`.

::: versionadded
3.8
:::
::::
:::::::::::::::

The following example demonstrates basic use of the `RobotFileParser`{.interpreted-text role="class"} class:

    >>> import urllib.robotparser
    >>> rp = urllib.robotparser.RobotFileParser()
    >>> rp.set_url("http://www.pythontest.net/robots.txt")
    >>> rp.read()
    >>> rrate = rp.request_rate("*")
    >>> rrate.requests
    1
    >>> rrate.seconds
    1
    >>> rp.crawl_delay("*")
    6
    >>> rp.can_fetch("*", "http://www.pythontest.net/")
    True
    >>> rp.can_fetch("*", "http://www.pythontest.net/no-robots-here/")
    False
