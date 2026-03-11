# `!tkinter.scrolledtext`{.interpreted-text role="mod"} \-\-- Scrolled Text Widget

::: {.module synopsis="Text widget with a vertical scroll bar."}
tkinter.scrolledtext
:::

**Source code:** `Lib/tkinter/scrolledtext.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

The `!tkinter.scrolledtext`{.interpreted-text role="mod"} module provides a class of the same name which implements a basic text widget which has a vertical scroll bar configured to do the \"right thing.\" Using the `ScrolledText`{.interpreted-text role="class"} class is a lot easier than setting up a text widget and scroll bar directly.

The text widget and scrollbar are packed together in a `Frame`{.interpreted-text role="class"}, and the methods of the `Grid`{.interpreted-text role="class"} and `Pack`{.interpreted-text role="class"} geometry managers are acquired from the `Frame`{.interpreted-text role="class"} object. This allows the `ScrolledText`{.interpreted-text role="class"} widget to be used directly to achieve most normal geometry management behavior.

Should more specific control be necessary, the following attributes are available:

::::: {.ScrolledText(master=None, .**kw)}
::: attribute
frame

The frame which surrounds the text and scroll bar widgets.
:::

::: attribute
vbar

The scroll bar widget.
:::
:::::
