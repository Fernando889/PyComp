# `!runpy`{.interpreted-text role="mod"} \-\-- Locating and executing Python modules

::: {.module synopsis="Locate and run Python modules without importing them first."}
runpy
:::

**Source code:** `Lib/runpy.py`{.interpreted-text role="source"}

------------------------------------------------------------------------

The `!runpy`{.interpreted-text role="mod"} module is used to locate and run Python modules without importing them first. Its main use is to implement the `-m`{.interpreted-text role="option"} command line switch that allows scripts to be located using the Python module namespace rather than the filesystem.

Note that this is *not* a sandbox module - all code is executed in the current process, and any side effects (such as cached imports of other modules) will remain in place after the functions have returned.

Furthermore, any functions and classes defined by the executed code are not guaranteed to work correctly after a `!runpy`{.interpreted-text role="mod"} function has returned. If that limitation is not acceptable for a given use case, `importlib`{.interpreted-text role="mod"} is likely to be a more suitable choice than this module.

The `!runpy`{.interpreted-text role="mod"} module provides two functions:

:::::::::: function
run_module(mod_name, init_globals=None, run_name=None, alter_sys=False)

::: index
pair: module; \_\_main\_\_
:::

Execute the code of the specified module and return the resulting module\'s globals dictionary. The module\'s code is first located using the standard import mechanism (refer to `302`{.interpreted-text role="pep"} for details) and then executed in a fresh module namespace.

The *mod_name* argument should be an absolute module name. If the module name refers to a package rather than a normal module, then that package is imported and the `__main__`{.interpreted-text role="mod"} submodule within that package is then executed and the resulting module globals dictionary returned.

The optional dictionary argument *init_globals* may be used to pre-populate the module\'s globals dictionary before the code is executed. *init_globals* will not be modified. If any of the special global variables below are defined in *init_globals*, those definitions are overridden by `run_module`{.interpreted-text role="func"}.

The special global variables `__name__`, `__spec__`, `__file__`, `__loader__` and `__package__` are set in the globals dictionary before the module code is executed. (Note that this is a minimal set of variables - other variables may be set implicitly as an interpreter implementation detail.)

`__name__` is set to *run_name* if this optional argument is not `None`{.interpreted-text role="const"}, to `mod_name + '.__main__'` if the named module is a package and to the *mod_name* argument otherwise.

`__spec__` will be set appropriately for the *actually* imported module (that is, `__spec__.name` will always be *mod_name* or `mod_name + '.__main__'`, never *run_name*).

`__file__`, `__loader__` and `__package__` are `set as normal <import-mod-attrs>`{.interpreted-text role="ref"} based on the module spec.

If the argument *alter_sys* is supplied and evaluates to `True`{.interpreted-text role="const"}, then `sys.argv[0]` is updated with the value of `__file__` and `sys.modules[__name__]` is updated with a temporary module object for the module being executed. Both `sys.argv[0]` and `sys.modules[__name__]` are restored to their original values before the function returns.

Note that this manipulation of `sys`{.interpreted-text role="mod"} is not thread-safe. Other threads may see the partially initialised module, as well as the altered list of arguments. It is recommended that the `sys` module be left alone when invoking this function from threaded code.

::: seealso
The `-m`{.interpreted-text role="option"} option offering equivalent functionality from the command line.
:::

::: versionchanged
3.1 Added ability to execute packages by looking for a `__main__`{.interpreted-text role="mod"} submodule.
:::

::: versionchanged
3.2 Added `__cached__` global variable (see `3147`{.interpreted-text role="pep"}).
:::

::: versionchanged
3.4 Updated to take advantage of the module spec feature added by `451`{.interpreted-text role="pep"}. This allows `__cached__` to be set correctly for modules run this way, as well as ensuring the real module name is always accessible as `__spec__.name`.
:::

::: versionchanged
3.12 The setting of `__cached__`, `__loader__`, and `__package__` are deprecated. See `~importlib.machinery.ModuleSpec`{.interpreted-text role="class"} for alternatives.
:::

::: versionchanged
3.15 `__cached__` is no longer set.
:::
::::::::::

