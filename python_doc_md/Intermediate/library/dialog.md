# Tkinter Dialogs

## `!tkinter.simpledialog`{.interpreted-text role="mod"} \-\-- Standard Tkinter input dialogs

::: {.module synopsis="Simple dialog windows"}
tkinter.simpledialog
:::

**Source code:** `Lib/tkinter/simpledialog.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

The `!tkinter.simpledialog`{.interpreted-text role="mod"} module contains convenience classes and functions for creating simple modal dialogs to get a value from the user.

::: function
askfloat(title, prompt, **kw) askinteger(title, prompt,**kw) askstring(title, prompt, \*\*kw)

The above three functions provide dialogs that prompt the user to enter a value of the desired type.
:::

::::: {.Dialog(parent, .title=None)}
The base class for custom dialogs.

::: method
body(master)

Override to construct the dialog\'s interface and return the widget that should have initial focus.
:::

::: method
buttonbox()

Default behaviour adds OK and Cancel buttons. Override for custom button layouts.
:::
:::::

## `!tkinter.filedialog`{.interpreted-text role="mod"} \-\-- File selection dialogs

::: {.module synopsis="Dialog classes for file selection"}
tkinter.filedialog
:::

**Source code:** `Lib/tkinter/filedialog.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

The `!tkinter.filedialog`{.interpreted-text role="mod"} module provides classes and factory functions for creating file/directory selection windows.

### Native Load/Save Dialogs

The following classes and functions provide file dialog windows that combine a native look-and-feel with configuration options to customize behaviour. The following keyword arguments are applicable to the classes and functions listed below:

> | *parent* - the window to place the dialog on top of
>
> | *title* - the title of the window
>
> | *initialdir* - the directory that the dialog starts in
>
> | *initialfile* - the file selected upon opening of the dialog
>
> | *filetypes* - a sequence of (label, pattern) tuples, \'\*\' wildcard is allowed
>
> | *defaultextension* - default extension to append to file (save dialogs)
>
> | *multiple* - when true, selection of multiple items is allowed

**Static factory functions**

The below functions when called create a modal, native look-and-feel dialog, wait for the user\'s selection, then return the selected value(s) or `None` to the caller.

::: function
askopenfile(mode=\"r\", **options) askopenfiles(mode=\"r\",**options)

The above two functions create an `Open`{.interpreted-text role="class"} dialog and return the opened file object(s) in read-only mode.
:::

::: function
asksaveasfile(mode=\"w\", \*\*options)

Create a `SaveAs`{.interpreted-text role="class"} dialog and return a file object opened in write-only mode.
:::

::: function
askopenfilename(**options) askopenfilenames(**options)

The above two functions create an `Open`{.interpreted-text role="class"} dialog and return the selected filename(s) that correspond to existing file(s).
:::

::: function
asksaveasfilename(\*\*options)

Create a `SaveAs`{.interpreted-text role="class"} dialog and return the selected filename.
:::

::: function
askdirectory(\*\*options)

| Prompt user to select a directory.
| Additional keyword option:
|  \*mustexist\* - determines if selection must be an existing directory.
:::

::: {.Open(master=None, .**options) .SaveAs(master=None, .**options)}
The above two classes provide native dialog windows for saving and loading files.
:::

**Convenience classes**

The below classes are used for creating file/directory windows from scratch. These do not emulate the native look-and-feel of the platform.

::: {.Directory(master=None, .**options)}
Create a dialog prompting the user to select a directory.
:::

:::: note
::: title
Note
:::

The *FileDialog* class should be subclassed for custom event handling and behaviour.
::::

:::::::::::::::: {.FileDialog(master, .title=None)}
Create a basic file selection dialog.

::: method
cancel_command(event=None)

Trigger the termination of the dialog window.
:::

::: method
dirs_double_event(event)

Event handler for double-click event on directory.
:::

::: method
dirs_select_event(event)

Event handler for click event on directory.
:::

::: method
files_double_event(event)

Event handler for double-click event on file.
:::

::: method
files_select_event(event)

Event handler for single-click event on file.
:::

::: method
filter_command(event=None)

Filter the files by directory.
:::

::: method
get_filter()

Retrieve the file filter currently in use.
:::

::: method
get_selection()

Retrieve the currently selected item.
:::

::: method
go(dir_or_file=os.curdir, pattern=\"\*\", default=\"\", key=None)

Render dialog and start event loop.
:::

::: method
ok_event(event)

Exit dialog returning current selection.
:::

::: method
quit(how=None)

Exit dialog returning filename, if any.
:::

::: method
set_filter(dir, pat)

Set the file filter.
:::

::: method
set_selection(file)

Update the current file selection to *file*.
:::
::::::::::::::::

:::: {.LoadFileDialog(master, .title=None)}
A subclass of FileDialog that creates a dialog window for selecting an existing file.

::: method
ok_command()

Test that a file is provided and that the selection indicates an already existing file.
:::
::::

:::: {.SaveFileDialog(master, .title=None)}
A subclass of FileDialog that creates a dialog window for selecting a destination file.

::: method
ok_command()

Test whether or not the selection points to a valid file that is not a directory. Confirmation is required if an already existing file is selected.
:::
::::

## `!tkinter.commondialog`{.interpreted-text role="mod"} \-\-- Dialog window templates

::: {.module synopsis="Tkinter base class for dialogs"}
tkinter.commondialog
:::

**Source code:** `Lib/tkinter/commondialog.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

The `!tkinter.commondialog`{.interpreted-text role="mod"} module provides the `Dialog`{.interpreted-text role="class"} class that is the base class for dialogs defined in other supporting modules.

:::: {.Dialog(master=None, .**options)}
::: method
show(\*\*options)

Render the Dialog window.
:::
::::

::: seealso
Modules `tkinter.messagebox`{.interpreted-text role="mod"}, `tut-files`{.interpreted-text role="ref"}
:::
