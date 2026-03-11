# Pending removal in Python 3.16

- The import system:
  - Setting `~module.__loader__`{.interpreted-text role="attr"} on a module while failing to set `__spec__.loader <importlib.machinery.ModuleSpec.loader>`{.interpreted-text role="attr"} is deprecated. In Python 3.16, `!__loader__`{.interpreted-text role="attr"} will cease to be set or taken into consideration by the import system or the standard library.
- `array`{.interpreted-text role="mod"}:
  - The `'u'` format code (`wchar_t`{.interpreted-text role="c:type"}) has been deprecated in documentation since Python 3.3 and at runtime since Python 3.13. Use the `'w'` format code (`Py_UCS4`{.interpreted-text role="c:type"}) for Unicode characters instead.
- `asyncio`{.interpreted-text role="mod"}:
  - `!asyncio.iscoroutinefunction`{.interpreted-text role="func"} is deprecated and will be removed in Python 3.16; use `inspect.iscoroutinefunction`{.interpreted-text role="func"} instead. (Contributed by Jiahao Li and Kumar Aditya in `122875`{.interpreted-text role="gh"}.)

  - `asyncio`{.interpreted-text role="mod"} policy system is deprecated and will be removed in Python 3.16. In particular, the following classes and functions are deprecated:

    - `asyncio.AbstractEventLoopPolicy`{.interpreted-text role="class"}
    - `asyncio.DefaultEventLoopPolicy`{.interpreted-text role="class"}
    - `asyncio.WindowsSelectorEventLoopPolicy`{.interpreted-text role="class"}
    - `asyncio.WindowsProactorEventLoopPolicy`{.interpreted-text role="class"}
    - `asyncio.get_event_loop_policy`{.interpreted-text role="func"}
    - `asyncio.set_event_loop_policy`{.interpreted-text role="func"}

    Users should use `asyncio.run`{.interpreted-text role="func"} or `asyncio.Runner`{.interpreted-text role="class"} with *loop_factory* to use the desired event loop implementation.

    For example, to use `asyncio.SelectorEventLoop`{.interpreted-text role="class"} on Windows:

        import asyncio

        async def main():
            ...

        asyncio.run(main(), loop_factory=asyncio.SelectorEventLoop)

    (Contributed by Kumar Aditya in `127949`{.interpreted-text role="gh"}.)
- `builtins`{.interpreted-text role="mod"}:
  - Bitwise inversion on boolean types, `~True` or `~False` has been deprecated since Python 3.12, as it produces surprising and unintuitive results (`-2` and `-1`). Use `not x` instead for the logical negation of a Boolean. In the rare case that you need the bitwise inversion of the underlying integer, convert to `int` explicitly (`~int(x)`).
- `functools`{.interpreted-text role="mod"}:
  - Calling the Python implementation of `functools.reduce`{.interpreted-text role="func"} with *function* or *sequence* as keyword arguments has been deprecated since Python 3.14.
- `logging`{.interpreted-text role="mod"}:
  - Support for custom logging handlers with the *strm* argument is deprecated and scheduled for removal in Python 3.16. Define handlers with the *stream* argument instead. (Contributed by Mariusz Felisiak in `115032`{.interpreted-text role="gh"}.)
- `mimetypes`{.interpreted-text role="mod"}:
  - Valid extensions start with a \'.\' or are empty for `mimetypes.MimeTypes.add_type`{.interpreted-text role="meth"}. Undotted extensions are deprecated and will raise a `ValueError`{.interpreted-text role="exc"} in Python 3.16. (Contributed by Hugo van Kemenade in `75223`{.interpreted-text role="gh"}.)
- `shutil`{.interpreted-text role="mod"}:
  - The `!ExecError`{.interpreted-text role="class"} exception has been deprecated since Python 3.14. It has not been used by any function in `!shutil`{.interpreted-text role="mod"} since Python 3.4, and is now an alias of `RuntimeError`{.interpreted-text role="exc"}.
- `symtable`{.interpreted-text role="mod"}:
  - The `Class.get_methods <symtable.Class.get_methods>`{.interpreted-text role="meth"} method has been deprecated since Python 3.14.
- `sys`{.interpreted-text role="mod"}:
  - The `~sys._enablelegacywindowsfsencoding`{.interpreted-text role="func"} function has been deprecated since Python 3.13. Use the `PYTHONLEGACYWINDOWSFSENCODING`{.interpreted-text role="envvar"} environment variable instead.
- `sysconfig`{.interpreted-text role="mod"}:
  - The `!sysconfig.expand_makefile_vars`{.interpreted-text role="func"} function has been deprecated since Python 3.14. Use the `vars` argument of `sysconfig.get_paths`{.interpreted-text role="func"} instead.
- `tarfile`{.interpreted-text role="mod"}:
  - The undocumented and unused `!TarFile.tarfile`{.interpreted-text role="attr"} attribute has been deprecated since Python 3.13.
