# `!curses`{.interpreted-text role="mod"} \-\-- Terminal handling for character-cell displays

::: {.module synopsis="An interface to the curses library, providing portable
terminal handling."}
curses
:::

**Source code:** `Lib/curses`{.interpreted-text role="source"}

------------------------------------------------------------------------

The `!curses`{.interpreted-text role="mod"} module provides an interface to the curses library, the de-facto standard for portable advanced terminal handling.

While curses is most widely used in the Unix environment, versions are available for Windows, DOS, and possibly other systems as well. This extension module is designed to match the API of ncurses, an open-source curses library hosted on Linux and the BSD variants of Unix.

::: availability
not Android, not iOS, not WASI.

This module is not supported on `mobile platforms <mobile-availability>`{.interpreted-text role="ref"} or `WebAssembly platforms <wasm-availability>`{.interpreted-text role="ref"}.
:::

This is an `optional module`{.interpreted-text role="term"}. If it is missing from your copy of CPython, look for documentation from your distributor (that is, whoever provided Python to you). If you are the distributor, see `optional-module-requirements`{.interpreted-text role="ref"}.

::: availability
Unix.
:::

:::: note
::: title
Note
:::

Whenever the documentation mentions a *character* it can be specified as an integer, a one-character Unicode string or a one-byte byte string.

Whenever the documentation mentions a *character string* it can be specified as a Unicode string or a byte string.
::::

::: seealso

Module `curses.ascii`{.interpreted-text role="mod"}

:   Utilities for working with ASCII characters, regardless of your locale settings.

Module `curses.panel`{.interpreted-text role="mod"}

:   A panel stack extension that adds depth to curses windows.

Module `curses.textpad`{.interpreted-text role="mod"}

:   Editable text widget for curses supporting `Emacs`{.interpreted-text role="program"}-like bindings.

`curses-howto`{.interpreted-text role="ref"}

:   Tutorial material on using curses with Python, by Andrew Kuchling and Eric Raymond.
:::

## Functions {#curses-functions}

The module `!curses`{.interpreted-text role="mod"} defines the following exception:

::: exception
error

Exception raised when a curses library function returns an error.
:::

:::: note
::: title
Note
:::

Whenever *x* or *y* arguments to a function or a method are optional, they default to the current cursor location. Whenever *attr* is optional, it defaults to `A_NORMAL`{.interpreted-text role="const"}.
::::

The module `!curses`{.interpreted-text role="mod"} defines the following functions:

:::: function
assume_default_colors(fg, bg, /)

Allow use of default values for colors on terminals supporting this feature. Use this to support transparency in your application.

- Assign terminal default foreground/background colors to color number `-1`. So `init_pair(x, COLOR_RED, -1)` will initialize pair *x* as red on default background and `init_pair(x, -1, COLOR_BLUE)` will initialize pair *x* as default foreground on blue.
- Change the definition of the color-pair `0` to `(fg, bg)`.

::: versionadded
3.14
:::
::::

::: function
baudrate()

Return the output speed of the terminal in bits per second. On software terminal emulators it will have a fixed high value. Included for historical reasons; in former times, it was used to write output loops for time delays and occasionally to change interfaces depending on the line speed.
:::

::: function
beep()

Emit a short attention sound.
:::

::: function
can_change_color()

Return `True` or `False`, depending on whether the programmer can change the colors displayed by the terminal.
:::

::: function
cbreak()

Enter cbreak mode. In cbreak mode (sometimes called \"rare\" mode) normal tty line buffering is turned off and characters are available to be read one by one. However, unlike raw mode, special characters (interrupt, quit, suspend, and flow control) retain their effects on the tty driver and calling program. Calling first `raw`{.interpreted-text role="func"} then `cbreak`{.interpreted-text role="func"} leaves the terminal in cbreak mode.
:::

::: function
color_content(color_number)

Return the intensity of the red, green, and blue (RGB) components in the color *color_number*, which must be between `0` and `COLORS - 1`. Return a 3-tuple, containing the R,G,B values for the given color, which will be between `0` (no component) and `1000` (maximum amount of component).
:::

::: function
color_pair(pair_number)

Return the attribute value for displaying text in the specified color pair. Only the first 256 color pairs are supported. This attribute value can be combined with `A_STANDOUT`{.interpreted-text role="const"}, `A_REVERSE`{.interpreted-text role="const"}, and the other `!A_\*`{.interpreted-text role="const"} attributes. `pair_number`{.interpreted-text role="func"} is the counterpart to this function.
:::

::: function
curs_set(visibility)

Set the cursor state. *visibility* can be set to `0`, `1`, or `2`, for invisible, normal, or very visible. If the terminal supports the visibility requested, return the previous cursor state; otherwise raise an exception. On many terminals, the \"visible\" mode is an underline cursor and the \"very visible\" mode is a block cursor.
:::

::: function
def_prog_mode()

Save the current terminal mode as the \"program\" mode, the mode when the running program is using curses. (Its counterpart is the \"shell\" mode, for when the program is not in curses.) Subsequent calls to `reset_prog_mode`{.interpreted-text role="func"} will restore this mode.
:::

::: function
def_shell_mode()

Save the current terminal mode as the \"shell\" mode, the mode when the running program is not using curses. (Its counterpart is the \"program\" mode, when the program is using curses capabilities.) Subsequent calls to `reset_shell_mode`{.interpreted-text role="func"} will restore this mode.
:::

::: function
delay_output(ms)

Insert an *ms* millisecond pause in output.
:::

::: function
doupdate()

Update the physical screen. The curses library keeps two data structures, one representing the current physical screen contents and a virtual screen representing the desired next state. The `doupdate`{.interpreted-text role="func"} ground updates the physical screen to match the virtual screen.

The virtual screen may be updated by a `~window.noutrefresh`{.interpreted-text role="meth"} call after write operations such as `~window.addstr`{.interpreted-text role="meth"} have been performed on a window. The normal `~window.refresh`{.interpreted-text role="meth"} call is simply `!noutrefresh`{.interpreted-text role="meth"} followed by `!doupdate`{.interpreted-text role="func"}; if you have to update multiple windows, you can speed performance and perhaps reduce screen flicker by issuing `!noutrefresh`{.interpreted-text role="meth"} calls on all windows, followed by a single `!doupdate`{.interpreted-text role="func"}.
:::

::: function
echo()

Enter echo mode. In echo mode, each character input is echoed to the screen as it is entered.
:::

::: function
endwin()

De-initialize the library, and return terminal to normal status.
:::

::: function
erasechar()

Return the user\'s current erase character as a one-byte bytes object. Under Unix operating systems this is a property of the controlling tty of the curses program, and is not set by the curses library itself.
:::

::: function
filter()

The `.filter`{.interpreted-text role="func"} routine, if used, must be called before `initscr`{.interpreted-text role="func"} is called. The effect is that, during those calls, `LINES`{.interpreted-text role="envvar"} is set to `1`; the capabilities `clear`, `cup`, `cud`, `cud1`, `cuu1`, `cuu`, `vpa` are disabled; and the `home` string is set to the value of `cr`. The effect is that the cursor is confined to the current line, and so are screen updates. This may be used for enabling character-at-a-time line editing without touching the rest of the screen.
:::

::: function
flash()

Flash the screen. That is, change it to reverse-video and then change it back in a short interval. Some people prefer such as \'visible bell\' to the audible attention signal produced by `beep`{.interpreted-text role="func"}.
:::

::: function
flushinp()

Flush all input buffers. This throws away any typeahead that has been typed by the user and has not yet been processed by the program.
:::

:::: function
getmouse()

After `~window.getch`{.interpreted-text role="meth"} returns `KEY_MOUSE`{.interpreted-text role="const"} to signal a mouse event, this method should be called to retrieve the queued mouse event, represented as a 5-tuple `(id, x, y, z, bstate)`. *id* is an ID value used to distinguish multiple devices, and *x*, *y*, *z* are the event\'s coordinates. (*z* is currently unused.) *bstate* is an integer value whose bits will be set to indicate the type of event, and will be the bitwise OR of one or more of the following constants, where *n* is the button number from 1 to 5: `BUTTONn_PRESSED`{.interpreted-text role="const"}, `BUTTONn_RELEASED`{.interpreted-text role="const"}, `BUTTONn_CLICKED`{.interpreted-text role="const"}, `BUTTONn_DOUBLE_CLICKED`{.interpreted-text role="const"}, `BUTTONn_TRIPLE_CLICKED`{.interpreted-text role="const"}, `BUTTON_SHIFT`{.interpreted-text role="const"}, `BUTTON_CTRL`{.interpreted-text role="const"}, `BUTTON_ALT`{.interpreted-text role="const"}.

::: versionchanged
3.10 The `BUTTON5_*` constants are now exposed if they are provided by the underlying curses library.
:::
::::

::: function
getsyx()

Return the current coordinates of the virtual screen cursor as a tuple `(y, x)`. If `leaveok <window.leaveok>`{.interpreted-text role="meth"} is currently `True`, then return `(-1, -1)`.
:::

::: function
getwin(file)

Read window related data stored in the file by an earlier `window.putwin`{.interpreted-text role="func"} call. The routine then creates and initializes a new window using that data, returning the new window object.
:::

::: function
has_colors()

Return `True` if the terminal can display colors; otherwise, return `False`.
:::

:::: function
has_extended_color_support()

Return `True` if the module supports extended colors; otherwise, return `False`. Extended color support allows more than 256 color pairs for terminals that support more than 16 colors (e.g. xterm-256color).

Extended color support requires ncurses version 6.1 or later.

::: versionadded
3.10
:::
::::

::: function
has_ic()

Return `True` if the terminal has insert- and delete-character capabilities. This function is included for historical reasons only, as all modern software terminal emulators have such capabilities.
:::

::: function
has_il()

Return `True` if the terminal has insert- and delete-line capabilities, or can simulate them using scrolling regions. This function is included for historical reasons only, as all modern software terminal emulators have such capabilities.
:::

::: function
has_key(ch)

Take a key value *ch*, and return `True` if the current terminal type recognizes a key with that value.
:::

::: function
halfdelay(tenths)

Used for half-delay mode, which is similar to cbreak mode in that characters typed by the user are immediately available to the program. However, after blocking for *tenths* tenths of seconds, raise an exception if nothing has been typed. The value of *tenths* must be a number between `1` and `255`. Use `nocbreak`{.interpreted-text role="func"} to leave half-delay mode.
:::

::: function
init_color(color_number, r, g, b)

Change the definition of a color, taking the number of the color to be changed followed by three RGB values (for the amounts of red, green, and blue components). The value of *color_number* must be between `0` and `COLORS - 1`. Each of *r*, *g*, *b*, must be a value between `0` and `1000`. When `init_color`{.interpreted-text role="func"} is used, all occurrences of that color on the screen immediately change to the new definition. This function is a no-op on most terminals; it is active only if `can_change_color`{.interpreted-text role="func"} returns `True`.
:::

::: function
init_pair(pair_number, fg, bg)

Change the definition of a color-pair. It takes three arguments: the number of the color-pair to be changed, the foreground color number, and the background color number. The value of *pair_number* must be between `1` and `COLOR_PAIRS - 1` (the `0` color pair can only be changed by `use_default_colors`{.interpreted-text role="func"} and `assume_default_colors`{.interpreted-text role="func"}). The value of *fg* and *bg* arguments must be between `0` and `COLORS - 1`, or, after calling `!use_default_colors`{.interpreted-text role="func"} or `!assume_default_colors`{.interpreted-text role="func"}, `-1`. If the color-pair was previously initialized, the screen is refreshed and all occurrences of that color-pair are changed to the new definition.
:::

::::: function
initscr()

Initialize the library. Return a `window <curses-window-objects>`{.interpreted-text role="ref"} object which represents the whole screen.

:::: note
::: title
Note
:::

If there is an error opening the terminal, the underlying curses library may cause the interpreter to exit.
::::
:::::

::: function
is_term_resized(nlines, ncols)

Return `True` if `resize_term`{.interpreted-text role="func"} would modify the window structure, `False` otherwise.
:::

::: function
isendwin()

Return `True` if `endwin`{.interpreted-text role="func"} has been called (that is, the curses library has been deinitialized).
:::

::: function
keyname(k)

Return the name of the key numbered *k* as a bytes object. The name of a key generating printable ASCII character is the key\'s character. The name of a control-key combination is a two-byte bytes object consisting of a caret (`b'^'`) followed by the corresponding printable ASCII character. The name of an alt-key combination (128\--255) is a bytes object consisting of the prefix `b'M-'` followed by the name of the corresponding ASCII character.
:::

::: function
killchar()

Return the user\'s current line kill character as a one-byte bytes object. Under Unix operating systems this is a property of the controlling tty of the curses program, and is not set by the curses library itself.
:::

::: function
longname()

Return a bytes object containing the terminfo long name field describing the current terminal. The maximum length of a verbose description is 128 characters. It is defined only after the call to `initscr`{.interpreted-text role="func"}.
:::

::: function
meta(flag)

If *flag* is `True`, allow 8-bit characters to be input. If *flag* is `False`, allow only 7-bit chars.
:::

::: function
mouseinterval(interval)

Set the maximum time in milliseconds that can elapse between press and release events in order for them to be recognized as a click, and return the previous interval value. The default value is 200 milliseconds, or one fifth of a second.
:::

::: function
mousemask(mousemask)

Set the mouse events to be reported, and return a tuple `(availmask, oldmask)`. *availmask* indicates which of the specified mouse events can be reported; on complete failure it returns `0`. *oldmask* is the previous value of the given window\'s mouse event mask. If this function is never called, no mouse events are ever reported.
:::

::: function
napms(ms)

Sleep for *ms* milliseconds.
:::

::: function
newpad(nlines, ncols)

Create and return a pointer to a new pad data structure with the given number of lines and columns. Return a pad as a window object.

A pad is like a window, except that it is not restricted by the screen size, and is not necessarily associated with a particular part of the screen. Pads can be used when a large window is needed, and only a part of the window will be on the screen at one time. Automatic refreshes of pads (such as from scrolling or echoing of input) do not occur. The `~window.refresh`{.interpreted-text role="meth"} and `~window.noutrefresh`{.interpreted-text role="meth"} methods of a pad require 6 arguments to specify the part of the pad to be displayed and the location on the screen to be used for the display. The arguments are *pminrow*, *pmincol*, *sminrow*, *smincol*, *smaxrow*, *smaxcol*; the *p* arguments refer to the upper left corner of the pad region to be displayed and the *s* arguments define a clipping box on the screen within which the pad region is to be displayed.
:::

::: function
newwin(nlines, ncols) newwin(nlines, ncols, begin_y, begin_x)

Return a new `window <curses-window-objects>`{.interpreted-text role="ref"}, whose left-upper corner is at `(begin_y, begin_x)`, and whose height/width is *nlines*/\*ncols\*.

By default, the window will extend from the specified position to the lower right corner of the screen.
:::

::: function
nl()

Enter newline mode. This mode translates the return key into newline on input, and translates newline into return and line-feed on output. Newline mode is initially on.
:::

::: function
nocbreak()

Leave cbreak mode. Return to normal \"cooked\" mode with line buffering.
:::

::: function
noecho()

Leave echo mode. Echoing of input characters is turned off.
:::

::: function
nonl()

Leave newline mode. Disable translation of return into newline on input, and disable low-level translation of newline into newline/return on output (but this does not change the behavior of `addch('\n')`, which always does the equivalent of return and line feed on the virtual screen). With translation off, curses can sometimes speed up vertical motion a little; also, it will be able to detect the return key on input.
:::

::: function
noqiflush()

When the `!noqiflush`{.interpreted-text role="func"} routine is used, normal flush of input and output queues associated with the `INTR`, `QUIT` and `SUSP` characters will not be done. You may want to call `!noqiflush`{.interpreted-text role="func"} in a signal handler if you want output to continue as though the interrupt had not occurred, after the handler exits.
:::

::: function
noraw()

Leave raw mode. Return to normal \"cooked\" mode with line buffering.
:::

::: function
pair_content(pair_number)

Return a tuple `(fg, bg)` containing the colors for the requested color pair. The value of *pair_number* must be between `0` and `COLOR_PAIRS - 1`.
:::

::: function
pair_number(attr)

Return the number of the color-pair set by the attribute value *attr*. `color_pair`{.interpreted-text role="func"} is the counterpart to this function.
:::

::: function
putp(str)

Equivalent to `tputs(str, 1, putchar)`; emit the value of a specified terminfo capability for the current terminal. Note that the output of `putp`{.interpreted-text role="func"} always goes to standard output.
:::

::: function
qiflush(\[flag\])

If *flag* is `False`, the effect is the same as calling `noqiflush`{.interpreted-text role="func"}. If *flag* is `True`, or no argument is provided, the queues will be flushed when these control characters are read.
:::

::: function
raw()

Enter raw mode. In raw mode, normal line buffering and processing of interrupt, quit, suspend, and flow control keys are turned off; characters are presented to curses input functions one by one.
:::

::: function
reset_prog_mode()

Restore the terminal to \"program\" mode, as previously saved by `def_prog_mode`{.interpreted-text role="func"}.
:::

::: function
reset_shell_mode()

Restore the terminal to \"shell\" mode, as previously saved by `def_shell_mode`{.interpreted-text role="func"}.
:::

::: function
resetty()

Restore the state of the terminal modes to what it was at the last call to `savetty`{.interpreted-text role="func"}.
:::

::: function
resize_term(nlines, ncols)

Backend function used by `resizeterm`{.interpreted-text role="func"}, performing most of the work; when resizing the windows, `resize_term`{.interpreted-text role="func"} blank-fills the areas that are extended. The calling application should fill in these areas with appropriate data. The `!resize_term`{.interpreted-text role="func"} function attempts to resize all windows. However, due to the calling convention of pads, it is not possible to resize these without additional interaction with the application.
:::

::: function
resizeterm(nlines, ncols)

Resize the standard and current windows to the specified dimensions, and adjusts other bookkeeping data used by the curses library that record the window dimensions (in particular the SIGWINCH handler).
:::

::: function
savetty()

Save the current state of the terminal modes in a buffer, usable by `resetty`{.interpreted-text role="func"}.
:::

:::: function
get_escdelay()

Retrieves the value set by `set_escdelay`{.interpreted-text role="func"}.

::: versionadded
3.9
:::
::::

:::: function
set_escdelay(ms)

Sets the number of milliseconds to wait after reading an escape character, to distinguish between an individual escape character entered on the keyboard from escape sequences sent by cursor and function keys.

::: versionadded
3.9
:::
::::

:::: function
get_tabsize()

Retrieves the value set by `set_tabsize`{.interpreted-text role="func"}.

::: versionadded
3.9
:::
::::

:::: function
set_tabsize(size)

Sets the number of columns used by the curses library when converting a tab character to spaces as it adds the tab to a window.

::: versionadded
3.9
:::
::::

::: function
setsyx(y, x)

Set the virtual screen cursor to *y*, *x*. If *y* and *x* are both `-1`, then `leaveok <window.leaveok>`{.interpreted-text role="meth"} is set `True`.
:::

::: function
setupterm(term=None, fd=-1)

Initialize the terminal. *term* is a string giving the terminal name, or `None`; if omitted or `None`, the value of the `TERM`{.interpreted-text role="envvar"} environment variable will be used. *fd* is the file descriptor to which any initialization sequences will be sent; if not supplied or `-1`, the file descriptor for `sys.stdout` will be used.
:::

::: function
start_color()

Must be called if the programmer wants to use colors, and before any other color manipulation routine is called. It is good practice to call this routine right after `initscr`{.interpreted-text role="func"}.

`start_color`{.interpreted-text role="func"} initializes eight basic colors (black, red, green, yellow, blue, magenta, cyan, and white), and two global variables in the `!curses`{.interpreted-text role="mod"} module, `COLORS`{.interpreted-text role="const"} and `COLOR_PAIRS`{.interpreted-text role="const"}, containing the maximum number of colors and color-pairs the terminal can support. It also restores the colors on the terminal to the values they had when the terminal was just turned on.
:::

::: function
termattrs()

Return a logical OR of all video attributes supported by the terminal. This information is useful when a curses program needs complete control over the appearance of the screen.
:::

::: function
termname()

Return the value of the environment variable `TERM`{.interpreted-text role="envvar"}, as a bytes object, truncated to 14 characters.
:::

::: function
tigetflag(capname)

Return the value of the Boolean capability corresponding to the terminfo capability name *capname* as an integer. Return the value `-1` if *capname* is not a Boolean capability, or `0` if it is canceled or absent from the terminal description.
:::

::: function
tigetnum(capname)

Return the value of the numeric capability corresponding to the terminfo capability name *capname* as an integer. Return the value `-2` if *capname* is not a numeric capability, or `-1` if it is canceled or absent from the terminal description.
:::

::: function
tigetstr(capname)

Return the value of the string capability corresponding to the terminfo capability name *capname* as a bytes object. Return `None` if *capname* is not a terminfo \"string capability\", or is canceled or absent from the terminal description.
:::

::: function
tparm(str\[, \...\])

Instantiate the bytes object *str* with the supplied parameters, where *str* should be a parameterized string obtained from the terminfo database. E.g. `tparm(tigetstr("cup"), 5, 3)` could result in `b'\033[6;4H'`, the exact result depending on terminal type.
:::

::: function
typeahead(fd)

Specify that the file descriptor *fd* be used for typeahead checking. If *fd* is `-1`, then no typeahead checking is done.

The curses library does \"line-breakout optimization\" by looking for typeahead periodically while updating the screen. If input is found, and it is coming from a tty, the current update is postponed until refresh or doupdate is called again, allowing faster response to commands typed in advance. This function allows specifying a different file descriptor for typeahead checking.
:::

::: function
unctrl(ch)

Return a bytes object which is a printable representation of the character *ch*. Control characters are represented as a caret followed by the character, for example as `b'^C'`. Printing characters are left as they are.
:::

::::: function
ungetch(ch)

Push *ch* so the next `~window.getch`{.interpreted-text role="meth"} will return it.

:::: note
::: title
Note
:::

Only one *ch* can be pushed before `!getch`{.interpreted-text role="meth"} is called.
::::
:::::

:::: function
update_lines_cols()

Update the `LINES`{.interpreted-text role="const"} and `COLS`{.interpreted-text role="const"} module variables. Useful for detecting manual screen resize.

::: versionadded
3.5
:::
::::

:::::: function
unget_wch(ch)

Push *ch* so the next `~window.get_wch`{.interpreted-text role="meth"} will return it.

:::: note
::: title
Note
:::

Only one *ch* can be pushed before `!get_wch`{.interpreted-text role="meth"} is called.
::::

::: versionadded
3.3
:::
::::::

::: function
ungetmouse(id, x, y, z, bstate)

Push a `KEY_MOUSE`{.interpreted-text role="const"} event onto the input queue, associating the given state data with it.
:::

::: function
use_env(flag)

If used, this function should be called before `initscr`{.interpreted-text role="func"} or newterm are called. When *flag* is `False`, the values of lines and columns specified in the terminfo database will be used, even if environment variables `LINES`{.interpreted-text role="envvar"} and `COLUMNS`{.interpreted-text role="envvar"} (used by default) are set, or if curses is running in a window (in which case default behavior would be to use the window size if `LINES`{.interpreted-text role="envvar"} and `COLUMNS`{.interpreted-text role="envvar"} are not set).
:::

::: function
use_default_colors()

Equivalent to `assume_default_colors(-1, -1)`.
:::

::: function
wrapper(func, /, *args,*\*kwargs)

Initialize curses and call another callable object, *func*, which should be the rest of your curses-using application. If the application raises an exception, this function will restore the terminal to a sane state before re-raising the exception and generating a traceback. The callable object *func* is then passed the main window \'stdscr\' as its first argument, followed by any other arguments passed to `!wrapper`{.interpreted-text role="func"}. Before calling *func*, `!wrapper`{.interpreted-text role="func"} turns on cbreak mode, turns off echo, enables the terminal keypad, and initializes colors if the terminal has color support. On exit (whether normally or by exception) it restores cooked mode, turns on echo, and disables the terminal keypad.
:::

## Window Objects {#curses-window-objects}

::: window
Window objects, as returned by `initscr`{.interpreted-text role="func"} and `newwin`{.interpreted-text role="func"} above, have the following methods and attributes:
:::

::::: method
window.addch(ch\[, attr\]) window.addch(y, x, ch\[, attr\])

Paint character *ch* at `(y, x)` with attributes *attr*, overwriting any character previously painted at that location. By default, the character position and attributes are the current settings for the window object.

:::: note
::: title
Note
:::

Writing outside the window, subwindow, or pad raises a `curses.error`{.interpreted-text role="exc"}. Attempting to write to the lower right corner of a window, subwindow, or pad will cause an exception to be raised after the character is printed.
::::
:::::

::: method
window.addnstr(str, n\[, attr\]) window.addnstr(y, x, str, n\[, attr\])

Paint at most *n* characters of the character string *str* at `(y, x)` with attributes *attr*, overwriting anything previously on the display.
:::

::::: method
window.addstr(str\[, attr\]) window.addstr(y, x, str\[, attr\])

Paint the character string *str* at `(y, x)` with attributes *attr*, overwriting anything previously on the display.

:::: note
::: title
Note
:::

- Writing outside the window, subwindow, or pad raises `curses.error`{.interpreted-text role="exc"}. Attempting to write to the lower right corner of a window, subwindow, or pad will cause an exception to be raised after the string is printed.
- A [bug in ncurses](https://bugs.python.org/issue35924), the backend for this Python module, can cause SegFaults when resizing windows. This is fixed in ncurses-6.1-20190511. If you are stuck with an earlier ncurses, you can avoid triggering this if you do not call `addstr`{.interpreted-text role="func"} with a *str* that has embedded newlines. Instead, call `addstr`{.interpreted-text role="func"} separately for each line.
::::
:::::

::: method
window.attroff(attr)

Remove attribute *attr* from the \"background\" set applied to all writes to the current window.
:::

::: method
window.attron(attr)

Add attribute *attr* to the \"background\" set applied to all writes to the current window.
:::

::: method
window.attrset(attr)

Set the \"background\" set of attributes to *attr*. This set is initially `0` (no attributes).
:::

::: method
window.bkgd(ch\[, attr\])

Set the background property of the window to the character *ch*, with attributes *attr*. The change is then applied to every character position in that window:

- The attribute of every character in the window is changed to the new background attribute.
- Wherever the former background character appears, it is changed to the new background character.
:::

::: method
window.bkgdset(ch\[, attr\])

Set the window\'s background. A window\'s background consists of a character and any combination of attributes. The attribute part of the background is combined (OR\'ed) with all non-blank characters that are written into the window. Both the character and attribute parts of the background are combined with the blank characters. The background becomes a property of the character and moves with the character through any scrolling and insert/delete line/character operations.
:::

::::: method
window.border(\[ls\[, rs\[, ts\[, bs\[, tl\[, tr\[, bl\[, br\]\]\]\]\]\]\]\])

Draw a border around the edges of the window. Each parameter specifies the character to use for a specific part of the border; see the table below for more details.

:::: note
::: title
Note
:::

A `0` value for any parameter will cause the default character to be used for that parameter. Keyword parameters can *not* be used. The defaults are listed in this table:
::::

  ----------------------------------------------------------------------------------
  Parameter   Description           Default value
  ----------- --------------------- ------------------------------------------------
  *ls*        Left side             `ACS_VLINE`{.interpreted-text role="const"}

  *rs*        Right side            `ACS_VLINE`{.interpreted-text role="const"}

  *ts*        Top                   `ACS_HLINE`{.interpreted-text role="const"}

  *bs*        Bottom                `ACS_HLINE`{.interpreted-text role="const"}

  *tl*        Upper-left corner     `ACS_ULCORNER`{.interpreted-text role="const"}

  *tr*        Upper-right corner    `ACS_URCORNER`{.interpreted-text role="const"}

  *bl*        Bottom-left corner    `ACS_LLCORNER`{.interpreted-text role="const"}

  *br*        Bottom-right corner   `ACS_LRCORNER`{.interpreted-text role="const"}
  ----------------------------------------------------------------------------------
:::::

::: method
window.box(\[vertch, horch\])

Similar to `border`{.interpreted-text role="meth"}, but both *ls* and *rs* are *vertch* and both *ts* and *bs* are *horch*. The default corner characters are always used by this function.
:::

::: method
window.chgat(attr) window.chgat(num, attr) window.chgat(y, x, attr) window.chgat(y, x, num, attr)

Set the attributes of *num* characters at the current cursor position, or at position `(y, x)` if supplied. If *num* is not given or is `-1`, the attribute will be set on all the characters to the end of the line. This function moves cursor to position `(y, x)` if supplied. The changed line will be touched using the `touchline`{.interpreted-text role="meth"} method so that the contents will be redisplayed by the next window refresh.
:::

::: method
window.clear()

Like `erase`{.interpreted-text role="meth"}, but also cause the whole window to be repainted upon next call to `refresh`{.interpreted-text role="meth"}.
:::

::: method
window.clearok(flag)

If *flag* is `True`, the next call to `refresh`{.interpreted-text role="meth"} will clear the window completely.
:::

::: method
window.clrtobot()

Erase from cursor to the end of the window: all lines below the cursor are deleted, and then the equivalent of `clrtoeol`{.interpreted-text role="meth"} is performed.
:::

::: method
window.clrtoeol()

Erase from cursor to the end of the line.
:::

::: method
window.cursyncup()

Update the current cursor position of all the ancestors of the window to reflect the current cursor position of the window.
:::

::: method
window.delch(\[y, x\])

Delete any character at `(y, x)`.
:::

::: method
window.deleteln()

Delete the line under the cursor. All following lines are moved up by one line.
:::

::: method
window.derwin(begin_y, begin_x) window.derwin(nlines, ncols, begin_y, begin_x)

An abbreviation for \"derive window\", `derwin`{.interpreted-text role="meth"} is the same as calling `subwin`{.interpreted-text role="meth"}, except that *begin_y* and *begin_x* are relative to the origin of the window, rather than relative to the entire screen. Return a window object for the derived window.
:::

::: method
window.echochar(ch\[, attr\])

Add character *ch* with attribute *attr*, and immediately call `refresh`{.interpreted-text role="meth"} on the window.
:::

:::: method
window.enclose(y, x)

Test whether the given pair of screen-relative character-cell coordinates are enclosed by the given window, returning `True` or `False`. It is useful for determining what subset of the screen windows enclose the location of a mouse event.

::: versionchanged
3.10 Previously it returned `1` or `0` instead of `True` or `False`.
:::
::::

:::: attribute
window.encoding

Encoding used to encode method arguments (Unicode strings and characters). The encoding attribute is inherited from the parent window when a subwindow is created, for example with `window.subwin`{.interpreted-text role="meth"}. By default, current locale encoding is used (see `locale.getencoding`{.interpreted-text role="func"}).

::: versionadded
3.3
:::
::::

::: method
window.erase()

Clear the window.
:::

::: method
window.getbegyx()

Return a tuple `(y, x)` of coordinates of upper-left corner.
:::

::: method
window.getbkgd()

Return the given window\'s current background character/attribute pair.
:::

::: method
window.getch(\[y, x\])

Get a character. Note that the integer returned does *not* have to be in ASCII range: function keys, keypad keys and so on are represented by numbers higher than 255. In no-delay mode, return `-1` if there is no input, otherwise wait until a key is pressed.
:::

:::: method
window.get_wch(\[y, x\])

Get a wide character. Return a character for most keys, or an integer for function keys, keypad keys, and other special keys. In no-delay mode, raise an exception if there is no input.

::: versionadded
3.3
:::
::::

::: method
window.getkey(\[y, x\])

Get a character, returning a string instead of an integer, as `getch`{.interpreted-text role="meth"} does. Function keys, keypad keys and other special keys return a multibyte string containing the key name. In no-delay mode, raise an exception if there is no input.
:::

::: method
window.getmaxyx()

Return a tuple `(y, x)` of the height and width of the window.
:::

::: method
window.getparyx()

Return the beginning coordinates of this window relative to its parent window as a tuple `(y, x)`. Return `(-1, -1)` if this window has no parent.
:::

:::: method
window.getstr() window.getstr(n) window.getstr(y, x) window.getstr(y, x, n)

Read a bytes object from the user, with primitive line editing capacity. The maximum value for *n* is 2047.

::: versionchanged
3.14 The maximum value for *n* was increased from 1023 to 2047.
:::
::::

::: method
window.getyx()

Return a tuple `(y, x)` of current cursor position relative to the window\'s upper-left corner.
:::

::: method
window.hline(ch, n) window.hline(y, x, ch, n)

Display a horizontal line starting at `(y, x)` with length *n* consisting of the character *ch*.
:::

::: method
window.idcok(flag)

If *flag* is `False`, curses no longer considers using the hardware insert/delete character feature of the terminal; if *flag* is `True`, use of character insertion and deletion is enabled. When curses is first initialized, use of character insert/delete is enabled by default.
:::

::: method
window.idlok(flag)

If *flag* is `True`, `!curses`{.interpreted-text role="mod"} will try and use hardware line editing facilities. Otherwise, line insertion/deletion are disabled.
:::

::: method
window.immedok(flag)

If *flag* is `True`, any change in the window image automatically causes the window to be refreshed; you no longer have to call `refresh`{.interpreted-text role="meth"} yourself. However, it may degrade performance considerably, due to repeated calls to wrefresh. This option is disabled by default.
:::

::: method
window.inch(\[y, x\])

Return the character at the given position in the window. The bottom 8 bits are the character proper, and upper bits are the attributes.
:::

::: method
window.insch(ch\[, attr\]) window.insch(y, x, ch\[, attr\])

Paint character *ch* at `(y, x)` with attributes *attr*, moving the line from position *x* right by one character.
:::

::: method
window.insdelln(nlines)

Insert *nlines* lines into the specified window above the current line. The *nlines* bottom lines are lost. For negative *nlines*, delete *nlines* lines starting with the one under the cursor, and move the remaining lines up. The bottom *nlines* lines are cleared. The current cursor position remains the same.
:::

::: method
window.insertln()

Insert a blank line under the cursor. All following lines are moved down by one line.
:::

::: method
window.insnstr(str, n\[, attr\]) window.insnstr(y, x, str, n\[, attr\])

Insert a character string (as many characters as will fit on the line) before the character under the cursor, up to *n* characters. If *n* is zero or negative, the entire string is inserted. All characters to the right of the cursor are shifted right, with the rightmost characters on the line being lost. The cursor position does not change (after moving to *y*, *x*, if specified).
:::

::: method
window.insstr(str\[, attr\]) window.insstr(y, x, str\[, attr\])

Insert a character string (as many characters as will fit on the line) before the character under the cursor. All characters to the right of the cursor are shifted right, with the rightmost characters on the line being lost. The cursor position does not change (after moving to *y*, *x*, if specified).
:::

:::: method
window.instr(\[n\]) window.instr(y, x\[, n\])

Return a bytes object of characters, extracted from the window starting at the current cursor position, or at *y*, *x* if specified. Attributes are stripped from the characters. If *n* is specified, `instr`{.interpreted-text role="meth"} returns a string at most *n* characters long (exclusive of the trailing NUL). The maximum value for *n* is 2047.

::: versionchanged
3.14 The maximum value for *n* was increased from 1023 to 2047.
:::
::::

::: method
window.is_linetouched(line)

Return `True` if the specified line was modified since the last call to `refresh`{.interpreted-text role="meth"}; otherwise return `False`. Raise a `curses.error`{.interpreted-text role="exc"} exception if *line* is not valid for the given window.
:::

::: method
window.is_wintouched()

Return `True` if the specified window was modified since the last call to `refresh`{.interpreted-text role="meth"}; otherwise return `False`.
:::

::: method
window.keypad(flag)

If *flag* is `True`, escape sequences generated by some keys (keypad, function keys) will be interpreted by `!curses`{.interpreted-text role="mod"}. If *flag* is `False`, escape sequences will be left as is in the input stream.
:::

::: method
window.leaveok(flag)

If *flag* is `True`, cursor is left where it is on update, instead of being at \"cursor position.\" This reduces cursor movement where possible. If possible the cursor will be made invisible.

If *flag* is `False`, cursor will always be at \"cursor position\" after an update.
:::

::: method
window.move(new_y, new_x)

Move cursor to `(new_y, new_x)`.
:::

::: method
window.mvderwin(y, x)

Move the window inside its parent window. The screen-relative parameters of the window are not changed. This routine is used to display different parts of the parent window at the same physical position on the screen.
:::

::: method
window.mvwin(new_y, new_x)

Move the window so its upper-left corner is at `(new_y, new_x)`.
:::

::: method
window.nodelay(flag)

If *flag* is `True`, `getch`{.interpreted-text role="meth"} will be non-blocking.
:::

::: method
window.notimeout(flag)

If *flag* is `True`, escape sequences will not be timed out.

If *flag* is `False`, after a few milliseconds, an escape sequence will not be interpreted, and will be left in the input stream as is.
:::

::: method
window.noutrefresh()

Mark for refresh but wait. This function updates the data structure representing the desired state of the window, but does not force an update of the physical screen. To accomplish that, call `doupdate`{.interpreted-text role="func"}.
:::

::: method
window.overlay(destwin\[, sminrow, smincol, dminrow, dmincol, dmaxrow, dmaxcol\])

Overlay the window on top of *destwin*. The windows need not be the same size, only the overlapping region is copied. This copy is non-destructive, which means that the current background character does not overwrite the old contents of *destwin*.

To get fine-grained control over the copied region, the second form of `overlay`{.interpreted-text role="meth"} can be used. *sminrow* and *smincol* are the upper-left coordinates of the source window, and the other variables mark a rectangle in the destination window.
:::

::: method
window.overwrite(destwin\[, sminrow, smincol, dminrow, dmincol, dmaxrow, dmaxcol\])

Overwrite the window on top of *destwin*. The windows need not be the same size, in which case only the overlapping region is copied. This copy is destructive, which means that the current background character overwrites the old contents of *destwin*.

To get fine-grained control over the copied region, the second form of `overwrite`{.interpreted-text role="meth"} can be used. *sminrow* and *smincol* are the upper-left coordinates of the source window, the other variables mark a rectangle in the destination window.
:::

::: method
window.putwin(file)

Write all data associated with the window into the provided file object. This information can be later retrieved using the `getwin`{.interpreted-text role="func"} function.
:::

::: method
window.redrawln(beg, num)

Indicate that the *num* screen lines, starting at line *beg*, are corrupted and should be completely redrawn on the next `refresh`{.interpreted-text role="meth"} call.
:::

::: method
window.redrawwin()

Touch the entire window, causing it to be completely redrawn on the next `refresh`{.interpreted-text role="meth"} call.
:::

::: method
window.refresh(\[pminrow, pmincol, sminrow, smincol, smaxrow, smaxcol\])

Update the display immediately (sync actual screen with previous drawing/deleting methods).

The 6 optional arguments can only be specified when the window is a pad created with `newpad`{.interpreted-text role="func"}. The additional parameters are needed to indicate what part of the pad and screen are involved. *pminrow* and *pmincol* specify the upper left-hand corner of the rectangle to be displayed in the pad. *sminrow*, *smincol*, *smaxrow*, and *smaxcol* specify the edges of the rectangle to be displayed on the screen. The lower right-hand corner of the rectangle to be displayed in the pad is calculated from the screen coordinates, since the rectangles must be the same size. Both rectangles must be entirely contained within their respective structures. Negative values of *pminrow*, *pmincol*, *sminrow*, or *smincol* are treated as if they were zero.
:::

::: method
window.resize(nlines, ncols)

Reallocate storage for a curses window to adjust its dimensions to the specified values. If either dimension is larger than the current values, the window\'s data is filled with blanks that have the current background rendition (as set by `bkgdset`{.interpreted-text role="meth"}) merged into them.
:::

::: method
window.scroll(\[lines=1\])

Scroll the screen or scrolling region upward by *lines* lines.
:::

::: method
window.scrollok(flag)

Control what happens when the cursor of a window is moved off the edge of the window or scrolling region, either as a result of a newline action on the bottom line, or typing the last character of the last line. If *flag* is `False`, the cursor is left on the bottom line. If *flag* is `True`, the window is scrolled up one line. Note that in order to get the physical scrolling effect on the terminal, it is also necessary to call `idlok`{.interpreted-text role="meth"}.
:::

::: method
window.setscrreg(top, bottom)

Set the scrolling region from line *top* to line *bottom*. All scrolling actions will take place in this region.
:::

::: method
window.standend()

Turn off the standout attribute. On some terminals this has the side effect of turning off all attributes.
:::

::: method
window.standout()

Turn on attribute *A_STANDOUT*.
:::

::: method
window.subpad(begin_y, begin_x) window.subpad(nlines, ncols, begin_y, begin_x)

Return a sub-window, whose upper-left corner is at `(begin_y, begin_x)`, and whose width/height is *ncols*/\*nlines\*.
:::

::: method
window.subwin(begin_y, begin_x) window.subwin(nlines, ncols, begin_y, begin_x)

Return a sub-window, whose upper-left corner is at `(begin_y, begin_x)`, and whose width/height is *ncols*/\*nlines\*.

By default, the sub-window will extend from the specified position to the lower right corner of the window.
:::

::: method
window.syncdown()

Touch each location in the window that has been touched in any of its ancestor windows. This routine is called by `refresh`{.interpreted-text role="meth"}, so it should almost never be necessary to call it manually.
:::

::: method
window.syncok(flag)

If *flag* is `True`, then `syncup`{.interpreted-text role="meth"} is called automatically whenever there is a change in the window.
:::

::: method
window.syncup()

Touch all locations in ancestors of the window that have been changed in the window.
:::

::: method
window.timeout(delay)

Set blocking or non-blocking read behavior for the window. If *delay* is negative, blocking read is used (which will wait indefinitely for input). If *delay* is zero, then non-blocking read is used, and `getch`{.interpreted-text role="meth"} will return `-1` if no input is waiting. If *delay* is positive, then `getch`{.interpreted-text role="meth"} will block for *delay* milliseconds, and return `-1` if there is still no input at the end of that time.
:::

::: method
window.touchline(start, count\[, changed\])

Pretend *count* lines have been changed, starting with line *start*. If *changed* is supplied, it specifies whether the affected lines are marked as having been changed (*changed*`=True`) or unchanged (*changed*`=False`).
:::

::: method
window.touchwin()

Pretend the whole window has been changed, for purposes of drawing optimizations.
:::

::: method
window.untouchwin()

Mark all lines in the window as unchanged since the last call to `refresh`{.interpreted-text role="meth"}.
:::

::: method
window.vline(ch, n\[, attr\]) window.vline(y, x, ch, n\[, attr\])

Display a vertical line starting at `(y, x)` with length *n* consisting of the character *ch* with attributes *attr*.
:::

## Constants

The `!curses`{.interpreted-text role="mod"} module defines the following data members:

::: data
ERR

Some curses routines that return an integer, such as `~window.getch`{.interpreted-text role="meth"}, return `ERR`{.interpreted-text role="const"} upon failure.
:::

::: data
OK

Some curses routines that return an integer, such as `napms`{.interpreted-text role="func"}, return `OK`{.interpreted-text role="const"} upon success.
:::

::: data
version

A bytes object representing the current version of the module.
:::

:::: data
ncurses_version

A named tuple containing the three components of the ncurses library version: *major*, *minor*, and *patch*. All values are integers. The components can also be accessed by name, so `curses.ncurses_version[0]` is equivalent to `curses.ncurses_version.major` and so on.

Availability: if the ncurses library is used.

::: versionadded
3.8
:::
::::

::: data
COLORS

The maximum number of colors the terminal can support. It is defined only after the call to `start_color`{.interpreted-text role="func"}.
:::

::: data
COLOR_PAIRS

The maximum number of color pairs the terminal can support. It is defined only after the call to `start_color`{.interpreted-text role="func"}.
:::

::: data
COLS

The width of the screen, i.e., the number of columns. It is defined only after the call to `initscr`{.interpreted-text role="func"}. Updated by `update_lines_cols`{.interpreted-text role="func"}, `resizeterm`{.interpreted-text role="func"} and `resize_term`{.interpreted-text role="func"}.
:::

::: data
LINES

The height of the screen, i.e., the number of lines. It is defined only after the call to `initscr`{.interpreted-text role="func"}. Updated by `update_lines_cols`{.interpreted-text role="func"}, `resizeterm`{.interpreted-text role="func"} and `resize_term`{.interpreted-text role="func"}.
:::

Some constants are available to specify character cell attributes. The exact constants available are system dependent.

+------------------------+------------------------------------------+
| Attribute              | Meaning                                  |
+========================+==========================================+
| ::: data               | Alternate character set mode             |
| A_ALTCHARSET           |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | Blink mode                               |
| A_BLINK                |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | Bold mode                                |
| A_BOLD                 |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | Dim mode                                 |
| A_DIM                  |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | Invisible or blank mode                  |
| A_INVIS                |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | Italic mode                              |
| A_ITALIC               |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | Normal attribute                         |
| A_NORMAL               |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | Protected mode                           |
| A_PROTECT              |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | Reverse background and foreground colors |
| A_REVERSE              |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | Standout mode                            |
| A_STANDOUT             |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | Underline mode                           |
| A_UNDERLINE            |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | Horizontal highlight                     |
| A_HORIZONTAL           |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | Left highlight                           |
| A_LEFT                 |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | Low highlight                            |
| A_LOW                  |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | Right highlight                          |
| A_RIGHT                |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | Top highlight                            |
| A_TOP                  |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | Vertical highlight                       |
| A_VERTICAL             |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+

::: versionadded
3.7 `A_ITALIC` was added.
:::

Several constants are available to extract corresponding attributes returned by some methods.

+-------------------------+--------------------------------------------------+
| Bit-mask                | Meaning                                          |
+=========================+==================================================+
| > ::: data              | Bit-mask to extract attributes                   |
| > A_ATTRIBUTES          |                                                  |
| > :::                   |                                                  |
+-------------------------+--------------------------------------------------+
| > ::: data              | Bit-mask to extract a character                  |
| > A_CHARTEXT            |                                                  |
| > :::                   |                                                  |
+-------------------------+--------------------------------------------------+
| > ::: data              | Bit-mask to extract color-pair field information |
| > A_COLOR               |                                                  |
| > :::                   |                                                  |
+-------------------------+--------------------------------------------------+

Keys are referred to by integer constants with names starting with `KEY_`. The exact keycaps available are system dependent.

+-------------------------+------------------------------------------------------+
| Key constant            | Key                                                  |
+=========================+======================================================+
| ::: data                | Minimum key value                                    |
| KEY_MIN                 |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Break key (unreliable)                               |
| KEY_BREAK               |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Down-arrow                                           |
| KEY_DOWN                |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Up-arrow                                             |
| KEY_UP                  |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Left-arrow                                           |
| KEY_LEFT                |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Right-arrow                                          |
| KEY_RIGHT               |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Home key (upward+left arrow)                         |
| KEY_HOME                |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Backspace (unreliable)                               |
| KEY_BACKSPACE           |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Function keys. Up to 64 function keys are supported. |
| KEY_F0                  |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Value of function key *n*                            |
| KEY_Fn                  |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Delete line                                          |
| KEY_DL                  |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Insert line                                          |
| KEY_IL                  |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Delete character                                     |
| KEY_DC                  |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Insert char or enter insert mode                     |
| KEY_IC                  |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Exit insert char mode                                |
| KEY_EIC                 |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Clear screen                                         |
| KEY_CLEAR               |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Clear to end of screen                               |
| KEY_EOS                 |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Clear to end of line                                 |
| KEY_EOL                 |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Scroll 1 line forward                                |
| KEY_SF                  |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Scroll 1 line backward (reverse)                     |
| KEY_SR                  |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Next page                                            |
| KEY_NPAGE               |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Previous page                                        |
| KEY_PPAGE               |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Set tab                                              |
| KEY_STAB                |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Clear tab                                            |
| KEY_CTAB                |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Clear all tabs                                       |
| KEY_CATAB               |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Enter or send (unreliable)                           |
| KEY_ENTER               |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Soft (partial) reset (unreliable)                    |
| KEY_SRESET              |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Reset or hard reset (unreliable)                     |
| KEY_RESET               |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Print                                                |
| KEY_PRINT               |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Home down or bottom (lower left)                     |
| KEY_LL                  |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Upper left of keypad                                 |
| KEY_A1                  |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Upper right of keypad                                |
| KEY_A3                  |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Center of keypad                                     |
| KEY_B2                  |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Lower left of keypad                                 |
| KEY_C1                  |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Lower right of keypad                                |
| KEY_C3                  |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Back tab                                             |
| KEY_BTAB                |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Beg (beginning)                                      |
| KEY_BEG                 |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Cancel                                               |
| KEY_CANCEL              |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Close                                                |
| KEY_CLOSE               |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Cmd (command)                                        |
| KEY_COMMAND             |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Copy                                                 |
| KEY_COPY                |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Create                                               |
| KEY_CREATE              |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | End                                                  |
| KEY_END                 |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Exit                                                 |
| KEY_EXIT                |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Find                                                 |
| KEY_FIND                |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Help                                                 |
| KEY_HELP                |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Mark                                                 |
| KEY_MARK                |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Message                                              |
| KEY_MESSAGE             |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Move                                                 |
| KEY_MOVE                |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Next                                                 |
| KEY_NEXT                |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Open                                                 |
| KEY_OPEN                |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Options                                              |
| KEY_OPTIONS             |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Prev (previous)                                      |
| KEY_PREVIOUS            |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Redo                                                 |
| KEY_REDO                |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Ref (reference)                                      |
| KEY_REFERENCE           |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Refresh                                              |
| KEY_REFRESH             |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Replace                                              |
| KEY_REPLACE             |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Restart                                              |
| KEY_RESTART             |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Resume                                               |
| KEY_RESUME              |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Save                                                 |
| KEY_SAVE                |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Shifted Beg (beginning)                              |
| KEY_SBEG                |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Shifted Cancel                                       |
| KEY_SCANCEL             |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Shifted Command                                      |
| KEY_SCOMMAND            |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Shifted Copy                                         |
| KEY_SCOPY               |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Shifted Create                                       |
| KEY_SCREATE             |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Shifted Delete char                                  |
| KEY_SDC                 |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Shifted Delete line                                  |
| KEY_SDL                 |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Select                                               |
| KEY_SELECT              |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Shifted End                                          |
| KEY_SEND                |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Shifted Clear line                                   |
| KEY_SEOL                |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Shifted Exit                                         |
| KEY_SEXIT               |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Shifted Find                                         |
| KEY_SFIND               |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Shifted Help                                         |
| KEY_SHELP               |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Shifted Home                                         |
| KEY_SHOME               |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Shifted Input                                        |
| KEY_SIC                 |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Shifted Left arrow                                   |
| KEY_SLEFT               |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Shifted Message                                      |
| KEY_SMESSAGE            |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Shifted Move                                         |
| KEY_SMOVE               |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Shifted Next                                         |
| KEY_SNEXT               |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Shifted Options                                      |
| KEY_SOPTIONS            |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Shifted Prev                                         |
| KEY_SPREVIOUS           |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Shifted Print                                        |
| KEY_SPRINT              |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Shifted Redo                                         |
| KEY_SREDO               |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Shifted Replace                                      |
| KEY_SREPLACE            |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Shifted Right arrow                                  |
| KEY_SRIGHT              |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Shifted Resume                                       |
| KEY_SRSUME              |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Shifted Save                                         |
| KEY_SSAVE               |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Shifted Suspend                                      |
| KEY_SSUSPEND            |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Shifted Undo                                         |
| KEY_SUNDO               |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Suspend                                              |
| KEY_SUSPEND             |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Undo                                                 |
| KEY_UNDO                |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Mouse event has occurred                             |
| KEY_MOUSE               |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Terminal resize event                                |
| KEY_RESIZE              |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+
| ::: data                | Maximum key value                                    |
| KEY_MAX                 |                                                      |
| :::                     |                                                      |
+-------------------------+------------------------------------------------------+

On VT100s and their software emulations, such as X terminal emulators, there are normally at least four function keys (`KEY_F1 <KEY_Fn>`{.interpreted-text role="const"}, `KEY_F2 <KEY_Fn>`{.interpreted-text role="const"}, `KEY_F3 <KEY_Fn>`{.interpreted-text role="const"}, `KEY_F4 <KEY_Fn>`{.interpreted-text role="const"}) available, and the arrow keys mapped to `KEY_UP`{.interpreted-text role="const"}, `KEY_DOWN`{.interpreted-text role="const"}, `KEY_LEFT`{.interpreted-text role="const"} and `KEY_RIGHT`{.interpreted-text role="const"} in the obvious way. If your machine has a PC keyboard, it is safe to expect arrow keys and twelve function keys (older PC keyboards may have only ten function keys); also, the following keypad mappings are standard:

  -------------------------------------------------------
  Keycap                                      Constant
  ------------------------------------------- -----------
  `Insert`{.interpreted-text role="kbd"}      KEY_IC

  `Delete`{.interpreted-text role="kbd"}      KEY_DC

  `Home`{.interpreted-text role="kbd"}        KEY_HOME

  `End`{.interpreted-text role="kbd"}         KEY_END

  `Page Up`{.interpreted-text role="kbd"}     KEY_PPAGE

  `Page Down`{.interpreted-text role="kbd"}   KEY_NPAGE
  -------------------------------------------------------

::: {#curses-acs-codes}
The following table lists characters from the alternate character set. These are inherited from the VT100 terminal, and will generally be available on software emulations such as X terminals. When there is no graphic available, curses falls back on a crude printable ASCII approximation.
:::

:::: note
::: title
Note
:::

These are available only after `initscr`{.interpreted-text role="func"} has been called.
::::

+------------------------+------------------------------------------+
| ACS code               | Meaning                                  |
+========================+==========================================+
| ::: data               | alternate name for upper right corner    |
| ACS_BBSS               |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | solid square block                       |
| ACS_BLOCK              |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | board of squares                         |
| ACS_BOARD              |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | alternate name for horizontal line       |
| ACS_BSBS               |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | alternate name for upper left corner     |
| ACS_BSSB               |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | alternate name for top tee               |
| ACS_BSSS               |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | bottom tee                               |
| ACS_BTEE               |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | bullet                                   |
| ACS_BULLET             |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | checker board (stipple)                  |
| ACS_CKBOARD            |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | arrow pointing down                      |
| ACS_DARROW             |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | degree symbol                            |
| ACS_DEGREE             |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | diamond                                  |
| ACS_DIAMOND            |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | greater-than-or-equal-to                 |
| ACS_GEQUAL             |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | horizontal line                          |
| ACS_HLINE              |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | lantern symbol                           |
| ACS_LANTERN            |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | left arrow                               |
| ACS_LARROW             |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | less-than-or-equal-to                    |
| ACS_LEQUAL             |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | lower left-hand corner                   |
| ACS_LLCORNER           |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | lower right-hand corner                  |
| ACS_LRCORNER           |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | left tee                                 |
| ACS_LTEE               |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | not-equal sign                           |
| ACS_NEQUAL             |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | letter pi                                |
| ACS_PI                 |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | plus-or-minus sign                       |
| ACS_PLMINUS            |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | big plus sign                            |
| ACS_PLUS               |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | right arrow                              |
| ACS_RARROW             |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | right tee                                |
| ACS_RTEE               |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | scan line 1                              |
| ACS_S1                 |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | scan line 3                              |
| ACS_S3                 |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | scan line 7                              |
| ACS_S7                 |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | scan line 9                              |
| ACS_S9                 |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | alternate name for lower right corner    |
| ACS_SBBS               |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | alternate name for vertical line         |
| ACS_SBSB               |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | alternate name for right tee             |
| ACS_SBSS               |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | alternate name for lower left corner     |
| ACS_SSBB               |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | alternate name for bottom tee            |
| ACS_SSBS               |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | alternate name for left tee              |
| ACS_SSSB               |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | alternate name for crossover or big plus |
| ACS_SSSS               |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | pound sterling                           |
| ACS_STERLING           |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | top tee                                  |
| ACS_TTEE               |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | up arrow                                 |
| ACS_UARROW             |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | upper left corner                        |
| ACS_ULCORNER           |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | upper right corner                       |
| ACS_URCORNER           |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+
| ::: data               | vertical line                            |
| ACS_VLINE              |                                          |
| :::                    |                                          |
+------------------------+------------------------------------------+

The following table lists mouse button constants used by `getmouse`{.interpreted-text role="meth"}:

+------------------------------+---------------------------------------------+
| Mouse button constant        | Meaning                                     |
+==============================+=============================================+
| ::: data                     | Mouse button *n* pressed                    |
| BUTTONn_PRESSED              |                                             |
| :::                          |                                             |
+------------------------------+---------------------------------------------+
| ::: data                     | Mouse button *n* released                   |
| BUTTONn_RELEASED             |                                             |
| :::                          |                                             |
+------------------------------+---------------------------------------------+
| ::: data                     | Mouse button *n* clicked                    |
| BUTTONn_CLICKED              |                                             |
| :::                          |                                             |
+------------------------------+---------------------------------------------+
| ::: data                     | Mouse button *n* double clicked             |
| BUTTONn_DOUBLE_CLICKED       |                                             |
| :::                          |                                             |
+------------------------------+---------------------------------------------+
| ::: data                     | Mouse button *n* triple clicked             |
| BUTTONn_TRIPLE_CLICKED       |                                             |
| :::                          |                                             |
+------------------------------+---------------------------------------------+
| ::: data                     | Shift was down during button state change   |
| BUTTON_SHIFT                 |                                             |
| :::                          |                                             |
+------------------------------+---------------------------------------------+
| ::: data                     | Control was down during button state change |
| BUTTON_CTRL                  |                                             |
| :::                          |                                             |
+------------------------------+---------------------------------------------+
| ::: data                     | Control was down during button state change |
| BUTTON_ALT                   |                                             |
| :::                          |                                             |
+------------------------------+---------------------------------------------+

::: versionchanged
3.10 The `BUTTON5_*` constants are now exposed if they are provided by the underlying curses library.
:::

The following table lists the predefined colors:

+-------------------------+----------------------------+
| Constant                | Color                      |
+=========================+============================+
| ::: data                | Black                      |
| COLOR_BLACK             |                            |
| :::                     |                            |
+-------------------------+----------------------------+
| ::: data                | Blue                       |
| COLOR_BLUE              |                            |
| :::                     |                            |
+-------------------------+----------------------------+
| ::: data                | Cyan (light greenish blue) |
| COLOR_CYAN              |                            |
| :::                     |                            |
+-------------------------+----------------------------+
| ::: data                | Green                      |
| COLOR_GREEN             |                            |
| :::                     |                            |
+-------------------------+----------------------------+
| ::: data                | Magenta (purplish red)     |
| COLOR_MAGENTA           |                            |
| :::                     |                            |
+-------------------------+----------------------------+
| ::: data                | Red                        |
| COLOR_RED               |                            |
| :::                     |                            |
+-------------------------+----------------------------+
| ::: data                | White                      |
| COLOR_WHITE             |                            |
| :::                     |                            |
+-------------------------+----------------------------+
| ::: data                | Yellow                     |
| COLOR_YELLOW            |                            |
| :::                     |                            |
+-------------------------+----------------------------+

# `!curses.textpad`{.interpreted-text role="mod"} \-\-- Text input widget for curses programs

::: {.module synopsis="Emacs-like input editing in a curses window."}
curses.textpad
:::

The `!curses.textpad`{.interpreted-text role="mod"} module provides a `Textbox`{.interpreted-text role="class"} class that handles elementary text editing in a curses window, supporting a set of keybindings resembling those of Emacs (thus, also of Netscape Navigator, BBedit 6.x, FrameMaker, and many other programs). The module also provides a rectangle-drawing function useful for framing text boxes or for other purposes.

The module `!curses.textpad`{.interpreted-text role="mod"} defines the following function:

::: function
rectangle(win, uly, ulx, lry, lrx)

Draw a rectangle. The first argument must be a window object; the remaining arguments are coordinates relative to that window. The second and third arguments are the y and x coordinates of the upper left hand corner of the rectangle to be drawn; the fourth and fifth arguments are the y and x coordinates of the lower right hand corner. The rectangle will be drawn using VT100/IBM PC forms characters on terminals that make this possible (including xterm and most other software terminal emulators). Otherwise it will be drawn with ASCII dashes, vertical bars, and plus signs.
:::

## Textbox objects {#curses-textpad-objects}

You can instantiate a `Textbox`{.interpreted-text role="class"} object as follows:

::::::: Textbox(win)
Return a textbox widget object. The *win* argument should be a curses `window <curses-window-objects>`{.interpreted-text role="ref"} object in which the textbox is to be contained. The edit cursor of the textbox is initially located at the upper left hand corner of the containing window, with coordinates `(0, 0)`. The instance\'s `stripspaces`{.interpreted-text role="attr"} flag is initially on.

`Textbox`{.interpreted-text role="class"} objects have the following methods:

::: method
edit(\[validator\])

This is the entry point you will normally use. It accepts editing keystrokes until one of the termination keystrokes is entered. If *validator* is supplied, it must be a function. It will be called for each keystroke entered with the keystroke as a parameter; command dispatch is done on the result. This method returns the window contents as a string; whether blanks in the window are included is affected by the `stripspaces`{.interpreted-text role="attr"} attribute.
:::

::: method
do_command(ch)

Process a single command keystroke. Here are the supported special keystrokes:

  -----------------------------------------------------------------------------------------------------------------
  Keystroke                                   Action
  ------------------------------------------- ---------------------------------------------------------------------
  `Control-A`{.interpreted-text role="kbd"}   Go to left edge of window.

  `Control-B`{.interpreted-text role="kbd"}   Cursor left, wrapping to previous line if appropriate.

  `Control-D`{.interpreted-text role="kbd"}   Delete character under cursor.

  `Control-E`{.interpreted-text role="kbd"}   Go to right edge (stripspaces off) or end of line (stripspaces on).

  `Control-F`{.interpreted-text role="kbd"}   Cursor right, wrapping to next line when appropriate.

  `Control-G`{.interpreted-text role="kbd"}   Terminate, returning the window contents.

  `Control-H`{.interpreted-text role="kbd"}   Delete character backward.

  `Control-J`{.interpreted-text role="kbd"}   Terminate if the window is 1 line, otherwise insert newline.

  `Control-K`{.interpreted-text role="kbd"}   If line is blank, delete it, otherwise clear to end of line.

  `Control-L`{.interpreted-text role="kbd"}   Refresh screen.

  `Control-N`{.interpreted-text role="kbd"}   Cursor down; move down one line.

  `Control-O`{.interpreted-text role="kbd"}   Insert a blank line at cursor location.

  `Control-P`{.interpreted-text role="kbd"}   Cursor up; move up one line.
  -----------------------------------------------------------------------------------------------------------------

Move operations do nothing if the cursor is at an edge where the movement is not possible. The following synonyms are supported where possible:

  -----------------------------------------------------------------------------------------------------
  Constant                                                  Keystroke
  --------------------------------------------------------- -------------------------------------------
  `~curses.KEY_LEFT`{.interpreted-text role="const"}        `Control-B`{.interpreted-text role="kbd"}

  `~curses.KEY_RIGHT`{.interpreted-text role="const"}       `Control-F`{.interpreted-text role="kbd"}

  `~curses.KEY_UP`{.interpreted-text role="const"}          `Control-P`{.interpreted-text role="kbd"}

  `~curses.KEY_DOWN`{.interpreted-text role="const"}        `Control-N`{.interpreted-text role="kbd"}

  `~curses.KEY_BACKSPACE`{.interpreted-text role="const"}   `Control-h`{.interpreted-text role="kbd"}
  -----------------------------------------------------------------------------------------------------

All other keystrokes are treated as a command to insert the given character and move right (with line wrapping).
:::

::: method
gather()

Return the window contents as a string; whether blanks in the window are included is affected by the `stripspaces`{.interpreted-text role="attr"} member.
:::

::: attribute
stripspaces

This attribute is a flag which controls the interpretation of blanks in the window. When it is on, trailing blanks on each line are ignored; any cursor motion that would land the cursor on a trailing blank goes to the end of that line instead, and trailing blanks are stripped when the window contents are gathered.
:::
:::::::
