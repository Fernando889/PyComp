# Module Objects {#moduleobjects}

::: index
pair: object; module
:::

> ::: index
> single: ModuleType (in module types)
> :::
>
> This instance of `PyTypeObject`{.interpreted-text role="c:type"} represents the Python module type. This is exposed to Python programs as `types.ModuleType`{.interpreted-text role="py:class"}.

> Return true if *p* is a module object, or a subtype of a module object. This function always succeeds.

> Return true if *p* is a module object, but not a subtype of `PyModule_Type`{.interpreted-text role="c:data"}. This function always succeeds.

> ::: index
> single: \_\_name\_\_ (module attribute) single: \_\_doc\_\_ (module attribute) single: \_\_file\_\_ (module attribute) single: \_\_package\_\_ (module attribute) single: \_\_loader\_\_ (module attribute)
> :::
>
> Return a new module object with `module.__name__`{.interpreted-text role="attr"} set to *name*. The module\'s `!__name__`{.interpreted-text role="attr"}, `~module.__doc__`{.interpreted-text role="attr"}, `~module.__package__`{.interpreted-text role="attr"} and `~module.__loader__`{.interpreted-text role="attr"} attributes are filled in (all but `!__name__`{.interpreted-text role="attr"} are set to `None`). The caller is responsible for setting a `~module.__file__`{.interpreted-text role="attr"} attribute.
>
> Return `NULL` with an exception set on error.
>
> ::: versionadded
> 3.3
> :::
>
> ::: versionchanged
> 3.4 `~module.__package__`{.interpreted-text role="attr"} and `~module.__loader__`{.interpreted-text role="attr"} are now set to `None`.
> :::

> Similar to `PyModule_NewObject`{.interpreted-text role="c:func"}, but the name is a UTF-8 encoded string instead of a Unicode object.

> ::: index
> single: \_\_dict\_\_ (module attribute)
> :::
>
> Return the dictionary object that implements *module*\'s namespace; this object is the same as the `~object.__dict__`{.interpreted-text role="attr"} attribute of the module object. If *module* is not a module object (or a subtype of a module object), `SystemError`{.interpreted-text role="exc"} is raised and `NULL` is returned.
>
> It is recommended extensions use other `PyModule_*` and `PyObject_*` functions rather than directly manipulate a module\'s `~object.__dict__`{.interpreted-text role="attr"}.
>
> The returned reference is borrowed from the module; it is valid until the module is destroyed.

> ::: index
> single: \_\_name\_\_ (module attribute) single: SystemError (built-in exception)
> :::
>
> Return *module*\'s `~module.__name__`{.interpreted-text role="attr"} value. If the module does not provide one, or if it is not a string, `SystemError`{.interpreted-text role="exc"} is raised and `NULL` is returned.
>
> ::: versionadded
> 3.3
> :::

> Similar to `PyModule_GetNameObject`{.interpreted-text role="c:func"} but return the name encoded to `'utf-8'`.
>
> The returned buffer is only valid until the module is renamed or destroyed. Note that Python code may rename a module by setting its `~module.__name__`{.interpreted-text role="py:attr"} attribute.

> Return a pointer to the `PyModuleDef`{.interpreted-text role="c:type"} struct from which the module was created, or `NULL` if the module wasn\'t created from a definition.
>
> On error, return `NULL` with an exception set. Use `PyErr_Occurred`{.interpreted-text role="c:func"} to tell this case apart from a missing `!PyModuleDef`{.interpreted-text role="c:type"}.

> ::: index
> single: \_\_file\_\_ (module attribute) single: SystemError (built-in exception)
> :::
>
> Return the name of the file from which *module* was loaded using *module*\'s `~module.__file__`{.interpreted-text role="attr"} attribute. If this is not defined, or if it is not a string, raise `SystemError`{.interpreted-text role="exc"} and return `NULL`; otherwise return a reference to a Unicode object.
>
> ::: versionadded
> 3.2
> :::

> Similar to `PyModule_GetFilenameObject`{.interpreted-text role="c:func"} but return the filename encoded to \'utf-8\'.
>
> The returned buffer is only valid until the module\'s `~module.__file__`{.interpreted-text role="py:attr"} attribute is reassigned or the module is destroyed.
>
> ::: deprecated
> 3.2 `PyModule_GetFilename`{.interpreted-text role="c:func"} raises `UnicodeEncodeError`{.interpreted-text role="exc"} on unencodable filenames, use `PyModule_GetFilenameObject`{.interpreted-text role="c:func"} instead.
> :::

