# `!tkinter.colorchooser`{.interpreted-text role="mod"} \-\-- Color choosing dialog

::: {.module synopsis="Color choosing dialog"}
tkinter.colorchooser
:::

**Source code:** `Lib/tkinter/colorchooser.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

The `!tkinter.colorchooser`{.interpreted-text role="mod"} module provides the `Chooser`{.interpreted-text role="class"} class as an interface to the native color picker dialog. `Chooser` implements a modal color choosing dialog window. The `Chooser` class inherits from the `~tkinter.commondialog.Dialog`{.interpreted-text role="class"} class.

:::: {.Chooser(master=None, .**options)}
::: function
askcolor(color=None, \*\*options)

Create a color choosing dialog. A call to this method will show the window, wait for the user to make a selection, and return the selected color (or `None`) to the caller.
:::
::::

::: seealso

Module `tkinter.commondialog`{.interpreted-text role="mod"}

:   Tkinter standard dialog module
:::
