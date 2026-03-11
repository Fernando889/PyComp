# Importing Modules {#importing}

> ::: index
> single: package variable; \_\_all\_\_ single: \_\_all\_\_ (package variable) single: modules (in module sys)
> :::
>
> This is a wrapper around `PyImport_Import()`{.interpreted-text role="c:func"} which takes a `const char *`{.interpreted-text role="c:expr"} as an argument instead of a `PyObject *`{.interpreted-text role="c:expr"}.

> ::: index
> pair: built-in function; \_\_import\_\_
> :::
>
> Import a module. This is best described by referring to the built-in Python function `__import__`{.interpreted-text role="func"}.
>
> The return value is a new reference to the imported module or top-level package, or `NULL` with an exception set on failure. Like for `__import__`{.interpreted-text role="func"}, the return value when a submodule of a package was requested is normally the top-level package, unless a non-empty *fromlist* was given.
>
> Failing imports remove incomplete module objects, like with `PyImport_ImportModule`{.interpreted-text role="c:func"}.

> Import a module. This is best described by referring to the built-in Python function `__import__`{.interpreted-text role="func"}, as the standard `__import__`{.interpreted-text role="func"} function calls this function directly.
>
> The return value is a new reference to the imported module or top-level package, or `NULL` with an exception set on failure. Like for `__import__`{.interpreted-text role="func"}, the return value when a submodule of a package was requested is normally the top-level package, unless a non-empty *fromlist* was given.
>
> ::: versionadded
> 3.3
> :::

> Similar to `PyImport_ImportModuleLevelObject`{.interpreted-text role="c:func"}, but the name is a UTF-8 encoded string instead of a Unicode object.
>
> ::: versionchanged
> 3.3 Negative values for *level* are no longer accepted.
> :::

> This is a higher-level interface that calls the current \"import hook function\" (with an explicit *level* of 0, meaning absolute import). It invokes the `__import__`{.interpreted-text role="func"} function from the `__builtins__` of the current globals. This means that the import is done using whatever import hooks are installed in the current environment.
>
> This function always uses absolute imports.

> Reload a module. Return a new reference to the reloaded module, or `NULL` with an exception set on failure (the module still exists in this case).

> Return the module object corresponding to a module name.
>
> The *name* argument may be of the form `package.module`. First check the modules dictionary if there\'s one there, and if not, create a new one and insert it in the modules dictionary.
>
> Return a `strong reference`{.interpreted-text role="term"} to the module on success. Return `NULL` with an exception set on failure.
>
> The module name *name* is decoded from UTF-8.
>
> This function does not load or import the module; if the module wasn\'t already loaded, you will get an empty module object. Use `PyImport_ImportModule`{.interpreted-text role="c:func"} or one of its variants to import a module. Package structures implied by a dotted name for *name* are not created if not already present.
>
> ::: versionadded
> 3.13
> :::

> Similar to `PyImport_AddModuleRef`{.interpreted-text role="c:func"}, but return a `borrowed
> reference`{.interpreted-text role="term"} and *name* is a Python `str`{.interpreted-text role="class"} object.
>
> ::: versionadded
> 3.3
> :::

> Similar to `PyImport_AddModuleRef`{.interpreted-text role="c:func"}, but return a `borrowed
> reference`{.interpreted-text role="term"}.