## Module definition {#pymoduledef_slot}

Modules created using the C API are typically defined using an array of `slots`{.interpreted-text role="dfn"}. The slots provide a \"description\" of how a module should be created.

::: versionchanged
3.15

Previously, a `PyModuleDef`{.interpreted-text role="c:type"} struct was necessary to define modules. The older way of defining modules is still available: consult either the `pymoduledef`{.interpreted-text role="ref"} section or earlier versions of this documentation if you plan to support earlier Python versions.
:::

The slots array is usually used to define an extension module\'s "main" module object (see `extension-modules`{.interpreted-text role="ref"} for details). It can also be used to `create extension modules dynamically <module-from-slots>`{.interpreted-text role="ref"}.

Unless specified otherwise, the same slot ID may not be repeated in an array of slots.

> > A slot ID, chosen from the available `Py_mod_*` values explained below.
> >
> > An ID of 0 marks the end of a `!PyModuleDef_Slot`{.interpreted-text role="c:type"} array.
>
> > Value of the slot, whose meaning depends on the slot ID.
> >
> > The value may not be NULL. To leave a slot out, omit the `PyModuleDef_Slot`{.interpreted-text role="c:type"} entry entirely.
>
> ::: versionadded
> 3.5
> :::

### Metadata slots

> `Slot ID <PyModuleDef_Slot.slot>`{.interpreted-text role="c:type"} for the name of the new module, as a NUL-terminated UTF8-encoded `const char *`.
>
> Note that modules are typically created using a `~importlib.machinery.ModuleSpec`{.interpreted-text role="py:class"}, and when they are, the name from the spec will be used instead of `!Py_mod_name`{.interpreted-text role="c:data"}. However, it is still recommended to include this slot for introspection and debugging purposes.
>
> ::: versionadded
> 3.15
>
> Use `PyModuleDef.m_name`{.interpreted-text role="c:member"} instead to support previous versions.
> :::

> `Slot ID <PyModuleDef_Slot.slot>`{.interpreted-text role="c:type"} for the docstring of the new module, as a NUL-terminated UTF8-encoded `const char *`.
>
> Usually it is set to a variable created with `PyDoc_STRVAR`{.interpreted-text role="c:macro"}.
>
> ::: versionadded
> 3.15
>
> Use `PyModuleDef.m_doc`{.interpreted-text role="c:member"} instead to support previous versions.
> :::

### Feature slots

> `Slot ID <PyModuleDef_Slot.slot>`{.interpreted-text role="c:type"} whose value points to a `PyABIInfo`{.interpreted-text role="c:struct"} structure describing the ABI that the extension is using.
>
> A suitable `!PyABIInfo`{.interpreted-text role="c:struct"} variable can be defined using the `PyABIInfo_VAR`{.interpreted-text role="c:macro"} macro, as in:
>
> ``` c
> PyABIInfo_VAR(abi_info);
>
> static PyModuleDef_Slot mymodule_slots[] = {
>    {Py_mod_abi, &abi_info},
>    ...
> };
> ```
>
> When creating a module, Python checks the value of this slot using `PyABIInfo_Check`{.interpreted-text role="c:func"}.
>
> ::: versionadded
> 3.15
> :::

> `Slot ID <PyModuleDef_Slot.slot>`{.interpreted-text role="c:type"} whose value is one of:
>
> > The module does not support being imported in subinterpreters.
>
> > The module supports being imported in subinterpreters, but only when they share the main interpreter\'s GIL. (See `isolating-extensions-howto`{.interpreted-text role="ref"}.)
>
> > The module supports being imported in subinterpreters, even when they have their own GIL. (See `isolating-extensions-howto`{.interpreted-text role="ref"}.)
>
> This slot determines whether or not importing this module in a subinterpreter will fail.
>
> If `Py_mod_multiple_interpreters` is not specified, the import machinery defaults to `Py_MOD_MULTIPLE_INTERPRETERS_SUPPORTED`.
>
> ::: versionadded
> 3.12
> :::

> `Slot ID <PyModuleDef_Slot.slot>`{.interpreted-text role="c:type"} whose value is one of:
>
> > The module depends on the presence of the global interpreter lock (GIL), and may access global state without synchronization.
>
> > The module is safe to run without an active GIL.
>
> This slot is ignored by Python builds not configured with `--disable-gil`{.interpreted-text role="option"}. Otherwise, it determines whether or not importing this module will cause the GIL to be automatically enabled. See `whatsnew313-free-threaded-cpython`{.interpreted-text role="ref"} for more detail.
>
> If `Py_mod_gil` is not specified, the import machinery defaults to `Py_MOD_GIL_USED`.
>
> ::: versionadded
> 3.13
> :::

