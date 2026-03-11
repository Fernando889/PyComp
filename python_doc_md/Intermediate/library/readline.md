# `!readline`{.interpreted-text role="mod"} \-\-- GNU readline interface

::: {.module synopsis="GNU readline support for Python."}
readline
:::

------------------------------------------------------------------------

The `!readline`{.interpreted-text role="mod"} module defines a number of functions to facilitate completion and reading/writing of history files from the Python interpreter. This module can be used directly, or via the `rlcompleter`{.interpreted-text role="mod"} module, which supports completion of Python identifiers at the interactive prompt. Settings made using this module affect the behaviour of both the interpreter\'s interactive prompt and the prompts offered by the built-in `input`{.interpreted-text role="func"} function.

Readline keybindings may be configured via an initialization file, typically `.inputrc` in your home directory. See [Readline Init File](https://tiswww.cwru.edu/php/chet/readline/rluserman.html#Readline-Init-File) in the GNU Readline manual for information about the format and allowable constructs of that file, and the capabilities of the Readline library in general.

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

The underlying Readline library API may be implemented by the `editline` (`libedit`) library instead of GNU readline. On macOS the `!readline`{.interpreted-text role="mod"} module detects which library is being used at run time.

The configuration file for `editline` is different from that of GNU readline. If you programmatically load configuration strings you can use `backend`{.interpreted-text role="data"} to determine which library is being used.

If you use `editline`/`libedit` readline emulation on macOS, the initialization file located in your home directory is named `.editrc`. For example, the following content in `~/.editrc` will turn ON *vi* keybindings and TAB completion:

    python:bind -v
    python:bind ^I rl_complete

Also note that different libraries may use different history file formats. When switching the underlying library, existing history files may become unusable.
::::

:::: data
backend

The name of the underlying Readline library being used, either `"readline"` or `"editline"`.

::: versionadded
3.13
:::
::::

## Init file

The following functions relate to the init file and user configuration:

::: function
parse_and_bind(string)

Execute the init line provided in the *string* argument. This calls `!rl_parse_and_bind`{.interpreted-text role="c:func"} in the underlying library.
:::

:::: function
read_init_file(\[filename\])

Execute a readline initialization file. The default filename is the last filename used. This calls `!rl_read_init_file`{.interpreted-text role="c:func"} in the underlying library. It raises an `auditing event <auditing>`{.interpreted-text role="ref"} `open` with the file name if given, and `"<readline_init_file>"` otherwise, regardless of which file the library resolves.

::: versionchanged
3.14 The auditing event was added.
:::
::::

## Line buffer

The following functions operate on the line buffer:

::: function
get_line_buffer()

Return the current contents of the line buffer (`!rl_line_buffer`{.interpreted-text role="c:data"} in the underlying library).
:::

::: function
insert_text(string)

Insert text into the line buffer at the cursor position. This calls `!rl_insert_text`{.interpreted-text role="c:func"} in the underlying library, but ignores the return value.
:::

::: function
redisplay()

Change what\'s displayed on the screen to reflect the current contents of the line buffer. This calls `!rl_redisplay`{.interpreted-text role="c:func"} in the underlying library.
:::

## History file

The following functions operate on a history file:

:::: function
read_history_file(\[filename\])

Load a readline history file, and append it to the history list. The default filename is `~/.history`{.interpreted-text role="file"}. This calls `!read_history`{.interpreted-text role="c:func"} in the underlying library and raises an `auditing event <auditing>`{.interpreted-text role="ref"} `open` with the file name if given and `"~/.history"` otherwise.

::: versionchanged
3.14 The auditing event was added.
:::
::::

:::: function
write_history_file(\[filename\])

Save the history list to a readline history file, overwriting any existing file. The default filename is `~/.history`{.interpreted-text role="file"}. This calls `!write_history`{.interpreted-text role="c:func"} in the underlying library and raises an `auditing event <auditing>`{.interpreted-text role="ref"} `open` with the file name if given and `"~/.history"` otherwise.

::: versionchanged
3.14 The auditing event was added.
:::
::::

::::: function
append_history_file(nelements\[, filename\])

Append the last *nelements* items of history to a file. The default filename is `~/.history`{.interpreted-text role="file"}. The file must already exist. This calls `!append_history`{.interpreted-text role="c:func"} in the underlying library. This function only exists if Python was compiled for a version of the library that supports it. It raises an `auditing event <auditing>`{.interpreted-text role="ref"} `open` with the file name if given and `"~/.history"` otherwise.

::: versionadded
3.5
:::

::: versionchanged
3.14 The auditing event was added.
:::
:::::

::: function
get_history_length() set_history_length(length)

Set or return the desired number of lines to save in the history file. The `write_history_file`{.interpreted-text role="func"} function uses this value to truncate the history file, by calling `!history_truncate_file`{.interpreted-text role="c:func"} in the underlying library. Negative values imply unlimited history file size.
:::

## History list

The following functions operate on a global history list:

::: function
clear_history()

Clear the current history. This calls `!clear_history`{.interpreted-text role="c:func"} in the underlying library. The Python function only exists if Python was compiled for a version of the library that supports it.
:::

::: function
get_current_history_length()

Return the number of items currently in the history. (This is different from `get_history_length`{.interpreted-text role="func"}, which returns the maximum number of lines that will be written to a history file.)
:::

::: function
get_history_item(index)

Return the current contents of history item at *index*. The item index is one-based. This calls `!history_get`{.interpreted-text role="c:func"} in the underlying library.
:::

::: function
remove_history_item(pos)

Remove history item specified by its position from the history. The position is zero-based. This calls `!remove_history`{.interpreted-text role="c:func"} in the underlying library.
:::

::: function
replace_history_item(pos, line)

Replace history item specified by its position with *line*. The position is zero-based. This calls `!replace_history_entry`{.interpreted-text role="c:func"} in the underlying library.
:::

::: function
add_history(line)

Append *line* to the history buffer, as if it was the last line typed. This calls `!add_history`{.interpreted-text role="c:func"} in the underlying library.
:::

::::: function
set_auto_history(enabled)

Enable or disable automatic calls to `!add_history`{.interpreted-text role="c:func"} when reading input via readline. The *enabled* argument should be a Boolean value that when true, enables auto history, and that when false, disables auto history.

::: versionadded
3.6
:::

::: impl-detail
Auto history is enabled by default, and changes to this do not persist across multiple sessions.
:::
:::::

## Startup hooks

::: function
set_startup_hook(\[function\])

Set or remove the function invoked by the `!rl_startup_hook`{.interpreted-text role="c:data"} callback of the underlying library. If *function* is specified, it will be used as the new hook function; if omitted or `None`, any function already installed is removed. The hook is called with no arguments just before readline prints the first prompt.
:::

::: function
set_pre_input_hook(\[function\])

Set or remove the function invoked by the `!rl_pre_input_hook`{.interpreted-text role="c:data"} callback of the underlying library. If *function* is specified, it will be used as the new hook function; if omitted or `None`, any function already installed is removed. The hook is called with no arguments after the first prompt has been printed and just before readline starts reading input characters. This function only exists if Python was compiled for a version of the library that supports it.
:::

:::: function
get_pre_input_hook()

Get the current pre-input hook function, or `None` if no pre-input hook function has been set. This function only exists if Python was compiled for a version of the library that supports it.

::: versionadded
3.15
:::
::::

## Completion {#readline-completion}

The following functions relate to implementing a custom word completion function. This is typically operated by the Tab key, and can suggest and automatically complete a word being typed. By default, Readline is set up to be used by `rlcompleter`{.interpreted-text role="mod"} to complete Python identifiers for the interactive interpreter. If the `!readline`{.interpreted-text role="mod"} module is to be used with a custom completer, a different set of word delimiters should be set.

::: function
set_completer(\[function\])

Set or remove the completer function. If *function* is specified, it will be used as the new completer function; if omitted or `None`, any completer function already installed is removed. The completer function is called as `function(text, state)`, for *state* in `0`, `1`, `2`, \..., until it returns a non-string value. It should return the next possible completion starting with *text*.

The installed completer function is invoked by the *entry_func* callback passed to `!rl_completion_matches`{.interpreted-text role="c:func"} in the underlying library. The *text* string comes from the first parameter to the `!rl_attempted_completion_function`{.interpreted-text role="c:data"} callback of the underlying library.
:::

::: function
get_completer()

Get the completer function, or `None` if no completer function has been set.
:::

::: function
get_completion_type()

Get the type of completion being attempted. This returns the `!rl_completion_type`{.interpreted-text role="c:data"} variable in the underlying library as an integer.
:::

::: function
get_begidx() get_endidx()

Get the beginning or ending index of the completion scope. These indexes are the *start* and *end* arguments passed to the `!rl_attempted_completion_function`{.interpreted-text role="c:data"} callback of the underlying library. The values may be different in the same input editing scenario based on the underlying C readline implementation. Ex: libedit is known to behave differently than libreadline.
:::

::: function
set_completer_delims(string) get_completer_delims()

Set or get the word delimiters for completion. These determine the start of the word to be considered for completion (the completion scope). These functions access the `!rl_completer_word_break_characters`{.interpreted-text role="c:data"} variable in the underlying library.
:::

::: function
set_completion_display_matches_hook(\[function\])

Set or remove the completion display function. If *function* is specified, it will be used as the new completion display function; if omitted or `None`, any completion display function already installed is removed. This sets or clears the `!rl_completion_display_matches_hook`{.interpreted-text role="c:data"} callback in the underlying library. The completion display function is called as `function(substitution, [matches], longest_match_length)` once each time matches need to be displayed.
:::

## Example {#readline-example}

The following example demonstrates how to use the `!readline`{.interpreted-text role="mod"} module\'s history reading and writing functions to automatically load and save a history file named `.python_history`{.interpreted-text role="file"} from the user\'s home directory. The code below would normally be executed automatically during interactive sessions from the user\'s `PYTHONSTARTUP`{.interpreted-text role="envvar"} file. :

    import atexit
    import os
    import readline

    histfile = os.path.join(os.path.expanduser("~"), ".python_history")
    try:
        readline.read_history_file(histfile)
        # default history len is -1 (infinite), which may grow unruly
        readline.set_history_length(1000)
    except FileNotFoundError:
        pass

    atexit.register(readline.write_history_file, histfile)

This code is actually automatically run when Python is run in `interactive mode <tut-interactive>`{.interpreted-text role="ref"} (see `rlcompleter-config`{.interpreted-text role="ref"}).

The following example achieves the same goal but supports concurrent interactive sessions, by only appending the new history. :

    import atexit
    import os
    import readline
    histfile = os.path.join(os.path.expanduser("~"), ".python_history")

    try:
        readline.read_history_file(histfile)
        h_len = readline.get_current_history_length()
    except FileNotFoundError:
        open(histfile, 'wb').close()
        h_len = 0

    def save(prev_h_len, histfile):
        new_h_len = readline.get_current_history_length()
        readline.set_history_length(1000)
        readline.append_history_file(new_h_len - prev_h_len, histfile)
    atexit.register(save, h_len, histfile)

The following example extends the `code.InteractiveConsole`{.interpreted-text role="class"} class to support history save/restore. :

    import atexit
    import code
    import os
    import readline

    class HistoryConsole(code.InteractiveConsole):
        def __init__(self, locals=None, filename="<console>",
                     histfile=os.path.expanduser("~/.console-history")):
            code.InteractiveConsole.__init__(self, locals, filename)
            self.init_history(histfile)

        def init_history(self, histfile):
            readline.parse_and_bind("tab: complete")
            if hasattr(readline, "read_history_file"):
                try:
                    readline.read_history_file(histfile)
                except FileNotFoundError:
                    pass
                atexit.register(self.save_history, histfile)

        def save_history(self, histfile):
            readline.set_history_length(1000)
            readline.write_history_file(histfile)

:::: note
::: title
Note
:::

The new `REPL`{.interpreted-text role="term"} introduced in version 3.13 doesn\'t support readline. However, readline can still be used by setting the `PYTHON_BASIC_REPL`{.interpreted-text role="envvar"} environment variable.
::::
