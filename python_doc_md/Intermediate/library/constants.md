# Built-in Constants {#built-in-consts}

A small number of constants live in the built-in namespace. They are:

::: data
False

The false value of the `bool`{.interpreted-text role="class"} type. Assignments to `False` are illegal and raise a `SyntaxError`{.interpreted-text role="exc"}.
:::

::: data
True

The true value of the `bool`{.interpreted-text role="class"} type. Assignments to `True` are illegal and raise a `SyntaxError`{.interpreted-text role="exc"}.
:::

::: data
None

An object frequently used to represent the absence of a value, as when default arguments are not passed to a function. Assignments to `None` are illegal and raise a `SyntaxError`{.interpreted-text role="exc"}. `None` is the sole instance of the `~types.NoneType`{.interpreted-text role="data"} type.
:::

::::::::: data
NotImplemented

A special value which should be returned by the binary special methods (e.g. `~object.__eq__`{.interpreted-text role="meth"}, `~object.__lt__`{.interpreted-text role="meth"}, `~object.__add__`{.interpreted-text role="meth"}, `~object.__rsub__`{.interpreted-text role="meth"}, etc.) to indicate that the operation is not implemented with respect to the other type; may be returned by the in-place binary special methods (e.g. `~object.__imul__`{.interpreted-text role="meth"}, `~object.__iand__`{.interpreted-text role="meth"}, etc.) for the same purpose. It should not be evaluated in a boolean context. `!NotImplemented`{.interpreted-text role="data"} is the sole instance of the `types.NotImplementedType`{.interpreted-text role="data"} type.

:::: note
::: title
Note
:::

When a binary (or in-place) method returns `!NotImplemented`{.interpreted-text role="data"} the interpreter will try the reflected operation on the other type (or some other fallback, depending on the operator). If all attempts return `!NotImplemented`{.interpreted-text role="data"}, the interpreter will raise an appropriate exception. Incorrectly returning `!NotImplemented`{.interpreted-text role="data"} will result in a misleading error message or the `!NotImplemented`{.interpreted-text role="data"} value being returned to Python code.

See `implementing-the-arithmetic-operations`{.interpreted-text role="ref"} for examples.
::::

:::: caution
::: title
Caution
:::

`!NotImplemented`{.interpreted-text role="data"} and `!NotImplementedError`{.interpreted-text role="exc"} are not interchangeable. This constant should only be used as described above; see `NotImplementedError`{.interpreted-text role="exc"} for details on correct usage of the exception.
::::

::: versionchanged
3.9 Evaluating `!NotImplemented`{.interpreted-text role="data"} in a boolean context was deprecated.
:::

::: versionchanged
3.14 Evaluating `!NotImplemented`{.interpreted-text role="data"} in a boolean context now raises a `TypeError`{.interpreted-text role="exc"}. It previously evaluated to `True`{.interpreted-text role="const"} and emitted a `DeprecationWarning`{.interpreted-text role="exc"} since Python 3.9.
:::
:::::::::

::: index
single: \...; ellipsis literal
:::

::: data
Ellipsis

The same as the ellipsis literal \"`...`\", an object frequently used to indicate that something is omitted. Assignment to `Ellipsis` is possible, but assignment to `...` raises a `SyntaxError`{.interpreted-text role="exc"}. `Ellipsis` is the sole instance of the `types.EllipsisType`{.interpreted-text role="data"} type.
:::

::: data
\_\_debug\_\_

This constant is true if Python was not started with an `-O`{.interpreted-text role="option"} option. See also the `assert`{.interpreted-text role="keyword"} statement.
:::

:::: note
::: title
Note
:::

The names `None`{.interpreted-text role="data"}, `False`{.interpreted-text role="data"}, `True`{.interpreted-text role="data"} and `__debug__`{.interpreted-text role="data"} cannot be reassigned (assignments to them, even as an attribute name, raise `SyntaxError`{.interpreted-text role="exc"}), so they can be considered \"true\" constants.
::::

## Constants added by the `site`{.interpreted-text role="mod"} module {#site-consts}

The `site`{.interpreted-text role="mod"} module (which is imported automatically during startup, except if the `-S`{.interpreted-text role="option"} command-line option is given) adds several constants to the built-in namespace. They are useful for the interactive interpreter shell and should not be used in programs.

::: data
quit(code=None) exit(code=None)

Objects that when printed, print a message like \"Use quit() or Ctrl-D (i.e. EOF) to exit\", and when accessed directly in the interactive interpreter or called as functions, raise `SystemExit`{.interpreted-text role="exc"} with the specified exit code.
:::

::: {.data noindex=""}
help

Object that when printed, prints the message \"Type help() for interactive help, or help(object) for help about object.\", and when accessed directly in the interactive interpreter, invokes the built-in help system (see `help`{.interpreted-text role="func"}).
:::

::: data
copyright credits

Objects that when printed or called, print the text of copyright or credits, respectively.
:::

::: data
license

Object that when printed, prints the message \"Type license() to see the full license text\", and when called, displays the full license text in a pager-like fashion (one screen at a time).
:::