::::::::: function
run_path(path_name, init_globals=None, run_name=None)

::: index
pair: module; \_\_main\_\_
:::

Execute the code at the named filesystem location and return the resulting module\'s globals dictionary. As with a script name supplied to the CPython command line, *file_path* may refer to a Python source file, a compiled bytecode file or a valid `sys.path`{.interpreted-text role="data"} entry containing a `__main__`{.interpreted-text role="mod"} module (e.g. a zipfile containing a top-level `__main__.py`{.interpreted-text role="file"} file).

For a simple script, the specified code is simply executed in a fresh module namespace. For a valid `sys.path`{.interpreted-text role="data"} entry (typically a zipfile or directory), the entry is first added to the beginning of `sys.path`. The function then looks for and executes a `__main__`{.interpreted-text role="mod"} module using the updated path. Note that there is no special protection against invoking an existing `__main__` entry located elsewhere on `sys.path` if there is no such module at the specified location.

The optional dictionary argument *init_globals* may be used to pre-populate the module\'s globals dictionary before the code is executed. *init_globals* will not be modified. If any of the special global variables below are defined in *init_globals*, those definitions are overridden by `run_path`{.interpreted-text role="func"}.

The special global variables `__name__`, `__spec__`, `__file__`, `__loader__` and `__package__` are set in the globals dictionary before the module code is executed. (Note that this is a minimal set of variables - other variables may be set implicitly as an interpreter implementation detail.)

`__name__` is set to *run_name* if this optional argument is not `None`{.interpreted-text role="const"} and to `'<run_path>'` otherwise.

If *file_path* directly references a script file (whether as source or as precompiled byte code), then `__file__` will be set to *file_path*, and `__spec__`, `__loader__` and `__package__` will all be set to `None`{.interpreted-text role="const"}.

If *file_path* is a reference to a valid `sys.path`{.interpreted-text role="data"} entry, then `__spec__` will be set appropriately for the imported `__main__`{.interpreted-text role="mod"} module (that is, `__spec__.name` will always be `__main__`). `__file__`, `__loader__` and `__package__` will be `set as normal <import-mod-attrs>`{.interpreted-text role="ref"} based on the module spec.

A number of alterations are also made to the `sys`{.interpreted-text role="mod"} module. Firstly, `sys.path`{.interpreted-text role="data"} may be altered as described above. `sys.argv[0]` is updated with the value of *file_path* and `sys.modules[__name__]` is updated with a temporary module object for the module being executed. All modifications to items in `sys`{.interpreted-text role="mod"} are reverted before the function returns.

Note that, unlike `run_module`{.interpreted-text role="func"}, the alterations made to `sys`{.interpreted-text role="mod"} are not optional in this function as these adjustments are essential to allowing the execution of `sys.path`{.interpreted-text role="data"} entries. As the thread-safety limitations still apply, use of this function in threaded code should be either serialised with the import lock or delegated to a separate process.

::: seealso
`using-on-interface-options`{.interpreted-text role="ref"} for equivalent functionality on the command line (`python path/to/script`).
:::

::: versionadded
3.2
:::

::: versionchanged
3.4 Updated to take advantage of the module spec feature added by `451`{.interpreted-text role="pep"}. This allows `__cached__` to be set correctly in the case where `__main__` is imported from a valid `sys.path`{.interpreted-text role="data"} entry rather than being executed directly.
:::

::: versionchanged
3.12 The setting of `__cached__`, `__loader__`, and `__package__` are deprecated.
:::

::: versionchanged
3.15 `__cached__` is no longer set.
:::
:::::::::

::: seealso

`338`{.interpreted-text role="pep"} \-- Executing modules as scripts

:   PEP written and implemented by Nick Coghlan.

`366`{.interpreted-text role="pep"} \-- Main module explicit relative imports

:   PEP written and implemented by Nick Coghlan.

`451`{.interpreted-text role="pep"} \-- A ModuleSpec Type for the Import System

:   PEP written and implemented by Eric Snow

`using-on-general`{.interpreted-text role="ref"} - CPython command line details

The `importlib.import_module`{.interpreted-text role="func"} function
:::
