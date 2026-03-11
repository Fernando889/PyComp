# `!html`{.interpreted-text role="mod"} \-\-- HyperText Markup Language support

::: {.module synopsis="Helpers for manipulating HTML."}
html
:::

**Source code:** `Lib/html/__init__.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

This module defines utilities to manipulate HTML.

:::: function
escape(s, quote=True)

Convert the characters `&`, `<` and `>` in string *s* to HTML-safe sequences. Use this if you need to display text that might contain such characters in HTML. If the optional flag *quote* is true (the default), the characters (`"`) and (`'`) are also translated; this helps for inclusion in an HTML attribute value delimited by quotes, as in `<a href="...">`. If *quote* is set to false, the characters (`"`) and (`'`) are not translated.

::: versionadded
3.2
:::
::::

:::: function
unescape(s)

Convert all named and numeric character references (e.g. `&gt;`, `&#62;`, `&#x3e;`) in the string *s* to the corresponding Unicode characters. This function uses the rules defined by the HTML 5 standard for both valid and invalid character references, and the `list of
HTML 5 named character references <html.entities.html5>`{.interpreted-text role="data"}.

::: versionadded
3.4
:::
::::

------------------------------------------------------------------------

Submodules in the `html` package are:

- `html.parser`{.interpreted-text role="mod"} \-- HTML/XHTML parser with lenient parsing mode
- `html.entities`{.interpreted-text role="mod"} \-- HTML entity definitions
