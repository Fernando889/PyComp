# `!tty`{.interpreted-text role="mod"} \-\-- Terminal control functions

::: {.module synopsis="Utility functions that perform common terminal control operations."}
tty
:::

**Source code:** `Lib/tty.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

The `!tty`{.interpreted-text role="mod"} module defines functions for putting the tty into cbreak and raw modes.

::: availability
Unix.
:::

Because it requires the `termios`{.interpreted-text role="mod"} module, it will work only on Unix.

The `!tty`{.interpreted-text role="mod"} module defines the following functions:

:::: function
cfmakeraw(mode)

Convert the tty attribute list *mode*, which is a list like the one returned by `termios.tcgetattr`{.interpreted-text role="func"}, to that of a tty in raw mode.

::: versionadded
3.12
:::
::::

::::: function
cfmakecbreak(mode)

Convert the tty attribute list *mode*, which is a list like the one returned by `termios.tcgetattr`{.interpreted-text role="func"}, to that of a tty in cbreak mode.

This clears the `ECHO` and `ICANON` local mode flags in *mode* as well as setting the minimum input to 1 byte with no delay.

::: versionadded
3.12
:::

::: versionchanged
3.12.2 The `ICRNL` flag is no longer cleared. This matches Linux and macOS `stty cbreak` behavior and what `setcbreak`{.interpreted-text role="func"} historically did.
:::
:::::

:::: function
setraw(fd, when=termios.TCSAFLUSH)

Change the mode of the file descriptor *fd* to raw. If *when* is omitted, it defaults to `termios.TCSAFLUSH`{.interpreted-text role="const"}, and is passed to `termios.tcsetattr`{.interpreted-text role="func"}. The return value of `termios.tcgetattr`{.interpreted-text role="func"} is saved before setting *fd* to raw mode; this value is returned.

::: versionchanged
3.12 The return value is now the original tty attributes, instead of `None`.
:::
::::

::::: function
setcbreak(fd, when=termios.TCSAFLUSH)

Change the mode of file descriptor *fd* to cbreak. If *when* is omitted, it defaults to `termios.TCSAFLUSH`{.interpreted-text role="const"}, and is passed to `termios.tcsetattr`{.interpreted-text role="func"}. The return value of `termios.tcgetattr`{.interpreted-text role="func"} is saved before setting *fd* to cbreak mode; this value is returned.

This clears the `ECHO` and `ICANON` local mode flags as well as setting the minimum input to 1 byte with no delay.

::: versionchanged
3.12 The return value is now the original tty attributes, instead of `None`.
:::

::: versionchanged
3.12.2 The `ICRNL` flag is no longer cleared. This restores the behavior of Python 3.11 and earlier as well as matching what Linux, macOS, & BSDs describe in their `stty(1)` man pages regarding cbreak mode.
:::
:::::

::: seealso

Module `termios`{.interpreted-text role="mod"}

:   Low-level terminal control interface.
:::
