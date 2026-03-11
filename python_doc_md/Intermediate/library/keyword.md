# `!keyword`{.interpreted-text role="mod"} \-\-- Testing for Python keywords

::: {.module synopsis="Test whether a string is a keyword in Python."}
keyword
:::

**Source code:** `Lib/keyword.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

This module allows a Python program to determine if a string is a `keyword <keywords>`{.interpreted-text role="ref"} or `soft keyword <soft-keywords>`{.interpreted-text role="ref"}.

::: function
iskeyword(s)

Return `True` if *s* is a Python `keyword <keywords>`{.interpreted-text role="ref"}.
:::

::: data
kwlist

Sequence containing all the `keywords <keywords>`{.interpreted-text role="ref"} defined for the interpreter. If any keywords are defined to only be active when particular `__future__`{.interpreted-text role="mod"} statements are in effect, these will be included as well.
:::

:::: function
issoftkeyword(s)

Return `True` if *s* is a Python `soft keyword <soft-keywords>`{.interpreted-text role="ref"}.

::: versionadded
3.9
:::
::::

:::: data
softkwlist

Sequence containing all the `soft keywords <soft-keywords>`{.interpreted-text role="ref"} defined for the interpreter. If any soft keywords are defined to only be active when particular `__future__`{.interpreted-text role="mod"} statements are in effect, these will be included as well.

::: versionadded
3.9
:::
::::
