# `!curses.ascii`{.interpreted-text role="mod"} \-\-- Utilities for ASCII characters

::: {.module synopsis="Constants and set-membership functions for ASCII characters."}
curses.ascii
:::

**Source code:** `Lib/curses/ascii.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

The `!curses.ascii`{.interpreted-text role="mod"} module supplies name constants for ASCII characters and functions to test membership in various ASCII character classes. The constants supplied are names for control characters as follows:

+---------------+-----------------------------------------------------------------------+
| Name          | Meaning                                                               |
+===============+=======================================================================+
| ::: data      |                                                                       |
| NUL           |                                                                       |
| :::           |                                                                       |
+---------------+-----------------------------------------------------------------------+
| ::: data      | Start of heading, console interrupt                                   |
| SOH           |                                                                       |
| :::           |                                                                       |
+---------------+-----------------------------------------------------------------------+
| ::: data      | Start of text                                                         |
| STX           |                                                                       |
| :::           |                                                                       |
+---------------+-----------------------------------------------------------------------+
| ::: data      | End of text                                                           |
| ETX           |                                                                       |
| :::           |                                                                       |
+---------------+-----------------------------------------------------------------------+
| ::: data      | End of transmission                                                   |
| EOT           |                                                                       |
| :::           |                                                                       |
+---------------+-----------------------------------------------------------------------+
| ::: data      | Enquiry, goes with `ACK`{.interpreted-text role="const"} flow control |
| ENQ           |                                                                       |
| :::           |                                                                       |
+---------------+-----------------------------------------------------------------------+
| ::: data      | Acknowledgement                                                       |
| ACK           |                                                                       |
| :::           |                                                                       |
+---------------+-----------------------------------------------------------------------+
| ::: data      | Bell                                                                  |
| BEL           |                                                                       |
| :::           |                                                                       |
+---------------+-----------------------------------------------------------------------+
| ::: data      | Backspace                                                             |
| BS            |                                                                       |
| :::           |                                                                       |
+---------------+-----------------------------------------------------------------------+
| ::: data      | Tab                                                                   |
| TAB           |                                                                       |
| :::           |                                                                       |
+---------------+-----------------------------------------------------------------------+
| ::: data      | Alias for `TAB`{.interpreted-text role="const"}: \"Horizontal tab\"   |
| HT            |                                                                       |
| :::           |                                                                       |
+---------------+-----------------------------------------------------------------------+
| ::: data      | Line feed                                                             |
| LF            |                                                                       |
| :::           |                                                                       |
+---------------+-----------------------------------------------------------------------+
| ::: data      | Alias for `LF`{.interpreted-text role="const"}: \"New line\"          |
| NL            |                                                                       |
| :::           |                                                                       |
+---------------+-----------------------------------------------------------------------+
| ::: data      | Vertical tab                                                          |
| VT            |                                                                       |
| :::           |                                                                       |
+---------------+-----------------------------------------------------------------------+
| ::: data      | Form feed                                                             |
| FF            |                                                                       |
| :::           |                                                                       |
+---------------+-----------------------------------------------------------------------+
| ::: data      | Carriage return                                                       |
| CR            |                                                                       |
| :::           |                                                                       |
+---------------+-----------------------------------------------------------------------+
| ::: data      | Shift-out, begin alternate character set                              |
| SO            |                                                                       |
| :::           |                                                                       |
+---------------+-----------------------------------------------------------------------+
| ::: data      | Shift-in, resume default character set                                |
| SI            |                                                                       |
| :::           |                                                                       |
+---------------+-----------------------------------------------------------------------+
| ::: data      | Data-link escape                                                      |
| DLE           |                                                                       |
| :::           |                                                                       |
+---------------+-----------------------------------------------------------------------+
| ::: data      | XON, for flow control                                                 |
| DC1           |                                                                       |
| :::           |                                                                       |
+---------------+-----------------------------------------------------------------------+
| ::: data      | Device control 2, block-mode flow control                             |
| DC2           |                                                                       |
| :::           |                                                                       |
+---------------+-----------------------------------------------------------------------+
| ::: data      | XOFF, for flow control                                                |
| DC3           |                                                                       |
| :::           |                                                                       |
+---------------+-----------------------------------------------------------------------+
| ::: data      | Device control 4                                                      |
| DC4           |                                                                       |
| :::           |                                                                       |
+---------------+-----------------------------------------------------------------------+
| ::: data      | Negative acknowledgement                                              |
| NAK           |                                                                       |
| :::           |                                                                       |
+---------------+-----------------------------------------------------------------------+
| ::: data      | Synchronous idle                                                      |
| SYN           |                                                                       |
| :::           |                                                                       |
+---------------+-----------------------------------------------------------------------+
| ::: data      | End transmission block                                                |
| ETB           |                                                                       |
| :::           |                                                                       |
+---------------+-----------------------------------------------------------------------+
| ::: data      | Cancel                                                                |
| CAN           |                                                                       |
| :::           |                                                                       |
+---------------+-----------------------------------------------------------------------+
| ::: data      | End of medium                                                         |
| EM            |                                                                       |
| :::           |                                                                       |
+---------------+-----------------------------------------------------------------------+
| ::: data      | Substitute                                                            |
| SUB           |                                                                       |
| :::           |                                                                       |
+---------------+-----------------------------------------------------------------------+
| ::: data      | Escape                                                                |
| ESC           |                                                                       |
| :::           |                                                                       |
+---------------+-----------------------------------------------------------------------+
| ::: data      | File separator                                                        |
| FS            |                                                                       |
| :::           |                                                                       |
+---------------+-----------------------------------------------------------------------+
| ::: data      | Group separator                                                       |
| GS            |                                                                       |
| :::           |                                                                       |
+---------------+-----------------------------------------------------------------------+
| ::: data      | Record separator, block-mode terminator                               |
| RS            |                                                                       |
| :::           |                                                                       |
+---------------+-----------------------------------------------------------------------+
| ::: data      | Unit separator                                                        |
| US            |                                                                       |
| :::           |                                                                       |
+---------------+-----------------------------------------------------------------------+
| ::: data      | Space                                                                 |
| SP            |                                                                       |
| :::           |                                                                       |
+---------------+-----------------------------------------------------------------------+
| ::: data      | Delete                                                                |
| DEL           |                                                                       |
| :::           |                                                                       |
+---------------+-----------------------------------------------------------------------+

Note that many of these have little practical significance in modern usage. The mnemonics derive from teleprinter conventions that predate digital computers.

The module supplies the following functions, patterned on those in the standard C library:

::: function
isalnum(c)

Checks for an ASCII alphanumeric character; it is equivalent to `isalpha(c) or isdigit(c)`.
:::

::: function
isalpha(c)

Checks for an ASCII alphabetic character; it is equivalent to `isupper(c) or islower(c)`.
:::

::: function
isascii(c)

Checks for a character value that fits in the 7-bit ASCII set.
:::

::: function
isblank(c)

Checks for an ASCII whitespace character; space or horizontal tab.
:::

::: function
iscntrl(c)

Checks for an ASCII control character (in the range 0x00 to 0x1f or 0x7f).
:::

::: function
isdigit(c)

Checks for an ASCII decimal digit, `'0'` through `'9'`. This is equivalent to `c in string.digits`.
:::

::: function
isgraph(c)

Checks for ASCII any printable character except space.
:::

::: function
islower(c)

Checks for an ASCII lower-case character.
:::

::: function
isprint(c)

Checks for any ASCII printable character including space.
:::

::: function
ispunct(c)

Checks for any printable ASCII character which is not a space or an alphanumeric character.
:::

::: function
isspace(c)

Checks for ASCII white-space characters; space, line feed, carriage return, form feed, horizontal tab, vertical tab.
:::

::: function
isupper(c)

Checks for an ASCII uppercase letter.
:::

::: function
isxdigit(c)

Checks for an ASCII hexadecimal digit. This is equivalent to `c in string.hexdigits`.
:::

::: function
isctrl(c)

Checks for an ASCII control character (ordinal values 0 to 31).
:::

::: function
ismeta(c)

Checks for a non-ASCII character (ordinal values 0x80 and above).
:::

These functions accept either integers or single-character strings; when the argument is a string, it is first converted using the built-in function `ord`{.interpreted-text role="func"}.

Note that all these functions check ordinal bit values derived from the character of the string you pass in; they do not actually know anything about the host machine\'s character encoding.

The following two functions take either a single-character string or integer byte value; they return a value of the same type.

::: function
ascii(c)

Return the ASCII value corresponding to the low 7 bits of *c*.
:::

::: function
ctrl(c)

Return the control character corresponding to the given character (the character bit value is bitwise-anded with 0x1f).
:::

::: function
alt(c)

Return the 8-bit character corresponding to the given ASCII character (the character bit value is bitwise-ored with 0x80).
:::

The following function takes either a single-character string or integer value; it returns a string.

::: index
single: \^ (caret); in curses module single: ! (exclamation); in curses module
:::

::: function
unctrl(c)

Return a string representation of the ASCII character *c*. If *c* is printable, this string is the character itself. If the character is a control character (0x00\--0x1f) the string consists of a caret (`'^'`) followed by the corresponding uppercase letter. If the character is an ASCII delete (0x7f) the string is `'^?'`. If the character has its meta bit (0x80) set, the meta bit is stripped, the preceding rules applied, and `'!'` prepended to the result.
:::

::: data
controlnames

A 33-element string array that contains the ASCII mnemonics for the thirty-two ASCII control characters from 0 (NUL) to 0x1f (US), in order, plus the mnemonic `SP` for the space character.
:::
