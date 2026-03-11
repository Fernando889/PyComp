# `!netrc`{.interpreted-text role="mod"} \-\-- netrc file processing

::: {.module synopsis="Loading of .netrc files."}
netrc
:::

**Source code:** `Lib/netrc.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

The `~netrc.netrc`{.interpreted-text role="class"} class parses and encapsulates the netrc file format used by the Unix `ftp`{.interpreted-text role="program"} program and other FTP clients.

:::::: netrc([file])
A `~netrc.netrc`{.interpreted-text role="class"} instance or subclass instance encapsulates data from a netrc file. The initialization argument, if present, specifies the file to parse. If no argument is given, the file `.netrc`{.interpreted-text role="file"} in the user\'s home directory \-- as determined by `os.path.expanduser`{.interpreted-text role="func"} \-- will be read. Otherwise, a `FileNotFoundError`{.interpreted-text role="exc"} exception will be raised. Parse errors will raise `NetrcParseError`{.interpreted-text role="exc"} with diagnostic information including the file name, line number, and terminating token.

If no argument is specified on a POSIX system, the presence of passwords in the `.netrc`{.interpreted-text role="file"} file will raise a `NetrcParseError`{.interpreted-text role="exc"} if the file ownership or permissions are insecure (owned by a user other than the user running the process, or accessible for read or write by any other user). This implements security behavior equivalent to that of ftp and other programs that use `.netrc`{.interpreted-text role="file"}. Such security checks are not available on platforms that do not support `os.getuid`{.interpreted-text role="func"}.

::: versionchanged
3.4 Added the POSIX permission check.
:::

::: versionchanged
3.7 `os.path.expanduser`{.interpreted-text role="func"} is used to find the location of the `.netrc`{.interpreted-text role="file"} file when *file* is not passed as argument.
:::

::: versionchanged
3.10 `netrc`{.interpreted-text role="class"} try UTF-8 encoding before using locale specific encoding. The entry in the netrc file no longer needs to contain all tokens. The missing tokens\' value default to an empty string. All the tokens and their values now can contain arbitrary characters, like whitespace and non-ASCII characters. If the login name is anonymous, it won\'t trigger the security check.
:::
::::::

:::::: exception
NetrcParseError

Exception raised by the `~netrc.netrc`{.interpreted-text role="class"} class when syntactical errors are encountered in source text. Instances of this exception provide three interesting attributes:

::: attribute
msg

Textual explanation of the error.
:::

::: attribute
filename

The name of the source file.
:::

::: attribute
lineno

The line number on which the error was found.
:::
::::::

## netrc Objects

A `~netrc.netrc`{.interpreted-text role="class"} instance has the following methods:

::: method
netrc.authenticators(host)

Return a 3-tuple `(login, account, password)` of authenticators for *host*. If the netrc file did not contain an entry for the given host, return the tuple associated with the \'default\' entry. If neither matching host nor default entry is available, return `None`.
:::

::: method
netrc.\_\_repr\_\_()

Dump the class data as a string in the format of a netrc file. (This discards comments and may reorder the entries.)
:::

Instances of `~netrc.netrc`{.interpreted-text role="class"} have public instance variables:

::: attribute
netrc.hosts

Dictionary mapping host names to `(login, account, password)` tuples. The \'default\' entry, if any, is represented as a pseudo-host by that name.
:::

::: attribute
netrc.macros

Dictionary mapping macro names to string lists.
:::