### Creation and initialization slots

> `Slot ID <PyModuleDef_Slot.slot>`{.interpreted-text role="c:type"} for a function that creates the module object itself. The function must have the signature:
>
> The function will be called with:
>
> - *spec*: a `ModuleSpec`-like object, meaning that any attributes defined for `importlib.machinery.ModuleSpec`{.interpreted-text role="py:class"} have matching semantics. However, any of the attributes may be missing.
> - *def*: `NULL`, or the module definition if the module is created from one.
>
> The function should return a new module object, or set an error and return `NULL`.
>
> This function should be kept minimal. In particular, it should not call arbitrary Python code, as trying to import the same module again may result in an infinite loop.
>
> If `Py_mod_create` is not specified, the import machinery will create a normal module object using `PyModule_New`{.interpreted-text role="c:func"}. The name is taken from *spec*, not the definition, to allow extension modules to dynamically adjust to their place in the module hierarchy and be imported under different names through symlinks, all while sharing a single module definition.
>
> There is no requirement for the returned object to be an instance of `PyModule_Type`{.interpreted-text role="c:type"}. However, some slots may only be used with `!PyModule_Type`{.interpreted-text role="c:type"} instances; in particular:
>
> - `Py_mod_exec`{.interpreted-text role="c:macro"},
> - `module state slots <ext-module-state-slots>`{.interpreted-text role="ref"} (`Py_mod_state_*`),
> - `Py_mod_token`{.interpreted-text role="c:macro"}.
>
> ::: versionadded
> 3.5
> :::
>
> ::: versionchanged
> 3.15
>
> The *slots* argument may be a `ModuleSpec`-like object, rather than a true `~importlib.machinery.ModuleSpec`{.interpreted-text role="py:class"} instance. Note that previous versions of CPython did not enforce this.
>
> The *def* argument may now be `NULL`, since modules are not necessarily made from definitions.
> :::

> `Slot ID <PyModuleDef_Slot.slot>`{.interpreted-text role="c:type"} for a function that will `execute`{.interpreted-text role="dfn"}, or initialize, the module. This function does the equivalent to executing the code of a Python module: typically, it adds classes and constants to the module. The signature of the function is:
>
> See the `capi-module-support-functions`{.interpreted-text role="ref"} section for some useful functions to call.
>
> For backwards compatibility, the `PyModuleDef.m_slots`{.interpreted-text role="c:type"} array may contain multiple `!Py_mod_exec`{.interpreted-text role="c:macro"} slots; these are processed in the order they appear in the array. Elsewhere (that is, in arguments to `PyModule_FromSlotsAndSpec`{.interpreted-text role="c:func"} and in return values of `PyModExport_{<name>}`{.interpreted-text role="samp"}), repeating the slot is not allowed.
>
> ::: versionadded
> 3.5
> :::
>
> ::: versionchanged
> 3.15
>
> Repeated `Py_mod_exec` slots are disallowed, except in `PyModuleDef.m_slots`{.interpreted-text role="c:type"}.
> :::

> `Slot ID <PyModuleDef_Slot.slot>`{.interpreted-text role="c:type"} for a table of module-level functions, as an array of `PyMethodDef`{.interpreted-text role="c:type"} values suitable as the *functions* argument to `PyModule_AddFunctions`{.interpreted-text role="c:func"}.
>
> Like other slot IDs, a slots array may only contain one `!Py_mod_methods`{.interpreted-text role="c:macro"} entry. To add functions from multiple `PyMethodDef`{.interpreted-text role="c:type"} arrays, call `PyModule_AddFunctions`{.interpreted-text role="c:func"} in the `Py_mod_exec`{.interpreted-text role="c:macro"} function.
>
> The table must be statically allocated (or otherwise guaranteed to outlive the module object).
>
> ::: versionadded
> 3.15
>
> Use `PyModuleDef.m_methods`{.interpreted-text role="c:member"} instead to support previous versions.
> :::

## Module state {#ext-module-state}

Extension modules can have *module state* \-- a piece of memory that is allocated on module creation, and freed when the module object is deallocated. The module state is specified using `dedicated slots <ext-module-state-slots>`{.interpreted-text role="ref"}.

A typical use of module state is storing an exception type \-- or indeed *any* type object defined by the module \--

Unlike the module\'s Python attributes, Python code cannot replace or delete data stored in module state.

