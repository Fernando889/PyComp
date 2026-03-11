# `!getpass`{.interpreted-text role="mod"} \-\-- Portable password input

::: {.module synopsis="Portable reading of passwords and retrieval of the userid."}
getpass
:::

**Source code:** `Lib/getpass.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

::: availability
not WASI.

This module does not work or is not available on WebAssembly. See `wasm-availability`{.interpreted-text role="ref"} for more information.
:::

The `!getpass`{.interpreted-text role="mod"} module provides two functions:

:::::::: function
getpass(prompt=\'Password: \', stream=None, \*, echo_char=None)

Prompt the user for a password without echoing. The user is prompted using the string *prompt*, which defaults to `'Password: '`. On Unix, the prompt is written to the file-like object *stream* using the replace error handler if needed. *stream* defaults to the controlling terminal (`/dev/tty`{.interpreted-text role="file"}) or if that is unavailable to `sys.stderr` (this argument is ignored on Windows).

The *echo_char* argument controls how user input is displayed while typing. If *echo_char* is `None` (default), input remains hidden. Otherwise, *echo_char* must be a single printable ASCII character and each typed character is replaced by it. For example, `echo_char='*'` will display asterisks instead of the actual input.

If echo free input is unavailable getpass() falls back to printing a warning message to *stream* and reading from `sys.stdin` and issuing a `GetPassWarning`{.interpreted-text role="exc"}.

:::: note
::: title
Note
:::

If you call getpass from within IDLE, the input may be done in the terminal you launched IDLE from rather than the idle window itself.
::::

:::: note
::: title
Note
:::

On Unix systems, when *echo_char* is set, the terminal will be configured to operate in `noncanonical mode <termios(3)#Canonical_and_noncanonical_mode>`{.interpreted-text role="manpage"}. In particular, this means that line editing shortcuts such as `Ctrl+U`{.interpreted-text role="kbd"} will not work and may insert unexpected characters into the input.
::::

::: versionchanged
3.14 Added the *echo_char* parameter for keyboard feedback.
:::
::::::::

::: exception
GetPassWarning

A `UserWarning`{.interpreted-text role="exc"} subclass issued when password input may be echoed.
:::

:::: function
getuser()

Return the \"login name\" of the user.

This function checks the environment variables `LOGNAME`{.interpreted-text role="envvar"}, `USER`{.interpreted-text role="envvar"}, `!LNAME`{.interpreted-text role="envvar"} and `USERNAME`{.interpreted-text role="envvar"}, in order, and returns the value of the first one which is set to a non-empty string. If none are set, the login name from the password database is returned on systems which support the `pwd`{.interpreted-text role="mod"} module, otherwise, an `OSError`{.interpreted-text role="exc"} is raised.

In general, this function should be preferred over `os.getlogin`{.interpreted-text role="func"}.

::: versionchanged
3.13 Previously, various exceptions beyond just `OSError`{.interpreted-text role="exc"} were raised.
:::
::::
