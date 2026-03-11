# `!tkinter.messagebox`{.interpreted-text role="mod"} \-\-- Tkinter message prompts

::: {.module synopsis="Various types of alert dialogs"}
tkinter.messagebox
:::

**Source code:** `Lib/tkinter/messagebox.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

The `!tkinter.messagebox`{.interpreted-text role="mod"} module provides a template base class as well as a variety of convenience methods for commonly used configurations. The message boxes are modal and will return a subset of (`True`, `False`, `None`, `OK`{.interpreted-text role="data"}, `CANCEL`{.interpreted-text role="data"}, `YES`{.interpreted-text role="data"}, `NO`{.interpreted-text role="data"}) based on the user\'s selection. Common message box styles and layouts include but are not limited to:

![](tk_msg.png)

:::: {.Message(master=None, .**options)}
Create a message window with an application-specified message, an icon and a set of buttons. Each of the buttons in the message window is identified by a unique symbolic name (see the *type* options).

The following options are supported:

> 
>
> *command*
>
> :   Specifies the function to invoke when the user closes the dialog. The name of the button clicked by the user to close the dialog is passed as argument. This is only available on macOS.
>
> *default*
>
> :   Gives the `symbolic name <messagebox-buttons>`{.interpreted-text role="ref"} of the default button for this message window (`OK`{.interpreted-text role="data"}, `CANCEL`{.interpreted-text role="data"}, and so on). If this option is not specified, the first button in the dialog will be made the default.
>
> *detail*
>
> :   Specifies an auxiliary message to the main message given by the *message* option. The message detail will be presented beneath the main message and, where supported by the OS, in a less emphasized font than the main message.
>
> *icon*
>
> :   Specifies an `icon <messagebox-icons>`{.interpreted-text role="ref"} to display. If this option is not specified, then the `INFO`{.interpreted-text role="data"} icon will be displayed.
>
> *message*
>
> :   Specifies the message to display in this message box. The default value is an empty string.
>
> *parent*
>
> :   Makes the specified window the logical parent of the message box. The message box is displayed on top of its parent window.
>
> *title*
>
> :   Specifies a string to display as the title of the message box. This option is ignored on macOS, where platform guidelines forbid the use of a title on this kind of dialog.
>
> *type*
>
> :   Arranges for a `predefined set of buttons <messagebox-types>`{.interpreted-text role="ref"} to be displayed.

::: method
show(\*\*options)

Display a message window and wait for the user to select one of the buttons. Then return the symbolic name of the selected button. Keyword arguments can override options specified in the constructor.
:::
::::

**Information message box**

::: function
showinfo(title=None, message=None, \*\*options)

Creates and displays an information message box with the specified title and message.
:::

**Warning message boxes**

::: function
showwarning(title=None, message=None, \*\*options)

Creates and displays a warning message box with the specified title and message.
:::

::: function
showerror(title=None, message=None, \*\*options)

Creates and displays an error message box with the specified title and message.
:::

**Question message boxes**

::: function
askquestion(title=None, message=None, *, type=YESNO,*\*options)

Ask a question. By default shows buttons `YES`{.interpreted-text role="data"} and `NO`{.interpreted-text role="data"}. Returns the symbolic name of the selected button.
:::

::: function
askokcancel(title=None, message=None, \*\*options)

Ask if operation should proceed. Shows buttons `OK`{.interpreted-text role="data"} and `CANCEL`{.interpreted-text role="data"}. Returns `True` if the answer is ok and `False` otherwise.
:::

::: function
askretrycancel(title=None, message=None, \*\*options)

Ask if operation should be retried. Shows buttons `RETRY`{.interpreted-text role="data"} and `CANCEL`{.interpreted-text role="data"}. Return `True` if the answer is yes and `False` otherwise.
:::

::: function
askyesno(title=None, message=None, \*\*options)

Ask a question. Shows buttons `YES`{.interpreted-text role="data"} and `NO`{.interpreted-text role="data"}. Returns `True` if the answer is yes and `False` otherwise.
:::

::: function
askyesnocancel(title=None, message=None, \*\*options)

Ask a question. Shows buttons `YES`{.interpreted-text role="data"}, `NO`{.interpreted-text role="data"} and `CANCEL`{.interpreted-text role="data"}. Return `True` if the answer is yes, `None` if cancelled, and `False` otherwise.
:::

::: {#messagebox-buttons}
Symbolic names of buttons:
:::

::: {.data value="'abort'"}
ABORT
:::

::: {.data value="'retry'"}
RETRY
:::

::: {.data value="'ignore'"}
IGNORE
:::

::: {.data value="'ok'"}
OK
:::

::: {.data value="'cancel'"}
CANCEL
:::

::: {.data value="'yes'"}
YES
:::

::: {.data value="'no'"}
NO
:::

::: {#messagebox-types}
Predefined sets of buttons:
:::

::: {.data value="'abortretryignore'"}
ABORTRETRYIGNORE

Displays three buttons whose symbolic names are `ABORT`{.interpreted-text role="data"}, `RETRY`{.interpreted-text role="data"} and `IGNORE`{.interpreted-text role="data"}.
:::

::: {.data value="'ok'" noindex=""}
OK

Displays one button whose symbolic name is `OK`{.interpreted-text role="data"}.
:::

::: {.data value="'okcancel'"}
OKCANCEL

Displays two buttons whose symbolic names are `OK`{.interpreted-text role="data"} and `CANCEL`{.interpreted-text role="data"}.
:::

::: {.data value="'retrycancel'"}
RETRYCANCEL

Displays two buttons whose symbolic names are `RETRY`{.interpreted-text role="data"} and `CANCEL`{.interpreted-text role="data"}.
:::

::: {.data value="'yesno'"}
YESNO

Displays two buttons whose symbolic names are `YES`{.interpreted-text role="data"} and `NO`{.interpreted-text role="data"}.
:::

::: {.data value="'yesnocancel'"}
YESNOCANCEL

Displays three buttons whose symbolic names are `YES`{.interpreted-text role="data"}, `NO`{.interpreted-text role="data"} and `CANCEL`{.interpreted-text role="data"}.
:::

::: {#messagebox-icons}
Icon images:
:::

::: {.data value="'error'"}
ERROR
:::

::: {.data value="'info'"}
INFO
:::

::: {.data value="'question'"}
QUESTION
:::

::: {.data value="'warning'"}
WARNING
:::
