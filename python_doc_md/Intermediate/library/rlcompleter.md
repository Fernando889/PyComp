# `!rlcompleter`{.interpreted-text role="mod"} \-\-- Completion function for GNU readline

::: {.module synopsis="Python identifier completion, suitable for the GNU readline library."}
rlcompleter
:::

**Source code:** `Lib/rlcompleter.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

The `!rlcompleter`{.interpreted-text role="mod"} module defines a completion function suitable to be passed to `~readline.set_completer`{.interpreted-text role="func"} in the `readline`{.interpreted-text role="mod"} module.

When this module is imported on a Unix platform with the `readline`{.interpreted-text role="mod"} module available, an instance of the `Completer`{.interpreted-text role="class"} class is automatically created and its `~Completer.complete`{.interpreted-text role="meth"} method is set as the `readline completer <readline-completion>`{.interpreted-text role="ref"}. The method provides completion of valid Python `identifiers and keywords <identifiers>`{.interpreted-text role="ref"}.

Example:

    >>> import rlcompleter
    >>> import readline
    >>> readline.parse_and_bind("tab: complete")
    >>> readline. <TAB PRESSED>
    readline.__doc__          readline.get_line_buffer(  readline.read_init_file(
    readline.__file__         readline.insert_text(      readline.set_completer(
    readline.__name__         readline.parse_and_bind(
    >>> readline.

The `!rlcompleter`{.interpreted-text role="mod"} module is designed for use with Python\'s `interactive mode <tut-interactive>`{.interpreted-text role="ref"}. Unless Python is run with the `-S`{.interpreted-text role="option"} option, the module is automatically imported and configured (see `rlcompleter-config`{.interpreted-text role="ref"}).

On platforms without `readline`{.interpreted-text role="mod"}, the `Completer`{.interpreted-text role="class"} class defined by this module can still be used for custom purposes.

::::: {#completer-objects}
:::: Completer
Completer objects have the following method:

::: method
Completer.complete(text, state)

Return the next possible completion for *text*.

When called by the `readline`{.interpreted-text role="mod"} module, this method is called successively with `state == 0, 1, 2, ...` until the method returns `None`.

If called for *text* that doesn\'t include a period character (`'.'`), it will complete from names currently defined in `__main__`{.interpreted-text role="mod"}, `builtins`{.interpreted-text role="mod"} and keywords (as defined by the `keyword`{.interpreted-text role="mod"} module).

If called for a dotted name, it will try to evaluate anything without obvious side-effects (functions will not be evaluated, but it can generate calls to `~object.__getattr__`{.interpreted-text role="meth"}) up to the last part, and find matches for the rest via the `dir`{.interpreted-text role="func"} function. Any exception raised during the evaluation of the expression is caught, silenced and `None`{.interpreted-text role="const"} is returned.
:::
::::
:::::