> ::: index
> pair: built-in function; compile
> :::
>
> Given a module name (possibly of the form `package.module`) and a code object read from a Python bytecode file or obtained from the built-in function `compile`{.interpreted-text role="func"}, load the module. Return a new reference to the module object, or `NULL` with an exception set if an error occurred. *name* is removed from `sys.modules`{.interpreted-text role="data"} in error cases, even if *name* was already in `sys.modules`{.interpreted-text role="data"} on entry to `PyImport_ExecCodeModule`{.interpreted-text role="c:func"}. Leaving incompletely initialized modules in `sys.modules`{.interpreted-text role="data"} is dangerous, as imports of such modules have no way to know that the module object is an unknown (and probably damaged with respect to the module author\'s intents) state.
>
> The module\'s `~module.__spec__`{.interpreted-text role="attr"} and `~module.__loader__`{.interpreted-text role="attr"} will be set, if not set already, with the appropriate values. The spec\'s loader will be set to the module\'s `!__loader__`{.interpreted-text role="attr"} (if set) and to an instance of `~importlib.machinery.SourceFileLoader`{.interpreted-text role="class"} otherwise.
>
> The module\'s `~module.__file__`{.interpreted-text role="attr"} attribute will be set to the code object\'s `~codeobject.co_filename`{.interpreted-text role="attr"}.
>
> This function will reload the module if it was already imported. See `PyImport_ReloadModule`{.interpreted-text role="c:func"} for the intended way to reload a module.
>
> If *name* points to a dotted name of the form `package.module`, any package structures not already created will still not be created.
>
> See also `PyImport_ExecCodeModuleEx`{.interpreted-text role="c:func"} and `PyImport_ExecCodeModuleWithPathnames`{.interpreted-text role="c:func"}.
>
> ::: versionchanged
> 3.12 The setting of `__cached__` and `~module.__loader__`{.interpreted-text role="attr"} is deprecated. See `~importlib.machinery.ModuleSpec`{.interpreted-text role="class"} for alternatives.
> :::
>
> ::: versionchanged
> 3.15 `__cached__` is no longer set.
> :::

> Like `PyImport_ExecCodeModule`{.interpreted-text role="c:func"}, but the `~module.__file__`{.interpreted-text role="attr"} attribute of the module object is set to *pathname* if it is non-`NULL`.
>
> See also `PyImport_ExecCodeModuleWithPathnames`{.interpreted-text role="c:func"}.

> Like `PyImport_ExecCodeModuleEx`{.interpreted-text role="c:func"}, but the path to any compiled file via *cpathname* is used appropriately when non-`NULL`. Of the three functions, this is the preferred one to use.
>
> ::: versionadded
> 3.3
> :::
>
> ::: versionchanged
> 3.12 Setting `__cached__` is deprecated. See `~importlib.machinery.ModuleSpec`{.interpreted-text role="class"} for alternatives.
> :::
>
> ::: versionchanged
> 3.15 `__cached__` no longer set.
> :::

> Like `PyImport_ExecCodeModuleObject`{.interpreted-text role="c:func"}, but *name*, *pathname* and *cpathname* are UTF-8 encoded strings. Attempts are also made to figure out what the value for *pathname* should be from *cpathname* if the former is set to `NULL`.
>
> ::: versionadded
> 3.2
> :::
>
> ::: versionchanged
> 3.3 Uses `!imp.source_from_cache`{.interpreted-text role="func"} in calculating the source path if only the bytecode path is provided.
> :::
>
> ::: versionchanged
> 3.12 No longer uses the removed `!imp`{.interpreted-text role="mod"} module.
> :::

> Return the magic number for Python bytecode files (a.k.a. `.pyc`{.interpreted-text role="file"} file). The magic number should be present in the first four bytes of the bytecode file, in little-endian byte order. Returns `-1` on error.
>
> ::: versionchanged
> 3.3 Return value of `-1` upon failure.
> :::

> Return the magic tag string for `3147`{.interpreted-text role="pep"} format Python bytecode file names. Keep in mind that the value at `sys.implementation.cache_tag` is authoritative and should be used instead of this function.
>
> ::: versionadded
> 3.2
> :::

> Return the dictionary used for the module administration (a.k.a. `sys.modules`). Note that this is a per-interpreter variable.

> Return the already imported module with the given name. If the module has not been imported yet then returns `NULL` but does not set an error. Returns `NULL` and sets an error if the lookup failed.
>
> ::: versionadded
> 3.7
> :::

> Return a finder object for a `sys.path`{.interpreted-text role="data"}/`!pkg.__path__`{.interpreted-text role="attr"} item *path*, possibly by fetching it from the `sys.path_importer_cache`{.interpreted-text role="data"} dict. If it wasn\'t yet cached, traverse `sys.path_hooks`{.interpreted-text role="data"} until a hook is found that can handle the path item. Return `None` if no hook could; this tells our caller that the `path based finder`{.interpreted-text role="term"} could not find a finder for this path item. Cache the result in `sys.path_importer_cache`{.interpreted-text role="data"}. Return a new reference to the finder object.

> Load a frozen module named *name*. Return `1` for success, `0` if the module is not found, and `-1` with an exception set if the initialization failed. To access the imported module on a successful load, use `PyImport_ImportModule`{.interpreted-text role="c:func"}. (Note the misnomer \-\-- this function would reload the module if it was already imported.)
>
> ::: versionadded
> 3.3
> :::
>
> ::: versionchanged
> 3.4 The `__file__` attribute is no longer set on the module.
> :::

> Similar to `PyImport_ImportFrozenModuleObject`{.interpreted-text role="c:func"}, but the name is a UTF-8 encoded string instead of a Unicode object.

> ::: index
> single: freeze utility
> :::
>
> This is the structure type definition for frozen module descriptors, as generated by the `freeze`{.interpreted-text role="program"} utility (see `Tools/freeze/`{.interpreted-text role="file"} in the Python source distribution). Its definition, found in `Include/import.h`{.interpreted-text role="file"}, is:
>
> ``` c
> struct _frozen {
>     const char *name;
>     const unsigned char *code;
>     int size;
>     bool is_package;
> };
> ```
>
> ::: versionchanged
> 3.11 The new `is_package` field indicates whether the module is a package or not. This replaces setting the `size` field to a negative value.
> :::

> This pointer is initialized to point to an array of `_frozen`{.interpreted-text role="c:struct"} records, terminated by one whose members are all `NULL` or zero. When a frozen module is imported, it is searched in this table. Third-party code could play tricks with this to provide a dynamically created collection of frozen modules.

> Add a single module to the existing table of built-in modules. This is a convenience wrapper around `PyImport_ExtendInittab`{.interpreted-text role="c:func"}, returning `-1` if the table could not be extended. The new module can be imported by the name *name*, and uses the function *initfunc* as the initialization function called on the first attempted import. This should be called before `Py_Initialize`{.interpreted-text role="c:func"}.

> Structure describing a single entry in the list of built-in modules. Programs which embed Python may use an array of these structures in conjunction with `PyImport_ExtendInittab`{.interpreted-text role="c:func"} to provide additional built-in modules. The structure consists of two members:
>
> > The module name, as an ASCII encoded string.
>
> > Initialization function for a module built into the interpreter.

> Add a collection of modules to the table of built-in modules. The *newtab* array must end with a sentinel entry which contains `NULL` for the `~_inittab.name`{.interpreted-text role="c:member"} field; failure to provide the sentinel value can result in a memory fault. Returns `0` on success or `-1` if insufficient memory could be allocated to extend the internal table. In the event of failure, no modules are added to the internal table. This must be called before `Py_Initialize`{.interpreted-text role="c:func"}.
>
> If Python is initialized multiple times, `PyImport_AppendInittab`{.interpreted-text role="c:func"} or `PyImport_ExtendInittab`{.interpreted-text role="c:func"} must be called before each Python initialization.

> The table of built-in modules used by Python initialization. Do not use this directly; use `PyImport_AppendInittab`{.interpreted-text role="c:func"} and `PyImport_ExtendInittab`{.interpreted-text role="c:func"} instead.

> Import the module *mod_name* and get its attribute *attr_name*.
>
> Names must be Python `str`{.interpreted-text role="class"} objects.
>
> Helper function combining `PyImport_Import`{.interpreted-text role="c:func"} and `PyObject_GetAttr`{.interpreted-text role="c:func"}. For example, it can raise `ImportError`{.interpreted-text role="exc"} if the module is not found, and `AttributeError`{.interpreted-text role="exc"} if the attribute doesn\'t exist.
>
> ::: versionadded
> 3.14
> :::

> Similar to `PyImport_ImportModuleAttr`{.interpreted-text role="c:func"}, but names are UTF-8 encoded strings instead of Python `str`{.interpreted-text role="class"} objects.
>
> ::: versionadded
> 3.14
> :::

> Gets the current lazy imports mode.
>
> ::: versionadded
> next
> :::

> Return a `strong reference`{.interpreted-text role="term"} to the current lazy imports filter, or `NULL` if none exists. This function always succeeds.
>
> ::: versionadded
> next
> :::

> Similar to `PyImport_ImportModuleAttr`{.interpreted-text role="c:func"}, but names are UTF-8 encoded strings instead of Python `str`{.interpreted-text role="class"} objects.
>
> This function always returns `0`.
>
> ::: versionadded
> next
> :::

> Sets the current lazy imports filter. The *filter* should be a callable that will receive `(importing_module_name, imported_module_name, [fromlist])` when an import can potentially be lazy and that must return `True` if the import should be lazy and `False` otherwise.
>
> Return `0` on success and `-1` with an exception set otherwise.
>
> ::: versionadded
> next
> :::

> Enumeration of possible lazy import modes.
>
> > Respect the `lazy` keyword in source code. This is the default mode.
>
> > Make all imports lazy by default.
>
> > Disable lazy imports entirely. Even explicit `lazy` statements become eager imports.
>
> ::: versionadded
> next
> :::

> This function is a building block that enables embedders to implement the `~importlib.abc.Loader.create_module`{.interpreted-text role="py:meth"} step of custom static extension importers (e.g. of statically-linked extensions).
>
> *spec* must be a `~importlib.machinery.ModuleSpec`{.interpreted-text role="class"} object.
>
> *initfunc* must be an `initialization function <extension-export-hook>`{.interpreted-text role="ref"}, the same as for `PyImport_AppendInittab`{.interpreted-text role="c:func"}.
>
> On success, create and return a module object. This module will not be initialized; call `PyModule_Exec`{.interpreted-text role="c:func"} to initialize it. (Custom importers should do this in their `~importlib.abc.Loader.exec_module`{.interpreted-text role="py:meth"} method.)
>
> On error, return NULL with an exception set.
>
> ::: versionadded
> 3.15
> :::