Keeping per-module information in attributes and module state, rather than in static globals, makes module objects *isolated* and safer for use in multiple sub-interpreters. It also helps Python do an orderly clean-up when it shuts down.

Extensions that keep references to Python objects as part of module state must implement `Py_mod_state_traverse`{.interpreted-text role="c:macro"} and `Py_mod_state_clear`{.interpreted-text role="c:macro"} functions to avoid reference leaks.

To retrieve the state from a given module, use the following functions:

> Return the \"state\" of the module, that is, a pointer to the block of memory allocated at module creation time, or `NULL`. See `Py_mod_state_size`{.interpreted-text role="c:macro"}.
>
> On error, return `NULL` with an exception set. Use `PyErr_Occurred`{.interpreted-text role="c:func"} to tell this case apart from missing module state.

> Set *\*result* to the size of *module*\'s state, as specified using `Py_mod_state_size`{.interpreted-text role="c:macro"} (or `PyModuleDef.m_size`{.interpreted-text role="c:member"}), and return 0.
>
> On error, set *\*result* to -1, and return -1 with an exception set.
>
> ::: versionadded
> 3.15
> :::

### Slots for defining module state {#ext-module-state-slots}

The following `PyModuleDef_Slot.slot`{.interpreted-text role="c:member"} IDs are available for defining the module state.

