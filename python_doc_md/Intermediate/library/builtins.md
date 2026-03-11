# `!builtins`{.interpreted-text role="mod"} \-\-- Built-in objects

::: {.module synopsis="The module that provides the built-in namespace."}
builtins
:::

------------------------------------------------------------------------

This module provides direct access to all \'built-in\' identifiers of Python; for example, `builtins.open` is the full name for the built-in function `open`{.interpreted-text role="func"}.

This module is not normally accessed explicitly by most applications, but can be useful in modules that provide objects with the same name as a built-in value, but in which the built-in of that name is also needed. For example, in a module that wants to implement an `open`{.interpreted-text role="func"} function that wraps the built-in `open`{.interpreted-text role="func"}, this module can be used directly:

    import builtins

    def open(path):
        f = builtins.open(path, 'r')
        return UpperCaser(f)

    class UpperCaser:
        '''Wrapper around a file that converts output to uppercase.'''

        def __init__(self, f):
            self._f = f

        def read(self, count=-1):
            return self._f.read(count).upper()

        # ...

As an implementation detail, most modules have the name `__builtins__` made available as part of their globals. The value of `__builtins__` is normally either this module or the value of this module\'s `~object.__dict__`{.interpreted-text role="attr"} attribute. Since this is an implementation detail, it may not be used by alternate implementations of Python.

::: seealso
- `built-in-consts`{.interpreted-text role="ref"}
- `bltin-exceptions`{.interpreted-text role="ref"}
- `built-in-funcs`{.interpreted-text role="ref"}
- `bltin-types`{.interpreted-text role="ref"}
:::