> `Slot ID <PyModuleDef_Slot.slot>`{.interpreted-text role="c:type"} for the size of the module state, in bytes.
>
> Setting the value to a non-negative value means that the module can be re-initialized and specifies the additional amount of memory it requires for its state.
>
> See [PEP 3121](http://www.python.org/dev/peps/pep-3121/ "PEP 3121") for more details.
>
> Use `PyModule_GetStateSize`{.interpreted-text role="c:func"} to retrieve the size of a given module.
>
> ::: versionadded
> 3.15
>
> Use `PyModuleDef.m_size`{.interpreted-text role="c:member"} instead to support previous versions.
> :::

> `Slot ID <PyModuleDef_Slot.slot>`{.interpreted-text role="c:type"} for a traversal function to call during GC traversal of the module object.
>
> The signature of the function, and meanings of the arguments, is similar as for `PyTypeObject.tp_traverse`{.interpreted-text role="c:member"}:
>
> This function is not called if the module state was requested but is not allocated yet. This is the case immediately after the module is created and before the module is executed (`Py_mod_exec`{.interpreted-text role="c:data"} function). More precisely, this function is not called if the state size (`Py_mod_state_size`{.interpreted-text role="c:data"}) is greater than 0 and the module state (as returned by `PyModule_GetState`{.interpreted-text role="c:func"}) is `NULL`.
>
> ::: versionadded
> 3.15
>
> Use `PyModuleDef.m_size`{.interpreted-text role="c:member"} instead to support previous versions.
> :::

> `Slot ID <PyModuleDef_Slot.slot>`{.interpreted-text role="c:type"} for a clear function to call during GC clearing of the module object.
>
> The signature of the function is:
>
> This function is not called if the module state was requested but is not allocated yet. This is the case immediately after the module is created and before the module is executed (`Py_mod_exec`{.interpreted-text role="c:data"} function). More precisely, this function is not called if the state size (`Py_mod_state_size`{.interpreted-text role="c:data"}) is greater than 0 and the module state (as returned by `PyModule_GetState`{.interpreted-text role="c:func"}) is `NULL`.
>
> Like `PyTypeObject.tp_clear`{.interpreted-text role="c:member"}, this function is not *always* called before a module is deallocated. For example, when reference counting is enough to determine that an object is no longer used, the cyclic garbage collector is not involved and the `Py_mod_state_free`{.interpreted-text role="c:macro"} function is called directly.
>
> ::: versionadded
> 3.15
>
> Use `PyModuleDef.m_clear`{.interpreted-text role="c:member"} instead to support previous versions.
> :::

> `Slot ID <PyModuleDef_Slot.slot>`{.interpreted-text role="c:type"} for a function to call during deallocation of the module object.
>
> The signature of the function is:
>
> This function is not called if the module state was requested but is not allocated yet. This is the case immediately after the module is created and before the module is executed (`Py_mod_exec`{.interpreted-text role="c:data"} function). More precisely, this function is not called if the state size (`Py_mod_state_size`{.interpreted-text role="c:data"}) is greater than 0 and the module state (as returned by `PyModule_GetState`{.interpreted-text role="c:func"}) is `NULL`.
>
> ::: versionadded
> 3.15
>
> Use `PyModuleDef.m_free`{.interpreted-text role="c:member"} instead to support previous versions.
> :::

### Module token {#ext-module-token}

Each module may have an associated *token*: a pointer-sized value intended to identify of the module state\'s memory layout. This means that if you have a module object, but you are not sure if it "belongs" to your extension, you can check using code like this:

``` c
PyObject *module = <the module in question>

void *module_token;
if (PyModule_GetToken(module, &module_token) < 0) {
    return NULL;
}
if (module_token != your_token) {
    PyErr_SetString(PyExc_ValueError, "unexpected module")
    return NULL;
}

// This module's state has the expected memory layout; it's safe to cast
struct my_state state = (struct my_state*)PyModule_GetState(module)
```

A module\'s token \-- and the *your_token* value to use in the above code \-- is:

- For modules created with `PyModuleDef`{.interpreted-text role="c:type"}: the address of that `PyModuleDef`{.interpreted-text role="c:type"};
- For modules defined with the `Py_mod_token`{.interpreted-text role="c:macro"} slot: the value of that slot;
- For modules created from an `PyModExport_*` `export hook <extension-export-hook>`{.interpreted-text role="ref"}: the slots array that the export hook returned (unless overridden with `Py_mod_token`{.interpreted-text role="c:macro"}).

> `Slot ID <PyModuleDef_Slot.slot>`{.interpreted-text role="c:type"} for the module token.
>
> If you use this slot to set the module token (rather than rely on the default), you must ensure that:
>
> - The pointer outlives the class, so it\'s not reused for something else while the class exists.
> - It \"belongs\" to the extension module where the class lives, so it will not clash with other extensions.
> - If the token points to a `PyModuleDef`{.interpreted-text role="c:type"} struct, the module should behave as if it was created from that `PyModuleDef`{.interpreted-text role="c:type"}. In particular, the module state must have matching layout and semantics.
>
> Modules created from `PyModuleDef`{.interpreted-text role="c:type"} always use the address of the `PyModuleDef`{.interpreted-text role="c:type"} as the token. This means that `!Py_mod_token`{.interpreted-text role="c:macro"} cannot be used in `PyModuleDef.m_slots`{.interpreted-text role="c:member"}.
>
> ::: versionadded
> 3.15
> :::

> Set *\*result* to the module token for *module* and return 0.
>
> On error, set *\*result* to NULL, and return -1 with an exception set.
>
> ::: versionadded
> 3.15
> :::

See also `PyType_GetModuleByToken`{.interpreted-text role="c:func"}.

## Creating extension modules dynamically {#module-from-slots}

The following functions may be used to create an extension module dynamically, rather than from an extension\'s `export hook <extension-export-hook>`{.interpreted-text role="ref"}.

> Create a new module object, given an array of `slots <pymoduledef_slot>`{.interpreted-text role="ref"} and the `~importlib.machinery.ModuleSpec`{.interpreted-text role="py:class"} *spec*.
>
> The *slots* argument must point to an array of `PyModuleDef_Slot`{.interpreted-text role="c:type"} structures, terminated by an entry slot with slot ID of 0 (typically written as `{0}` or `{0, NULL}` in C). The *slots* argument may not be `NULL`.
>
> The *spec* argument may be any `ModuleSpec`-like object, as described in `Py_mod_create`{.interpreted-text role="c:macro"} documentation. Currently, the *spec* must have a `name` attribute.
>
> On success, return the new module. On error, return `NULL` with an exception set.
>
> Note that this does not process the module\'s execution slot (`Py_mod_exec`{.interpreted-text role="c:data"}). Both `!PyModule_FromSlotsAndSpec`{.interpreted-text role="c:func"} and `PyModule_Exec`{.interpreted-text role="c:func"} must be called to fully initialize a module. (See also `multi-phase-initialization`{.interpreted-text role="ref"}.)
>
> The *slots* array only needs to be valid for the duration of the `!PyModule_FromSlotsAndSpec`{.interpreted-text role="c:func"} call. In particular, it may be heap-allocated.
>
> ::: versionadded
> 3.15
> :::

> Execute the `Py_mod_exec`{.interpreted-text role="c:data"} slot(s) of *module*.
>
> On success, return 0. On error, return -1 with an exception set.
>
> For clarity: If *module* has no slots, for example if it uses `legacy single-phase initialization <single-phase-initialization>`{.interpreted-text role="ref"}, this function does nothing and returns 0.
>
> ::: versionadded
> 3.15
> :::

## Module definition struct {#pymoduledef}

Traditionally, extension modules were defined using a *module definition* as the "description\" of how a module should be created. Rather than using an array of `slots <pymoduledef_slot>`{.interpreted-text role="ref"} directly, the definition has dedicated members for most common functionality, and allows additional slots as an extension mechanism.

This way of defining modules is still available and there are no plans to remove it.

> The module definition struct, which holds information needed to create a module object.
>
> This structure must be statically allocated (or be otherwise guaranteed to be valid while any modules created from it exist). Usually, there is only one variable of this type for each extension module defined this way.
>
> > Always initialize this member to `PyModuleDef_HEAD_INIT`{.interpreted-text role="c:macro"}:
> >
> > > The type of `!PyModuleDef.m_base`{.interpreted-text role="c:member"}.
> >
> > > The required initial value for `!PyModuleDef.m_base`{.interpreted-text role="c:member"}.
>
> > Corresponds to the `Py_mod_name`{.interpreted-text role="c:macro"} slot.
>
> > These members correspond to the `Py_mod_doc`{.interpreted-text role="c:macro"} slot. Setting this to NULL is equivalent to omitting the slot.
>
> > Corresponds to the `Py_mod_state_size`{.interpreted-text role="c:macro"} slot. Setting this to zero is equivalent to omitting the slot.
> >
> > When using `legacy single-phase initialization <single-phase-initialization>`{.interpreted-text role="ref"} or when creating modules dynamically using `PyModule_Create`{.interpreted-text role="c:func"} or `PyModule_Create2`{.interpreted-text role="c:func"}, `!m_size`{.interpreted-text role="c:member"} may be set to -1. This indicates that the module does not support sub-interpreters, because it has global state.
>
> > Corresponds to the `Py_mod_methods`{.interpreted-text role="c:macro"} slot. Setting this to NULL is equivalent to omitting the slot.
>
> > An array of additional slots, terminated by a `{0, NULL}` entry.
> >
> > If the array contains slots corresponding to `PyModuleDef`{.interpreted-text role="c:type"} members, the values must match. For example, if you use `Py_mod_name`{.interpreted-text role="c:macro"} in `!m_slots`{.interpreted-text role="c:member"}, `PyModuleDef.m_name`{.interpreted-text role="c:member"} must be set to the same pointer (not just an equal string).
> >
> > ::: versionchanged
> > 3.5
> >
> > Prior to version 3.5, this member was always set to `NULL`, and was defined as:
> >
> > > 
> > :::

> The type of `PyModuleDef` objects.

::: {#moduledef-dynamic}
The following API can be used to create modules from a `!PyModuleDef`{.interpreted-text role="c:type"} struct:
:::

> Create a new module object, given the definition in *def*. This is a macro that calls `PyModule_Create2`{.interpreted-text role="c:func"} with *module_api_version* set to `PYTHON_API_VERSION`{.interpreted-text role="c:macro"}, or to `PYTHON_ABI_VERSION`{.interpreted-text role="c:macro"} if using the `limited API <limited-c-api>`{.interpreted-text role="ref"}.

> Create a new module object, given the definition in *def*, assuming the API version *module_api_version*. If that version does not match the version of the running interpreter, a `RuntimeWarning`{.interpreted-text role="exc"} is emitted.
>
> Return `NULL` with an exception set on error.
>
> This function does not support slots. The `~PyModuleDef.m_slots`{.interpreted-text role="c:member"} member of *def* must be `NULL`.
>
> :::: note
> ::: title
> Note
> :::
>
> Most uses of this function should be using `PyModule_Create`{.interpreted-text role="c:func"} instead; only use this if you are sure you need it.
> ::::

> This macro calls `PyModule_FromDefAndSpec2`{.interpreted-text role="c:func"} with *module_api_version* set to `PYTHON_API_VERSION`{.interpreted-text role="c:macro"}, or to `PYTHON_ABI_VERSION`{.interpreted-text role="c:macro"} if using the `limited API <limited-c-api>`{.interpreted-text role="ref"}.
>
> ::: versionadded
> 3.5
> :::

> Create a new module object, given the definition in *def* and the ModuleSpec *spec*, assuming the API version *module_api_version*. If that version does not match the version of the running interpreter, a `RuntimeWarning`{.interpreted-text role="exc"} is emitted.
>
> Return `NULL` with an exception set on error.
>
> Note that this does not process execution slots (`Py_mod_exec`{.interpreted-text role="c:data"}). Both `PyModule_FromDefAndSpec` and `PyModule_ExecDef` must be called to fully initialize a module.
>
> :::: note
> ::: title
> Note
> :::
>
> Most uses of this function should be using `PyModule_FromDefAndSpec`{.interpreted-text role="c:func"} instead; only use this if you are sure you need it.
> ::::
>
> ::: versionadded
> 3.5
> :::

> Process any execution slots (`Py_mod_exec`{.interpreted-text role="c:data"}) given in *def*.
>
> ::: versionadded
> 3.5
> :::

## Support functions {#capi-module-support-functions}

The following functions are provided to help initialize a module object. They are intended for a module\'s execution slot (`Py_mod_exec`{.interpreted-text role="c:data"}), the initialization function for legacy `single-phase initialization <single-phase-initialization>`{.interpreted-text role="ref"}, or code that creates modules dynamically.

> Add an object to *module* as *name*. This is a convenience function which can be used from the module\'s initialization function.
>
> On success, return `0`. On error, raise an exception and return `-1`.
>
> Example usage:
>
> ``` c
> static int
> add_spam(PyObject *module, int value)
> {
>     PyObject *obj = PyLong_FromLong(value);
>     if (obj == NULL) {
>         return -1;
>     }
>     int res = PyModule_AddObjectRef(module, "spam", obj);
>     Py_DECREF(obj);
>     return res;
>  }
> ```
>
> To be convenient, the function accepts `NULL` *value* with an exception set. In this case, return `-1` and just leave the raised exception unchanged.
>
> The example can also be written without checking explicitly if *obj* is `NULL`:
>
> ``` c
> static int
> add_spam(PyObject *module, int value)
> {
>     PyObject *obj = PyLong_FromLong(value);
>     int res = PyModule_AddObjectRef(module, "spam", obj);
>     Py_XDECREF(obj);
>     return res;
>  }
> ```
>
> Note that `Py_XDECREF()` should be used instead of `Py_DECREF()` in this case, since *obj* can be `NULL`.
>
> The number of different *name* strings passed to this function should be kept small, usually by only using statically allocated strings as *name*. For names that aren\'t known at compile time, prefer calling `PyUnicode_FromString`{.interpreted-text role="c:func"} and `PyObject_SetAttr`{.interpreted-text role="c:func"} directly. For more details, see `PyUnicode_InternFromString`{.interpreted-text role="c:func"}, which may be used internally to create a key object.
>
> ::: versionadded
> 3.10
> :::

> Similar to `PyModule_AddObjectRef`{.interpreted-text role="c:func"}, but \"steals\" a reference to *value*. It can be called with a result of function that returns a new reference without bothering to check its result or even saving it to a variable.
>
> Example usage:
>
> ``` c
> if (PyModule_Add(module, "spam", PyBytes_FromString(value)) < 0) {
>     goto error;
> }
> ```
>
> ::: versionadded
> 3.13
> :::

> Similar to `PyModule_AddObjectRef`{.interpreted-text role="c:func"}, but steals a reference to *value* on success (if it returns `0`).
>
> The new `PyModule_Add`{.interpreted-text role="c:func"} or `PyModule_AddObjectRef`{.interpreted-text role="c:func"} functions are recommended, since it is easy to introduce reference leaks by misusing the `PyModule_AddObject`{.interpreted-text role="c:func"} function.
>
> :::: note
> ::: title
> Note
> :::
>
> Unlike other functions that steal references, `PyModule_AddObject()` only releases the reference to *value* **on success**.
>
> This means that its return value must be checked, and calling code must `Py_XDECREF`{.interpreted-text role="c:func"} *value* manually on error.
> ::::
>
> Example usage:
>
> ``` c
> PyObject *obj = PyBytes_FromString(value);
> if (PyModule_AddObject(module, "spam", obj) < 0) {
>     // If 'obj' is not NULL and PyModule_AddObject() failed,
>     // 'obj' strong reference must be deleted with Py_XDECREF().
>     // If 'obj' is NULL, Py_XDECREF() does nothing.
>     Py_XDECREF(obj);
>     goto error;
> }
> // PyModule_AddObject() stole a reference to obj:
> // Py_XDECREF(obj) is not needed here.
> ```
>
> ::: deprecated
> 3.13
>
> `PyModule_AddObject`{.interpreted-text role="c:func"} is `soft deprecated`{.interpreted-text role="term"}.
> :::

> Add an integer constant to *module* as *name*. This convenience function can be used from the module\'s initialization function. Return `-1` with an exception set on error, `0` on success.
>
> This is a convenience function that calls `PyLong_FromLong`{.interpreted-text role="c:func"} and `PyModule_AddObjectRef`{.interpreted-text role="c:func"}; see their documentation for details.

> Add a string constant to *module* as *name*. This convenience function can be used from the module\'s initialization function. The string *value* must be `NULL`-terminated. Return `-1` with an exception set on error, `0` on success.
>
> This is a convenience function that calls `PyUnicode_InternFromString`{.interpreted-text role="c:func"} and `PyModule_AddObjectRef`{.interpreted-text role="c:func"}; see their documentation for details.

> Add an int constant to *module*. The name and the value are taken from *macro*. For example `PyModule_AddIntMacro(module, AF_INET)` adds the int constant *AF_INET* with the value of *AF_INET* to *module*. Return `-1` with an exception set on error, `0` on success.

> Add a string constant to *module*.

> Add a type object to *module*. The type object is finalized by calling internally `PyType_Ready`{.interpreted-text role="c:func"}. The name of the type object is taken from the last component of `~PyTypeObject.tp_name`{.interpreted-text role="c:member"} after dot. Return `-1` with an exception set on error, `0` on success.
>
> ::: versionadded
> 3.9
> :::

> Add the functions from the `NULL` terminated *functions* array to *module*. Refer to the `PyMethodDef`{.interpreted-text role="c:type"} documentation for details on individual entries (due to the lack of a shared module namespace, module level \"functions\" implemented in C typically receive the module as their first parameter, making them similar to instance methods on Python classes).
>
> This function is called automatically when creating a module from `PyModuleDef` (such as when using `multi-phase-initialization`{.interpreted-text role="ref"}, `PyModule_Create`, or `PyModule_FromDefAndSpec`). Some module authors may prefer defining functions in multiple `PyMethodDef`{.interpreted-text role="c:type"} arrays; in that case they should call this function directly.
>
> The *functions* array must be statically allocated (or otherwise guaranteed to outlive the module object).
>
> ::: versionadded
> 3.5
> :::

> Set the docstring for *module* to *docstring*. This function is called automatically when creating a module from `PyModuleDef` (such as when using `multi-phase-initialization`{.interpreted-text role="ref"}, `PyModule_Create`, or `PyModule_FromDefAndSpec`).
>
> Return `0` on success. Return `-1` with an exception set on error.
>
> ::: versionadded
> 3.5
> :::

> Indicate that *module* does or does not support running without the global interpreter lock (GIL), using one of the values from `Py_mod_gil`{.interpreted-text role="c:macro"}. It must be called during *module*\'s initialization function when using `single-phase-initialization`{.interpreted-text role="ref"}. If this function is not called during module initialization, the import machinery assumes the module does not support running without the GIL. This function is only available in Python builds configured with `--disable-gil`{.interpreted-text role="option"}. Return `-1` with an exception set on error, `0` on success.
>
> ::: versionadded
> 3.13
> :::

### Module lookup (single-phase initialization)

The legacy `single-phase initialization <single-phase-initialization>`{.interpreted-text role="ref"} initialization scheme creates singleton modules that can be looked up in the context of the current interpreter. This allows the module object to be retrieved later with only a reference to the module definition.

These functions will not work on modules created using multi-phase initialization, since multiple such modules can be created from a single definition.

> Returns the module object that was created from *def* for the current interpreter. This method requires that the module object has been attached to the interpreter state with `PyState_AddModule`{.interpreted-text role="c:func"} beforehand. In case the corresponding module object is not found or has not been attached to the interpreter state yet, it returns `NULL`.

> Attaches the module object passed to the function to the interpreter state. This allows the module object to be accessible via `PyState_FindModule`{.interpreted-text role="c:func"}.
>
> Only effective on modules created using single-phase initialization.
>
> Python calls `PyState_AddModule` automatically after importing a module that uses `single-phase initialization <single-phase-initialization>`{.interpreted-text role="ref"}, so it is unnecessary (but harmless) to call it from module initialization code. An explicit call is needed only if the module\'s own init code subsequently calls `PyState_FindModule`. The function is mainly intended for implementing alternative import mechanisms (either by calling it directly, or by referring to its implementation for details of the required state updates).
>
> If a module was attached previously using the same *def*, it is replaced by the new *module*.
>
> The caller must have an `attached thread state`{.interpreted-text role="term"}.
>
> Return `-1` with an exception set on error, `0` on success.
>
> ::: versionadded
> 3.3
> :::

> Removes the module object created from *def* from the interpreter state. Return `-1` with an exception set on error, `0` on success.
>
> The caller must have an `attached thread state`{.interpreted-text role="term"}.
>
> ::: versionadded
> 3.3
> :::
